# Whirly Mask2Former Training Script

## Features

- Loads custom vector-based Detectron2 dataset (SVG path → polygons)
- Mask2Former config tuned for circuit diagrams
- Mixed precision training and multi-GPU support
- Standard COCO metrics logging (extend with topology metrics)

## Usage

### 1. Install dependencies

```bash
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu118/torch2.0/index.html
pip install fvcore iopath pycocotools
```

### 2. Prepare your annotation JSONs

Each file should contain:
```json
{
  "image_path": "datasets/images/img_00001.png",
  "width": 1024,
  "height": 768,
  "annotations": [
    { "label": "wire", "svg_path": "M10 10 H 90 V 90 H 10 Z" }
  ]
}
```

### 3. Configure your labels

Edit `LABEL_MAP` in `train_circuit.py` to match your classes.

### 4. Train

```bash
python train_circuit.py
```

### 5. Extend

- Add your topology metric hooks to `Trainer.build_evaluator`.
- Tune hyperparameters in `mask2former_circuit_config.py`.

---

MIT License