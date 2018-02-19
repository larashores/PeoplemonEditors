from tkinter import ttk
import tkinter as tk


class MultiWidget(ttk.Frame):
    def __init__(self, parent=None, current_widget=None, pack_dict=None):
        ttk.Frame.__init__(self, parent)
        self.pack_dict = pack_dict
        if pack_dict is None:
            pack_dict = {}
        self.pack_dict = pack_dict
        self.current_widget = None
        if current_widget is not None:
            self.current_widget = current_widget
            self.current_widget.pack()

    def change_widget(self, WidgetType):
        if type(self.current_widget) == WidgetType:
            return False
        if self.current_widget:
            self.current_widget.destroy()
        if WidgetType is None:
            self.current_widget = ttk.Frame(self)
            self.current_widget.pack(expand=tk.YES, fill=tk.BOTH)
            return True
        self.current_widget = WidgetType(self)
        padx = None
        pady = None
        expand = tk.YES
        fill = tk.BOTH
        if WidgetType in self.pack_dict:
            dict_ = self.pack_dict[WidgetType]
            if 'padx' in dict_:
                padx = dict_['padx']
            if 'pady' in dict_:
                pady = dict_['pady']
            if 'fill' in dict_:
                fill = dict_['fill']
            if 'expand' in dict_:
                expand = dict_['expand']
        self.current_widget.pack(expand=expand, fill=fill, padx=padx, pady=pady)
        return True

