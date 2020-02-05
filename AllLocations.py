from Location import *

houseJeff = Location("Jeffs_House", 1, Home())
houseJoe = Location("Joes_House", 1, Home())

Office = Location("Office", 2, Empty)
Factory = Location("WorkPlace", 2, Empty)

Pub = Location("Pub", 3, Empty)

Store = Location("Park", 4, Empty)

buildingList = [houseJeff, houseJoe, Office, Factory, Office]

def FindwithTag(tag):
    for building in buildingList:
        if building.type == tag:
            return building
        else:
            pass