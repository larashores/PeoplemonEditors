from Editor.observable import Observable
from Editor.signal import Signal


class EditorModel(Observable):
    def __init__(self):
        Observable.__init__(self)
        self._current_frame = -1
        self.signal_frame_changed = Signal()

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, val):
        self._current_frame = int(val)
        self.signal_frame_changed(self._current_frame)
