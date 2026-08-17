import os
import uuid
import requests
import pytest

API_BASE = "http://127.0.0.1:3000"

@pytest.fixture(scope="session")
def api_base():
    return API_BASE

@pytest.fixture
def client(api_base):
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session

@pytest.fixture(scope="session")
def api_key(api_base):
    username = f"test-user-{uuid.uuid4().hex[:12]}"
    email = f"{username}@test.com"
    resp = requests.post(
        f"{api_base}/auth",
        json={"username": username, "email": email},
        timeout=15,
    )
    assert resp.status_code == 201, f"Auth failed: {resp.text}"
    return resp.json()["api_key_data"]["api_key"]

@pytest.fixture
def admin_token():
    token = os.environ.get("ADMIN_TOKEN")
    if not token:
        pytest.skip("ADMIN_TOKEN not set — skipping admin-only tests")
    return token
