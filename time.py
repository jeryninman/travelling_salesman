#  Jeryn Inman Student ID: #000948438


# Class to represent time during a day, starting at 8 am,
# overrides all simple forms of comparison, and a to-string method
# time class written to use as a control on the flow of the program, allowing it to stop at chosen points
class Time:

    def __init__(self, h, m):
        self.hour = h
        self.minute = m

    def advance(self, minutes_advanced):
        self.minute += minutes_advanced
        while self.minute >= 60:
            self.hour += 1
            self.minute -= 60

    # Equal to operator override
    def __eq__(self, other):
        return self.hour == other.hour and self.minute == other.minute

    # not equal to operator override
    def __ne__(self, other):
        return self.hour != other.hour or self.minute != other.minute

    # greater than equal to operator override
    def __ge__(self, other):
        return (self.hour, self.minute) >= (other.hour, other.minute)

    # greater than operator override
    def __gt__(self, other):
        return (self.hour, self.minute) > (other.hour, other.minute)

    # less than equal to operator override
    def __le__(self, other):
        return (self.hour, self.minute) <= (other.hour, other.minute)

    # less than operator override
    def __lt__(self, other):
        return (self.hour, self.minute) < (other.hour, other.minute)

    # subtract operator override
    def __sub__(self, other):
        return self.hour - other.hour and self.minute - other.minute

    # to string method
    def __str__(self):
        if self.minute < 10:  # style
            return str(self.hour) + ":0" + str(int(self.minute))
        else:
            return str(self.hour) + ":" + str(int(self.minute))
