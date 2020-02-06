import abc
from AllLocations import *
from Actors import *


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


    def Do(self):
        self.energy = self.stateController.agent.energy
        self.hunger = self.stateController.agent.hunger
        self.money = self.stateController.agent.money
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location
        self.workPlace = self.stateController.agent.workplace

        th = 4
        print("Do Gets Called: " + self.stateController.agent.location.name)
        if self.stateController.agent.dead == True:
            self.Exit(Dead())
        elif self.location.name == self.home.name and self.location.type == 1:
            print("is home")
            if self.energy > th or self.hunger > th or self.money > th:
                print("relaxes")
                self.Exit(Relax())
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


        elif self.location.type == 2:
            print("im at work")
            if self.hunger < th or self.energy < th:
                self.Exit(Travel(self.home))

            else:
                self.Exit(Work())

        elif self.location.type == 3:
            print("im at fun")
            if self.hunger < th or self.energy < th:
                self.Exit(Travel(self.home))

        elif self.location.type == 4:
            print("im at the shop")
            if (self.energy < th or self.hunger < th) and self.stateController.agent.home.package.food > 6:
                print("going back home")
                self.Exit(Travel(self.home))
            elif self.stateController.agent.home.package.food > 7:
                self.Exit(Travel(self.workPlace))
            else:
                print("im buying foods")
                self.Exit(Buy())
        else:
            print("im lost, walking home")
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
            pass
        elif self.location.type == 3: # at fun
            pass

        elif self.location.type == 4: # at store
            pass

        else:
            pass




    def Enter(self):
        self.stateController.agent.Think("I think im going to sleep")


    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Eat
class Eat(State):
    def __init__(self):
        super().__init__()


    def Do(self):
        self.hunger = self.stateController.agent.hunger
        self.energy = self.stateController.agent.energy
        self.foodLeft = self.stateController.agent.home.package.food
        self.location = self.stateController.agent.location
        self.home = self.stateController.agent.location

        if self.location.type == 1:
            if self.energy < 4 and self.hunger >= 4:
                self.Exit(Sleep())
            elif self.hunger >= 10:
                self.Exit(Choose())
            elif self.foodLeft <= 4:
                closestStore = FindwithTag(4)
                self.Exit(Travel(closestStore))
            else:
                self.stateController.agent.Think("im putting plate out")
                self.stateController.agent.Eat()

        elif self.location.type == 4:
            if self.energy < 4 and self.hunger >= 4:
                self.Exit(Sleep())
            pass
        else:
            pass


    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Clean
class Clean(State):
    def __init__(self):
        super().__init__()


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

    def Do(self):
        self.hunger = self.stateController.agent.hunger
        self.energy = self.stateController.agent.energy
        self.dishes = self.stateController.agent.home.package.dishes


        if self.energy <= 0:
            self.Exit(Dead())

        elif self.hunger <= 0:
            self.Exit(Dead())

        elif self.energy < 4 or self.hunger < 4 or self.dishes > 4:
            if self.hunger < 4:
                self.Exit(Eat())

            elif self.energy < 4:
                self.Exit(Sleep())

            elif self.dishes > 4:
                self.Exit(Clean())
            else:
                print("yo mama gay as hell")
        else:
            self.stateController.agent.Relax()


    def Enter(self):
        pass

    def Exit(self, state):

        self.stateController.ChangeState(state)

# ---------------------------------------------Work
class Work(State):
    def __init__(self):
        super().__init__()

    def Do(self):
        print("work hard")
        pass

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Slack
class Slack(State):
    def __init__(self):
        super().__init__()

    def Do(self):
        print("slack hard")
        pass

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# ---------------------------------------------Buy
class Buy(State):
    def __init__(self):
        super().__init__()

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
        elif self.hunger < 4:
            self.Exit(Eat())
        else:
            print("buy hard")
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

    def Do(self):
        print("die hard")
        print(self.agentName + " has DIED")
        pass

    def Enter(self):
        self.agentName = self.stateController.agent.fName
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)
