import numpy as np
from PIL import Image
import io

# Placeholder: replace with YOLO/Detectron2 model loading
def detect_diagram(image_bytes):
    # For MVP, return dummy detected boxes and classes
    image = Image.open(io.BytesIO(image_bytes))
    w, h = image.size
    # Example detection: one resistor and one wire
    detections = [
        {"class": "resistor", "bbox": [w//4, h//4, w//2, h//8], "score": 0.99},
        {"class": "wire", "bbox": [w//4, h//2, w//2, h//20], "score": 0.95}
    ]
    return detections