"""
Event Logging for Brand-Specific Badge Awards
- Tracks when and why badges are awarded for Whirlpool, Maytag, KitchenAid, and Jenn-Air uploads.
- Enables badge history display, audit, and analytics.
"""

import json
import datetime

BADGE_EVENTS_PATH = "badge_events.json"
ALLOWED_BRANDS = ["whirlpool", "maytag", "kitchenaid", "jenn-air"]

def log_badge_event(user_id: str, appliance_id: str, badge: str, reason: str, brand: str):
    """
    Record a badge award event for analytics and user history.
    Args:
        user_id (str): User receiving badge.
        appliance_id (str): Appliance identifier.
        badge (str): Badge name.
        reason (str): Reason for award.
        brand (str): Brand for which badge was awarded.
    """
    if brand not in ALLOWED_BRANDS:
        return  # Only log events for supported brands

    try:
        with open(BADGE_EVENTS_PATH, "r") as f:
            events = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        events = []

    event = {
        "user_id": user_id,
        "appliance_id": appliance_id,
        "badge": badge,
        "reason": reason,
        "brand": brand,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    events.append(event)
    with open(BADGE_EVENTS_PATH, "w") as f:
        json.dump(events, f, indent=2)

# Example usage:
if __name__ == "__main__":
    log_badge_event(
        user_id="niko4244",
        appliance_id="maytag_dryer_003",
        badge="Schematic Uploader",
        reason="Uploaded a Maytag dryer schematic.",
        brand="maytag"
    )