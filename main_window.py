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
    """Кастомный переключатель светлой и тёмной темы."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFixedSize(54, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Переключить тему")

    def paintEvent(self, event):
        """Отрисовывает переключатель."""

        from PySide6.QtGui import QPainter, QBrush, QColor

        painter = QPainter(self)
        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        # Фон переключателя
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

        # Положение круглого переключателя
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

        # Символ темы
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

        self.create_interface()
        self.apply_styles()

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
        self.theme_toggle.toggled.connect(
            self.toggle_theme
        )

        self.numbers_button.setObjectName("activeCategory")

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

        category_layout.addSpacing(15)

        self.help_button.setMinimumWidth(85)
        self.help_button.setMinimumHeight(34)

        category_layout.addWidget(self.help_button)

        category_layout.addWidget(
            self.theme_toggle
        )

        main_layout.addLayout(category_layout)

        # =================================================
        # Таблица
        # =================================================

        table_frame = QFrame()
        table_frame.setObjectName("tableFrame")

        table_layout = QVBoxLayout(table_frame)
        table_layout.setContentsMargins(8, 8, 8, 8)
        table_layout.setSpacing(0)

        # -------------------------------------------------
        # Чекбоксы
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Таблица чисел
        # -------------------------------------------------

        self.table = QTableWidget()

        self.table.setObjectName("numberTable")

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

        # Равномерное распределение ширины
        self.table.horizontalHeader().setSectionResizeMode(
            0,
            self.table.horizontalHeader().ResizeMode.Stretch,
        )

        self.table.horizontalHeader().setSectionResizeMode(
            1,
            self.table.horizontalHeader().ResizeMode.Stretch,
        )

        self.table.horizontalHeader().setSectionResizeMode(
            2,
            self.table.horizontalHeader().ResizeMode.Stretch,
        )

        self.table.horizontalHeader().setSectionResizeMode(
            3,
            self.table.horizontalHeader().ResizeMode.Stretch,
        )

        self.table.horizontalHeader().setSectionResizeMode(
            4,
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

        # -------------------------------------------------
        # Поле результата
        # -------------------------------------------------

        result_frame = QFrame()
        result_frame.setObjectName("resultFrame")

        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(10, 4, 10, 4)

        self.result_label = QLabel(
            "Заданное число: —"
        )

        self.result_label.setObjectName(
            "resultLabel"
        )

        self.result_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        result_layout.addWidget(
            self.result_label
        )

        bottom_layout.addWidget(
            result_frame,
            stretch=1,
        )

        # -------------------------------------------------
        # Кнопка действия
        # -------------------------------------------------

        self.action_button = QPushButton(
            "Показать результат"
        )

        self.action_button.setObjectName(
            "actionButton"
        )

        self.action_button.setMinimumWidth(150)
        self.action_button.setMinimumHeight(42)

        self.action_button.clicked.connect(
            self.handle_action
        )

        bottom_layout.addWidget(
            self.action_button
        )

        main_layout.addLayout(
            bottom_layout
        )

    def apply_styles(self):
        """Настраивает внешний вид приложения."""

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #f7f8fa;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 13px;
                color: #263238;
            }

            /* -------------------------------
               Кнопки категорий
               ------------------------------- */

            QPushButton {
                background-color: #ffffff;
                border: 1px solid #d9dde3;
                border-radius: 6px;
                padding: 5px 12px;
                color: #374151;
            }

            QPushButton:hover {
                background-color: #f0f3f6;
            }

            QPushButton:pressed {
                background-color: #e7ebef;
            }

            QPushButton#activeCategory {
                background-color: #e2e5e9;
                border: 1px solid #d0d5db;
                color: #1f2933;
                font-weight: 600;
            }

            /* -------------------------------
               Основная область таблицы
               ------------------------------- */

            QFrame#tableFrame {
                background-color: #ffffff;
                border: 1px solid #e1e5e9;
                border-radius: 7px;
            }

            /* -------------------------------
               Чекбоксы
               ------------------------------- */

            QCheckBox#columnCheckBox {
                spacing: 7px;
                padding: 4px;
                color: #4b5563;
            }

            QCheckBox#columnCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #bfc5cc;
                border-radius: 3px;
                background-color: #ffffff;
            }

            QCheckBox#columnCheckBox::indicator:hover {
                border: 1px solid #9aa3ad;
            }

            QCheckBox#columnCheckBox::indicator:checked {
                background-color: #e0e4e8;
                border: 1px solid #8e98a3;
            }

            /* -------------------------------
               Таблица
               ------------------------------- */

            QTableWidget#numberTable {
                background-color: #ffffff;
                border: none;
                gridline-color: #e3e6e9;
                color: #343a40;
                font-size: 13px;
            }

            QTableWidget#numberTable::item {
                padding: 3px;
                border: none;
            }

            QTableWidget#numberTable::item:selected {
                background-color: #ffffff;
                color: #343a40;
            }

            /* -------------------------------
               Результат
               ------------------------------- */

            QFrame#resultFrame {
                background-color: #ffffff;
                border: 1px solid #e0e4e8;
                border-radius: 7px;
            }

            QLabel#resultLabel {
                color: #183b56;
                font-size: 17px;
                font-weight: 600;
            }

            /* -------------------------------
               Основная кнопка
               ------------------------------- */

            QPushButton#actionButton {
                background-color: #d7dadd;
                border: 1px solid #c8ccd0;
                border-radius: 6px;
                color: #263238;
                font-weight: 600;
                padding: 7px 15px;
            }

            QPushButton#actionButton:hover {
                background-color: #cdd1d5;
            }

            QPushButton#actionButton:pressed {
                background-color: #c1c5c9;
            }
            """
        )

    def toggle_theme(self, dark: bool):
        """Переключает светлую и тёмную тему."""

        if dark:
            self.apply_dark_styles()
        else:
            self.apply_styles()

    def apply_dark_styles(self):
        """Применяет тёмную тему."""

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #20252b;
            }

            QWidget {
                font-family: "Segoe UI";
                font-size: 13px;
                color: #e6e9ed;
            }

            QPushButton {
                background-color: #2b3138;
                border: 1px solid #3b434d;
                border-radius: 6px;
                padding: 5px 12px;
                color: #e6e9ed;
            }

            QPushButton:hover {
                background-color: #343b44;
            }

            QPushButton:pressed {
                background-color: #252a30;
            }

            QPushButton#activeCategory {
                background-color: #3a424c;
                border: 1px solid #4a5562;
                color: #ffffff;
                font-weight: 600;
            }

            QFrame#tableFrame {
                background-color: #272d33;
                border: 1px solid #3b434d;
                border-radius: 7px;
            }

            QCheckBox#columnCheckBox {
                spacing: 7px;
                padding: 4px;
                color: #dce1e6;
            }

            QCheckBox#columnCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #59636e;
                border-radius: 3px;
                background-color: #2b3138;
            }

            QCheckBox#columnCheckBox::indicator:hover {
                border: 1px solid #778391;
            }

            QCheckBox#columnCheckBox::indicator:checked {
                background-color: #59636e;
                border: 1px solid #8995a2;
            }

            QTableWidget#numberTable {
                background-color: #272d33;
                border: none;
                gridline-color: #3b424a;
                color: #e4e7eb;
                font-size: 13px;
            }

            QTableWidget#numberTable::item {
                padding: 3px;
                border: none;
            }

            QTableWidget#numberTable::item:selected {
                background-color: #272d33;
                color: #e4e7eb;
            }

            QFrame#resultFrame {
                background-color: #272d33;
                border: 1px solid #3b434d;
                border-radius: 7px;
            }

            QLabel#resultLabel {
                color: #dce8f2;
                font-size: 17px;
                font-weight: 600;
            }

            QPushButton#actionButton {
                background-color: #3a424b;
                border: 1px solid #4a535e;
                border-radius: 6px;
                color: #f0f2f4;
                font-weight: 600;
                padding: 7px 15px;
            }

            QPushButton#actionButton:hover {
                background-color: #46505b;
            }

            QPushButton#actionButton:pressed {
                background-color: #323941;
            }
            """
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

        self.last_selected_columns = (
            selected_columns.copy()
        )

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