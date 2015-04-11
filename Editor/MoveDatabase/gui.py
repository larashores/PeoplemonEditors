__author__ = 'Vincent'

from Editor.Database.database import Database
from Editor.Database.gui import EditorMenu, Editor

from MoveDatabase.Move import Move
from MoveDatabase.controller import MoveController

from Editor.ItemDatabase.gui import ItemEditor
from Editor.guicomponents.entrylabel import EntryLabel

from tkinter import *

class MoveEditor(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.controller.applyfuncs.append(self.apply)
        self.controller.loadfuncs.append(self.load)
        chkFrm = Frame(self)
        topFrm = Frame(self)
        scdFrm = Frame(self)
        btmFrm = Frame(self)
        lstFrm = Frame(self)
        chkFrm.pack()
        topFrm.pack()
        scdFrm.pack()
        btmFrm.pack()
        lstFrm.pack()

        self.attackVar   = IntVar()
        self.accuracyVar = IntVar()
        self.priorityVar = IntVar()
        self.ppVar       = IntVar()
        self.typeVar     = IntVar()
        self.effectVar   = IntVar()
        self.chanceOfEffectVar  = IntVar()
        self.effectIntensityVar = IntVar()
        self.attackAnimVar      = StringVar()
        self.defenderAnimVar    = StringVar()

        self.targetsSelfVar     = IntVar()
        self.isSpecialVar       = IntVar()


        Checkbutton(chkFrm,text='Is Special',var=self.isSpecialVar).pack(side=LEFT)
        Checkbutton(chkFrm,text='Targets Self',var=self.targetsSelfVar).pack(side=LEFT)

        EntryLabel(topFrm,text='Attack',textvariable=self.attackVar).pack(side=LEFT)
        EntryLabel(topFrm,text='Accuracy',textvariable=self.accuracyVar).pack(side=LEFT)
        EntryLabel(topFrm,text='Effect',textvariable=self.effectVar).pack(side=LEFT)

        EntryLabel(scdFrm,text='Priority',textvariable=self.priorityVar).pack(side=LEFT)
        EntryLabel(scdFrm,text='PP',textvariable=self.ppVar).pack(side=LEFT)

        EntryLabel(btmFrm,text='Chance of Effect',textvariable=self.chanceOfEffectVar).pack(side=LEFT)
        EntryLabel(btmFrm,text='Effect Intensity',textvariable=self.effectIntensityVar).pack(side=LEFT)
        EntryLabel(lstFrm,text='Attacker Animation',textvariable=self.attackAnimVar).pack(side=LEFT)
        EntryLabel(lstFrm,text='Defender Animation',textvariable=self.defenderAnimVar).pack(side=LEFT)
    def apply(self):
        self.controller.update({'isSpecial':bool(self.isSpecialVar.get()),
                                     'atk': self.attackVar.get(),
                                     'acc': self.accuracyVar.get(),
                                     'priority': self.priorityVar.get(),
                                     'pp': self.ppVar.get(),
                                     'type': self.typeVar.get(),
                                     'effect': self.effectVar.get(),
                                     'chanceOfEffect': self.chanceOfEffectVar.get(),
                                     'effectIntensity': self.effectIntensityVar.get(),
                                     'effectTargetsSelf': bool(self.targetsSelfVar.get()),
                                     'attackerAnim': self.attackAnimVar.get(),
                                     'defenderAnim': self.defenderAnimVar.get()})
    def load(self,ind):
        if ind == -1:
            return
        params = self.controller.loadAttribs(ind,['isSpecial','atk','acc','priority','pp','type','effect','chanceOfEffect',
                                    'effectIntensity','effectTargetsSelf','attackerAnim','defenderAnim'])
        for var, param in zip( (self.isSpecialVar,self.attackVar,self.accuracyVar,
                                self.priorityVar,self.ppVar,self.typeVar,self.effectVar,
                                self.chanceOfEffectVar,self.effectIntensityVar,self.targetsSelfVar,
                                self.attackAnimVar,self.defenderAnimVar),params):
            if var == self.targetsSelfVar or var == self.isSpecialVar:
                var.set(int(param))
            else:
                var.set(param)


if __name__ == '__main__':
    root = Tk()
    root.title("Sex is real and it affects the future")
    control = MoveController(Database(Move))
    move = MoveEditor(root,control)
    move.pack(side=RIGHT)
    menu = EditorMenu(control)
    root.config(menu=menu)
    edit = Editor(root,control)
    edit.pack(expand=YES,fill=BOTH)
    item = ItemEditor(edit,control)
    item.pack()

    mainloop()