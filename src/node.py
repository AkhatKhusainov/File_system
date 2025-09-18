from __future__ import annotations

from datetime import datetime
from typing import Optional


class Node:
    """Базовый узел файловой системы.

    Содержит общие поля и логику:
    - name: имя узла (файла или директории)
    - owner: владелец (строка или None)
    - created_at: время создания
    - modified_at: время последнего изменения
    - parent: родительская директория (или None для корня)

    Абстрактные методы size(), list_paths(), tree(), to_dict() должны
    быть реализованы в наследниках (File и Directory).
    """

    def __init__(self, name: str, owner: Optional[str] = None) -> None:
        self.name: str = name
        self.owner: Optional[str] = owner
        self.created_at: datetime = datetime.now()
        self.modified_at: datetime = datetime.now()
        self.parent: Optional["Directory"] = None

    # --- Metadata helpers -------------------------------------------------
    def _touch(self) -> None:
        """Обновить поле modified_at текущим временем.

        Небольшой внутренний хелпер, чтобы в одном месте менять время
        модификации при любых изменениях (add/rename/modify и т.п.).
        """
        self.modified_at = datetime.now()

    def rename(self, new_name: str) -> None:
        """Переименовать узел и обновить modified_at.

        Поднимаем ValueError, если имя пустое или не строка.
        """
        if not isinstance(new_name, str) or new_name == "":
            raise ValueError("new_name must be a non-empty string")
        if new_name != self.name:
            self.name = new_name
            self._touch()

    # --- Introspection ----------------------------------------------------
    def size(self) -> int:
        """Вернуть размер узла в байтах.

        Для файла — это фактический размер, для директории — сумма
        размеров всех дочерних узлов.
        """
        raise NotImplementedError("size() is not implemented for Node")

    def list_paths(self, prefix: str = "") -> list[str]:
        """Вернуть список ПОЛНЫХ путей до всех файлов внутри узла.

        Для файла — список из одного элемента. Для директории —
        рекурсивный обход детей с добавлением собственного имени к префиксу.
        """
        raise NotImplementedError("list_paths() is not implemented for Node")

    def tree(self, indent: int = 0) -> str:
        """Вернуть «красивое» строковое представление дерева.

        Отступ indent задаёт количество пробелов слева для текущего уровня.
        Директории заканчиваются на "/", рядом указываем суммарный размер.
        Файлы показывают собственный размер.
        """
        raise NotImplementedError("tree() is not implemented for Node")

    def to_dict(self) -> dict:
        """Вернуть словарь с данными и метаданными узла."""
        raise NotImplementedError("to_dict() is not implemented for Node")

