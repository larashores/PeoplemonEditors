__author__ = 'Vincent'

from Editor.AnimationEditor.animation import Animation
import os

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

class Controller:
    def __init__(self):
        self.canvas = None
        self.last_frame = 0
        self.animation = Animation()
        self.texture = None
        self.apply_funcs = []
        self.last_visited = None

    def newSheet(self, imgpath):
        """
        Create a new sprite sheet image on the canvas
        """
        self.canvas.newSheet(imgpath)
        self.texture = os.path.split(imgpath)[1]

    def getFrameInfo(self, ind):
        frame = self.animation.frames[ind]
        return (frame.paramDict['length'], frame.paramDict['x'], frame.paramDict['y'], frame.paramDict['height'],
                frame.paramDict['width'], frame.paramDict['render_x'], frame.paramDict['render_y'],
                frame.paramDict['rotation'])

    def getNumberFrames(self):
        return len(self.animation.frames)

    def apply(self):
        if not self.animationLoaded():
            return
        vars = self.canvas.vars
        ind = vars['active_frame'].get()-1
        if vars['man_frames'].get():
            if ind == self.last_frame:
                self.animation.editFrame(ind, length=vars['length'].get(), width=vars['width'].get(),
                                         height=vars['height'].get(), x=vars['x'].get(), y=vars['y'].get(),
                                         render_x=vars['render_x'].get(), render_y=vars['render_y'].get(),
                                         rotation=vars['rotation'].get())
            else:
                self.last_frame = ind
        else:
            (num_frames, offset, length, width,
             height, x, y, render_x, render_y, rotation) = (vars['num_frames'].get(), vars['spacing'].get(),
                                                            vars['length'].get(), vars['width'].get(),
                                                            vars['height'].get(), vars['x'].get(), vars['y'].get(),
                                                            vars['render_x'].get(), vars['render_y'].get(),
                                                            vars['rotation'].get())
            self.animation.addAll(num_frames, (offset, 0), length, (x, y), width, height, (render_x, render_y),
                                  rotation)
        for func in self.apply_funcs:
            func()

    def save(self, path):
        self.animation.paramDict['loop'] = bool(self.canvas.vars['loop'].get())
        self.animation.paramDict['texture'] = self.texture
        data = self.animation.toByteArray()
        file = open(path, 'wb')
        file.write(data)
        file.close()

    def load(self, path):
        try:
            file = open(path, 'rb')
            data = bytearray(file.read())
            anim = self.animation.fromByteArray(data)
        except:
            showerror(title='Error', message='Error loading animation')
            return
        texture = anim.paramDict['texture']
        sheet_path = askopenfilename(title='Sprite sheet?', initialfile=texture, initialdir=self.last_visited)
        if sheet_path:
            try:
                self.last_visited = os.path.split(sheet_path)[0]
                self.newSheet(sheet_path)
            except:
                showerror(title='Error', message='Error loading Sprite sheet')
                return
        else:
            return
        self.animation = anim
        self.canvas.vars['active_frame'].set(1)
        self.canvas.vars['loop'].set(int(self.animation.paramDict['loop']))
        self.canvas.vars['man_frames'].set(1)
        self.canvas.vars['num_frames'].set(len(self.animation.frames))
        for func in self.apply_funcs:
            func()

    def changeScale(self, scale):
        self.canvas.changeScale(scale)

    def getScale(self):
        return self.canvas.scale

    def animationLoaded(self):
        if self.texture:
            return True
        else:
            return False

    def getSpriteSheet(self):
        return self.canvas.sheet