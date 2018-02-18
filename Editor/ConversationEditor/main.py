from Editor.ConversationEditor.editor import ConversationEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'conversation_editorrrrr'
TITLE = 'Convrsation Editor'
EXTENSION = 'conv'
FILE_TYPE = 'Conversation'

if __name__ == '__main__':
    run_simple_editor(ConversationEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
