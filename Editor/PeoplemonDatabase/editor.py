import tkinter as tk
from tkinter import ttk

from Editor.utilities.make_var import make_str_var, make_int_var, make_combo_var, make_check_var
from Editor.utilities.arrayconnector import ArrayConnector
from Editor.utilities.sortconnector import SortConnector
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.entrylabel import EntryLabel
from Editor.guicomponents.combolabel import ComboLabel
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.guicomponents.variabletext import VariableText
from Editor.guicomponents.sortbox import SortBox
from Editor.PeoplemonDatabase.saveables import *
from Editor.saveable.saveableArray import array

import collections

XP_MAP = {'Slow': 0, 'Regular': 1, 'Fast': 2}

SORT_MAP = collections.OrderedDict()

for string, func in (('Peoplemon ID', lambda p: p.id.get()),
                     ('Name', lambda p: p.name.get()),
                     ('Type', lambda p: p.type.get()),
                     ('Base XP Yield', lambda p: p.base_xp_yield.get()),
                     ('XP Group', lambda p: p.xp_group.get()),
                     ('Evolve Level', lambda p: p.evolve_level.get()),
                     ('Number of Learned Moves', lambda p: len(p.learn_moves)),
                     ('Number of Available Moves', lambda p: len(p.valid_moves)),
                     ('Attack', lambda p: p.base_stats.attack.get()),
                     ('Defense', lambda p: p.base_stats.defense.get()),
                     ('Sp. Attack', lambda p: p.base_stats.special_attack.get()),
                     ('Sp. Defense', lambda p: p.base_stats.special_defense.get()),
                     ('HP', lambda p: p.base_stats.hp.get()),
                     ('Speed', lambda p: p.base_stats.speed.get()),
                     ('Accuracy', lambda p: p.base_stats.accuracy.get()),
                     ('Evade', lambda p: p.base_stats.evade.get()),
                     ('Critical', lambda p: p.base_stats.critical.get()),
                     ('EV Attack Award', lambda p: p.ev_stats.attack.get()),
                     ('EV Defense Award', lambda p: p.ev_stats.defense.get()),
                     ('EV Sp. Attack Award', lambda p: p.ev_stats.special_attack.get()),
                     ('EV Sp. Defense Award', lambda p: p.ev_stats.special_defense.get()),
                     ('EV HP Award', lambda p: p.ev_stats.hp.get()),
                     ('EV Speed Award', lambda p: p.ev_stats.speed.get()),
                     ('EV Accuracy Award', lambda p: p.ev_stats.accuracy.get()),
                     ('EV Evade Award', lambda p: p.ev_stats.evade.get()),
                     ('EV Critical Award', lambda p: p.ev_stats.critical.get())):
    SORT_MAP[string] = func
print(SORT_MAP)

class StatsGUI(ttk.Frame):
    def __init__(self, parent=None, title='Stats'):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text=title, style='Subtitle.TLabel')
        grid = WidgetGrid(self, 2)
        self.attack = grid.add_widget(EntryLabel, text='Attack')
        self.defense = grid.add_widget(EntryLabel, text='Defense')
        self.special_attack = grid.add_widget(EntryLabel, text='Sp. Attack')
        self.special_defense = grid.add_widget(EntryLabel, text='Sp. Defense')
        self.hp = grid.add_widget(EntryLabel, text='HP')
        self.speed = grid.add_widget(EntryLabel, text='Speed')
        self.accuracy = grid.add_widget(EntryLabel, text='Accuracy')
        self.evade = grid.add_widget(EntryLabel, text='Evade')
        self.critical = grid.add_widget(EntryLabel, text='Critical')

        self.all_widgets = (self.attack, self.defense, self.special_attack, self.special_defense, self.hp,
                            self.speed, self.accuracy, self.evade, self.critical)
        label.pack()
        grid.pack(expand=tk.YES, fill=tk.X)

        for widget in self.all_widgets:
            intValidate(widget.entry, 'u16')

    def state(self, *args, **kwargs):
        for widget in self.all_widgets:
            widget.state(*args, **kwargs)


class PeoplemonEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)

        lft_frm = ttk.Frame(self)
        title = ttk.Label(lft_frm, text='Move Database Editor', style='Title.TLabel')
        self.sort = SortBox(lft_frm)
        self.items = ListChoice(lft_frm, width=50, height=12)
        self.add_button = ttk.Button(lft_frm, text='Add')
        sep6 = ttk.Separator(lft_frm)
        desc_lbl = ttk.Label(lft_frm, text='Description', style='Subtitle.TLabel')
        self.description = VariableText(lft_frm, width=40, height=10)
        sep = ttk.Separator(self, orient=tk.VERTICAL)

        middle_frm = ttk.Frame(self)
        grid = WidgetGrid(middle_frm, 4)
        self.id = grid.add_widget(EntryLabel, text='ID', expand=tk.YES)
        self.name = grid.add_widget(EntryLabel, text='Name', expand=tk.YES)
        self.base_xp = grid.add_widget(EntryLabel, text='Base XP Yield', expand=tk.YES)
        self.xp_group = grid.add_widget(ComboLabel, text='XP Group', expand=tk.YES)
        self.special_id = grid.add_widget(EntryLabel, text='Special Ability ID', expand=tk.YES)
        self.type = grid.add_widget(EntryLabel, text='Type', expand=tk.YES)
        self.evolve_level = grid.add_widget(EntryLabel, text='Evolve Level', expand=tk.YES)
        self.evolve_id = grid.add_widget(EntryLabel, text='Evolve ID', expand=tk.YES)
        sep2 = ttk.Separator(middle_frm)

        base_frm = ttk.Frame(middle_frm)
        self.base_stats = StatsGUI(base_frm, title='Base Stats')
        sep3 = ttk.Separator(base_frm, orient=tk.VERTICAL)
        self.ev_stats = StatsGUI(base_frm, title='EV Awards')

        sep4 = ttk.Separator(middle_frm)
        learn_move_frm = ttk.Frame(middle_frm)
        move_lbl = ttk.Label(learn_move_frm, text='Learned Moves', style='Subtitle.TLabel')
        self.learn_list = ListChoice(learn_move_frm, width=40, height=8)
        self.add_learn_move = ttk.Button(learn_move_frm, text='Add')
        move_frm = ttk.Frame(learn_move_frm)
        self.learn_move_id = EntryLabel(move_frm, text='Move ID')
        self.learn_level = EntryLabel(move_frm, text='Learn Level')

        sep5 = ttk.Separator(middle_frm, orient=tk.VERTICAL)
        available_frm = ttk.Frame(middle_frm)
        available_lbl = ttk.Label(available_frm, text='Available Moves', style='Subtitle.TLabel')
        self.available_list = ListChoice(available_frm, width=40, height=8)
        self.add_available_button = ttk.Button(available_frm, text='Add')
        self.available_move_id = EntryLabel(available_frm, text='Move ID')

        lft_frm.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        title.pack()
        self.sort.pack(fill=tk.X, pady=5)
        self.items.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_button.pack()
        sep6.pack(fill=tk.X, padx=10, pady=10)
        desc_lbl.pack()
        self.description.pack(expand=tk.YES, fill=tk.BOTH)

        sep.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        middle_frm.pack(side=tk.LEFT, fill=tk.BOTH)
        grid.pack(fill=tk.X)

        sep2.pack(fill=tk.X, pady=(10, 0), padx=10)
        base_frm.pack(fill=tk.X)
        self.base_stats.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)
        sep3.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.ev_stats.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

        sep4.pack(fill=tk.X, pady=10, padx=10)
        learn_move_frm.pack(side=tk.LEFT, fill=tk.BOTH)
        move_lbl.pack()
        self.learn_list.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_learn_move.pack(pady=(3, 0))
        move_frm.pack(fill=tk.X)
        self.learn_move_id.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, padx=2)
        self.learn_level.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, padx=2)

        sep5.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        available_frm.pack(side=tk.LEFT, fill=tk.BOTH)
        available_lbl.pack()
        self.available_list.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_available_button.pack(pady=(3, 0))
        self.available_move_id.pack(fill=tk.X)

        for widget in self.type, self.special_id, self.learn_level, self.evolve_level, self.evolve_id:
            intValidate(widget.entry, 'u8')

        for widget in self.id, self.base_xp, self.available_move_id, self.learn_move_id:
            intValidate(widget.entry, 'u16')


class PeoplemonEditor:

    def __init__(self, parent=None):
        self.gui = PeoplemonEditorGUI(parent)
        self.peoplemon_array = array(Peoplemon)()
        self.main_saveable = self.peoplemon_array

        gui = self.gui
        self.learn_move_connector = None
        self.available_move_connector = None
        self.item_connector = ArrayConnector(self.peoplemon_array, self.gui.items, self.gui.add_button,
                                             gui.description, gui.id, gui.name, gui.base_xp, gui.xp_group,
                                             gui.special_id, gui.type, gui.evolve_level, gui.evolve_id,
                                             gui.base_stats, gui.ev_stats, gui.learn_list, gui.learn_move_id,
                                             gui.learn_level, gui.available_list, gui.available_move_id,
                                             gui.add_available_button, gui.add_learn_move)
        self.gui.items.signal_select.connect(self.on_select)
        self.sort_connector = SortConnector(gui.items, gui.sort.combo, SORT_MAP)
        gui.learn_list.set_key(lambda learn: learn.learn_level.get())
        gui.available_list.set_key(lambda move: move.get())

    def on_select(self, id):
        peoplemon = self.item_connector.cur_selection
        gui = self.gui
        int_map = {gui.id: peoplemon.id, gui.base_xp: peoplemon.base_xp_yield,
                   gui.special_id: peoplemon.special_ability_id, gui.type: peoplemon.type,
                   gui.evolve_level: peoplemon.evolve_level, gui.evolve_id: peoplemon.evolve_id}
        for widget, saveable in int_map.items():
            widget.entry.config(textvariable=make_int_var(saveable))
        for widget, saveable in ((gui.description, peoplemon.description), (gui.name.entry, peoplemon.name)):
            widget.config(textvariable=make_str_var(saveable))
        gui.xp_group.combo.config(textvariable=make_combo_var(peoplemon.xp_group, XP_MAP))

        for stats_gui, stats, in ((self.gui.base_stats, peoplemon.base_stats), (self.gui.ev_stats, peoplemon.ev_stats)):
            for widget, saveable in ((stats_gui.attack, stats.attack), (stats_gui.defense, stats.defense),
                                     (stats_gui.special_attack, stats.special_attack),
                                     (stats_gui.special_defense, stats.special_defense),
                                     (stats_gui.hp, stats.hp), (stats_gui.speed, stats.speed),
                                     (stats_gui.accuracy, stats.accuracy), (stats_gui.evade, stats.evade),
                                     (stats_gui.critical, stats.critical)):
                widget.entry.config(textvariable=make_int_var(saveable))
        self.learn_move_connector = ArrayConnector(peoplemon.learn_moves, gui.learn_list, gui.add_learn_move,
                                                   gui.learn_move_id, gui.learn_level)
        self.available_move_connector = ArrayConnector(peoplemon.valid_moves, gui.available_list,
                                                       gui.add_available_button, gui.available_move_id)
        self.gui.learn_list.signal_select.connect(self.on_learn_move_select)
        self.gui.available_list.signal_select.connect(self.on_available_move_select)

    def on_learn_move_select(self, ind):
        if ind is None:
            return
        learn_move = self.item_connector.cur_selection.learn_moves[ind]
        for widget, saveable in ((self.gui.learn_move_id, learn_move.move_id),
                                 (self.gui.learn_level, learn_move.learn_level)):
            widget.entry.config(textvariable=make_int_var(saveable))

    def on_available_move_select(self, ind):
        if ind is None:
            return
        move = self.item_connector.cur_selection.valid_moves[ind]
        self.gui.available_move_id.entry.config(textvariable=make_int_var(move))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)


if __name__ == '__main__':
    root = tk.Tk()
    from Editor.styles import configure_styles
    configure_styles()
    editor = PeoplemonEditor(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()