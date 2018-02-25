import tkinter as tk
from tkinter import ttk

from Editor.utilities.make_var import make_str_var, make_int_var
from utilities.arrayconnector import ArrayConnector
from utilities.sortconnector import SortConnector
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.guicomponents.variabletext import VariableText
from Editor.guicomponents.sortbox import SortBox
from Editor.ItemDatabase.saveables import *
from Editor.saveable.saveableArray import array

import collections

SORT_MAP = collections.OrderedDict((('Item ID', lambda item: item.id.get()),
                                   ('Item Name', lambda item: item.name.get()),
                                   ('Item Price', lambda item: item.price.get())))


class ItemEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)

        title = ttk.Label(self, text='Item Database Editor', style='Title.TLabel')
        self.sort = SortBox(self)
        self.items = ListChoice(self)
        sep = ttk.Separator(self)
        self.add_button = ttk.Button(self, text='Add')
        grid = WidgetGrid(self, 2)
        self.id = grid.add_widget(EntryLabel, text='ID', expand=tk.YES)
        self.price = grid.add_widget(EntryLabel, text='Sell Price', expand=tk.YES)
        self.name = grid.add_widget(EntryLabel, text='Name', expand=tk.YES)
        description_label = ttk.Label(self, text='Description')
        self.description = VariableText(self, height=10, width=50)

        title.pack()
        self.sort.pack(expand=tk.YES, fill=tk.X, pady=5)
        self.items.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_button.pack()
        sep.pack(fill=tk.X, pady=(10, 0), padx=10)
        grid.pack(fill=tk.X)
        description_label.pack()
        self.description.pack(fill=tk.BOTH)

        intValidate(self.id.entry, 'u16')
        intValidate(self.price.entry, 'u32')


class ItemEditor:
    def __init__(self, parent=None):
        self.gui = ItemEditorGUI(parent)
        self.sort_connector = SortConnector(self.gui.items, self.gui.sort.combo, SORT_MAP)
        self.items = array(Item)()
        self.main_saveable = self.items

        self.item_connector = ArrayConnector(self.items, self.gui.items, self.gui.add_button,
                                             self.gui.id, self.gui.name, self.gui.price,
                                             self.gui.description)
        self.gui.items.signal_select.connect(self.on_select)

    def on_select(self, ind):
        if ind is None:
            return
        item = self.item_connector.cur_selection
        for widget, saveable, var_func in (
                (self.gui.id.entry, item.id, make_int_var),
                (self.gui.name.entry, item.name, make_str_var),
                (self.gui.price.entry, item.price, make_int_var),
                (self.gui.description, item.description, make_str_var)):
            widget.configure(textvariable=var_func(saveable))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)

if __name__ == '__main__':
    root = tk.Tk()
    editor = ItemEditorGUI(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()