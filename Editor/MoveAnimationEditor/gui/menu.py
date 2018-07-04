from Editor.utilities.location_saver import save_location, load_locations, load_location
from Editor.signal import Signal

import os
import tkinter as tk
from tkinter.messagebox import showinfo, showerror, askokcancel, showwarning
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askopenfilename, asksaveasfilename
from guicomponents.simplesavemenu import SimpleSaveMenu

LOCATION_SAVE = 'move_animation_editor_save_path'
LOCATION_LOAD = 'move_animation_editor_load_path'
LOCATIONS_EXPORT = 'move_animation_editor_export_path_anim', 'move_animation_editor_export_path_texture'
LOCATION_ADD_IMAGE = 'move_animation_editor_load_image'


class EditorMenu(SimpleSaveMenu):
    def __init__(self, controller):
        SimpleSaveMenu.__init__(self, 'Animation', extension='devanim', file_type='Animation')
        self.signal_help = Signal()
        self.signal_about = Signal()

        self.controller = controller
        self.file_menu.add_command(label='Export', command=self.export)

        edit = tk.Menu(self, tearoff=0)
        edit.add_command(label='Change All Frame Lengths', command=self.change_all)
        edit.add_command(label='Shift All Frames', command=self.shift_all)
        self.add_cascade(label='Edit', menu=edit)

        animation = tk.Menu(self, tearoff=0)
        animation.add_command(label='Add Image', command=self._add_image)
        animation.add_command(label='Add Frame', command=self.controller.add_frame)
        animation.add_command(label='Insert Frame', command=self.controller.insert_frame)
        animation.add_command(label='Delete Frame', command=self.controller.delete_frame)
        self.add_cascade(label='Animation', menu=animation)

        help = tk.Menu(self, tearoff=0)
        help.add_command(label='Help Topics', command=self.signal_help)
        help.add_command(label='About', command=self.signal_about)
        self.add_cascade(label='Help', menu=help)

    def _add_image(self):
        path = askopenfilename(title='Load from?', initialdir=load_location(LOCATION_ADD_IMAGE))
        if path:
            name = os.path.split(path)[-1]
            if any(img.name == name for img in self.controller.animation.images):
                showwarning('Warning', 'Image with name "{}" has already been added'.format(name))
                return
            self.controller.add_image(path)
            save_location({LOCATION_ADD_IMAGE: os.path.split(path)[0]})

    def change_all(self):
        length = askinteger(title='Change Length', prompt="Choose a Length")
        if length:
            self.controller.change_all_length(length)

    def shift_all(self):
        x = askinteger(title='X-Shift', prompt='Choose x-shift amount')
        y = askinteger(title='Y-Shift', prompt='Choose y-shift amount')
        if (x is not None) and (y is not None):
            self.controller.shift_all(x, y)

    def export(self):
        anim_path = asksaveasfilename(title='Export Animation', initialdir=load_location(LOCATIONS_EXPORT[0]),
                                      defaultextension='anim', filetypes=[('Animation File', 'anim')])
        if not anim_path:
            return
        texture_path = asksaveasfilename(title='Export Sprite Sheet File',
                                         initialdir=load_location(LOCATIONS_EXPORT[0]),
                                         defaultextension='.png', filetypes=[('PNG', '.png')])
        if not texture_path:
            return
        try:
            self.controller.export(anim_path, texture_path)
            showinfo('Saved', 'Animation exported')
            save_location({LOCATIONS_EXPORT[0]: os.path.split(anim_path)[0],
                           LOCATIONS_EXPORT[1]: os.path.split(texture_path)[1]})
        except:
            showerror('Error', 'Animation not exported')
            raise
