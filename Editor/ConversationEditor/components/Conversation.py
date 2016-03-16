__author__ = 'Vincent'

from Editor.Component_new import Component
from Editor.structreader import pack, unpack
from Editor.ConversationEditor.components.lines import BaseLine

class Conversation(Component):
    def __init__(self):
        Component.__init__(self)
        self.addParam('lines', [])

    def toByteArray(self):
        data = bytearray()
        pack(data, len(self['lines']), 'u16')
        for line in self['lines']:
            data += line.toByteArray()
        return data

    @staticmethod
    def fromByteArray(byteArray):
        num_lines = unpack(byteArray, 'u16')
        conversation = Conversation()
        for _ in range(num_lines):
            conversation['lines'].append(BaseLine.fromByteArray(byteArray))

        return conversation