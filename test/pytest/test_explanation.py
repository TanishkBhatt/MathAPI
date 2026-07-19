TOPIC_ID = "quadratic-equations"


def test_explanation_success(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={"api_key": api_key, "topic_id": TOPIC_ID},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert "definition" in data["explanation"]
    assert "origin" in data["explanation"]


def test_explanation_with_all_includes(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={
            "api_key": api_key,
            "topic_id": TOPIC_ID,
            "include_formulae": True,
            "include_examples": True,
            "include_questions": True,
            "include_sources": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["explanation"]["formulae"]) > 0
    assert len(data["explanation"]["solved_examples"]) > 0
    assert len(data["explanation"]["try_yourself_questions"]) > 0
    assert len(data["explanation"]["learning_sources"]) > 0


def test_explanation_without_includes(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={"api_key": api_key, "topic_id": TOPIC_ID},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["explanation"]["formulae"] == []
    assert data["explanation"]["solved_examples"] == []
    assert data["explanation"]["try_yourself_questions"] == []
    assert data["explanation"]["learning_sources"] == []


def test_explanation_invalid_topic(client, api_base, api_key):
    resp = client.get(
        f"{api_base}/api/v1/explanation",
        params={"api_key": api_key, "topic_id": "non-existent-topic"},
    )
    assert resp.status_code == 404


def test_explanation_missing_topic_id(client, api_base, api_key):
    resp = client.get(f"{api_base}/api/v1/explanation?api_key={api_key}")
    assert resp.status_code == 422
