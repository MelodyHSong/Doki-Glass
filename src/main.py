# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Author: ☆ MelodyHSong ☆
# ☆ Language: Python
# ☆ File Name: main.py
# ☆ Date: 2026-02-09
# ☆
# ☆ Description: Doki-Glass v1.3.0a - Now with threaded hotkey handling, 
# ☆ safe registration, and first-run user choice logic.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆

import win32gui, win32con, win32api, win32clipboard
import time, json, os, winreg, sys, threading
import ctypes
import pywintypes

APP_NAME = "Doki-Glass"
VERSION = "1.3.0a"
CONFIG_DIR = os.path.join(os.environ['APPDATA'], APP_NAME)
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

HOTKEY_TOGGLE_ID = 1
HOTKEY_HUNTER_ID = 2
HOTKEY_CONFIG_ID = 3

def is_admin():
    # ☆ Description: Check for administrative privileges.
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def load_config():
    # ☆ Description: Load or create the application configuration.
    if not os.path.exists(CONFIG_DIR): 
        os.makedirs(CONFIG_DIR)
    defaults = {
        "alpha": 215,
        "run_at_startup": True,
        "enable_hotkeys": "FirstRun",
        "targets": ["CabinetWClass", "ApplicationFrameWindow", "Notepad", "Chrome_WidgetWin_1"]
    }
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as f: 
            json.dump(defaults, f, indent=4)
        return defaults
    with open(CONFIG_PATH, 'r') as f: 
        return json.load(f)

def manage_startup(enable):
    # ☆ Description: Manage Windows Registry startup entry.
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

def safe_register(hk_id, vk):
    # ☆ Description: Attempt registration while ignoring Error 1409.
    try:
        win32gui.RegisterHotKey(None, hk_id, win32con.MOD_ALT, vk)
    except pywintypes.error as e:
        if e.winerror == 1409:
            pass 
        else:
            raise e

config = load_config()
is_active = True

def apply_glass(hwnd, lparam):
    # ☆ Description: Apply transparency to windows in the target list.
    if not is_active: return
    try:
        class_name = win32gui.GetClassName(hwnd)
        if class_name in config["targets"]:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if not (style & win32con.WS_EX_LAYERED):
                win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_LAYERED)
                win32gui.SetLayeredWindowAttributes(hwnd, 0, config["alpha"], win32con.LWA_ALPHA)
    except:
        pass 

def hotkey_listener():
    # ☆ Description: Threaded listener to process hotkey messages.
    global is_active, config
    safe_register(HOTKEY_TOGGLE_ID, 0x21) # Alt + PgUp
    safe_register(HOTKEY_HUNTER_ID, 0x22) # Alt + PgDn
    safe_register(HOTKEY_CONFIG_ID, 0x4F) # Alt + O
    
    try:
        while True:
            msg = win32gui.GetMessage(None, 0, 0)
            if msg[0] != 0:
                msg_data = msg[1]
                if msg_data[1] == win32con.WM_HOTKEY:
                    hid = msg_data[2]
                    if hid == HOTKEY_TOGGLE_ID:
                        is_active = not is_active
                    elif hid == HOTKEY_CONFIG_ID:
                        os.startfile(CONFIG_PATH)
                    elif hid == HOTKEY_HUNTER_ID:
                        hwnd = win32gui.GetForegroundWindow()
                        c_name = win32gui.GetClassName(hwnd)
                        prompt = f"Class: {c_name}\n\nAdd to target list?"
                        if win32api.MessageBox(0, prompt, f"{APP_NAME} Hunter", 3 | 64) == 6:
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(c_name)
                            win32clipboard.CloseClipboard()
                            if c_name not in config["targets"]:
                                config["targets"].append(c_name)
                                with open(CONFIG_PATH, 'w') as f:
                                    json.dump(config, f, indent=4)
                win32gui.TranslateMessage(msg_data)
                win32gui.DispatchMessage(msg_data)
    finally:
        for i in [HOTKEY_TOGGLE_ID, HOTKEY_HUNTER_ID, HOTKEY_CONFIG_ID]:
            try: win32gui.UnregisterHotKey(None, i)
            except: pass

if __name__ == "__main__":
    # 1. Elevate First: Prevents prompt from being closed by elevation restart.
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    # 2. Config & Startup Management
    config = load_config()
    manage_startup(config.get("run_at_startup", True))

    # 3. Choice Logic: Only runs once we are in the final Admin process
    current_hk_state = config.get("enable_hotkeys", "FirstRun")
    if current_hk_state == "FirstRun":
        prompt = (
            "Doki-Glass v1.3.0a\n\n"
            "Would you like to enable Global Hotkeys?\n"
            "(Alt + PgUp / Alt + PgDn / Alt + O)\n\n"
            "Select 'No' to disable them and prevent this message from appearing again."
        )
        res = win32api.MessageBox(0, prompt, f"{APP_NAME} Setup", 4 | 32)
        config["enable_hotkeys"] = True if res == 6 else False
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        current_hk_state = config["enable_hotkeys"]

    # 4. Threading: Start listener only if user enabled it
    if current_hk_state is True:
        listener_thread = threading.Thread(target=hotkey_listener, daemon=True)
        listener_thread.start()

    # 5. Core Engine
    try:
        while True:
            win32gui.EnumWindows(apply_glass, None)
            time.sleep(0.5)
    except KeyboardInterrupt:
        sys.exit()

# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆
# ☆ Post-Mortem Note (v1.3.0a): 
# ☆ The "First Run" prompt was failing because the non-admin process was spawning 
# ☆ the admin process and closing before the user could interact. 
# ☆ Fixed by moving the Choice Logic AFTER the successful is_admin() check.
# ☆ Multi-threading added to prevent EnumWindows from starving the message queue.
# ☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆