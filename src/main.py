# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Program: Doki-Glass v1.2.0a 
# ☆ Language: Python
# ☆ License: MIT
# ☆ Date 2026-02-08
# ☆ 
# ☆ Description: A lightweight utility to apply a glass-like transparency effect.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import win32gui, win32con, win32api, win32clipboard
import time, json, os, winreg, sys

APP_NAME = "Doki-Glass"
VERSION = "1.2.0a"
CONFIG_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

HOTKEY_TOGGLE_ID = 1
HOTKEY_HUNTER_ID = 2

def load_config():
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
    if not is_active: return
    try:
        class_name = win32gui.GetClassName(hwnd)
        if class_name in config["targets"]:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if not (style & win32con.WS_EX_LAYERED):
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(hwnd, 0, config["alpha"], win32con.LWA_ALPHA)
    except Exception:
        pass 

if __name__ == "__main__":
    manage_startup(config.get("run_at_startup", True))
    
    # NEW MODIFIERS: Windows Key + Shift
    MODIFIERS = win32con.MOD_WIN | win32con.MOD_SHIFT
    
    # Force clear any previous registrations
    win32gui.UnregisterHotKey(None, HOTKEY_TOGGLE_ID)
    win32gui.UnregisterHotKey(None, HOTKEY_HUNTER_ID)
    
    try:
        # Registering Win + Shift + G (0x47) and Win + Shift + C (0x43)
        h1 = win32gui.RegisterHotKey(None, HOTKEY_TOGGLE_ID, MODIFIERS, 0x47) 
        h2 = win32gui.RegisterHotKey(None, HOTKEY_HUNTER_ID, MODIFIERS, 0x43)
        
        if not h1 or not h2:
            raise RuntimeError("Windows blocked the Win+Shift+G/C combination.")
    except Exception as e:
        win32api.MessageBox(0, f"Hotkey Registration Failed:\n{e}\n\nTry running as Admin or checking PowerToys settings.", APP_NAME, win32con.MB_ICONERROR)
        sys.exit(1)

    try:
        while True:
            # Check for Windows Messages
            if win32gui.PeekMessage(None, 0, 0, win32con.PM_REMOVE)[0]:
                msg = win32gui.GetMessage(None, 0, 0)
                msg_data = msg[1]
                
                if msg_data[1] == win32con.WM_HOTKEY:
                    if msg_data[2] == HOTKEY_TOGGLE_ID:
                        is_active = not is_active
                    
                    elif msg_data[2] == HOTKEY_HUNTER_ID:
                        hwnd = win32gui.GetForegroundWindow()
                        c_name = win32gui.GetClassName(hwnd)
                        prompt = f"Class: {c_name}\n\nAdd to config and copy to clipboard?"
                        
                        # Custom Logic for User Choice
                        res = win32api.MessageBox(0, prompt, f"{APP_NAME} Hunter {VERSION}", win32con.MB_YESNOCANCEL | win32con.MB_ICONINFORMATION)

                        if res in [win32con.IDYES, win32con.IDNO]:
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(c_name)
                            win32clipboard.CloseClipboard()
                            
                            if res == win32con.IDYES:
                                if c_name not in config["targets"]:
                                    config["targets"].append(c_name)
                                    with open(CONFIG_PATH, 'w') as f:
                                        json.dump(config, f, indent=4)
                
                win32gui.TranslateMessage(msg_data)
                win32gui.DispatchMessage(msg_data)

            # Apply the effect
            win32gui.EnumWindows(apply_glass, None)
            time.sleep(0.5)
    finally:
        win32gui.UnregisterHotKey(None, HOTKEY_TOGGLE_ID)
        win32gui.UnregisterHotKey(None, HOTKEY_HUNTER_ID)