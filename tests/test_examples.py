def test_examples_success(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/examples",
        params={"topic_id": topic_id},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_examples"] > 0
    example = data["examples"][0]
    assert "question" in example
    assert "answer" in example
    assert "steps" in example

def test_examples_with_limit(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/examples",
        params={"topic_id": topic_id, "limit": 1},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["total_examples"] == 1

def test_examples_invalid_topic(client, api_base, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/examples",
        params={"topic_id": "non-existent-topic"},
        headers=auth_headers,
    )
    assert resp.status_code == 404