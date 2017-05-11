import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, askokcancel
import os

from Editor.MoveAnimationEditor.guicomponents.listchoice import ListChoice
from Editor.MoveAnimationEditor.guicomponents.entrylabel import EntryLabel
from Editor.MoveAnimationEditor.guicomponents.integercheck import IntegerCheck

from Editor.MoveAnimationEditor.frame import Frame
from Editor.MoveAnimationEditor.gui.canvasobjects import CanvasImage
from Editor.MoveAnimationEditor.saveables.DrawnImage import DrawnImage
from Editor.MoveAnimationEditor.runtime_models.Outline import Outline

from Editor.saveable.saveableArray import ChangeType
from PIL import ImageTk, Image

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
        self.frame_select = ttk.Scale(self.center_side, from_=1, to=1, command=self.handle_frame)
        self.frame_label = ttk.Label(self.center_side, text='Frame', style='Title.TLabel')
        self.canvas = tk.Canvas(self.center_side, width=SIZE[0], height=SIZE[1],
                                highlightthickness=0, background='white')

        self.length_var = tk.IntVar(self)
        self.length_var.trace_variable('w', self.change_length)
        self.length = EntryLabel(self.right_side, text="Frame Length", validate='key', entry_variable=self.length_var,
                                 validatecommand=IntegerCheck(self, 'u16').vcmd)

        self.trans_var = tk.IntVar(self)
        self.transparency = ttk.Scale(self.right_side, from_=0, to=255, command=self.change_transparency)
        self.transparency_alt = ttk.Entry(self.right_side, width=15, validate='key', justify=tk.CENTER, textvariable=self.trans_var,
                                          validatecommand=IntegerCheck(self, 'u8').vcmd)
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
        self.canvas.bind('<Delete>', self.delete_selection)
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<Button-3>', self.click_canvas)
        self.canvas.bind('<B3-Motion>', self.drag_canvas)
        self.canvas.bind('<Up>', lambda event: self.move(Editor.UP))
        self.canvas.bind('<Down>', lambda event: self.move(Editor.DOWN))
        self.canvas.bind('<Left>', lambda event: self.move(Editor.LEFT))
        self.canvas.bind('<Right>', lambda event: self.move(Editor.RIGHT))
        self.canvas.bind('<Control-c >', self.copy)
        self.canvas.bind('<Control-v >', self.paste)
        self.canvas.ids_to_image = {}

        self.right_side.pack(side=tk.LEFT, fill=tk.Y)
        ttk.Label(self.right_side, text='Frame Settings', style='Title.TLabel').pack(pady=(10, 10))
        self.length.pack()
        ttk.Label(self.right_side, text='Selection Transparency').pack(pady=(10, 0))
        self.transparency.pack(fill=tk.X, padx=(3, 3))
        self.transparency_alt.pack()
        self.apply.pack(pady=(5, 0))
        ttk.Button(self.right_side, text='Preview', command=self.preview_anim).pack(pady=(30, 0))

        self.images = []            # Holds images for when they are first added to the editor
        self.preview_drawn_images = []
        self.prev_frame = None      # Stores previous frame so images won't be garbage collected
        self.cur_preview = None     # Stores current preview image to prevent garbage collection
        self.selected = None        # Stores the id of the current selected image
        self.outline = None         # Stores the current outline object
        self.cur_frame = 0          # Stores the current selected frame
        self.copied = None
        self.ids_to_drawn = {}

        self.background = CanvasImage(self.canvas, 'icons\\layout.png')
        self.background.draw()


        def handler(event):
            x = event.x
            y = event.y
            tags = self.canvas.find_overlapping(x-1, y-1, x+1, y+1)
            print(tags)
            max_transparent = 0
            select = None
            for tag in tags:
                if tag in self.canvas.ids_to_image:
                    img = self.canvas.ids_to_image[tag]
                    if tag == self.background.id:
                        continue
                    relative = (event.x-img.location.x, event.y-img.location.y)
                    if relative[0] < 0 or relative[1] < 0 or relative[0] > img.width or relative[1] > img.height:
                        continue
                    print('location:', relative)
                    transparency = img.img.load()[relative[0], relative[1]][3]
                    if transparency > max_transparent:
                        select = img
            if select and select.select_func:
                select.select_func(event, select)

        #self.canvas.bind('<Button-1>', handler)

        self.frame_select.set(1)
        self.transparency.set(1)
        self.toggle_transparency()
        self.length_var.set(30)

        self.canvas_clicked = False

        PATH = r'E:\Applications\Peoplemon 2\Move Animations'
        ttk.Button(self.right_side, text='Convert', command=lambda: self.controller.convert_all(PATH)).pack()

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
            frm = self.frames[self.cur_frame]
            frm.images.append(self.copied)
            self.copied.draw()
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

    def click_canvas(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def drag_canvas(self, event):
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

    def add_image(self, img, name=''):
        """
        Adds an image to the program that can be used in animations. Can then be selected from self.image_list

        path -> The path of the image to open

        pre-conditions: None
        post-conditions: The image is added to image_list and selected

        return -> None
        """
        if type(img) == str:
            name = os.path.split(img)[1]
            try:
                img = CanvasImage(self.preview, img, name=name)
                img.scale_max()
                img.center()
            except OSError:
                showerror('Invalid Image', 'Image could not be loaded')
                return
        else:
            img = CanvasImage(self.preview, img, name=name)
        self.images.append(img)
        self.image_list.addChoice(name)
        self.image_list.update()
        self.image_list.setSelection(-1)

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

        #if answer:
        #    self.controller.editor_model.current_frame = self.controller.editor_model.current_frame

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
        images = self.frames[self.cur_frame].images
        if self.selected:
            ind = images.index(self.selected)
            if prev:
                ind -= 1
            else:
                ind += 1
            img = images[ind % len(images)]
            self.select(event, img)
        elif len(images) != 0:
            self.select(event, images[0])

    def handle_frame(self, event):
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
            self.outline.destroy()
        self.frame_label.config(text='Frame {}'.format(ind+1))
        self.canvas.delete('drawn_image')
        self.canvas.delete('outline')
        self.ids_to_drawn.clear()
        self.frame_select.set(ind + 1)
        frame = self.controller.animation.frames[ind]
        self.length_var.set(frame.length)
        _ids = frame.draw(self.canvas)
        self.ids_to_drawn.update(_ids)
        '''
        if self.cur_frame != 0:
            last_frm = self.frames[self.cur_frame - 1].copy()
            for img in last_frm:
                img.transparency /= 2
                img.select_func = None
            last_frm.draw()
            self.prev_frame = last_frm
        '''
        self.toggle_transparency()

    def delete_selection(self, event):
        if self.selected is None:
            return
        self.outline.destroy(self.canvas)
        self.selected.destroy(self.canvas)
        self.controller.animation.frames[self.controller.editor_model.current_frame].images.remove(self.selected)
        self.selected = None
        self.toggle_transparency()

    def insert_frame(self, ind):
        """
        Adds a frame to the of the animation and selects that frame

        ind -> The frame to add the new frame after (1-based)

        pre-conditions: None
        post-conditions: New frame added and selected

        return -> None
        """
        num_frames = len(self.controller.animation.frames)
        self.controller.animation.frames.insert((ind % num_frames),
                                                self.controller.animation.frames[(ind % (num_frames+1))-1].copy())
        self.frame_select.config(to=len(self.controller.animation.frames))
        self.frame_select.set((ind % (num_frames+1)) + 1)
        self.change_frame(ind)

    def delete_frame(self, ind):
        """
        Deletes a frame from the animation and selects the next frame)

        ind -> The frame to delete (1-based)

        pre-conditions: None
        post-conditions: New frame deleted and next selected

        return -> None
        """
        if ind == 1 and len(self.frames) == 1:
            return
        self.frames.pop((ind % len(self.frames)) - 1)
        self.frame_select.config(to=len(self.frames))
        if len(self.frames) < ind:
            ind = len(self.frames)
        self.frame_select.set(ind)
        self.handle_frame(None)

    def change_length(self, name, empty, mode):
        try:
            num = int(self.length_var.get())
        except ValueError:
            return
        if num != self.controller.animation.frames[self.cur_frame].length:
            self.controller.animation.frames[self.cur_frame].length = num

    def change_transparency(self, event):
        """
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
        """

    def apply_transparency(self):
        if self.selected:
            transparency = self.trans_var.get()
            self.transparency.set(transparency)
            self.change_transparency(None)

    def move(self, direction):
        if not self.selected:
            return
        if direction == Editor.UP:
            add = (0, -1)
        elif direction == Editor.DOWN:
            add = (0, 1)
        elif direction == Editor.RIGHT:
            add = (1, 0)
        elif direction == Editor.LEFT:
            add = (-1, 0)

        self.selected.location += add
        self.outline.move(*add)
        self.selected.destroy()
        self.outline.destroy()
        self.selected.draw()
        self.outline.draw()

    def preview_anim(self):
        import time
        new_frames = []
        for ind, frame in enumerate(self.frames):
            frm = Frame()
            frm.length = frame.length
            new_frames.append(frm)
            image = Image.new('RGBA', SIZE)
            for img in frame.images:
                top = Image.new('RGBA', SIZE)
                processed = img.create_image()
                top_left = img.get_center() - (processed.size[0]/2, processed.size[1]/2)
                top_left.set(int(round(top_left[0])), int(round(top_left[1])))
                bottom_right = top_left + (processed.size[0], processed.size[1])
                print('Index:', ind, (top_left[0], top_left[1]))
                #new_image.paste(processed, (top_left[0], top_left[1], bottom_right[0], bottom_right[1]))
                top.paste(processed, (top_left[0], top_left[1]))
                image = Image.alpha_composite(image, top)

            cvs = CanvasImage(self.canvas, image)
            cvs.make_tk()
            frm.images.append(cvs)

        self.background.make_tk()
        for frame in new_frames:
            start = time.time()
            self.canvas.delete(tk.ALL)
            self.background.draw_unprocessed()
            frame.draw_unprocessed()
            self.canvas.update_idletasks()
            self.canvas.update()
            end = time.time()
            wait = frame.length/1000 - (end-start)
            wait = 0 if wait < 0 else wait
            print(wait)
            time.sleep(wait)

        self.cur_frame = -1
        self.selected = None
        self.outline = None
        self.change_frame(None)
