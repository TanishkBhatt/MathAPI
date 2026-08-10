import time
import uuid


def test_auth_success(client, api_base):
    username = "new-test-user"
    email = "new-test-user@test.com"
    resp = client.post(f"{api_base}/auth", json={"username": username, "email": email})
    assert resp.status_code == 201
    data = resp.json()
    assert data["success"] is True
    assert "api_key" in data["api_key_data"]
    assert data["api_key_data"]["username"] == username


def test_auth_duplicate(client, api_base):
    resp = client.post(f"{api_base}/auth", json={"username": "duplicate", "email": "duplicate@test.com"})
    assert resp.status_code == 201
    resp2 = client.post(f"{api_base}/auth", json={"username": "duplicate", "email": "duplicate@test.com"})
    assert resp2.status_code == 201
    assert resp2.json()["success"] is True
    assert resp2.json()["message"] == "User Is Already Authenticated"


def test_auth_missing_username(client, api_base):
    resp = client.post(f"{api_base}/auth", json={"email": "test@test.com"})
    assert resp.status_code == 422


def test_auth_missing_email(client, api_base):
    resp = client.post(f"{api_base}/auth", json={"username": "test"})
    assert resp.status_code == 422


def test_auth_invalid_email(client, api_base):
    resp = client.post(f"{api_base}/auth", json={"username": "test", "email": "not-an-email"})
    assert resp.status_code == 422


def test_auth_returns_expiry(client, api_base):
    username = f"expiry-test-{uuid.uuid4().hex[:12]}"
    email = f"{username}@test.com"
    resp = client.post(f"{api_base}/auth", json={"username": username, "email": email})
    assert resp.status_code == 201
    expiry = resp.json()["api_key_data"]["expiry"]
    assert expiry is not None
    now = time.time()
    assert expiry > now
    assert expiry - now < 186 * 24 * 3600  # ~6 calendar months (with slack)
