from Editor.PlaylistEditor.editor import PlaylistEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'playlisteditorrr'
TITLE = 'Playlist Editor'
EXTENSION = 'playlist'
FILE_TYPE = 'Playlist'

if __name__ == '__main__':
    run_simple_editor(PlaylistEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
