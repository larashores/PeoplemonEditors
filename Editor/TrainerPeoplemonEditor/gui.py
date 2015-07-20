__author__ = 'Vincent'

from tkinter import *
from Editor.guicomponents.entrylabel import EntryLabel
from Editor.fonts import TITLE_FONT,SUBTITLE_FONT

from Editor.Database.gui import EditorMenu

from Editor.PeoplemonDatabase.gui import PeoplemonEditor
from Editor.TrainerPeoplemonEditor.controller import Controller

from Editor.TrainerPeoplemonEditor.peoplemon import IVs

class Barrier(Frame):
    '''
    Fill should always be X when packing
    '''
    def __init__(self,parent):
        Frame.__init__(self,parent,height=2,bd=1,relief=SUNKEN)

class TrainerPeoplemonEditor(Frame):
    STATS = 'HP','Attack','Defense','Sp. Attack','Sp. Defense','Accuracy','Evade','Speed','Critical'
    def __init__(self,controller):
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
            self.moveVarList.append( (IntVar(),IntVar()) )


        Label(leftFrm,text='Trainer Peoplemon Editor', font=TITLE_FONT).pack()

        EntryLabel(leftFrm,text='Nickname', textvariable=self.nickVar).pack()

        frm = Frame(leftFrm)
        frm.pack()
        EntryLabel(frm,text='ID',textvariable=self.idVar).pack(side=LEFT)
        EntryLabel(frm,text='Level',textvariable=self.levelVar).pack(side=LEFT)

        EntryLabel(leftFrm,text='Hold Item ID',textvariable=self.holdVar).pack()

        Barrier(leftFrm).pack(expand=YES,fill=X,padx=(5,5),pady=(5,0))
        Label(leftFrm,text='Moves',font=SUBTITLE_FONT).pack()
        frm = Frame(leftFrm)
        frm.pack(expand=YES,fill=X)
        Label(frm,text='ID').pack(side=LEFT,expand=YES,fill=X)
        Label(frm,text='PP').pack(side=LEFT,expand=YES,fill=X)
        for idVar,PPVar in self.moveVarList:
            frm = Frame(leftFrm)
            frm.pack(pady=(0,6))
            Entry(frm,textvariable=idVar,justify=CENTER).pack(side=LEFT,padx=(3,3))
            Entry(frm,textvariable=PPVar,justify=CENTER).pack(side=LEFT,padx=(3,3))

        PeoplemonEditor.makeStats(self,middleFrm,'IVs',self.IVVars)
        PeoplemonEditor.makeStats(self,rightFrm,'EVs',self.EVVars)
    def apply(self):
        self.controller.update({'nickname':   self.nickVar.get(),
                                'id':         self.idVar.get(),
                                'level':      self.levelVar.get(),
                                'holdItemID': self.holdVar.get()})
        ind = 0
        for IDVar,PPVar in self.moveVarList:
            self.controller.updateMove(ind,IDVar.get(),PPVar.get())
            ind += 1
        for var,name in zip(self.IVVars,IVs.stats):
            self.controller.updateIV(var.get(),name)
        for var,name in zip(self.EVVars,IVs.stats):
            self.controller.updateEV(var.get(),name)

    def load(self):
        print('loading')
        nicknames, id, level, hold, = self.controller.load( ('nickname','id','level','holdItemID') )
        self.nickVar.set(nicknames)
        self.idVar.set(id)
        self.levelVar.set(level)
        self.holdVar.set(hold)
        for ind in range(4):
            id,pp =self.controller.loadMove(ind)
            self.moveVarList[ind][0].set(id)
            self.moveVarList[ind][1].set(pp)

        for ind,val in enumerate(self.controller.loadEV()):
            self.EVVars[ind].set(val)

        for ind,val in enumerate(self.controller.loadIV()):
            self.IVVars[ind].set(val)


if __name__ == '__main__':
    root = Tk()
    root.title("I Liek Turtlez")
    controller = Controller()

    menu = EditorMenu(controller)
    root.config(menu=menu)
    editor = TrainerPeoplemonEditor(controller)
    editor.pack()

    root.mainloop()