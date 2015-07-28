'''
#-------------------------------------------------------------------------------
# Name:        module1

# Author:      Vincent
#
# Date Created:     01/15/2015
# Date Modified:    01/15/2015
#-------------------------------------------------------------------------------

Purpose:

'''

from Editor import structreader

from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice_new import ListChoice
from Editor.guicomponents.integercheck import IntegerCheck

from tkinter import *
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename,askopenfilename
from tkinter.messagebox import showinfo, showerror

TITLE_FONT = ('tkdefaultfont', 16, 'bold')
SUBTITLE_FONT = ('tkdefaultfont', 11, 'bold')

class EditorMenu(Menu):
    def __init__(self, controller):
        Menu.__init__(self)
        self.editor = editor.gui
        self.controller = controller
        self.last_path = None
        file = Menu(self, tearoff=0)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

    def save(self):
        path = asksaveasfilename(initialdir=self.last_path, title='Save To?')
        if path == '':
            return
        try:
            self.last_path = path
            self.controller.save(path)
        except:
            showerror('Error Saving', 'Error saving: File not saved')

    def load(self):
        path = askopenfilename(initialdir=self.last_path, title='Open from?')
        if path == '':
            return
        try:
            self.last_path = path
            file = open(path,'rb')
            data = bytearray(file.read())
            self.editor.vars['id'].set(structreader.unpack(data,'u16'))
            self.editor.vars['min_lvl'].set(structreader.unpack(data,'u16'))
            self.editor.vars['max_lvl'].set(structreader.unpack(data,'u16'))
            self.editor.vars['rarity'].set(structreader.unpack(data,'u16'))
            self.editor.vars['x'].set(structreader.unpack(data,'u32'))
            self.editor.vars['y'].set(structreader.unpack(data,'u32'))
            self.editor.vars['width'].set(structreader.unpack(data,'u32'))
            self.editor.vars['height'].set(structreader.unpack(data,'u32'))
            self.editor.choices.clear()
            for x in range(structreader.unpack(data,'u16')):
                string = structreader.unpack(data,'str')
                code = structreader.unpack(data,'u16')
                self.editor._add( (string,code) )
        except:
            showerror('Error Loading', 'Error Loading: File not correctly loaded')

class WildEditorGUI(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        ttk.Label(self, text='Wild Pokemon Editor', style='Title.TLabel').pack(padx=10)
        self.vars = controller.vars
        self.controller = controller
        for name, var_name in [('ID', 'id'),
                              ('Minimum Level', 'min_lvl'),
                              ('Maximum Level', 'max_lvl'),
                              ('Rarity (1-?)', 'rarity')]:
            var = IntVar()
            self.vars[var_name] = var
            EntryLabel(self, text=name, entry_variable=var, validate='key',
                       validatecommand=IntegerCheck(self, 'u16').vcmd).pack()


        self.makeSep()
        ttk.Label(self,text='Peoplemon Location', style='Subtitle.TLabel').pack()
        top = ttk.Frame(self)
        bottom = ttk.Frame(self)
        top.pack()
        bottom.pack()
        for name, var_name, frame in [('X', 'x', top),
                                      ('Y', 'y', top),
                                      ('Width', 'width', bottom),
                                      ('Height', 'height', bottom)]:
            var = IntVar()
            self.vars[var_name] = var
            EntryLabel(frame, text=name, entry_variable=var, width=10, validate='key',
                       validatecommand=IntegerCheck(self, 'u32').vcmd).pack(side=LEFT, padx=2)
        self.makeSep()

        self.makeOverides()

    def makeOverides(self):
        frm = ttk.Frame(self)
        frm.pack()
        ttk.Label(frm, text='Overrides').pack()
        input_frm = ttk.Frame(frm)
        input_frm.pack(pady=(0, 2))
        self.string = EntryLabel(input_frm, text='String Code', width=15)
        self.string.pack(side=LEFT, padx=(2, 1))
        self.value_var = IntVar()
        self.code = EntryLabel(input_frm, entry_variable=self.value_var, text='Value', width=15, validate='key',
                               validatecommand=IntegerCheck(self, 'u16').vcmd)
        self.code.pack(side=LEFT, padx=(1, 2))
        self.choices = ListChoice(frm,delete_cmd=self.delete)
        self.choices.pack()
        ttk.Button(frm, text='Add', command=self.add, style='Action.TButton').pack(pady=(5, 10))

    def makeSep(self):
        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X, pady=(12, 0), padx=5)

    def add(self):
        tup = self.string.get(),self.code.get()
        self._add(tup)

    def _add(self, tup):
        self.choices.addChoice(str(tup))
        self.controller.addChoice(tup)

    def delete(self, ind):
        self.choices.delete(ind)
        self.controller.model.delete(ind)



class WildEditor():
    def __init__(self, parent=None):
        self.vars = {}
        self.gui = WildEditorGUI(parent, self)
        self.model = WildEditorModel()

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)

    def save(self, path):
        _id = self.vars['id'].get()
        min_lvl = self.vars['min_lvl'].get()
        max_lvl = self.vars['max_lvl'].get()
        rarity = self.vars['rarity'].get()
        x = self.vars['x'].get()
        y = self.vars['y'].get()
        width = self.vars['width'].get()
        height = self.vars['height'].get()
        self.model.updateInfo(_id,min_lvl,max_lvl,rarity, x, y, width, height)
        try:
            self._save(path)
            showinfo(title='Saved', message='File saved')
        except:
            showerror(title='Error', message='File not saved')

    def _save(self, path):
        data = bytearray()
        structreader.pack(data, self.model.id, 'u16')
        structreader.pack(data, self.model.min_lvl, 'u16')
        structreader.pack(data, self.model.max_lvl, 'u16')
        structreader.pack(data, self.model.rarity, 'u16')
        structreader.pack(data, self.model.x, 'u32')
        structreader.pack(data, self.model.y, 'u32')
        structreader.pack(data, self.model.width, 'u32')
        structreader.pack(data, self.model.height, 'u32')
        structreader.pack(data, len(self.model.overrides), 'u16')
        for override in self.model.overrides:
            structreader.pack(data,override[0], 'str')
            structreader.pack(data,int(override[1]), 'u16')
        file = open(path, 'wb')
        file.write(data)
        file.close()

    def addChoice(self, tup):
        self.model.addOverride(tup[0], tup[1])


class WildEditorModel:
    def __init__(self):
        self.id = 0
        self.min_lvl = 1
        self.max_lvl = 100
        self.rarity = 1
        self.overrides = []

    def __iter__(self):
        for override in self.overrides:
            yield override

    def updateInfo(self, _id, min_lvl, max_lvl, rarity, x, y, width, height):
        self.id = _id
        self.min_lvl = min_lvl
        self.max_lvl = max_lvl
        self.rarity = rarity
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def addOverride(self, string, code):
        self.overrides.append((string, code))

    def delete(self, ind):
        self.overrides.pop(ind)

if __name__ == '__main__':
    root = Tk()
    style = ttk.Style()
    style.configure('Title.TLabel', font=TITLE_FONT)
    style.configure('Subtitle.TLabel', font=SUBTITLE_FONT)
    style.configure('Action.TButton', width=8)
    root.wm_title('Wild Peoplemon Editor')
    editor = WildEditor(root)
    menu = EditorMenu(editor)
    root.config(menu=menu)
    root.resizable(0,0)
    root.iconbitmap('icons/editor.ico')

    editor.pack()
    mainloop()
