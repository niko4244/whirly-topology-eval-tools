"""
API Endpoint to Retrieve Brand-Specific Badge Award Events
- Returns badge history (events) for Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads.
- Provides audit trail for user badge achievements.
"""

from fastapi import FastAPI, Query
from typing import List, Dict
import json

BADGE_EVENTS_PATH = "badge_events.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

app = FastAPI()

@app.get("/badges/events")
def api_badge_events(user_id: str = Query(..., description="User identifier")) -> List[Dict]:
    """
    Returns badge award event history for this user, filtered to supported brands.
    """
    try:
        with open(BADGE_EVENTS_PATH, "r") as f:
            events = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        events = []
    filtered_events = [
        e for e in events
        if e["user_id"] == user_id and e["brand"] in ALLOWED_BRANDS
    ]
    return filtered_events