import os

class AutoLoopBATManager:
    def __init__(self, bat_path):
        self.bat_path = bat_path
        self.process_list = []

    def read_bat(self):
        """Читает AutoLoop.bat и извлекает список процессов."""
        if not self.bat_path or not os.path.exists(self.bat_path):
            raise FileNotFoundError(f"Файл {self.bat_path} не найден.")
        
        self.process_list = []
        with open(self.bat_path, "r", encoding="windows-1251") as file:  # Явно указываем кодировку
            current_process = {}
            for line in file:
                # Извлекаем переменные Process<i>Name и Process<i>Path
                if line.startswith('Set "Process') and "Name=" in line:
                    parts = line.split("=")
                    current_process["name"] = parts[1].strip().replace('"', "")
                elif line.startswith('Set "Process') and "Path=" in line:
                    parts = line.split("=")
                    current_process["path"] = parts[1].strip().replace('"', "")
                
                # Если оба значения получены, добавляем их в список процессов
                if "name" in current_process and "path" in current_process:
                    full_path = os.path.join(current_process["path"], current_process["name"])
                    self.process_list.append([
                        current_process["name"],  # Имя процесса
                        full_path,                # Полный путь
                        10                        # Интервал (по умолчанию)
                    ])
                    current_process = {}  # Сбрасываем текущий процесс
        return self.process_list
    
    
    
            
    def write_bat(self, process_list):
        """Генерирует AutoLoop.bat в формате ANSI с корректным синтаксисом."""
        if not self.bat_path:
            raise FileNotFoundError("Путь к AutoLoop.bat не задан.")
        
        self.process_list = process_list
        with open(self.bat_path, "w", encoding="ansi") as file:  # Используем ANSI
            # Начало файла
            file.write(
                "@Echo Off\n"
                "chcp 1251\n"
                'Echo Текущая кодовая страница: 1251\n\n'
                "SetLocal EnableDelayedExpansion\n\n"
            )
        
            # Генерация переменных для процессов
            for i, process in enumerate(self.process_list, start=1):
                directory = os.path.normpath(os.path.dirname(process[1]))
                filename = os.path.basename(process[1])
                
                # Путь без кавычек
                file.write(
                    f'Set "Process{i}Name={filename}"\n'
                    f'Set "Process{i}Path={directory}"\n'
                )
        
            # Генерация цикла
            file.write("\n:loop\n")
            for i in range(1, len(self.process_list) + 1):
                file.write(
                    f'TaskList /FI "ImageName EQ %Process{i}Name%" | Find /I "%Process{i}Name%" > Nul\n'
                    f"If !ErrorLevel! NEQ 0 (\n"
                    f'    If Exist "%Process{i}Path%\\%Process{i}Name%" (\n'
                    f'        Pushd "%Process{i}Path%"\n'
                    f'        Start "" "%Process{i}Name%"\n'
                    f'        Popd\n'
                    f'    ) Else (\n'
                    f'        Echo Файл %Process{i}Name% не найден в "%Process{i}Path%".\n'
                    f'    )\n'
                    f')\n\n'
                )
        
            # Завершение
            file.write(
                "timeout /T 10\n"
                "goto loop\n"
            )
    