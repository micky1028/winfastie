import json
import ctypes
import sys
import os
import tkinter as tk
from modules.gui import SetupApp

def load_config():
    # Gestisce il percorso sia per lo script normale che per l'eseguibile PyInstaller
    if getattr(sys, 'frozen', False):
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    config_path = os.path.join(base_dir, "config", "settings.json")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    # Controllo privilegi di amministrazione (necessari per winget)
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    config = load_config()
    
    root = tk.Tk()
    app = SetupApp(root, config)
    root.mainloop()

if __name__ == "__main__":
    main()