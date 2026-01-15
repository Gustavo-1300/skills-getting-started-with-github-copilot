from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Should be a dict with at least one activity
    assert isinstance(data, dict)
    assert "Soccer Team" in data


def test_signup_and_remove_participant():
    activity = "Soccer Team"
    email = "teststudent@mergington.edu"

    # Ensure not already present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Attempt duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400

    # Remove participant
    resp_del = client.delete(f"/activities/{activity}/participants?email={email}")
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]
