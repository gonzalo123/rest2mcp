from flask import Blueprint, request, jsonify

from lib.store import get_all_notes, get_note, create_note, update_note, delete_note

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/api/notes", methods=["GET"])
def list_notes():
    return jsonify(get_all_notes())


@notes_bp.route("/api/notes/<int:note_id>", methods=["GET"])
def read_note(note_id: int):
    note = get_note(note_id)
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note)


@notes_bp.route("/api/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    note = create_note(title=data["title"], body=data.get("body", ""))
    return jsonify(note), 201


@notes_bp.route("/api/notes/<int:note_id>", methods=["PUT"])
def edit_note(note_id: int):
    data = request.get_json()
    note = update_note(note_id, title=data.get("title"), body=data.get("body"))
    if note is None:
        return jsonify({"error": "Note not found"}), 404
    return jsonify(note)


@notes_bp.route("/api/notes/<int:note_id>", methods=["DELETE"])
def remove_note(note_id: int):
    if delete_note(note_id):
        return jsonify({"status": "deleted"})
    return jsonify({"error": "Note not found"}), 404
