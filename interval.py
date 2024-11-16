# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Interval class
from enum import Enum
class Interval:
    '''A class that contains a minimum and maximum value representing a range'''
    __slots__ = 'min', 'max', 'aabbBoxHit'
    def __add__(self, displacement: float):
        '''Shifts the entire interval by a displacement'''
        return Interval(self.min + displacement, self.max + displacement)
    def __init__(self, min=float('inf'), max=float('-inf'), aabbBoxHit = False):
        '''Creates an interval from a minimum and maximum value'''
        self.min = min
        self.max = max
        self.aabbBoxHit = aabbBoxHit
    def Size(self) -> float:
        '''Returns the size of the interval'''
        return self.max - self.min
    def Contains(self, x:float) -> bool:
        '''Returns true if the specified value falls within the range of the interval(uses <= and >= comparators)'''
        return self.min <= x and x <= self.max
    def Surrounds(self, x:float) -> bool:
        '''Returns true if the specified value falls within the range of the interval(uses < and > comparators)'''
        return self.min < x and x < self.max
    def Clamp(self, x: float) -> float:
        '''Clamps the specified value to the range of the interval, a value greater than the maximum returns the maximum,
        a value less than the minimum returns the minimum and returns the value if it falls within the range'''
        if x < self.min: return self.min
        if x > self.max: return self.max
        return x
    def Expand(self, delta: float):
        '''Expands an interval by a factor, this expansion is applied evenly to both ends of the interval so both the minimum
        and maximum of the interval will be increased by the value / 2'''
        padding = delta / 2
        return Interval(self.min - padding, self.max + padding)
    @staticmethod
    def CreateEmptyInterval() -> 'Interval':
        '''Creates an empty interval that encompasses nothing'''
        return Interval(float('inf'), float('-inf'))
    @staticmethod
    def CreateInfiniteInterval() -> 'Interval':
        '''Creates an infinite interval that encompasses everything'''
        return Interval(float('-inf'), float('inf'))
    @staticmethod
    def CombineIntervals(interval1: 'Interval', interval2: 'Interval') -> 'Interval':
        '''Combines 2 intervals to create 1 interval'''
        if interval1.min <= interval2.min:
            mini = interval1.min
        else:
            mini = interval2.min
        if interval1.max >= interval2.max:
            maxi = interval1.max
        else:
            maxi = interval2.max
        return Interval(mini, maxi)