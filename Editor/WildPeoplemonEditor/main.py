from Editor.utilities.simple_editor import run_simple_editor
from WildPeoplemonEditor.editor import WildEditor

LOCATION = 'wildpeoplemoneditor'
TITLE = 'Wild Peoplmon Editor'
EXTENSION = 'ppl'
FILE_TYPE = 'Wilk Peoplemon'


if __name__ == '__main__':
    run_simple_editor(WildEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)