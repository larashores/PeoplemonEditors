import tkinter as tk
from tkinter import ttk

from Editor.utilities.make_var import make_str_var, make_int_var, make_combo_var, make_check_var
from Editor.utilities.arrayconnector import ArrayConnector
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.entrylabel import EntryLabel
from Editor.guicomponents.combolabel import ComboLabel
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.guicomponents.variabletext import VariableText
from Editor.guicomponents.sortbox import SortBox
from Editor.MoveDatabase.saveables import *
from Editor.saveable.saveableArray import array

import collections

CLASSIFICATIONS = {'Direct Attack': 0,
                   'Passive Attack': 1,
                   'Direct Defense': 2,
                   'Passive Defense': 3,
                   'Attacking Ailment': 4,
                   'Defending Ailment': 5}

SORT_MAP = collections.OrderedDict()
for string, func in (('ID', lambda move: move.id.get()),
                     ('Name', lambda move: move.name.get()),
                     ('Classification', lambda move: move.classification.get()),
                     ('Description', lambda move: move.description.get()),
                     ('Attack', lambda move: move.attack.get()),
                     ('Accuracy', lambda move: move.accuracy.get()),
                     ('Effect', lambda move: move.effect.get()),
                     ('Chance of Effect', lambda move: move.effect_chance.get()),
                     ('Effect Intensity', lambda move: move.effect_intensity.get()),
                     ('Effect Score', lambda move: move.effect_score.get()),
                     ('Priority', lambda move: move.priority.get()),
                     ('PP', lambda move: move.pp.get()),
                     ('Type', lambda move: move.type.get()),
                     ('is Special', lambda move: move.is_special.get()),
                     ('Targets Self', lambda move: move.effect_targets_self.get())):
    SORT_MAP['Move ' + string] = func


class MoveEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)

        lft_frm = ttk.Frame(self)
        title = ttk.Label(lft_frm, text='Move Database Editor', style='Title.TLabel')
        self.sort = SortBox(lft_frm)
        self.items = ListChoice(lft_frm, width=50)
        self.add_button = ttk.Button(lft_frm, text='Add')

        right_frm = ttk.Frame(self)
        sep2 = ttk.Separator(self, orient=tk.VERTICAL)

        self.name = EntryLabel(right_frm, text='Name')
        id_frm = ttk.Frame(right_frm)
        self.id = EntryLabel(id_frm, text='ID')
        self.classification = ComboLabel(id_frm, text='Move Classification', values=list(CLASSIFICATIONS.keys()))
        grid = WidgetGrid(right_frm, 3)
        self.attack = grid.add_widget(EntryLabel, text='Attack')
        self.accuracy = grid.add_widget(EntryLabel, text='Accuracy')
        self.effect = grid.add_widget(EntryLabel, text='Effect')
        self.priority = grid.add_widget(EntryLabel, text='Priority')
        self.pp = grid.add_widget(EntryLabel, text='PP')
        self.type = grid.add_widget(EntryLabel, text='Type')
        self.chance = grid.add_widget(EntryLabel, text='Chance of Effect')
        self.intensity = grid.add_widget(EntryLabel, text='Effect Intensity')
        self.score = grid.add_widget(EntryLabel, text='Effect Score')
        self.attacker_anim = grid.add_widget(EntryLabel, text='Attacker Anim', expand=tk.YES)
        self.defender_anim = grid.add_widget(EntryLabel, text='Defender Anim', expand=tk.YES)
        chk_frm = ttk.Frame(right_frm)
        self.is_special = ttk.Checkbutton(chk_frm, text='Is Special')
        self.targets_self = ttk.Checkbutton(chk_frm, text='Targets Self')

        description_label = ttk.Label(right_frm, text='Description')
        self.description = VariableText(right_frm, height=10, width=40)

        lft_frm.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        title.pack()
        self.sort.pack(fill=tk.X, pady=5)
        self.items.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_button.pack()

        right_frm.pack(fill=tk.BOTH, side=tk.RIGHT)
        sep2.pack(expand=tk.YES, fill=tk.Y, padx=10, pady=10)
        self.name.pack(fill=tk.X)
        id_frm.pack(fill=tk.X)
        self.id.pack(side=tk.LEFT, fill=tk.X, padx=2)
        self.classification.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X,  padx=(2, 2))
        grid.pack(fill=tk.BOTH)
        chk_frm.pack()
        self.is_special.pack(side=tk.LEFT, fill=tk.X)
        self.targets_self.pack(side=tk.LEFT, fill=tk.X)

        description_label.pack()
        self.description.pack(expand=tk.YES, fill=tk.BOTH)

        self.classification.state(('readonly', ))

        for widget in self.id, self.attack, self.accuracy, self.priority, self.pp:
            intValidate(widget.entry, 'u16')
        for widget in self.type, self.effect, self.intensity, self.score, self.chance:
            intValidate(widget.entry, 'u8')


class MoveEditor:
    def __init__(self, parent=None):
        self.gui = MoveEditorGUI(parent)
        self.moves = array(Move)()
        self.main_saveable = self.moves
        self.sort_var = tk.StringVar(parent)
        self.sort_var.trace('w', lambda *args: self.gui.items.set_key(SORT_MAP[self.sort_var.get()]))
        self.sort_var.set('Move ID')
        self.gui.sort.combo.config(values=list(SORT_MAP.keys()), textvariable=self.sort_var)

        gui = self.gui
        self.item_connector = ArrayConnector(self.moves, self.gui.items, self.gui.add_button,
                                             gui.name, gui.id, gui.classification, gui.attack, gui.accuracy,
                                             gui.effect, gui.priority, gui.pp, gui.type, gui.chance, gui.intensity,
                                             gui.score, gui.attacker_anim, gui.defender_anim, gui.is_special,
                                             gui.targets_self, gui.description)
        self.gui.items.signal_select.connect(self.on_select)

    def on_select(self, id):
        move = self.item_connector.cur_selection
        gui = self.gui
        for widget, saveable in (
                (gui.id, move.id),
                (gui.attack, move.attack),
                (gui.accuracy, move.accuracy),
                (gui.effect, move.effect),
                (gui.priority, move.priority),
                (gui.pp, move.pp),
                (gui.type, move.type),
                (gui.chance, move.effect_chance),
                (gui.intensity, move.effect_intensity),
                (gui.score, move.effect_score)):
            widget.entry.config(textvariable=make_int_var(saveable))

        for widget, saveable in (
                (gui.name.entry, move.name),
                (gui.attacker_anim.entry, move.attacker_anim),
                (gui.defender_anim.entry, move.defender_anim),
                (gui.description, move.description)):
            widget.config(textvariable=make_str_var(saveable))

        for widget, saveable in (
                (gui.is_special, move.is_special),
                (gui.targets_self, move.effect_targets_self)):
            widget.config(variable=make_check_var(saveable))

        gui.classification.combo.config(textvariable=make_combo_var(move.classification, CLASSIFICATIONS))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)


if __name__ == '__main__':
    root = tk.Tk()
    editor = MoveEditorGUI(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()