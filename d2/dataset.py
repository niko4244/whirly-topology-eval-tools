# dataset.py - Detectron2 dataset registration for Whirly COCO
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.structures import BoxMode
import json, os

def load_whirly_coco(json_file, images_root):
    with open(json_file) as f:
        coco = json.load(f)
    images = {img['id']: img for img in coco['images']}
    annos_by_image = {}
    for ann in coco['annotations']:
        annos_by_image.setdefault(ann['image_id'], []).append(ann)
    dataset = []
    for img_id, img in images.items():
        record = {
            'file_name': os.path.join(images_root, img['file_name']),
            'image_id': img['id'],
            'height': img['height'],
            'width': img['width'],
            'annotations': []
        }
        for ann in annos_by_image.get(img_id, []):
            record['annotations'].append({
                "bbox": ann['bbox'],
                "bbox_mode": BoxMode.XYWH_ABS,
                "category_id": ann['category_id'] - 1,
                "segmentation": ann.get('segmentation', []),
                "whirly_meta": ann.get('whirly_meta', {})
            })
        dataset.append(record)
    return dataset

def register_whirly_datasets():
    DatasetCatalog.register(
        "whirly_train",
        lambda: load_whirly_coco("datasets/instances_train.json", "datasets/images")
    )
    DatasetCatalog.register(
        "whirly_val",
        lambda: load_whirly_coco("datasets/instances_val.json", "datasets/images")
    )
    MetadataCatalog.get("whirly_train").set(thing_classes=['resistor','capacitor','wire'])
    MetadataCatalog.get("whirly_val").set(thing_classes=['resistor','capacitor','wire'])