def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_get_activities_returns_expected_activity_shape(client):
    response = client.get("/activities")

    assert response.status_code == 200

    chess_club = response.json()["Chess Club"]
    assert set(chess_club.keys()) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert isinstance(chess_club["participants"], list)
