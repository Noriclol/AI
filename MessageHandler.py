from Enums import Message
import Clock as clk
class MessageHandler:
    def __init__(self):
        self.msgInbox = []

    def UpdateMsgHandler(self):
        pass

    def SendMsg(self, type, SenderID, RecieverID, Delay, Data=None):
        self.message = Message(type, SenderID, RecieverID, Delay, Data)
        if self.message.delay is 0:
            # send message

            pass
        elif time == clk.GetTime:
            # send later

            pass
        return Message

    def Send(self, type, toPerson):
        msg = self.CreateMsg(type, toPerson)
        toPerson.msgHandler.Recieve(msg)

    def Resend(self, msg):


    def Recieve(self, message):
        self.msgInbox.append(message)
        pass

    def getRecipiants(self):
        RecipiantList = []
        for person in self.agent.list:
            if person.GameID == self.agent.GameID:
                pass
            else:
                RecipiantList.append(person)
        return RecipiantList


class Message:
    def __init__(self, Type, SenderID, RecieverID, Delay, Data):
        self.sender = SenderID
        self.reciever = RecieverID
        self.type = Type
        self.delay = Delay
        self.data = Data

    def PrintMessage(self):
        print("To: " + str(self.reciever.fName))
        print("From: " + str(self.sender.fName))
        print("MessageType: " + str(self.type.fName))

msgHandler = MessageHandler()