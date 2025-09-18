from src.file import File
from src.node import Node


class Directory(Node):
    """Директория (папка), содержит список дочерних узлов.

    Дочерние узлы могут быть как файлами, так и другими директориями.
    """

    def __init__(self, name: str, owner: str | None = None):
        super().__init__(name=name, owner=owner)
        self.children: list[Node] = []

    # --- Mutations ---------------------------------------------------------
    def add(self, node: Node) -> None:
        """Добавить узел в директорию и обновить modified_at.

        Также проставляем обратную ссылку node.parent на текущую директорию.
        """
        if not isinstance(node, Node):
            raise TypeError("add() expects a Node")
        # attach parent and add to children
        node.parent = self
        self.children.append(node)
        self._touch()

    # --- Queries -----------------------------------------------------------

    # --- Introspection ----------------------------------------------------
    def size(self) -> int:
        """Суммарный размер всех дочерних узлов (в байтах)."""
        total = 0
        for child in self.children:
            total += child.size()
        return total

    def list_paths(self, prefix: str = "") -> list[str]:
        """Вернуть все пути файлов внутри директории рекурсивно."""
        base = f"{prefix}/{self.name}" if prefix else self.name
        paths: list[str] = []
        for child in self.children:
            paths.extend(child.list_paths(prefix=base))
        return paths

    def tree(self, indent: int = 0) -> str:
        """Вернуть строковое представление дерева с размерами.

        Директория выводится как "name/ (SIZE B)", далее дети с отступом.
        """
        lines: list[str] = []
        lines.append((" " * indent) + f"{self.name}/ ({self.size()} B)")
        for child in self.children:
            lines.append(child.tree(indent=indent + 2))
        return "\n".join(lines)

    def to_dict(self) -> dict:
        """Рекурсивно упаковать директорию и всех детей в словарь."""
        return {
            "type": "dir",
            "name": self.name,
            "owner": self.owner,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat(),
            "children": [child.to_dict() for child in self.children],
        }
