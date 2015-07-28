'''
#-------------------------------------------------------------------------------
# Name:        listchoice.py

# Author:      Vincent
#
# Date Created:     01/15/2015
# Date Modified:    01/15/2015
#-------------------------------------------------------------------------------

Purpose:

'''

from tkinter import *

class ListChoiceGUI(Frame):
    '''
    Purpose:    Scrolling Listbox where entries can be added and deleted
    Attributes:
        parent:     Parent widget
        choicelist: The list where choice strings are stored
        indexvar:   IntVar where the selected index is stored
    '''
    def __init__(self,parent,controller,**kwargs):
        Frame.__init__(self,parent)
        self.controller = controller
        self.MakeWidgets(kwargs)
        self.lbox.bind('<Delete>', (lambda event: self.delete()) )
    def MakeWidgets(self,kwargs):
        frm = Frame(self)
        sbar = Scrollbar(frm)
        lbox = Listbox(frm,**kwargs)
        frm.pack(expand=YES,fill=X)
        sbar.config(command=lbox.yview)
        lbox.config(yscrollcommand=sbar.set)
        lbox.config(selectmode=SINGLE)

        hsbar = Scrollbar(self,orient=HORIZONTAL)
        hsbar.config(command=lbox.xview)
        lbox.config(xscrollcommand=hsbar.set)

        sbar.pack(side=RIGHT,fill=Y)
        hsbar.pack(side=TOP,fill=X)
        lbox.pack(side=LEFT,expand=YES,fill=X)
        self.lbox = lbox
    def delete(self):
        self.controller.delete(self.lbox.curselection()[0])

class ListChoice():
    def __init__(self,parent=None):
        self.model = ListChoiceModel()
        self.gui = ListChoiceGUI(parent,self)
    def pack(self,**kwargs):
        self.gui.pack(**kwargs)
    def addChoice(self,string):
        self.model.addChoice(string)
        self.update()
    def delete(self,ind):
        self.model.delete(int(ind))
        self.update()
    def clear(self):
        self.model.choices.clear()
        self.update()
    def update(self):
        self.gui.lbox.delete(0,END)
        for choice in self.model:
            self.gui.lbox.insert(END,choice)
    def choices(self):
        return list(self.model)

class ListChoiceModel():
    def __init__(self):
        self.choices = []
    def __iter__(self):
        for choice in self.choices:
            yield choice
    def addChoice(self,string):
        self.choices.append(string)
    def delete(self,ind):
        self.choices.pop(ind)

if __name__ == '__main__':
    root = Tk()
    list1 = ListChoice()
    list1.pack()

    for choice in ['1','poop','2','4asfd']:
        list1.addChoice(choice)
    mainloop()