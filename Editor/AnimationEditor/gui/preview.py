__author__ = 'Vincent'

from tkinter import *

from Editor.AnimationEditor.gui.changeScale import askChange
from Editor.AnimationEditor.gui.frameViewer import FrameCanvas
import os

class EditorMenu(Menu):
    def __init__(self, frameViewer):
        Menu.__init__(self)
        self.viewer = frameViewer
        edit = Menu(self, tearoff=0)
        edit.add_command(label='Change Scale', command=self.changeScale)
        self.add_cascade(label='Edit', menu=edit)

    def changeScale(self):
        scale = askChange(self.viewer.scale)
        if scale:
            self.viewer.scale = scale
            if self.viewer.loaded:
                self.viewer.apply()

class PreviewWindow(Toplevel):
    def __init__(self, parent, controller):
        """

        :param parent: The parent widget
        :return:
        """
        Toplevel.__init__(self, parent)
        self.title('Animation Preview')
        self.cur_frame = IntVar()
        self.viewer = FrameCanvas(self, controller, self.cur_frame)
        self.viewer.pack(padx=(5, 5), pady=(0, 5))
        self.viewer.apply()

        self.config(menu=EditorMenu(self.viewer))

        ind = self.cur_frame.get()
        length = self.viewer.images[ind][1]
        self.after(length, self.nextImage)
        self.iconbitmap(os.path.join('resources\\editor.ico'))


    def nextImage(self):
        ind = self.cur_frame.get()-1
        length = self.viewer.images[ind][1]
        self.viewer.next()
        self.after(length, self.nextImage)
