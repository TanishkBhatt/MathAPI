TOPIC_ID = "quadratic-equations"


def test_formulae_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/formulae",
        params={"api_key": api_key, "topic_id": TOPIC_ID},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["total_formulae"] > 0
    formula = data["formulae"][0]
    assert "title" in formula
    assert "code" in formula


def test_formulae_invalid_topic(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/formulae",
        params={"api_key": api_key, "topic_id": "non-existent-topic"},
    )
    assert resp.status_code == 404
