from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Basic sanity: one known activity exists
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure the test email is not present prior to signup
    res = client.get("/activities")
    assert res.status_code == 200
    participants = res.json()[activity]["participants"]

    if email in participants:
        # remove it first to ensure a consistent starting state
        client.post(f"/activities/{activity}/unregister?email={email}")

    # Sign up the test user
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json().get("message", "")

    # Verify the participant was added
    res = client.get("/activities")
    assert res.status_code == 200
    assert email in res.json()[activity]["participants"]

    # Unregister the test user
    res = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 200
    assert f"Unregistered {email}" in res.json().get("message", "")

    # Verify the participant was removed
    res = client.get("/activities")
    assert res.status_code == 200
    assert email not in res.json()[activity]["participants"]
