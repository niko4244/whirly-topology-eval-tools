"""
Generate CSV Reports for Admin: Uploads, Badges, and Badge Events (Supported Brands Only)
- Enables downloading reports for business analytics and audit.
"""

import csv
import json

LEADERBOARD_PATH = "leaderboard.json"
BADGE_EVENTS_PATH = "badge_events.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

def export_leaderboard_csv(csv_path="leaderboard_report.csv"):
    with open(LEADERBOARD_PATH, "r") as f:
        leaderboard = json.load(f)
    with open(csv_path, "w", newline='') as csvfile:
        fieldnames = ["user_id", "uploads", "badges", "last_upload"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, stats in leaderboard.items():
            writer.writerow({
                "user_id": user,
                "uploads": stats.get("uploads", 0),
                "badges": ";".join(stats.get("badges", [])),
                "last_upload": stats.get("last_upload", "")
            })

def export_badge_events_csv(csv_path="badge_events_report.csv"):
    try:
        with open(BADGE_EVENTS_PATH, "r") as f:
            events = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        events = []
    with open(csv_path, "w", newline='') as csvfile:
        fieldnames = ["user_id", "appliance_id", "badge", "reason", "brand", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for event in events:
            if event["brand"] in ALLOWED_BRANDS:
                writer.writerow(event)

# Usage:
if __name__ == "__main__":
    export_leaderboard_csv()
    export_badge_events_csv()