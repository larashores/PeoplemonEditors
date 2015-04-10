__author__ = 'Vincent'


from Editor.Database.controller import Controller
from Editor.Database.database import Database

from Editor.Component import Component

from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from Editor.guicomponents.listchoice import ListChoice

TITLE_NAME = 'Database Editor'
TITLE_FONT = ('tkdefaultfont',16,'bold')


class Barrier(Frame):
    '''
    Fill should always be X when packing
    '''
    def __init__(self,parent):
        Frame.__init__(self,parent,height=2,bd=1,relief=SUNKEN)

class Editor(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        Label(self,text=TITLE_NAME,font=TITLE_FONT).pack()
        frm = Frame(self)
        frm.pack()
        self.val = IntVar()
        if hasattr(controller, 'sorts'):
            for ind,(name, func) in enumerate(controller.sorts):
                Radiobutton(frm,
                            text=name,
                            variable = self.val,
                            value = ind,
                           command = lambda: controller.changeSort()).pack(side=LEFT)
        self.list = ObjList(self,controller)
        self.list.pack(expand=YES,fill=X)
        Barrier(self).pack(fill=X,pady=(10,0),padx=(20,20))

class ObjList(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.controller.loadfuncs.append(self.load)

        self.list = ListChoice(self,
                               click_cmd = self.choose,
                               delete_cmd= self.delete,
                               up_cmd    = self.up,
                               down_cmd  = self.down,
                               width     = 50)
        self.list.pack(expand=YES,fill=BOTH)
        Button(self,text='Add New',command=self.add).pack(pady=(5,0))
    def choose(self,ind):
        if ind == -1:
            return
        self.controller.click(ind)
    def up(self):
        self.controller.up()
    def down(self):
        self.controller.down()
    def delete(self):
        self.controller.delObj()
    def add(self):
        self.controller.addObj()
        self.list.setPosition(1.0)      #Moves to end
    def load(self,ind):
        pos = self.list.getPosition()
        self.updateView()
        if ind == -1:
            return
        self.list.setSelection(ind)
        self.list.setPosition(pos)
    def updateView(self):
        self.list.clear()
        for string in self.controller.getStrings():
            self.list.addChoice(string)

class EditorMenu(Menu):
    def __init__(self,controller):
        Menu.__init__(self)
        self.controller = controller
        file = Menu(self, tearoff=0)
        file.add_command(label='Save',command=self.save)
        file.add_command(label='Load',command=self.load)
        self.add_cascade(label='File',menu=file)
    def save(self):
        path = asksaveasfilename()
        if path == '':
            return
        self.controller.saveToFile(path)
    def load(self):
        path = askopenfilename()
        if path == '':
            return
        self.controller.loadFromFile(path)

if __name__ == '__main__':
    root = Tk()
    root.title("Sex is real and it affects the future")
    control = Controller(Database,Component)
    menu = EditorMenu(control)
    root.config(menu=menu)
    edit = Editor(root,control)
    edit.pack(expand=YES,fill=BOTH)
    mainloop()