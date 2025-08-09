"""
Add feedback UI and API integration for brand-filtered system.
Allows technicians to rate uploads/search results for supported brands.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

API_BASE = "http://localhost:8000"

@app.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        appliance_id = request.form.get("appliance_id")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        r = requests.post(
            f"{API_BASE}/search/feedback",
            json={
                "user_id": user_id,
                "appliance_id": appliance_id,
                "rating": rating,
                "comment": comment
            }
        )
        result = r.json()
        if "message" in result:
            flash(result["message"])
        else:
            flash("Feedback submitted!")
        return redirect(url_for("feedback"))
    return render_template("feedback.html")

@app.route("/feedback/summary/<appliance_id>")
def feedback_summary(appliance_id):
    r = requests.get(f"{API_BASE}/search/feedback/summary", params={"appliance_id": appliance_id})
    summary = r.json()
    return render_template("feedback_summary.html", summary=summary, appliance_id=appliance_id)