# Whirly Vector-based Dataset Pipeline

This directory contains utilities to convert PDF circuit diagrams to SVG, and then extract vector paths for annotation and dataset creation.

## Tools

- `pdf_to_svg.py`: Uses `pdf2svg` to convert multi-page PDFs to SVGs.
- `svg_to_paths_json.py`: Parses SVG files to extract vector paths and attributes, saving as JSON.

## Usage

### 1. Convert PDF to SVG

Install pdf2svg:

```bash
sudo apt-get install pdf2svg
```

Convert each page:

```bash
python pdf_to_svg.py input.pdf svg_output_dir/
```

### 2. Extract vector paths from SVG

Install svgpathtools:

```bash
pip install svgpathtools
```

Extract paths:

```bash
python svg_to_paths_json.py svg_output_dir/input_page_1.svg svg_output_dir/input_page_1.paths.json
```

### 3. Next Steps

- Annotate paths with semantic labels (`resistor`, `capacitor`, `wire`, etc).
- Build a dataset with vector path data for mask generation and Detectron2 training.
- Optionally rasterize vector annotations at high resolution for segmentation/instance masks.

---

Want an annotation tool or COCO conversion utility next? Just ask!