import pytest

from starlette.testclient import TestClient
from app.main import app

from app.models import Customer as MongoCustomer


@pytest.fixture
def api_client():
    client = TestClient(app)
    return client
