# api.py - core FastAPI app: inference lookup and corrections endpoint
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any, Dict
from .db import get_db_pool, get_redis
import json

app = FastAPI(title="Whirly Backend")

class ElementCorrection(BaseModel):
    id: str
    action: str
    new_label: str = None
    terminals: List[List[float]] = None
    new_elements: List[Dict[str, Any]] = None

class CorrectionPayload(BaseModel):
    image_id: str
    user_id: str = None
    elements: List[ElementCorrection]
    annotation_meta: Dict[str, Any] = {}

@app.on_event("startup")
async def startup():
    app.state.db = await get_db_pool()
    app.state.redis = await get_redis()

@app.get("/api/inference/{image_id}")
async def get_inference(image_id: str):
    async with app.state.db.acquire() as conn:
        row = await conn.fetchrow("SELECT inference_json, svg, raster_path FROM inferences WHERE image_id=$1", image_id)
        if not row:
            raise HTTPException(status_code=404, detail="inference not found")
        return {"image_id": image_id, "svg": row['svg'], "components": row['inference_json'].get('components', [])}

@app.post("/api/corrections", status_code=201)
async def post_correction(payload: CorrectionPayload):
    async with app.state.db.acquire() as conn:
        row = await conn.fetchrow("SELECT inference_json, svg, raster_path FROM inferences WHERE image_id=$1", payload.image_id)
        if not row:
            raise HTTPException(status_code=404, detail="image not found")
        q = """
        INSERT INTO corrections (image_id, user_id, original_inference, correction, status)
        VALUES ($1,$2,$3,$4,'raw') RETURNING id
        """
        rec_id = await conn.fetchval(q, payload.image_id, payload.user_id, row['inference_json'], json.dumps(payload.dict()))
        # enqueue
        await app.state.redis.lpush('corrections_queue', rec_id)
        return {"correction_id": rec_id}