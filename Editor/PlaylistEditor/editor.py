import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.entrylabel import EntryLabel
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.PlaylistEditor.saveables import Playlist
from Editor.utilities.make_var import make_int_var, make_str_var
from Editor.utilities.arrayconnector import ArrayConnector


class PlaylistEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        title = ttk.Label(self, text='Playlist Editor', style='Title.TLabel')
        self.songs = ListChoice(self)
        self.name = EntryLabel(self, text='Song Name', width=50)
        self.button = ttk.Button(self, text='Add')

        title.pack()
        self.songs.pack(expand=tk.YES, fill=tk.BOTH)
        self.name.pack(fill=tk.X, pady=10)
        self.button.pack(fill=tk.X)


class PlaylistEditor:
    def __init__(self, parent=None):
        self.gui = PlaylistEditorGUI(parent)
        self.playlist = Playlist()
        self.main_saveable = self.playlist
        self.connector = ArrayConnector(self.playlist, self.gui.songs, self.gui.button, self.gui.name)
        self.connector.bind_move()
        self.gui.songs.signal_select.connect(self.on_select)

    def on_select(self, ind):
        current = self.connector.cur_selection
        self.gui.name.entry.config(textvariable=make_str_var(current))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)