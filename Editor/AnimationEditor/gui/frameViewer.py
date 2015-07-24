__author__ = 'Vincent'

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk
from Editor.AnimationEditor.rotatedrec import rotatedRectangle
from Editor.AnimationEditor.gui.changeScale import askChange

class EditorMenu(tk.Menu):
    def __init__(self, frameViewer):
        tk.Menu.__init__(self)
        self.viewer = frameViewer
        edit = tk.Menu(self, tearoff=0)
        edit.add_command(label='Change Scale', command=self.changeScale)
        self.add_cascade(label='Edit', menu=edit)

    def changeScale(self):
        scale = askChange(self.viewer.scale)
        if scale:
            self.viewer.scale = scale
            if self.viewer.loaded:
                self.viewer.apply()

class FrameWindow(tk.Toplevel):
    def __init__(self, parent, controller):
        """

        :param parent: The parent widget
        :param spriteSheet:  The PIL image of the spriteSheet
        :return:
        """
        tk.Toplevel.__init__(self, parent)
        self.title('Frame Viewer')
        viewer = FrameViewer(self, controller)
        viewer.pack(padx=(5, 5), pady=(0, 5))

        self.config(menu=EditorMenu(viewer.canvas))

class FrameViewer(ttk.Frame):
    def __init__(self,parent,controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        style = ttk.Style()
        style.configure('Bold.TLabel', font=('TkDefaultFont', 11, 'bold'))

        self.active_frame = tk.IntVar()
        self.active_frame.set(1)

        self.canvas = FrameCanvas(self, controller, self.active_frame)

        self.top_frm = ttk.Frame(self)
        self.top_frm.pack()
        ttk.Label(self.top_frm, text='Frame Number', style='Bold.TLabel').pack()        # Top Label

        frm = ttk.Frame(self.top_frm)   # Frame Controls
        ttk.Button(frm, text='Previous', width=10, command=self.canvas.prev).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Entry(frm, width=5, textvariable=self.active_frame, justify=tk.CENTER).pack(side=tk.LEFT)
        ttk.Button(frm, text='Next', width=10, command=self.canvas.next).pack(side=tk.LEFT, padx=(5,0))
        frm.pack(pady=(0, 5))

        self.canvas.pack()


class FrameCanvas(ttk.Frame):
    def __init__(self, parent, controller, active_var):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.active_frame = active_var
        self.controller.apply_funcs.append(self.apply)
        self.spriteSheet = None
        self.scale = 10
        self.loaded = False
        self.images = []
        self.curPILimage = None
        self.store_image = None


        style = ttk.Style()
        style.configure('Blue.Boxed.TFrame', background='blue')

        canvas_frm = ttk.Frame(self, relief=tk.GROOVE, style='Blue.Boxed.TFrame')
        canvas_frm.pack()
        self.canvas = tk.Canvas(canvas_frm, height=300, width=250, highlightthickness=0)
        self.canvas.pack(padx=(5, 5), pady=(5, 5))

        self.canvas.configure(xscrollincrement='1', yscrollincrement='1')
        self.x_scroll_offset = 0
        self.y_scroll_offset = 0

        self.axes = []
        x_axis = self.canvas.create_line(-2000, 0, 2000, 0)
        y_axis = self.canvas.create_line(0, -2000, 0, 2000)
        self.axes.extend([x_axis, y_axis])

    def getReccomendedScale(self, width, height):
        scale = 50
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        while (width*scale > screen_width) or (height*scale > screen_height):
            if scale > 1:
                scale -= 1
            else:
                break
        return scale - int((scale//1.5))

    def makeFrameImages(self):
        self.images.clear()
        numFrames = self.controller.getNumberFrames()
        for ind in range(numFrames):
            length, x, y, height, width, render_x, render_y, rotation = self.controller.getFrameInfo(ind)
            subimage = self.getSubImage(x, y, width, height)
            self.images.append((subimage, length, (render_x, render_y), rotation))

    def getSubImage(self, x, y, width, height):
        subimage = self.spriteSheet.crop((x, y, x+width, y+height))
        subimage.load()
        return subimage

    def apply(self):
        self.canvas.xview_scroll(-self.x_scroll_offset, tk.UNITS)    #scroll back
        self.canvas.yview_scroll(-self.y_scroll_offset, tk.UNITS)

        self.spriteSheet = self.controller.getSpriteSheet()
        self.makeFrameImages()
        posWidth, posHeight, negWidth, negHeight = self.getMaxDimension()
        width = posWidth-negWidth
        height = posHeight-negHeight
        self.x_scroll_offset = int(negWidth*self.scale)
        self.y_scroll_offset = int(negHeight*self.scale)
        if not self.loaded:
            self.loaded = True
            self.scale = self.getReccomendedScale(width, height)
        self.canvas.config(width=width*self.scale, height=height*self.scale)
        self.canvas.xview_scroll(self.x_scroll_offset, tk.UNITS)
        self.canvas.yview_scroll(self.y_scroll_offset, tk.UNITS)
        self.reDraw()

    def reDraw(self):
        if self.curPILimage:
            self.canvas.delete(self.curPILimage)
        image, draw_coords = self.getImage()
        x, y = draw_coords
        self.curPILimage = self.canvas.create_image((x, y), image=image)
        for line in self.axes:
            self.canvas.tag_raise(line)

    def getMaxDimension(self):
        max_xs = []
        min_xs = []
        max_ys = []
        min_ys = []
        for image in self.images:
            dim = image[0].size
            rotate = image[3]
            offset = image[2]
            bound_coords, width, height = rotatedRectangle((0, 0), dim[0], dim[1], rotate)
            max_x = bound_coords[0]+width+offset[0]
            max_y = bound_coords[1]+height+offset[1]
            min_x = bound_coords[0]+offset[0]
            min_y = bound_coords[1]+offset[1]
            max_xs.append(max_x)
            max_ys.append(max_y)
            min_xs.append(min_x)
            min_ys.append(min_y)
        return max(max_xs), max(max_ys), min(min_xs), min(min_ys)

    def getImage(self):
        ind = int(self.active_frame.get())-1
        image = self.images[ind][0]
        offset = self.images[ind][2]
        rotation = self.images[ind][3]
        image = image.resize((image.size[0]*self.scale, image.size[1]*self.scale))
        image = image.convert('RGBA')
        draw = (image.size[0]/2)+(offset[0]*self.scale),(image.size[1]/2)+(offset[1]*self.scale)
        image = image.rotate(-rotation, expand=1)
        self.store_image = ImageTk.PhotoImage(image)
        return self.store_image, draw

    def prev(self):
        if len(self.images) == 0:
            return
        if self.active_frame.get() == 1:
            self.active_frame.set(len(self.images))
        else:
            self.active_frame.set(self.active_frame.get() - 1)
        self.reDraw()

    def next(self):
        if len(self.images) == 0:
            return
        if self.active_frame.get() == len(self.images):
            self.active_frame.set(1)
        else:
            self.active_frame.set(self.active_frame.get() + 1)
        self.reDraw()

if __name__ == '__main__':
    root = tk.Tk()
    fr = FrameWindow(root,None)
    tk.mainloop()
