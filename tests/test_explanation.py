def test_explanation_success(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={"topic_id": topic_id},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "definition" in data["explanation"]
    assert "origin" in data["explanation"]

def test_explanation_with_all_includes(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={
            "topic_id": topic_id,
            "include_formulae": True,
            "include_examples": True,
            "include_questions": True,
            "include_sources": True,
        },
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["explanation"]["formulae"]) > 0
    assert len(data["explanation"]["solved_examples"]) > 0
    assert len(data["explanation"]["try_yourself_questions"]) > 0
    assert len(data["explanation"]["sources"]) > 0

def test_explanation_without_includes(client, api_base, topic_id, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={"topic_id": topic_id},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["explanation"]["formulae"] == []
    assert data["explanation"]["solved_examples"] == []
    assert data["explanation"]["try_yourself_questions"] == []
    assert data["explanation"]["sources"] == []

def test_explanation_invalid_topic(client, api_base, auth_headers):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={"topic_id": "non-existent-topic"},
        headers=auth_headers,
    )
    assert resp.status_code == 404

def test_explanation_missing_topic_id(client, api_base, auth_headers):
    resp = client.get(f"{api_base}/api/v1/explanation", headers=auth_headers)
    assert resp.status_code == 422