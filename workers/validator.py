import aioredis, asyncio, asyncpg, json

REDIS_URL="redis://localhost:6379/0"
DATABASE_URL="postgresql://user:pass@localhost:5432/whirly"

async def validate_correction(correction_id, db_pool):
    async with db_pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM corrections WHERE id=$1", correction_id)
        payload = row['correction']
        original = row['original_inference']
    results = {"valid": True, "issues": []}
    for el in payload['elements']:
        if el.get('terminals'):
            for t in el['terminals']:
                if not (0 <= t[0] <= original['image_width'] and 0 <= t[1] <= original['image_height']):
                    results['valid'] = False
                    results['issues'].append(f"Terminal {t} out of bounds")
    if results['valid']:
        coco = conversion_function(original, payload)  # Implement your own conversion
        async with db_pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO curated_examples (image_id, svg, raster_path, coco_annotation, netlist_json, created_from_correction_id)
                VALUES ($1,$2,$3,$4,$5,$6)
            """, payload['image_id'], original['svg'], original['raster_path'], json.dumps(coco), json.dumps(original.get('netlist')), correction_id)
            await conn.execute("UPDATE corrections SET status='validated', validation_info=$1 WHERE id=$2", json.dumps(results), correction_id)
    else:
        async with db_pool.acquire() as conn:
            await conn.execute("UPDATE corrections SET status='rejected', validation_info=$1 WHERE id=$2", json.dumps(results), correction_id)

async def worker():
    r = await aioredis.from_url(REDIS_URL)
    db = await asyncpg.create_pool(DATABASE_URL)
    while True:
        item = await r.brpop("corrections_queue", timeout=5)
        if item:
            _, cid = item
            await validate_correction(int(cid), db)
        else:
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(worker())