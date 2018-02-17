from Editor.NPCEditor.editor import NpcEditor
from Editor.utilities.simple_editor import run_simple_editor

LOCATION = 'npc_editorrr'
TITLE = 'NPC Editor'
EXTENSION = 'npc'
FILE_TYPE = 'NPC'

if __name__ == '__main__':
    run_simple_editor(NpcEditor, TITLE, EXTENSION, FILE_TYPE, LOCATION)
