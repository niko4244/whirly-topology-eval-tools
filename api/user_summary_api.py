"""
API Endpoint for User Summary
- Shows uploads, badges, badge event history, and feedback for supported brands.
"""

from fastapi import FastAPI, Query
from typing import Dict, List
import json

LEADERBOARD_PATH = "leaderboard.json"
BADGE_EVENTS_PATH = "badge_events.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

app = FastAPI()

def get_json_safe(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return {} if path == LEADERBOARD_PATH else []

@app.get("/user/summary")
def api_user_summary(user_id: str = Query(..., description="User identifier")) -> Dict:
    leaderboard = get_json_safe(LEADERBOARD_PATH)
    badge_events = get_json_safe(BADGE_EVENTS_PATH)
    user_stats = leaderboard.get(user_id, {})
    user_events = [e for e in badge_events if e["user_id"] == user_id and e["brand"] in ALLOWED_BRANDS]
    # Feedback: (assume feedback stored in feedback.json)
    try:
        with open("feedback.json", "r") as f:
            feedback = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        feedback = []
    user_feedback = [f for f in feedback if f.get("user_id") == user_id and any(b in f.get("query", "").lower() for b in ALLOWED_BRANDS)]
    return {
        "uploads": user_stats.get("uploads", 0),
        "badges": user_stats.get("badges", []),
        "last_upload": user_stats.get("last_upload", ""),
        "badge_events": user_events,
        "feedback": user_feedback
    }