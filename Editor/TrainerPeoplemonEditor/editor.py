import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.TrainerPeoplemonEditor.saveables import TrainerPeoplemon
from Editor.utilities.make_var import make_int_var, make_str_var


class TrainerPeoplemonEditorGUI(ttk.Frame):
    STATS = 'HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Accuracy', 'Evade', 'Speed', 'Critical'

    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)

        second_row_frm = ttk.Frame(self)
        leftFrm = ttk.Frame(second_row_frm)
        sep1 = ttk.Separator(second_row_frm, orient=tk.VERTICAL)
        middleFrm = ttk.Frame(second_row_frm)
        sep2 = ttk.Separator(second_row_frm, orient=tk.VERTICAL)
        rightFrm = ttk.Frame(second_row_frm)
        moves_lbl_frm = ttk.Frame(leftFrm)

        title = ttk.Label(self, text='Trainer Peoplemon Editor', style='Title.TLabel')
        grid1 = WidgetGrid(leftFrm, 2)
        self.nick = grid1.add_widget(EntryLabel, text='Nickname')
        self.id = grid1.add_widget(EntryLabel, text='ID')
        self.level = grid1.add_widget(EntryLabel, text='Level')
        self.xp = grid1.add_widget(EntryLabel, text='Current XP')
        self.next_xp = grid1.add_widget(EntryLabel, text='XP Until Level Up')
        self.cur_hp = grid1.add_widget(EntryLabel, text='Current HP')
        self.cur_ail = grid1.add_widget(EntryLabel, text='Ailment')
        self.hold = grid1.add_widget(EntryLabel, text='Hold Item ID')
        sep3 = ttk.Separator(leftFrm)

        for entrylabel, int_type in ((self.id, 'u16'),
                                     (self.level, 'u16'),
                                     (self.xp, 'u32'),
                                     (self.next_xp, 'u32'),
                                     (self.cur_hp, 'u16'),
                                     (self.cur_ail, 'u8'),
                                     (self.hold, 'u16')):
            intValidate(entrylabel.entry, int_type)

        move_lbl = ttk.Label(leftFrm, text='Moves', style='Subtitle.TLabel')
        id_lbl = ttk.Label(moves_lbl_frm, text='IV')
        pp_lbl = ttk.Label(moves_lbl_frm, text='PP')
        self.moves_widgets = []
        grid2 = WidgetGrid(leftFrm, 2)
        for _ in range(8):
            widget = grid2.add_widget(ttk.Entry, justify=tk.CENTER)
            intValidate(widget, 'u16')
            self.moves_widgets.append(widget)

        iv_title = ttk.Label(middleFrm, text='IVs', style='Subtitle.TLabel')
        self.iv_widgets, grid3 = self.make_base_stats_widget(middleFrm)

        ev_title = ttk.Label(rightFrm, text='EVs', style='Subtitle.TLabel')
        self.ev_widgets, grid4 = self.make_base_stats_widget(rightFrm)

        title.pack()
        second_row_frm.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=(0, 10))
        leftFrm.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT,)
        grid1.pack(expand=tk.YES, fill=tk.X)
        sep3.pack(fill=tk.X, padx=(5, 5), pady=(12, 0))
        move_lbl.pack()
        moves_lbl_frm.pack(fill=tk.X, padx=(3, 3))
        id_lbl.pack(side=tk.LEFT, expand=tk.YES)
        pp_lbl.pack(side=tk.LEFT, expand=tk.YES)
        grid2.pack(expand=tk.YES, fill=tk.X)
        sep1.pack(fill=tk.Y, pady=(5, 5), padx=10, side=tk.LEFT)

        middleFrm.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)
        iv_title.pack()
        grid3.pack(expand=tk.YES, fill=tk.X)
        sep2.pack(fill=tk.Y, pady=(5, 5), padx=10, side=tk.LEFT)

        rightFrm.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)
        ev_title.pack()
        grid4.pack(expand=tk.YES, fill=tk.X)

    def make_base_stats_widget(self, parent=None):
        grid = WidgetGrid(parent, 2)
        widgets = []
        for text in self.STATS:
            widget = grid.add_widget(EntryLabel, text=text)
            intValidate(widget.entry, 'u16')
            widgets.append(widget)
        return widgets, grid


class TrainerPeoplemonEditor:
    def __init__(self, parent=None):
        self.gui = TrainerPeoplemonEditorGUI(parent)
        self.peoplemon = TrainerPeoplemon()
        self.main_saveable = self.peoplemon
        int_entry_map = {self.gui.id: self.peoplemon.id,
                         self.gui.level: self.peoplemon.level,
                         self.gui.xp: self.peoplemon.cur_xp,
                         self.gui.next_xp: self.peoplemon.next_level_up_xp,
                         self.gui.cur_hp: self.peoplemon.cur_hp,
                         self.gui.cur_ail: self.peoplemon.cur_ail,
                         self.gui.hold: self.peoplemon.hold_item}
        for widget, saveable in int_entry_map.items():
            widget.entry.config(textvariable=make_int_var(saveable))
        moves = (self.peoplemon.move1.id, self.peoplemon.move1.pp, self.peoplemon.move2.id, self.peoplemon.move2.pp,
                 self.peoplemon.move3.id, self.peoplemon.move3.pp, self.peoplemon.move4.id, self.peoplemon.move4.pp)
        for entry, saveable in zip(self.gui.moves_widgets, moves):
            entry.config(textvariable=make_int_var(saveable))
        for widget, saveable in zip(self.gui.iv_widgets, [x for x in self.peoplemon.ivs]):
            widget.entry.config(textvariable=make_int_var(saveable))
        for widget, saveable in zip(self.gui.ev_widgets, [x for x in self.peoplemon.evs]):
            widget.entry.config(textvariable=make_int_var(saveable))
        self.gui.nick.entry.config(textvariable=make_str_var(self.peoplemon.nickname))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)

if __name__ == '__main__':
    root = tk.Tk()
    editor = TrainerPeoplemonEditorGUI()
    editor.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=(5, 10))
    root.mainloop()

