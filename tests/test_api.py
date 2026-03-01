import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest

from api.app import create_app
from lib.store import reset_store


@pytest.fixture(autouse=True)
def clean_store():
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_list_notes_empty(client):
    response = client.get("/api/notes")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_note(client):
    response = client.post("/api/notes", json={"title": "Test", "body": "Hello"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["title"] == "Test"
    assert data["body"] == "Hello"
    assert "id" in data


def test_create_note_without_title(client):
    response = client.post("/api/notes", json={"body": "No title"})
    assert response.status_code == 400


def test_get_note(client):
    client.post("/api/notes", json={"title": "Test"})
    response = client.get("/api/notes/1")
    assert response.status_code == 200
    assert response.get_json()["title"] == "Test"


def test_get_note_not_found(client):
    response = client.get("/api/notes/999")
    assert response.status_code == 404


def test_update_note(client):
    client.post("/api/notes", json={"title": "Old"})
    response = client.put("/api/notes/1", json={"title": "New"})
    assert response.status_code == 200
    assert response.get_json()["title"] == "New"


def test_delete_note(client):
    client.post("/api/notes", json={"title": "ToDelete"})
    response = client.delete("/api/notes/1")
    assert response.status_code == 200
    response = client.get("/api/notes/1")
    assert response.status_code == 404
