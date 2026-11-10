def test_sources_success(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/sources",
        params={"topic_id": topic_id},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_sources"] > 0
    source = data["sources"][0]
    assert "title" in source
    assert "type" in source
    assert "link" in source

def test_sources_invalid_topic(client, api_base, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/sources",
        params={"topic_id": "non-existent-topic"},
        headers=auth_headers,
    )
    assert resp.status_code == 404