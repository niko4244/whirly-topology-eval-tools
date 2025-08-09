"""
Gamification: Badges and Leaderboard for Tech Sheet Contributions
- Tracks and rewards users for uploading useful tech sheets and knowledge expansions.
"""

import json
import datetime

def award_contribution_badge(user_id: str, appliance_id: str, kb_path: str = "knowledge_base.json", leaderboard_path: str = "leaderboard.json"):
    """
    Assign badges for tech sheet uploads that expand the KB or solve real issues.
    Args:
        user_id (str): Unique user identifier.
        appliance_id (str): Appliance for which a tech sheet was uploaded.
        kb_path (str): Path to KB.
        leaderboard_path (str): Path to leaderboard.
    Returns:
        dict: Badge info and updated leaderboard.
    """
    try:
        with open(kb_path, "r") as f:
            kb = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        kb = {}
    contribution = kb.get(appliance_id, {})

    # Badge logic
    badges = []
    if contribution.get("symbols"):
        badges.append("Symbol Scout")
    if contribution.get("diagrams"):
        badges.append("Schematic Uploader")
    if len(contribution.get("text", "")) > 100:
        badges.append("Documentation Champion")

    # Load leaderboard
    try:
        with open(leaderboard_path, "r") as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        leaderboard = {}
    leaderboard_entry = leaderboard.get(user_id, {"uploads": 0, "badges": []})
    leaderboard_entry["uploads"] += 1
    leaderboard_entry["badges"] = list(set(leaderboard_entry["badges"] + badges))
    leaderboard_entry["last_upload"] = datetime.datetime.utcnow().isoformat()
    leaderboard[user_id] = leaderboard_entry

    with open(leaderboard_path, "w") as f:
        json.dump(leaderboard, f, indent=2)

    return {
        "user_id": user_id,
        "appliance_id": appliance_id,
        "badges": badges,
        "leaderboard": leaderboard
    }

# Example usage:
if __name__ == "__main__":
    results = award_contribution_badge("niko4244", "dryer-001")
    print(results)