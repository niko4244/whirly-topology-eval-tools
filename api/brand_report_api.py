# Add feedback CSV report endpoint for admin

from fastapi import FastAPI, Response
from knowledge.brand_report import export_leaderboard_csv, export_badge_events_csv
from knowledge.feedback_csv_report import export_feedback_csv

app = FastAPI()

@app.get("/admin/report/leaderboard.csv")
def download_leaderboard_csv():
    export_leaderboard_csv()
    with open("leaderboard_report.csv", "rb") as file:
        content = file.read()
    return Response(content, media_type="text/csv")

@app.get("/admin/report/badge_events.csv")
def download_badge_events_csv():
    export_badge_events_csv()
    with open("badge_events_report.csv", "rb") as file:
        content = file.read()
    return Response(content, media_type="text/csv")

@app.get("/admin/report/feedback.csv")
def download_feedback_csv():
    export_feedback_csv()
    with open("feedback_report.csv", "rb") as file:
        content = file.read()
    return Response(content, media_type="text/csv")