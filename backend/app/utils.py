# utils.py - small helpers
import json
from typing import Any

class JSONEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        try:
            return super().default(obj)
        except Exception:
            return str(obj)

def safe_json_dumps(obj):
    return JSONEncoder().encode(obj)