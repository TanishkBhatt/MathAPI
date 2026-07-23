def test_daily_challenge_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/daily-challenge",
        params={"api_key": api_key},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_questions"] == 3
    assert len(data["questions"]) == 3
    assert "challenge_date" in data
    q = data["questions"][0]
    assert "question" in q
    assert "options" in q
    assert "answer" in q
    assert "difficulty" in q


def test_daily_challenge_missing_key(client, api_base):
    resp = client.get(f"{api_base}/api/v1/daily-challenge")
    assert resp.status_code == 401


def test_daily_challenge_invalid_key(client, api_base):
    resp = client.get(f"{api_base}/api/v1/daily-challenge?api_key=bogus")
    assert resp.status_code == 401
