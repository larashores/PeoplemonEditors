import tkinter as tk
from tkinter import ttk


class VariableText(ttk.Frame):
    def __init__(self, parent=None, *args, textvariable=None, **kwargs):
        ttk.Frame.__init__(self, parent)
        self._text = CustomText(self, *args, **kwargs)
        self._variable = None
        self._trace = None
        self._changing = False

        self._text.bind('<<TextModified>>', self._on_text_change)
        self._text.pack(expand=tk.YES, fill=tk.BOTH)

        self._set_text_variable(textvariable)

    def config(self, *args, **kwargs):
        if 'textvariable' in kwargs:
            self._set_text_variable(kwargs.pop('textvariable'))
        self._text.config(*args, **kwargs)

    def configure(self, *args, **kwargs):
        self.config(*args, **kwargs)

    def _on_var_change(self, _arg1, _arg2, _arg3):
        self._changing = True
        old_mark = self._text.index(tk.INSERT)
        self._text.delete(1.0, tk.END)
        self._text.insert(tk.END, self._variable.get())
        self._text.mark_set(tk.INSERT, old_mark)
        self._changing = False

    def _on_text_change(self, _event):
        if not self._changing and self._variable is not None:
            text = self._text.get(1.0, tk.END)[:-1]
            self._variable.set(text)

    def _set_text_variable(self, variable):
        self._variable = variable
        if self._trace:
            self._variable.trace_vdelete('w', self._trace)
            self._trace = None
        if self._variable:
            self._trace = variable.trace('w', self._on_var_change)
            self._on_var_change(None, None, None)


class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        try:
            result = self.tk.call(cmd)
        except tk.TclError:
            if command != 'delete' or args != (tk.SEL_FIRST, tk.SEL_LAST):
                raise
        else:
            if command in ("insert", "delete", "replace"):
                self.event_generate("<<TextModified>>")

            return result


if __name__ == '__main__':
    root = tk.Tk()
    var = tk.StringVar(root)
    text1 = VariableText(root, textvariable=var)
    text2 = VariableText(root, textvariable=var)
    text1.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    text2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
    root.mainloop()
