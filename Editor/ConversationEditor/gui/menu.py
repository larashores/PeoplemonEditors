import tkinter as tk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter.messagebox import askokcancel, showerror, showinfo


class EditorMenu(tk.Menu):
    def __init__(self, controller):
        tk.Menu.__init__(self)
        self.last_path = None
        self.controller = controller
        file = tk.Menu(self, tearoff=0)
        file.add_command(label='New', command=self.new)
        file.add_command(label='Save', command=self.save)
        file.add_command(label='Load', command=self.load)
        self.add_cascade(label='File', menu=file)

    def save(self):
        path = asksaveasfilename(title='Save Conversation', initialdir=self.last_path,
                                 defaultextension='.convo', filetypes=[('Conversation File', '.convo')])
        if not path:
            return

        self.controller.save(path)
        try:
            showinfo('Saved', 'Animation saved')
        except ValueError:
            return
        except:
            showerror('Error', 'Animation not saved')

    def load(self):
        path = askopenfilename(title='Load Conversation', initialdir=self.last_path,
                               defaultextension='.convo', filetypes=[('Conversation File', '.convo')])
        if not path:
            return

        self.controller.load(path)
        try:
            pass
        except:
            showerror('Error', 'Animation not loaded')
            return

    def new(self):
        answer = askokcancel(title='New Animation', message='Create New Animation?')
        if answer:
            self.controller.new()
