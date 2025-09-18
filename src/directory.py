from src.file import File
from src.node import Node


class Directory(Node):
    """Directory node that can contain files and subdirectories.

    Responsibilities:
    - store children
    - update metadata (`modified_at`) on structural changes
    - provide aggregated `size`, listing of file paths, tree view, and dict representation
    """

    def __init__(self, name: str, owner: str | None = None):
        super().__init__(name=name, owner=owner)
        # Child nodes contained in this directory. Only File or Directory instances are allowed.
        self.children: list[File | Directory] = []

    # --- Mutations ---------------------------------------------------------
    def add(self, node: Node) -> None:
        """Add a child node and update metadata.

        - sets child's parent to this directory
        - appends to children list
        - touches this directory's modified_at
        """
        if not isinstance(node, Node):
            raise TypeError("add() expects a Node")
        node.parent = self
        self.children.append(node)
        self._touch()

    # --- Introspection ----------------------------------------------------
    def size(self) -> int:
        """Total size of all children (recursive)."""
        total = 0
        for child in self.children:
            total += child.size()
        return total

    def list_paths(self, prefix: str = "") -> list[str]:
        """Return full paths of all files under this directory.

        Directories themselves are not included in the output, only files.
        """
        base = f"{prefix}/{self.name}" if prefix else self.name
        paths: list[str] = []
        for child in self.children:
            paths.extend(child.list_paths(prefix=base))
        return paths

    def tree(self, indent: int = 0) -> str:
        """Pretty-printed multiline tree with sizes."""
        lines: list[str] = []
        lines.append((" " * indent) + f"{self.name}/ ({self.size()} B)")
        for child in self.children:
            lines.append(child.tree(indent=indent + 2))
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Recursive, JSON-serializable representation of this directory."""
        return {
            "type": "dir",
            "name": self.name,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "children": [child.to_dict() for child in self.children],
        }
