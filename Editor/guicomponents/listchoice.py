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

import inspect

from tkinter import *

class ListChoiceGUI(Frame):
    '''
    Purpose:    Scrolling Listbox where entries can be added and deleted
    Attributes:
        parent:     Parent widget
        choicelist: The list where choice strings are stored
        indexvar:   IntVar where the selected index is stored
    '''
    def __init__(self,parent,controller,click_cmd,delete_cmd,up_cmd,down_cmd,**kwargs):
        Frame.__init__(self,parent)
        self.controller = controller
        self.click_cmd = click_cmd
        self.delete_cmd = delete_cmd
        self.up_cmd = up_cmd
        self.down_cmd = down_cmd
        self.MakeWidgets(kwargs)
        self.lbox.bind('<Delete>', (lambda event: self.delete()) )
        self.lbox.bind('<Button-1>', (lambda event: self.click()) )
        self.lbox.bind('<Up>',(lambda event: self.up()) )
        self.lbox.bind('<Down>',(lambda event: self.down()) )
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
        self.sbar = sbar
        self.hsbar = hsbar
    def delete(self):
        ind = self.lbox.curselection()[0]
        self.delete_cmd(ind)
    def click(self):
        self.after(20,self._click)
    def _click(self):
        val = self.lbox.curselection()
        if len(val) != 1:
            self.click_cmd(-1)
        else:
            self.click_cmd(int(val[0]))

    def up(self):
        self.after(20,lambda: self.up_cmd())
    def down(self):
        self.after(20,lambda: self.down_cmd())

class ListChoice():
    def __init__(self,parent=None,*,
                 click_cmd=lambda x: None,
                 delete_cmd=lambda x: None,
                 up_cmd=lambda x: None,
                 down_cmd=lambda x: None,**kwargs):
        self.model = ListChoiceModel()
        self.gui = ListChoiceGUI(parent,self,click_cmd,delete_cmd,up_cmd,down_cmd,**kwargs)
    def __iter__(self):
        for choice in self.model:
            yield choice
    def __getitem__(self,index):
        return self.model.choices[index]
    def __len__(self):
        return len(self.model.choices)
    def pack(self,**kwargs):
        self.gui.pack(**kwargs)
    def index(self,ind):
        return self.model.choices.index(ind)
    def addChoice(self,string):
        self.model.addChoice(string)
        self.update()

    def setPosition(self,fraction):
        self.gui.lbox.yview_moveto(fraction)
    def getPosition(self):
        return self.gui.lbox.yview()[0]
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
    def getCurSelection(self):
        return self.gui.lbox.curselection()[0]
    def setSelection(self,ind):
        self.gui.lbox.selection_clear(0)
        self.gui.lbox.selection_set(ind)

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
    list1.pack(expand=YES,fill=BOTH)

    for choice in ['1','poop','2','4asfd']:
        list1.addChoice(choice)
    mainloop()