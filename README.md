# ⚡ windows_but_fast

<p align="center">
  <b>A high-performance, minimalist Windows deployment tool powered by winget.</b>
</p>

---

## 🖤 Overview

`windows_but_fast` is a lightweight, custom-rendered Windows utility designed to streamline the installation and setup of essential software. Built with a sleek **Noir aesthetic** and a custom Python/Tkinter engine, it provides a fast, distraction-free interface for batch-deploying your favorite developer tools, browsers, and utilities.

## ✨ Features

* **Custom Noir Interface:** Minimalist dark-mode design built from scratch using `tkinter.Canvas` with custom smooth scrolling and components.
* **Winget Integration:** Direct, asynchronous background execution of Windows Package Manager commands with real-time progress and live stream output.
* **Modular Configuration:** Easily customizable app lists, categories, and packages via an external `config/settings.json` file.
* **Single-Executable Ready:** Easily packable into a standalone `.exe` via PyInstaller.

## 🚀 Installation & Usage

### Option A: Run from Source (Recommended for Developers)
1. Clone the repository:
   ```bash
   git clone [https://github.com/tuo-username/windows_but_fast.git](https://github.com/tuo-username/windows_but_fast.git)
   cd windows_but_fast
