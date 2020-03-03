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

    def __eq__ (self, other):
        if self.minutes == other.minutes and self.hours == other.hours

    def PrintTime(self):
        print("Day " + str(self.days) + "  " + str(self.hours) + ":" + str(self.minutes))
    def GetTime(self):
        time = (self.hours, self.minutes)
        return self.days
    def GetHour(self):
        return self.hours

gameClock = Clock()
# 0h - 7h home
# 8h - 17h work
# 18h - 22h if low on food at home, go store. otherwise go to pub with friends.
# 22h - 24h home