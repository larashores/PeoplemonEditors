import tkinter as tk
from tkinter import ttk

from Editor.AnimationEditor.gui import sidebar
from Editor.AnimationEditor.gui.spriteCanvas import SpriteSheetCanvas


class AnimationEditor(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        left = ttk.Frame(self)
        left.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        right = ttk.Frame(self, style='Boxed.TFrame')
        right.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.Y)

        self.sidebar = sidebar.SideBar(right, controller)
        self.canvas = SpriteSheetCanvas(left, controller, self.sidebar.vars)

        self.canvas.pack(side=tk.LEFT)
        self.sidebar.pack(padx=5, pady=5)

