# File: train_maskrcnn_whirly.py
# Usage (single GPU):
#   python train_maskrcnn_whirly.py --data_root /path/to/data --output_dir /path/to/out --epochs 50 --batch_size 2
# Usage (distributed multi-gpu):
#   torchrun --nproc_per_node=4 train_maskrcnn_whirly.py --data_root /... --output_dir /...

import os
import argparse
from pathlib import Path

import torch
import torch.utils.data
import torchvision
from torchvision.models.detection import maskrcnn_resnet50_fpn
from torchvision.transforms import functional as F

import albumentations as A
from albumentations.pytorch import ToTensorV2
from pycocotools.coco import COCO
from PIL import Image
import numpy as np

# ----------------------------
# Dataset: COCO-style wrapper
# ----------------------------
class CocoInstanceDataset(torch.utils.data.Dataset):
    def __init__(self, root, annFile, transforms=None):
        self.root = root
        self.coco = COCO(annFile)
        self.ids = list(sorted(self.coco.imgs.keys()))
        self.transforms = transforms

    def __getitem__(self, index):
        img_id = self.ids[index]
        img_info = self.coco.loadImgs(img_id)[0]
        path = os.path.join(self.root, img_info['file_name'])
        img = np.array(Image.open(path).convert("RGB"))

        ann_ids = self.coco.getAnnIds(imgIds=img_id)
        anns = self.coco.loadAnns(ann_ids)

        masks = []
        boxes = []
        labels = []
        areas = []
        iscrowd = []

        for ann in anns:
            mask = self.coco.annToMask(ann)  # HxW binary
            if mask.sum() == 0:
                continue
            masks.append(mask)
            bbox = ann['bbox']
            boxes.append([bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]])
            labels.append(ann['category_id'])
            areas.append(ann.get('area', bbox[2] * bbox[3]))
            iscrowd.append(ann.get('iscrowd', 0))

        if len(boxes) == 0:
            boxes = torch.zeros((0, 4), dtype=torch.float32)
            labels = torch.as_tensor([], dtype=torch.int64)
            masks = torch.zeros((0, img.shape[0], img.shape[1]), dtype=torch.uint8)
            areas = torch.as_tensor([], dtype=torch.float32)
            iscrowd = torch.as_tensor([], dtype=torch.uint8)
        else:
            boxes = torch.as_tensor(boxes, dtype=torch.float32)
            labels = torch.as_tensor(labels, dtype=torch.int64)
            masks = torch.as_tensor(np.stack(masks, axis=0), dtype=torch.uint8)
            areas = torch.as_tensor(areas, dtype=torch.float32)
            iscrowd = torch.as_tensor(iscrowd, dtype=torch.uint8)

        target = {
            "boxes": boxes,
            "labels": labels,
            "masks": masks,
            "image_id": torch.tensor([img_id]),
            "area": areas,
            "iscrowd": iscrowd,
        }

        if self.transforms:
            augmented = self.transforms(image=img, masks=[m.numpy() for m in masks] if len(masks) else None)
            img = augmented['image']
            if masks is not None and augmented.get('masks') is not None:
                new_masks = np.stack(augmented['masks']).astype(np.uint8) if len(augmented['masks']) else np.zeros((0, img.shape[1], img.shape[2]), dtype=np.uint8)
                target['masks'] = torch.as_tensor(new_masks)
        else:
            img = F.to_tensor(Image.fromarray(img))

        return img, target

    def __len__(self):
        return len(self.ids)

def collate_fn(batch):
    return tuple(zip(*batch))

def train_one_epoch(model, optimizer, data_loader, device, epoch, scaler=None, print_freq=50):
    model.train()
    running_loss = 0.0
    for i, (images, targets) in enumerate(data_loader):
        images = list(img.to(device) for img in images)
        targets = [{k: v.to(device) if isinstance(v, torch.Tensor) else v for k, v in t.items()} for t in targets]

        with torch.cuda.amp.autocast(enabled=(scaler is not None)):
            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        if scaler:
            scaler.scale(losses).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            losses.backward()
            optimizer.step()

        running_loss += losses.item()
        if (i + 1) % print_freq == 0:
            avg = running_loss / (i + 1)
            print(f"[Epoch {epoch}] Iter {i+1}/{len(data_loader)} — avg loss: {avg:.4f}")

    return running_loss / len(data_loader)

def get_data_transforms():
    return A.Compose([
        A.LongestMaxSize(max_size=1024),
        A.PadIfNeeded(min_height=1024, min_width=1024, border_mode=0),
        A.RandomBrightnessContrast(p=0.5),
        A.GaussNoise(p=0.2),
        ToTensorV2()
    ], bbox_params=A.BboxParams(format='pascal_voc', label_fields=[]))

def main(args):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    print("Device:", device)

    train_ann = os.path.join(args.data_root, "annotations", "instances_train.json")
    val_ann = os.path.join(args.data_root, "annotations", "instances_val.json")
    train_img_root = os.path.join(args.data_root, "images")

    transforms = get_data_transforms()

    dataset = CocoInstanceDataset(train_img_root, train_ann, transforms=transforms)
    dataset_val = CocoInstanceDataset(train_img_root, val_ann, transforms=get_data_transforms())

    train_sampler = torch.utils.data.RandomSampler(dataset)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=args.batch_size, sampler=train_sampler,
                                              num_workers=args.num_workers, collate_fn=collate_fn)

    num_classes = args.num_classes  # background + N classes
    model = maskrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, num_classes)

    mask_in_features = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    model.roi_heads.mask_predictor = torchvision.models.detection.mask_rcnn.MaskRCNNPredictor(mask_in_features, hidden_layer, num_classes)

    model.to(device)

    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=args.lr, momentum=0.9, weight_decay=0.0005)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=8, gamma=0.1)

    scaler = torch.cuda.amp.GradScaler() if args.amp else None

    start_epoch = 0
    best_loss = float('inf')

    for epoch in range(start_epoch, args.epochs):
        train_loss = train_one_epoch(model, optimizer, data_loader, device, epoch, scaler=scaler, print_freq=50)
        lr_scheduler.step()
        ckpt_dir = Path(args.output_dir)
        ckpt_dir.mkdir(parents=True, exist_ok=True)
        ckpt_path = ckpt_dir / f"maskrcnn_epoch{epoch+1}.pt"
        torch.save({'epoch': epoch+1, 'model_state_dict': model.state_dict(), 'optimizer_state_dict': optimizer.state_dict()}, ckpt_path)
        print(f"Saved checkpoint: {ckpt_path}")

    print("Training complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Mask R-CNN for Whirly")
    parser.add_argument("--data_root", required=True, type=str, help="Path to dataset root")
    parser.add_argument("--output_dir", default="./checkpoints", type=str)
    parser.add_argument("--epochs", default=20, type=int)
    parser.add_argument("--batch_size", default=2, type=int)
    parser.add_argument("--num_workers", default=4, type=int)
    parser.add_argument("--lr", default=0.005, type=float)
    parser.add_argument("--num_classes", default=10, type=int, help="Including background")
    parser.add_argument("--amp", action="store_true", help="Enable mixed precision")
    args = parser.parse_args()
    main(args)