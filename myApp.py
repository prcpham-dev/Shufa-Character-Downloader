#!/usr/bin/env python3
"""
Launcher for Shufa Downloader
- Double-clickable
- Uses venv if it exists, else falls back to system Python
- Forces working directory to project root (fixes 'Start does nothing')
- Works on Windows, macOS, Linux
"""

import os
import sys
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
APP = str(HERE / "app.py")

def venv_python():
    """Return path to venv python if it exists, else None."""
    win = HERE / "venv" / "Scripts" / "python.exe"    # Windows
    nix = HERE / "venv" / "bin" / "python3"           # macOS/Linux
    if win.exists():
        return str(win)
    if nix.exists():
        return str(nix)
    return None

def open_myApp():
    py = venv_python() or sys.executable

    # Ensure we run in the project folder so relative paths work
    env = os.environ.copy()
    # (optional) add project root to PATH so chromedriver in project root can be found
    env["PATH"] = str(HERE) + os.pathsep + env.get("PATH", "")

    try:
        # Use cwd=HERE so app.py sees the project as the current folder
        subprocess.call([py, APP], cwd=str(HERE), env=env)
    except Exception as e:
        # Show a GUI error dialog so double-click users see the issue
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk(); root.withdraw()
            messagebox.showerror("Shufa Downloader – Launch Error", str(e))
        finally:
            raise

if __name__ == "__main__":
    open_myApp()
