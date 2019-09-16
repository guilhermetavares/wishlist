import pytest


def test_api_client(api_client):
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {'version': '1.0.0'}
