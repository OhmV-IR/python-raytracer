# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Ray class
from vector3 import Vector3
class Ray:
    def __init__(self, origin: Vector3, direction: Vector3, scattered=False, attenuation=Vector3(0,0,0), time=0):
        self.origin = origin
        self.time = time
        self.direction = direction
        self.scattered = scattered
        self.attenuation = attenuation
    def PointAtTime(self, time: float):
        return self.origin + self.direction * time
