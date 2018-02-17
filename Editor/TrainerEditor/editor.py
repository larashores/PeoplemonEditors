import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice_2 import ListChoice
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.utilities.make_var import make_str_var, make_int_var, make_combo_var, make_check_var
from Editor.utilities.arrayconnector import ArrayConnector

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
        self.current_motion_widget = Still(self.right_frm)

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

        self.right_frm.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT)
        sep2.pack(fill=tk.Y, padx=(10, 0), side=tk.LEFT)
        motion_lbl.pack(padx=10)
        self.current_motion_widget.pack()

        self.ai_type.state(['readonly'])
        self.motion_type.state(['readonly'])
        intValidate(self.sight_range.entry, 'u8')
        intValidate(self.item_id.entry, 'u16')

    def change_widget(self, WidgetType):
        if self.current_motion_widget:
            self.current_motion_widget.destroy()
        self.current_motion_widget = WidgetType(self.right_frm)


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

        for widget, saveable in str_entry_map.items():
            widget.entry.config(textvariable=make_str_var(saveable))
        self.gui.sight_range.entry.config(textvariable=make_int_var(self.trainer.sight_range))
        self.node_connector = None
        self.peoplemon_connector = ArrayConnector(self.trainer.peoplemon,
                                                  self.gui.peoplemon_list, self.gui.add_peoplemon, self.gui.file_name)
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
        self.trainer.behavior.signal_changed.connect(self.behavior_changed)

        self.last_behavior = None

    def select_peoplemon(self, ind):
        if ind is not None:
            current = self.peoplemon_connector.cur_selection
            self.gui.file_name.entry.config(textvariable=make_str_var(current))

    def select_item(self, ind):
        if ind is not None:
            current = self.item_connector.cur_selection
            self.gui.item_id.entry.config(textvariable=make_int_var(current))

    def select_node(self, ind):
        if ind is not None:
            node_widget = self.gui.current_motion_widget
            current = self.node_connector.cur_selection
            combo_map = {D_UP: 0, D_RIGHT: 1, D_DOWN: 2, D_LEFT: 3}
            node_widget.steps.entry.config(textvariable=make_int_var(current.num_steps))
            node_widget.direction.config(textvariable=make_combo_var(current.direction, combo_map))

    def behavior_changed(self, Type):
        widget_map = {StandStillBehavior: Still, SpinInPlaceBehavior: SpinInPlace,
                      FollowPathBehavior: FollowPath, WanderBehavior: WanderFreely}
        self.gui.change_widget(widget_map[Type])
        if Type == StandStillBehavior:
            self.gui.current_motion_widget.pack()
        elif Type == WanderBehavior:
            self.gui.current_motion_widget.pack(padx=10, fill=tk.X)
            self.gui.current_motion_widget.radius.entry.config(
                textvariable=make_int_var(self.trainer.behavior.wander.radius))
        elif Type == SpinInPlaceBehavior:
            self.gui.current_motion_widget.pack(padx=10, fill=tk.X)
            dir_map = {D_CLOCK: 0, D_COUNTER: 1, D_RANDOM: 2}
            self.gui.current_motion_widget.combo.config(
                textvariable=make_combo_var(self.trainer.behavior.spin.motion, dir_map))
        elif Type == FollowPathBehavior:
            for node in self.trainer.behavior.follow.nodes:
                self.gui.current_motion_widget.node_list.clear()
                self.gui.current_motion_widget.node_list.append(str(node), node)
            self.gui.current_motion_widget.pack(padx=10, fill=tk.BOTH)
            self.gui.current_motion_widget.check.config(
                variable=make_check_var(self.trainer.behavior.follow.reverse_loop))
            self.node_connector = ArrayConnector(self.trainer.behavior.follow.nodes,
                                                 self.gui.current_motion_widget.node_list,
                                                 self.gui.current_motion_widget.add_button,
                                                 self.gui.current_motion_widget.direction,
                                                 self.gui.current_motion_widget.steps)
            self.gui.current_motion_widget.node_list.signal_select.connect(self.select_node)

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)


class Still(ttk.Label):
    def __init__(self, parent=None):
        ttk.Label.__init__(self, parent, text='No Options')


class SpinInPlace(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        ttk.Label(self, text='Direction').pack()
        self.combo = ttk.Combobox(self, justify=tk.CENTER, values=[D_CLOCK, D_COUNTER,  D_RANDOM])
        self.combo.state(['readonly'])
        self.combo.pack(expand=tk.YES, fill=tk.X)


class WanderFreely(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.radius = EntryLabel(self, text='Wander Radius')
        self.radius.pack(expand=tk.YES, fill=tk.X)
        intValidate(self.radius.entry, 'u8')


class FollowPath(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.nodes = []
        self.check = ttk.Checkbutton(self, text='Reverse loop')
        self.node_list = ListChoice(self)
        lbl = ttk.Label(self, text='Direction')
        self.direction = ttk.Combobox(self, justify=tk.CENTER, value=(D_UP, D_LEFT, D_RIGHT, D_DOWN))
        self.steps = EntryLabel(self, text='Number of Steps')
        self.add_button = ttk.Button(self, text='Add')

        self.check.pack()
        self.node_list.pack(expand=tk.YES, fill=tk.BOTH)
        lbl.pack()
        self.direction.pack(fill=tk.X)
        self.steps.pack(fill=tk.X)
        self.add_button.pack(pady=5)

        self.direction.state(['readonly'])
        intValidate(self.steps.entry, 'u8')


if __name__ == '__main__':
    root = tk.Tk()
    editor = TrainerEditor(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=(5, 10))
    root.mainloop()

