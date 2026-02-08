# ☆ Doki-Glass ☆

> "Clear windows, clear mind... though I still can't see where I left my keys."

Welcome to **Doki-Glass**! This project is a lightweight, configurable utility designed to enhance the aesthetics of your Windows 11 desktop. By applying a "Layered" window style to specific application classes, it gives your workspace a modern, see-through interface without the performance tax of heavy customization suites.

---

## ☆ Installation & Prerequisites

To use the pre-built version, you just need Windows 11. If you are building from source, you will need:
* **Python 3.12+**
* **Administrative Privileges** (for certain system windows)
* **Hardware Acceleration Off** (specifically for Chromium-based browsers like Opera GX)

### Quick Install

If you just want the app running:
1. **Download:** Grab the latest `Doki-Glass-Setup.exe` from the [Releases](https://github.com/MelodyHSong/Doki-Glass/releases) page.
2. **Install:** Run the setup.
3. **Configure:** Find your settings at `%APPDATA%\Doki-Glass\config.json`.

---

## ☆ Usage

Doki-Glass runs silently in the background. It monitors your system and applies transparency to supported windows as soon as they appear.

### Features
* **Auto-Glass:** Seamlessly makes new windows translucent.
* **Smart Startup:** Control whether the app launches at boot directly via the config file.
* **JSON Config:** Change opacity (0-255) or target new apps without touching code.

### Hotkeys
* `Alt + G`: **Toggle** the transparency logic on or off.
* `Alt + C`: **Class Hunter** — Instantly identifies the internal name of the active window so you can add it to your config.

### Config Options (`config.json`)
* `alpha`: Set transparency (0 is invisible, 255 is solid).
* `run_at_startup`: Set to `true` or `false` to toggle launch on Windows boot.
* `targets`: A list of Window Class names to affect.

---

## ☆ Development & Customization

### Example Usage

To set up your development environment:
```powershell
pip install pywin32 keyboard
```

To build your own standalone executable:

```powershell
pyinstaller --noconsole --onefile --name Doki-Glass src/main.py
```
## ☆ License
This project is licensed under the MIT License. You are free to use, modify, and distribute this code in your own projects—just keep the headers intact!

*I’d tell a joke about glass, but I'm afraid it might be too transparent. — MelodyHSong*

