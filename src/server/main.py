import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import requests
from mcp.server.fastmcp import FastMCP

from settings import API_BASE_URL

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    level=logging.INFO,
    datefmt="%d/%m/%Y %X",
)

logger = logging.getLogger(__name__)

mcp = FastMCP(name="notes-api")

BASE = API_BASE_URL


@mcp.tool()
def list_notes() -> str:
    """List all notes stored in the system.

    Returns a JSON array of note objects, each containing:
    id, title, body, and created_at fields.
    """
    response = requests.get(f"{BASE}/api/notes")
    return response.text


@mcp.tool()
def get_note(note_id: int) -> str:
    """Get a single note by its ID.

    Returns the note object with id, title, body, and created_at fields.
    Returns an error if the note is not found.
    """
    response = requests.get(f"{BASE}/api/notes/{note_id}")
    return response.text


@mcp.tool()
def create_note(title: str, body: str = "") -> str:
    """Create a new note.

    Args:
        title: The title of the note (required).
        body: The body content of the note (optional, defaults to empty string).

    Returns the created note object with its assigned id.
    """
    response = requests.post(
        f"{BASE}/api/notes",
        json={"title": title, "body": body},
    )
    return response.text


@mcp.tool()
def update_note(note_id: int, title: str = "", body: str = "") -> str:
    """Update an existing note by its ID.

    Args:
        note_id: The ID of the note to update.
        title: New title for the note (optional, send empty string to keep current).
        body: New body for the note (optional, send empty string to keep current).

    Returns the updated note object, or an error if not found.
    """
    payload = {}
    if title:
        payload["title"] = title
    if body:
        payload["body"] = body
    response = requests.put(
        f"{BASE}/api/notes/{note_id}",
        json=payload,
    )
    return response.text


@mcp.tool()
def delete_note(note_id: int) -> str:
    """Delete a note by its ID.

    Args:
        note_id: The ID of the note to delete.

    Returns a status confirmation or an error if the note is not found.
    """
    response = requests.delete(f"{BASE}/api/notes/{note_id}")
    return response.text


if __name__ == "__main__":
    mcp.run()
