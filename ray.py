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
    @staticmethod
    def CreateNullRay() -> 'Ray':
        '''This function is used by materials which do not scatter rays to return a null ray with blank values
        and the scattered attribute set to false'''
        return Ray(Vector3(0,0,0), Vector3(0,0,0))
    def PointAtTime(self, time: float):
        return self.origin + self.direction * time
