def test_topics_success(client, api_base, api_key):
    resp = client.get(f"{api_base}/api/v1/topics?api_key={api_key}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_topics"] >= 10
    assert len(data["topics"]) == data["total_topics"]
    topic = data["topics"][0]
    assert "topic_id" in topic
    assert "topic_name" in topic
    assert "branch" in topic
    assert "difficulty" in topic


def test_topics_missing_key(client, api_base):
    resp = client.get(f"{api_base}/api/v1/topics")
    assert resp.status_code == 401


def test_topics_invalid_key(client, api_base):
    resp = client.get(f"{api_base}/api/v1/topics?api_key=invalid_key_123")
    assert resp.status_code == 401
