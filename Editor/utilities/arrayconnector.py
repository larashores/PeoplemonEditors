import tkinter as tk

class ArrayConnector:
    def __init__(self, array, list_choice, add_button=None, *editing_widgets):
        self._array = array
        self._list_choice = list_choice
        self._editing_widgets = [x for x in editing_widgets]
        self.cur_selection = None

        array.signal_add.connect(self.on_added)
        array.signal_remove.connect(self.on_removed)
        list_choice.signal_select.connect(self.on_select)
        list_choice.signal_delete.connect(self.on_delete_pressed)
        if add_button:
            add_button.config(command=self.on_add_clicked)

        self._enable_set(False)

        self._list_choice.clear()
        for obj in self._array:
            self._list_choice.append(str(obj), obj)

    def _enable_set(self, enable):
        for widget in self._editing_widgets:
            try:
                widget.config(state=tk.NORMAL if enable else tk.DISABLED)
            except:
                widget.state(('!disabled' if enable else 'disabled', ))

    def disconnect(self):
        self._array.signal_add.disconnect(self.on_added)
        self._array.signal_remove.disconnect(self.on_removed)
        self._list_choice.signal_select.disconnect(self.on_select)
        self._list_choice.signal_delete.disconnect(self.on_delete_pressed)

    def clear_editing_widgets(self):
        self._editing_widgets.clear()

    def add_editing_widgets(self, *widget):
        if widget not in self._editing_widgets:
            self._editing_widgets.extend(widget)

    def on_added(self, ind, val):
        self._list_choice.insert(ind, str(val), val)

    def on_removed(self, ind, val):
        self._list_choice.pop(ind)
        self._enable_set(False)
        if len(self._array):
            self._list_choice.set_selection(-1)

    def on_add_clicked(self):
        self._array.append(self._array.array_type())
        self._list_choice.set_selection(-1)

    def on_delete_pressed(self):
        self._array.pop(self._list_choice.get_selection())

    def on_change(self, val):
        ind = self._list_choice.get_selection()
        self._list_choice.update_str(ind, str(self._array[ind]))

    def on_select(self, ind):
        if ind is not None:
            if self.cur_selection is not None:
                self.cur_selection.signal_changed.disconnect(self.on_change)
            self.cur_selection = self._array[ind]
            self.cur_selection.signal_changed.connect(self.on_change)
            self._enable_set(True)
