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


class MainWindow(QMainWindow):
    """Главное окно игры «Угадай число»."""

    def __init__(self):
        super().__init__()

        self.game = Game()

        self.setWindowTitle("Угадай число")
        self.resize(530, 390)

        self.column_checkboxes = []
        self.last_selected_columns = None

        self.create_interface()

    def create_interface(self):
        """Создаёт интерфейс главного окна."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(8)

        # Верхнее меню категорий
        category_layout = QHBoxLayout()
        category_layout.setSpacing(5)

        self.numbers_button = QPushButton("Числа")
        self.cities_button = QPushButton("Города")
        self.names_button = QPushButton("Имена")
        self.plants_button = QPushButton("Растения")
        self.animals_button = QPushButton("Животные")
        self.help_button = QPushButton("Справка")

        category_buttons = [
            self.numbers_button,
            self.cities_button,
            self.names_button,
            self.plants_button,
            self.animals_button,
        ]

        for button in category_buttons:
            button.setMinimumHeight(25)
            category_layout.addWidget(button)

        category_layout.addStretch()

        self.help_button.setMinimumHeight(25)
        self.help_button.setMinimumWidth(65)

        category_layout.addWidget(self.help_button)

        main_layout.addLayout(category_layout)

        # Область таблицы
        table_frame = QFrame()
        table_frame.setFrameShape(QFrame.Shape.Box)
        table_frame.setFrameShadow(QFrame.Shadow.Plain)

        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(5, 5, 5, 5)
        table_layout.setSpacing(0)

        # Чекбоксы над столбцами
        checkbox_layout = QGridLayout()
        checkbox_layout.setContentsMargins(0, 0, 0, 0)
        checkbox_layout.setHorizontalSpacing(0)

        for column_number in range(5):
            checkbox = QCheckBox(
                f"Столбец {column_number + 1}"
            )

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

        # Таблица чисел
        self.table = QTableWidget()

        self.table.setRowCount(17)
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

        columns = [
            [
                16, 17, 18, 19, 20, 20, 22, 23, 24,
                25, 26, 27, 28, 29, 30, 31, 16
            ],
            [
                8, 9, 10, 11, 12, 13, 14, 15, 24,
                25, 26, 27, 28, 29, 30, 31, 8
            ],
            [
                4, 5, 6, 7, 12, 13, 14, 15, 20,
                21, 22, 23, 28, 29, 30, 31, 4
            ],
            [
                2, 3, 6, 7, 10, 11, 14, 15, 18,
                19, 22, 23, 26, 27, 30, 31, 2
            ],
            [
                1, 3, 5, 7, 9, 11, 13, 15, 17,
                19, 21, 23, 25, 27, 29, 31, 1
            ],
        ]

        for column in range(5):
            for row in range(17):
                item = QTableWidgetItem(
                    str(columns[column][row])
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    item,
                )

        self.table.horizontalHeader().setStretchLastSection(
            True
        )

        for column in range(5):
            self.table.setColumnWidth(
                column,
                95,
            )

        for row in range(17):
            self.table.setRowHeight(
                row,
                24,
            )

        table_layout.addWidget(self.table)

        main_layout.addWidget(table_frame)

        # Нижняя часть
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(15)

        self.result_label = QLabel(
            "Заданное число: —"
        )

        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.result_label.setMinimumHeight(35)

        result_frame = QFrame()
        result_frame.setFrameShape(
            QFrame.Shape.Box
        )
        result_frame.setFrameShadow(
            QFrame.Shadow.Plain
        )

        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(
            5, 5, 5, 5
        )

        result_layout.addWidget(
            self.result_label
        )

        bottom_layout.addWidget(
            result_frame
        )

        # Кнопка результата / сброса
        self.action_button = QPushButton(
            "Показать результат"
        )

        self.action_button.setMinimumWidth(120)
        self.action_button.setMinimumHeight(35)

        self.action_button.clicked.connect(
            self.handle_action
        )

        bottom_layout.addWidget(
            self.action_button
        )

        main_layout.addLayout(
            bottom_layout
        )

    def get_selected_columns(self) -> list[str]:
        """Возвращает выбранные пользователем столбцы."""

        selected_columns = []

        for index, checkbox in enumerate(
            self.column_checkboxes,
            start=1,
        ):
            if checkbox.isChecked():
                selected_columns.append(
                    str(index)
                )

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
            number = self.game.calculate_number(
                selected_columns
            )
        except ValueError as error:
            QMessageBox.warning(
                self,
                "Ошибка",
                str(error),
            )
            return

        self.result_label.setText(
            f"Заданное число: {number}"
        )

        self.last_selected_columns = selected_columns.copy()

        self.action_button.setText(
            "Сброс"
        )

    def reset_game(self):
        """Сбрасывает результат и выбранные столбцы."""

        for checkbox in self.column_checkboxes:
            checkbox.setChecked(False)

        self.last_selected_columns = None

        self.result_label.setText(
            "Заданное число: —"
        )

        self.action_button.setText(
            "Показать результат"
        )