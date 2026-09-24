import json
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Category:
    identifier: str
    name: str
    columns: list[dict]
    objects: list[dict]

    def get_column_values(self) -> dict[str, int]:
        return {
            str(column["id"]): int(column["value"])
            for column in self.columns
        }

    def get_object_table(self) -> list[dict]:
        return self.objects

class DataRepository:
    def __init__(self, file_path: str | Path | None = None):
        if file_path is None:
            file_path = (
                Path(__file__).resolve().parent
                / "data"
                / "data.json"
            )

        self.file_path = Path(file_path)
        self._categories: list[Category] = []

        self.load()

    def load(self) -> None:
        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self._categories = []

        for category_data in data["categories"]:
            category = Category(
                identifier=str(category_data["id"]),
                name=str(category_data["name"]),
                columns=category_data["columns"],
                objects=category_data["objects"],
            )

            self._categories.append(category)

    def get_categories(self) -> list[Category]:
        return self._categories

    def get_category(self, identifier: str) -> Category | None:
        for category in self._categories:
            if category.identifier == identifier:
                return category

        return None