import tkinter as tk
import tkinter.ttk as ttk


from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice import ListChoice

from Editor.guicomponents.integercheck import intValidate


class SimpleLine(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.label = EntryLabel(self, text=type(self).LABEL)
        self.label.pack(fill=tk.X)


class FailLine(SimpleLine):
    def __init__(self, parent=None):
        SimpleLine.__init__(self, parent)
        self.fail_line = EntryLabel(self, text='Fail Line:')
        self.fail_line.pack(fill=tk.X)


class TalkEdit(SimpleLine):
    LABEL = 'Display Line:'

    def __init__(self, parent=None):
        SimpleLine.__init__(self, parent)


class OptionEdit(SimpleLine):
    LABEL = 'Display Line:'

    def __init__(self, parent):
        SimpleLine.__init__(self, parent)
        option_lbl = ttk.Label(self, text='Options', style='Subtitl.TLabel')
        self.options = ListChoice(self)
        self.add_option = ttk.Button(self, text='Add')
        self.option_display = EntryLabel(self, text='Option Line')
        self.jump = EntryLabel(self, text='Jump Point')

        option_lbl.pack()
        self.options.pack(expand=tk.YES, fill=tk.BOTH)
        self.add_option.pack()
        self.option_display.pack(expand=tk.YES, fill=tk.X)
        self.jump.pack(expand=tk.YES, fill=tk.X)


class GiveItemEdit(SimpleLine):
    LABEL = 'Item Id:'

    def __init__(self, parent=None):
        SimpleLine.__init__(self, parent)
        intValidate(self.label.entry, 'u16')


class TakeItemEdit(FailLine):
    LABEL = 'Item Id:'

    def __init__(self, parent=None):
        FailLine.__init__(self, parent)
        intValidate(self.label.entry, 'u16')


class GiveMoneyEdit(SimpleLine):
    LABEL = 'Amount:'

    def __init__(self, parent=None):
        SimpleLine.__init__(self, parent)
        intValidate(self.label.entry, 'u16')


class TakeMoneyEdit(FailLine):
    LABEL = 'Amount:'

    def __init__(self, parent=None):
        FailLine.__init__(self, parent)
        intValidate(self.label.entry, 'u16')


class JumpEdit(SimpleLine):
    LABEL = 'Jump Name:'


class JumpPointEdit(SimpleLine):
    LABEL = 'Jump Name:'


class SaveEdit(SimpleLine):
    LABEL = 'String Value'


class CheckSavedEdit(FailLine):
    LABEL = 'String Value'


class CheckTalkedEdit(SimpleLine):
    LABEL = 'Fail Line:'


class RunScriptEdit(SimpleLine):
    LABEL = 'Script Name:'
