import numpy as np

class Package:
    pass
class Empty(Package):
    pass

class Home(Package):
    def __init__(self):
        super().__init__()
        self.food = 10
        self.dishes = 0

    def CleanDish(self):
        if self.dishes >= 0:
            pass
        else:
            self.dishes -= 1


class Location:
    def __init__(self, place = "place", type = 1, package = None):
        self.name = place
        self.type = type
        self.package = package

