"""
Unit tests for brand-filtered, gamified tech sheet upload and reporting system.
Covers: upload workflow, badge awarding, badge event logging, leaderboard, CSV export.
"""

import os
import json
from knowledge.gamification import award_contribution_badge
from knowledge.badge_award_events import log_badge_event
from knowledge.brand_report import export_leaderboard_csv, export_badge_events_csv

LEADERBOARD_PATH = "leaderboard.json"
BADGE_EVENTS_PATH = "badge_events.json"

def setup_module(module):
    # Clean up for test isolation
    for path in [LEADERBOARD_PATH, BADGE_EVENTS_PATH, "leaderboard_report.csv", "badge_events_report.csv"]:
        if os.path.exists(path):
            os.remove(path)

def test_award_badge_and_event_logging():
    # Prepare data for supported brand
    sheet_data = {
        "brand": "whirlpool",
        "symbols": ["relay", "motor", "pump", "switch", "fuse"],
        "diagrams": ["wiring1.png"],
        "text": "This is a long enough documentation to pass the threshold." * 20
    }
    user_id = "testuser"
    appliance_id = "whirlpool_test_001"
    award_contribution_badge(user_id, appliance_id, sheet_data)

    # Leaderboard populated
    with open(LEADERBOARD_PATH, "r") as f:
        leaderboard = json.load(f)
    assert user_id in leaderboard
    stats = leaderboard[user_id]
    assert stats["uploads"] == 1
    assert "Symbol Scout" in stats["badges"]
    assert "Schematic Uploader" in stats["badges"]
    assert "Documentation Champion" in stats["badges"]

    # Badge events
    with open(BADGE_EVENTS_PATH, "r") as f:
        events = json.load(f)
    event_badges = [e["badge"] for e in events if e["user_id"] == user_id]
    assert set(event_badges) == {"Symbol Scout", "Schematic Uploader", "Documentation Champion"}

def test_csv_export():
    # Populate with one badge event
    log_badge_event(
        user_id="testuser2",
        appliance_id="maytag_test_002",
        badge="Schematic Uploader",
        reason="Uploaded schematic.",
        brand="maytag"
    )
    # Export leaderboard
    export_leaderboard_csv("leaderboard_report.csv")
    assert os.path.exists("leaderboard_report.csv")
    with open("leaderboard_report.csv") as f:
        lines = f.readlines()
    assert "user_id" in lines[0]  # CSV header present

    # Export badge events
    export_badge_events_csv("badge_events_report.csv")
    with open("badge_events_report.csv") as f:
        contents = f.read()
    assert "Schematic Uploader" in contents
    assert "maytag" in contents

def test_no_badges_for_other_brands():
    # Brand not allowed
    sheet_data = {
        "brand": "samsung",
        "symbols": ["relay", "motor", "pump", "switch", "fuse"],
        "diagrams": ["wiring1.png"],
        "text": "This is a long enough documentation to pass the threshold." * 20
    }
    award_contribution_badge("user_otherbrand", "samsung_test_003", sheet_data)
    # Leaderboard should not have user
    with open(LEADERBOARD_PATH, "r") as f:
        leaderboard = json.load(f)
    assert "user_otherbrand" not in leaderboard

def teardown_module(module):
    # Clean up after tests
    for path in [LEADERBOARD_PATH, BADGE_EVENTS_PATH, "leaderboard_report.csv", "badge_events_report.csv"]:
        if os.path.exists(path):
            os.remove(path)