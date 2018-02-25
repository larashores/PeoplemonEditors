import tkinter as tk


class SortConnector:
    def __init__(self, listchoice, combo, sortmap):
        self.listchoice = listchoice
        self.combo = combo
        self.sortmap = sortmap
        self.var = tk.StringVar()
        self.var.trace('w', lambda *args: self.listchoice.set_key(self.sortmap[self.var.get()]))
        self.var.set(list(sortmap.keys())[0])
        combo.config(textvariable=self.var, values=list(sortmap.keys()))
