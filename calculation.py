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
    """Стратегия определения объекта по сумме значений столбцов."""

    def find_object(
        self,
        category: Any,
        selected_columns: list[str],
    ) -> dict | None:
        base_values = self.determine_base_values(
            category,
            selected_columns,
        )

        total = self.sum_values(base_values)

        return self.find_object_by_number(category, total)

    def determine_base_values(
        self,
        category: Any,
        selected_columns: list[str],
    ) -> list[int]:
        """Определяет базовые значения выбранных столбцов."""
        column_values = category.get_column_values()

        values = []

        for column_id in selected_columns:
            if column_id not in column_values:
                raise ValueError(
                    f"Неизвестный столбец: {column_id}"
                )

            values.append(column_values[column_id])

        return values

    @staticmethod
    def sum_values(values: list[int]) -> int:
        """Суммирует значения выбранных столбцов."""
        return sum(values)

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