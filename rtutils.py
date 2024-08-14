from random import random, randint
# Constants
pi = 3.1415926535897932385
infinity = float('inf')
def DegreesToRadians(degrees: float) -> float:
    return degrees * pi / 180.0
def RandomFloat() -> float:
    return random()
def RandomFloatRange(min: float, max: float):
    return min + (max-min)*RandomFloat()
def RandomInteger(min: int, max: int):
    return randint(min, max)
def fmin(f1: float, f2: float) -> float:
    if f1 <= f2:
        return f1
    else:
        return f2
def fmax(f1: float, f2: float) -> float:
    if f1 >= f2:
        return f1
    else:
        return f2