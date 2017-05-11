import tkinter as tk
from tkinter.messagebox import showinfo, showerror, askokcancel
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askopenfilename, asksaveasfilename

import os

from Editor import structreader as sr
from Editor.location_saver import save_location, load_locations_new

LOCATIONS_SAVE = 'move_animation_editor_save_path_anim', 'move_animation_editor_save_path_texture'
LOCATIONS_LOAD = 'move_animation_editor_load_path_anim', 'move_animation_editor_load_path_texture'
LOCATIONS_EXPORT = 'move_animation_editor_export_path_anim', 'move_animation_editor_export_path_texture'


class EditorMenu(tk.Menu):
    def __init__(self, controller):
        tk.Menu.__init__(self)
        self.last_save_path = load_locations_new(LOCATIONS_SAVE)
        self.last_load_path = load_locations_new(LOCATIONS_LOAD)
        self.last_export_path = load_locations_new(LOCATIONS_EXPORT)
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

    def get_paths(self, animation_type, last_paths, last_path_names, verb, texture=True):
        last_paths.clear()
        last_paths.extend(load_locations_new(last_path_names))
        path_dict = {}
        anim_path = asksaveasfilename(title=verb+' Animation File', initialdir=os.path.split(last_paths[0])[0],
                                      defaultextension=animation_type, filetypes=[('Animation File', animation_type)])
        if not anim_path:
            raise ValueError("Path not chosen")
        path_dict[last_path_names[0]] = anim_path
        self.controller.last_anim_path = os.path.splitext(anim_path)[0]
        texture_path = asksaveasfilename(title=verb+' Sprite Sheet File', initialdir=os.path.split(last_paths[1])[0],
                                         defaultextension='.png', filetypes=[('PNG', '.png')])
        if not texture_path:
            save_location(path_dict)
            raise ValueError("Path not chosen")
        path_dict[last_path_names[1]] = texture_path
        save_location(path_dict)
        self.controller.last_texture_path = os.path.splitext(texture_path)[0]
        return anim_path, texture_path

    def get_path(self, animation_type, last_paths, last_path_names, verb, texture=True):
        last_paths.clear()
        last_paths.extend(load_locations_new(last_path_names))
        path_dict = {}
        anim_path = asksaveasfilename(title=verb+' Animation File', initialdir=os.path.split(last_paths[0])[0],
                                      defaultextension=animation_type, filetypes=[('Animation File', animation_type)])
        if not anim_path:
            raise ValueError("Path not chosen")
        path_dict[last_path_names[0]] = anim_path
        self.controller.last_anim_path = os.path.splitext(anim_path)[0]
        save_location(path_dict)
        return anim_path

    def save(self):
        try:
            anim_path = self.get_path('.devanim', self.last_save_path, LOCATIONS_SAVE, 'Save')
            self.controller.save(anim_path)
            showinfo('Saved', 'Animation saved')
        except:
            showerror('Error', 'Animation not saved')
            raise

    def export(self):
        try:
            anim_path, texture_path = self.get_paths('.anim', self.last_export_path, LOCATIONS_EXPORT, 'Export')
            self.controller.export(anim_path, texture_path)
            showinfo('Saved', 'Animation saved')
        except ValueError:
            return
        except:
            showerror('Error', 'Animation not saved')

    def load(self):
        self.last_load_path = load_locations_new(LOCATIONS_LOAD)
        location_dict = {}
        anim_path = askopenfilename(title='Load Animation File', initialdir=self.last_load_path[0],
                                    defaultextension='.devanim', filetypes=[('Animation File', '.devanim')])
        if not anim_path:
            return
        location_dict[LOCATIONS_LOAD[0]] = anim_path
        try:
            file = open(anim_path, 'rb')
            data = bytearray(file.read())
            file.close()
            self.controller.load(data, anim_path)
        except:
            showerror('Error', 'Animation not loaded')
            raise
        save_location(location_dict)

    def new(self):
        answer = askokcancel(title='New Animation', message='Create New Animation?')
        if answer:
            self.controller.new()