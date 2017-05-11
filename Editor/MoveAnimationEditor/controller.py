from Editor.MoveAnimationEditor.gui.point import Point
from Editor.MoveAnimationEditor.runtime_models.EditorModel import EditorModel
from Editor.MoveAnimationEditor.saveables.Frame import Frame
from Editor.MoveAnimationEditor.saveables.saveables import Animation, AnimImage
from Editor.MoveAnimationEditor.saveables.saveables import AnimationExport, FrameExport, PieceExport

import os
from PIL import Image
from tkinter.filedialog import askopenfilename
from tkinter import ttk
import tkinter as tk


class Controller:
    def __init__(self):
        self.last_path = None
        self.last_anim_path = None
        self.last_texture_path = None
        self.editor = None
        self.animation = Animation()
        self.editor_model = EditorModel()
        self.animation.frames.append(Frame())

    def add_image(self):
        path = askopenfilename(title='Load from?', initialdir=self.last_path)
        if path:
            self.last_path = path
            file = open(path, 'rb')
            image = Image.open(file)
            anim_image = AnimImage()
            anim_image.image = image
            anim_image.name = os.path.split(path)[-1]
            self.animation.images.append(anim_image)

    def add_frame(self):
        self.animation.frames.append(self.animation.frames[-1].copy())
        self.editor_model.current_frame = len(self.animation.frames) - 1

    def insert_frame(self):
        ind = self.editor_model.current_frame
        new_frame = self.animation.frames[ind].copy() if ind != 0 else Frame()
        self.animation.frames.insert(ind, new_frame)
        self.editor_model.current_frame = self.editor_model.current_frame

    def delete_frame(self):
        if len(self.animation.frames) == 1:
            return
        self.animation.frames.pop(self.editor_model.current_frame)
        next_ind = self.editor_model.current_frame
        if next_ind >= len(self.animation.frames):
            next_ind -= 1
        self.editor_model.current_frame = next_ind

    def new(self):
        self.animation.images.clear()
        self.animation.frames.clear()
        self.animation.frames.append(Frame())
        self.editor_model.current_frame = 0
        self.editor.winfo_toplevel().wm_title("Move Animation Editor")

    def save_sprite_sheet(self, texture_path):
        all_images = sorted(self.animation.images, key=lambda anim_img: anim_img.image.size[1], reverse=True)
        max_height = all_images[0].image.size[1] if len(all_images) != 0 else 1
        total_width = 0 if len(all_images) != 0 else 1
        for img in all_images:
            total_width += img.image.size[0]
        sheet = Image.new('RGBA', (total_width, max_height))

        locations = {}
        cur_width = 0
        for img in all_images:
            width, height = img.image.size
            locations[img.name] = (cur_width, 0, width, height)
            box = (cur_width, 0, cur_width + width, height)
            sheet.paste(img.image, box)
            cur_width += img.image.size[0]
        sheet.save(texture_path)

        return locations

    def export(self, animation_path, texture_path):
        locations = self.save_sprite_sheet(texture_path)

        names_to_anim_image = {}
        for anim_image in self.animation.images:
            names_to_anim_image[anim_image.name] = anim_image

        export = AnimationExport()
        export.loop = 0

        for frame in self.animation.frames:
            new_frame = FrameExport()
            new_frame.length = frame.length
            export.frames.append(new_frame)
            if len(frame.images) == 0:
                new_image = PieceExport()
                new_image.scale_x = 100
                new_image.scale_y = 100
                new_image.transparency = 255
                continue
            for drawn_img in frame.images:
                img = names_to_anim_image[drawn_img.name]
                orig_width, orig_height = img.image.size  # Width and height of loaded image

                image_offset_left = drawn_img.crop_left*orig_width / 255        # How much displaced from left
                image_offset_top = drawn_img.crop_top*orig_height / 255        # Displacement from top
                image_offset_right = drawn_img.crop_right*orig_width / 255       # Displacement from right
                image_offset_bottom = drawn_img.crop_bottom*orig_height / 255     # Displacement from bottom

                start_x = locations[drawn_img.name][0]                         # X location of image in sprite sheet
                start_y = locations[drawn_img.name][1]                         # Y location
                scale_x = (orig_width / drawn_img.width) * 100                 # X scaling for image
                scale_y = (orig_height / drawn_img.height) * 100               # Y scaling for image

                x = start_x + image_offset_left                            # X position to start in sprite sheet
                y = start_y + image_offset_top                             # Y position
                width = orig_width - image_offset_right - image_offset_left     # Width to grab from sprite sheet
                height = orig_height - image_offset_bottom - image_offset_top   # Height to grab

                rotation = drawn_img.rotation                                  # Image rotation
                transparency = drawn_img.transparency                          # Image transparency

                # Get offsets
                top_left = Point(drawn_img.x + image_offset_left, drawn_img.y + image_offset_top)
                bottom_right = Point(top_left.x + width, top_left.y + height)
                image_center = Point(*drawn_img.get_center())                  # Rotation point of image
                cropped_center = top_left.midpoint(bottom_right)           # Rotation point of cropped image

                top_left.rotate(image_center, rotation)
                cropped_center.rotate(image_center, rotation)
                top_left.rotate(cropped_center, -rotation)
                offset_x = top_left.x
                offset_y = top_left.y

                rounded = lambda num: int(round(num))

                new_image = PieceExport()
                new_image.source_x = rounded(x)
                new_image.source_y = rounded(y)
                new_image.width = rounded(width)
                new_image.height = rounded(height)
                new_image.scale_x = rounded(scale_x)
                new_image.scale_y = rounded(scale_y)
                new_image.x_offset = rounded(offset_x)
                new_image.y_offset = rounded(offset_y)
                new_image.rotation = rounded(rotation)
                new_image.transparency = rounded(transparency)
                new_frame.pieces.append(new_image)

        file = open(animation_path, 'wb')
        file.write(export.to_byte_array())
        file.close()

    def load(self, anim_data, anim_path):
        self.animation.load_in_place(anim_data, True)


        self.editor_model.current_frame = 0
        self.editor.selected = None
        self.editor.outline = None
        self.editor.winfo_toplevel().wm_title("Move Animation Editor | {}".format(anim_path))

    def save(self, animation_path):
        data = self.animation.to_byte_array()

        file = open(animation_path, 'wb')
        file.write(data)
        file.close()
        self.editor.winfo_toplevel().wm_title("Move Animation Editor | {}".format(animation_path))

    def change_all_length(self, length):
        for frame in self.animation.frames:
            frame.length = length

    def shift_all(self, x, y):
        for frame in self.animation.frames:
            for img in frame.images:
                img.x += x
                img.y += y
        self.editor_model.current_frame = self.editor_model.current_frame
