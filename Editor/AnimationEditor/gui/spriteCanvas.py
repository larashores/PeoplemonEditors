__author__ = 'Vincent'

import tkinter as tk

from PIL import Image, ImageTk

START_RES = (800, 600)


class SpriteSheetCanvas(tk.Canvas):
    def __init__(self, parent, controller, vars):
        self.controller = controller
        self.controller.apply_funcs.append(self.apply)
        controller.canvas = self
        self.vars = vars
        tk.Canvas.__init__(self, parent, width=START_RES[0], height=START_RES[1], highlightthickness=0)
        self.size = START_RES   # Size of the canvas
        self.scale = 1
        self.recs = []
        self.grid = Grid(self.scale)
        self.sheet = None
        self.sheetTk = None
        self.sprite_sheet_tkItem = None

        # Bind tag
        self.bind('<Button-1>', self.mousePress)
        #self.bind('<B1-Motion>', self.mouseDrag)
        self.bind('<Button-3>', self.rightClick)

    def newSheet(self, imgpath):
        """
        Puts a new sheet on the canvas
        :param imgpath:     The path of the sprite sheet
        :return:            A flag returning whether or not
        """
        self.sheet = Image.open(imgpath)
        self.scale = self.getReccomendedScale(*self.sheet.size)
        self.scaleAndShow()

    def scaleAndShow(self):
        self.grid = Grid(self.scale)
        x, y = self.sheet.size
        self.size = (x*self.scale, y*self.scale)
        new_sheet = self.sheet.resize(self.size)
        self.sheetTk = ImageTk.PhotoImage(new_sheet)

        self.config(width=self.size[0], height=self.size[1])
        self.sprite_sheet_tkItem = self.create_image((self.size[0]//2, self.size[1]//2), image=self.sheetTk)

    def getReccomendedScale(self, width, height):
        scale = 4
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        while (width*scale > screen_width) or (height*scale > screen_height):
            if scale > 1:
                scale -= 1
            else:
                break
        return scale

    def mousePress(self, event):
        """
        Proccess mouse click to place rectangle and find cooridinate

        :param event:
        :return:
        """
        if not self.sheet:
            return
        self.mouseDrag(event)

    def mouseDrag(self, event):
        if not self.sheet:
            return
        x, y = self.grid.snapToGrid((event.x, event.y))
        x, y = self.grid.toGridCoords(x, y)
        self.vars['x'].set(x)
        self.vars['y'].set(y)
        self.controller.apply()

    def rightClick(self,event):
        """
        Purpose: Proccess right mouse click to update active frame
        """
        if self.vars['man_frames'].get():
            x, y = event.x, event.y
            items = self.find_overlapping(x, y, x, y)
            for item in items:
                tags = self.gettags(item)
                if len(tags) == 1 and tags[0].isnumeric():
                    frame_ind = int(tags[0])
                    self.vars['active_frame'].set(frame_ind+1)
                    self.controller.apply()

    def apply(self):
        """
        Applies change in options or from a mouse click
        """
        self.drawAllFrames()

    def drawBox(self, x, y, width, height, color, tag):
        """
        Draws box on image, takes scaled coordinates
        """
        rec = self.create_rectangle((x, y, x+width, y+height), outline=color, fill='')
        fill_rec = self.create_rectangle((x, y, x+width, y+height), outline=color, fill='white', tags=tag)
        self.tag_lower(fill_rec)
        self.tag_raise(rec)
        self.recs.append((rec, fill_rec))

    def deleteRecs(self):
        """
        Deletes all rectangles on screen
        """
        for rec, fill_rec in self.recs:
            self.delete(rec)
            self.delete(fill_rec)
        self.recs.clear()

    def drawAllFrames(self):
        """
        Purpose:    Creates all frames assuming they are in order
        Inputs:     None
        Output:
            Creates frames in the sprite sheet and draws rectangles
        """
        color = 'black'
        self.deleteRecs()
        for ind in range(self.controller.getNumberFrames()):
            length, x, y, height, width, render_x, render_y, rotation = self.controller.getFrameInfo(ind)
            x, y = self.grid.toScaledCoords(x, y)
            width, height = self.grid.toScaledCoords(width, height)

            self.drawBox(x, y, width, height, color, tag=str(ind))
            self.update()

        self.changeToCurrent()

    def changeToCurrent(self):
        """
        Purpose: Changes the active frame, updates rectangle, and updates
                 sidebar
        """
        for recs in self.recs:                          # Set all rectangles to black
            self.itemconfig(recs[0], outline='black')
        rec = self.recs[self.vars['active_frame'].get()-1][0]
        self.itemconfig(rec, outline='red')
        self.tag_raise(rec)

    def changeScale(self, scale):
        if not self.sheet:
            return
        self.scale = scale
        self.scaleAndShow()
        self.drawAllFrames()



class Grid:
    """
    Makes a grid on top of another set of cooridnates and allows for converting
    between them. The scale is how many units of the top cooridnates are between
    each grid.
    """
    def __init__(self, scale):
        self.scale = scale

    def snapToGrid(self, coords):
        """
        Purpose: Will return closest point on a grid that is overlayed on a larger
                 grid
        Inputs:
            coords: (x,y) pair of actual cooridnates on larger grid
            scale:  The ratio of the size of the larger grid over the smaller grid
        Output:
            (x,y) cooridnates of the overlayed smaller grid
        """
        x, y = coords[0], coords[1]
        left = x % self.scale
        top = y % self.scale
        right = self.scale - left
        bottom = self.scale - top
        if top < bottom:
            y = y - top
        else:
            y = y + bottom
        if left < right:
            x = x - left
        else:
            x = x - right
        return x, y

    def toGridCoords(self, x, y):
        """
        Purpose: Converts actual cooridnates to cooridnates on the scaled grid
        Inputs:
            x:   x cooridnate
            y:   y cooridnate
        Output:
            Returns (x,y) cooridnate pair
        """
        return x//self.scale, y//self.scale

    def toScaledCoords(self, x, y):
        """
        Purpose: Converts grid cooridnates to scaled top cooridnates
        Inputs:
            x:   x cooridnate
            y:   y cooridnate
        Output:
            Returns (x,y) cooridnate pair
        """
        return x*self.scale, y*self.scale
