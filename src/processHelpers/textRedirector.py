class TextRedirector:
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag

    def write(self, msg):
        if msg:
            self.text_widget.after(0, self.append, msg)

    def flush(self):
        pass

    def append(self, msg):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", msg, (self.tag,))
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")