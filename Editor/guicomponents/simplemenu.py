import tkinter as tk
from Editor.signal import Signal


class SimpleMenu(tk.Menu):
    def __init__(self, *args, **kwargs):
        tk.Menu.__init__(self, *args, **kwargs)
        self._signals = []

    def add_action(self, name, add_action=None):
        signal = Signal()
        self._signals.append(signal)
        self.add_command(label=name, command=lambda: signal())
        if add_action is not None:
            signal.connect(add_action)
        return signal