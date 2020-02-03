import numpy as np


class Location:
    def __init__(self, place = "place"):
        self.locationName = place


class Workplace(Location):
    def __init__(self, place):
        super().__init__()
        self.locationName = place

class Store(Location):
    def __init__(self, place):
        super().__init__()
        self.locationName = place


class Recreational(Location):
    def __init__(self, place):
        super().__init__()
        self.locationName = place

class RecreationalFree(Location):
    def __init__(self, place):
        super().__init__()
        self.locationName = place



class Home(Location):
    def __init__(self, place):
        super().__init__()
        self.locationName = place
        self.food = 10
        self.dishes = 0

    def CleanDish(self):
        if self.dishes >= 0:
            pass
        else:
            self.dishes -= 1

