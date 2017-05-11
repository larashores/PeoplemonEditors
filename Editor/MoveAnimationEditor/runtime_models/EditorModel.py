from Editor.observable import Observable


class EditorModel(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._current_frame = -1

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, val):
        self._current_frame = int(val)
        self.notify_observers(self._current_frame)