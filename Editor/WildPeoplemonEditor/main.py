import tkinter as tk
import os

from utilities.simplesaver import SimpleSaver
from WildPeoplemonEditor.wildeditor import WildEditor
from guicomponents.simplesavemenu import SimpleSaveMenu
from Editor.styles import configure_styles

LOCATION = 'wildpeoplemoneditor'

if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title('Wild Peoplemon Editor')
    root.iconbitmap(os.path.join('resources\\editor.ico'))
    menu = SimpleSaveMenu(LOCATION, parent=root, extension='wild', file_type='Wild Peoplemon')
    root.config(menu=menu)
    editor = WildEditor(root)
    editor.pack(expand=tk.YES, fill=tk.BOTH)
    saver = SimpleSaver(editor.peoplemon)
    saver.connect_to_menu(menu)

    configure_styles()
    root.mainloop()
