import os, json, argparse, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
import svgwrite
import cairosvg
from pycocotools import mask as maskUtils
from io import BytesIO

# -----------------------
# Utility: draw component
# -----------------------
def draw_resistor(dwg, x, y, length=80, height=20, id='r1', stroke='#000', stroke_width=2):
    g = dwg.g(id=id, **{'data-class':'resistor'})
    pts = []
    segments = 6
    seg_len = length / segments
    for i in range(segments+1):
        pts.append((x + i*seg_len, y + ( (i%2)*height - height/2 )))
    g.add(dwg.polyline(points=pts, fill='none', stroke=stroke, stroke_width=stroke_width))
    g.add(dwg.line(start=(x - 10, y), end=(x, y), stroke=stroke, stroke_width=stroke_width))
    g.add(dwg.line(start=(x+length, y), end=(x+length+10, y), stroke=stroke, stroke_width=stroke_width))
    dwg.add(g)
    return dict(id=id, bbox=[x-10, y-height/2, x+length+10, y+height/2])

def draw_capacitor(dwg, x, y, id='c1', stroke='#000', stroke_width=2):
    g = dwg.g(id=id, **{'data-class':'capacitor'})
    g.add(dwg.line(start=(x, y-12), end=(x, y+12), stroke=stroke, stroke_width=stroke_width))
    g.add(dwg.line(start=(x+12, y-12), end=(x+12, y+12), stroke=stroke, stroke_width=stroke_width))
    g.add(dwg.line(start=(x-10, y), end=(x, y), stroke=stroke, stroke_width=stroke_width))
    g.add(dwg.line(start=(x+12, y), end=(x+22, y), stroke=stroke, stroke_width=stroke_width))
    dwg.add(g)
    return dict(id=id, bbox=[x-10, y-12, x+22, y+12])

def draw_wire(dwg, pts, id='w1', stroke='#000', stroke_width=2, dash=False):
    g = dwg.g(id=id, **{'data-class':'wire'})
    if dash:
        g.add(dwg.polyline(points=pts, fill='none', stroke=stroke, stroke_width=stroke_width, stroke_dasharray=[4,4]))
    else:
        g.add(dwg.polyline(points=pts, fill='none', stroke=stroke, stroke_width=stroke_width))
    dwg.add(g)
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return dict(id=id, bbox=[min(xs), min(ys), max(xs), max(ys)])

def svg_to_png_bytes(svg_text, output_w, output_h, scale=1.0):
    png_bytes = cairosvg.svg2png(bytestring=svg_text.encode('utf-8'), output_width=output_w, output_height=output_h)
    return png_bytes

def augment_image_pil(img: Image.Image, cfg):
    if random.random() < cfg.get('blur_p', 0.3):
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3, 1.8)))
    if random.random() < cfg.get('rotate_p', 0.2):
        angle = random.uniform(-6, 6)
        img = img.rotate(angle, expand=False, fillcolor=(255,255,255))
    if random.random() < cfg.get('noise_p', 0.4):
        arr = np.array(img).astype(np.float32)
        noise = np.random.normal(scale=cfg.get('noise_sigma', 8), size=arr.shape)
        arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(arr)
    return img

def make_coco_annotation(ann_id, img_id, bbox, category_id):
    x1, y1, x2, y2 = bbox
    w = x2 - x1; h = y2 - y1
    area = w*h
    return dict(id=ann_id, image_id=img_id, category_id=category_id, bbox=[x1,y1,w,h], area=area, iscrowd=0, segmentation=[])

def generate_one(out_dir, idx, width=1024, height=768, augment_cfg=None):
    dwg = svgwrite.Drawing(size=(width, height))
    dwg.add(dwg.rect(insert=(0,0), size=(width, height), fill='white'))
    x1 = random.randint(80, width//2 - 100)
    y1 = random.randint(80, height-80)
    rmeta = draw_resistor(dwg, x1, y1, length=random.randint(60, 120), id=f"r_{idx}")
    x2 = random.randint(width//2 + 20, width - 160)
    y2 = random.randint(80, height-80)
    cmeta = draw_capacitor(dwg, x2, y2, id=f"c_{idx}")
    pts = [(rmeta['bbox'][2], (y1)), ((x1+x2)//2, (y1+y2)//2), (cmeta['bbox'][0], (y2))]
    wmeta = draw_wire(dwg, pts, id=f"w_{idx}")

    svg_text = dwg.tostring()
    png_bytes = svg_to_png_bytes(svg_text, width, height)
    img = Image.open(BytesIO(png_bytes)).convert("RGB")
    if augment_cfg:
        img = augment_image_pil(img, augment_cfg)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    img_path = out_dir / f"img_{idx:06d}.png"
    svg_path = out_dir / f"img_{idx:06d}.svg"
    img.save(img_path)
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_text)
    coco_img = dict(id=idx, file_name=str(img_path.name), height=height, width=width)
    annotations = []
    ann_id = idx*10
    annotations.append(make_coco_annotation(ann_id+1, idx, rmeta['bbox'], category_id=1))  # resistor
    annotations.append(make_coco_annotation(ann_id+2, idx, cmeta['bbox'], category_id=2))  # capacitor
    annotations.append(make_coco_annotation(ann_id+3, idx, wmeta['bbox'], category_id=3))  # wire
    return coco_img, annotations

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=str, default='out')
    parser.add_argument('--n', type=int, default=10)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
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
    print("Done.")