import tkinter as tk
from tkinter import ttk
from styles import configure_styles
from guicomponents.variabletext import VariableText

COLUMNS = [
    'Welcome to the Tutorial',
    '''New Animation: Ctrl-N
Load Animation: Ctrl-O
Save Animation: Ctrl-S
Save Animation As: Ctrl-Shift-S
Export Animaton: Ctrl-E

Add Image: I
Add Frame: N
Insert Frame: B
Delete Frame: X

Move Image Into Foreground: Ctrl-Next
Move Image Into Background: Ctrl-Previous
Select Next Image: Next
Select Previous Image: Previous
Delete Image: Delete

Move Image: Direction Keys
Copy Image: Ctrl-C
Paste Image: Ctrl-V''']


class HelpMenu(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Move Animation Editor Help', style='Title.TLabel')
        self.topics = ttk.Treeview(self)
        self.var = tk.StringVar()
        self.info = VariableText(self, textvariable=self.var)
        self.var.set(COLUMNS[0])
        self.info.text.configure(state=tk.DISABLED)

        label.pack()
        self.topics.heading('#0', text='Topic')
        self.topics.pack(side=tk.LEFT, fill=tk.Y)
        self.info.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

        item = self.topics.insert('', tk.END, text='Overview')
        self.topics.insert('', tk.END, text='Shortcuts')
        self.topics.selection_set(item)

        self.topics.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        item = self.topics.identify('item', event.x, event.y)
        try:
            ind = int(item[1:])
            page = COLUMNS[ind - 1]
            self.info.text.configure(state=tk.NORMAL)
            self.var.set(page)
            self.info.text.configure(state=tk.DISABLED)
        except ValueError:
            pass


if __name__ == '__main__':
    root = tk.Tk()
    configure_styles()
    help = HelpMenu(root)
    help.pack(expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
