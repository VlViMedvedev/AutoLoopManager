import os
from PyQt5 import QtWidgets, QtCore

class AutoLoopManager(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.auto_loop_path = None
        self.process_list = []

        # Читаем файлы при запуске
        self.load_autoloop_files()

    def init_ui(self):
        # Настройка интерфейса
        self.setWindowTitle("AutoLoop Manager")
        self.resize(600, 400)

        layout = QtWidgets.QVBoxLayout()

        # Таблица для списка процессов
        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Приложение", "Путь", "Интервал (сек)"])
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Кнопки управления
        button_layout = QtWidgets.QHBoxLayout()

        self.add_button = QtWidgets.QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_process)
        button_layout.addWidget(self.add_button)

        self.remove_button = QtWidgets.QPushButton("Удалить")
        self.remove_button.clicked.connect(self.remove_process)
        button_layout.addWidget(self.remove_button)

        self.apply_button = QtWidgets.QPushButton("Применить")
        self.apply_button.clicked.connect(self.apply_changes)
        button_layout.addWidget(self.apply_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_autoloop_files(self):
        # Проверяем наличие AutoLoop.vbs
        startup_folder = os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup")
        vbs_file = os.path.join(startup_folder, "AutoLoop.vbs")

        if not os.path.exists(vbs_file):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл AutoLoop.vbs не найден.")
            return

        # Читаем путь к AutoLoop.bat
        with open(vbs_file, "r") as file:
            for line in file:
                if "WshShell.Run" in line:
                    self.auto_loop_path = line.split('"')[1]
                    break

        if not self.auto_loop_path or not os.path.exists(self.auto_loop_path):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Файл AutoLoop.bat не найден.")
            return

        # Читаем содержимое AutoLoop.bat
        with open(self.auto_loop_path, "r") as file:
            for line in file:
                if line.startswith("start"):
                    parts = line.split('"')
                    if len(parts) > 1:
                        path = parts[1]
                        app_name = os.path.basename(path)
                        interval = 10  # Интервал по умолчанию
                        self.process_list.append([app_name, path, interval])

        # Заполняем таблицу
        self.update_table()

    def update_table(self):
        self.table.setRowCount(0)
        for app_name, path, interval in self.process_list:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(app_name))
            self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(path))
            self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(interval)))

    def add_process(self):
        # Диалог для добавления приложения
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите приложение")
        if path:
            app_name = os.path.basename(path)
            interval, ok = QtWidgets.QInputDialog.getInt(self, "Интервал", "Введите интервал (сек):", 10, 1, 3600)
            if ok:
                self.process_list.append([app_name, path, interval])
                self.update_table()

    def remove_process(self):
        # Удаление выбранного приложения
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.process_list.pop(selected_row)
            self.update_table()

    def apply_changes(self):
        # Генерация AutoLoop.bat
        if not self.auto_loop_path:
            return

        with open(self.auto_loop_path, "w") as file:
            for app_name, path, interval in self.process_list:
                file.write(f'@echo off\n')
                file.write(f'timeout /T {interval}\n')
                file.write(f'start "" "{path}"\n')

        QtWidgets.QMessageBox.information(self, "Успех", "Изменения применены.")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = AutoLoopManager()
    window.show()
    app.exec_()
