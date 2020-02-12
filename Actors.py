import FSM
import MessageHandler
import numpy as np
from Location import *
import abc


class BaseGameEntity(abc.ABC):

    def __init__(self, list):

        self.GameID = len(list)

    @abc.abstractmethod
    def EntityUpdate(self):
        pass

    @abc.abstractmethod
    def EntityInit(self):
        pass

    @abc.abstractmethod
    def EntityMessageReciever(self):
        pass

class Person(BaseGameEntity):
    def __init__(self ,list, currentHome, currentWorkplace, fName = "john", lName = "Smith"):
        super().__init__(list)
        print("init Person")
        self.fName = fName
        self.lName = lName
        self.money = 10
        self.hunger = 10
        self.boredom = 10
        self.energy = 10
        self.location = currentHome
        self.home = currentHome
        self.workplace = currentWorkplace

        self.GameID = len(list)
        list.append(self)

        self.stateMachine = FSM.StateController(self)
        self.msgHandler = MessageHandler.MessageHandler(self)
        self.dead = False



    def EntityInit(self):
        self.stateMachine.ChangeState(FSM.Choose())

    def EntityUpdate(self):
        self.stateMachine.Update()
    # Communication

    def EntityMessageReciever(self):
        pass

    def Think(self, text):
        print(self.fName + ": " + text)

    def Say(self, text, otherPerson):
        print(self.fName + "(Says): " + text + " (to) " + otherPerson)

    # StateAction

    def Travel(self, newLocation):
        self.location = newLocation
        self.location = self.location
        print("traveling to " + self.location.name)

    # --------------Sleep Actions
    def Sleep(self):
        if self.energy < 10:
            self.energy += 2
            self.hunger -= 1
            self.Think("ZZZZzzzz: " + str(self.energy))
        else:
            print("sleep full" + str(self.energy))

    def Slack(self):
        self.hunger -= 1
        self.energy += 1
        self.Think("slacking at work")

    # --------------Eat Actions
    def Eat(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 1
            self.home.package.food -= 1
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))

    def EatFun(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 1
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))

    def EatStore(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 1
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))

    def EatWork(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 5
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))

    def EatShop(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 5
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))

    # ----------------Relax Actions
    def Relax(self):
        self.Think("Relaxing")
        self.hunger -= 1
        self.energy -= 1

    def RelaxBar(self):
        self.Think("Relaxing at bar")

    # ----------------home specific
    def Clean(self):
        if self.home.package.dishes <= 0:
            self.energy -= 1
            self.hunger -= 1
            self.home.package.CleanDish()
            self.Think("cleaning dishes")
            self.Think("dishes left: " + str(self.home.package.dishes))
        else:
            print("no dishes left: "  + str(self.home.package.dishes))

    # ---------------- work specific
    def Work(self):
        self.money += 2
        self.boredom -= 1
        self.hunger -= 1
        self.Think("Getting that bread")

    # ---------------- fun specific
    def Hangout(self):
        self.Think("Hanging out")
        self.boredom -= 1

    # ----------------- shop specific
    def Buy(self):
        self.Think("Buying food")
        self.hunger -= 1
        self.energy -= 1
        self.home.package.food += 8

    #------------------ social
    def CallFriend(self):
        self.Think("Calling Friend")
        pass

    #-----------------Dead specific
    def DeadCheck(self):
        if self.hunger <= 0 or self.energy <= 0:
            self.dead = True