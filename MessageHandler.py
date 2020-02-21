from Enums import Message

class MessageHandler:
    def __init__(self, agent):
        self.agent = agent
        self.msgInbox = None
        self.msgOutbox = None

    def CreateMsg(self, type):
        self.message = Message(type)
        self.message.messageHandler = self
        self.msgOutbox.append(Message)
        return Message

    def GetMsg(self, message):
        self.msgInbox.append(message)

    def Send(self, toPerson, type):
        msg = self.CreateMsg(type)
        toPerson.msgHandler.Recieve(toPerson.GameID, msg)

    def Recieve(self, fromPerson, message):
        self.msgInbox.append(fromPerson, message)
    pass


class Message:
    def __init__(self, type):
        self.messageHandler = None
        self.sender = None
        self.reciever = None
        self.type = type

    def Printmessage(self):
        print("To: " + str(self.reciever.fName))