import tkinter as tk
from tkinter import ttk


class SortBox(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        sort_lbl = ttk.Label(self, text='Sort By: ')
        self.combo = ttk.Combobox(self, justify=tk.CENTER)

        sort_lbl.pack(side=tk.LEFT)
        self.combo.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, padx=(0, 20))

        self.combo.state(['readonly'])
