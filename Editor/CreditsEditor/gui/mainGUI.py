__author__ = 'Vincent'


import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice_new import ListChoice
from Editor.guicomponents.integercheck import IntegerCheck

TEXT = 'Text Credit'
IMAGE = 'Image Credit'

class Editor(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.loadFunc = self.loadFile
        ttk.Label(self, text='Credits Editor', style='Title.TLabel').pack()
        self.checkVar = tk.IntVar()
        ttk.Checkbutton(self, text='Add Before?', variable=self.checkVar).pack()
        self.list = ListChoice(self, update_cmd=self.chooseCredit, delete_cmd=self.delete, width=50)
        self.list.pack()

        butFrame = ttk.Frame(self)
        butFrame.pack(pady=(5, 0))
        ttk.Button(butFrame, text='Add Text', width=15, command=self.addText).pack(side=tk.LEFT, padx=2)
        ttk.Button(butFrame, text='Add Image', width=15, command=self.addImage).pack(side=tk.LEFT, padx=2)
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(expand=tk.YES, fill=tk.X, padx=10, pady=12)
        self.typeVar = tk.StringVar()
        self.typeVar.set(TEXT)
        self.button = None
        self.edit = None
        self.cur_ind = None

    def loadFile(self):
        self.loadList()
        if self.controller.getNumCredits() == 0:
            if self.edit:
                self.edit.destroy()
                self.edit = None
            if self.button:
                self.button.destroy()
                self.button = None
        else:
            self.list.setSelection(0)

    def loadList(self):
        self.list.clear()
        for string in self.controller.getStrings():
            self.list.addChoice(string)

    def delete(self, ind):
        self.controller.delete(ind)
        self.list.delete(ind)
        if self.controller.getNumCredits() == 0:
            self.edit.destroy()
            self.button.destroy()
            self.edit = None
            self.button = None

    def makeApply(self):
        self.button = ttk.Button(self, text='Apply', width=8, command=self.apply)
        self.button.pack(pady=(5, 10), side=tk.BOTTOM)

    def addText(self):
        if self.edit:
            self.edit.destroy()
        self.edit = TextEditor(self, self.controller, relief=tk.GROOVE)
        self.edit.pack()
        if not self.button:
            self.makeApply()
        ind = self.getInsertIndex()
        self.controller.addTextCredit(ind)
        self.loadList()
        self.list.setSelection(ind)

    def addImage(self):
        if self.edit:
            self.edit.destroy()
        self.edit = ImageEditor(self, self.controller, relief=tk.GROOVE)
        self.edit.pack()
        if not self.button:
            self.makeApply()
        ind = self.getInsertIndex()
        self.controller.addImageCredit(ind)
        self.loadList()
        self.list.setSelection(ind)

    def getInsertIndex(self):
        if self.checkVar.get() == 1:
            ind = self.cur_ind if self.cur_ind else 0
        else:
            ind = self.controller.getNumCredits()
        return ind

    def chooseCredit(self, ind):
        self.cur_ind = ind
        if self.edit:
            self.edit.destroy()
        type = self.controller.getCreditType(ind)
        if type == 'text':
            if self.edit:
                self.edit.destroy()
            self.edit = TextEditor(self, self.controller, relief=tk.GROOVE)
            self.edit.pack()
            if not self.button:
                self.makeApply()
        elif type == 'image':
            if self.edit:
                self.edit.destroy()
            self.edit = ImageEditor(self, self.controller, relief=tk.GROOVE)
            self.edit.pack()
            if not self.button:
                self.makeApply()
        self.edit.load(ind)

    def apply(self):
        self.edit.apply(self.cur_ind)
        self.loadList()


class TextEditor(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.textVar = tk.StringVar()
        self.xPosVar = tk.IntVar()
        self.yBufVar = tk.IntVar()
        self.fontVar = tk.IntVar()
        self.colors = (0, 0, 0)

        frm = ttk.Frame(self)
        frm.pack(padx=(4, 5), pady=(2, 0))
        EntryLabel(frm, text='X Position', entry_variable=self.xPosVar, validate='key',
                   validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=tk.LEFT)
        EntryLabel(frm, text='Y Buffer', entry_variable=self.yBufVar, validate='key',
                   validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=tk.LEFT)

        frm = ttk.Frame(self)
        frm.pack(padx=(4, 5), pady=(0, 4))
        EntryLabel(frm, text='Text', entry_variable=self.textVar).pack(side=tk.LEFT)
        EntryLabel(frm, text='Font Size', entry_variable=self.fontVar, validate='key',
                   validatecommand=IntegerCheck(self, 'u16').vcmd).pack(side=tk.LEFT)

        self.canvas = tk.Canvas(self, width=100, height=20, bg=self.rgbToHex(*self.colors), relief=tk.GROOVE, bd=5,
                                highlightthickness=0)
        self.canvas.pack()
        ttk.Button(self, text='Color', width=10, command=self.chooseColor).pack(pady=(2, 5))

    def load(self, ind):
        xPos, yBuf, text, red, green, blue, fontSize = self.controller.loadTextCredit(ind)
        self.xPosVar.set(xPos)
        self.yBufVar.set(yBuf)
        self.textVar.set(text)
        self.fontVar.set(fontSize)
        self.canvas.configure(bg=self.rgbToHex(red, green, blue))

    def apply(self, ind):
        text = self.textVar.get()
        fontSize = self.fontVar.get()
        xPos = self.xPosVar.get()
        yPos = self.yBufVar.get()
        red, green, blue = self.colors
        self.controller.editTextCredit(ind, xPos, yPos, text, red, green, blue, fontSize)

    def chooseColor(self):
        rgb, color = askcolor(self.rgbToHex(*self.colors), title='Choose Text color')
        if rgb:
            self.colors = [int(c) for c in rgb]
            self.canvas.configure(bg=self.rgbToHex(*self.colors))

    def rgbToHex(self, r, g, b):
        return '#%02x%02x%02x' % (r, g, b)


class ImageEditor(ttk.Frame):
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.pathVar = tk.StringVar()
        self.xPosVar = tk.IntVar()
        self.yBufVar = tk.IntVar()

        frm = ttk.Frame(self)
        frm.pack(padx=(4, 5), pady=(2, 0))
        EntryLabel(frm, text='X Position', entry_variable=self.xPosVar).pack(side=tk.LEFT)
        EntryLabel(frm, text='Y Buffer', entry_variable=self.yBufVar).pack(side=tk.LEFT)

        frm = ttk.Frame(self)
        frm.pack(padx=(4, 5), pady=(0, 4))
        EntryLabel(frm, text='Path', entry_variable=self.pathVar).pack(padx=2, pady=(2, 5))

    def load(self, ind):
        xPos, yBuf, path = self.controller.loadImageCredit(ind)
        self.xPosVar.set(xPos)
        self.yBufVar.set(yBuf)
        self.pathVar.set(path)

    def apply(self, ind):
        xPos = self.xPosVar.get()
        yPos = self.yBufVar.get()
        path = self.pathVar.get()
        self.controller.editImageCredit(ind, xPos, yPos, path)



