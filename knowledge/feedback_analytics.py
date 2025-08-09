"""
Feedback analytics for admin dashboard and reporting.
Includes brand-filtered feedback volume, average ratings, and text analytics.
"""

import json

FEEDBACK_PATH = "feedback.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

def feedback_overview():
    try:
        with open(FEEDBACK_PATH, "r") as f:
            feedback = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        feedback = []
    by_brand = {b: [] for b in ALLOWED_BRANDS}
    for f in feedback:
        if f["brand"] in ALLOWED_BRANDS:
            by_brand[f["brand"]].append(f)
    report = {}
    for brand, items in by_brand.items():
        if items:
            avg = sum(i["rating"] for i in items) / len(items)
        else:
            avg = None
        report[brand] = {
            "count": len(items),
            "average_rating": round(avg, 2) if avg else None
        }
    return report