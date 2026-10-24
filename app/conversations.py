"""Saves chat conversations as JSON files on this machine.

Conversations can hold company details and photos, so they live in a
git-ignored directory and never become part of the public wiki.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

# Client-generated ids are 32 lowercase hex characters (a UUID without dashes).
# Checking the shape also keeps ids from escaping the storage directory.
ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")


class ConversationStore:
    def __init__(self, directory: Path) -> None:
        self.directory = directory

    def _path(self, conversation_id: str) -> Path | None:
        if not ID_PATTERN.fullmatch(conversation_id):
            return None
        return self.directory / f"{conversation_id}.json"

    def list(self) -> list[dict]:
        if not self.directory.exists():
            return []
        items = []
        for path in self.directory.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            items.append(
                {
                    "id": path.stem,
                    "title": data.get("title", ""),
                    "updated_at": data.get("updated_at", ""),
                    "messages": len(data.get("messages", [])),
                }
            )
        return sorted(items, key=lambda item: item["updated_at"], reverse=True)

    def get(self, conversation_id: str) -> dict | None:
        path = self._path(conversation_id)
        if path is None or not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def save(self, conversation_id: str, title: str, messages: list[dict], meta: dict) -> dict | None:
        path = self._path(conversation_id)
        if path is None:
            return None
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        existing = self.get(conversation_id) or {}
        data = {
            "title": title,
            "created_at": existing.get("created_at", now),
            "updated_at": now,
            "messages": messages,
            "meta": meta,
        }
        self.directory.mkdir(parents=True, exist_ok=True)
        # Write to a temp file first so a crash never leaves a half-written conversation.
        temp = path.with_suffix(".tmp")
        temp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        temp.replace(path)
        return {"id": conversation_id, "updated_at": now}

    def delete(self, conversation_id: str) -> bool:
        path = self._path(conversation_id)
        if path is None or not path.exists():
            return False
        path.unlink()
        return True
