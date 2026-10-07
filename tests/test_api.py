"""Integration tests for the spec-first connexion app (in-process client)."""

from typing import cast

import pytest
from starlette.testclient import TestClient

from driven_dev.api import APP_VERSION, create_app


@pytest.fixture()
def client() -> TestClient:
    return cast(TestClient, create_app().test_client())


def test_health_returns_ok_and_version(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": APP_VERSION}


def test_health_rejects_unknown_query_params(client: TestClient) -> None:
    response = client.get("/health?bogus=1")
    assert response.status_code == 400


def test_unknown_path_is_404(client: TestClient) -> None:
    assert client.get("/nope").status_code == 404
