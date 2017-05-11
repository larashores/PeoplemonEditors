from Editor.location_saver import save_location, load_locations, load_location

import os
import tkinter as tk
from tkinter.messagebox import showinfo, showerror, askokcancel
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askopenfilename, asksaveasfilename


LOCATION_SAVE = 'move_animation_editor_save_path'
LOCATION_LOAD = 'move_animation_editor_load_path'
LOCATIONS_EXPORT = 'move_animation_editor_export_path_anim', 'move_animation_editor_export_path_texture'


class EditorMenu(tk.Menu):
    def __init__(self, controller):
        tk.Menu.__init__(self)
        self.last_save_path = load_location(LOCATION_SAVE)
        self.last_load_path = load_location(LOCATION_LOAD)
        self.last_export_paths = load_locations(LOCATIONS_EXPORT)
        self.controller = controller
        file = tk.Menu(self, tearoff=0)
        file.add_command(label='New', command=self.new)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Export', command=self.export)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

        edit = tk.Menu(self, tearoff=0)
        edit.add_command(label='Change All Frame Lengths', command=self.change_all)
        edit.add_command(label='Shift All Frames', command=self.shift_all)
        self.add_cascade(label='Edit', menu=edit)

        animation = tk.Menu(self, tearoff=0)
        animation.add_command(label='Add Image', command=self.controller.add_image)
        animation.add_command(label='Add Frame', command=self.controller.add_frame)
        animation.add_command(label='Insert Frame', command=self.controller.insert_frame)
        animation.add_command(label='Delete Frame', command=self.controller.delete_frame)
        self.add_cascade(label='Animation', menu=animation)

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

    def save(self):
        path = asksaveasfilename(title='Save Animation', initialdir=load_location(LOCATION_SAVE),
                                 defaultextension='devanim', filetypes=[('Animation File', 'devanim')])
        if not path:
            return
        try:
            self.controller.save(path)
            save_location({LOCATION_SAVE: os.path.split(path)[0]})
        except:
            showerror('Error', 'Animation not saved')
            raise

    def load(self):
        path = askopenfilename(title='Load Animation', initialdir=load_location(LOCATION_LOAD),
                               defaultextension='devanim', filetypes=[('Animation File', 'devanim')])
        if not path:
            return
        try:
            file = open(path, 'rb')
            data = bytearray(file.read())
            file.close()
            self.controller.load(data, path)
            save_location({LOCATION_LOAD: os.path.split(path)[0]})
        except:
            showerror('Error', 'Animation not loaded')
            raise

    def new(self):
        answer = askokcancel(title='New Animation', message='Create New Animation?')
        if answer:
            self.controller.new()