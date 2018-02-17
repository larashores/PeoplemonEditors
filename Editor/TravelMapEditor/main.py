from Editor.TravelMapEditor.editor import TravelEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'travelmapeditor'
TITLE = 'Travel Map Editor'
EXTENSION = 'map'
FILE_TYPE = 'Travel Map'


if __name__ == '__main__':
    run_simple_editor(TravelEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)