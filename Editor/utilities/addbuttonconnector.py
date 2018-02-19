from Editor.signal import Signal


class AddButtonConnector:
    def __init__(self, array, list, button_args):
        self.signal_about_to_add = Signal()
        self.array = array
        self.list = list
        for button in button_args:
            button.configure(command=lambda button=button: self.on_add(button_args[button]))

    def on_add(self, args):
        obj = self.array.array_type()
        self.signal_about_to_add(obj, args)
        self.array.append(obj)
        self.list.set_selection(-1)
