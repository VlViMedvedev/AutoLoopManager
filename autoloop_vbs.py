import os

class AutoLoopVBSManager:
    def __init__(self, startup_folder):
        self.startup_folder = startup_folder
        self.vbs_path = os.path.join(startup_folder, "AutoLoop.vbs")
        self.bat_path = None

    def read_vbs(self):
        """Читает файл AutoLoop.vbs и извлекает путь до AutoLoop.bat."""
        if not os.path.exists(self.vbs_path):
            raise FileNotFoundError(f"Файл {self.vbs_path} не найден.")
    
        current_directory = None
        bat_path = None
    
        with open(self.vbs_path, "r") as file:
            for line in file:
                if "WshShell.CurrentDirectory" in line:
                    current_directory = line.split("=")[1].strip().replace('"', "")
                if "WshShell.Run" in line:
                    parts = line.split("cmd.exe /c")
                    if len(parts) > 1:
                        bat_path = parts[1].split(",")[0].strip().replace('"', "")
                    break
    
        if not os.path.isabs(bat_path) and current_directory:
            bat_path = os.path.join(current_directory, bat_path)
    
        if not os.path.exists(bat_path):
            raise FileNotFoundError(f"Файл {bat_path} не найден.")
    
        self.bat_path = bat_path
        return self.bat_path

    def write_vbs(self, bat_path):
        """Генерирует файл AutoLoop.vbs с указанным путем до AutoLoop.bat."""
        self.bat_path = bat_path
        with open(self.vbs_path, "w") as file:
            file.write(
                f'''Set WshShell = CreateObject("WScript.Shell")\n'''
                f'''WshShell.CurrentDirectory = "{os.path.dirname(bat_path)}"\n'''
                f'''WshShell.Run "cmd.exe /c {os.path.basename(bat_path)}", 0, True\n'''
            )
