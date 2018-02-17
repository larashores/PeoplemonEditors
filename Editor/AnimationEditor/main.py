import tkinter as tk
from tkinter import ttk

import os

from Editor.AnimationEditor.controller import Controller
from Editor.AnimationEditor.gui.menu import EditorMenu
from Editor.AnimationEditor.gui.mainGUI import AnimationEditor
from Editor.AnimationEditor.gui.frameViewer import FrameWindow


if __name__ == '__main__':
    controller = Controller()
    root = tk.Tk()
    root.iconbitmap(os.path.join(os.getcwd(), 'resources\\editor.ico'))
    menu = EditorMenu(controller)
    root.config(menu=menu)
    root.title('Animation Editor')

    window = FrameWindow(root, controller)
    window.protocol('WM_DELETE_WINDOW', lambda: None)

    style = ttk.Style()
    style.configure('Boxed.TFrame', relief=tk.RIDGE, borderwidth=5)
    style.configure('Action.TButton', width=8)

    editor = AnimationEditor(root, controller)
    editor.pack()

    root.mainloop()
