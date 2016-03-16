"""
#-------------------------------------------------------------------------------
# Name:        module1

# Author:      Vincent
#
# Date Created:     01/26/2015
# Date Modified:    01/26/2015
#-------------------------------------------------------------------------------

Conversation save format:
u16                            numLines
for (numLines)
{
      char                     code
      if (code=='t') //talk
          string               line

      if (code=='o') //option
          string               line
          u16                  numOptions
          for (numOptions)
                string         line
                string         gotoLineIfPicked

       if (code=='g') //give
           u8                  isItem
           u16                 moneyOrItemId

       if (code=='r') //take
           u8                  isItem
           u16                 moneyOrItemId
           string              failLine

       if (code=='j') //jump
           string              gotoLine

       if (code=='s') //save a string
           string              value

       if (code=='c') //check if string has been saved in the past
           string              value
           string              failLine

       if (code=='l') //jump point
           string              labelName  /*note, attempting to "jump" to a
                                            label that doesn't exist will
                                            terminate the conversation*/

       if (code=='w') /*go to failLine if the player has already talked to this
                        npc*/
           string              failLine
}

"""

from Editor.ConversationEditor.components.Conversation import Conversation


class Controller:
    def __init__(self):
        self.conversation = Conversation()
        self.load_func = lambda: None

    def __iter__(self):
        for line in self.conversation['lines']:
            yield line

    def addLine(self, ind, line):
        """
        Purpose: Adds line to conversation at index ind
        Inputs:
            ind:    Index to add line at ('end' adds to end)
            line:   Line object
        """
        if ind == 'end':
            self.conversation['lines'].append(line)
        else:
            self.conversation['lines'].insert(ind, line)

    def deleteLine(self, ind):
        """
        Purpose: Deletes line at index ind
        Inputs:
            ind:    Index to delete line from
        """
        self.conversation['lines'].pop(ind)

    def get_line(self, ind):
        return self.conversation['lines'][ind]

    def update(self):
        self.load_func()

    def get_length(self):
        return len(self.conversation['lines'])

    def save(self, file_name):
        data = self.conversation.toByteArray()
        file = open(file_name, 'wb')
        file.write(data)
        file.close()

    def load(self, file_name):
        file = open(file_name, 'rb')
        data = bytearray(file.read())
        self.conversation = Conversation.fromByteArray(data)
        self.update()

    def new(self):
        self.conversation = Conversation()
        self.update()
