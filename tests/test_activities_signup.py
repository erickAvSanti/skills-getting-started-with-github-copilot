def test_signup_success_adds_participant(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    before = client.get("/activities").json()[activity_name]["participants"]
    assert email not in before

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    after = client.get("/activities").json()[activity_name]["participants"]
    assert email in after
    assert len(after) == len(before) + 1


def test_signup_activity_not_found_returns_404(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "a@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_already_registered_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_activity_full_returns_400(client):
    activity_name = "Science Olympiad"
    activity = client.get("/activities").json()[activity_name]

    # Fill remaining slots
    remaining_slots = activity["max_participants"] - len(activity["participants"])
    for i in range(remaining_slots):
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": f"fill{i}@mergington.edu"},
        )

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": "overflow@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_success_removes_participant(client):
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    before = client.get("/activities").json()[activity_name]["participants"]
    assert email in before

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    after = client.get("/activities").json()[activity_name]["participants"]
    assert email not in after
    assert len(after) == len(before) - 1


def test_unregister_activity_not_found_returns_404(client):
    response = client.delete(
        "/activities/Unknown Club/participants",
        params={"email": "a@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_not_found_returns_404(client):
    activity_name = "Chess Club"
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": "absent@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
