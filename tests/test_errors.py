ENDPOINTS = [
    "/api/v1/topics",
    "/api/v1/explanation?topic_id={topic_id}",
    "/api/v1/examples?topic_id={topic_id}",
    "/api/v1/questions?topic_id={topic_id}",
    "/api/v1/formulae?topic_id={topic_id}",
    "/api/v1/sources?topic_id={topic_id}",
]

def test_all_endpoints_401_without_key(client, api_base, topic_id):
    for path in ENDPOINTS:
        path = path.format(topic_id=topic_id)
        resp = client.get(f"{api_base}{path}")
        assert resp.status_code == 401, f"{path} should return 401, got {resp.status_code}"

def test_all_endpoints_401_invalid_key(client, api_base, topic_id):
    for path in ENDPOINTS:
        path = path.format(topic_id=topic_id)
        resp = client.get(f"{api_base}{path}", headers={"X-API-Key": "bogus"})
        assert resp.status_code == 401, f"{path} should return 401, got {resp.status_code}"