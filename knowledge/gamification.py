# (add badge event logging to badge award process)
from knowledge.badge_award_events import log_badge_event

def award_contribution_badge(user_id: str, appliance_id: str, sheet_data: dict):
    """
    Award badges for uploads of supported brands and update leaderboard.
    Also logs badge award events for audit and analytics.
    """
    brand = sheet_data.get("brand", "")
    if brand not in ALLOWED_BRANDS:
        return  # Only award for supported brands

    try:
        with open(LEADERBOARD_PATH, "r") as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        leaderboard = {}

    user_stats = leaderboard.setdefault(user_id, {"uploads": 0, "badges": [], "last_upload": ""})

    # Awards and logging
    if len(sheet_data.get("symbols", [])) >= 5 and BADGES["symbol_rich"] not in user_stats["badges"]:
        user_stats["badges"].append(BADGES["symbol_rich"])
        log_badge_event(
            user_id=user_id,
            appliance_id=appliance_id,
            badge=BADGES["symbol_rich"],
            reason="Uploaded tech sheet with 5+ symbols.",
            brand=brand
        )
    if len(sheet_data.get("diagrams", [])) >= 1 and BADGES["schematic_upload"] not in user_stats["badges"]:
        user_stats["badges"].append(BADGES["schematic_upload"])
        log_badge_event(
            user_id=user_id,
            appliance_id=appliance_id,
            badge=BADGES["schematic_upload"],
            reason="Uploaded tech sheet with a schematic/diagram.",
            brand=brand
        )
    if len(sheet_data.get("text", "")) > 500 and BADGES["text_upload"] not in user_stats["badges"]:
        user_stats["badges"].append(BADGES["text_upload"])
        log_badge_event(
            user_id=user_id,
            appliance_id=appliance_id,
            badge=BADGES["text_upload"],
            reason="Uploaded tech sheet with substantial documentation.",
            brand=brand
        )

    user_stats["uploads"] += 1
    user_stats["last_upload"] = datetime.datetime.utcnow().isoformat()
    leaderboard[user_id] = user_stats
    with open(LEADERBOARD_PATH, "w") as f:
        json.dump(leaderboard, f, indent=2)