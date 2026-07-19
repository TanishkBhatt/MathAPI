TOPIC_ID = "quadratic-equations"


def test_questions_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"api_key": api_key, "topic_id": TOPIC_ID},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_questions"] > 0
    q = data["questions"][0]
    assert "question" in q
    assert "options" in q
    assert "answer" in q
    assert "difficulty" in q


def test_questions_with_limit(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"api_key": api_key, "topic_id": TOPIC_ID, "limit": 3},
    )
    assert resp.status_code == 200
    assert resp.json()["total_questions"] == 3


def test_questions_filter_difficulty(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"api_key": api_key, "topic_id": TOPIC_ID, "difficulty": "Beginner"},
    )
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert q["difficulty"] == "Beginner"


def test_questions_filter_type(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"api_key": api_key, "topic_id": TOPIC_ID, "question_type": "Numerical"},
    )
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert "Numerical" in q["question_type"]


def test_questions_invalid_topic(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"api_key": api_key, "topic_id": "non-existent-topic"},
    )
    assert resp.status_code == 404
