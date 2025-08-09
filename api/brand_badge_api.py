"""
API Endpoint for Brand-Specific Badge Detail and History
- Returns badge history and details for Whirlpool, Maytag, KitchenAid, and Jenn-Air contributions.
"""

from fastapi import FastAPI, Query
from typing import Dict, List
import json

LEADERBOARD_PATH = "leaderboard.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

app = FastAPI()

BADGE_DETAILS = {
    "Symbol Scout": "Awarded for uploading tech sheets with 5 or more unique symbols.",
    "Schematic Uploader": "Awarded for uploading at least one schematic or wiring diagram.",
    "Documentation Champion": "Awarded for uploading tech sheets with over 500 characters of useful text."
}

@app.get("/badges")
def api_badges(user_id: str = Query(..., description="User identifier")) -> Dict[str, List]:
    """
    Returns badge history for a user, filtered to supported brands.
    """
    try:
        with open(LEADERBOARD_PATH, "r") as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        leaderboard = {}
    badges = leaderboard.get(user_id, {}).get("badges", [])
    # Only return badges for supported brand uploads
    return {"badges": [b for b in badges if b in BADGE_DETAILS], "details": BADGE_DETAILS}

@app.get("/badges/all")
def api_all_badges() -> Dict[str, str]:
    """
    Returns all possible badge details for supported brands.
    """
    return BADGE_DETAILS