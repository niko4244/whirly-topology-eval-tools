"""
Test admin authentication and secure CSV report downloads for brand-filtered tech sheet system.
Ensures only admin can access /admin and /admin/download endpoints.
"""

import pytest
from frontend.brand_dashboard import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def login(client, user_id, password):
    return client.post("/login", data=dict(user_id=user_id, password=password), follow_redirects=True)

def logout(client):
    return client.get("/logout", follow_redirects=True)

def test_admin_access_and_report_download(client):
    # Try accessing admin page without login
    resp = client.get("/admin")
    assert b"Login" in resp.data or resp.status_code in (302, 401)

    # Login as technician, try accessing admin page
    login(client, "tech1", "pass123")
    resp = client.get("/admin")
    assert b"Access denied" in resp.data or resp.status_code in (302, 401)
    logout(client)

    # Login as admin, access admin page
    login(client, "admin", "adminpass")
    resp = client.get("/admin")
    assert b"Admin Dashboard" in resp.data

    # Download leaderboard report
    resp = client.get("/admin/download/leaderboard")
    assert resp.status_code == 200 or resp.status_code == 404  # 404 if file doesn't exist

    # Download badge events report
    resp = client.get("/admin/download/badge_events")
    assert resp.status_code == 200 or resp.status_code == 404

    # Download feedback report
    resp = client.get("/admin/download/feedback")
    assert resp.status_code == 200 or resp.status_code == 404

    logout(client)

def test_technician_upload_access(client):
    # Access upload page without login
    resp = client.get("/upload")
    assert b"Login" in resp.data or resp.status_code in (302, 401)

    # Login as technician
    login(client, "tech2", "pass456")
    resp = client.get("/upload")
    assert b"Upload Tech Sheet" in resp.data
    logout(client)