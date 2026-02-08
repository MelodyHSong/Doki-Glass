---
layout: default
title: 🎯 Target Gallery
description: A collection of verified window classes for Doki-Glass.
---

# 🎯 Known Targets Gallery

This gallery contains application class names verified to work with **Doki-Glass v1.2.0a**. Use the **Class Hunter** (`Ctrl + Alt + C`) to discover more and help us grow the collection!

---

## ☆ Verified Applications

| Application | Class Name | Optimal Settings |
| :--- | :--- | :--- |
| **Visual Studio Code** | `Chrome_WidgetWin_1` | Hardware Acceleration: **OFF** |
| **Discord** | `Chrome_WidgetWin_1` | Hardware Acceleration: **OFF** |
| **Steam** | `SDL_app` | Works best in Library/Store views |
| **File Explorer** | `CabinetWClass` | Native support, looks perfect! |
| **Notepad** | `Notepad` | Simple and clean. |
| **Windows Terminal** | `CASCADIA_HOSTING_WINDOW_CLASS` | Enable "Acrylic" in Terminal settings |
| **Spotify** | `Chrome_WidgetWin_1` | Hardware Acceleration: **OFF** |
| **Obsidian** | `Chrome_WidgetWin_1` | Hardware Acceleration: **OFF** |

---

## ☆ The "Chromium" Rule

Most modern desktop apps (Discord, VS Code, Slack, Spotify) are built using Electron. By default, these apps render their own frames which can block the transparency effect.

**To fix "Solid Black" or "Opaque" windows:**
1. Open the app's **Settings**.
2. Search for **"Hardware Acceleration"** or **"GPU Acceleration"**.
3. Toggle it to **OFF** and restart the app.
4. Doki-Glass should now be able to "see through" the window!

---

## ☆ Troubleshooting Gallery Quirk

### 👻 Ghost Windows
Some apps (like Steam or Telegram) create temporary invisible windows. If Doki-Glass feels like it’s lagging when these apps open, don't worry! Version **1.2.0a** includes "Ghost Handle Protection" to ignore these invalid windows automatically.

### 🖼️ UWP / System Apps
Apps like **Settings** or **Calculator** use the `ApplicationFrameWindow` class. These are handled natively, but because Windows manages their lifecycle strictly, you may occasionally need to refresh the effect by toggling `Ctrl + Alt + G`.

---

## ☆ How to Contribute
Found a class that isn't listed here?
1. Focus the window and press `Ctrl + Alt + C`.
2. Click **Yes** to verify it works.
3. [Open an Issue](https://github.com/MelodyHSong/Doki-Glass/issues) with the App Name and Class Name so we can add it to the gallery!

---

<p align="center">
  <i>Stay clear, stay Doki~ ☆</i>
</p>