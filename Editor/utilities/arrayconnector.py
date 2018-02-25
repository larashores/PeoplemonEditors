import tkinter as tk


class ArrayConnector:
    def __init__(self, array, sorted_choice, add_button=None, *editing_widgets):
        self._array = array
        self._sorted_choice = sorted_choice
        self._editing_widgets = [x for x in editing_widgets]
        self.cur_selection = None

        array.signal_add.connect(self._on_added)
        array.signal_remove.connect(self._on_removed)
        sorted_choice.signal_select.connect(self._on_select)
        sorted_choice.bind('<Delete>', lambda event: self._on_delete_pressed())
        if add_button:
            add_button.config(command=self._on_add_clicked)

        self._enable_set(False)
        self._sorted_choice.clear()
        for obj in self._array:
            self._sorted_choice.append(obj)

    def disconnect(self):
        self._array.signal_add.disconnect(self._on_added)
        self._array.signal_remove.disconnect(self._on_removed)
        self._sorted_choice.signal_select.disconnect(self._on_select)
        self._sorted_choice.signal_delete.disconnect(self._on_delete_pressed)

    def clear_editing_widgets(self):
        self._editing_widgets.clear()

    def add_editing_widgets(self, *widget):
        if widget not in self._editing_widgets:
            self._editing_widgets.extend(widget)

    def _on_added(self, ind, val):
        self._sorted_choice.insert(ind, val)

    def _on_removed(self, ind, val):
        self._sorted_choice.pop(ind)
        if len(self._sorted_choice):
            self._sorted_choice.set_selection(ind)

    def _on_add_clicked(self):
        self._array.append(self._array.array_type())
        self._sorted_choice.set_selection(-1)

    def _on_delete_pressed(self):
        selection = self._sorted_choice.get_selection()
        if selection is not None:
            self._array.pop(selection)

    def _on_select(self, ind):
        if ind is None:
            self._enable_set(False)
            return
        if self.cur_selection is not None:
            self.cur_selection.signal_changed.disconnect(self._on_change)
        self.cur_selection = self._array[ind]
        self.cur_selection.signal_changed.connect(self._on_change)
        self._enable_set(True)

    def _on_change(self, *args):
        ind = self._sorted_choice.get_selection()
        self._sorted_choice.update_line(ind, self._array[ind])

    def _enable_set(self, enable):
        for widget in self._editing_widgets:
            try:
                widget.config(state=tk.NORMAL if enable else tk.DISABLED)
            except:
                widget.state(('!disabled' if enable else 'disabled', ))
