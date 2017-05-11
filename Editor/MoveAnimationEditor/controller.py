__author__ = 'Vincent'
import numpy as np

from tkinter.filedialog import askopenfilename
import MoveAnimationEditor.structreader as sr
import os
from PIL import Image
from MoveAnimationEditor.gui.point import Point

from Editor.MoveAnimationEditor.saveables.saveables import Animation
from Editor.MoveAnimationEditor.saveables.DrawnImage import DrawnImage
from Editor.MoveAnimationEditor.saveables.Frame import Frame
from Editor.MoveAnimationEditor.saveables.saveables import AnimImage
from Editor.MoveAnimationEditor.runtime_models.EditorModel import EditorModel


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
        self.editor.images.sort(key=lambda image: image.img.size[1], reverse=True)
        max_height = self.editor.images[0].img.size[1] if len(self.editor.images) != 0 else 1
        total_width = 0 if len(self.editor.images) != 0 else 1
        for img in self.editor.images:
            total_width += img.img.size[0]

        sheet = Image.new('RGBA', (total_width, max_height))

        locations = {}
        cur_width = 0
        for image in self.editor.images:
            width, height = image.img.size
            locations[image.name] = (cur_width, 0, width, height)
            box = (cur_width, 0, cur_width + width, height)
            sheet.paste(image.img, box)
            cur_width += image.img.size[0]

        sheet.save(texture_path)
        return locations

    def save(self, animation_path):
        data = self.animation.to_byte_array()

        file = open(animation_path, 'wb')
        file.write(data)
        file.close()
        self.editor.winfo_toplevel().wm_title("Move Animation Editor | {}".format(animation_path))

    def export(self, animation_path, texture_path):
        print('exporting ', animation_path, texture_path)
        locations = self.save_sprite_sheet(texture_path)

        data = bytearray()
        sr.pack(data, os.path.split(texture_path)[-1], 'str')
        sr.pack(data, 0, 'u8')
        sr.pack(data, len(self.editor.frames), 'u16')
        for frame in self.editor.frames:
            sr.pack(data, frame.length, 'u32')

            if len(frame.images) == 0:
                sr.pack(data, 1, 'u16')
                sr.pack(data, 0, 'u32')
                sr.pack(data, 0, 'u32')
                sr.pack(data, 0, 'u32')
                sr.pack(data, 0, 'u32')
                sr.pack(data, 100, 'u32')
                sr.pack(data, 100, 'u32')
                sr.pack(data, 0, 's32')
                sr.pack(data, 0, 's32')
                sr.pack(data, 0, 'u32')
                sr.pack(data, 255, 'u8')
                continue

            sr.pack(data, len(frame.images), 'u16')
            for image in frame.images:
                orig_width, orig_height = image.img.size                   # Width and height of loaded image

                image_offset_left = image.crop_limits[0]*orig_width        # How much displaced from left
                image_offset_top = image.crop_limits[1]*orig_height        # Displacement from top
                image_offset_right = image.crop_limits[2]*orig_width       # Displacement from right
                image_offset_bottom = image.crop_limits[3]*orig_height     # Displacement from bottom

                start_x = locations[image.name][0]                         # X location of image in sprite sheet
                start_y = locations[image.name][1]                         # Y location
                scale_x = (orig_width / image.width) * 100                 # X scaling for image
                scale_y = (orig_height / image.height) * 100               # Y scaling for image

                x = start_x + image_offset_left                            # X position to start in sprite sheet
                y = start_y + image_offset_top                             # Y position
                width = orig_width - image_offset_right - image_offset_left     # Width to grab from sprite sheet
                height = orig_height - image_offset_bottom - image_offset_top   # Height to grab

                rotation = image.rotation                                  # Image rotation
                transparency = image.transparency * 255                    # Image transparency

                # Get offsets
                top_left = Point(image.location[0] + image_offset_left, image.location[1] + image_offset_top)
                bottom_right = Point(top_left.x + width, top_left.y + height)
                image_center = Point(*image.get_center())                  # Rotation point of image
                cropped_center = top_left.midpoint(bottom_right)           # Rotation point of cropped image

                top_left.rotate(image_center, rotation)
                cropped_center.rotate(image_center, rotation)
                top_left.rotate(cropped_center, -rotation)
                offset_x = top_left.x
                offset_y = top_left.y

                rounded = lambda num: int(round(num))
                sr.pack(data, rounded(x), 'u32')
                sr.pack(data, rounded(y), 'u32')
                sr.pack(data, rounded(width), 'u32')
                sr.pack(data, rounded(height), 'u32')
                sr.pack(data, rounded(scale_x), 'u32')
                sr.pack(data, rounded(scale_y), 'u32')
                sr.pack(data, rounded(offset_x), 's32')
                sr.pack(data, rounded(offset_y), 's32')
                sr.pack(data, rounded(rotation), 'u32')
                sr.pack(data, rounded(transparency), 'u8')

        file = open(animation_path, 'wb')
        file.write(data)
        file.close()

    def load(self, anim_data, anim_path):
        self.animation.load_in_place(anim_data, True)

        self.editor_model.current_frame = 0
        self.editor.selected = None
        self.editor.outline = None
        self.editor.winfo_toplevel().wm_title("Move Animation Editor | {}".format(anim_path))

    def convert_all(self, path):
        import os
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    if int(os.path.split(root)[-1]) <= 92:
                        continue
                except:
                    pass
                if file.endswith('devanim'):
                    self.convert_devanim(os.path.join(root, file),
                                         os.path.join(root, 'spritesheet.png'))

    def convert_devanim(self, anim_path, text_path):
        file = open(anim_path, 'rb')
        data = bytearray(file.read())
        texture_name = sr.unpack(data, 'str')
        print('loading ', anim_path, text_path)
        try:
            self.load(data, anim_path, text_path)
            print('loaded')
            self.export(os.path.splitext(anim_path)[0] + '.anim',
                    text_path)
        except:
            print('Didnt work')

    def change_all_length(self, length):
        for frame in self.editor.frames:
            frame.length = length

    def shift_all(self, x, y):
        print('shifting')
        for frame in self.editor.frames:
            for img in frame.images:
                img.location.x += x
                img.location.y += y
        self.editor.handle_frame(None)
