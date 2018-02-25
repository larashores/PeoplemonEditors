import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.integercheck import intValidate
from Editor.utilities.arrayconnector import ArrayConnector
from Editor.utilities.make_var import make_int_var, make_str_var
from Editor.TravelMapEditor.saveables import Location
from Editor.saveable.saveableArray import array


class TravelEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.entries = []
        title = ttk.Label(self, text='Travel Map Editor', style='Title.TLabel')
        self.maps = ListChoice(self)
        self.add_button = ttk.Button(self, text='Add')
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        top = ttk.Frame(self)
        mid = ttk.Frame(self)
        bot = ttk.Frame(self)
        self.entry_x = EntryLabel(top, text='X Position')
        self.entry_y = EntryLabel(top, text='Y Position')
        self.entry_display = EntryLabel(mid, text='Display Name')
        self.entry_ref = EntryLabel(mid, text='Reference Name')
        self.entry_map = EntryLabel(bot, text='Map Name')
        self.entry_spawn = EntryLabel(bot, text='Spawn ID')
        self.entries += self.entry_x, self.entry_y, self.entry_display, self.entry_ref, self.entry_map, self.entry_spawn

        title.pack()
        self.maps.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_button.pack(pady=10)
        sep.pack(fill=tk.X, padx=10)
        top.pack(fill=tk.BOTH)
        mid.pack(fill=tk.BOTH)
        bot.pack(fill=tk.BOTH)
        self.entry_x.pack(expand=tk.YES, fill=tk.X, side=tk.LEFT, padx=(0, 5))
        self.entry_y.pack(expand=tk.YES, fill=tk.X,  side=tk.LEFT, padx=(5, 0))
        self.entry_display.pack(expand=tk.YES, fill=tk.X,  side=tk.LEFT, padx=(0, 5))
        self.entry_ref.pack(expand=tk.YES, fill=tk.X,  side=tk.LEFT, padx=(5, 0))
        self.entry_map.pack(expand=tk.YES, fill=tk.X,  side=tk.LEFT, padx=(0, 5))
        self.entry_spawn.pack(expand=tk.YES, fill=tk.X,  side=tk.LEFT, padx=(5, 0), pady=(10, 2))

        for entry in self.entry_x, self.entry_y, self.entry_spawn:
            intValidate(entry.entry, 'u16')


class TravelEditor:
    MapType = array(Location)

    def __init__(self, parent=None):
        self.gui = TravelEditorGUI(parent)
        self.maps = self.MapType()
        self.main_saveable = self.maps
        for entry in self.gui.entries:
            entry.state(('disabled', ))
        self.cur_selected = None

        self.array_connector = ArrayConnector(self.maps, self.gui.maps, self.gui.add_button, *self.gui.entries)
        self.gui.maps.signal_select.connect(self.select_override)
        self.gui.maps.set_key(lambda map: map.spawn_id.get())

    def select_override(self, ind):
        if ind is not None:
            current = self.array_connector.cur_selection
            int_map = {self.gui.entry_x: current.x,
                       self.gui.entry_y: current.y,
                       self.gui.entry_spawn: current.spawn_id}
            str_map = {self.gui.entry_display: current.display_name,
                       self.gui.entry_ref: current.reference_name,
                       self.gui.entry_map: current.map_name}
            for entry, saveable in int_map.items():
                entry.entry.config(textvariable=make_int_var(saveable))
            for entry, saveable in str_map.items():
                entry.entry.config(textvariable=make_str_var(saveable))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)
