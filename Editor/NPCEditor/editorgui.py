'''
#-------------------------------------------------------------------------------
# Name:        module1

# Author:      Vincent
#
# Date Created:     02/12/2015
# Date Modified:    02/12/2015
#-------------------------------------------------------------------------------

Purpose:

'''

TITLE_FONT = ('tkdefaultfont',16,'bold')

OLAN_PATH = r'Resources\olan.jpg'


import tkinter as tk
from tkinter import ttk
from Editor.guicomponents.listchoice_new import ListChoice
from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.NPCEditor.controller import Controller
from tkinter.filedialog import asksaveasfilename, askopenfilename
from Editor.NPCEditor.constants import *



class Editor(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.vars = {'name': tk.StringVar(),
                     'animation': tk.StringVar(),
                     'conversation': tk.StringVar(),
                     }
        self.controller.load_funcs['name'] = self.loadName
        self.controller.load_funcs['animation'] = self.loadAnimation
        self.controller.load_funcs['conversation'] = self.loadConversation
        ttk.Label(self, text='NPC Editor',  style='Title.TLabel').pack()
        EntryLabel(self, text='NPC Name', entry_variable=self.vars['name']).pack()
        EntryLabel(self, text='Animation Name', entry_variable=self.vars['animation']).pack()
        EntryLabel(self, text='Conversation Filename', entry_variable=self.vars['conversation']).pack()
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(expand=tk.YES, fill=tk.X, padx=3, pady=(12, 5))
        self.walk = WalkType(self, self.controller)
        self.walk.pack(pady=(0, 3))

    def apply(self):
        self.controller.updateModel('name', self.vars['name'].get())
        self.controller.updateModel('anim', self.vars['animation'].get())
        self.controller.updateModel('convo', self.vars['conversation'].get())

    def loadName(self, x):
        self.vars['name'].set(x)

    def loadAnimation(self, x):
        self.vars['animation'].set(x)

    def loadConversation(self, x):
        self.vars['conversation'].set(x)


class EditorMenu(tk.Menu):
    def __init__(self,editor,controller):
        tk.Menu.__init__(self)
        self.controller = controller
        self.last_path = None
        self.editor = editor
        file = tk.Menu(self, tearoff=0)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

    def save(self):
        self.editor.apply()
        path = asksaveasfilename(title='Save to?', initialdir=self.last_path)
        if path:
            self.last_path = path
            self.controller.save(path)

    def load(self):
        path = askopenfilename(title='Load from?', initialdir=self.last_path)
        if path:
            self.last_path = path
            self.controller.load(path)


class WalkType(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.var = tk.StringVar()
        self.controller.load_funcs['behavior'] = self.load
        self.edit = None
        ttk.Label(self, text='Motion Type').pack()
        combo = ttk.Combobox(self, textvariable=self.var, values=[B_STILL, B_SPIN, B_FOLLOW, B_WANDER])
        combo.state(['readonly'])
        combo.pack()
        combo.bind('<<ComboboxSelected>>', self.changeEdit)
        self.var.set('Stand Still')

    def changeEdit(self,event):
        var = self.var.get()
        self.controller.updateModel('behavior', var)
        try:
                self.edit.destroy()
        except AttributeError:
            pass
        if var == B_SPIN:
            self.edit = SpinInPlace(self, self.controller)
            self.edit.pack()
        elif var == B_WANDER:
            self.edit = WanderFreely(self, self.controller)
            self.edit.pack()
        elif var == B_FOLLOW:
            self.edit = FollowPath(self, self.controller)
            self.edit.pack()

    def load(self, string):
        self.var.set(string)
        self.changeEdit(None)

# --------------------Walk Editing classes----------------


class SpinInPlace(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.load_funcs['direction'] = self.load
        self.var = tk.StringVar()
        ttk.Label(self, text='Direction').pack()
        combo = ttk.Combobox(self, textvariable=self.var, values=[D_CLOCK, D_COUNTER,  D_RANDOM])
        combo.state(['readonly'])
        combo.pack()
        combo.bind('<<ComboboxSelected>>', lambda event: self.update())
        self.var.set(D_CLOCK)

    def update(self):
        self.controller.updateModel('direction', self.var.get())

    def load(self, string):
        self.var.set(string)


class WanderFreely(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.load_funcs['wanderRadius'] = self.load
        self.rad_var = tk.IntVar()
        EntryLabel(self, text='Wander Radius', entry_variable=self.rad_var).pack()
        ttk.Button(self, text='Apply', command=self.apply).pack(pady=(5, 0))

    def apply(self):
        self.controller.updateModel('wander',self.rad_var.get())

    def load(self,radius):
        self.rad_var.set(radius)


class FollowPath(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.load_funcs['nodes'] = self.load
        self.nodes = []
        self.rev_var = tk.IntVar()
        ttk.Checkbutton(self, text='Reverse loop', variable=self.rev_var, command=self.apply).pack()
        self.dir_var = tk.StringVar()
        self.dispNodes = ListChoice(self, delete_cmd=self.delete)
        self.dispNodes.pack()
        frm = ttk.Frame(self)
        new_frm = ttk.Frame(frm)
        new_frm.pack(side=tk.LEFT)
        ttk.Label(new_frm, text='Direction').pack()
        combo = ttk.Combobox(new_frm, textvariable=self.dir_var, values=('Up', 'Left', 'Right', 'Down'), width=5)
        combo.pack()
        combo.state(['readonly'])
        self.dir_var.set('Up')
        self.steps_var = tk.IntVar()
        EntryLabel(frm, text='Number of Steps', entry_variable=self.steps_var, width=14).pack(side=tk.LEFT)
        frm.pack()

        ttk.Button(self, text='Add', command=self.add).pack(pady=(8, 0))

    def add(self):
        tup = (self.dir_var.get().lower(), self.steps_var.get())
        self.controller.updateModel('add', tup)
        self.dispNodes.addChoice(tup)

    def delete(self, ind):
        self.controller.updateModel('del', ind)
        self.dispNodes.delete(ind)

    def apply(self):
        self.controller.updateModel('rev', self.rev_var.get())

    def load(self, tup):
        self.rev_var.set(tup[0])
        nodes = tup[1]
        for node in nodes:
            self.dispNodes.addChoice(node)
"""
class Olan(tk.Canvas):
    def __init__(self, parent):
        tk.Canvas.__init__(self,parent,width=500,height=630,highlightthickness=0)
        self.olan = Image.open(OLAN_PATH)
        self.olanTk = ImageTk.PhotoImage(self.olan)
        self.create_image( (250,315),image=self.olanTk)
"""

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)
    style = ttk.Style()
    style.configure('Title.TLabel', font=TITLE_FONT)
    #olan = Olan(root)
    #olan.place( relx=.5,rely=.5,anchor=CENTER)
    control = Controller()
    edit = Editor(root,control)
    menu = EditorMenu(edit,control)
    root.config(menu=menu)
    root.title('NPC Editor')
    root.iconbitmap('icons/editor.ico')
    #root.geometry('500x630')
    edit.pack(padx=(5, 5), pady=(3, 3))
    tk.mainloop()
