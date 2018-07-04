import time
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel

import logging
import operator

from PIL import ImageTk, Image

from Editor.guicomponents.entrylabel import EntryLabel
from Editor.guicomponents.CanvasPlus import CanvasPlus
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.listchoice import ListChoice
from Editor.MoveAnimationEditor.runtime_models.Outline import Outline
from Editor.MoveAnimationEditor.saveables.DrawnImage import DrawnImage
from Editor.guicomponents.simplemenu import SimpleMenu

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
        self.image_list = ListChoice(self.sidebar)
        self.preview = CanvasPlus(self.sidebar, width=1, height=200, borderwidth=2, relief=tk.SUNKEN, background='white')
        self.frame_select = ttk.Scale(self.center_side, from_=1, to=1, command=self.on_frame_scale_changed)
        self.frame_label = ttk.Label(self.center_side, text='Frame', style='Title.TLabel')
        self.canvas = CanvasPlus(self.center_side, width=SIZE[0], height=SIZE[1],
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
        self.canvas.bind('<Control-Prior>', self.move_forward)
        self.canvas.bind('<Control-Next>', self.move_backward)
        self.canvas.bind('<Prior>', lambda event: self.handle_next(event, False))
        self.canvas.bind('<Next>', lambda event: self.handle_next(event, True))
        self.canvas.bind('<Delete>', self.on_delete_click)
        self.canvas.bind('<Control-Button-1>', self.on_ctrl_click)
        self.canvas.bind('<Control-B1-Motion>', self.on_ctrl_drag)
        self.canvas.bind('<Button-1>', self.on_left_click)
        self.canvas.bind('<Button-3>', self.on_right_click)
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

        self.cur_preview = None     # Stores current preview image to prevent garbage collection
        self.outline = None         # Stores the current outline object
        self.copied = None          # Stroes a DrawnImage object that was copied

        # Create the background photo
        image = Image.open('resources\\layout.png')
        self.background = ImageTk.PhotoImage(image)
        self.canvas.create_image(image.size[0]//2, image.size[1]//2, image=self.background)

        self.transparency.set(255)
        self.toggle_transparency()

        self.controller.animation.frames.signal_add.connect(self.on_frame_add_or_remove)
        self.controller.animation.frames.signal_remove.connect(self.on_frame_add_or_remove)
        self.controller.animation.images.signal_add.connect(self.on_preview_add)
        self.controller.animation.images.signal_remove.connect(self.on_preview_remove)
        self.image_list.signal_select.connect(self.on_preview_selected)
        self.image_list.signal_delete.connect(self.on_preview_deleted)
        self.controller.editor_model.signal_frame_changed.connect(self.on_frame_change)
        self.on_frame_change(0)

    def on_left_click(self, event):
        clicked_image = self.selected_image(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        if type(clicked_image) == DrawnImage and clicked_image != self.get_selected():
            self.select(clicked_image)

    def on_right_click(self, event):
        pos = (self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))
        selected = self.selected_image(*pos) is not None
        self.on_left_click(event)
        menu = SimpleMenu(self, tearoff=0)
        if self.cur_preview is not None:
            menu.add_action('Insert', lambda: self.insert_image(pos))
        if selected:
            menu.add_action('Copy', self.copy)
        if self.copied is not None:
            menu.add_action('Paste', lambda: self.paste_at(pos))
        if selected:
            menu.add_action('Move Back', self.move_backward)
            menu.add_action('Move Forward', self.move_forward)
            menu.add_action('Delete', self.on_delete_click)
        menu.tk_popup(event.x_root, event.y_root)

    def on_ctrl_click(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def on_ctrl_drag(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def on_delete_click(self, event=None):
        if self.get_selected() is None:
            return
        self.controller.animation.frames[self.controller.editor_model.current_frame].images.remove(self.get_selected())
        self.set_selected(None)
        self.toggle_transparency()

    def move_backward(self, event=None):
        self.move_depth(operator.sub)

    def move_forward(self, event=None):
        self.move_depth(operator.add)

    def move_depth(self, op):
        if self.get_selected():
            frame = self.controller.animation.frames[self.controller.editor_model.current_frame]
            ind = frame.images.index(self.get_selected())
            next_ind = max(0, min(op(ind, 1), len(frame.images)))
            print(ind, next_ind)
            frame.images.remove(self.get_selected())
            frame.images.insert(next_ind, self.get_selected())
            self.outline.draw(self.canvas)

    def on_preview_add(self, ind, anim_img):
        logging.info("Loading Image " + anim_img.name)
        img = DrawnImage(anim_img)
        self.image_list.append(img)
        self.image_list.set_selection(-1)

    def on_preview_remove(self, ind, anim_img):
        to_remove = (ind for ind, img in enumerate(self.image_list) if img.anim_img == anim_img)
        for ind in to_remove:
            img = self.image_list.pop(ind)
            if self.preview:
                img.destroy(self.preview)
        self.controller.editor_model.current_frame = self.controller.editor_model.current_frame

    def on_preview_selected(self, ind):
        if ind is None:
            if self.cur_preview is not None:
                self.cur_preview.destroy(self.preview)
            return
        img = self.image_list[ind]
        img.scale_max(self.preview)
        img.center(self.preview)
        if self.cur_preview:
            self.preview.delete(tk.ALL)
        img.draw(self.preview)
        self.cur_preview = img

    def on_preview_deleted(self):
        ind = self.image_list.get_selection()
        if ind is None:
            return
        anim_image = self.controller.animation.images[ind]
        answer = None
        for frame in self.controller.animation.frames:
            new = [image for image in frame.images if image.anim_img == anim_image]
            if len(new) and answer is None:
                answer = askokcancel(title='Delete Image', message='Deleting this image will also delete it '
                                                                   'from all frames of the animation')
                if answer is False:
                    return
            for image in new:
                frame.images.remove(image)
        self.controller.animation.images.pop(ind)

    def on_image_add(self, ind, image):
        logging.info("Adding {} level: {}".format(image.name, image.level))
        frame = self.controller.animation.frames[self.controller.editor_model.current_frame]
        image.level = ind
        image.draw(self.canvas)
        for i in range(ind+1, len(frame.images)):
            img = frame.images[i]
            img.level = i
            img.redraw(self.canvas)

        self.select(image)

    def on_image_remove(self, ind, image):
        logging.info("Removing {} level: {}".format(image.name, image.level))
        frame = self.controller.animation.frames[self.controller.editor_model.current_frame]
        if image == self.get_selected():
            self.outline.destroy(self.canvas)
        image.destroy(self.canvas)
        for i in range(ind, len(frame.images)):
            img = frame.images[i]
            img.level = ind
            img.redraw(self.canvas)

    def on_frame_add_or_remove(self, ind, frame):
        self.frame_select.config(to=len(self.controller.animation.frames))

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

    def on_frame_change(self, ind):
        if self.outline:
            self.outline.destroy(self.canvas)
        self.frame_label.config(text='Frame {}'.format(ind+1))
        self.canvas.delete('drawn_image')
        self.canvas.delete('outline')
        self.frame_select.set(ind + 1)
        if self.controller.editor_model.current_frame != 0:
            last_frm = self.controller.animation.frames[ind - 1]
            last_frm.draw_half_transparent(self.canvas)
        frame = self.controller.animation.frames[ind]
        self.length_var.set(frame.length)
        frame.draw(self.canvas)
        frame.images.signal_add.connect(self.on_image_add)
        frame.images.signal_remove.connect(self.on_image_remove)
        if self.get_selected():
            self.select(self.get_selected())
        self.toggle_transparency()

    def insert_image(self, pos=None):
        """
        Inserts the currently selected image into the current frame

        pre-conditions: self.cur_preview is a CanvasImage object
                        self.cur_frame is a valid index of a Frame in self.frames
        post-conditions: Image is inserted into current frame

        return -> None
        """
        if self.cur_preview is None:
            return
        frame = self.controller.animation.frames[self.controller.editor_model.current_frame]
        img = self.cur_preview
        new = img.copy()
        new.canvas = self.canvas
        new.scale_original()
        if pos is not None:
            new.x = int(pos[0] - new.width/2)
            new.y = int(pos[1] - new.height/2)
        else:
            new.center(self.canvas)
        frame.images.append(new)

    def selected_image(self, x, y):
        self.canvas.focus_set()
        references = self.canvas.find_overlapping_references(x, y, x, y)
        for ref in reversed(references):
            if type(ref) == Outline:
                return ref
            if type(ref) == DrawnImage:
                center_x, center_y = ref.get_center()
                top_left_x = center_x - (ref.scaled_img.size[0] / 2)
                top_left_y = center_y - (ref.scaled_img.size[1] / 2)
                x_, y_ = int(x-top_left_x), int(y-top_left_y)
                transparency = ref.scaled_img.load()[x_, y_][3]
                if transparency > 0:
                    return ref
        return None

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
        self.set_selected(image)
        self.controller.animation.frames[self.controller.editor_model.current_frame].last_selected = image
        self.outline = Outline(self.canvas, image)
        self.outline.draw(self.canvas)
        self.toggle_transparency()
        self.transparency.set(image.transparency)
        self.trans_var.set(image.transparency)

    def copy(self, event=None):
        self.copied = self.get_selected().copy()

    def paste(self, event):
        self.paste_at()

    def paste_at(self, location=None):
        if self.copied:
            frm = self.controller.animation.frames[self.controller.editor_model.current_frame]
            cpy = self.copied.copy()
            if location:
                cpy.x = int(location[0] - cpy.width/2)
                cpy.y = int(location[1] - cpy.height/2)
            frm.images.append(cpy)
            self.select(cpy)

    def toggle_transparency(self):
        if self.get_selected():
            self.transparency.state(['!disabled'])
            self.transparency_alt.state(['!disabled'])
            self.apply.state(['!disabled'])
        else:
            self.transparency.state(['disabled'])
            self.transparency_alt.state(['disabled'])
            self.apply.state(['disabled'])

    def handle_next(self, event, prev):
        """
        Event handler for toggling selection to the next image

        event -> The event object
        prev -> True if the previous image should actually be selected, otherwise false

        pre-conditions: self.cur_frame is a valid index of self.frames
        post-conditions: Current selected object is changed
        """
        images = self.controller.animation.frames[self.controller.editor_model.current_frame].images
        if self.get_selected():
            ind = images.index(self.get_selected())
            if prev:
                ind -= 1
            else:
                ind += 1
            img = images[ind % len(images)]
            self.select(img)
        elif len(images) != 0:
            self.select(images[0])

    def change_length(self, name, empty, mode):
        try:
            num = int(self.length_var.get())
        except ValueError:
            return
        if num != self.controller.animation.frames[self.controller.editor_model.current_frame].length:
            self.controller.animation.frames[self.controller.editor_model.current_frame].length = num

    def change_transparency(self, event):
        if self.get_selected():
            transparency = round(self.transparency.get())
            self.get_selected().transparency = transparency
            self.trans_var.set(transparency)
            self.get_selected().destroy(self.canvas)
            self.get_selected().draw(self.canvas)
            self.outline.destroy(self.canvas)
            self.outline.draw(self.canvas)

    def apply_transparency(self):
        if self.outline:
            transparency = self.trans_var.get()
            self.transparency.set(transparency)
            self.change_transparency(None)

    def move(self, direction):
        if not self.get_selected():
            return
        if direction == Editor.UP:
            self.get_selected().y -= 1
            self.outline.move(0, -1)
        elif direction == Editor.DOWN:
            self.get_selected().y += 1
            self.outline.move(0, 1)
        elif direction == Editor.RIGHT:
            self.get_selected().x += 1
            self.outline.move(1, 0)
        elif direction == Editor.LEFT:
            self.get_selected().x -= 1
            self.outline.move(-1, 0)

        self.outline.redraw(self.canvas)

    def preview_anim(self):
        def clear_canvas():
            self.canvas.delete('drawn_image')
            self.canvas.delete('outline')
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

    def set_selected(self, img):
        self.controller.animation.frames[self.controller.editor_model.current_frame].last_selected = img

    def get_selected(self):
        return self.controller.animation.frames[self.controller.editor_model.current_frame].last_selected
