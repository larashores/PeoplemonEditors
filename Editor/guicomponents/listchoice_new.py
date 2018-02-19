"""
#-------------------------------------------------------------------------------
# Name:        listchoice.py

# Author:      Vincent
#
# Date Created:     01/15/2015
# Date Modified:    01/15/2015
#-------------------------------------------------------------------------------

Purpose:

"""

import inspect

import tkinter as tk
from tkinter import ttk


class ListChoiceGUI(ttk.Frame):
    """
    Purpose:    Scrolling Listbox where entries can be added and deleted
    Attributes:
        parent:     Parent widget
        choicelist: The list where choice strings are stored
        indexvar:   IntVar where the selected index is stored
    """
    def __init__(self, parent, controller, update_cmd, delete_cmd, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.update_cmd = update_cmd
        self.delete_cmd = delete_cmd
        self.lbox = None
        self.sbar = None
        self.hsbar = None
        self.last_selection = None
        self.MakeWidgets(kwargs)
        if delete_cmd is not None:
            self.lbox.bind('<Delete>', lambda event: self.delete())
        self.lbox.bind('<Button-1>', lambda event: self.click())
        self.lbox.bind('<Up>', lambda event: self.up())
        self.lbox.bind('<Down>', lambda event: self.down())

    def MakeWidgets(self, kwargs):
        frm = ttk.Frame(self)
        sbar = ttk.Scrollbar(frm)
        lbox = tk.Listbox(frm, selectmode=tk.SINGLE,  **kwargs)
        sbar.config(command=lbox.yview)
        lbox.config(yscrollcommand=sbar.set)
        lbox.config(selectmode=tk.SINGLE)

        hsbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        hsbar.config(command=lbox.xview)
        lbox.config(xscrollcommand=hsbar.set)

        sbar.pack(side=tk.RIGHT, fill=tk.Y)
        hsbar.pack(side=tk.BOTTOM, fill=tk.X)
        lbox.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frm.pack(expand=tk.YES, fill=tk.BOTH)

        self.lbox = lbox
        self.sbar = sbar
        self.hsbar = hsbar

    def delete(self):
        if self.controller.getSelection() is not None:
            self.delete_cmd(self.controller.getSelection())

    def click(self):
        self.after(20, self._click)

    def _click(self):
        val = self.lbox.curselection()
        if len(val) != 1:
            pass
        else:
            self.controller.setSelection(val[0])

    def up(self):
        ind = self.controller.getSelection()
        self.controller.up()

    def down(self):
        ind = self.controller.getSelection()
        self.controller.down()

    def updateSelection(self):
        ind = self.controller.getSelection()
        self.lbox.selection_clear(0, tk.END)
        self.lbox.selection_set(ind)
        self.after(20, lambda: self.lbox.activate(ind))
        self.update_cmd(ind)


class ListChoice:
    def __init__(self, parent=None, *,
                 update_cmd=lambda x: None,
                 delete_cmd=lambda x: None,
                 **kwargs):
        self.model = ListChoiceModel()
        self.gui = ListChoiceGUI(parent, self, update_cmd, delete_cmd, **kwargs)

    def __iter__(self):
        for choice in self.model:
            yield choice

    def __getitem__(self, index):
        return self.model.choices[index]

    def __len__(self):
        return len(self.model.choices)

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)

    def index(self, ind):
        return self.model.choices.index(ind)

    def addChoice(self, string):
        self.model.addChoice(string)
        self.model.setCurrentIndex(-1)
        self.update()

    def insertChoice(self, ind, string):
        if ind < 0 and len(self) != 0:
            ind %= (len(self) + 1)
        self.model.insertChoice(ind, string)
        self.model.setCurrentIndex(ind)
        self.update()

    def setPosition(self, ind):
        if ind < 0 and len(self) != 0:
            ind %= (len(self) + 1)
        self.gui.lbox.yview_moveto(ind)

    def get_top(self):
        return (self.gui.lbox.yview()[0]) * len(self)

    def set_top(self, top):
        if len(self) == 0:
            return
        value = top / len(self)
        self.gui.lbox.yview_moveto(value)

    def getYPosition(self):
        return self.gui.lbox.yview()[1]

    def delete(self, ind):
        self.model.delete(int(ind))
        self.update()
        if self.getSelection() is not None:
            self.gui.updateSelection()

    def clear(self):
        self.model.choices.clear()
        self.update()
        self.model.cur_selection = None

    def update(self):
        self.gui.lbox.delete(0, tk.END)
        for choice in self.model:
            self.gui.lbox.insert(tk.END, choice)

    def choices(self):
        return list(self.model)

    def getSelection(self):
        return self.model.getCurentIndex()

    def setSelection(self, ind):
        if ind < 0 and ind >= -len(self):
            ind %= len(self)

        l_ind = self.getSelection()
        if l_ind != int(ind):
            self.model.setCurrentIndex(ind)
        self.gui.updateSelection()

    def up(self):
        l_ind = self.getSelection()
        self.model.up()
        if l_ind != self.getSelection():
            self.gui.updateSelection()

    def down(self):
        l_ind = self.getSelection()
        self.model.down()
        if l_ind != self.getSelection():
            self.gui.updateSelection()

    def getPosition(self):
        return self.gui.lbox.yview()[0]

class ListChoiceModel:
    def __init__(self):
        self.choices = []
        self.cur_selection = None

    def __iter__(self):
        for choice in self.choices:
            yield choice

    def addChoice(self, string):
        self.choices.append(string)
        if self.cur_selection is None:
            self.cur_selection = 0

    def insertChoice(self, ind, string):
        self.choices.insert(ind, string)
        if self.cur_selection is None:
            self.cur_selection = 0

    def setCurrentIndex(self, ind):
        if ind is not None and ind < 0:
            ind = len(self.choices) - ind
        self.cur_selection = ind

    def getCurentIndex(self):
        return self.cur_selection

    def up(self):
        ind = self.getCurentIndex()
        if ind > 0:
            self.cur_selection = ind - 1

    def down(self):
        ind = self.getCurentIndex()
        if ind < len(self.choices)-1:
            self.cur_selection = ind + 1

    def delete(self, ind):
        self.choices.pop(ind)
        if ind == self.cur_selection:
            if self.cur_selection == 0:
                if len(self.choices) == 0:
                    self.cur_selection = None
            else:
                if len(self.choices)-1 > self.cur_selection:
                    self.cur_selection += 0
                else:
                    self.cur_selection -= 1
        elif ind < self.cur_selection:
            self.cur_selection -= 1
        else:
            pass



if __name__ == '__main__':
    root = tk.Tk()

    def delete(ind):
        list1.delete(ind)
    list1 = ListChoice(update_cmd=lambda ind: print('Selecting', ind), delete_cmd=delete)
    list1.pack(expand=tk.YES, fill=tk.BOTH)

    for choice in ['1', 'poop', '2', '4asfd','45','hey','adga','meeee','asdfas','425','adsf']:
        list1.addChoice(choice)
    list1.setSelection(10)


    tk.mainloop()

