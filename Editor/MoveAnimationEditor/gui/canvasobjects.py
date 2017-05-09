from MoveAnimationEditor.gui.point import Point
from abc import ABCMeta, abstractmethod

from PIL import Image, ImageTk

import copy as cp
import MoveAnimationEditor.rotation as rt
import numpy as np


class Shape:
    """
    Represents any shape drawn on the canvas
    """
    __metaclass__ = ABCMeta

    def __init__(self, canvas):
        self.location = Point(0, 0)     # The top-left corner of the non-rotated image
        self.width, self.height = 0, 0  # The width and height of the bounding box of the Shape
        self.rotation = 0               # The degrees a Shape is rotated clockwise
        self.transparency = 1           # The transparency of a Shape. Zero is fully transparent and 1 is opaque
        self.canvas = canvas            # The canvas that the Shape belongs to

    def get_bound(self):
        """
        Gets the bounding box of the Shape

        pre-conditions: None
        post-conditions: None

        return -> The bounding box
        """
        return self.location.x, self.location.y, self.location.x+self.width, self.location.y+self.height

    def get_center(self):
        """
        Gets the center point of the Shape (an integer)

        pre-conditions: None
        post-conditions: None

        return -> The center point of the Shape
        """
        return Point(self.location.x+(self.get_width()//2), self.location.y+(self.get_height()//2))

    def get_width(self):
        """
        Gets the width of the shape

        pre-conditions: None
        post-conditions: None

        return -> The width of the Shape
        """
        return self.width

    def get_height(self):
        """
        Gets the height of the shape

        pre-conditions: None
        post-conditions: None

        return -> The height of the Shape
        """
        return self.height

    def center(self):
        """
        Centers the Shape on the canvas

        pre-conditions: None
        post-conditions: Changes location of the Shape so it's centered

        return -> None
        """
        s_width, s_height = self.canvas.winfo_width(), self.canvas.winfo_height()
        self.location = Point(s_width/2 - self.width/2, s_height/2 - self.height/2)

    def move(self, dx, dy):
        """
        Moves the Shape by the given offsets without redrawing

        dx -> The amount to move in the x-coordinate
        dy -> The amount to move in the y-direction

        pre-conditions: None
        post-conditions: The location of the Shape is changed

        return -> None
        """
        self.location += (dx, dy)

    @abstractmethod
    def draw(self):
        """
        Draws the Shape on the canvas

        pre-conditions: Shape is not already drawn on the canvas
        post-conditions: Shape is drawn on the canvas

        return -> None
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Destroys the Shape from the canvas

        pre-conditions: Shape is drawn on the canvas
        post-conditions: Shape is removed from the canvas

        return -> None
        """
        pass


def PrintAttributeAccess(*, gets=[], sets=[]):
    def _PrintAttributeAccess(cls):
        class Wrapper(cls):
            """Example of overloading __getatr__ and __setattr__
            This example creates a dictionary where members can be accessed as attributes
            """
            def __init__(self, *args, **kwargs):
                cls.__init__(self, *args, **kwargs)
                cls.__setattr__(self, 'gets', gets)
                cls.__setattr__(self, 'sets', sets)

            def __getattribute__(self, name):
                """Maps values to attributes.
                Only called if there *isn't* an attribute with this name
                """
                to_print = gets == "all" or name in gets
                if to_print:
                    print("Getting '{}' of <0x{:04X}>".format(name, id(self)), end='')
                try:
                    attr = cls.__getattribute__(self, name)
                except AttributeError:
                    if to_print:
                        print("")
                    raise
                if to_print:
                    print(", value={}".format(attr))
                return attr

            def __setattr__(self, name, value):
                """Maps attributes to values.
                Only if we are initialised
                """
                to_print = sets is "all" or name in sets
                if to_print:
                    print("Setting '{}' of <0x{:04X}>, value={}".format(name, id(self), value))
                cls.__setattr__(self, name, value)
        return Wrapper
    return _PrintAttributeAccess


@PrintAttributeAccess(sets=['center_clicked'])
class Outline(Shape):
    """
    The outline that surrounds a shape
    """
    TOP_LEFT = 1
    TOP_RIGHT = 2
    BOTTOM_LEFT = 3
    BOTTOM_RIGHT = 4
    LEFT = 1
    TOP = 2
    RIGHT = 3
    BOTTOM = 4


    def __init__(self, canvas, image):
        Shape.__init__(self, canvas)
        self.image = image              # The CanvasImage object
        self.canvas = canvas
        self.rotation = image.rotation

        location = image.location
        self.location = image.location
        self.top_left = Point(location.x, location.y)
        self.top_right = Point(location.x + image.width, location.y)
        self.bottom_left = Point(location.x, location.y + image.height)
        self.bottom_right = Point(location.x + image.width, location.y + image.height)

        self.width, self.height = self.get_width(), self.get_height()
        self.ids = []

        self.last_pos = Point(0, 0)
        self.center_clicked = False
        self.resize_clicked = None
        self.rotate_clicked = False
        self.crop_clicked = None

    def draw(self):
        """
        Draws the Outline on the canvas

        pre-conditions: Outline is not already drawn on the canvas
        post-conditions: Outline is drawn on the canvas

        return -> None
        """
        center = self.get_center()

        # -------------Make mover----------------
        coords = center.x - 10, center.y - 10, center.x + 10, center.y + 10
        mover = self.canvas.create_oval(coords, fill='grey')
        self.canvas.tag_bind(mover, '<Button-1>', self.on_translate_click)
        self.ids.append(mover)
        # ---------------------------------------

        # ------------Make crop outline-------------------
        limits = self.image.crop_limits
        left = limits[0] * self.get_width()
        upper = limits[1] * self.get_height()
        right = limits[2] * self.get_width()
        bottom = limits[3] * self.get_height()
        top_left_crop = self.top_left + (left, upper)
        top_right_crop = self.top_right + (-right, upper)
        bottom_left_crop = self.bottom_left + (left, -bottom)
        bottom_right_crop = self.bottom_right + (-right, -bottom)
        for point in top_left_crop, top_right_crop, bottom_left_crop, bottom_right_crop:
            point.set(*rt.rotation(point.x, point.y, self.get_center(), self.rotation))
        for coord1, coord2 in ((top_left_crop, top_right_crop), (top_right_crop, bottom_right_crop),
                               (bottom_right_crop, bottom_left_crop), (bottom_left_crop, top_left_crop)):
            self.ids.append(self.canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y, fill='red'))
        # -------------------------------------------------

        # -------------Make bounding box--------------
        rotated = []
        for coord in self.top_left, self.top_right, self.bottom_left, self.bottom_right:
            rotated.append(Point(*rt.rotation(coord.x, coord.y, center, self.rotation)))
        top_left = rotated[0]
        top_right = rotated[1]
        bottom_left = rotated[2]
        bottom_right = rotated[3]

        for coord1, coord2 in ((top_left, top_right), (top_right, bottom_right),
                               (bottom_right, bottom_left), (bottom_left, top_left)):
            ln = self.canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y)
            self.canvas.tag_bind(ln, '<Button-1>', self.on_translate_click)
            self.ids.append(ln)
        # ---------------------------------------------

        # --------------------Make resizers-------------------------
        corners = zip((Outline.TOP_LEFT, Outline.TOP_RIGHT, Outline.BOTTOM_LEFT, Outline.BOTTOM_RIGHT),
                      rotated)
        for location, coords in corners:
            circ_coords = coords.x - 5, coords.y - 5, coords.x + 5, coords.y + 5
            resizer = self.canvas.create_oval(circ_coords, fill='blue')
            self.canvas.tag_bind(resizer, '<Button-1>',
                                 lambda event, location=location: self.on_resize_click(event, location))
            self.ids.append(resizer)
        # -----------------------------------------------------------

        # ------------------------Make rotator---------------------------
        start_point = top_left.midpoint(top_right)
        end_point = start_point + Point(np.sin(np.deg2rad(self.rotation)), -np.cos(np.deg2rad(self.rotation))) * 25

        self.ids.append(self.canvas.create_line(start_point.x, start_point.y, end_point.x, end_point.y))
        rotator_coords = end_point.x - 7.5, end_point.y - 7.5, end_point.x + 7.5, end_point.y + 7.5
        rotator = self.canvas.create_oval(rotator_coords, fill='green')
        self.canvas.tag_bind(rotator, '<Button-1>', self.on_rotate_click)
        self.ids.append(rotator)
        # ----------------------------------------------------------------

        # ---------------Make crop circles----------------
        mid1 = top_left_crop.midpoint(top_right_crop)
        mid2 = top_right_crop.midpoint(bottom_right_crop)
        mid3 = bottom_right_crop.midpoint(bottom_left_crop)
        mid4 = bottom_left_crop.midpoint(top_left_crop)
        for location, point in (Outline.LEFT, mid4), (Outline.TOP, mid1), (Outline.RIGHT, mid2), (Outline.BOTTOM, mid3):
            id = self.canvas.create_oval(point.x-3, point.y-3, point.x+3, point.y+3, fill='red')
            self.canvas.tag_bind(id, '<Button-1>',
                                 lambda event, location=location: self.on_crop_click(event, location))
            self.ids.append(id)
        # ------------------------------------------------

        self.canvas.bind('<B1-Motion>', self.handle_move)
        self.canvas.bind('<ButtonRelease-1>', self.on_left_release)

    def get_width(self):
        """
        Gets the width of the shape

        pre-conditions: None
        post-conditions: None

        return -> The width of the Shape
        """
        return self.top_left.distance_to(self.top_right)

    def get_height(self):
        """
        Gets the height of the shape

        pre-conditions: None
        post-conditions: None

        return -> The height of the Shape
        """
        return self.top_left.distance_to(self.bottom_left)

    def get_center(self):
        """
        Gets the center point of the Shape (an integer)

        pre-conditions: None
        post-conditions: None

        return -> The center point of the Shape
        """
        return self.top_left.midpoint(self.bottom_right)

    def destroy(self):
        """
        Destroys the Shape from the canvas

        pre-conditions: Shape is drawn on the canvas
        post-conditions: Shape is removed from the canvas

        return -> None
        """
        for _id in self.ids:
            self.canvas.delete(_id)
        self.ids.clear()

    def on_resize_click(self, event, location):
        """
        Event handler for clicking a resize button

        event ----> The event object
        location -> Which resizer was clicked

        pre-conditions: None
        post-conditions: Current resizer clicked changed

        return -> None
        """
        self.resize_clicked = location

    def on_rotate_click(self, event):
        """
        Event handler for clicking the rotator button

        event ----> The event object

        pre-conditions: None
        post-conditions: Rotate_clicked flag set

        return -> None
        """
        self.rotate_clicked = True

    def on_translate_click(self, event):
        """
        Event handler for clicking the translate button

        event ----> The event object

        pre-conditions: None
        post-conditions: center_clicked flag set
                         last_pos set to point of event

        return -> None
        """
        print('center clicked')
        self.last_pos = Point(event.x, event.y)
        self.center_clicked = True

    def on_crop_click(self, event, location):
        """
        Event handler for clicking a crop button

        event ----> The event object
        location -> Which crop button was clicked

        pre-conditions: None
        post-conditions: Current crop button clicked changed

        return -> None
        """
        self.crop_clicked = location

    def redraw(self):
        """
        Redraws both the outline and the image

        pre-conditions: None
        post-conditions: Images redrawn

        return -> None
        """
        self.destroy()
        self.image.destroy()
        self.image.draw()
        self.draw()

    def handle_move(self, event):
        """
        Handler for moving the mouse. Dispatches control to appropriate function

        event -> The event object

        pre-conditions: None
        post-conditions: Appropriate move action taken

        return -> None
        """
        print(self.center_clicked)
        if self.center_clicked:
            self.on_translate(event)
        elif self.resize_clicked:
            self.on_resize(event)
        elif self.rotate_clicked:
            self.on_rotate(event)
        elif self.crop_clicked:
            self.on_crop(event)

    def on_translate(self, event):
        """
        Handles translation of the outline and image together

        event -> The event object

        pre-conditions: Mouse is over translate button and clicked
        post-conditions: Outline and image moved to new location

        return -> None
        """
        print('translating')
        x = event.x - self.last_pos[0]
        y = event.y - self.last_pos[1]
        self.move(x, y)
        self.image.move(x, y)
        self.last_pos = Point(event.x, event.y)
        self.redraw()

    def on_resize(self, event):
        """
        Handles resizing of the outline and image together

        event -> The event object

        pre-conditions: Mouse is over resize button and clicked
        post-conditions: Outline and image resized

        return -> None
        """
        center = self.get_center().as_tuple()
        x, y = self.top_left.x, self.top_left.y
        event_x, event_y = rt.rotation(event.x, event.y, center, -self.rotation)
        width, height = self.get_width(), self.get_height()

        if self.resize_clicked == Outline.TOP_LEFT:
            width = x - event_x + width
            height = y - event_y + height
            x = event_x
            y = event_y
            lock = self.bottom_right
        elif self.resize_clicked == Outline.TOP_RIGHT:
            width = event_x - x
            height = y - event_y + height
            y = event_y
            lock = self.bottom_left
        elif self.resize_clicked == Outline.BOTTOM_LEFT:
            width = x - event_x + width
            height = event_y - y
            x = event_x
            lock = self.top_right
        elif self.resize_clicked == Outline.BOTTOM_RIGHT:
            width = event_x - x
            height = event_y - y
            lock = self.top_left
        else:
            raise Exception('Incorrect resizer clicked')
        width = 1 if width < 0 else width
        height = 1 if height < 0 else height

        old = lock.copy()
        self.top_left.set(x, y)
        self.top_right.set(x+width, y)
        self.bottom_left.set(x, y+height)
        self.bottom_right.set(x+width, y+height)

        dif = Point(*rt.rotation(lock.x, lock.y, self.get_center(), self.rotation)) - \
            Point(*rt.rotation(old.x, old.y, center, self.rotation))
        # Adjust for center being different
        self.top_left -= dif
        self.top_right -= dif
        self.bottom_left -= dif
        self.bottom_right -= dif

        self.location = Point(x, y)
        self.width, self.height = self.get_width(), self.get_height()

        self.image.location = self.location
        self.image.width = self.get_width()
        self.image.height = self.get_height()
        self.image.destroy()
        self.destroy()
        self.image.draw()
        self.draw()

    def on_rotate(self, event):
        """
        Handles rotating of the outline and image together

        event -> The event object

        pre-conditions: Mouse is over rotate button and clicked
        post-conditions: Outline and image rotated

        return -> None
        """
        center = self.get_center()
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        try:
            self.rotation = np.rad2deg(np.arctan((x - center.x) / (center.y - y)))
        except ZeroDivisionError:
            if event.x - center.x >= 0:
                self.rotation = 90
            else:
                self.rotation = -90
        print(self.rotation)
        if y > center.y:
            self.rotation -= 180
        self.rotation %= 360

        self.image.set_rotation(self.rotation)
        self.redraw()

    def on_crop(self, event):
        """
        Handles cropping of the outline and image together

        event -> The event object

        pre-conditions: Mouse is over crop button and clicked
        post-conditions: Outline and image cropped

        return -> None
        """
        center = self.get_center().as_tuple()
        x, y = self.top_left.x, self.top_left.y
        event_x, event_y = rt.rotation(self.canvas.canvasx(event.x),
                                       self.canvas.canvasy(event.y),
                                       center, -self.rotation)
        width, height = self.get_width(), self.get_height()
        if self.crop_clicked == Outline.TOP:
            if event_y < y:
                amount = 0
            elif event_y > (y + height):
                amount = height
            else:
                amount = event_y - y
            amount /= height

        elif self.crop_clicked == Outline.RIGHT:
            if event_x > self.top_right.x:
                amount = 0
            elif event_x < self.top_left.x:
                amount = width
            else:
                amount = width - (event_x - x)
            amount /= width

        elif self.crop_clicked == Outline.BOTTOM:
            if event_y < y:
                amount = height
            elif event_y > y + height:
                amount = 0
            else:
                amount = height - (event_y - y)
            amount /= height

        elif self.crop_clicked == Outline.LEFT:
            if event_x < x:
                amount = 0
            elif event_x > x + width:
                amount = width
            else:
                amount = event_x - x
            amount /= width

        else:
            raise Exception('Incorrect crop set')

        opposite = self.image.crop_limits[(self.crop_clicked - 3) % 4]
        if opposite + amount > 1:   # Cannot crop into negative
            amount = 1 - opposite
        self.image.crop_limits[self.crop_clicked - 1] = amount

        self.redraw()

    def on_left_release(self, event):
        """
        Handles releasing the mouse button. Turns all clicked flags off

        pre-conditions: None
        post-conditions: All clicked flags turned off

        return -> None
        """
        print('release')
        self.center_clicked = False
        self.resize_clicked = None
        self.rotate_clicked = False
        self.crop_clicked = None

    def move(self, dx, dy):
        """
        Handles moving the Outline by its self

        dx -> The amount to move in the x-coordinate
        dy -> The amount to move in the y-direction

        pre-conditions: None
        post-conditions: The location of the Outline is changed

        return -> None
        """
        Shape.move(self, dx, dy)
        self.top_left += (dx, dy)
        self.top_right += (dx, dy)
        self.bottom_left += (dx, dy)
        self.bottom_right += (dx, dy)


class CanvasImage(Shape):
    """
    Stores an image file to draw on the canvas
    """
    def __init__(self, canvas, img,  select_func=None, name=None):
        Shape.__init__(self, canvas)
        self.select_func = select_func
        if type(img) == str:
            self.img = Image.open(img)             # PIL image object
        else:
            self.img = img
        self.name = name                            # Name of this image. Should be the same for all identical images
        self.orig_width, self.orig_height = self.img.size
        self.width, self.height = self.img.size
        self.img_tk = None                          # tkinter PhotoImage object
        self.id = None                              # ID of image drawn on canvas
        self.crop_limits = [0, 0, 0, 0]         # The percentage of the image that should be cropped in each direction

    def copy(self):
        """
        Copies the image into a new image. Image file is shared

        pre-conditions: None
        post-conditions: New image object created

        return -> The new image object
        """
        new = cp.copy(self)
        new.location = self.location.copy()
        new.crop_limits = cp.deepcopy(new.crop_limits)
        new.img_tk = None
        new.id = None
        return new

    def set_rotation(self, rotation):
        """
        Sets the rotation of the image

        rotation -> The rotation to set to

        pre-conditions: rotation in degrees
        post-conditions: rotation set

        return -> None
        """
        self.rotation = rotation

    def create_image(self):
        """
        Draws the Image on the canvas

        pre-conditions: Image is not already drawn on the canvas
        post-conditions: Image is drawn on the canvas

        return -> None
        """
        diagonal = int((self.width**2 + self.height**2)**.5)
        img = Image.new('RGBA', (diagonal, diagonal))

        width, height = self.img.size
        left, upper, right, bottom = 0, 0, width, height
        if self.crop_limits != [0, 0, 0, 0]:
            left = int(width * self.crop_limits[0])
            upper = int(height * self.crop_limits[1])
            right = int(width - (width * self.crop_limits[2]))
            bottom = int(height - (height * self.crop_limits[3]))
            to_paste = self.img.crop((left, upper, right, bottom))
        else:
            to_paste = self.img
        scale_x, scale_y = self.width / self.img.size[0], self.height / self.img.size[1]
        to_paste = to_paste.resize((int(to_paste.size[0]*scale_x), int(to_paste.size[1]*scale_y)), Image.ANTIALIAS)

        x_off = round((img.size[0]-to_paste.size[0])/2 + (left/2 - (width-right)/2)*scale_x)
        y_off = round((img.size[1]-to_paste.size[1])/2 + (upper/2 - (height-bottom)/2)*scale_y)
        img.paste(to_paste, (x_off,
                             y_off,
                             x_off+to_paste.size[0],
                             y_off+to_paste.size[1]))

        if self.transparency != 1:
            img_load = img.load()
            for row in range(img.size[0]):
                for col in range(img.size[1]):
                    pixel = img_load[row, col]
                    img_load[row, col] = pixel[0], pixel[1], pixel[2], int(pixel[3]*(self.transparency))

        img = img.rotate(-self.rotation)
        return img

    def draw(self):
        img = self.create_image()
        self.img_tk = ImageTk.PhotoImage(img)
        self.id = self.canvas.create_image(self.get_center().as_tuple(), image=self.img_tk)
        try:
            self.canvas.ids_to_image[self.id] = self
        except AttributeError:
            pass

        def handler(event):
            relative = Point(event.x-self.location.x, event.y-self.location.y)
            if relative.x < 0 or relative.y < 0:
                return
            transparency = self.img.load()[relative.x, relative.y][3]
            if transparency < 10:
                return
            else:
                self.select_func(event, self)

        if self.select_func:
            #self.canvas.tag_bind(self.id, '<Button-1>', lambda event: self.select_func(event, self))
            #elf.canvas.tag_bind(self.id, '<Button-1>', handler)
            self.canvas.tag_bind(self.id, '<Button-3>', lambda event: print(self.location))

    def make_tk(self):
        self.img_tk = ImageTk.PhotoImage(self.img)

    def draw_unprocessed(self):
        self.id = self.canvas.create_image(self.get_center().as_tuple(), image=self.img_tk)
        if self.select_func:
            self.canvas.tag_bind(self.id, '<Button-1>', lambda event: self.select_func(event, self))

    def destroy(self):
        """
        Destroys the Image from the canvas

        pre-conditions: Image is drawn on the canvas
        post-conditions: Image is removed from the canvas

        return -> None
        """
        self.canvas.delete(self.id)
        self.id = None

    def move(self, dx, dy):
        """
        Moves the Image by the given offsets without redrawing

        dx -> The amount to move in the x-coordinate
        dy -> The amount to move in the y-direction

        pre-conditions: None
        post-conditions: The location of the Image is changed

        return -> None
        """
        Shape.move(self, dx, dy)

    def scale_max(self):
        """
        Scales the image to the largest size it can be to fit within the canvas

        pre-conditions: None
        post-conditions: Image scaled but not redrawn

        return -> None
        """
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        im_width, im_height = self.img.size
        if im_width <= width and im_height <= height:
            return im_width, im_height
        if im_width > im_height:
            ratio = im_width / width
        else:
            ratio = im_height / height

        self.width = im_width/ratio
        self.height = im_height/ratio

    def scale_original(self):
        """
        Sets the image back to the original scale

        pre-conditions: None
        post-conditions; Image scaled but not redrawn

        return -> None
        """
        self.width, self.height = self.img.size