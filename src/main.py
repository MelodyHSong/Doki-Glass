# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Program: Doki-Glass v1.2.0a 
# ☆ Language: Python
# ☆ License: MIT
# ☆ Date: 2026-02-08
# ☆ 
# ☆ Description: A lightweight utility to apply a glass-like transparency effect.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import win32gui, win32con, win32api, win32clipboard
import time, json, os, winreg, sys
import ctypes

APP_NAME = "Doki-Glass"
VERSION = "1.2.0a"
CONFIG_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

HOTKEY_TOGGLE_ID = 1
HOTKEY_HUNTER_ID = 2

def is_admin():
    """Check for administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def load_config():
    """Load or create the application configuration."""
    if not os.path.exists(CONFIG_DIR): 
        os.makedirs(CONFIG_DIR)
    defaults = {
        "alpha": 215,
        "run_at_startup": True,
        "targets": ["CabinetWClass", "ApplicationFrameWindow", "Notepad", "Chrome_WidgetWin_1"]
    }
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f: 
            json.dump(defaults, f, indent=4)
        return defaults
    with open(CONFIG_PATH, 'r') as f: 
        return json.load(f)

def manage_startup(enable):
    """Manage Windows Registry startup entry."""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    if getattr(sys, "frozen", False):
        exe_path = f'"{os.path.realpath(sys.executable)}"'
    else:
        script_path = os.path.realpath(os.path.abspath(sys.argv[0]))
        exe_path = f'"{os.path.realpath(sys.executable)}" "{script_path}"'
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
        if enable: 
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        else:
            try: winreg.DeleteValue(key, APP_NAME)
            except: pass
        winreg.CloseKey(key)
    except: pass

config = load_config()
is_active = True

def apply_glass(hwnd, lparam):
    """Apply transparency to windows in the target list."""
    if not is_active: return
    try:
        class_name = win32gui.GetClassName(hwnd)
        if class_name in config["targets"]:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if not (style & win32con.WS_EX_LAYERED):
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(hwnd, 0, config["alpha"], win32con.LWA_ALPHA)
    except:
        pass # Handle invalid handles from dynamic apps

if __name__ == "__main__":
    # Ensure Admin rights (Mandatory for system window modification)
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # Update startup preferences
    manage_startup(config.get("run_at_startup", True))
    
    # Silent Hotkey Registration (Alt + PgUp / Alt + PgDn)
    # We use silent registration to avoid false-positive error 1409 popups.
    win32gui.RegisterHotKey(None, HOTKEY_TOGGLE_ID, win32con.MOD_ALT, 0x21) 
    win32gui.RegisterHotKey(None, HOTKEY_HUNTER_ID, win32con.MOD_ALT, 0x22)

    try:
        while True:
            # Process Windows Messages for Hotkeys
            if win32gui.PeekMessage(None, 0, 0, win32con.PM_REMOVE)[0]:
                msg = win32gui.GetMessage(None, 0, 0)
                if msg[1][1] == win32con.WM_HOTKEY:
                    hid = msg[1][2]
                    
                    if hid == HOTKEY_TOGGLE_ID:
                        is_active = not is_active
                    
                    elif hid == HOTKEY_HUNTER_ID:
                        hwnd = win32gui.GetForegroundWindow()
                        c_name = win32gui.GetClassName(hwnd)
                        prompt = f"Class: {c_name}\n\nAdd to target list?"
                        if win32api.MessageBox(0, prompt, f"{APP_NAME} Hunter", 3 | 64) == 6: # IDYES
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(c_name)
                            win32clipboard.CloseClipboard()
                            
                            if c_name not in config["targets"]:
                                config["targets"].append(c_name)
                                with open(CONFIG_PATH, 'w') as f:
                                    json.dump(config, f, indent=4)
                
                win32gui.TranslateMessage(msg[1])
                win32gui.DispatchMessage(msg[1])

            # Core Transparency Engine
            win32gui.EnumWindows(apply_glass, None)
            time.sleep(0.5)
            
    finally:
        # Cleanup
        win32gui.UnregisterHotKey(None, HOTKEY_TOGGLE_ID)
        win32gui.UnregisterHotKey(None, HOTKEY_HUNTER_ID)