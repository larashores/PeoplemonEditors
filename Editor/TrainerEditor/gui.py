__author__ = 'Vincent'


import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice_new import ListChoice
from Editor.guicomponents.integercheck import IntegerCheck

from Editor.TrainerEditor.constants import *

TITLE_FONT = ('tkdefaultfont', 16, 'bold')
SUBTITLE_FONT = ('tkdefaultfont', 10, 'bold')


class TrainerEditor(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.vars = {'name': tk.StringVar(),
                     'animation': tk.StringVar(),
                     'beforeConvo': tk.StringVar(),
                     'afterConvo': tk.StringVar(),
                     'lostText': tk.StringVar(),
                     'sightRange': tk.IntVar(),
                     'aiType': tk.StringVar(),
                     }
        self.aiTypes = {AI_RANDOM: 0, AI_DUMB: 1, AI_SMART: 2, AI_SUICIDAL: 3, AI_AGGRESSIVE: 4, AI_DEFENSIVE: 5,
                        AI_AVERAGE: 6, AI_ADAPTIVE: 7}
        self.controller.load_funcs.append(self.load)
        self.controller.apply_funcs.append(self.apply)

        ttk.Label(self, text='Trainer Editor',  style='Title.TLabel').pack()

        top_frm = ttk.Frame(self)
        middle_frm = ttk.Frame(self)
        bottom_frm = ttk.Frame(self)

        top_frm.pack()
        middle_frm.pack()
        bottom_frm.pack()

        EntryLabel(top_frm, text='Trainer Name', entry_variable=self.vars['name'],
                   width=22).pack(side=tk.LEFT, padx=5)
        EntryLabel(top_frm, text='Animation Name', entry_variable=self.vars['animation'],
                   width=22).pack(side=tk.LEFT, padx=5)
        EntryLabel(middle_frm, text='Before Battle Conversation', entry_variable=self.vars['beforeConvo'],
                   width=22).pack(side=tk.LEFT, padx=5)
        EntryLabel(middle_frm, text='After Battle Conversation', entry_variable=self.vars['afterConvo'],
                   width=22).pack(side=tk.LEFT, padx=5)
        EntryLabel(bottom_frm, text='Lost Battle Text', entry_variable=self.vars['lostText'],
                   width=22).pack(side=tk.LEFT, padx=5)
        EntryLabel(bottom_frm, text='Sight Range', entry_variable=self.vars['sightRange'], width=22,
                   validate='key', validatecommand=IntegerCheck(self, 'u8').vcmd).pack(side=tk.LEFT, padx=5)

        ttk.Label(self,text='AI Type').pack()
        combo = ttk.Combobox(self, textvariable=self.vars['aiType'], values=(AI_RANDOM, AI_DUMB, AI_SMART, AI_SUICIDAL,
                                                                             AI_AGGRESSIVE, AI_DEFENSIVE, AI_AVERAGE,
                                                                             AI_ADAPTIVE))
        combo.state(['readonly'])
        combo.pack()
        combo.bind('<<ComboboxSelected>>', self.changeChoice)
        self.vars['aiType'].set(AI_RANDOM)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(expand=tk.YES, fill=tk.X, padx=8, pady=(12, 5))
        frm = ttk.Frame(self)
        frm.pack(padx=10)
        self.peoplemon = ParamList(frm, controller, 'peoplemon')
        self.peoplemon.pack(side=tk.LEFT)
        ttk.Separator(frm, orient=tk.VERTICAL).pack(side=tk.LEFT,expand=tk.YES, fill=tk.Y, padx=(10, 12), pady=8)
        self.items = ParamList(frm, controller, 'items')
        self.items.pack(side=tk.LEFT)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(expand=tk.YES, fill=tk.X, padx=8, pady=(12, 5))
        self.walk = WalkType(self, self.controller)
        self.walk.pack(pady=(0, 10))

    def changeChoice(self, event):
        text = self.vars['aiType'].get()
        self.controller.updateModel('aiType', self.aiTypes[text])

    def apply(self):
        self.controller.updateModel('name', self.vars['name'].get())
        self.controller.updateModel('anim', self.vars['animation'].get())
        self.controller.updateModel('beforeConvo', self.vars['beforeConvo'].get())
        self.controller.updateModel('afterConvo', self.vars['afterConvo'].get())

        self.controller.updateModel('lostText', self.vars['lostText'].get())
        self.controller.updateModel('sight', self.vars['sightRange'].get())

        var = self.vars['aiType'].get()
        for name, value in self.aiTypes.items():
            if var == name:
                _type = value
        self.controller.updateModel('aiType', _type)

    def load(self):
        self.peoplemon.clear()
        self.items.clear()
        name, anim, before, after, lost, sight, aiType = self.controller.loadAttribs(['name', 'animation',
                                                                                      'beforeConvo', 'afterConvo',
                                                                                      'lostText', 'sightRange',
                                                                                      'aiType'])
        self.vars['name'].set(name)
        self.vars['animation'].set(anim)
        self.vars['beforeConvo'].set(before)
        self.vars['afterConvo'].set(after)
        self.vars['lostText'].set(lost)
        self.vars['sightRange'].set(sight)

        for name, value in self.aiTypes.items():
            if aiType == value:
                _type = name
        self.vars['aiType'].set(_type)


class ParamList(ttk.Frame):
    def __init__(self, parent, controller, type):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.load_funcs.append(self.load)
        self.type = type
        if type == 'peoplemon':
            text = 'Filename'
            ttk.Label(self, text='Peoplemon List', style='Subtitle.TLabel').pack()
            validate = 'none'
            self.choice_var = tk.StringVar()
        elif type == 'items':
            text = 'Item ID'
            ttk.Label(self, text='Item List', style='Subtitle.TLabel').pack()
            validate = 'key'
            self.choice_var = tk.IntVar()
        else:
            raise Exception('Unkown type ' + str(type))

        self.choices = ListChoice(self, delete_cmd=self.delete, height=6)
        self.choices.pack()

        frm = ttk.Frame(self)
        frm.pack(pady=(5, 5))
        ttk.Label(frm, text=text).pack(side=tk.LEFT)
        ttk.Entry(frm, textvariable=self.choice_var, width=15, validate=validate, validatecommand=IntegerCheck(self, 'u16').vcmd, justify=tk.CENTER).pack(side=tk.LEFT)
        ttk.Button(self, text='Add', style='Action.TButton', command=lambda: self.add(self.choice_var.get())).pack()

    def add(self, name):
        self.choices.addChoice(name)
        if self.type == 'peoplemon':
            self.controller.updateModel('add-peoplemon', name)
        elif self.type == 'items':
            self.controller.updateModel('add-item', name)

    def delete(self, ind):
        self.choices.delete(ind)
        if self.type == 'peoplemon':
            self.controller.updateModel('del-peoplemon', ind)
        elif self.type == 'items':
            self.controller.updateModel('del-item', ind)

    def clear(self):
        self.choices.clear()

    def load(self):
        if self.type == 'peoplemon':
            for name in self.controller.getPeoplemon():
                self.choices.addChoice(name)
        elif self.type == 'items':
            for _id in self.controller.getItems():
                self.choices.addChoice(_id)


class EditorMenu(tk.Menu):
    def __init__(self, controller):
        tk.Menu.__init__(self)
        self.controller = controller
        self.last_path = None
        file = tk.Menu(self, tearoff=0)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

    def save(self):
        self.controller.apply()
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
        self.controller.load_funcs.append(self.load)
        self.edit = None
        ttk.Label(self, text='Motion Type').pack()
        combo = ttk.Combobox(self, textvariable=self.var, values=[B_STILL, B_SPIN, B_FOLLOW, B_WANDER])
        combo.state(['readonly'])
        combo.pack(pady=(0, 5))
        combo.bind('<<ComboboxSelected>>', self.changeEdit)
        self.var.set('Stand Still')

    def changeEdit(self, event):
        var = self.var.get()
        self.controller.updateModel('behavior', var)
        try:
                self.edit.destroy()
        except AttributeError:
            pass
        if var == B_SPIN:
            self.edit = SpinInPlace(self, self.controller)
            self.edit.pack()
            self.edit.load()
        elif var == B_WANDER:
            self.edit = WanderFreely(self, self.controller)
            self.edit.pack()
            self.edit.load()
        elif var == B_FOLLOW:
            self.edit = FollowPath(self, self.controller)
            self.edit.pack()
            self.edit.load()

    def load(self):
        string = self.controller.getType()
        self.var.set(string)
        self.changeEdit(None)

# --------------------Walk Editing classes----------------


class SpinInPlace(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.var = tk.StringVar()
        ttk.Label(self, text='Direction').pack()
        combo = ttk.Combobox(self, textvariable=self.var, values=[D_CLOCK, D_COUNTER,  D_RANDOM])
        combo.state(['readonly'])
        combo.pack()
        combo.bind('<<ComboboxSelected>>', lambda event: self.update())
        self.var.set(D_CLOCK)

    def update(self):
        self.controller.updateModel('direction', self.var.get())

    def load(self):
        string = self.controller.getDirection()
        self.var.set(string)


class WanderFreely(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.apply_funcs.append(self.apply)
        self.rad_var = tk.IntVar()
        EntryLabel(self, text='Wander Radius', entry_variable=self.rad_var, validate='key',
                   validatecommand=IntegerCheck(self, 'u8').vcmd).pack()

    def apply(self):
        self.controller.updateModel('wander', self.rad_var.get())

    def load(self):
        radius = self.controller.getWanderRadius()
        self.rad_var.set(radius)


class FollowPath(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.nodes = []
        self.rev_var = tk.IntVar()
        ttk.Checkbutton(self, text='Reverse loop', variable=self.rev_var, command=self.apply).pack()
        self.dir_var = tk.StringVar()
        self.dispNodes = ListChoice(self, delete_cmd=self.delete, height=4)
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
        EntryLabel(frm, text='Number of Steps', entry_variable=self.steps_var, width=14, validate='key',
                   validatecommand=IntegerCheck(self, 'u8').vcmd).pack(side=tk.LEFT)
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

    def load(self):
        reverse_loop = self.controller.getReverseLoop()
        self.rev_var.set(reverse_loop)
        for node in self.controller.getNodes():
            self.dispNodes.addChoice(node)


if __name__ == '__main__':
    from Editor.TrainerEditor.controller import Controller

    root = tk.Tk()
    root.title('Trainer Editor')
    root.iconbitmap('icons/editor.ico')
    style = ttk.Style()
    style.configure('Title.TLabel', font=TITLE_FONT)
    style.configure('Subtitle.TLabel', font=SUBTITLE_FONT)

    controller = Controller()

    editor = TrainerEditor(root, controller)
    editor.pack()


    menu = EditorMenu(controller)
    root.configure(menu=menu)

    root.mainloop()

