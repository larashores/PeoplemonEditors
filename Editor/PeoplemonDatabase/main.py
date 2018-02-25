from Editor.PeoplemonDatabase.editor import PeoplemonEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'peoplemon_editoror'
TITLE = 'Peoplemon Database Editor'
EXTENSION = 'db'
FILE_TYPE = 'Peoplemon'

if __name__ == '__main__':
    run_simple_editor(PeoplemonEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
