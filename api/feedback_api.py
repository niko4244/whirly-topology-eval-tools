"""
Feedback API endpoints for brand-filtered tech sheet system.
Allows submitting and viewing feedback for supported brands only.
"""

from fastapi import FastAPI, Query, HTTPException
from typing import Dict, List
import json
import datetime

FEEDBACK_PATH = "feedback.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

app = FastAPI()

def get_json_safe(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return []

def save_json_safe(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_brand_from_appliance(appliance_id):
    # Dummy extraction for demo (real system would use DB or naming convention)
    for brand in ALLOWED_BRANDS:
        if brand.replace("-", "").lower() in appliance_id.replace("-", "").lower():
            return brand
    return ""

@app.post("/search/feedback")
def submit_feedback(
    user_id: str = Query(...),
    appliance_id: str = Query(...),
    rating: int = Query(..., ge=1, le=5),
    comment: str = Query("")
) -> Dict:
    brand = get_brand_from_appliance(appliance_id)
    if brand not in ALLOWED_BRANDS:
        raise HTTPException(
            status_code=400,
            detail="Feedback only accepted for Whirlpool, Maytag, KitchenAid, and Jenn-Air appliances."
        )
    feedback = get_json_safe(FEEDBACK_PATH)
    feedback.append({
        "user_id": user_id,
        "appliance_id": appliance_id,
        "brand": brand,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.datetime.utcnow().isoformat()
    })
    save_json_safe(FEEDBACK_PATH, feedback)
    return {"message": "Feedback submitted successfully."}

@app.get("/search/feedback/summary")
def feedback_summary(appliance_id: str = Query(...)) -> Dict:
    feedback = get_json_safe(FEEDBACK_PATH)
    brand = get_brand_from_appliance(appliance_id)
    feedback_filtered = [
        f for f in feedback if f["appliance_id"] == appliance_id and f["brand"] in ALLOWED_BRANDS
    ]
    if not feedback_filtered:
        return {"feedback": [], "average_rating": None}
    avg_rating = sum(f["rating"] for f in feedback_filtered) / len(feedback_filtered)
    return {
        "feedback": feedback_filtered,
        "average_rating": round(avg_rating, 2)
    }