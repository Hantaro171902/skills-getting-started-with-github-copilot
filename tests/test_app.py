import os
import sys

# Ensure `src` is on path so tests can import `app` directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fastapi.testclient import TestClient
from app import app


def test_get_activities():
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Basketball Team" in data


def test_signup_and_unregister():
    client = TestClient(app)
    email = "testuser+pytest@example.com"
    activity = "Chess Club"

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]

    # Unregister
    r2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r2.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]
