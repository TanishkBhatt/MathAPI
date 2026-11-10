def test_formulae_success(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/formulae",
        params={"topic_id": topic_id},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_formulae"] > 0
    formula = data["formulae"][0]
    assert "title" in formula
    assert "code" in formula

def test_formulae_invalid_topic(client, api_base, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/formulae",
        params={"topic_id": "non-existent-topic"},
        headers=auth_headers,
    )
    assert resp.status_code == 404