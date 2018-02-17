from Editor.TrainerEditor.editor import TrainerEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'trainereditorrrr'
TITLE = 'Trainer Editor'
EXTENSION = 'trainer'
FILE_TYPE = 'Trainer'

if __name__ == '__main__':
    run_simple_editor(TrainerEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
