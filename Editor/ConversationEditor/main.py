import tkinter as tk
import tkinter.ttk as ttk
from Editor.ConversationEditor.gui.mainGUI import ConversationEditor
from Editor.ConversationEditor.controller import Controller
from Editor.ConversationEditor.gui.menu import EditorMenu

from Editor.fonts import TITLE_FONT, SUBTITLE_FONT
import os

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Conversation Editor')

    style = ttk.Style()
    style.configure('Title.TLabel', font=TITLE_FONT)
    style.configure('Subtitle.TLabel', font=SUBTITLE_FONT)

    controller = Controller()

    menu = EditorMenu(controller)
    root.config(menu=menu)
    editor = ConversationEditor(root, controller)
    editor.pack(expand=tk.YES, fill=tk.BOTH)

    root.iconbitmap(os.path.join(os.getcwd(), 'icons\editor.ico'))

    tk.mainloop()
