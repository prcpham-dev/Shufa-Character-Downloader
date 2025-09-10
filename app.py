import os, sys, threading
import tkinter as tk
from tkinter import ttk
from src.preprocess import load_settings, save_settings, prepare_data
from run import run_main
from src.textRedirector import TextRedirector

CHAR_TYPE_VALUE = {
    "行书": "8", "楷书": "9", 
    "草书": "7", "章草": "1", 
    "隶书": "6", "魏碑": "5", 
    "简牍": "4", "篆书": "3", 
    "png大图": "shiliang", 
    "钢笔": "gangbi",
}

CHARACTER_TYPES = list(CHAR_TYPE_VALUE.keys())

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.title("Shufa Downloader")
        self.geometry("860x600")

        self.is_running = False
        self.settings = load_settings()

        # ---------- Top controls ----------
        control_row = ttk.Frame(self)
        control_row.pack(fill="x", padx=10, pady=(10, 0))

        self.start_btn = ttk.Button(control_row, text="Start", command=self.start)
        self.start_btn.pack(side="left")

        self.stop_btn = ttk.Button(control_row, text="Stop", command=self.stop, state="disabled")
        self.stop_btn.pack(side="left", padx=(8, 0))

        self.save_btn = ttk.Button(control_row, text="Save Settings", command=self.save_settings)
        self.save_btn.pack(side="left", padx=(8, 0))

        self.delete_btn = ttk.Button(control_row, text="Delete Images", command=self.delete_images)
        self.delete_btn.pack(side="left", padx=(8, 0))

        self.status_var = tk.StringVar(value="Status: Idle")
        ttk.Label(control_row, textvariable=self.status_var).pack(side="right")

        # ---------- Settings ----------
        settings_frame = ttk.LabelFrame(self, text="Settings")
        settings_frame.pack(fill="x", padx=10, pady=(10, 0))

        for i in range(6):
            settings_frame.columnconfigure(i, weight=1, uniform="c")

        # Row 0: Wait Time + Batch Size
        ttk.Label(settings_frame, text="Wait Time:").grid(row=0, column=0, sticky="w", padx=(6, 4), pady=(8, 4))
        self.wait_time_var = tk.IntVar(value=self.settings.get("wait_time", 15))
        ttk.Scale(
            settings_frame, from_=15, to=60, variable=self.wait_time_var,
            orient="horizontal", length=160,
            command=lambda v: self.force_int(self.wait_time_var, v)
        ).grid(row=0, column=1, sticky="ew", padx=(0, 6), pady=(8, 4))
        ttk.Label(settings_frame, textvariable=self.wait_time_var, width=4)\
            .grid(row=0, column=2, sticky="w", padx=(0, 6), pady=(8, 4))

        ttk.Label(settings_frame, text="Batch Size:").grid(row=0, column=3, sticky="w", padx=(6, 4), pady=(8, 4))
        self.batch_size_var = tk.IntVar(value=self.settings.get("batch_size", 4))
        ttk.Scale(
            settings_frame, from_=1, to=10, variable=self.batch_size_var,
            orient="horizontal", length=160,
            command=lambda v: self.force_int(self.batch_size_var, v)
        ).grid(row=0, column=4, sticky="ew", padx=(0, 6), pady=(8, 4))
        ttk.Label(settings_frame, textvariable=self.batch_size_var, width=4)\
            .grid(row=0, column=5, sticky="w", padx=(0, 6), pady=(8, 4))

        # Row 1: Amount + Character Type
        ttk.Label(settings_frame, text="Amount:").grid(row=1, column=0, sticky="w", padx=(6, 4), pady=(4, 4))
        self.count_var = tk.IntVar(value=self.settings.get("count", 5))
        ttk.Scale(
            settings_frame, from_=0, to=10, variable=self.count_var,
            orient="horizontal", length=160,
            command=lambda v: self.force_int(self.count_var, v)
        ).grid(row=1, column=1, sticky="ew", padx=(0, 6), pady=(4, 4))
        ttk.Label(settings_frame, textvariable=self.count_var, width=4)\
            .grid(row=1, column=2, sticky="w", padx=(0, 6), pady=(4, 4))

        ttk.Label(settings_frame, text="Character Type:").grid(row=1, column=3, sticky="w", padx=(6, 4), pady=(4, 4))
        self.character_type_var = tk.StringVar(
            value=self.settings.get("character_type", CHARACTER_TYPES[0])
        )
        self.character_type_combo = ttk.Combobox(
            settings_frame, textvariable=self.character_type_var,
            values=CHARACTER_TYPES, state="readonly", width=14
        )
        self.character_type_combo.grid(row=1, column=4, columnspan=2, sticky="w", padx=(0, 6), pady=(4, 4))

        # Row 2: Author
        ttk.Label(settings_frame, text="Author:").grid(row=2, column=0, sticky="w", padx=(6, 4), pady=(4, 8))
        self.author_var = tk.StringVar(value=self.settings.get("author", ""))
        ttk.Entry(settings_frame, textvariable=self.author_var, width=40)\
            .grid(row=2, column=1, columnspan=4, sticky="ew", padx=(0, 6), pady=(4, 8))

        # ---------- Notebook ----------
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Characters tab
        self.characters_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.characters_frame, text="Characters")
        self.characters_frame.rowconfigure(1, weight=1)
        self.characters_frame.columnconfigure(0, weight=1)

        ttk.Label(self.characters_frame, text="Characters / Poem:")\
            .grid(row=0, column=0, sticky="w", padx=8, pady=(8, 0))
        self.characters_text = tk.Text(self.characters_frame, wrap="word", height=12)
        self.characters_text.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.characters_text.insert("1.0", self.settings.get("characters", ""))

        # Logs tab
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="Logs")
        self.logs_frame.rowconfigure(1, weight=1)
        self.logs_frame.columnconfigure(0, weight=1)

        ttk.Label(self.logs_frame, text="Logs:")\
            .grid(row=0, column=0, sticky="w", padx=8, pady=(8, 0))

        self.text = tk.Text(self.logs_frame, wrap="word", state="disabled")
        self.text.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def force_int(self, var, val):
        """
        Force the value to be int when scrolling the scale.
        """
        var.set(int(float(val)))

    def start(self):
        """
        Start the downloading process.
        """
        if self.is_running:
            return

        # Basic ui changes
        self.is_running = True
        self.save_settings()
        self.notebook.select(self.logs_frame)
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.set_status("Running...")
        print("▶️ Start downloading...")

        author, characters, character_type_value, wait_time, batch_size, count = prepare_data()

        # Stop if missing info
        if not author or not characters or not character_type_value:
            print("⚠️ Please provide Author, Character(s), and Character Type.")
            self.on_done()
            return

        # Start process
        self.worker = threading.Thread(
            target=self.run_job,
            args=(author, characters, character_type_value, wait_time, batch_size, count),
            daemon=True,
        )
        self.worker.start()

    def run_job(self, author, characters, character_type_value, wait_time, batch_size, count):
        """
        Background worker that actually runs the download task.
        Runs inside a thread so TextRedirector captures stdout.
        """
        try:
            run_main(
                author=author, character_type_value=character_type_value,
                characters=characters, wait_time=wait_time,
                batch_size=batch_size, count=count, headless=True,
            )
        except Exception as e:
            print(f"⚠️ Runner error: {e}")
        finally:
            self.after(0, self.on_done)

    def stop(self):
        """
        Stop button.
        """
        # Will finish
        self.on_done()

    def on_done(self):
        """
        Called when the downloading process is done or stopped.
        """
        self.is_running = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.set_status("Idle")

    def save_settings(self):
        """
        Save current settings to setting.json.
        """
        self.settings = {
            "wait_time": self.wait_time_var.get(),
            "batch_size": self.batch_size_var.get(),
            "count": self.count_var.get(),
            "character_type_value": CHAR_TYPE_VALUE.get(self.character_type_var.get()),
            "author": self.author_var.get(),
            "characters": self.characters_text.get("1.0", "end-1c"),
        }
        save_settings(self.settings)
        print("✅ Settings saved.")

    def delete_images(self):
        """
        Delete all images in the images/ folder.
        """
        images_dir = "images"
        if os.path.exists(images_dir):
            print("🗑️ Deleting all images...")
            try:
                for root, dirs, files in os.walk(images_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                print("🗑️ All images have been deleted.")
            except Exception as e:
                print(f"Error deleting images: {e}")
        else:
            print("No images folder found.")

    def set_status(self, text: str):
        """
        Set the status text.
        """
        self.status_var.set(f"Status: {text}")

    def on_close(self):
        """
        Handle window close event.
        """
        self.destroy()


if __name__ == "__main__":
    App().mainloop()
