import tkinter as tk
import tkinter as ttk

from Editor.ConversationEditor.components.lines import *

from Editor.guicomponents.buttongrid import ButtonGrid

from Editor.ConversationEditor.gui.editFrames import *


class ConversationEditor(ttk.Frame):
    BUTTONS = (('Talk', TalkEdit, TalkLine),
               ('Option', OptionEdit, OptionLine),
               ('Give Item', GiveItemEdit, GiveItemLine),
               ('Take Item', TakeItemEdit, TakeItemLine),
               ('Jump To', JumpEdit, Jump),
               ('Jump Point', JumpPointEdit, JumpPoint),
               ('Give Money', GiveMoneyEdit, GiveMoneyLine),
               ('Take Money', TakeMoneyEdit, TakeMoneyLine),
               ('Save String', SaveEdit, Save),
               ('Check String', CheckSaveEdit, CheckSave),
               ('Check Talked', CheckTalkedEdit, CheckTalked),
               ('Run Script', RunScriptEdit, ScriptLine))

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.load_func = self.load

        self.check_var = tk.IntVar()
        self.button_grid = ButtonGrid(self, 4)
        for label, editor, line in self.BUTTONS:
            command = lambda x=line: self.addToList(x)
            self.button_grid.addButton(label, command)

        self.lines = ListChoice(self, update_cmd=self.lineClick,
                                delete_cmd=self.deleteLine,
                                width=50, height=8)
        self.line_frame = None

        ttk.Label(self, text='Conversation Editor', style='Title.TLabel').pack(pady=(0, 10))
        ttk.Label(self, text='Add', style='Subtitle.TLabel').pack()
        ttk.Checkbutton(self, text='Add Before (Otherwise at end)', variable=self.check_var).pack()
        self.button_grid.pack()

        ttk.Label(self, text='Lines', style='Subtitle.TLabel').pack()
        self.lines.pack(expand=tk.YES, fill=tk.BOTH, padx=(10, 10))

    def addToList(self, Line):
        if not self.check_var.get():
            self.controller.addLine('end', Line())
            ind = -1
            top = None
        else:
            ind = self.lines.getSelection()
            self.controller.addLine(ind, Line())
            top = self.lines.get_top()
        self.load()
        self.lines.setSelection(ind)

        if self.check_var.get():
            self.lines.set_top(top)
        else:
            self.lines.setPosition(1.0)

    def load(self):
        top = self.lines.get_top()
        self.lines.clear()
        for line in self.controller:
            self.lines.addChoice(line)
        self.lines.set_top(top)

    def lineClick(self, index):
        if self.line_frame:
            self.line_frame.destroy()

        if index is not None:
            line = self.controller.get_line(index)
            print(index)
            editor_map = dict(zip(map(lambda grp: grp[2], self.BUTTONS), map(lambda grp: grp[1], self.BUTTONS)))
            self.line_frame = editor_map[line.__class__](self, self.controller, line)

            self.line_frame.pack(side=tk.TOP, expand=tk.YES, fill=tk.X)

    def deleteLine(self, index):
        self.controller.deleteLine(int(index))
        self.load()
        if index == self.controller.get_length():
            index -= 1
        if index < 0:   # Choices now empty
            return
        self.lines.setSelection(index)
