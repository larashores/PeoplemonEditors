from Editor.TrainerPeoplemonEditor.editor import TrainerPeoplemonEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'trainerpeoplemoneditor'
TITLE = 'Trainer Peoplemon Editor'
EXTENSION = 'ppl'
FILE_TYPE = 'Trainer Peoplemon'

if __name__ == '__main__':
    run_simple_editor(TrainerPeoplemonEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)