__all__ = [
    "notes_bp",
]

import flask
from sqlalchemy.sql import select

from obsidian_gate.models import ParsedNote
from obsidian_gate.models.db import db

notes_bp = flask.Blueprint("notes", __name__, url_prefix="/notes")


@notes_bp.route("/")
def list_notes():
    notes = db.session.execute(select(ParsedNote.title))
    return flask.jsonify({"notes": list(notes)})


@notes_bp.route("/<int:note_id>")
def get_notes(note_id: int):
    note = db.session.execute(select(ParsedNote).where(ParsedNote.id == note_id)).one_or_none()
    if note is None:
        return flask.jsonify({"error": "Note does not exist"})

    return flask.jsonify(dict(note))
