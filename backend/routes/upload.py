from fastapi import APIRouter, UploadFile
from .process_diagram import process_diagram

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile):
    # Forward upload to ML process
    resp = await process_diagram(file)
    return resp