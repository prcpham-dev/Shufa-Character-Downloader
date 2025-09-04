import tkinter as tk
from tkinter import ttk, messagebox
import sys
import asyncio, threading
import traceback
import run


class TextRedirector:
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, msg):
        if msg:
            self.text_widget.after(0, self._append, msg)

    def flush(self):
        pass

    def _append(self, msg):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", msg, (self.tag,))
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shufa Downloader")
        self.geometry("520x360")
        self.is_running = False

        # ---------- UI ----------
        control_row = ttk.Frame(self)
        control_row.pack(fill="x", padx=10, pady=(10, 0))

        # buttons and status
        self.start_btn = ttk.Button(control_row, text="Start", command=self.start)
        self.start_btn.pack(side="left")

        self.stop_btn = ttk.Button(control_row, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(8, 0))

        self.status_var = tk.StringVar(value="Status: Idle")
        ttk.Label(control_row, textvariable=self.status_var).pack(side="right")

        # log box
        self.text = tk.Text(self, height=14, wrap="word", state="disabled")
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        # redirect stdout and stderr
        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")

        self.protocol("WM_DELETE_WINDOW", self._on_close)


    def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self._set_status("Running...")
        print("▶️ Start downloading...\n")

    def stop(self):
        self._on_done()
        print("Stop Downloading...\n")

    def _on_done(self):
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self._set_status("Idle")

    def _set_status(self, text: str):
        self.status_var.set(f"Status: {text}")

    def _on_close(self):
        if self.is_running:
            self.stop()
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
