from __future__ import annotations

import datetime

from sqlalchemy import (
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from obsidian_gate.models.db import db


class ParsedNote(db.Model): 
    __tablename__ = "parsed_notes"
    __table_args__ = (
        UniqueConstraint("path"),
    )
 
    id: Mapped[int] = mapped_column(primary_key=True)
    path: Mapped[str] = mapped_column(String(4096), index=True)

    mtime: Mapped[float] = mapped_column()
    size: Mapped[int] = mapped_column()
    content_hash: Mapped[str] = mapped_column(String(64), index=True)

    title: Mapped[str] = mapped_column(String(512))
    requires_auth: Mapped[bool] = mapped_column(default=False)
 
    parser_version: Mapped[str] = mapped_column(String(32))
    parsed_content: Mapped[dict] = mapped_column(JSONB)
 
    parsed_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
 
    def __repr__(self) -> str:
        return f"<ParsedNote path={self.path!r}, hash={self.content_hash[:8]}>"
