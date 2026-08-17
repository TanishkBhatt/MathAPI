def test_random_question_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/random-question",
        params={"api_key": api_key},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    q = data["question"]
    assert "question" in q
    assert "options" in q
    assert "answer" in q
    assert "difficulty" in q
    assert "topic_id" in q


def test_random_question_missing_key(client, api_base):
    resp = client.get(f"{api_base}/api/v1/random-question")
    assert resp.status_code == 401


def test_random_question_invalid_key(client, api_base):
    resp = client.get(f"{api_base}/api/v1/random-question?api_key=bogus")
    assert resp.status_code == 401
