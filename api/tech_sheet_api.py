"""
API Endpoints for Tech Sheet Upload & Knowledge Base Expansion
- Allows uploading, extraction, and retrieval of appliance tech sheets and extracted symbols/diagrams.
"""

from fastapi import FastAPI, UploadFile, File
from docs.tech_sheet_ingest import save_uploaded_sheet, extract_symbols_and_diagrams, add_to_knowledge_base

app = FastAPI()

@app.post("/techsheet/upload/{appliance_id}")
async def upload_tech_sheet(appliance_id: str, file: UploadFile = File(...)):
    """
    Upload a tech sheet for an appliance and expand the knowledge base.
    """
    temp_path = f"temp_upload_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    saved_path = save_uploaded_sheet(temp_path)
    sheet_data = extract_symbols_and_diagrams(saved_path)
    add_to_knowledge_base(appliance_id, sheet_data)
    return {"message": "Tech sheet ingested", "symbols": sheet_data["symbols"], "diagrams": sheet_data["diagrams"]}