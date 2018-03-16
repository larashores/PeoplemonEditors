from Editor.saveable.composite import Composite
from Editor.saveable.saveableString import SaveableString
from Editor.TrainerEditor.saveables import Behavior


class Npc(Composite):
    name = SaveableString
    animation = SaveableString
    convo_file = SaveableString
    behahavior = Behavior
