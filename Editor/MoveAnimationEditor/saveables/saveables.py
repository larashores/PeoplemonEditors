from Editor.saveable.composite import Composite
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.MoveAnimationEditor.saveables.Frame import Frame
from Editor.MoveAnimationEditor.saveables.AnimImage import AnimImage

import tkinter as tk
from tkinter import ttk


class AnimImageOld(Composite):
    name = SaveableString
    x = saveable_int('u32')
    y = saveable_int('u32')
    width = saveable_int('u32')
    height = saveable_int('u32')


class Animation(Composite):
    images = array(AnimImage)
    frames = array(Frame)

    def load_in_place(self, byte_array, pre_generate_images=False):
        Composite.load_in_place(self, byte_array)
        names_to_image = {}
        for anim_image in self.images:
            names_to_image[anim_image.name] = anim_image

        if pre_generate_images:
            window = tk.Toplevel()
            progress = ttk.Progressbar(window, orient=tk.HORIZONTAL,
                                       maximum=len(self.frames)-1,
                                       length=200,
                                       mode='determinate')

            ttk.Label(window, text='Loading Animation', style='Title.TLabel').pack()
            progress.pack(expand=tk.YES, fill=tk.X, padx=(10, 10), pady=(0, 10))
        for ind, frm in enumerate(self.frames):
            for drawn in frm.images:
                drawn.set_image(names_to_image[drawn.name])
            if pre_generate_images:
                frm.pre_generate_images()
                progress.step(1)
                window.update()
        if pre_generate_images:
            window.destroy()


class PieceExport(Composite):
    source_x = saveable_int('u32')
    source_y = saveable_int('u32')
    width = saveable_int('u32')
    height = saveable_int('u32')
    scale_x = saveable_int('u32')
    scale_y = saveable_int('u32')
    x_offset = saveable_int('s32')
    y_offset = saveable_int('s32')
    rotation = saveable_int('u32')
    transparency = saveable_int('u8')


class FrameExport(Composite):
    length = saveable_int('u32')
    pieces = array(PieceExport)


class AnimationExport(Composite):
    texture = SaveableString
    loop = saveable_int('u8')
    frames = array(FrameExport)


class AnimationOld(Composite):
    texture = SaveableString
    images = array(AnimImageOld)
    frames = array(Frame)



