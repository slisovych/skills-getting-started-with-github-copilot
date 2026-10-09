from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_signup_rejects_duplicate_registration():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()
