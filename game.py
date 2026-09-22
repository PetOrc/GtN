from calculation import GuessingStrategy, NumberGuessingStrategy
from data import Category, DataRepository


class Game:
    """Основная логика игры."""

    def __init__(
        self,
        data_repository: DataRepository | None = None,
        strategy: GuessingStrategy | None = None,
    ):
        self.data_repository = data_repository or DataRepository()
        self.strategy = strategy or NumberGuessingStrategy()

    def get_categories(self) -> list[Category]:
        """Возвращает список доступных категорий."""
        return self.data_repository.get_categories()

    def get_category(self, identifier: str) -> Category | None:
        """Возвращает категорию по идентификатору."""
        return self.data_repository.get_category(identifier)

    def guess(
        self,
        category: Category,
        selected_columns: list[str],
    ) -> dict | None:
        """Определяет объект по выбранным столбцам."""

        if not selected_columns:
            raise ValueError("Не выбран ни один столбец.")

        return self.strategy.find_object(
            category,
            selected_columns,
        )