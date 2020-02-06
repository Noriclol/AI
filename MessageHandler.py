from Enums import Message

class MessageHandler:
    def __init__(self, agent):
        self.agent = agent
        self.msgInbox = None
        self.msgOutbox = None

        def CreateMsg( type):
            self.msgOutbox.append(type)

        def GetMsg(type):
            self.msgInbox.append(type)

        def Send(toPerson, type):
            msg = CreateMsg(type)
            toPerson.msgHandler.Recieve(toPerson, type)

        def Recieve(fromPerson, type):
            pass
    pass


class Message:
    def __init__(self, type):
        self.messageHandler = None
        self.type = type