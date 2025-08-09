"""
Basic authentication/authorization for technician/admin dashboard.
Protects admin/report endpoints and enables logout/login.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import functools

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Dummy user store
USERS = {
    "tech1": {"password": "pass123", "role": "technician"},
    "tech2": {"password": "pass456", "role": "technician"},
    "admin": {"password": "adminpass", "role": "admin"}
}

def login_required(role=None):
    def decorator(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                flash("Access denied.")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")
        user = USERS.get(user_id)
        if user and user["password"] == password:
            session["user_id"] = user_id
            session["role"] = user["role"]
            flash("Logged in!")
            return redirect(url_for("index"))
        flash("Login failed.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route("/admin")
@login_required(role="admin")
def admin():
    # ... as before ...
    pass

@app.route("/admin/download/<report>")
@login_required(role="admin")
def admin_download(report):
    # ... as before ...
    pass

@app.route("/upload", methods=["GET", "POST"])
@login_required(role="technician")
def upload():
    # ... as before ...
    pass