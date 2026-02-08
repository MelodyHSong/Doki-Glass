# ☆ Doki-Glass ☆

> "Clear windows, clear mind... though I still can't see where I left my keys."

Welcome to **Doki-Glass**! This project is a lightweight, configurable utility designed to enhance the aesthetics of your Windows 11 desktop. By applying a "Layered" window style to specific application classes, it gives your workspace a modern, see-through interface without the performance tax of heavy customization suites.

<img width="1918" height="979" alt="image" src="https://github.com/user-attachments/assets/4609eafd-e05f-4c8d-ab4b-9508b8e47a1d" />


---

## ☆ Release History

| Version | Status | Key Changes |
| :--- | :--- | :--- |
| **v1.2.0a** | **Latest** | Triple-key hotkeys, Auto-Hunter Dialog, and Steam/SDL crash protection. |
| **v1.0.0a** | Stable/Alpha | Initial release with JSON config, Inno Setup installer, and basic hotkeys. |
| **v0.5.0INDEV** | Indev | Migration to native Win32 API and Registry-based startup management. |

## ☆ Installation & Prerequisites

To use the pre-built version, you just need Windows 11. If you are building from source, you will need:
* **Python 3.12+**
* **Administrative Privileges** are required for installation.
* **Hardware Acceleration** should be disabled in Chromium browsers (Opera GX, Chrome) for the best effect.

### Quick Install

1. **Download:** Grab the latest `Doki-Glass-Installer.exe` from the [Releases](https://github.com/MelodyHSong/Doki-Glass/releases) page.
2. **Install:** Run the setup. It will handle the startup registry keys for you.
3. **Configure:** Find your settings at `%APPDATA%\Doki-Glass\config.json`.

---

## ☆ Usage

Doki-Glass runs silently in the background. It monitors your system and applies transparency to supported windows as soon as they appear.

### Features
* **Auto-Glass:** Instantly makes supported windows translucent.
* **Smart Startup:** Toggle launch-at-boot via the `run_at_startup` config setting.
* **Auto-Hunter:** Identify new windows and add them to your targets with a single click.

### Hotkeys
To avoid conflicts with development tools and creative software, we use triple-key combinations:
* `Ctrl + Alt + G`: **Toggle** the transparency logic on or off.
* `Ctrl + Alt + C`: **Class Hunter** — Identifies the focused window, copies the class name, and offers to add it to your config automatically.

### Default Targets
* **File Explorer** (`CabinetWClass`)
* **UWP Apps** (`ApplicationFrameWindow`) — Settings, Calculator, etc.
* **Notepad** (`Notepad`)
* **Chromium Browsers** (`Chrome_WidgetWin_1`) — Opera GX, Chrome, Brave.

---

## ☆ Development & Customization

### Prerequisites
* `pip install pywin32`

### Build from Source
To create your own standalone executable:
```powershell
pyinstaller --noconsole --onefile --icon="assets/icon.ico" --name Doki-Glass src/main.py
```
## ☆ License
This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects—just keep the headers intact!

*I’d tell a joke about glass, but I'm afraid it might be too transparent. — MelodyHSong*


