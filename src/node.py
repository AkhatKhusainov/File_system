from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


class Node:
    """Base filesystem node with common metadata and helpers.

    Provides:
    - name and optional owner metadata
    - created_at and modified_at timestamps
    - parent reference (set by Directory.add)
    - rename() operation that updates modified_at
    - abstract methods to be implemented by subclasses
    """

    def __init__(self, name: str, owner: Optional[str] = None) -> None:
        self.name: str = name
        self.owner: Optional[str] = owner
        self.created_at: datetime = datetime.now()
        self.modified_at: datetime = datetime.now()
        self.parent: Optional["Directory"] = None

    # --- Metadata helpers -------------------------------------------------
    def _touch(self) -> None:
        """Update the modification timestamp to current time."""
        self.modified_at = datetime.now()

    def rename(self, new_name: str) -> None:
        """Rename node and update `modified_at` if name actually changes."""
        if not isinstance(new_name, str) or new_name == "":
            raise ValueError("new_name must be a non-empty string")
        if new_name != self.name:
            self.name = new_name
            self._touch()

    # --- Introspection ----------------------------------------------------
    def size(self) -> int:
        """Return node size in bytes. Must be implemented by subclasses."""
        raise NotImplementedError("size() is not implemented for Node")

    def list_paths(self, prefix: str = "") -> list[str]:
        """Return list of full file paths. Must be implemented by subclasses."""
        raise NotImplementedError("list_paths() is not implemented for Node")

    def tree(self, indent: int = 0) -> str:
        """Return pretty-printed tree. Must be implemented by subclasses."""
        raise NotImplementedError("tree() is not implemented for Node")

    def to_dict(self) -> dict:
        """Return JSON-serializable dict. Must be implemented by subclasses."""
        raise NotImplementedError("to_dict() is not implemented for Node")

