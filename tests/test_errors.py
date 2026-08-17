ENDPOINTS = [
    "/api/v1/topics",
    "/api/v1/explanation?topic_id=quadratic-equations",
    "/api/v1/examples?topic_id=quadratic-equations",
    "/api/v1/questions?topic_id=quadratic-equations",
    "/api/v1/formulae?topic_id=quadratic-equations",
    "/api/v1/sources?topic_id=quadratic-equations",
]


def test_all_endpoints_401_without_key(client, api_base):
    for path in ENDPOINTS:
        resp = client.get(f"{api_base}{path}")
        assert resp.status_code == 401, f"{path} should return 401, got {resp.status_code}"


def test_all_endpoints_401_invalid_key(client, api_base):
    for path in ENDPOINTS:
        resp = client.get(f"{api_base}{path}&api_key=bogus" if "?" in path else f"{api_base}{path}?api_key=bogus")
        assert resp.status_code == 401, f"{path} should return 401, got {resp.status_code}"
