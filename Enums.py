from enum import Enum
from enum import auto


class StateEnums(Enum):
    WorkHard = auto()
    SlackAtWork = auto()
    Clean = auto()
    Sleep = auto()
    Eat = auto()
    hangout = auto()
    callperson = auto()

class Tag(Enum):
    Person = auto()
    Recreational = auto()
    RecreationalFree = auto()
    Workplace = auto()
    Home = auto()

class locationType(Enum):
    House = auto()
    Workplace = auto()
    Recreational = auto()
    Store = auto()

class Message(Enum):
    AsktoJoin = auto()
    AsktoMeet = auto()
    AsktoWait = auto()


