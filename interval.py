# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Interval class
from enum import Enum
class Interval:
    min = float(0)
    max = float(0)
    aabbBoxHit = False
    def __add__(self, displacement):
        return Interval(self.min + displacement, self.max + displacement)
    def __init__(self, min=float('inf'), max=float('-inf'), aabbBoxHit = False, createFromTwoIntervals=False, interval1=None, interval2=None):
        if createFromTwoIntervals:
            if interval1.min <= interval2.min:
                self.min = interval1.min
            else:
                self.min = interval2.min
            if interval1.max >= interval2.max:
                self.max = interval1.max
            else:
                self.max = interval2.max
        else:
            self.min = min
            self.max = max
            self.aabbBoxHit = aabbBoxHit
    def Size(self) -> float:
        return self.max - self.min
    def Contains(self, x:float) -> bool:
        return self.min <= x and x <= self.max
    def Surrounds(self, x:float) -> bool:
        return self.min < x and x < self.max
    def Clamp(self, x: float) -> float:
        if x < self.min: return self.min
        if x > self.max: return self.max
        return x
    def Expand(self, delta: float):
        padding = delta / 2
        return Interval(self.min - padding, self.max + padding)
class Intervals(Enum):
    EMPTY = Interval(float('inf'), float('-inf'))
    UNIVERSE = Interval(float('-inf'), float('inf'))