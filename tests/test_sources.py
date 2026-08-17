TOPIC_ID = "quadratic-equations"


def test_sources_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/sources",
        params={"api_key": api_key, "topic_id": TOPIC_ID},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_sources"] > 0
    source = data["learning_sources"][0]
    assert "title" in source
    assert "type" in source
    assert "link" in source


def test_sources_invalid_topic(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/sources",
        params={"api_key": api_key, "topic_id": "non-existent-topic"},
    )
    assert resp.status_code == 404
