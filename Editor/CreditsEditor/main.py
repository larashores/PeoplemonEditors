from Editor.CreditsEditor.editor import CreditsEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'credits_editorrrr'
TITLE = 'Credits Editor'
EXTENSION = 'cr'
FILE_TYPE = 'Credits'

if __name__ == '__main__':
    run_simple_editor(CreditsEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
