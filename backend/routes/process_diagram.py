from fastapi import APIRouter, UploadFile, HTTPException, File
from backend.ml_inference import run_detection_from_bytes

router = APIRouter()

@router.post("/process-diagram")
async def process_diagram(file: UploadFile = File(...)):
    contents = await file.read()
    detections = run_detection_from_bytes(contents, conf=0.3)
    # Map detections to components structure for graph building
    components = []
    for i,d in enumerate(detections):
        x1, y1, x2, y2 = d['x1'], d['y1'], d['x2'], d['y2']
        components.append({'id': f'c{i}', 'bbox':[x1,y1,x2-x1,y2-y1], 'label': d['name'], 'score': d['confidence']})
    # Continue with wire segmentation/skeletonization and graph building
    # ... (your code here)
    return {"components": components, "detections": detections}