import tkinter as tk
import os

from Editor.styles import configure_styles
from guicomponents.simplesavemenu import SimpleSaveMenu
from utilities.simplesaver import SimpleSaver


def run_simple_editor(EditorType, name, extension, file_type, location):
    root = tk.Tk()
    root.wm_title(name)
    root.iconbitmap(os.path.join('resources\\editor.ico'))
    menu = SimpleSaveMenu(location, parent=root, extension=extension, file_type=file_type)
    root.config(menu=menu)
    editor = EditorType(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH, padx=10, pady=(0, 10))
    saver = SimpleSaver(editor.main_saveable)
    saver.connect_to_menu(menu)

    configure_styles()
    root.mainloop()