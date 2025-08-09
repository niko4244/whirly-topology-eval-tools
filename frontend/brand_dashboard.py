# Integrate secure CSV download into Flask frontend

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from frontend.brand_auth import login_required
from frontend.brand_csv_download import admin_report_download
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

API_BASE = "http://localhost:8000"

@app.route("/admin/download/<report>")
@login_required(role="admin")
def admin_download(report):
    return admin_report_download(report)