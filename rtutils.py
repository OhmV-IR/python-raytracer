from random import random, randint
# Constants
pi = 3.1415926535897932385
'''The mathematical constant pi'''
infinity = float('inf')
'''Positive infinity float'''
def DegreesToRadians(degrees: float) -> float:
    '''Converts a degree value into radians'''
    return degrees * pi / 180.0
def RandomFloat() -> float:
    '''Returns a random float between 0 and 1'''
    return random()
def RandomFloatRange(min: float, max: float):
    '''Returns a random float between your maximum and minimum specified values'''
    return min + (max-min)*RandomFloat()
def RandomInteger(min: int, max: int):
    '''Returns a random integer in your specified range(including both end points)'''
    return randint(min, max)
def fmin(f1: float, f2: float) -> float:
    '''Returns the smaller of the 2 arguments'''
    if f1 <= f2:
        return f1
    else:
        return f2
def fmax(f1: float, f2: float) -> float:
    '''Returns the larger of the 2 arguments'''
    if f1 >= f2:
        return f1
    else:
        return f2