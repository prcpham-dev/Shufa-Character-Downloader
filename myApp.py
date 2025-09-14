#!/usr/bin/env python3
"""
Launcher for Shufa Downloader
- Double-clickable
- Prefers venv Python
- Runs interface from src/
"""

import os
import sys
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent

def venv_python():
    win = HERE / "venv" / "Scripts" / "python.exe"      # Windows
    nix = HERE / "venv" / "bin" / "python3"             # macOS/Linux
    if win.exists(): return str(win)
    if nix.exists(): return str(nix)
    return None

def open_app():
    py = venv_python() or sys.executable
    env = os.environ.copy()
    # Make everything in src/ importable as top-level modules
    env["PYTHONPATH"] = str(HERE / "src") + os.pathsep + env.get("PYTHONPATH", "")
    # (optional) expose project root to PATH
    env["PATH"] = str(HERE) + os.pathsep + env.get("PATH", "")

    try:
        # Run src/interface.py as module "interface"
        subprocess.call([py, "-m", "interface"], cwd=str(HERE), env=env)
    except Exception as e:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk(); root.withdraw()
            messagebox.showerror("Shufa Downloader – Launch Error", str(e))
        finally:
            raise

if __name__ == "__main__":
    open_app()
