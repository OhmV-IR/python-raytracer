from interval import Interval
from ray import Ray
from hitrecord import HitRecord
from vector3 import Vector3
class AABB:
    x = None
    y = None
    z = None
    def __add__(self, offset: Vector3):
        return AABB(False, self.x + offset.x, self.y + offset.y, self.z + offset.z)
    @staticmethod
    def PadToMinimums(self):
        delta = 0.0001
        if self.x.Size() < delta:
            self.x = self.x.Expand(delta)
        if self.y.Size() < delta:
            self.y = self.y.Expand(delta)
        if self.z.Size() < delta:
            self.z = self.z.Expand(delta)
    def __init__(self, usingPoints: bool, x=None, y=None, z=None, point1=None, point2=None, using2Boxes=False, box1=None, box2=None):
        if usingPoints:
            if point1.x <= point2.x:
                self.x = Interval(point1.x, point2.x)
            else:
                self.x = Interval(point2.x, point1.x)
            if point1.y <= point2.y:
                self.y = Interval(point1.y, point2.y)
            else:
                self.y = Interval(point2.y, point1.y)
            if point1.z <= point2.z:
                self.z = Interval(point1.z, point2.z)
            else:
                self.z = Interval(point2.z, point1.z)
        elif using2Boxes:
            self.x = Interval(None, None, False, True, box1.x, box2.x)
            self.y = Interval(None, None, False, True, box1.y, box2.y)
            self.z = Interval(None, None, False, True, box1.z, box2.z)
        else:
            self.x = x
            self.y = y
            self.z = z
        self = AABB.PadToMinimums(self)
    def AxisInterval(self, n:int):
        if n == 1:
            return self.y
        elif n == 2:
            return self.z
        else:
            return self.x
    def LongestAxis(self):
        if self.x.Size() > self.y.Size():
            if self.x.Size() > self.z.Size():
                return 0
            else:
                return 2
        else:
            if self.y.Size() > self.z.Size():
                return 1
            else:
                return 2
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        rayOrigin = ray.origin
        rayDirection = ray.direction
        for axis in range(0,3):
            ax = self.AxisInterval(axis)
            if axis == 0:
                adinv = 1.0 / rayDirection.x
                t0 = (ax.min - rayOrigin.x) * adinv
                t1 = (ax.max - rayOrigin.x) * adinv
            elif axis == 1:
                adinv = 1.0 / rayDirection.y
                t0 = (ax.min - rayOrigin.y) * adinv
                t1 = (ax.max - rayOrigin.y) * adinv
            else:
                adinv = 1.0 / rayDirection.z
                t0 = (ax.min - rayOrigin.z) * adinv
                t1 = (ax.max - rayOrigin.z) * adinv
            if t0 < t1:
                if t0 > t.min:
                    tmin = t0
                if t1 < t.max:
                    tmax = t1
            else:
                if t1 > t.min:
                    tmin = t1
                if t0 < t.max:
                    tmax = t0
            if tmax <= tmin:
                return Interval(tmin, tmax, False)
            else:
                return Interval(tmin, tmax, True)