"""
Add secure CSV download endpoints to Flask frontend, using authentication.
Restricts report download to admin users only.
"""

from flask import send_file, session, flash, redirect, url_for
import os

def admin_report_download(report):
    if "user_id" not in session or session.get("role") != "admin":
        flash("Admin access required to download reports.")
        return redirect(url_for("login"))
    report_files = {
        "leaderboard": "leaderboard_report.csv",
        "badge_events": "badge_events_report.csv",
        "feedback": "feedback_report.csv"
    }
    path = report_files.get(report)
    if path and os.path.exists(path):
        return send_file(path, as_attachment=True)
    flash("Report not found.")
    return redirect(url_for("admin"))