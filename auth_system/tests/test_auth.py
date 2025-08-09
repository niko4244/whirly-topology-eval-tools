import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_login_mfa():
    # Register
    r = client.post("/auth/register", json={"email": "mfauser@example.com", "password": "StrongPass123"})
    assert r.status_code == 200
    # Enable MFA
    token = client.post("/auth/token", data={"username": "mfauser@example.com", "password": "StrongPass123"}).json()
    assert "access_token" in token or token.get("token_type") == "mfa_challenge"
    # MFA Enable
    headers = {"Authorization": f"Bearer {token.get('access_token')}"}
    mfa_enable = client.post("/auth/mfa_enable", headers=headers)
    assert mfa_enable.status_code == 200
    mfa_secret = mfa_enable.json()["mfa_secret"]
    # MFA Verify
    mfa_token = client.post("/auth/mfa_verify", json={"email": "mfauser@example.com", "code": mfa_secret[::-1][:6]})
    assert mfa_token.status_code == 200

def test_password_policy_and_lockout():
    # Weak password
    r = client.post("/auth/register", json={"email": "weakpass@example.com", "password": "short"})
    assert r.status_code == 400
    # Lockout
    client.post("/auth/register", json={"email": "lockout@example.com", "password": "StrongPass123"})
    for _ in range(6):
        r = client.post("/auth/token", data={"username": "lockout@example.com", "password": "WrongPass"})
    assert r.status_code == 403

def test_password_reset():
    client.post("/auth/register", json={"email": "resetuser@example.com", "password": "StrongPass123"})
    r = client.post("/auth/password_reset", json={"email": "resetuser@example.com"})
    assert r.status_code == 200
    token = r.json()["token"]
    r2 = client.post("/auth/password_reset/confirm", json={"token": token, "new_password": "NewStrongPass123"})
    assert r2.status_code == 200