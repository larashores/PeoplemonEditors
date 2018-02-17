class ArrayConnector:
    def __init__(self, array, list_choice, add_button, *editing_widgets):
        self._array = array
        self._list_choice = list_choice
        self._editing_widgets = editing_widgets

        array.signal_add.connect(self.on_added)
        array.signal_remove.connect(self.on_removed)
        list_choice.signal_select.connect(self.on_select)
        list_choice.signal_delete.connect(self.on_delete_pressed)
        add_button.config(command=self.on_add_clicked)

    def on_added(self, ind, val):
        self._list_choice.insert(ind, str(val))

    def on_removed(self, ind, val):
        self._list_choice.pop(ind)
        for widget in self._editing_widgets:
            widget.state(('disabled', ))

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
            for widget in self._editing_widgets:
                widget.state(('!disabled', ))
