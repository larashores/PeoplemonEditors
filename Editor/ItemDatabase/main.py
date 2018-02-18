from Editor.ItemDatabase.editor import ItemEditor

from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'item editorrrr'
TITLE = 'Item Database Editor'
EXTENSION = 'db'
FILE_TYPE = 'Item Database'

if __name__ == '__main__':
    run_simple_editor(ItemEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
