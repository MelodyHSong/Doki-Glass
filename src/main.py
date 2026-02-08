import win32gui, win32con, win32api
import time, keyboard, json, os, winreg, sys

APP_NAME = "Doki-Glass"
CONFIG_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def load_config():
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    
    defaults = {
        "alpha": 215,
        "run_at_startup": True,
        "targets": ["CabinetWClass", "ApplicationFrameWindow", "Notepad", "Chrome_WidgetWin_1"],
        "hotkeys": {
            "toggle": "alt+g",
            "hunter": "alt+c"
        }
    }
    
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(defaults, f, indent=4)
        return defaults
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def manage_startup(enable):
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    # Ensure the path is quoted to handle spaces in file paths
    exe_path = f'"{os.path.realpath(sys.executable)}"'
    
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if enable:
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass 
        winreg.CloseKey(key)
    except Exception as e:
        pass # Silently fail if registry access is denied

config = load_config()
is_active = True

def apply_glass(hwnd, lparam):
    if not is_active: return
    class_name = win32gui.GetClassName(hwnd)
    if class_name in config["targets"]:
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if not (style & win32con.WS_EX_LAYERED):
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, config["alpha"], win32con.LWA_ALPHA)

def toggle():
    global is_active
    is_active = not is_active

def identify_window():
    hwnd = win32gui.GetForegroundWindow()
    print(f"Class: {win32gui.GetClassName(hwnd)}")

if __name__ == "__main__":
    # Apply startup preference
    manage_startup(config.get("run_at_startup", True))
    
    keyboard.add_hotkey(config["hotkeys"]["toggle"], toggle)
    keyboard.add_hotkey(config["hotkeys"]["hunter"], identify_window)
    
    while True:
        win32gui.EnumWindows(apply_glass, None)
        time.sleep(1)