__author__ = 'Vincent'

from Editor.ItemDatabase.controller import ItemController
from Editor.Database.gui import Editor, EditorMenu
from Editor.Database.database import Database

from Editor.ItemDatabase.Item import Item

from tkinter import *
from tkinter.messagebox import showerror
from Editor.guicomponents.entrylabel import EntryLabel

TITLE_NAME = 'Item Database Editor'
TITLE_FONT = ('tkdefaultfont',16,'bold')



class ItemEditor(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.controller.loadfuncs.append(self.load)
        frm = Frame(self)
        frm.pack()
        self.id_var = IntVar()
        self.name_var = StringVar()
        EntryLabel(frm,
                   text='ID',
                   textvariable=self.id_var).pack(side=LEFT)
        name = EntryLabel(frm,
                   text='Name',
                   textvariable=self.name_var)
        name.pack(side=LEFT)
        Label(self,text='Description').pack()
        self.desc = Text(self,height=10,width=45)
        self.desc.pack()
        Button(self,text='Apply',command=self.apply).pack(side=BOTTOM)
        name.bind('<Return>', lambda x: self.apply())
        self.desc.bind('<Return>', lambda x: self.apply())
    def apply(self):
        success = self.controller.update(
                                         [self.id_var.get(),
                                          self.name_var.get(),
                                          self.desc.get(1.0, END)] )
        if success is False:
            showerror(title='Error',message='ID Already Taken')
            self.controller.load()
    def load(self,ind):
        attrs = self.controller.loadObj(ind)
        self.id_var.set(attrs[0])
        self.name_var.set(attrs[1])
        self.desc.delete('1.0',END)
        self.desc.insert(END,attrs[2])

if __name__ == '__main__':
    root = Tk()
    root.title("Sex is real and it affects the future")
    control = ItemController(Database,Item)
    menu = EditorMenu(control)
    root.config(menu=menu)
    edit = Editor(root,control)
    edit.pack(expand=YES,fill=BOTH)
    item = ItemEditor(edit,control)
    item.pack()
    mainloop()