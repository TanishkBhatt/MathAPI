TOPIC_ID = "quadratic-equations"


def test_examples_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/examples",
        params={"api_key": api_key, "topic_id": TOPIC_ID},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_examples"] > 0
    example = data["examples"][0]
    assert "question" in example
    assert "answer" in example
    assert "steps" in example


def test_examples_with_limit(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/examples",
        params={"api_key": api_key, "topic_id": TOPIC_ID, "limit": 1},
    )
    assert resp.status_code == 200
    assert resp.json()["total_examples"] == 1


def test_examples_invalid_topic(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/examples",
        params={"api_key": api_key, "topic_id": "non-existent-topic"},
    )
    assert resp.status_code == 404
