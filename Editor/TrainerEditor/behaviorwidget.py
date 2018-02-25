import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.integercheck import intValidate
from Editor.TrainerEditor.constants import *
from Editor.TrainerEditor.saveables import *
from Editor.utilities.make_var import make_str_var, make_int_var, make_combo_var, make_check_var
from Editor.utilities.arrayconnector import ArrayConnector


class BehaviorWidgetConnector:
    def __init__(self, behavior_widget, behavior_obj):
        self.gui = behavior_widget
        self.behavior = behavior_obj
        self.node_connector = None
        self.signal_repack = Signal()
        self.behavior.signal_changed.connect(self.behavior_changed)

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
        if Type not in widget_map:
            return
        self.gui.change_widget(widget_map[Type])
        current = self.gui.current_motion_widget
        if Type == StandStillBehavior:
            self.signal_repack(False)
        elif Type == WanderBehavior:
            current.radius.entry.config(textvariable=make_int_var(self.behavior.wander.radius))
            self.signal_repack(False)
        elif Type == SpinInPlaceBehavior:
            dir_map = {D_CLOCK: 0, D_COUNTER: 1, D_RANDOM: 2}
            current.combo.config(textvariable=make_combo_var(self.behavior.spin.motion, dir_map))
            self.signal_repack(False)
        elif Type == FollowPathBehavior:
            for node in self.behavior.follow.nodes:
                current.node_list.clear()
                current.node_list.append(str(node), node)
            current.pack(padx=10, fill=tk.BOTH)
            current.check.config(
                variable=make_check_var(self.behavior.follow.reverse_loop))
            self.node_connector = ArrayConnector(self.behavior.follow.nodes,
                                                 current.node_list,
                                                 current.add_button,
                                                 current.direction,
                                                 current.steps)
            self.node_connector.bind_move()
            current.node_list.signal_select.connect(self.select_node)
            self.signal_repack(True)


class BehaviorWidget(ttk.Frame):
    def __init__(self, parent=None, *, expand_follow=tk.NO):
        ttk.Frame.__init__(self, parent)
        self.current_motion_widget = Still(self)
        self.current_motion_widget.pack()
        self.expand = expand_follow

    def change_widget(self, WidgetType):
        if self.current_motion_widget:
            self.current_motion_widget.destroy()
        self.current_motion_widget = WidgetType(self)
        if isinstance(self.current_motion_widget, FollowPath):
            self.current_motion_widget.pack(padx=10, expand=self.expand, fill=tk.BOTH)
        elif isinstance(self.current_motion_widget, Still):
            self.current_motion_widget.pack()
        else:
            self.current_motion_widget.pack(padx=10)


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
