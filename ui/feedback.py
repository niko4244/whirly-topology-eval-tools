"""
User-Centric Features:
- Provide clear, actionable feedback with contextual images and annotated diagrams.
- Gamify energy savings and maintenance achievements for user engagement.
"""

from typing import List, Dict
import datetime

def present_feedback(diagnosis: Dict, images: List[str] = None):
    """
    Generate annotated feedback and plain-language reports for users.
    Args:
        diagnosis (dict): Diagnosis details (e.g., {'fault': True, 'root_cause': 'Relay stuck', ...}).
        images (list of str): Paths to contextual images/diagrams.
    Returns:
        dict: Structured feedback ready for UI rendering.
    """
    report = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "summary": "",
        "diagnosis": diagnosis,
        "images": images or [],
        "recommendations": []
    }
    if diagnosis.get("fault"):
        report["summary"] = f"Attention: Fault detected! Likely root cause: {diagnosis.get('root_cause', 'Unknown')}."
        report["recommendations"].append("Recommended action: " + diagnosis.get("action", "Please consult a technician."))
    else:
        report["summary"] = "No faults detected. Appliance is operating normally."
        report["recommendations"].append("Keep monitoring for optimal performance.")
    return report

def gamify_energy_savings(user_id: str, stats: Dict, leaderboard_path: str = "leaderboard.json"):
    """
    Award badges, track leaderboard, and encourage user engagement for energy saving.
    Args:
        user_id (str): Unique user identifier.
        stats (dict): User's energy savings stats (e.g., {'savings_kwh': 15, 'streak_days': 7}).
        leaderboard_path (str): Path to the leaderboard file.
    Returns:
        dict: Badge or achievement info.
    """
    badge = None
    if stats.get('savings_kwh', 0) > 10:
        badge = "Energy Saver"
    if stats.get('streak_days', 0) >= 7:
        badge = "Weekly Champion"

    # Load and update leaderboard
    try:
        with open(leaderboard_path, "r") as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        leaderboard = {}
    leaderboard[user_id] = stats
    with open(leaderboard_path, "w") as f:
        json.dump(leaderboard, f, indent=2)

    return {
        "badge": badge,
        "leaderboard": leaderboard
    }