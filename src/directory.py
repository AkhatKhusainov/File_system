from src.file import File
from src.node import Node


class Directory(Node):
    def __init__(self, name: str, owner: str | None = None):
        super().__init__(name=name, owner=owner)
        self.children: list[File | Directory] = []

    # --- Mutations ---------------------------------------------------------
    def add(self, node: Node) -> None:
        if not isinstance(node, Node):
            raise TypeError("add() expects a Node")
        # attach parent and add to children
        node.parent = self
        self.children.append(node)
        self._touch()

    def remove(self, name: str) -> bool:
        for index, child in enumerate(self.children):
            if child.name == name:
                del self.children[index]
                self._touch()
                return True
        # try recursively
        for child in self.children:
            if isinstance(child, Directory) and child.remove(name):
                self._touch()
                return True
        return False

    # --- Queries -----------------------------------------------------------
    def find(self, name: str) -> Node | None:
        if self.name == name:
            return self
        for child in self.children:
            if child.name == name:
                return child
            if isinstance(child, Directory):
                found = child.find(name)
                if found is not None:
                    return found
        return None

    # --- Introspection ----------------------------------------------------
    def size(self) -> int:
        total = 0
        for child in self.children:
            total += child.size()
        return total

    def list_paths(self, prefix: str = "") -> list[str]:
        base = f"{prefix}/{self.name}" if prefix else self.name
        paths: list[str] = []
        for child in self.children:
            paths.extend(child.list_paths(prefix=base))
        return paths

    def tree(self, indent: int = 0) -> str:
        lines: list[str] = []
        lines.append((" " * indent) + f"{self.name}/ ({self.size()} B)")
        for child in self.children:
            lines.append(child.tree(indent=indent + 2))
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "type": "dir",
            "name": self.name,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "children": [child.to_dict() for child in self.children],
        }
