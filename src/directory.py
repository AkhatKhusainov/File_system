from src.file import File
from src.node import Node


class Directory(Node):
    def __init__(self, name):
        super().__init__(name)
        self.children: list[File | Directory] = []

    def add(self, node):
        self.children.append(node)

    def size(self) -> int:
        total = 0
        for ch in self.children:
            total += ch.size()
        return total
