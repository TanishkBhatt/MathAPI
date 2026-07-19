def test_contribute_missing_admin_token(client, api_base):
    resp = client.post(f"{api_base}/contribute", json=[{"topic_id": "test"}])
    assert resp.status_code == 422


def test_contribute_invalid_admin_token(client, api_base):
    resp = client.post(
        f"{api_base}/contribute?admin_token=wrong-token",
        json=[{"topic_id": "quadratic-equations"}],
    )
    assert resp.status_code == 401


def test_contribute_valid_admin_token(client, api_base, admin_token):
    resp = client.post(
        f"{api_base}/contribute?admin_token={admin_token}&contribution_type=Question",
        json=[{"topic_id": "test"}],
    )
    assert resp.status_code == 422
