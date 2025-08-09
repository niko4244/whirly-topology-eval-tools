# Detectron2 Custom Vector Dataset Loader

This loader enables training Mask2Former and other Detectron2 models directly on vector-annotated circuit datasets.

## Features

- Loads annotation JSONs with SVG path strings and semantic labels.
- Parses SVG paths to polygons using `svgpathtools` and `shapely`.
- Converts polygons to Detectron2 segmentation format (lists of x, y).
- Computes bounding boxes directly from polygons.
- Handles multi-polygon objects and invalid shapes gracefully.

## Usage

1. Prepare your annotation JSONs:
    ```json
    {
      "image_path": "datasets/images/img_00001.png",
      "width": 1024,
      "height": 768,
      "annotations": [
        {
          "label": "wire",
          "svg_path": "M10 10 H 90 V 90 H 10 Z"
        },
        ...
      ]
    }
    ```

2. Set your label mapping:
    ```python
    label_map = {"wire": 0, "resistor": 1, "capacitor": 2}
    ```

3. Register your dataset:
    ```python
    from detectron2.data import DatasetCatalog, MetadataCatalog
    from d2.dataset_vector import load_circuit_dataset

    def get_circuit_dicts():
        return load_circuit_dataset("/path/to/json_annotations", label_map)

    DatasetCatalog.register("circuit_vector_train", get_circuit_dicts)
    MetadataCatalog.get("circuit_vector_train").set(thing_classes=list(label_map.keys()))
    ```

4. Use in your training config:
    ```python
    cfg.DATASETS.TRAIN = ("circuit_vector_train",)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(label_map)
    ```

## Notes

- The loader samples SVG paths to polygons; increase sampling density for more accuracy if needed.
- For elliptical or curved wires/components, polygon approximation is usually sufficient for instance segmentation.
- Extend with additional attributes (e.g., confidence, terminals) as needed for your domain.

---
MIT License