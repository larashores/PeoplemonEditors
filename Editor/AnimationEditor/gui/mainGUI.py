__author__ = 'Vincent'



from tkinter import *
from tkinter import ttk

from Editor.AnimationEditor.gui import sidebar
from Editor.AnimationEditor.gui.spriteCanvas import SpriteSheetCanvas
from Editor.AnimationEditor.controller import Controller
from Editor.AnimationEditor.gui.frameViewer import FrameWindow

import os

from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import showinfo, showerror, showwarning

from Editor.AnimationEditor.gui.changeScale import askChange


class EditorMenu(Menu):
    def __init__(self, controller):
        Menu.__init__(self)
        self.controller = controller
        file = Menu(self, tearoff=0)
        file.add_command(label='New', command=self.new)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

        edit = Menu(self, tearoff=0)
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


class AnimationEditor(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        left = ttk.Frame(self)
        left.pack(side=LEFT, expand=YES, fill=BOTH)
        right = ttk.Frame(self, style='Boxed.TFrame')
        right.pack(side=RIGHT, expand=YES, fill=Y)

        self.sidebar = sidebar.SideBar(right, controller)
        self.canvas = SpriteSheetCanvas(left, controller, self.sidebar.vars)

        self.canvas.pack(side=LEFT)
        self.sidebar.pack(padx=5, pady=5)


if __name__ == '__main__':
    controller = Controller()
    root = Tk()
    menu = EditorMenu(controller)
    root.config(menu=menu)
    root.title('Animation Editor')

    FrameWindow(root, controller)

    style = ttk.Style()
    style.configure('Boxed.TFrame', relief=RIDGE, borderwidth=5)
    style.configure('Action.TButton', width=8)

    editor = AnimationEditor(root, controller)
    editor.pack()

    root.mainloop()
