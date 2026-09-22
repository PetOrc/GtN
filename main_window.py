from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from game import Game


class ThemeToggle(QCheckBox):
    """Переключатель светлой и тёмной темы."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(54, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Переключить тему")
        self.setChecked(False)

    def mouseReleaseEvent(self, event):
        """Переключает состояние при нажатии мышью."""

        if event.button() == Qt.MouseButton.LeftButton:
            self.setChecked(not self.isChecked())
            self.update()
            event.accept()
            return

        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        """Отрисовывает переключатель."""

        from PySide6.QtGui import QBrush, QColor, QPainter

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.isChecked():
            track_color = QColor("#3b4654")
        else:
            track_color = QColor("#dfe3e8")

        painter.setBrush(QBrush(track_color))
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            14,
            14,
        )

        if self.isChecked():
            circle_x = 29
            circle_color = QColor("#f4f6f8")
        else:
            circle_x = 3
            circle_color = QColor("#ffffff")

        painter.setBrush(QBrush(circle_color))

        painter.drawEllipse(
            circle_x,
            3,
            22,
            22,
        )

        painter.setPen(
            QColor("#66717d")
            if not self.isChecked()
            else QColor("#3b4654")
        )

        painter.drawText(
            5 if not self.isChecked() else 32,
            18,
            "☀" if not self.isChecked() else "☾",
        )


class MainWindow(QMainWindow):
    """Главное окно игры «Угадай число»."""

    def __init__(self):
        super().__init__()

        self.game = Game()

        self.setWindowTitle("Угадай число")
        self.resize(1000, 700)
        self.setMinimumSize(600, 600)

        self.column_checkboxes = []
        self.last_selected_columns = None

        # Категория «Числа» выбрана по умолчанию.
        self.current_category = self.game.get_category("4")

        self.create_interface()
        self.load_style("light.qss")

        self.refresh_category_table()

    def create_interface(self):
        """Создаёт интерфейс главного окна."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        category_layout = QHBoxLayout()
        category_layout.setSpacing(7)

        self.numbers_button = QPushButton("Числа")
        self.cities_button = QPushButton("Города")
        self.names_button = QPushButton("Имена")
        self.plants_button = QPushButton("Растения")
        self.animals_button = QPushButton("Животные")
        self.help_button = QPushButton("Справка")

        self.theme_toggle = ThemeToggle()
        self.theme_toggle.toggled.connect(self.toggle_theme)

        # Порядок кнопок соответствует порядку категорий:
        # Числа → Города → Имена → Растения → Животные.
        category_buttons = [
            self.numbers_button,
            self.cities_button,
            self.names_button,
            self.plants_button,
            self.animals_button,
        ]

        for button in category_buttons:
            button.setMinimumHeight(34)
            button.setSizePolicy(
                button.sizePolicy().Policy.Expanding,
                button.sizePolicy().Policy.Fixed,
            )
            category_layout.addWidget(button)

        self.help_button.setMinimumWidth(85)
        self.help_button.setMinimumHeight(34)

        category_layout.addSpacing(15)
        category_layout.addWidget(self.help_button)
        category_layout.addWidget(self.theme_toggle)

        main_layout.addLayout(category_layout)

        # Подключение категорий.
        self.numbers_button.clicked.connect(
            lambda: self.select_category("4")
        )
        self.cities_button.clicked.connect(
            lambda: self.select_category("2")
        )
        self.names_button.clicked.connect(
            lambda: self.select_category("5")
        )
        self.plants_button.clicked.connect(
            lambda: self.select_category("3")
        )
        self.animals_button.clicked.connect(
            lambda: self.select_category("1")
        )

        # По умолчанию активна категория «Числа».
        self.numbers_button.setObjectName("activeCategory")

        # =================================================
        # Таблица
        # =================================================

        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")

        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(8, 8, 8, 8)
        table_layout.setSpacing(0)

        checkbox_layout = QGridLayout()
        checkbox_layout.setContentsMargins(0, 0, 0, 4)
        checkbox_layout.setHorizontalSpacing(0)

        for column_number in range(5):
            checkbox = QCheckBox(
                f"Столбец {column_number + 1}"
            )

            checkbox.setObjectName("columnCheckBox")

            checkbox.stateChanged.connect(
                self.columns_changed
            )

            checkbox_layout.addWidget(
                checkbox,
                0,
                column_number,
                alignment=Qt.AlignmentFlag.AlignCenter,
            )

            self.column_checkboxes.append(checkbox)

        table_layout.addLayout(checkbox_layout)

        self.table = QTableWidget()
        self.table.setObjectName("numberTable")

        self.table.setColumnCount(5)

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection
        )

        self.table.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        for column in range(5):
            self.table.horizontalHeader().setSectionResizeMode(
                column,
                self.table.horizontalHeader().ResizeMode.Stretch,
            )

        self.table.verticalHeader().setSectionResizeMode(
            self.table.verticalHeader().ResizeMode.Stretch
        )

        table_layout.addWidget(self.table)

        main_layout.addWidget(
            table_frame,
            stretch=1,
        )

        # =================================================
        # Нижняя панель
        # =================================================

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(12)

        result_frame = QFrame()
        result_frame.setObjectName("resultFrame")

        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(10, 4, 10, 4)

        self.result_label = QLabel(
            "Заданный объект: —"
        )

        self.result_label.setObjectName("resultLabel")

        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        result_layout.addWidget(self.result_label)

        bottom_layout.addWidget(
            result_frame,
            stretch=1,
        )

        self.action_button = QPushButton(
            "Показать результат"
        )

        self.action_button.setObjectName("actionButton")
        self.action_button.setMinimumWidth(150)
        self.action_button.setMinimumHeight(42)

        self.action_button.clicked.connect(
            self.handle_action
        )

        bottom_layout.addWidget(
            self.action_button
        )

        main_layout.addLayout(bottom_layout)

    def load_style(self, filename: str):
        """Загружает стиль интерфейса из QSS-файла."""

        style_path = (
            Path(__file__).resolve().parent
            / "styles"
            / filename
        )

        with style_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            self.setStyleSheet(file.read())

    def toggle_theme(self, dark: bool):
        """Переключает тему интерфейса."""

        if dark:
            self.load_style("dark.qss")
        else:
            self.load_style("light.qss")

    def select_category(self, category_id: str):
        """Выбирает категорию игры."""

        category = self.game.get_category(category_id)

        if category is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось загрузить выбранную категорию.",
            )
            return

        self.current_category = category

        for checkbox in self.column_checkboxes:
            checkbox.setChecked(False)

        self.last_selected_columns = None

        self.result_label.setText(
            "Заданный объект: —"
        )

        self.action_button.setText(
            "Показать результат"
        )

        category_button_map = {
            "4": self.numbers_button,
            "2": self.cities_button,
            "5": self.names_button,
            "3": self.plants_button,
            "1": self.animals_button,
        }

        category_buttons = [
            self.numbers_button,
            self.cities_button,
            self.names_button,
            self.plants_button,
            self.animals_button,
        ]

        for button in category_buttons:
            button.setObjectName("")

        active_button = category_button_map.get(category_id)

        if active_button is not None:
            active_button.setObjectName("activeCategory")

        self.refresh_category_table()

        # Обновляем оформление после изменения objectName.
        for button in category_buttons:
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def refresh_category_table(self):
        """Заполняет таблицу данными выбранной категории."""

        if self.current_category is None:
            return

        objects = self.current_category.get_object_table()

        column_objects = []

        for column_number in range(1, 6):
            column_id = str(column_number)

            objects_in_column = [
                obj
                for obj in objects
                if column_id in obj.get("columns", [])
            ]

            column_objects.append(objects_in_column)

        row_count = max(
            len(column)
            for column in column_objects
        )

        self.table.clearContents()
        self.table.setRowCount(row_count)

        for column_index, objects_in_column in enumerate(
            column_objects
        ):
            for row_index, obj in enumerate(
                objects_in_column
            ):
                item = QTableWidgetItem(
                    str(obj["number"])
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(
                    row_index,
                    column_index,
                    item,
                )

    def get_selected_columns(self) -> list[str]:
        """Возвращает выбранные пользователем столбцы."""

        selected_columns = []

        for index, checkbox in enumerate(
            self.column_checkboxes,
            start=1,
        ):
            if checkbox.isChecked():
                selected_columns.append(str(index))

        return selected_columns

    def columns_changed(self):
        """Обрабатывает изменение выбранных столбцов."""

        selected_columns = self.get_selected_columns()

        if self.last_selected_columns is None:
            return

        if selected_columns != self.last_selected_columns:
            self.action_button.setText(
                "Показать результат"
            )

    def handle_action(self):
        """Обрабатывает нажатие основной кнопки."""

        if self.action_button.text() == "Сброс":
            self.reset_game()
            return

        self.show_result()

    def show_result(self):
        """Показывает результат по выбранным столбцам."""

        selected_columns = self.get_selected_columns()

        if not selected_columns:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите хотя бы один столбец.",
            )
            return

        try:
            obj = self.game.guess(
                self.current_category,
                selected_columns,
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Ошибка",
                str(error),
            )
            return

        if obj is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось определить объект.",
            )
            return

        self.result_label.setText(
            f"Заданный объект: {obj['name']}"
        )

        self.last_selected_columns = (
            selected_columns.copy()
        )

        self.action_button.setText("Сброс")

    def reset_game(self):
        """Сбрасывает результат и выбранные столбцы."""

        for checkbox in self.column_checkboxes:
            checkbox.setChecked(False)

        self.last_selected_columns = None

        self.result_label.setText(
            "Заданный объект: —"
        )

        self.action_button.setText(
            "Показать результат"
        )
