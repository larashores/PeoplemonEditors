from MoveAnimationEditor.controller import Controller
from Editor.MoveAnimationEditor.gui.editor import Editor
from Editor.MoveAnimationEditor.gui.menu import EditorMenu

import tkinter as tk
from tkinter import ttk

import os
import logging

if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG,
    #                    format='%(asctime)s %(levelname)s "%(message)s"')

    controller = Controller()
    root = tk.Tk()
    root.iconbitmap(os.path.join('resources\\editor.ico'))
    root.title("Move Animation Editor")
    root.bind('<n>', lambda event: controller.add_frame())
    root.bind('<N>', lambda event: controller.add_frame())
    root.bind('<b>', lambda event: controller.insert_frame())
    root.bind('<B>', lambda event: controller.insert_frame())
    root.bind('<i>', lambda event: menu.add_image())
    root.bind('<I>', lambda event: menu.add_image())
    root.bind('<D>', lambda event: controller.delete_frame())
    root.bind('<d>', lambda event: controller.delete_frame())
    root.bind('<Control-e>', lambda event: menu.export())
    root.bind('<Control-E>', lambda event: menu.export())

    menu = EditorMenu(controller)
    controller.connect_to_menu(menu)
    root.config(menu=menu)
    style = ttk.Style()
    style.configure('Title.TLabel', font=('tkdefaultfont', 12, 'bold'))
    editor = Editor(root, controller)
    controller.editor = editor
    editor.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
