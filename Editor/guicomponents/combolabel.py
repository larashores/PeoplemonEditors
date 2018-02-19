from tkinter import ttk
import tkinter as tk


class ComboLabel(ttk.Frame):
    def __init__(self, parent=None, *, text=None, values=None):
        ttk.Frame.__init__(self, parent)
        self.label = ttk.Label(self, text=text, anchor=tk.CENTER)
        self.combo = ttk.Combobox(self, values=values, justify=tk.CENTER, width=17,)

        self.label.pack(fill=tk.X)
        self.combo.pack(expand=tk.YES, fill=tk.X)

    def state(self, statespec=None):
        self.label.state(statespec)
        self.combo.state(statespec)
        return ttk.Frame.state(self, statespec)
