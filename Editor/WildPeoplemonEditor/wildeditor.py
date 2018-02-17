import tkinter as tk
from tkinter import ttk

from utilities.arrayconnector import ArrayConnector
from Editor.utilities.make_var import make_int_var, make_str_var
from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice_2 import ListChoice
from Editor.guicomponents.integercheck import intValidate
from WildPeoplemonEditor.saveables import WildPeoplemon


class WildEditorGUI(ttk.Frame):
    def __init__(self, *args, **kwargs):
        ttk.Frame.__init__(self, *args, **kwargs)
        title = ttk.Label(self, text='Wild Pokemon Editor', style='Title.TLabel')
        self.entry_id = EntryLabel(self, text='ID')
        self.entry_min = EntryLabel(self, text='Minimum Level')
        self.entry_max = EntryLabel(self, text='Maximum Level')
        self.entry_rarity = EntryLabel(self, text='Rarity (1-?)')
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.string = EntryLabel(self, text='String Code')
        self.code = EntryLabel(self, text='Value')
        self.choices = ListChoice(self)
        self.add = ttk.Button(self, text='Add')

        for entry in (self.entry_id, self.entry_min, self.entry_max, self.entry_rarity, self.code):
            intValidate(entry.entry, 'u16')

        title.pack(padx=10)
        self.entry_id.pack(padx=10, expand=tk.YES, fill=tk.X)
        self.entry_min.pack(padx=10, expand=tk.YES, fill=tk.X)
        self.entry_max.pack(padx=10, expand=tk.YES, fill=tk.X)
        self.entry_rarity.pack(padx=10, expand=tk.YES, fill=tk.X)
        sep.pack(fill=tk.X, pady=(12, 0), padx=5)
        self.string.pack(padx=10, expand=tk.YES, fill=tk.X)
        self.code.pack(padx=10, expand=tk.YES, fill=tk.X)
        self.choices.pack(padx=10, pady=(10, 5), expand=tk.YES, fill=tk.X)
        self.add.pack(pady=(5, 10))


class WildEditor:
    def __init__(self, parent=None):
        self.gui = WildEditorGUI(parent)
        self.peoplemon = WildPeoplemon()
        self.main_saveable = self.peoplemon
        for entry, int_type in ((self.gui.entry_id, self.peoplemon.id),
                                (self.gui.entry_min, self.peoplemon.min_lvl),
                                (self.gui.entry_max, self.peoplemon.max_lvl),
                                (self.gui.entry_rarity, self.peoplemon.rarity)):
            entry.entry.config(textvariable=make_int_var(int_type))

        self.array_connector = ArrayConnector(self.peoplemon.overrides, self.gui.choices, self.gui.add,
                                              self.gui.code, self.gui.string)
        self.gui.choices.signal_select.connect(self.select_override)

    def select_override(self, ind):
        if ind is not None:
            current = self.array_connector.cur_selection
            self.gui.string.entry.config(textvariable=make_str_var(current.code))
            self.gui.code.entry.config(textvariable=make_int_var(current.override))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)
