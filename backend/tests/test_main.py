import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_login_get_me():
    # Register
    r = client.post("/auth/register", json={"email": "test@example.com", "password": "testpass"})
    assert r.status_code == 200
    # Login
    r = client.post("/auth/token", data={"username": "test@example.com", "password": "testpass"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Get self
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert data["email"] == "test@example.com"

def test_document_crud():
    # Register and login
    r = client.post("/auth/register", json={"email": "docuser@example.com", "password": "docpass"})
    r = client.post("/auth/token", data={"username": "docuser@example.com", "password": "docpass"})
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Upload document
    r = client.post("/documents", json={"name": "Doc1", "path": "/uploads/doc1.pdf"}, headers=headers)
    assert r.status_code == 200
    doc_id = r.json()["id"]
    # List documents
    r = client.get("/documents", headers=headers)
    assert r.status_code == 200
    docs = r.json()
    assert any(d["name"] == "Doc1" for d in docs)
    # Scan document
    r = client.put(f"/documents/{doc_id}/scan", headers=headers)
    assert r.status_code == 200
    assert r.json()["scanned"] is True
    # Delete document
    r = client.delete(f"/documents/{doc_id}", headers=headers)
    assert r.status_code == 204