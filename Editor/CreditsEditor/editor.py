import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor

from Editor.CreditsEditor.saveables import *
from Editor.guicomponents.entrylabel_ttk import EntryLabel
from Editor.guicomponents.listchoice import ListChoice
from Editor.guicomponents.integercheck import intValidate
from Editor.guicomponents.multiwidget import MultiWidget
from Editor.utilities.arrayconnector import ArrayConnector
from Editor.utilities.addbuttonconnector import AddButtonConnector
from Editor.utilities.make_var import make_str_var, make_int_var
from Editor.signal import Signal


class CreditsEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        title = ttk.Label(self, text='Credits Editor', style='Title.TLabel')
        self.checkVar = tk.IntVar()
        chk = ttk.Checkbutton(self, text='Add Before?', variable=self.checkVar)
        self.list = ListChoice(self)
        butFrame = ttk.Frame(self)
        self.add_text_button = ttk.Button(butFrame, text='Add Text', width=14)
        self.add_image_button = ttk.Button(butFrame, text='Add Image', width=14)
        entry_frm = ttk.Frame(self)
        self.x_pos = EntryLabel(entry_frm, text='X Position')
        self.y_buf = EntryLabel(entry_frm, text='Y Buffer')

        self.multi_widget = MultiWidget(self)

        title.pack()
        chk.pack()
        self.list.pack(expand=tk.YES, fill=tk.BOTH)
        butFrame.pack(fill=tk.X, pady=(5, 5))
        self.add_text_button.pack(side=tk.LEFT, padx=10, expand=tk.YES)
        self.add_image_button.pack(side=tk.LEFT, padx=10, expand=tk.YES)

        entry_frm.pack(fill=tk.X)
        self.x_pos.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, padx=5)
        self.y_buf.pack(side=tk.LEFT, expand=tk.YES, fill=tk.X, padx=5)
        self.multi_widget.pack(fill=tk.BOTH)

        intValidate(self.x_pos.entry, 'u16')
        intValidate(self.y_buf.entry, 'u16')


class TextEditorGUI(ttk.Frame):
    def __init__(self, parent=None, **kwargs):
        ttk.Frame.__init__(self, parent, **kwargs)
        self.colors = (0, 0, 0)
        self.signal_color_selected = Signal()

        color_frm = ttk.Frame(self)
        self.text = EntryLabel(self, text='Text')
        self.size = EntryLabel(self, text='Font Size')
        self.color_button = ttk.Button(color_frm, text='Color', command=self.choose_color)
        self.color_preview = tk.Canvas(color_frm, width=90, height=20, bg=self.rgb_to_hex(0, 0, 0), relief=tk.GROOVE,
                                       bd=5, highlightthickness=0)

        self.text.pack(fill=tk.X)
        self.size.pack(fill=tk.X)
        color_frm.pack(expand=tk.YES)
        self.color_button.pack(padx=10, pady=(5, 0), side=tk.LEFT)
        self.color_preview.pack(padx=10, pady=(5, 0), side=tk.LEFT)

        intValidate(self.size.entry, 'u16')

    def choose_color(self):
        rgb, color = askcolor(self.rgb_to_hex(*self.colors), title='Choose Text color')
        if rgb:
            self.colors = [int(c) for c in rgb]
            self.signal_color_selected(*self.colors)

    def change_color(self, r, g, b):
        self.color_preview.configure(bg=self.rgb_to_hex(r, g, b))

    @staticmethod
    def rgb_to_hex(r, g, b):
        return '#%02x%02x%02x' % (r, g, b)


class ImageEditorGUI(ttk.Frame):
    def __init__(self, parent=None):
        ttk.Frame.__init__(self, parent)
        self.path = EntryLabel(self, text='Image Path')

        self.path.pack(expand=tk.YES, fill=tk.X)


class CreditsEditor:
    TYPE_MAP = {ImageType: ImageEditorGUI, TextType: TextEditorGUI}

    def __init__(self, parent=None):
        self.gui = CreditsEditorGUI(parent)
        self.credits = array(Credit)()
        self.main_saveable = self.credits

        self.array_connector = ArrayConnector(self.credits, self.gui.list, None, self.gui.x_pos, self.gui.y_buf)
        self.add_button_connector = AddButtonConnector(self.credits, self.gui.list,
                                                       {self.gui.add_text_button: TextType,
                                                        self.gui.add_image_button: ImageType})

        self.add_button_connector.signal_about_to_add.connect(self.on_credit_about_to_add)
        self.gui.list.signal_select.connect(self.credit_changed)
        self.gui.list.signal_delete.connect(self.on_delete)
        self.credits.signal_add.connect(self.on_credit_add)

    @staticmethod
    def on_credit_about_to_add(credit, type):
        credit.type.set(type)

    def on_delete(self):
        if not len(self.gui.list):
            self.gui.multi_widget.change_widget(None)

    def credit_changed(self, ind):
        current = self.array_connector.cur_selection
        self.gui.multi_widget.change_widget(self.TYPE_MAP[current.type.get()])
        widget = self.gui.multi_widget.current_widget
        if current.type.get() == ImageType:
            widget.path.entry.configure(textvariable=make_str_var(current.type.image))
        elif current.type.get() == TextType:
            text_credit = current.type.text
            widget.text.entry.configure(textvariable=make_str_var(text_credit.text))
            widget.size.entry.configure(textvariable=make_int_var(text_credit.size))
            widget.signal_color_selected.connect(self.on_color_selected)
            for saveable in (text_credit.blue,):
                saveable.signal_changed.connect(self.on_color_changed)
            self.on_color_changed(None)
        self.gui.x_pos.entry.config(textvariable=make_int_var(current.x))
        self.gui.y_buf.entry.config(textvariable=make_int_var(current.y_buf))

    def on_color_selected(self, r, g, b):
        current = self.array_connector.cur_selection
        current.type.text.red = r
        current.type.text.green = g
        current.type.text.blue = b

    def on_color_changed(self, val):
        text_credit = self.array_connector.cur_selection.type.text
        r, g, b = text_credit.red.get(), text_credit.green.get(), text_credit.blue.get()
        self.gui.multi_widget.current_widget.change_color(r, g, b)
        self.gui.list.itemconfig(self.gui.list.get_selection(), foreground=TextEditorGUI.rgb_to_hex(r, g, b))

    def on_credit_add(self, ind, val):
        if val.type.get() == TextType:
            text = val.type.text
            self.gui.list.itemconfig(ind,
                                     foreground=TextEditorGUI.rgb_to_hex(
                                         text.red.get(), text.green.get(), text.blue.get()))

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)
