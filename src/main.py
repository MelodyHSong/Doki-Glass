# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Program: Doki-Glass v1.0.0a (Win32 Stable)
# ☆ Language: Python
# ☆ License: MIT
# ☆ Date 2026-08-02
# ☆ 
# ☆ Description: A lightweight utility to apply a glass-like transparency effect to specified windows on Windows OS.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import win32gui
import win32con
import win32api
import time
import json
import os
import winreg
import sys

# Constants for File Management
APP_NAME = "Doki-Glass"
CONFIG_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

# Unique IDs for Global Hotkeys
HOTKEY_TOGGLE_ID = 1
HOTKEY_HUNTER_ID = 2

def load_config():
    """Loads user settings or generates defaults."""
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
    """Adds or removes the app from Windows Registry Startup."""
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # Ensure path is quoted to handle potential spaces in directories

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
    except Exception:
        pass # Silently fail if registry is locked/restricted

config = load_config()
is_active = True

def apply_glass(hwnd, lparam):
    """Iterates through windows and applies the alpha-blending style."""
    if not is_active:
        return
        
    class_name = win32gui.GetClassName(hwnd)
    if class_name in config["targets"]:
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if not (style & win32con.WS_EX_LAYERED):

            # Apply WS_EX_LAYERED to allow transparency

            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, 0, config["alpha"], win32con.LWA_ALPHA)

if __name__ == "__main__":
    manage_startup(config.get("run_at_startup", True))
    
    # ☆ Register Native Hotkeys using win32gui ☆
    # Alt (0x0001) + G (0x47) / C (0x43)
    try:
        win32gui.RegisterHotKey(None, HOTKEY_TOGGLE_ID, win32con.MOD_ALT, 0x47)
        win32gui.RegisterHotKey(None, HOTKEY_HUNTER_ID, win32con.MOD_ALT, 0x43)
    except Exception as e:
        win32api.MessageBox(0, f"Failed to register hotkeys: {e}", "Doki-Glass Error", win32con.MB_ICONERROR)
    
    try:
        while True:

            # Native Windows Message Loop
            # This is non-blocking to allow the window enumeration to run

            if win32gui.PeekMessage(None, 0, 0, win32con.PM_REMOVE)[0]:
                msg = win32gui.GetMessage(None, 0, 0)
                data = msg[1]
                if data[1] == win32con.WM_HOTKEY:
                    if data[2] == HOTKEY_TOGGLE_ID:
                        is_active = not is_active
                    
                    elif data[2] == HOTKEY_HUNTER_ID:
                        hwnd = win32gui.GetForegroundWindow()
                        c_name = win32gui.GetClassName(hwnd)
                        w_title = win32gui.GetWindowText(hwnd)
                        
                        # Use a path the app is allowed to write to
                        # This saves to Documents/Doki-Glass Output
                        docs_path = os.path.join(os.path.expanduser('~'), 'Documents')
                        output_dir = os.path.join(docs_path, "Doki-Glass Output")
                        
                        if not os.path.exists(output_dir):
                            os.makedirs(output_dir)
                        
                        output_file = os.path.join(output_dir, "identified_class.txt")
                        
                        with open(output_file, "a") as f: # Changed to 'a' to append instead of overwrite
                            f.write(f"[{time.ctime()}] Title: {w_title} | Class: {c_name}\n")
                        
                        win32api.MessageBox(0, f"Saved to Documents/Doki-Glass Output", "Doki-Glass Hunter", win32con.MB_ICONINFORMATION)

                win32gui.TranslateMessage(data)
                win32gui.DispatchMessage(data)

            # Check and apply glass effect to windows

            win32gui.EnumWindows(apply_glass, None)

            time.sleep(0.5) # Balanced for responsiveness vs CPU usage
            
    finally:
        # Clean up hotkeys on exit
        win32gui.UnregisterHotKey(None, HOTKEY_TOGGLE_ID)
        win32gui.UnregisterHotKey(None, HOTKEY_HUNTER_ID)