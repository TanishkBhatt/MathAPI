def test_questions_success(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"topic_id": topic_id},
        headers=auth_headers,
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

def test_questions_with_limit(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"topic_id": topic_id, "limit": 3},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["total_questions"] == 3

def test_questions_filter_difficulty(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"topic_id": topic_id, "difficulty": "Beginner"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert q["difficulty"] == "Beginner"

def test_questions_filter_type(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"topic_id": topic_id, "question_type": "Numerical"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert "Numerical" in q["question_type"]

def test_questions_invalid_topic(client, api_base, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/questions",
        params={"topic_id": "non-existent-topic"},
        headers=auth_headers,
    )
    assert resp.status_code == 404