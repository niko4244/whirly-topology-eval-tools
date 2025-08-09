import argparse
from simple_svg_synth import generate_one
import os, json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, default='out')
    parser.add_argument('--n', type=int, default=100)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()

    import random, numpy as np
    random.seed(args.seed); np.random.seed(args.seed)
    coco = {'images':[], 'annotations':[], 'categories':[
        {'id':1,'name':'resistor'},{'id':2,'name':'capacitor'},{'id':3,'name':'wire'}]}
    ann_id = 1
    for i in range(args.n):
        img_meta, anns = generate_one(args.out, i, width=1024, height=768, augment_cfg={'blur_p':0.4, 'noise_p':0.5})
        coco['images'].append(img_meta)
        for a in anns:
            a['id'] = ann_id; ann_id += 1
            coco['annotations'].append(a)
    with open(os.path.join(args.out, 'instances.json'), 'w') as f:
        json.dump(coco, f)