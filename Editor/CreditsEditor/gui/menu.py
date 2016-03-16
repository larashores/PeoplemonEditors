import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename


class EditorMenu(tk.Menu):
    def __init__(self, controller):
        tk.Menu.__init__(self)
        self.controller = controller
        self.last_path = None
        file = tk.Menu(self, tearoff=0)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

    def save(self):
        path = asksaveasfilename(title='Save To?', initialdir=self.last_path,
                                 defaultextension='.credits', filetypes=[('Conversation File', '.credits')])
        if path == '':
            return

        try:
            self.last_path = path
            self.controller.saveToFile(path)
        except:
            showerror('Error', 'Error Saving: File not saved')
        showinfo('Saved', 'Animation Saved')

    def load(self):
        path = askopenfilename(title='Load From?', initialdir=self.last_path,
                                 defaultextension='.credits', filetypes=[('Conversation File', '.credits')])
        if path == '':
            return
        self.last_path = path
        try:
            self.controller.loadFromFile(path)
        except:
            showerror('Error', 'Error Loading: File not loaded')
