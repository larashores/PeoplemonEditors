import tkinter as tk
from tkinter import ttk

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.combolabel import ComboLabel
from Editor.guicomponents.widgetgrid import WidgetGrid
from Editor.TrainerEditor.constants import *
from Editor.TrainerEditor.behaviorwidget import BehaviorWidgetConnector, BehaviorWidget
from Editor.TrainerEditor.saveables import StandStillBehavior, SpinInPlaceBehavior, WanderBehavior, FollowPathBehavior
from Editor.NPCEditor.saveables import Npc
from Editor.utilities.make_var import make_int_var, make_str_var, make_combo_var


class NpcEditorGUI(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        title = ttk.Label(self, text='NPC Editor',  style='Title.TLabel')
        grid = WidgetGrid(self, 2)
        self.npc_name = grid.add_widget(EntryLabel, text='NPC Name')
        self.anim_name = grid.add_widget(EntryLabel, text='Animation Name', padx=(2, 2))
        self.conv_name = grid.add_widget(EntryLabel, text='Conversation Name')
        self.motion_type = grid.add_widget(ComboLabel, text='Motion Type',
                                           values=[B_STILL, B_SPIN, B_FOLLOW, B_WANDER])
        sep = ttk.Separator(self, orient=tk.HORIZONTAL)
        lbl = ttk.Label(self, text='Motion Type', style='Subtitle.TLabel')
        self.behavior = BehaviorWidget(self, expand_follow=tk.YES)

        title.pack()
        grid.pack(expand=tk.YES, fill=tk.X)
        sep.pack(expand=tk.YES, fill=tk.X, padx=10, pady=(10, 0))
        lbl.pack()
        self.behavior.pack(expand=tk.YES, fill=tk.BOTH)

        self.motion_type.state(['readonly'])


class NpcEditor:
    def __init__(self, parent=None):
        self.gui = NpcEditorGUI(parent)
        self.npc = Npc()
        self.main_saveable = self.npc

        for widget, saveable in ((self.gui.npc_name, self.npc.name),
                                 (self.gui.anim_name, self.npc.animation),
                                 (self.gui.conv_name, self.npc.convo_file)):
            widget.entry.config(textvariable=make_str_var(saveable))

        behavior_map = {B_STILL: StandStillBehavior, B_SPIN: SpinInPlaceBehavior,
                        B_FOLLOW: FollowPathBehavior, B_WANDER: WanderBehavior}
        self.behavior_connector = BehaviorWidgetConnector(self.gui.behavior, self.npc.behahavior)
        self.gui.motion_type.combo.config(textvariable=make_combo_var(self.npc.behahavior, behavior_map))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)
