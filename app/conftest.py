import pytest
from fastapi.testclient import TestClient
from main import app
from security import RateLimiter

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture()
def clear_rate_limit_storage():
    RateLimiter.clear_storage()
    yield
    RateLimiter.clear_storage()