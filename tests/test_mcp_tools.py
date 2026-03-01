import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from server.main import list_notes, get_note, create_note, update_note, delete_note


def _mock_response(data):
    mock = MagicMock()
    mock.text = json.dumps(data)
    return mock


@patch("server.main.requests.get")
def test_list_notes(mock_get):
    mock_get.return_value = _mock_response([{"id": 1, "title": "Note 1"}])
    result = json.loads(list_notes())
    assert len(result) == 1
    assert result[0]["title"] == "Note 1"


@patch("server.main.requests.get")
def test_get_note(mock_get):
    mock_get.return_value = _mock_response({"id": 1, "title": "Note 1"})
    result = json.loads(get_note(1))
    assert result["id"] == 1


@patch("server.main.requests.post")
def test_create_note(mock_post):
    mock_post.return_value = _mock_response({"id": 1, "title": "New", "body": "Content"})
    result = json.loads(create_note("New", "Content"))
    assert result["title"] == "New"


@patch("server.main.requests.put")
def test_update_note(mock_put):
    mock_put.return_value = _mock_response({"id": 1, "title": "Updated"})
    result = json.loads(update_note(1, title="Updated"))
    assert result["title"] == "Updated"


@patch("server.main.requests.delete")
def test_delete_note(mock_delete):
    mock_delete.return_value = _mock_response({"status": "deleted"})
    result = json.loads(delete_note(1))
    assert result["status"] == "deleted"
