"""Automated checks for every endpoint of the API."""

import pytest
from fastapi.testclient import TestClient

from app.main import APP_VERSION, app, items

client = TestClient(app)


@pytest.fixture(autouse=True)
def empty_database():
    """Give every test a clean, empty database."""
    items.clear()
    yield
    items.clear()


def test_health_returns_ok_and_version():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": APP_VERSION}


def test_create_item_returns_201_and_the_item():
    response = client.post("/items", json={"name": "coffee", "price": 2.5})
    assert response.status_code == 201
    assert response.json() == {"id": 1, "name": "coffee", "price": 2.5}


def test_list_items_starts_empty():
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []


def test_get_missing_item_returns_404():
    response = client.get("/items/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item_without_price_returns_422():
    response = client.post("/items", json={"name": "tea"})
    assert response.status_code == 422


def test_get_existing_item_returns_it():
    created = client.post("/items", json={"name": "tea", "price": 1.5}).json()
    response = client.get(f"/items/{created['id']}")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "tea", "price": 1.5}
