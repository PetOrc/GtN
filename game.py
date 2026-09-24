from calculation import GuessingStrategy, NumberGuessingStrategy
from data import Category, DataRepository

class Game:
    def __init__(self, data_repository: DataRepository | None = None, strategy: GuessingStrategy | None = None):
        self.data_repository = data_repository or DataRepository()
        self.strategy = strategy or NumberGuessingStrategy()

    def get_categories(self) -> list[Category]:
        return self.data_repository.get_categories()

    def get_category(self, identifier: str) -> Category | None:
        return self.data_repository.get_category(identifier)

    def calculate_number(self, selected_columns: list[str]) -> int:
        if not selected_columns:
            raise ValueError("Не выбран ни один столбец.")

        return self.strategy.calculate_number(selected_columns)

    def guess(self, category: Category, selected_columns: list[str]) -> dict | None:
        if not selected_columns:
            raise ValueError("Не выбран ни один столбец.")

        return self.strategy.find_object(category, selected_columns)