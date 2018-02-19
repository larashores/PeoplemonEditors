import tkinter as tk
from tkinter import ttk

from Editor.signal import Signal


class ListChoiceGUI(ttk.Frame):
    def __init__(self, parent=None, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.signal_delete = Signal()
        self.signal_up = Signal()
        self.signal_down = Signal()
        self.signal_select = Signal()

        frm = ttk.Frame(self)
        self.lbox = tk.Listbox(frm, selectmode=tk.SINGLE, **kwargs)
        self.sbar = ttk.Scrollbar(frm)
        self.hsbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)

        self.hsbar.config(command=self.lbox.xview)
        self.sbar.config(command=self.lbox.yview)
        self.lbox.config(xscrollcommand=self.hsbar.set)
        self.lbox.config(yscrollcommand=self.sbar.set)
        self.lbox.config(selectmode=tk.SINGLE)

        self.sbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.lbox.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frm.pack(expand=tk.YES, fill=tk.BOTH)

        self.lbox.bind('<Delete>', lambda event: self.signal_delete() if self.lbox.size() >= 1 else None)
        self.lbox.bind('<Button-1>', lambda event: self.after(20, self._click))
        self.lbox.bind('<Up>', lambda event: self.signal_up())
        self.lbox.bind('<Down>', lambda event: self.signal_down())

    def _click(self):
        val = self.lbox.curselection()
        if len(val) != 1:
            pass
        else:
            self.signal_select(val[0])

    def state(self, *args, **kwargs):
        pass

    def update_selection(self, ind):
        self.lbox.selection_clear(0, tk.END)
        self.lbox.selection_set(ind)
        self.after(20, lambda: self.lbox.activate(ind))


class ListChoice:
    def __init__(self, parent=None, **kwargs):
        self.signal_select = Signal()
        self.signal_delete = Signal()

        self._gui = ListChoiceGUI(parent, **kwargs)
        self._choices = []
        self._cur_selection = None

        self._gui.signal_select.connect(self.set_selection)
        self._gui.signal_delete.connect(self.signal_delete)
        self._gui.signal_up.connect(self._up)
        self._gui.signal_down.connect(self._down)

    def itemconfig(self, *args, **kwargs):
        self._gui.lbox.itemconfig(*args, **kwargs)

    def __getitem__(self, index):
        return self._choices[index][1]

    def __len__(self):
        return len(self._choices)

    def __iter__(self, *args, **kwargs):
        return self._choices.__iter__(*args, **kwargs)

    def state(self, *args, **kwargs):
        self._gui.state(*args, **kwargs)

    def pack(self, **kwargs):
        self._gui.pack(**kwargs)

    def append(self, string, data=None):
        self.insert(len(self._choices), string, data)

    def insert(self, ind, string, data=None):
        if data is None:
            data = string
        self._choices.insert(ind, (string, data))
        self._gui.lbox.insert(ind, string)

    def pop(self, ind=-1):
        val = self._choices.pop(ind)
        self._gui.lbox.delete(ind)
        return val[1]

    def remove_data(self, data):
        to_remove = (ind for ind, x in enumerate(self._choices) if x[1] == data)
        for ind in to_remove:
            self.pop(ind)

    def clear(self):
        self._choices.clear()
        self._gui.lbox.delete(0, tk.END)
        self._cur_selection = None

    def get_selection(self):
        return self._cur_selection

    def set_selection(self, ind):
        if not len(self._choices):
            return
        ind %= len(self._choices)
        self._cur_selection = ind
        self._gui.update_selection(ind)
        self.signal_select(ind)

    def get_top(self):
        return self._gui.lbox.yview()[0] * len(self._choices)

    def set_top(self, top=None):
        if not self._choices:
            return
        if top is None:
            top = len(self._choices) - 1
        value = top / len(self._choices)
        self._gui.lbox.yview_moveto(value)

    def update_str(self, ind, string):
        top = self.get_top()
        self._choices[ind] = (string, self._choices[ind][1])
        self._gui.lbox.delete(ind)
        self._gui.lbox.insert(ind, string)
        self._gui.update_selection(ind)
        self.set_top(top)

    def _up(self):
        ind = self._cur_selection
        if ind > 0:
            self.set_selection(ind - 1)

    def _down(self):
        ind = self._cur_selection
        if self._cur_selection < len(self._choices) - 1:
            self.set_selection(ind + 1)

if __name__ == '__main__':
    root = tk.Tk()

    def delete():
        if list1:
            print('deleting ' + str(list1.get_selection()))
            list1.pop(list1.get_selection())
    list1 = ListChoice()
    list1.pack(expand=tk.YES, fill=tk.BOTH)

    list1.signal_delete.connect(delete)

    for choice in ['first', 'second', 'third', 'fifth', 'sixth', 'seventh', 'eight', 'ninth', 'tenth']:
        list1.append(choice)
    list1.insert(0, "zeroth")
    list1.insert(4, "fourth")
    list1.append('eleventh', 7)
    list1.set_top()
    list1.remove_data(7)
    tk.mainloop()
