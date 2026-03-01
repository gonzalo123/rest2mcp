from datetime import datetime

_notes: dict[int, dict] = {}
_next_id: int = 1


def reset_store() -> None:
    global _notes, _next_id
    _notes = {}
    _next_id = 1


def get_all_notes() -> list[dict]:
    return list(_notes.values())


def get_note(note_id: int) -> dict | None:
    return _notes.get(note_id)


def create_note(title: str, body: str) -> dict:
    global _next_id
    note = {
        "id": _next_id,
        "title": title,
        "body": body,
        "created_at": datetime.now().isoformat(),
    }
    _notes[_next_id] = note
    _next_id += 1
    return note


def update_note(note_id: int, title: str | None = None, body: str | None = None) -> dict | None:
    note = _notes.get(note_id)
    if note is None:
        return None
    if title is not None:
        note["title"] = title
    if body is not None:
        note["body"] = body
    return note


def delete_note(note_id: int) -> bool:
    if note_id in _notes:
        del _notes[note_id]
        return True
    return False
