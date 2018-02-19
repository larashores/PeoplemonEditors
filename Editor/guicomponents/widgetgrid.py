import tkinter as tk
from tkinter import ttk


class WidgetGrid(ttk.Frame):
    def __init__(self, parent, columns):
        ttk.Frame.__init__(self, parent)
        self.n_cols = columns
        self.cur_ind = 0
        self.rows = []
        self.expand_overrides = {}
        self.fill_overrides = {}
        self.padx_overrdies = {}
        self.pady_overrides = {}

    def pack(self, expand=tk.NO, fill=tk.NONE, **kwargs):
        for row_list in self.rows:
            row_list[0].pack(expand=tk.YES, fill=tk.BOTH)
            for ind, widget in enumerate(row_list):
                if ind == 0:
                    continue
                else:
                    e = expand if widget not in self.expand_overrides else self.expand_overrides[widget]
                    f = fill if widget not in self.fill_overrides else self.fill_overrides[widget]
                    x = 2 if widget not in self.padx_overrdies else self.padx_overrdies[widget]
                    y = 2 if widget not in self.pady_overrides else self.pady_overrides[widget]
                    widget.pack(expand=e, fill=f, side=tk.LEFT, padx=x, pady=y)
        ttk.Frame.pack(self, expand=expand, fill=fill, **kwargs)

    def add_widget(self, WidgetType, expand=None, fill=None, padx=None, pady=None, *args, **kwargs):
        row = self._get_row()
        if row == len(self.rows):
            self.rows.append([ttk.Frame(self)])
        cur = self.rows[row]
        widget = WidgetType(cur[0], *args, **kwargs)
        cur.append(widget)
        if expand is not None:
            self.expand_overrides[widget] = expand
        if fill is not None:
            self.fill_overrides[widget] = fill
        if padx is not None:
            self.padx_overrdies[widget] = padx
        if pady is not None:
            self.pady_overrides[widget] = pady
        return widget

    def _get_row(self):
        row = self.cur_ind // self.n_cols
        self.cur_ind += 1
        return row


if __name__ == '__main__':
    root = tk.Tk()
    grid = WidgetGrid(root, 2)
    for _ in range(10):
        grid.add_widget(ttk.Entry, text='adf')
    grid.pack(expand=tk.YES, fill=tk.X)
    root.mainloop()
