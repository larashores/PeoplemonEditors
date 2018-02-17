from Editor.saveable.composite import Composite
from Editor.saveable.saveableInt import saveable_int
from Editor.saveable.saveableArray import array
from Editor.saveable.saveableString import SaveableString


class Song(SaveableString):
    def __str__(self):
        return '"' + self.get() + '"'


class Playlist(array(Song)):
    pass
