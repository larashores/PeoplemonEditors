__author__ = 'Vincent'

from tkinter import *
from tkinter import ttk
from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.integercheck import IntegerCheck
from Editor.fonts import TITLE_FONT

from Editor.Database.gui import EditorMenu

from Editor.PeoplemonDatabase.gui import PeoplemonEditor
from Editor.TrainerPeoplemonEditor.controller import Controller

from Editor.TrainerPeoplemonEditor.peoplemon import IVs


SUBTITLE_FONT = ('tkdefaultfont', 12, 'bold')


class TrainerPeoplemonEditor(Frame):
    STATS = 'HP', 'Attack', 'Defense', 'Sp. Attack', 'Sp. Defense', 'Accuracy', 'Evade', 'Speed', 'Critical'

    def __init__(self, controller):
        self.controller = controller
        self.controller.loadFunc = self.load
        self.controller.applyFunc = self.apply
        Frame.__init__(self)

        leftFrm = Frame(self)
        middleFrm = Frame(self)
        rightFrm = Frame(self)

        leftFrm.pack(side=LEFT)
        middleFrm.pack(side=LEFT)
        rightFrm.pack(side=LEFT)

        self.nickVar = StringVar()
        self.idVar = IntVar()
        self.levelVar = IntVar()
        self.holdVar = IntVar()

        self.IVVars = []
        self.EVVars = []

        self.moveVarList = []
        for _ in range(4):
            self.moveVarList.append((IntVar(), IntVar()))

        ttk.Label(leftFrm, text='Trainer Peoplemon Editor', style='Title.TLabel').pack(padx=10)

        EntryLabel(leftFrm, text='Nickname', entry_variable=self.nickVar).pack()

        frm = ttk.Frame(leftFrm)
        frm.pack()
        EntryLabel(frm, text='ID', entry_variable=self.idVar, validate='all',
                   validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=LEFT)
        EntryLabel(frm, text='Level', entry_variable=self.levelVar, validate='key',
                   validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=LEFT)

        EntryLabel(leftFrm, text='Hold Item ID', entry_variable=self.holdVar, validate='key',
                   validatecommand=IntegerCheck(self, 'u16').vcmd).pack()

        ttk.Separator(leftFrm).pack(expand=YES, fill=X, padx=(5, 5), pady=(12, 0))
        ttk.Label(leftFrm, text='Moves', style='Subtitle.TLabel').pack()
        frm = ttk.Frame(leftFrm)
        frm.pack(expand=YES,fill=X)
        Label(frm, text='ID').pack(side=LEFT, expand=YES, fill=X)
        Label(frm, text='PP').pack(side=LEFT, expand=YES, fill=X)
        for idVar, PPVar in self.moveVarList:
            frm = Frame(leftFrm)
            frm.pack(pady=(0,6))
            ttk.Entry(frm, textvariable=idVar, justify=CENTER, validate='key',
                      validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=LEFT, padx=(3,3))
            ttk.Entry(frm, textvariable=PPVar, justify=CENTER, validate='key',
                      validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=LEFT, padx=(3,3))

        PeoplemonEditor.makeStats(self, middleFrm, 'IVs', self.IVVars)
        PeoplemonEditor.makeStats(self, rightFrm, 'EVs', self.EVVars)

    def apply(self):
        self.controller.update({'nickname':   self.nickVar.get(),
                                'id':         self.idVar.get(),
                                'level':      self.levelVar.get(),
                                'holdItemID': self.holdVar.get()})
        ind = 0
        for IDVar, PPVar in self.moveVarList:
            self.controller.updateMove(ind, IDVar.get(), PPVar.get())
            ind += 1
        for var, name in zip(self.IVVars, IVs.stats):
            self.controller.updateIV(var.get(), name)
        for var, name in zip(self.EVVars, IVs.stats):
            self.controller.updateEV(var.get(), name)

    def load(self):
        nicknames, id, level, hold, = self.controller.load(('nickname', 'id', 'level', 'holdItemID'))
        self.nickVar.set(nicknames)
        self.idVar.set(id)
        self.levelVar.set(level)
        self.holdVar.set(hold)
        for ind in range(4):
            id, pp = self.controller.loadMove(ind)
            self.moveVarList[ind][0].set(id)
            self.moveVarList[ind][1].set(pp)

        for ind, val in enumerate(self.controller.loadEV()):
            self.EVVars[ind].set(val)

        for ind, val in enumerate(self.controller.loadIV()):
            self.IVVars[ind].set(val)


if __name__ == '__main__':
    root = Tk()
    root.title("Trainer Peoplemon Editor")
    root.iconbitmap('icons/editor.ico')
    style = ttk.Style()
    style.configure('Title.TLabel', font=TITLE_FONT)
    style.configure('Subtitle.TLabel', font=SUBTITLE_FONT)

    controller = Controller()

    menu = EditorMenu(controller)
    root.config(menu=menu)
    editor = TrainerPeoplemonEditor(controller)
    editor.pack()

    root.mainloop()
