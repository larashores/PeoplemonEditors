import tkinter as tk
from tkinter.messagebox import showerror, showinfo, showwarning
from tkinter.filedialog import asksaveasfilename, askopenfilename

import os

from Editor.AnimationEditor.gui.changeScale import askChange


class EditorMenu(tk.Menu):
    def __init__(self, controller):
        tk.Menu.__init__(self)
        self.controller = controller
        file = tk.Menu(self, tearoff=0)
        file.add_command(label='New', command=self.new)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

        edit = tk.Menu(self, tearoff=0)
        edit.add_command(label='Change Scale', command=self.changeScale)
        self.add_cascade(label='Edit', menu=edit)

    def save(self):
        if not self.controller.animationLoaded():
            showwarning(title='Warning', message='No Animation Loaded')
            return
        path = asksaveasfilename(title='Save Animation', initialdir=self.controller.last_visited)
        if not path:
            return
        self.controller.last_visited = os.path.split(path)[0]
        try:
            self.controller.save(path)
            showinfo('Saved', 'Animation saved')
        except:
            showerror('Error', 'Animation not saved')

    def load(self):
        path = askopenfilename(title='Animation File?', initialdir=self.controller.last_visited)
        if path:
            self.controller.last_visited = os.path.split(path)[0]
            self.controller.load(path)

    def new(self):
        path = askopenfilename(title='Sprite Sheet?', initialdir=self.controller.last_visited)
        if path:
            self.controller.last_visited = os.path.split(path)[0]
            self.controller.newSheet(path)

    def changeScale(self):
        scale = askChange(self.controller.getScale())
        self.controller.changeScale(scale)
