import time

class Clock:
    def __init__(self):
        self.minutes = 0
        self.hours = 0
        self.days = 0

    def Tick(self):
        self.minutes += 1
        if self.minutes > 59:
            self.minutes = 0
            self.hours += 1
        if self.hours > 24:
            self.hours = 0
            self.days += 1


    def Time(self):
        print("Day " + str(self.days) + "  " + str(self.hours) + ":" + str(self.minutes))
