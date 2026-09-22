import os

from app.app import app


def test_environment():
    client = app.test_client()

    response = client.get("/environment")

    assert response.status_code == 200


def test_version():
    client = app.test_client()

    response = client.get("/version")

    assert response.status_code == 200


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")

    # Database may not be running during unit testing,
    # so verify the endpoint exists.
    assert response.status_code in [200, 503]
