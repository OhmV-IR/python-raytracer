from interval import Interval
from ray import Ray
from hitrecord import HitRecord
from vector3 import Vector3
class AABB:
    ''' Bounding boxes for easy hit/miss checks, helps with performance'''
    __slots__ = 'x','y','z'
    def __add__(self: 'AABB', offset: Vector3):
        '''Offsets/moves the box by a vector'''
        return AABB(self.x + offset.x, self.y + offset.y, self.z + offset.z)
    @staticmethod
    def PadToMinimums(self: 'AABB'):
        '''Ensures that all dimensions of the box are at least a small value as to avoid floating point errors when doing hit detection math'''
        delta = 0.0001
        if self.x.Size() < delta:
            self.x = self.x.Expand(delta)
        if self.y.Size() < delta:
            self.y = self.y.Expand(delta)
        if self.z.Size() < delta:
            self.z = self.z.Expand(delta)
    @staticmethod
    def CreateBoundingBoxFromPoints(point1: Vector3, point2: Vector3):
        '''Create a bounding box from the top-left corner of the box(point 1) and the bottom-right corner of the box(point 2)'''
        if point1.x <= point2.x:
            x = Interval(point1.x, point2.x)
        else:
            x = Interval(point2.x, point1.x)
        if point1.y <= point2.y:
            y = Interval(point1.y, point2.y)
        else:
            y = Interval(point2.y, point1.y)
        if point1.z <= point2.z:
            z = Interval(point1.z, point2.z)
        else:
            z = Interval(point2.z, point1.z)
        return AABB(x,y,z)
    @staticmethod
    def CreateBoundingBoxFromBoxes(box1: 'AABB', box2: 'AABB'):
        '''Create a bounding box by merging 2 existing boxes'''
        x = Interval.CombineIntervals(box1.x, box2.x)
        y = Interval.CombineIntervals(box1.y, box2.y)
        z = Interval.CombineIntervals(box1.z, box2.z)
        return AABB(x,y,z)
    def __init__(self: 'AABB', x: Interval, y: Interval, z: Interval):
        '''Create a bounding box using 3 intervals to describe the volume of the box'''
        self.x = x
        self.y = y
        self.z = z
        self = AABB.PadToMinimums(self)
    def AxisInterval(self: 'AABB', n:int):
        '''If n = 1, x interval is returned and so forth'''
        if n == 1:
            return self.y
        elif n == 2:
            return self.z
        else:
            return self.x
    def LongestAxis(self: 'AABB'):
        '''Returns the number of the smallest axis(0 for x, 1 for y, 2 for z)'''
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
    def hit(self: 'AABB', ray: Ray, t: Interval) -> Interval:
        '''Checks if the ray hit the bounding box'''
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