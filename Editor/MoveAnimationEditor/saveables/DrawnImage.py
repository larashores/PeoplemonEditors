from Editor.saveable.composite import Composite
from Editor.saveable.saveableString import SaveableString
from Editor.saveable.saveableInt import saveable_int

from Editor.MoveAnimationEditor import utilities as util
from Editor.MoveAnimationEditor.saveables.AnimImage import AnimImage


from PIL import ImageTk, Image

import copy as cp


class DrawnImage(Composite):
    name = SaveableString
    x = saveable_int('s32')
    y = saveable_int('s32')
    width = saveable_int('u32')
    height = saveable_int('u32')
    rotation = saveable_int('u32')
    transparency = saveable_int('u8')
    crop_left = saveable_int('u8')
    crop_top = saveable_int('u8')
    crop_right = saveable_int('u8')
    crop_bottom = saveable_int('u8')

    def __init__(self, image=None):
        Composite.__init__(self)
        self.transparency = 255
        self.canvas = None
        self.scaled_img = None
        self.anim_img = None
        self.img_tk = None
        self.changed = False
        if image:
            self.set_image(image)
        self.register(self.item_changed)

        self.canvas_to_id = {}
        self.id_to_canvas = {}

    def item_changed(self, key):
        self.changed = True

    def copy(self):
        """
        Copies the image into a new image. Image file is shared

        pre-conditions: None
        post-conditions: New image object created

        return -> The new image object
        """
        new = Composite.copy(self)
        new.canvas = self.canvas
        new.anim_img = self.anim_img
        new.scaled_img = self.scaled_img
        return new

    def set_image(self, img):
        if not isinstance(img, AnimImage) and img is not None:
            raise ValueError('Cannot create DrawnImage with {}. Only AnimImages'.format(img))
        self.anim_img = img
        self.name = img.name

    def scale_max(self, canvas):
        """
        Scales the image to the largest size it can be to fit within the canvas

        pre-conditions: None
        post-conditions: Image scaled but not redrawn

        return -> None
        """
        im_width, im_height = self.anim_img.image.size
        width_ratio = im_width / canvas.winfo_width()
        height_ratio = im_height / canvas.winfo_height()
        ratio = max(width_ratio, height_ratio)

        self.width = int(im_width/ratio)
        self.height = int(im_height/ratio)

    def scale_original(self):
        """
        Sets the image back to the original scale

        pre-conditions: None
        post-conditions; Image scaled but not redrawn

        return -> None
        """
        self.width, self.height = self.anim_img.image.size

    def center(self, canvas):
        """
        Centers the Shape on the canvas

        pre-conditions: None
        post-conditions: Changes location of the Shape so it's centered

        return -> None
        """
        s_width, s_height = canvas.winfo_width(), canvas.winfo_height()
        self.x = int(s_width / 2 - self.width / 2)
        self.y = int(s_height / 2 - self.height / 2)

    def create_image(self):
        """
        Draws the Image on the canvas

        pre-conditions: Image is not already drawn on the canvas
        post-conditions: Image is drawn on the canvas

        return -> None
        """
        diagonal = int((self.width**2 + self.height**2)**.5)
        img = Image.new('RGBA', (diagonal, diagonal))

        orig_width, orig_height = self.anim_img.image.size
        left, upper, right, bottom = 0, 0, orig_width, orig_height
        if self.crop_left != 0 or self.crop_top != 0 or self.crop_right != 0 or self.crop_bottom != 0:
            left = int(orig_width * self.crop_left / 255)
            upper = int(orig_height * self.crop_top / 255)
            right = int(orig_width - (orig_width * self.crop_right / 255))
            bottom = int(orig_height - (orig_height * self.crop_bottom / 255))
            to_paste = self.anim_img.image.crop((left, upper, right, bottom))
        else:
            to_paste = self.anim_img.image
        scale_x, scale_y = self.width / orig_width, self.height / orig_height
        to_paste = to_paste.resize((int(to_paste.size[0]*scale_x), int(to_paste.size[1]*scale_y)), Image.ANTIALIAS)

        x_off = round((img.size[0]-to_paste.size[0])/2 + (left/2 - (orig_width-right)/2)*scale_x)
        y_off = round((img.size[1]-to_paste.size[1])/2 + (upper/2 - (orig_height-bottom)/2)*scale_y)
        img.paste(to_paste, (x_off,
                             y_off,
                             x_off+to_paste.size[0],
                             y_off+to_paste.size[1]))

        if self.transparency != 255:
            img_load = img.load()
            for row in range(img.size[0]):
                for col in range(img.size[1]):
                    pixel = img_load[row, col]
                    img_load[row, col] = pixel[0], pixel[1], pixel[2], int(pixel[3]*(self.transparency / 255))

        self.scaled_img = img.rotate(-self.rotation)
        self.img_tk = ImageTk.PhotoImage(img)
        self.changed = False

    def draw(self, canvas):
        if self.changed:
            self.create_image()
        _id = canvas.create_image(self.get_center(), image=self.img_tk, tags='drawn_image')
        self.canvas_to_id[canvas] = _id
        self.id_to_canvas[_id] = canvas
        return _id

    def get_center(self):
        """
        Gets the center point of the Shape (an integer)

        pre-conditions: None
        post-conditions: None

        return -> The center point of the Shape
        """
        return util.midpoint(self.x, self.y, self.x + self.width, self.y + self.height)

    def destroy(self, canvas):
        """
        Destroys the Image from the canvas

        pre-conditions: Image is drawn on the canvas
        post-conditions: Image is removed from the canvas

        return -> None
        """
        _id = self.canvas_to_id.pop(canvas)
        canvas.delete(_id)
        return _id

    def move(self, dx, dy):
        """
        Moves the Shape by the given offsets without redrawing

        dx -> The amount to move in the x-coordinate
        dy -> The amount to move in the y-direction

        pre-conditions: None
        post-conditions: The location of the Shape is changed

        return -> None
        """
        self.x += dx
        self.y += dy

    def get_id(self, canvas):
        return self.canvas_to_id[canvas]