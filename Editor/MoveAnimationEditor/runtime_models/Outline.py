import MoveAnimationEditor.rotation as rt
from MoveAnimationEditor.gui.point import Point
import numpy as np


class Outline:
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

    NEXT_ID = 0

    def __init__(self, canvas, image, id_map):
        self.image = image              # The CanvasImage object
        self.canvas = canvas
        self.rotation = image.rotation

        self.location = Point(image.x, image.y)
        location = self.location
        self.top_left = Point(location.x, location.y)
        self.top_right = Point(location.x + image.width, location.y)
        self.bottom_left = Point(location.x, location.y + image.height)
        self.bottom_right = Point(location.x + image.width, location.y + image.height)

        self.width, self.height = self.get_width(), self.get_height()

        self.last_pos = Point(0, 0)
        self.center_clicked = False
        self.resize_clicked = None
        self.rotate_clicked = False
        self.crop_clicked = None
        self.id_map = id_map

        self.id = self.NEXT_ID
        self.NEXT_ID += 1

    def draw(self, canvas):
        """
        Draws the Outline on the canvas

        pre-conditions: Outline is not already drawn on the canvas
        post-conditions: Outline is drawn on the canvas

        return -> None
        """
        center = self.get_center()
        tags = ('anim', 'outline-{}'.format(self.id))

        # -------------Make mover----------------
        coords = center.x - 10, center.y - 10, center.x + 10, center.y + 10
        mover = canvas.create_oval(coords, fill='grey', tags=tags)
        canvas.tag_bind(mover, '<Button-1>', self.on_translate_click)
        # ---------------------------------------

        # ------------Make crop outline-------------------
        left = (self.image.crop_left / 255) * self.get_width()
        upper = (self.image.crop_top / 255) * self.get_height()
        right = (self.image.crop_right / 255) * self.get_width()
        bottom = (self.image.crop_bottom / 255) * self.get_height()
        top_left_crop = self.top_left + (left, upper)
        top_right_crop = self.top_right + (-right, upper)
        bottom_left_crop = self.bottom_left + (left, -bottom)
        bottom_right_crop = self.bottom_right + (-right, -bottom)
        for point in top_left_crop, top_right_crop, bottom_left_crop, bottom_right_crop:
            point.set(*rt.rotation(point.x, point.y, self.get_center(), self.rotation))
        for coord1, coord2 in ((top_left_crop, top_right_crop), (top_right_crop, bottom_right_crop),
                               (bottom_right_crop, bottom_left_crop), (bottom_left_crop, top_left_crop)):
            canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y, fill='red', tags=tags)
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
            ln = canvas.create_line(coord1.x, coord1.y, coord2.x, coord2.y, tags=tags)
            canvas.tag_bind(ln, '<Button-1>', self.on_translate_click)
        # ---------------------------------------------

        # --------------------Make resizers-------------------------
        corners = zip((Outline.TOP_LEFT, Outline.TOP_RIGHT, Outline.BOTTOM_LEFT, Outline.BOTTOM_RIGHT),
                      rotated)
        for location, coords in corners:
            circ_coords = coords.x - 5, coords.y - 5, coords.x + 5, coords.y + 5
            resizer = canvas.create_oval(circ_coords, fill='blue', tags=tags)
            canvas.tag_bind(resizer, '<Button-1>',
                            lambda event, loc=location: self.on_resize_click(event, loc))
        # -----------------------------------------------------------

        # ------------------------Make rotator---------------------------
        start_point = top_left.midpoint(top_right)
        end_point = start_point + Point(np.sin(np.deg2rad(self.rotation)), -np.cos(np.deg2rad(self.rotation))) * 25

        canvas.create_line(start_point.x, start_point.y, end_point.x, end_point.y, tags=tags)
        rotator_coords = end_point.x - 7.5, end_point.y - 7.5, end_point.x + 7.5, end_point.y + 7.5
        rotator = canvas.create_oval(rotator_coords, fill='green', tags=tags)
        canvas.tag_bind(rotator, '<Button-1>', self.on_rotate_click)
        # ----------------------------------------------------------------

        # ---------------Make crop circles----------------
        mid1 = top_left_crop.midpoint(top_right_crop)
        mid2 = top_right_crop.midpoint(bottom_right_crop)
        mid3 = bottom_right_crop.midpoint(bottom_left_crop)
        mid4 = bottom_left_crop.midpoint(top_left_crop)
        for location, point in (Outline.LEFT, mid4), (Outline.TOP, mid1), (Outline.RIGHT, mid2), (Outline.BOTTOM, mid3):
            _id = canvas.create_oval(point.x-3, point.y-3, point.x+3, point.y+3, fill='red', tags=tags)
            canvas.tag_bind(_id, '<Button-1>',
                            lambda event, loc=location: self.on_crop_click(event, loc))
        # ------------------------------------------------

        canvas.bind('<ButtonRelease-1>', self.on_left_release)
        canvas.bind('<B1-Motion>', lambda event: self.on_motion(event, canvas))

    def on_translate_click(self, event):
        """
        Event handler for clicking the translate button

        event ----> The event object

        pre-conditions: None
        post-conditions: center_clicked flag set
                         last_pos set to point of event

        return -> None
        """
        self.last_pos = Point(event.x, event.y)
        self.center_clicked = True

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

    def on_left_release(self, event):
        """
        Handles releasing the mouse button. Turns all clicked flags off

        pre-conditions: None
        post-conditions: All clicked flags turned off

        return -> None
        """
        self.center_clicked = False
        self.resize_clicked = None
        self.rotate_clicked = False
        self.crop_clicked = None

    def on_motion(self, event, canvas):
        """
        Handler for moving the mouse. Dispatches control to appropriate function

        event -> The event object

        pre-conditions: None
        post-conditions: Appropriate move action taken

        return -> None
        """
        if self.center_clicked:
            self.on_translate(event, canvas)
        elif self.resize_clicked:
            self.on_resize(event)
        elif self.rotate_clicked:
            self.on_rotate(event)
        elif self.crop_clicked:
            self.on_crop(event)

    def on_translate(self, event, canvas):
        """
        Handles translation of the outline and image together

        event -> The event object

        pre-conditions: Mouse is over translate button and clicked
        post-conditions: Outline and image moved to new location

        return -> None
        """
        dx = event.x - self.last_pos.x
        dy = event.y - self.last_pos.y
        self.move(dx, dy)
        self.image.move(dx, dy)
        self.last_pos = Point(event.x, event.y)
        self.redraw(canvas)

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

    def redraw(self, canvas):
        """
        Redraws both the outline and the image

        pre-conditions: None
        post-conditions: Images redrawn

        return -> None
        """
        old_id = self.image.destroy(canvas)
        new_id = self.image.draw(canvas)
        del self.id_map[old_id]
        self.id_map[new_id] = self.image
        self.destroy(canvas)
        self.draw(canvas)

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

    def move(self, dx, dy):
        """
        Handles moving the Outline by its self

        dx -> The amount to move in the x-coordinate
        dy -> The amount to move in the y-direction

        pre-conditions: None
        post-conditions: The location of the Outline is changed

        return -> None
        """
        self.top_left += (dx, dy)
        self.top_right += (dx, dy)
        self.bottom_left += (dx, dy)
        self.bottom_right += (dx, dy)

    def destroy(self, canvas):
        canvas.delete('outline-{}'.format(self.id))
