import tkinter as tk
from tkinter import ttk


class ButtonGrid(ttk.Frame):
    def __init__(self, parent, columns):
        ttk.Frame.__init__(self, parent)
        self.n_cols = columns
        self.cur_ind = 0
        self.rows = []

    def addButton(self, txt, cmd=lambda: None):
        row = self._get_row()
        if row <= len(self.rows):
            self.rows.append(ttk.Frame(self))
            self.rows[row].pack()
        button = ttk.Button(self.rows[row], text=txt, command=cmd)
        button.pack(side=tk.LEFT, padx=(2, 2), pady=(2, 2))

    def _get_row(self):
        row = self.cur_ind // self.n_cols
        self.cur_ind += 1
        return row