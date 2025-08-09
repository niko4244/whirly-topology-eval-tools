# Add feedback analytics to admin dashboard

from fastapi import FastAPI
from typing import Dict, List
import json
from knowledge.feedback_analytics import feedback_overview

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

@app.get("/admin/summary")
def api_admin_summary() -> Dict:
    leaderboard = get_json_safe(LEADERBOARD_PATH)
    badge_events = get_json_safe(BADGE_EVENTS_PATH)
    badge_events = [e for e in badge_events if e["brand"] in ALLOWED_BRANDS]
    total_uploads = sum(user.get("uploads", 0) for user in leaderboard.values())
    unique_users = len(leaderboard)
    badge_count = sum(len(user.get("badges", [])) for user in leaderboard.values())
    uploads_by_brand = {b: 0 for b in ALLOWED_BRANDS}
    for event in badge_events:
        uploads_by_brand[event["brand"]] += 1
    trending_reasons = {}
    for event in badge_events:
        trending_reasons[event["reason"]] = trending_reasons.get(event["reason"], 0) + 1
    feedback_stats = feedback_overview()
    feedback_count = sum(stats["count"] for stats in feedback_stats.values())
    return {
        "total_uploads": total_uploads,
        "unique_users": unique_users,
        "total_badges_awarded": badge_count,
        "uploads_by_brand": uploads_by_brand,
        "trending_badge_reasons": trending_reasons,
        "feedback_count": feedback_count,
        "feedback_stats": feedback_stats
    }