# validator.py - async worker to pop corrections, validate, and store curated examples
import asyncio
import asyncpg
import aioredis
import json
from shapely.geometry import Point, Polygon
from ..db import DATABASE_URL, REDIS_URL

async def conversion_function(original, correction):
    # Stub: convert correction + original -> COCO annotation + netlist
    # In prod this must be deterministic and robust.
    coco = {
        "images": [{"id": 1, "file_name": original.get('raster_path', ''), "height": original.get('image_height', 1024), "width": original.get('image_width', 1024)}],
        "annotations": []
    }
    return coco

async def validate_and_store(conn, correction_row):
    correction = correction_row['correction']
    original = correction_row['original_inference']
    results = {"valid": True, "issues": []}
    # simple example check
    for el in correction['elements']:
        if el.get('terminals'):
            for t in el['terminals']:
                x,y = t
                if x < 0 or y < 0:
                    results['valid'] = False
                    results['issues'].append(f"terminal out of bounds {t}")
    if results['valid']:
        coco = await conversion_function(original, correction)
        await conn.execute("INSERT INTO curated_examples (image_id, svg, raster_path, coco_annotation, netlist_json, created_from_correction_id) VALUES ($1,$2,$3,$4,$5,$6)", correction['image_id'], original.get('svg'), original.get('raster_path'), json.dumps(coco), json.dumps(original.get('netlist')), correction_row['id'])
        await conn.execute("UPDATE corrections SET status='validated', validation_info=$1 WHERE id=$2", json.dumps(results), correction_row['id'])
    else:
        await conn.execute("UPDATE corrections SET status='rejected', validation_info=$1 WHERE id=$2", json.dumps(results), correction_row['id'])

async def worker_loop():
    redis = await aioredis.from_url(REDIS_URL)
    pool = await asyncpg.create_pool(DATABASE_URL)
    while True:
        item = await redis.brpop('corrections_queue', timeout=5)
        if item:
            _, cid = item
            async with pool.acquire() as conn:
                row = await conn.fetchrow('SELECT * FROM corrections WHERE id=$1', int(cid))
                if row:
                    await validate_and_store(conn, row)
        else:
            await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(worker_loop())