__author__ = 'Vincent'

from Editor.PeoplemonDatabase.controller import PeoplemonController
from Editor.PeoplemonDatabase.Peoplemon import Peoplemon

from Editor.ItemDatabase.gui import ItemEditor
from Editor.Database.database import Database
from Editor.Database.gui import EditorMenu,Editor

from Editor.guicomponents.entrylabel import EntryLabel
from Editor.PeoplemonDatabase.Peoplemon import BaseStats

from tkinter import *

import time

TITLE_NAME = 'Item Database Editor'
TITLE_FONT = ('tkdefaultfont',16,'bold')


class PeoplemonEditor(Frame):
    STATS = 'HP','Attack','Defense','Accuracy','Evade','Speed','Critical','Sp. Attack','Sp. Defense'

    def __init__(self,parent,controller):
        Frame.__init__(self)
        self.controller = controller
        self.controller.loadfuncs.append(self.load)
        self.controller.applyfuncs.append(self.apply)
        self.baseStatVars = []
        self.evAwardVars = []

        topfrm = Frame(self,bd=3,relief=GROOVE)
        topfrm.pack()
        self.typeVar = IntVar()
        EntryLabel(topfrm,text="Type",textvariable=self.typeVar).pack(side=LEFT,padx=(6,3),pady=(0,8))
        self.specialIDVar = IntVar()
        EntryLabel(topfrm,text="Special Ability ID",textvariable=self.specialIDVar).pack(side=LEFT,padx=(3,3),pady=(0,8))
        self.evolveLevelVar = IntVar()
        EntryLabel(topfrm,text="Evolve Level",textvariable=self.evolveLevelVar).pack(side=LEFT,padx=(3,3),pady=(0,8))
        self.evolveIDVar = IntVar()
        EntryLabel(topfrm,text="Evolve ID",textvariable=self.evolveIDVar).pack(side=LEFT,padx=(3,6),pady=(0,8))

        basefrm = Frame(self)
        awardfrm = Frame(self)
        basefrm.pack(side=LEFT)
        awardfrm.pack(side=LEFT)
        self.makeStats(basefrm,'Base Stats',self.baseStatVars)
        self.makeStats(awardfrm,'EV Awards',self.evAwardVars)
    def makeStats(self,frame,text,varList):
        frm = Frame(frame,bd=3,relief=GROOVE)
        frm.pack()
        Label(frm,text=text,font=[TITLE_FONT[0]]+[14]+[TITLE_FONT[2]]).pack()
        upfrm = Frame(frm)
        upfrm.pack()
        leftfrm = Frame(upfrm)
        rightfrm = Frame(upfrm)
        leftfrm.pack(side=LEFT,padx=(4,2))
        rightfrm.pack(side=RIGHT,padx=(2,4))
        for ind,stat in enumerate(PeoplemonEditor.STATS):
            var = IntVar(self)
            varList.append(var)
            if ind <=3:
                label = EntryLabel(leftfrm,text=stat,textvariable = var)
                label.pack()
            elif ind<8:
                label = EntryLabel(rightfrm,text=stat,textvariable = var)
                label.pack()
            else:
                label = EntryLabel(frm,text=stat,textvariable = var)
                label.pack(side=BOTTOM,pady=(0,5))
    def load(self,ind):
        vals = self.controller.loadPeoplemon(ind,['type','specialAbilityId','evolveLevel','evolveID'])
        for val,var in zip(vals,(self.typeVar,self.specialIDVar,self.evolveLevelVar,self.evolveIDVar)):
            var.set(val)
        self.loadStat(self.baseStatVars,self.controller.loadPeoplemon(ind,BaseStats.stats,['baseStats']))
        self.loadStat(self.evAwardVars,self.controller.loadPeoplemon(ind,BaseStats.stats,['evAwards']))
    def loadStat(self,statVars,stats):
        for stat,var in zip(stats,statVars):
            var.set(stat)
    def apply(self):
        self.controller.update(   {'type': self.typeVar.get(),
                                             'specialAbilityId': self.specialIDVar.get(),
                                             'evolveLevel': self.evolveLevelVar.get(),
                                             'evolveID': self.evolveIDVar.get() })
        stats = {}

        for ind,var in enumerate(self.baseStatVars):
            stats[BaseStats.stats[ind]] = var.get()
        self.controller.update(stats,['baseStats'])

        stats = {}
        for ind,var in enumerate(self.evAwardVars):
            stats[BaseStats.stats[ind]] = var.get()
        self.controller.update(stats,['evAwards'])




if __name__ == '__main__':

    '''class Outer(Frame):
        def __init__(self,parent):
            Frame.__init__(self,parent)
            self.var = IntVar()
            Entry(self,textvariable=self.var).pack()
            Button(self,text='Outer Test',command=self.getVar).pack()
        def getVar(self):
            print(self.var.get())

    class Inner(Frame):
        def __init__(self,outer):
            Frame.__init__(self)
            self.outer=outer
            Button(self,text='Inner Test',command=self.getVar).pack()
        def getVar(self):
            print(self.outer.var.get())

    root = Tk()
    out = Outer(root)
    out.pack()
    inn = Inner(out)
    inn.pack()
    root.mainloop()'''

    root = Tk()
    root.title("Sex is real and it affects the future")
    control = PeoplemonController(Database,Peoplemon)
    menu = EditorMenu(control)
    root.config(menu=menu)
    peoplemon = PeoplemonEditor(root,control)

    edit = Editor(root,control)
    edit.pack(side=LEFT,expand=YES,fill=BOTH)

    item = ItemEditor(edit,control)
    item.pack()


    peoplemon.pack(side=RIGHT,padx=(10,0))
    mainloop()