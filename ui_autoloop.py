import os
from PyQt5 import QtWidgets
from autoloop_vbs import AutoLoopVBSManager
from autoloop_bat import AutoLoopBATManager


class AutoLoopManagerGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
        # Инициализация менеджеров
        startup_folder = os.path.expandvars(r"%AppData%\Microsoft\Windows\Start Menu\Programs\Startup")
        self.vbs_manager = AutoLoopVBSManager(startup_folder)
        self.bat_manager = None
    
        print("[DEBUG] Запуск load_data")  # Отладочное сообщение
        self.load_data()  # Загружаем данные

    def init_ui(self):
        """Настройка графического интерфейса."""
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

    def load_data(self):
        """Загрузка данных из файлов AutoLoop.vbs и AutoLoop.bat."""
        try:
            print("[DEBUG] Вызов read_vbs")  # Отладочное сообщение
            bat_path = self.vbs_manager.read_vbs()
            print("[DEBUG] Вызов read_bat")  # Отладочное сообщение
            self.bat_manager = AutoLoopBATManager(bat_path)
            process_list = self.bat_manager.read_bat()
            print("[DEBUG] Обновление таблицы")  # Отладочное сообщение
            self.update_table(process_list)
        except FileNotFoundError as e:
            print(f"[DEBUG] Ошибка загрузки: {e}")
            self.bat_manager = None
            self.update_table([])
    

    def update_table(self, process_list):
        """Обновляет таблицу с процессами."""
        self.table.setRowCount(0)
        for app_name, path, interval in process_list:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(app_name))
            self.table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(path))
            self.table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(interval)))

    def add_process(self):
        """Добавление нового процесса."""
        if not self.bat_manager:
            # Если bat_manager ещё не инициализирован, создаём пустую структуру
            default_bat_path = os.path.join(os.getcwd(), "AutoLoop.bat")
            self.bat_manager = AutoLoopBATManager(default_bat_path)
            self.bat_manager.process_list = []

        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите приложение")
        if path:
            app_name = os.path.basename(path)
            interval, ok = QtWidgets.QInputDialog.getInt(
                self, "Интервал", "Введите интервал (сек):", 10, 1, 3600
            )
            if ok:
                self.bat_manager.process_list.append([app_name, path, interval])
                self.update_table(self.bat_manager.process_list)

    def remove_process(self):
        """Удаление выбранного процесса."""
        selected_row = self.table.currentRow()
        if selected_row >= 0 and self.bat_manager:
            self.bat_manager.process_list.pop(selected_row)
            self.update_table(self.bat_manager.process_list)

    def apply_changes(self):
        """Создаёт/обновляет файлы AutoLoop.vbs и AutoLoop.bat."""
        if not self.bat_manager:
            # Если файлы отсутствуют, создаём их
            default_bat_path = os.path.join(os.getcwd(), "AutoLoop.bat")
            self.bat_manager = AutoLoopBATManager(default_bat_path)

        # Проверяем, есть ли путь к файлу bat
        if not self.bat_manager.bat_path:
            self.bat_manager.bat_path = os.path.join(os.getcwd(), "AutoLoop.bat")

        # Пишем данные в AutoLoop.bat
        self.bat_manager.write_bat(self.bat_manager.process_list)

        # Пишем путь в AutoLoop.vbs
        self.vbs_manager.write_vbs(self.bat_manager.bat_path)

        QtWidgets.QMessageBox.information(self, "Успех", "Файлы успешно обновлены.")
