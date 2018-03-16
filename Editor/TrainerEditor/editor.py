import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.entrylabel import EntryLabel
from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.utilities.make_var import make_str_var, make_int_var, make_combo_var, make_check_var
from Editor.utilities.arrayconnector import ArrayConnector

from Editor.TrainerEditor.behaviorwidget import BehaviorWidget, BehaviorWidgetConnector
from Editor.TrainerEditor.constants import *
from Editor.TrainerEditor.saveables import *


class TrainerEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.aiTypes = {AI_RANDOM: 0, AI_DUMB: 1, AI_SMART: 2, AI_SUICIDAL: 3, AI_AGGRESSIVE: 4, AI_DEFENSIVE: 5,
                        AI_AVERAGE: 6, AI_ADAPTIVE: 7}

        title = ttk.Label(self, text='Trainer Editor',  style='Title.TLabel')
        left_frm = ttk.Frame(self)
        grid = WidgetGrid(left_frm, 2)
        self.name = grid.add_widget(EntryLabel, text='Trainer Name')
        self.anim_name = grid.add_widget(EntryLabel, text='Animation Name')
        self.before_convo = grid.add_widget(EntryLabel, text='Before Battle Convo')
        self.after_convo = grid.add_widget(EntryLabel, text='After Battle Convo')
        self.lost_text = grid.add_widget(EntryLabel, text='Lost Battle Text')
        self.sight_range = grid.add_widget(EntryLabel, text='Sight Range')
        self.playlist = grid.add_widget(EntryLabel, text='Playlist')
        self.background = grid.add_widget(EntryLabel, text='Background Image')
        grid.add_widget(ttk.Label, text='AI Type', width=12, anchor=tk.CENTER)
        grid.add_widget(ttk.Label, text='Motion Type', width=12, anchor=tk.CENTER)
        self.ai_type = grid.add_widget(ttk.Combobox, values=(AI_RANDOM, AI_DUMB, AI_SMART, AI_SUICIDAL,
                                       AI_AGGRESSIVE, AI_DEFENSIVE, AI_AVERAGE, AI_ADAPTIVE), justify=tk.CENTER)
        self.motion_type = grid.add_widget(ttk.Combobox, values=(B_STILL, B_SPIN, B_FOLLOW, B_WANDER),
                                           justify=tk.CENTER)
        sep = ttk.Separator(left_frm)

        second_row = ttk.Frame(left_frm)
        col1 = ttk.Frame(second_row)
        peoplemon_lbl = ttk.Label(col1, text='Peoplemon List')
        self.peoplemon_list = ListChoice(col1)
        self.file_name = EntryLabel(col1, text='Filename')
        self.add_peoplemon = ttk.Button(col1, text='Add')

        col2 = ttk.Frame(second_row)
        item_lbl = ttk.Label(col2, text='Item List')
        self.item_list = ListChoice(col2)
        self.item_id = EntryLabel(col2, text='Item ID')
        self.add_item = ttk.Button(col2, text='Add')

        self.right_frm = ttk.Frame(self)
        sep2 = ttk.Separator(self.right_frm, orient=tk.VERTICAL)
        motion_lbl = ttk.Label(self.right_frm, text='Motion Options', style='Subtitle.TLabel')
        self.behavior_widget = BehaviorWidget(self.right_frm)

        title.pack()
        left_frm.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)
        grid.pack(expand=tk.YES, fill=tk.X)
        sep.pack(expand=tk.YES, fill=tk.X, padx=10, pady=5)

        second_row.pack(expand=tk.YES, fill=tk.BOTH, padx=20)
        col1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, padx=(0, 20))
        col2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, padx=(20, 0))

        peoplemon_lbl.pack()
        self.peoplemon_list.pack(expand=tk.YES, fill=tk.BOTH)
        self.file_name.pack(expand=tk.YES, fill=tk.X)
        self.add_peoplemon.pack(pady=(10, 0))

        item_lbl.pack()
        self.item_list.pack(expand=tk.YES, fill=tk.BOTH)
        self.item_id.pack(expand=tk.YES, fill=tk.X)
        self.add_item.pack(pady=(10, 0))

        self.right_frm.pack(fill=tk.BOTH, side=tk.LEFT)
        sep2.pack(fill=tk.Y, padx=(10, 0), side=tk.LEFT)
        motion_lbl.pack(padx=10)
        self.behavior_widget.pack(expand=tk.YES, fill=tk.BOTH)

        self.ai_type.state(['readonly'])
        self.motion_type.state(['readonly'])
        intValidate(self.sight_range.entry, 'u8')
        intValidate(self.item_id.entry, 'u16')


class TrainerEditor:
    def __init__(self, parent=None):
        self.gui = TrainerEditorGUI(parent)
        self.trainer = Trainer()
        self.main_saveable = self.trainer
        str_entry_map = {self.gui.name: self.trainer.name,
                         self.gui.anim_name: self.trainer.animation,
                         self.gui.before_convo: self.trainer.before_convo,
                         self.gui.after_convo: self.trainer.after_convo,
                         self.gui.lost_text: self.trainer.lose_message,
                         self.gui.playlist: self.trainer.playlist,
                         self.gui.background: self.trainer.background_image}

        self.gui.item_list.set_key(lambda item: item.get())
        for widget, saveable in str_entry_map.items():
            widget.entry.config(textvariable=make_str_var(saveable))
        self.gui.sight_range.entry.config(textvariable=make_int_var(self.trainer.sight_range))
        self.node_connector = None
        self.peoplemon_connector = ArrayConnector(self.trainer.peoplemon,
                                                  self.gui.peoplemon_list, self.gui.add_peoplemon, self.gui.file_name)
        self.peoplemon_connector.bind_move()
        self.item_connector = ArrayConnector(self.trainer.items,
                                             self.gui.item_list, self.gui.add_item, self.gui.item_id)
        self.gui.peoplemon_list.signal_select.connect(self.select_peoplemon)
        self.gui.item_list.signal_select.connect(self.select_item)

        ai_map = {AI_RANDOM: 0, AI_DUMB: 1, AI_SMART: 2, AI_SUICIDAL: 3, AI_AGGRESSIVE: 4, AI_DEFENSIVE: 5,
                  AI_AVERAGE: 6, AI_ADAPTIVE: 7}
        behavior_map = {B_STILL: StandStillBehavior, B_SPIN: SpinInPlaceBehavior,
                        B_FOLLOW: FollowPathBehavior, B_WANDER: WanderBehavior}
        self.gui.ai_type.config(textvariable=make_combo_var(self.trainer.ai_type, ai_map))
        self.gui.motion_type.config(textvariable=make_combo_var(self.trainer.behavior, behavior_map))
        self.behavior_connect = BehaviorWidgetConnector(self.gui.behavior_widget, self.trainer.behavior)
        self.behavior_connect.signal_repack.connect(self.on_repack)

    def on_repack(self, expand):
        self.gui.right_frm.pack_forget()
        self.gui.right_frm.pack(side=tk.LEFT, expand=expand, fill=tk.BOTH)

    def select_peoplemon(self, ind):
        if ind is not None:
            current = self.peoplemon_connector.cur_selection
            self.gui.file_name.entry.config(textvariable=make_str_var(current))

    def select_item(self, ind):
        if ind is not None:
            current = self.item_connector.cur_selection
            self.gui.item_id.entry.config(textvariable=make_int_var(current))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)


if __name__ == '__main__':
    root = tk.Tk()
    editor = TrainerEditor(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=(5, 10))
    root.mainloop()

