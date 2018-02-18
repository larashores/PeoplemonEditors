from Editor.MoveDatabase.editor import MoveEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'move_EDITORADF'
TITLE = 'Move Editor'
EXTENSION = 'db'
FILE_TYPE = 'Move Database'

if __name__ == '__main__':
    run_simple_editor(MoveEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
