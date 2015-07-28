'''
#-------------------------------------------------------------------------------
# Name:        entrylabel.py

# Author:      Vincent
#
# Date Created:     01/15/2015
# Date Modified:    01/15/2015
#-------------------------------------------------------------------------------

Purpose:    EntryLabel widget

'''

from tkinter import *

def keyExtract(keys, kwargs):
    '''
    Extracts keys from a keyword dict for use with widgets
    '''
    values = []
    for key in keys:
        if key in kwargs:
            values.append(kwargs[key])
            kwargs.pop(key)
        else:
            values.append(None)
    return tuple(values)

class EntryLabel(Frame):
    '''
    Entry with a Label above.
    '''
    def __init__(self,parent=None,**kwargs):

        f_dict ,e_dict = self.getArgs(kwargs)
        Frame.__init__(self,parent,**f_dict)
        self.enabled = True
        self.label = Label(self,**kwargs)
        self.label.pack(fill=X)
        self.entry = Entry(self,justify=CENTER,**e_dict)
        self.entry.pack()
    def getArgs(self,kwargs):
        '''
        Returns kwarg dicts for the Frame and Entry respectively
        '''
        f_height, f_width = keyExtract(('f_height','f_width'),kwargs)
        e_height, e_width, var = keyExtract(('e_height','e_width','textvariable'),kwargs)
        f_dict = {'height':f_height,'width':f_width}
        e_dict = {'height':e_height,'width':e_width,'textvariable':var}
        return f_dict, e_dict,
    def toggleState(self):
        if self.enabled:
            self.entry.config(state=DISABLED)
            self.label.config(state=DISABLED)
        else:
            self.entry.config(state=NORMAL)
            self.label.config(state=NORMAL)
        self.enabled = not self.enabled
    def get(self):
        return self.entry.get()