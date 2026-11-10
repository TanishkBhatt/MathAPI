import os
import uuid
import requests
import pytest

API_BASE = os.getenv("MATHAPI_BASE_URL", "http://127.0.0.1:3000")
TOPIC_ID = os.getenv("MATHAPI_TOPIC_ID", "01_number_system")

@pytest.fixture(scope="session")
def api_base():
    return API_BASE

@pytest.fixture(scope="session")
def topic_id():
    return TOPIC_ID

@pytest.fixture
def client(api_base):
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    yield session

@pytest.fixture
def auth_headers(api_key):
    return {"X-API-Key": api_key}

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