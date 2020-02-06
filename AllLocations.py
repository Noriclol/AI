from Location import *

houseJeff = Location("Jeffs_House", 1, Home())
houseJoe = Location("Joes_House", 1, Home())

Office = Location("Office", 2, Empty)
Factory = Location("WorkPlace", 2, Empty)

Pub = Location("Pub", 3, Empty)

Store = Location("Store", 4, Empty)

buildingList = [houseJeff, houseJoe, Office, Factory, Store, Pub]

def FindwithTag(tag):
    for building in buildingList:
        if building.type == tag:
            print("BuildingFound: " + str(building.name))
            return building
        else:
            pass
    print("no building found")

def FindwithTagandName(tag, name):
    for building in buildingList:
        if building.type == tag and building.name == name:
            print("BuildingFound: " + str(building.name))
            return building
        else:
            pass
    print("no building found")