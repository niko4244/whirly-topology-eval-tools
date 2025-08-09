# coco_to_d2.py - utility for converting COCO to Detectron2 format if needed
import json
import sys

def convert_coco_to_d2(coco_json, images_root, out_json):
    from d2.dataset import load_whirly_coco
    dataset = load_whirly_coco(coco_json, images_root)
    with open(out_json, "w") as f:
        json.dump(dataset, f)
    print(f"Wrote Detectron2-style dataset to {out_json}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--coco", required=True)
    parser.add_argument("--images_root", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    convert_coco_to_d2(args.coco, args.images_root, args.out)