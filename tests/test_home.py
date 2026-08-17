def test_home_success(client, api_base):
    resp = client.get(f"{api_base}/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["message"] == "MathAPI - API Services"
    assert "help" in data
    assert "docs" in data
    assert "repo" in data
    assert "author" in data
