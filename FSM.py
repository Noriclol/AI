import abc
from Location import *
from Actors import *


# Main StateController Class
class StateController:
    # agent = Person()

    def __init__(self, agent):
        self.agent = agent
        self.currentState = None
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
        print("money" + str(self.agent.money))
# ParentState
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
# ParentState


class Choose(State):
    def __init__(self):
        super().__init__()


    def Do(self):
        self.energy = self.stateController.agent.energy
        self.hunger = self.stateController.agent.hunger
        self.money = self.stateController.agent.money
        self.location = self.stateController.agent.location.locationName
        self.home = self.stateController.agent.location.locationName
        self.workPlace = self.stateController.agent.workplace.locationName

        th = 4
        print("Do Gets Called: " + self.stateController.agent.fName)
        if self.stateController.agent.dead == True:
            self.Exit(Dead())
        elif self.location == self.home:
            if self.energy > th or self.hunger > th or self.money > th:

                self.Exit(Relax())
            else:

                # do what needs to be done(from most important to last)
                if self.energy < th and self.hunger < th:
                    self.Exit(Eat())

                elif self.energy < th <= self.hunger:
                    self.Exit(Sleep())

                elif self.stateController.agent.home.dishes > 5:
                    self.Exit(Clean())

                elif self.money < th <= self.hunger and self.energy < th:
                    # not enough money, go to work
                    self.Exit(Travel(self.workPlace))
                else:
                    print("else gets called twice")

        # if at workplace
        elif self.location == Workplace():
            print("im at work")
            if self.hunger < th or self.energy < th: #if too Hungry or tired
                self.Exit(Travel(Home))

            else:
                self.Exit(Work())

        elif self.location == Recreational():
            print("im at fun")
            if self.hunger < th or self.energy < th: #if too Hungry or tired
                self.Exit(Travel(self.home))
        elif self.location == Store():
            if self.energy < th or self.hunger < th:
                self.Exit(Travel(self.home))
            else:
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

# TravelState


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


# --------------------------------------------------------------#### Home States
# -------------------------------------------------------------- Sleep


class Sleep(State):
    def __init__(self):
        super().__init__()


    def Do(self):
        self.energy = self.stateController.agent.hunger
        self.hunger = self.stateController.agent.energy

        if self.hunger < 4:
            self.Exit(Eat())
        elif self.energy >= 10:
            self.Exit(Choose())
        else:
            self.stateController.agent.Sleep()


    def Enter(self):
        self.stateController.agent.Think("I think im going to sleep")


    def Exit(self, state):
        self.stateController.ChangeState(state)


# -------------------------------------------------------------- Eat


class Eat(State):
    def __init__(self):
        super().__init__()


    def Do(self):
        self.hunger = self.stateController.agent.hunger
        self.energy = self.stateController.agent.energy
        self.foodLeft = self.stateController.agent.home.food

        if self.energy < 4 and self.hunger >= 4:
            self.Exit(Sleep())
        elif self.hunger >= 10:
            self.Exit(Choose)
        elif self.foodLeft >= 0:
            Travel(Store())
        else:
            self.stateController.agent.Eat()

    def Enter(self):
        self.stateController.agent.Think("im putting plate out")


        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# -------------------------------------------------------------- Clean
class Clean(State):
    def __init__(self):
        super().__init__()


    def Do(self):
        self.Energy = self.stateController.agent.hunger
        self.Hunger = self.stateController.agent.energy

        if self.Energy < 4 and self.Hunger < 4:
            self.Exit(Eat())
        elif self.Energy < 4 and self.Hunger >= 4:
            self.Exit(Sleep())
        else:
            self.stateController.agent.Clean()

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

class Relax(State):
    def __init__(self):
        super().__init__()

    def Do(self):
        self.hunger = self.stateController.agent.hunger
        self.energy = self.stateController.agent.energy
        self.dishes = self.stateController.agent.home.dishes


        if self.energy <= 0:
            self.Exit(Dead())
        elif self.hunger <= 0:
            self.Exit(Dead())
        elif self.energy < 4 or self.hunger < 4 or self.dishes > 4:
            if self.energy < 4 and self.hunger < 4:
                self.Exit(Eat())
            elif self.energy < 4:
                self.Exit(Sleep())
            elif self.dishes > 4:
                self.Exit(Clean())
        else:
            # self.stateController.GetStats()
            self.stateController.agent.Relax()


    def Enter(self):
        pass

    def Exit(self, state):

        self.stateController.ChangeState(state)
# -------------------------------------------------------------- ##### Work States
# -------------------------------------------------------------- Work

class Work(State):
    def __init__(self):
        super().__init__()

    def Do(self):

        pass

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)



class Slack(State):
    def __init__(self):
        super().__init__()

    def Do(self):

        pass

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

# -------------------------------------------------------------- ##### Shop States

class Shop(State):
    def __init__(self):
        super().__init__()

    def Do(self):

        pass

    def Enter(self):
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)



class Dead(State):
    def __init__(self):
        super().__init__()

    def Do(self):
        print(self.agentName + " has DIED")
        pass

    def Enter(self):
        self.agentName = self.stateController.agent.fName
        pass

    def Exit(self, state):
        self.stateController.ChangeState(state)

    # if hungry and sleepy eat food,
    # if no clean dishes do dishes then eat
    # if sleepy sleep
    # if neither do dishes or hang out with friends