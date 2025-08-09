from ultralytics import YOLO
import numpy as np
from PIL import Image
import io, os

MODEL_PATH = os.environ.get('WHIRLY_MODEL', 'runs/whirly/exp1/weights/best.pt')
model = YOLO(MODEL_PATH)

def run_detection_from_bytes(image_bytes, conf=0.25, iou=0.45, imgsz=640, device=None):
    """
    image_bytes: bytes (uploaded file contents)
    returns: list of detections dict [{'x1','y1','x2','y2','confidence','class','name'}]
    """
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    results = model.predict(img, imgsz=imgsz, conf=conf, iou=iou, device=device, verbose=False)
    out = []
    r = results[0]
    boxes = r.boxes
    for box in boxes:
        xyxy = box.xyxy.cpu().numpy().tolist()[0]
        conf_score = float(box.conf.cpu().numpy()[0])
        cls = int(box.cls.cpu().numpy()[0])
        name = model.names.get(cls, str(cls))
        out.append({
            'x1': int(xyxy[0]), 'y1': int(xyxy[1]), 'x2': int(xyxy[2]), 'y2': int(xyxy[3]),
            'confidence': conf_score, 'class': cls, 'name': name
        })
    return out