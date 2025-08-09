# Usage: python tools/coco_to_yolo.py --coco /path/to/instances_train.json --images /path/to/images --out /out/labels
import json, os, argparse
from pathlib import Path

def convert(coco_json, images_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    with open(coco_json) as f:
        coco = json.load(f)
    imgs = {im['id']: im for im in coco['images']}
    for ann in coco['annotations']:
        img = imgs[ann['image_id']]
        fname = Path(img['file_name']).stem + '.txt'
        w = img['width']; h = img['height']
        bbox = ann['bbox']  # x,y,width,height (COCO)
        x, y, bw, bh = bbox
        cx = x + bw/2.0
        cy = y + bh/2.0
        cx /= w; cy /= h; bw /= w; bh /= h
        cls_id = ann.get('category_id', 0)
        with open(Path(out_dir)/fname, 'a') as fo:
            fo.write(f"{cls_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}\n")

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--coco', required=True)
    p.add_argument('--images', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    convert(args.coco, args.images, args.out)