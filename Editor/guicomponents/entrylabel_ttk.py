__author__ = 'Vincent'

from tkinter import *
from tkinter import ttk

class EntryLabel(ttk.Frame):
    """
    Entry with a Label above.
    """
    def __init__(self, parent, anchor=CENTER, background=None, borderwidth=None, compound=None, cursor=None,
                 font=None, foreground=None, image=None, padding=None, relief=None, takefocus=None,
                 text=None, underline=None, width=20, height=None, wraplength=None,
                 exportselection=0, invalidatecommand=None, validatecommand=None, validate='none', show=None,
                 entry_variable=None, label_variable=None,
                 entry_style=None, label_style=None, label_justify=CENTER, entry_justify=CENTER):
        ttk.Frame.__init__(self, parent, height=height)
        frame = ttk.Frame(self)
        frame.pack(expand=YES, fill=X)

        self.enabled = True
        self.label = ttk.Label(frame, anchor=anchor, background=background, borderwidth=borderwidth, compound=compound,
                               cursor=cursor, font=font, foreground=foreground, image=image, justify=label_justify,
                               padding=padding, relief=relief, takefocus=takefocus, text=text,
                               textvariable=label_variable, underline=underline, wraplength=wraplength,
                               style=label_style)
        self.label.pack(fill=X)
        self.entry = ttk.Entry(frame, cursor=cursor, exportselection=exportselection, font=font,
                               invalidatecommand=invalidatecommand, justify=entry_justify, show=show, style=entry_style,
                               takefocus=takefocus, textvariable=entry_variable, validate=validate,
                               validatecommand=validatecommand, width=width)
        self.entry.pack()

    def state(self, statespec=None):
        self.label.state(statespec)
        self.entry.state(statespec)
        return ttk.Frame.state(self, statespec)

    def instate(self, statespec, callback=None, *args, **kw):
        return ttk.Frame.instate(self, statespec, callback, *args, **kw)

    def get(self):
        return self.entry.get()

    def insert(self, index, string):
        self.entry.insert(index, string)