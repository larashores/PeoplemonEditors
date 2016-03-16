import tkinter as tk
from Editor.CreditsEditor.controller import Controller
from Editor.CreditsEditor.gui.menu import EditorMenu
from Editor.CreditsEditor.gui.mainGUI import Editor

import os

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Credits Editor')
    root.iconbitmap(os.path.join(os.getcwd(),'icons/editor.ico'))
    controller = Controller()
    menu = EditorMenu(controller)
    root.configure(menu=menu)

    from Editor import styles
    edit = Editor(root, controller)
    edit.pack(expand=tk.YES, fill=tk.BOTH, padx=10)
    tk.mainloop()
