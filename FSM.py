import abc
from AllLocations import *
from Actors import *
import Clock as clk
import Thresholds as th

# Main StateController Class
class StateController:
    # agent = Person()

    def __init__(self, agent):
        self.agent = agent
        self.currentState = Choose()
        self.stateInput = 0

    def Update(self):
        self.currentState.Do()

    def ChangeState(self, state):
        self.currentState = state
        self.currentState.stateController = self
        self.currentState.Enter()

    def ChoosePreferedState(self):
        if 0 <= clk.gameClock.GetHour() < 7:
            return self.agent.home
        if 7 <= clk.gameClock.GetHour() < 17:
            return self.agent.workplace
        if 17 <= clk.gameClock.GetHour() < 22:
            if self.agent.home.package.food < 10:
                return FindwithTag(4)
            else:
                return FindwithTag(3)
        if 22 <= clk.gameClock.GetHour() < 24:
            return self.agent.home
    
    def GetStats(self):
        print("energy" + str(self.agent.energy))
        print("hunger" + str(self.agent.hunger))
        print("food left" + str(self.agent.home.package.food))
        print("money" + str(self.agent.money))
        print("DOA" + str(self.agent.dead))
        print("Location" + str(self.agent.location.name))

# States
# ---------------------------------------------Parent
class State(abc.ABC):
    def __init__(self):

        self.stateController = None

    @abc.abstractmethod
    def OnMessage(self):
        pass
    @abc.abstractmethod
    def Do(self):
        pass

    @abc.abstractmethod
    def Enter(self):
        pass

    @abc.abstractmethod
    def Exit(self):
        pass

# ---------------------------------------------Choose
class Choose(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self, message):
        self.stateController.agent.HandleMessage(message)
        if self.stateController.agent.msgHandler.msgInbox[0].type == 1:

        if self.stateController.agent.msgHandler.msgInbox[0].type == 2:
            pass
        if self.stateController.agent.msgHandler.msgInbox[0].type == 3:
            pass

    def Do(self):
        self.energy = self.stateController.agent.energy
        self.hunger = self.stateController.agent.hunger
        self.money = self.stateController.agent.money
        self.boredom = self.stateController.agent.boredom
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location
        self.workPlace = self.stateController.agent.workplace

        th = 4
        #print("Do Gets Called: " + self.stateController.agent.location.name)
        if self.stateController.agent.dead == True:
            self.Exit(Dead())

        # if at home
        elif self.location.type == 1:
            if self.energy > th or self.hunger > th or self.money > th:
                if 0 <= clk.gameClock.GetHour() < 7 or 22 <= clk.gameClock.GetHour() < 24: #if best time
                    #print("is best time" + str(clk.gameClock.GetHour()))
                    self.Exit(Relax())
                else:
                    #print("is not best time: " + str(clk.gameClock.GetHour()))
                    self.Exit(Travel(self.stateController.ChoosePreferedState()))
            else:
                if self.energy < th and self.hunger < th:
                    self.Exit(Eat())

                elif self.energy < th <= self.hunger:
                    self.Exit(Sleep())

                elif self.stateController.agent.home.dishes > 5:
                    self.Exit(Clean())

                elif self.money < th <= self.hunger and self.energy < th:
                    self.Exit(Travel(self.workPlace))
                else:
                    print("ERROR! else gets called twice")

        # if at work
        elif self.location.type == 2:
            # ----------------------------------------------------------- check here for messages
            if self.energy > th or self.hunger > th: #if other needs satisfied
                print("at Work")
                if 7 <= clk.gameClock.GetHour() < 17: #if best time
                    print("good time")
                    if self.money < 1000:
                        print("work")
                        self.Exit(Work())
                    else:
                        self.Exit(Sleep())
                else:
                    self.Exit(Travel(self.stateController.ChoosePreferedState()))

            else:
                print("not at Work")
                if self.hunger < th:
                    self.Exit(Eat())

                elif self.energy < th:
                    self.Exit(Sleep())
                else:
                    print("Else get called")

        # if at fun
        elif self.location.type == 3:
            if self.energy > th or self.hunger > th or self.boredom > th:  # if other needs satisfied
                if 17 <= clk.gameClock.GetHour() < 22 and self.home.package.food < 6: # should check somewhere about if food at home.ll
                    if self.money > 5 and self.boredom < 10:
                        self.Exit(Eat)
                    elif self.boredom < 10:

                        self.stateController.agent.msgHandler.SendMsg(1, self.stateController.agent.GameID, self.stateController.agent.GameID, 0)
                        self.Exit(Relax())

                    else:
                        self.Exit(Sleep())
                else:
                    self.Exit(Travel(self.stateController.ChoosePreferedState()))

            else:
                if self.energy < th and self.hunger < th:
                    self.Exit(Eat())

                elif self.energy < th <= self.hunger:
                    self.Exit(Sleep())

        elif self.location.type == 4:
            print("im at store")
            if self.energy > th or self.hunger > th:  # if other needs satisfied
                print("ERROR 1")
                if self.stateController.agent.home.package.food > 7: #have enough food at home
                    self.Exit(Travel(self.stateController.ChoosePreferedState()))
                else:
                    print("ERROR 11")
                    self.Exit(Buy())
            else:
                print("ERROR 2")
                if self.energy < th and self.hunger < th:
                    self.Exit(Eat())

                elif self.energy < th <= self.hunger:
                    self.Exit(Sleep())
                    print("ERROR 22")
                else:
                    print("ERROR 23")

        else:
            self.Exit(Travel(self.home))

    def Enter(self):
        self.energy = None
        self.hunger = None
        self.money =  None
        self.location = None
        self.home = None
        self.workPlace = None

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Travel
class Travel(State):
    def __init__(self, destination):
        super().__init__()
        self.destination = destination

    def OnMessage(self):
        pass

    def Do(self):
        self.Exit(Choose())

    def Enter(self):
        self.stateController.agent.Travel(self.destination)

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Sleep
class Sleep(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self):
        pass

    def Do(self):
        self.energy = self.stateController.agent.energy
        self.hunger = self.stateController.agent.hunger
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location

        if self.location.type == 1: # at home
            if self.hunger < 4:
                self.Exit(Eat())
            elif self.energy >= 10:
                self.Exit(Choose())
            else:
                self.stateController.agent.Sleep()

        elif self.location.type == 2: # at work
            print("atWork")
            if self.hunger < 4:
                print("goeat")
                self.Exit(Eat())
            elif self.energy >= 10:
                print("goChoose")
                self.Exit(Choose())
            else:
                print("sleepwork")
                self.stateController.agent.Sleep()

        
        elif self.location.type == 3: # at fun
            print("atFun")
            if self.hunger < 4:
                self.Exit(Eat())
            elif self.energy >= 10:
                self.Exit(Choose())
            else:
                self.stateController.agent.Sleep()
            pass

        elif self.location.type == 4: # at store
            print("atStore")
            if self.hunger < 4:
                print("eat")
                self.Exit(Eat())
            elif self.energy >= 10:
                print("choose")
                self.Exit(Choose())
            else:

                self.stateController.agent.Sleep()


        else:
            print("passed")
            pass


    def Enter(self):
        self.stateController.agent.Think("I think im going to sleep at: " + str(self.stateController.agent.location.name))


    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Eat
class Eat(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self):
        pass

    def Do(self):
        self.hunger = self.stateController.agent.hunger
        self.energy = self.stateController.agent.energy
        self.money = self.stateController.agent.money
        self.foodLeft = self.stateController.agent.home.package.food
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location
        # ---------------------------------------------Eat HOME
        if self.location.type == 1:
            if self.energy < 4 and self.hunger >= 4:
                self.Exit(Sleep())
            elif self.hunger >= 10:
                self.Exit(Choose())
            elif self.foodLeft <= 4:
                closestStore = FindwithTag(4)
                self.Exit(Travel(closestStore))
            else:
                self.stateController.agent.Eat()

        # ---------------------------------------------Eat WORK
        elif self.location.type == 2:
            if self.money < 5:
                print("i dont have enough money so i will eat at home")
                if self.foodLeft == 0:
                    self.Exit(Travel(FindwithTag(4)))
                else:
                    self.Exit(self.home)

            else:
                if self.energy < 4 and self.hunger >= 4:
                    self.Exit(Sleep())
                elif self.hunger >= 10:
                    self.Exit(Choose())
                else:
                    self.stateController.agent.EatWork()

        # ---------------------------------------------Eat FUN
        elif self.location.type == 3:
            if self.money < 5:
                print("i dont have enough money so i will eat at home")
                if self.foodLeft == 0:
                    self.Exit(Travel(FindwithTag(4)))
                else:
                    self.Exit(Travel(self.home))

            else:
                if self.energy < 4 and self.hunger >= 4:
                    self.Exit(Sleep())
                elif self.hunger >= 10:
                    self.Exit(Choose())
                else:
                    self.stateController.agent.EatFun()

        # ---------------------------------------------Eat STORE
        elif self.location.type == 4:
            print("food gets called at store")
            if self.money < 5:
                print("i dont have enough money so i will eat at home")
                if self.foodLeft == 0:
                    self.Exit(Buy())
                else:
                    self.Exit(Travel(self.home))
            else:
                if self.energy < 4 and self.hunger >= 4:
                    print("self.energy and")
                    self.Exit(Sleep())
                elif self.hunger >= 10:
                    print("self.hunger >= 10")
                    self.Exit(Choose())
                elif self.foodLeft <= 4:
                    print("self.foodLeft <= 4:")
                    self.Exit(Buy())
                else:
                    print("eatstore gets called")
                    self.stateController.agent.EatStore()
        else:
            print("food called on location without food function")
            pass


    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Clean
class Clean(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self):
        pass

    def Do(self):
        self.Energy = self.stateController.agent.hunger
        self.Hunger = self.stateController.agent.energy
        self.dishes = self.stateController.agent.location.package.dishes

        if self.Energy < 4 and self.Hunger < 4:
            self.Exit(Eat())
        elif self.Energy < 4 and self.Hunger >= 4:
            self.Exit(Sleep())
        elif self.dishes == 0:
            self.Exit(Choose())
        else:
            self.stateController.agent.Clean()

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Relax
class Relax(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self):
        pass

    def Do(self):
        self.hunger = self.stateController.agent.hunger
        self.energy = self.stateController.agent.energy
        self.dishes = self.stateController.agent.home.package.dishes
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location

        if self.location.type == 1:
            if self.energy < 4 or self.hunger < 4 or self.dishes > 4:
                if self.hunger < 4:
                    self.Exit(Eat())

                elif self.energy < 4:
                    self.Exit(Sleep())

                elif self.dishes > 4:
                    self.Exit(Clean())
                else:
                    pass
            else:
                self.stateController.agent.Relax()

        elif self.location.type == 3:
            if self.energy > 4 or self.hunger > 4:
                self.stateController.agent.Relax()
            else:
                if self.hunger < 4:
                    self.Exit(Eat())

                elif self.energy < 4:
                    self.Exit(Sleep())




    def Enter(self):
        pass

    def Exit(self, state):

        self.stateController.ChangeState(state)

# ---------------------------------------------Work
class Work(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self, message):
        self.Energy = self.stateController.agent.hunger
        self.Hunger = self.stateController.agent.energy
        self.money = self.stateController.agent.money
        if self.Hunger <= th.lowHunger or self.Energy <= th.lowSleep:
            print("")
            pass
        else:
            self.stateController.agent.msgHandler.HandleMessage(message)

    def Do(self):
        self.Energy = self.stateController.agent.hunger
        self.Hunger = self.stateController.agent.energy
        self.money = self.stateController.agent.money

        if self.Energy < 4 and self.Hunger < 4:
            self.Exit(Eat())
        elif self.Energy < 4 and self.Hunger >= 4:
            self.Exit(Sleep())
        elif self.money >= 10000:
            self.Exit(Choose())
        else:
            self.stateController.agent.Work()

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Buy
class Buy(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self):
        pass

    def Do(self):
        self.energy = self.stateController.agent.energy
        self.hunger = self.stateController.agent.hunger
        self.money = self.stateController.agent.money
        self.foodLeft = self.stateController.agent.home.package.food
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location
        self.workPlace = self.stateController.agent.workplace
        if self.energy < 4 and self.foodLeft > 6: #im tired and i already have food at home
            self.Exit(Travel(self.home))
        elif self.hunger < 4 and self.foodLeft > 6:
            self.Exit(Eat())
        else:
            self.stateController.agent.Buy()

    def Enter(self):

        self.energy = None
        self.hunger = None
        self.money =  None
        self.location = None
        self.home = None
        self.workPlace = None
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Dead
class Dead(State):
    def __init__(self):
        super().__init__()

    def OnMessage(self):
        pass

    def Do(self):
        print("die hard")
        print(self.agentName + " has DIED")
        pass

    def Enter(self):
        self.agentName = self.stateController.agent.fName
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

class Socialize(State):
    pass
