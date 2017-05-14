import time
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel

from PIL import ImageTk, Image

from Editor.MoveAnimationEditor.entrylabel import EntryLabel
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.listchoice_new import ListChoice
from Editor.MoveAnimationEditor.runtime_models.Outline import Outline
from Editor.MoveAnimationEditor.saveables.DrawnImage import DrawnImage
from Editor.saveable.saveableArray import ChangeType

SIZE = 800, 460


class Editor(ttk.Frame):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.sidebar = ttk.Frame(self)
        self.center_side = ttk.Frame(self)
        self.right_side = ttk.Frame(self)
        self.image_list = ListChoice(self.sidebar, update_cmd=self.load_preview, delete_cmd=self.delete_image)
        self.preview = tk.Canvas(self.sidebar, width=1, height=200, borderwidth=2, relief=tk.SUNKEN, background='white')
        self.frame_select = ttk.Scale(self.center_side, from_=1, to=1, command=self.on_frame_scale_changed)
        self.frame_label = ttk.Label(self.center_side, text='Frame', style='Title.TLabel')
        self.canvas = tk.Canvas(self.center_side, width=SIZE[0], height=SIZE[1],
                                highlightthickness=0, background='white')

        self.length_var = tk.IntVar(self)
        self.frame_trace = self.length_var.trace_variable('w', self.change_length)
        self.length = EntryLabel(self.right_side, text="Frame Length", entry_variable=self.length_var)
        intValidate(self.length.entry, 'u16')

        self.trans_var = tk.IntVar(self)
        self.transparency = ttk.Scale(self.right_side, from_=0, to=255, command=self.change_transparency)
        self.transparency_alt = ttk.Entry(self.right_side, width=15, justify=tk.CENTER, textvariable=self.trans_var)
        intValidate(self.transparency_alt, 'u8')
        self.apply = ttk.Button(self.right_side, text='Apply', command=self.apply_transparency)

        self.sidebar.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        ttk.Label(self.sidebar, text='Images', style='Title.TLabel').pack()
        self.image_list.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        self.preview.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        ttk.Button(self.sidebar, text='Insert Image', command=self.insert_image).pack(pady=(3, 5))

        self.center_side.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_label.pack()
        self.frame_select.pack(fill=tk.X)
        self.canvas.pack()
        self.canvas.bind('<Prior>', lambda event: self.handle_next(event, False))
        self.canvas.bind('<Next>', lambda event: self.handle_next(event, True))
        self.canvas.bind('<Delete>', self.on_delete_click)
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
        self.canvas.bind('<B3-Motion>', self.on_right_drag)
        self.canvas.bind('<Up>', lambda event: self.move(Editor.UP))
        self.canvas.bind('<Down>', lambda event: self.move(Editor.DOWN))
        self.canvas.bind('<Left>', lambda event: self.move(Editor.LEFT))
        self.canvas.bind('<Right>', lambda event: self.move(Editor.RIGHT))
        self.canvas.bind('<Control-c >', self.copy)
        self.canvas.bind('<Control-v >', self.paste)

        self.right_side.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(self.right_side, text='Frame Settings', style='Title.TLabel').pack(pady=(10, 10))
        self.length.pack()
        ttk.Label(self.right_side, text='Selection Transparency').pack(pady=(10, 0))
        self.transparency.pack(fill=tk.X, padx=(3, 3))
        self.transparency_alt.pack()
        self.apply.pack(pady=(5, 0))
        ttk.Button(self.right_side, text='Preview', command=self.preview_anim).pack(pady=(30, 0))

        self.preview_drawn_images = []  # Holds all images in the preview window
        self.cur_preview = None     # Stores current preview image to prevent garbage collection
        self.selected = None        # Stores the selected DrawImage
        self.outline = None         # Stores the current outline object
        self.copied = None          # Stroes a DrawnImage object that was copied
        self.ids_to_drawn = {}      # All DrawnImage's on the canvas can be references through id with this map

        # Create the background photo
        image = Image.open('resources\\layout.png')
        self.background = ImageTk.PhotoImage(image)
        self.canvas.create_image(image.size[0]//2, image.size[1]//2, image=self.background)

        self.transparency.set(255)
        self.toggle_transparency()

        self.controller.animation.images.register(self.anim_images_updates)
        self.controller.editor_model.register(self.change_frame)
        self.controller.animation.frames.register(self.frames_updated)
        self.change_frame(0)

    def on_left_click(self, event):
        self.canvas.focus_set()
        ids = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        to_select = None
        for _id in reversed(ids):
            if 'drawn_image' in self.canvas.gettags(_id) and _id in self.ids_to_drawn:
                img = self.ids_to_drawn[_id]
                center_x, center_y = img.get_center()
                top_left_x = center_x - (img.scaled_img.size[0] / 2)
                top_left_y = center_y - (img.scaled_img.size[1] / 2)
                x, y = int(event.x-top_left_x), int(event.y-top_left_y)
                transparency = img.scaled_img.load()[x, y][3]
                if transparency > 0 and to_select is None:
                    if img == self.selected:
                        return
                    to_select = img
        if to_select:
            self.select(to_select)

    def on_right_click(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def on_right_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def anim_images_updates(self, update_type, anim_img):
        if update_type == ChangeType.ADD:
            self.preview_drawn_images.append(DrawnImage(anim_img))
            self.image_list.addChoice(anim_img.name)
            self.image_list.update()
            self.image_list.setSelection(-1)
        elif update_type == ChangeType.REMOVE:
            for ind, img in enumerate(self.preview_drawn_images):
                if img.anim_img == anim_img:
                    img.destroy(self.preview)
                    self.preview_drawn_images.pop(ind)
                    self.image_list.delete(ind)
                    break
            self.controller.editor_model.current_frame = self.controller.editor_model.current_frame

    def select(self, image):
        """
        Selects an image on the canvas for editing. Draws outline around image

        image -> The CanvasImage object to select

        pre-conditions: Image is drawn on the canvas
        post-conditions: The image is selected

        return -> None
        """
        if self.outline:
            self.outline.destroy(self.canvas)
        self.selected = image
        self.outline = Outline(self.canvas, image, self.ids_to_drawn)
        self.outline.draw(self.canvas)
        self.toggle_transparency()
        self.transparency.set(image.transparency)
        self.trans_var.set(image.transparency)

    def frames_updated(self, update_type, frame):
        self.frame_select.config(to=len(self.controller.animation.frames))

    def copy(self, event):
        self.copied = self.selected.copy()

    def paste(self, event):
        if self.copied:
            frm = self.controller.animation.frames[self.cur_frame]
            frm.images.append(self.copied)
            _id = self.copied.draw(self.canvas)
            self.ids_to_drawn[_id] = self.copied
            self.select(self.copied)
            self.copied = self.copied.copy()

    def toggle_transparency(self):
        if self.selected:
            self.transparency.state(['!disabled'])
            self.transparency_alt.state(['!disabled'])
            self.apply.state(['!disabled'])
        else:
            self.transparency.state(['disabled'])
            self.transparency_alt.state(['disabled'])
            self.apply.state(['disabled'])

    def load_preview(self, ind):
        """
        Loads an image into the preview window

        ind -> The index of the image in self.image_list to add to the animation

        pre-conditions: Image at index 'ind' of self.images exists and is a CanvasImage
        post-conditions: Image in preview is changed

        return -> None
        """
        img = self.preview_drawn_images[ind]
        img.scale_max(self.preview)
        img.center(self.preview)
        if self.cur_preview:
            self.preview.delete(tk.ALL)
        img.draw(self.preview)
        self.cur_preview = img

    def delete_image(self, ind):
        """
        Deletes an image from the list of images to be used. Also deletes image from all frames it's used in

        ind -> Index of the image in self.image_list to delete

        pre-conditions: Image at index 'ind' of self.images exists and is a CanvasImage
        post-conditions: Image deleted from image list and any frame's it is used in

        return -> None
        """
        name = self.controller.animation.images[ind].name
        answer = None
        for frame in self.controller.animation.frames:
            new = [image for image in frame.images if name == image.name]
            if len(new) != 0 and answer is None:
                answer = askokcancel(title='Delete Image', message='Deleting this image will also delete it'
                                                                   'from all frames of the animation')
                if answer is False:
                    return
            for image in new:
                frame.images.remove(image)
        self.controller.animation.images.pop(ind)

    def insert_image(self):
        """
        Inserts the currently selected image into the current frame

        pre-conditions: self.cur_preview is a CanvasImage object
                        self.cur_frame is a valid index of a Frame in self.frames
        post-conditions: Image is inserted into current frame

        return -> None
        """
        if self.cur_preview is None:
            return
        img = self.cur_preview
        new = img.copy()
        new.canvas = self.canvas
        new.scale_original()
        new.center(self.canvas)
        new.select_func = self.select

        self.controller.animation.frames[self.controller.editor_model.current_frame].images.append(new)
        _id = new.draw(self.canvas)
        self.ids_to_drawn[_id] = new

    def handle_next(self, event, prev):
        """
        Event handler for toggling selection to the next image

        event -> The event object
        prev -> True if the previous image should actually be selected, otherwise false

        pre-conditions: self.cur_frame is a valid index of self.frames
        post-conditions: Current selected object is changed
        """
        images = self.controller.animation.frames[self.controller.editor_model.current_frame].images
        if self.selected:
            ind = images.index(self.selected)
            if prev:
                ind -= 1
            else:
                ind += 1
            img = images[ind % len(images)]
            self.select(img)
        elif len(images) != 0:
            self.select(images[0])

    def on_frame_scale_changed(self, event):
        """
        Event handler for when the frame selector scale is moved

        event -> The event object

        pre-conditions: self.cur_frame is valid index into self.frames
        post-conditions: Frame changed if number changed enough

        return -> None
        """
        num = self.frame_select.get()
        rounded = round(num)
        if rounded != num:
            self.frame_select.set(rounded)
            return
        if num - 1 != self.controller.editor_model.current_frame:
            self.controller.editor_model.current_frame = num - 1

    def change_frame(self, ind):
        if self.outline:
            self.outline.destroy(self.canvas)
        self.frame_label.config(text='Frame {}'.format(ind+1))
        self.canvas.delete('drawn_image')
        self.canvas.delete('outline')
        self.ids_to_drawn.clear()
        self.frame_select.set(ind + 1)
        frame = self.controller.animation.frames[ind]
        self.length_var.set(frame.length)
        _ids = frame.draw(self.canvas)
        self.ids_to_drawn.update(_ids)
        self.selected = None
        if self.controller.editor_model.current_frame != 0:
            last_frm = self.controller.animation.frames[self.controller.editor_model.current_frame - 1]
            last_frm.draw_half_transparent(self.canvas)
        self.toggle_transparency()

    def on_delete_click(self, event):
        if self.selected is None:
            return
        self.outline.destroy(self.canvas)
        self.selected.destroy(self.canvas)
        self.controller.animation.frames[self.controller.editor_model.current_frame].images.remove(self.selected)
        self.selected = None
        self.toggle_transparency()

    def change_length(self, name, empty, mode):
        try:
            num = int(self.length_var.get())
        except ValueError:
            return
        if num != self.controller.animation.frames[self.controller.editor_model.current_frame].length:
            self.controller.animation.frames[self.controller.editor_model.current_frame].length = num

    def change_transparency(self, event):
        if self.selected:
            transparency = round(self.transparency.get())
            self.selected.transparency = transparency
            self.trans_var.set(transparency)
            _old = self.selected.destroy(self.canvas)
            _new = self.selected.draw(self.canvas)
            del self.ids_to_drawn[_old]
            self.ids_to_drawn[_new] = self.selected
            self.outline.destroy(self.canvas)
            self.outline.draw(self.canvas)

    def apply_transparency(self):
        if self.selected:
            transparency = self.trans_var.get()
            self.transparency.set(transparency)
            self.change_transparency(None)

    def move(self, direction):
        if not self.selected:
            return
        if direction == Editor.UP:
            self.selected.y -= 1
            self.outline.move(0, -1)
        elif direction == Editor.DOWN:
            self.selected.y += 1
            self.outline.move(0, 1)
        elif direction == Editor.RIGHT:
            self.selected.x += 1
            self.outline.move(1, 0)
        elif direction == Editor.LEFT:
            self.selected.x -= 1
            self.outline.move(-1, 0)

        self.outline.redraw(self.canvas)

    def preview_anim(self):
        def clear_canvas():
            self.canvas.delete('drawn_image')
            self.canvas.delete('outline')
            self.ids_to_drawn.clear()
        clear_canvas()
        for frame in self.controller.animation.frames:
            start = time.time()
            clear_canvas()
            frame.draw(self.canvas)
            self.canvas.update_idletasks()
            self.canvas.update()
            end = time.time()
            wait = frame.length/1000 - (end-start)
            wait = 0 if wait < 0 else wait
            time.sleep(wait)

        self.controller.editor_model.current_frame = self.controller.editor_model.current_frame
