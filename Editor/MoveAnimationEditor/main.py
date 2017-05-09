import tkinter as tk
from tkinter import ttk

from MoveAnimationEditor.gui.editor import Editor
import os

from MoveAnimationEditor.controller import Controller
from Editor.MoveAnimationEditor.gui.menu import EditorMenu


if __name__ == '__main__':
    controller = Controller()
    root = tk.Tk()
    root.iconbitmap(os.path.join('icons\\editor.ico'))
    root.title("Move Animation Editor")
    root.bind('<Pause>', lambda event: controller.add_frame())
    root.bind('<End>', lambda event: controller.insert_frame())
    menu = EditorMenu(controller)
    root.config(menu=menu)
    style = ttk.Style()
    style.configure('Title.TLabel', font=('tkdefaultfont', 12, 'bold'))
    editor = Editor(root, controller)
    controller.editor = editor
    editor.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
