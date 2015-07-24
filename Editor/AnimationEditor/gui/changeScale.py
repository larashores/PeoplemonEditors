__author__ = 'Vincent'

from tkinter import *
from tkinter import ttk
from Editor.AnimationEditor.gui import entrylabel

def askChange(previous):
    answer = []
    window = ScaleChange(answer, previous)
    window.mainloop()
    if answer:
        return int(answer[0])

class ScaleChange(Toplevel):
    def __init__(self, answer_lst, previous):
        Toplevel.__init__(self)
        self.title('Change Scale')
        self.answer_lst = answer_lst
        frame = ttk.Frame(self)
        frame.pack(padx=(5, 5), pady=(0, 5))
        self.entry = entrylabel.EntryLabel(frame, text='New Scale')
        self.entry.insert(0, str(previous))
        self.entry.pack()
        but_frame = ttk.Frame(frame)
        but_frame.pack(pady=(5, 0))
        ttk.Button(but_frame, text='Ok', style='Action.TButton', command=self.ok).pack(side=LEFT, padx=(0, 2))
        ttk.Button(but_frame, text='Cancel', style='Action.TButton', command=self.cancel).pack(side=LEFT, padx=(2, 0))
        self.grab_set()

    def ok(self):
        self.answer_lst.append(self.entry.get())
        self.destroy()
        self.quit()

    def cancel(self):
        self.destroy()
        self.quit()