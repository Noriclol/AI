import FSM
import MessageHandler
import AllActors
import numpy as np
from Location import *


class Person:
    def __init__(self, currentHome, currentWorkplace, fName = "john", lName = "Smith"):
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

        self.PersonalID = AllActors.personlist.__sizeof__()
        AllActors.personlist.append(self)

        self.stateMachine = FSM.StateController(self)
        self.msgHandler = MessageHandler.MessageHandler(self)
        self.dead = False



    def PersonInit(self):
        self.stateMachine.ChangeState(FSM.Choose())

    def PersonUpdate(self):
        self.stateMachine.Update()
    # Communication

    def Think(self, text):
        print(self.fName + ": " + text)

    def Say(self, text, otherPerson):
        print(self.fName + "(Says): " + text + " (to) " + otherPerson)

    # StateAction

    def Travel(self, newLocation):
        self.location = newLocation
        self.location = self.location
        print("traveling to " + self.location.name)

    def Sleep(self):
        if self.energy < 10:
            self.energy += 2
            self.hunger -= 1
            self.Think("ZZZZzzzz: " + str(self.energy))
        else:
            print("sleep full" + str(self.energy))
            pass
    def EatOut(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 1
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))
    def Eat(self):
        if self.hunger < 10:
            self.hunger += 5
            self.energy += 1
            self.home.package.food -= 1
            self.Think("nom nom : " + str(self.hunger))
        else:
            print("hunger full: " + str(self.hunger))

    def Clean(self):
        if self.home.package.dishes <= 0:
            self.energy -= 1
            self.hunger -= 1
            self.home.package.CleanDish()
            self.Think("cleaning dishes")
            self.Think("dishes left: " + str(self.home.package.dishes))
        else:
            print("no dishes left: "  + str(self.home.package.dishes))

    def WorkHard(self):
        self.money += 2
        self.boredom -= 1
        self.hunger -= 1
        self.Think("Getting that bread")

    def Slack(self):
        self.hunger -= 1
        self.energy += 1
        self.Think("slacking at work")

    def CallFriend(self):
        self.Think("Calling Friend")
        pass

    def Hangout(self):
        self.Think("Hanging out")
        self.boredom -= 1

    def Relax(self):
        self.Think("Relaxing")
        self.hunger -= 1
        self.energy -= 1

    def Buy(self):
        self.hunger -= 1
        self.energy -= 1
        self.home.package.food += 8

    def DeadCheck(self):
        if self.hunger <= 0 or self.energy <= 0:
            self.dead = True