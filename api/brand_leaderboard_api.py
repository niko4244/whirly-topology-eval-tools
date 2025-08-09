"""
API Endpoint for Gamified Brand-Specific Leaderboard
- Tracks and displays user contributions for Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads only.
- Shows badge counts and upload stats per user.
"""

from fastapi import FastAPI, Query
from typing import Dict, List
import json

LEADERBOARD_PATH = "leaderboard.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

app = FastAPI()

def get_leaderboard() -> Dict[str, Dict]:
    """
    Loads leaderboard, filters uploads to supported brands, returns user stats.
    """
    try:
        with open(LEADERBOARD_PATH, "r") as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        leaderboard = {}
    # Filter uploads and badges for supported brands only
    filtered_board = {}
    for user, entry in leaderboard.items():
        # Count only uploads and badges for allowed brands
        uploads = entry.get("uploads", 0)
        # Check if last upload was for supported brand
        last_brand = entry.get("badges", [])
        if any(b.lower() in ALLOWED_BRANDS for b in last_brand):
            filtered_board[user] = {
                "uploads": uploads,
                "badges": entry.get("badges", []),
                "last_upload": entry.get("last_upload", "")
            }
    return filtered_board

@app.get("/leaderboard")
def api_leaderboard() -> Dict[str, Dict]:
    """
    Returns brand-specific leaderboard for gamified contributions.
    """
    return get_leaderboard()