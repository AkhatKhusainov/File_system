from __future__ import annotations

from typing import Optional

from src.node import Node


class File(Node):
    """Regular file node that stores its size in bytes.

    Supports modifying size (which updates `modified_at`) and provides
    implementations for size reporting, path listing, tree view, and dict
    serialization.
    """

    def __init__(self, name: str, size_bytes: int = 0, owner: Optional[str] = None) -> None:
        super().__init__(name=name, owner=owner)
        # File size in bytes. Always stored as int.
        self.size_bytes: int = int(size_bytes)

    # --- Mutations ---------------------------------------------------------
    def modify(self, new_size: Optional[int] = None) -> None:
        """Change file size and update `modified_at` if changed."""
        changed: bool = False
        if new_size is not None and int(new_size) != self.size_bytes:
            self.size_bytes = int(new_size)
            changed = True
        if changed:
            self._touch()

    # --- Introspection ----------------------------------------------------
    def size(self) -> int:
        return self.size_bytes

    def list_paths(self, prefix: str = "") -> list[str]:
        """Return a single path to this file (files are leaves)."""
        base = f"{prefix}/{self.name}" if prefix else self.name
        return [base]

    def tree(self, indent: int = 0) -> str:
        """Return single-line pretty representation of this file."""
        return (" " * indent) + f"{self.name} ({self.size_bytes} B)"

    def to_dict(self) -> dict:
        """JSON-serializable representation of this file."""
        return {
            "type": "file",
            "name": self.name,
            "size": self.size_bytes,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
        }

