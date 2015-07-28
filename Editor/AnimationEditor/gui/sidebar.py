__author__ = 'Vincent'

from tkinter import *
from tkinter import ttk

from Editor.AnimationEditor.gui.preview import PreviewWindow

from tkinter.messagebox import showwarning

from Editor.AnimationEditor.gui.entrylabel import EntryLabel


class SideBar(ttk.Frame):
    """
    Sidebar selecting next to spritesheet. Sidebar.canvas attribute should be
    assigned after initializing
    """
    def __init__(self, parent, controller, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.controller = controller
        self.controller.apply_funcs.append(self.apply)
        self.vars = {}
        self.widgets = {}
        for name, var_name, cType in (('Length (ms)', 'length', 'u32'),
                               ('Width', 'width', 'u32'),
                               ('Height', 'height', 'u32'),
                               ('Rotation', 'rotation', 'u32'),
                               ('Active Frame', 'active_frame', 'u8'),
                               ('# of Frames', 'num_frames', 'u8'),
                               ('Spacing', 'spacing', 'u16')):
            var = self.createVar(var_name)
            self.vars[var_name] = var
            entry = EntryLabel(self, text=name, entry_variable=var, height=10, validate='key',
                               validatecommand=IntegerCheck(self, cType).vcmd)
            entry.pack()
            self.widgets[var_name] = entry
            if var_name == 'height':
                self.makeXY(('x', 'y'), 'u32')
                ttk.Separator(self, orient=HORIZONTAL).pack(expand=YES, fill=X, padx=5, pady=(12, 5))
                ttk.Label(self, text='Render Offsets').pack()
                self.makeXY(('render_x', 'render_y'), 's32')

        var = self.createVar('man_frames')         # Variable for manual entry of number of frames
        ttk.Checkbutton(self, text='Manual frame edit', command=self.checkAction, variable=var).pack(anchor=W)
        var = self.createVar('loop')
        ttk.Checkbutton(self, text='Loop', variable=var).pack(anchor=W)

        # setting defaults
        for var in ('active_frame', 'num_frames'):
            self.vars[var].set(1)
        self.vars['length'].set(100)
        self.vars['height'].set(15)
        self.vars['width'].set(10)

        action_frame = ttk.Frame(self)
        action_frame.pack(pady=5)
        ttk.Button(action_frame, text='Apply',
                   command=self.applyHandle, style='Action.TButton').pack(side=LEFT, padx=2)
        ttk.Button(action_frame, text='Preview',
                   command=self.preview, style='Action.TButton').pack(side=RIGHT, padx=2)

        self.checkAction()

    def applyHandle(self):
        if not self.controller.animationLoaded():
            showwarning(title='Warning', message='No Animation Loaded')
            return
        self.controller.apply()

    def preview(self):
        if not self.controller.animationLoaded():
            showwarning(title='Warning', message='No Animation Loaded')
            return
        PreviewWindow(self, self.controller)

    def checkAction(self):
        if self.vars['man_frames'].get():
            self.widgets['num_frames'].state(['disabled'])
            self.widgets['spacing'].state(['disabled'])
            self.widgets['active_frame'].state(['!disabled'])
        else:
            self.widgets['active_frame'].state(['disabled'])
            self.widgets['num_frames'].state(['!disabled'])
            self.widgets['spacing'].state(['!disabled'])


    def makeXY(self, var_names,cType):
        """
        Purpose: Makes cooridnate widgets
        """
        coord_frame = ttk.Frame(self)
        for var_name,display_name in zip(var_names, ('X', 'Y')):
            var = self.createVar(var_name)
            entry = EntryLabel(coord_frame, text=display_name, entry_variable=var, width=5, validate='key',
                               validatecommand=IntegerCheck(self, cType).vcmd)
            entry.pack(side=LEFT)
        coord_frame.pack()

    def createVar(self, name):
        """
        Purpose: Creates an IntVar, adds it to self.vars, and returns it
        Inputs:
            name: Name of variable in self.vars dict
        Output:
            Returns the variable
        """
        var = IntVar()
        self.vars[name] = var
        return var

    def apply(self):
        if not self.vars['man_frames'].get():
            self.vars['active_frame'].set(1)
        ind = self.vars['active_frame'].get()-1
        length, x, y, height, width, render_x, render_y, rotation = self.controller.getFrameInfo(ind)
        self.vars['x'].set(x)
        self.vars['y'].set(y)
        self.vars['width'].set(width)
        self.vars['height'].set(height)
        self.vars['length'].set(length)
        self.vars['rotation'].set(rotation)
        self.vars['render_x'].set(render_x)
        self.vars['render_y'].set(render_y)
        self.checkAction()


class IntegerCheck:
    def __init__(self, parent, intType):
        self.parent = parent
        if intType == 'u8':
            self.low = 0
            self.high = 256
        elif intType == 's8':
            self.low = -128
            self.high = 127
        elif intType == 'u16':
            self.low = 0
            self.high = 65535
        elif intType == 's16':
            self.low = -32768
            self.high = 32767
        elif intType == 'u32':
            self.low = 0
            self.high = 4294967295
        elif intType == 's32':
            self.low = -2147483648
            self.high = 2147483647
        else:
            raise Exception('Unknown type')
        self.vcmd = parent.register(self.inIntegerRange), '%d', '%P'

    def inIntegerRange(self, _type, afterText):
        """
        Validates an entry to make sure the correct text is being inputted
        :param type:        0 for deletion, 1 for insertion, -1 for focus in
        :param afterText:   The text that the entry will display if validated
        :return:
        """
        if _type == '0':
            return True
        elif _type == '1':
            try:
                num = int(afterText)
            except ValueError:
                if (self.low < 0) and (afterText == '-'):
                    return True
                else:
                    return False
            if (num >= self.low) and (num <= self.high):
                return True
        return False
