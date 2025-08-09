"""
GPU-ready YOLOv8 training script using ultralytics Python API.
Supports: mixed precision, resume, multi-gpu via torchrun, wandb logging (optional).
Usage single-GPU:
  python ml/train_yolov8.py --data ml/data.yaml --img 640 --batch 16 --epochs 100 --weights yolov8n.pt --project runs/whirly --name exp1 --amp

Multi-GPU (4 GPUs):
  torchrun --nproc_per_node=4 ml/train_yolov8.py --data ml/data.yaml --img 640 --batch 16 --epochs 100 --weights yolov8n.pt --project runs/whirly_multi --amp
"""
import argparse, os
from ultralytics import YOLO

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--data', required=True, help='path to data.yaml')
    p.add_argument('--img', type=int, default=640)
    p.add_argument('--batch', type=int, default=16)
    p.add_argument('--epochs', type=int, default=100)
    p.add_argument('--weights', default='yolov8n.pt', help='initial weights (yolov8n.pt / yolov8s.pt / custom)')
    p.add_argument('--project', default='runs/whirly', help='save dir')
    p.add_argument('--name', default=None, help='experiment name (appended to project)')
    p.add_argument('--resume', action='store_true', help='resume if checkpoint exists')
    p.add_argument('--device', default=None, help='cuda device (e.g., 0) or cpu')
    p.add_argument('--amp', action='store_true', help='enable mixed precision')
    p.add_argument('--patience', type=int, default=50, help='early stopping patience')
    p.add_argument('--workers', type=int, default=8)
    p.add_argument('--verbose', action='store_true')
    p.add_argument('--wandb', action='store_true', help='use wandb logging')
    return p.parse_args()

def main():
    args = parse_args()
    model = YOLO(args.weights)
    train_kwargs = dict(
        data=args.data,
        imgsz=args.img,
        epochs=args.epochs,
        batch=args.batch,
        project=args.project,
        name=args.name,
        workers=args.workers,
        device=args.device,
        patience=args.patience,
        exist_ok=True,
    )
    if args.amp:
        train_kwargs['mixed_precision'] = 'fp16'
    if args.wandb:
        os.environ['WANDB_PROJECT'] = args.project
    if args.verbose:
        print("Training YOLOv8 with options:", train_kwargs)
    model.train(**train_kwargs)
    print("Training finished. Check results folder under", args.project)

if __name__ == '__main__':
    main()