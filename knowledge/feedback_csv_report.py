"""
Export feedback as CSV for admin/business analytics (supported brands only).
"""

import json
import csv

FEEDBACK_PATH = "feedback.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

def export_feedback_csv(csv_path="feedback_report.csv"):
    try:
        with open(FEEDBACK_PATH, "r") as f:
            feedback = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        feedback = []
    with open(csv_path, "w", newline='') as csvfile:
        fieldnames = ["user_id", "appliance_id", "brand", "rating", "comment", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in feedback:
            if item["brand"] in ALLOWED_BRANDS:
                writer.writerow(item)