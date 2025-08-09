# db.py - async DB + Redis connection helpers
import os
import asyncpg
import aioredis
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/whirly")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

_db_pool: Optional[asyncpg.pool.Pool] = None
_redis = None

async def get_db_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    return _db_pool

async def get_redis():
    global _redis
    if _redis is None:
        _redis = await aioredis.from_url(REDIS_URL)
    return _redis