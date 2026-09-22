from abc import ABC, abstractmethod
from typing import Any


class GuessingStrategy(ABC):
    """Абстрактная стратегия определения объекта."""

    @abstractmethod
    def find_object(
        self,
        category: Any,
        selected_columns: list[str],
    ) -> dict | None:
        """Определяет объект по выбранным столбцам."""
        raise NotImplementedError


class NumberGuessingStrategy(GuessingStrategy):
    """Стратегия определения числа по выбранным столбцам."""

    COLUMN_VALUES = {
        "1": 16,
        "2": 8,
        "3": 4,
        "4": 2,
        "5": 1,
    }

    def calculate_number(
        self,
        selected_columns: list[str],
    ) -> int:
        """Вычисляет число по выбранным столбцам."""

        total = 0

        for column_id in selected_columns:
            if column_id not in self.COLUMN_VALUES:
                raise ValueError(
                    f"Неизвестный столбец: {column_id}"
                )

            total += self.COLUMN_VALUES[column_id]

        return total

    def find_object(
        self,
        category: Any,
        selected_columns: list[str],
    ) -> dict | None:
        """Определяет объект по выбранным столбцам."""

        number = self.calculate_number(selected_columns)

        return self.find_object_by_number(
            category,
            number,
        )

    @staticmethod
    def find_object_by_number(
        category: Any,
        number: int,
    ) -> dict | None:
        """Находит объект с заданным номером."""

        for obj in category.get_object_table():
            if int(obj["number"]) == number:
                return obj

        return None