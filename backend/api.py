from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any, Dict
import asyncpg, os, json
import aioredis

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost:5432/whirly")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
app = FastAPI(title="Whirly Correction API")

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
    app.state.db = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    app.state.redis = await aioredis.from_url(REDIS_URL)

@app.post("/corrections", status_code=201)
async def post_correction(payload: CorrectionPayload):
    async with app.state.db.acquire() as conn:
        original_inference = await conn.fetchrow("SELECT inference_json FROM inferences WHERE image_id=$1", payload.image_id)
        if not original_inference:
            raise HTTPException(status_code=404, detail="image not found")
        q = """
        INSERT INTO corrections (image_id, user_id, original_inference, correction, status)
        VALUES ($1,$2,$3,$4,'raw') RETURNING id
        """
        rec_id = await conn.fetchval(q, payload.image_id, payload.user_id, original_inference['inference_json'], json.dumps(payload.dict()))
        await app.state.redis.lpush("corrections_queue", rec_id)
        return {"correction_id": rec_id}