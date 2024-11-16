#P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Abstract hittable class used by all objects that rays can intersect with
from math import cos, sin
from ray import Ray
from hitrecord import HitRecord
from abc import abstractmethod, ABC, abstractproperty
from vector3 import Vector3
from interval import Interval
from aabb import AABB
from rtutils import DegreesToRadians, fmin, fmax
class hittable(ABC):
    '''The abstract class which all objects which a ray can hit are derived from. All hittable objects implement the hit method which will return whether or not
    an inputted ray has hit the object.'''
    @abstractmethod
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        pass
class hittableList(hittable):
    '''A class which contains a list of hittable objects, has a bounding box and qualifies as a hittable object itself'''
    def __init__(self, root=False):
        '''Creates a list of hittable objects, if this is your scene, set root to true'''
        self.root = root
        self.hittablelist = []
        self.boundingBox = None
    def add(self, obj: hittable):
        '''Adds an object to the hittable list and expands the bounding box of the hittable list to encompass the new object'''
        self.hittablelist.append(obj)
        if self.boundingBox == None:
            self.boundingBox = obj.boundingBox
        else:
            self.boundingBox = AABB.CreateBoundingBoxFromBoxes(self.boundingBox, obj.boundingBox)
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        '''Checks if a provided ray has hit any encompassed object and returns the hitrecord data from the hit of that object if so'''
        closest = t.max
        currentreturn = HitRecord.CreateFalseHit()
        for i in range(0,len(self.hittablelist)):
            hitrecord = self.hittablelist[i].hit(ray, Interval(t.min, closest))
            if hitrecord.hit == True:
                closest = hitrecord.t
                currentreturn = hitrecord
        return currentreturn

class BVHNode(hittable):
    '''A bounding volume hierarchy node that takes a list of hittable objects and splits them into sublists, improving performance'''
    def __init__(self, hittableArr, startIndex, endIndex):
        '''Creates a bounding volume hierarchy from a list of hittable objects and a start-end index showing which objects should be used in the hittable list'''
        self.boundingBox = hittableArr[startIndex].boundingBox
        for i in range(startIndex+1, endIndex):
            self.boundingBox = AABB.CreateBoundingBoxFromBoxes(self.boundingBox, hittableArr[i].boundingBox)
        axis = self.boundingBox.LongestAxis()
        if axis == 0:
            comparator = BVHNode.BoxCompareX
        elif axis == 1:
            comparator = BVHNode.BoxCompareY
        else:
            comparator = BVHNode.BoxCompareZ
        objectSpan = endIndex - startIndex
        if objectSpan == 1:
            self.left = self.right = hittableArr[startIndex]
        elif objectSpan == 2:
            self.left = hittableArr[startIndex]
            self.right = hittableArr[startIndex+1]
        else:
            hittableArr.sort(False, comparator) # sorts entire list, not just start/end index which could be an issue
            mid = startIndex + objectSpan / 2
            self.left = BVHNode(hittableArr, startIndex, mid)
            self.right = BVHNode(hittableArr, mid, endIndex)
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        '''Determines if a ray will hit the bounding tree, and then determines which side of the bounding tree it will hit and
        returns that hit record information'''
        boundingBoxHit = self.boundingBox.hit(ray, t)
        if boundingBoxHit.hit == False:
            return HitRecord.CreateFalseHit()
        # Checks if the ray hit the left side of the bounding box tree
        hitleft = self.left.hit(ray, t)
        if hitleft.hit:
            hitright = self.right.hit(ray, hitleft.t)
        else:
            hitright = self.right.hit(ray, t.max)
        # Return the hit record information of which side it hit
        if hitleft.hit == True:
            return hitleft
        elif hitright.hit == True:
            return hitright
        else:
            return HitRecord.CreateFalseHit()
    @staticmethod
    def BoxCompare(hittable1: hittable, hittable2: hittable, axisIndex: int) -> bool:
        '''Compares the intervals of the bounding boxes of 2 hittable objects using an axis index, 
        if axisIndex=0 then if hittable1 has a lower minimum value in the bounding box x interval, this will return true'''
        hittable1AxisInterval = hittable1.boundingBox.AxisInterval(axisIndex)
        hittable2AxisInterval = hittable2.boundingBox.AxisInterval(axisIndex)
        return hittable1AxisInterval.min < hittable2AxisInterval.min
    @staticmethod
    def BoxCompareX(hittable1: hittable, hittable2: hittable) -> bool:
        '''Shorthand for BoxCompare(hittable1, hittable2, 0)'''
        return BVHNode.BoxCompare(hittable1, hittable2, 0)
    @staticmethod
    def BoxCompareY(hittable1: hittable, hittable2: hittable) -> bool:
        '''Shorthand for BoxCompare(hittable1, hittable2, 1)'''
        return BVHNode.BoxCompare(hittable1, hittable2, 1)
    @staticmethod
    def BoxCompareZ(hittable1: hittable, hittable2: hittable) -> bool:
        '''Shorthand for BoxCompare(hittable1, hittable2, 2)'''
        return BVHNode.BoxCompare(hittable1, hittable2, 2)

class Translate(hittable):
    '''Translates a hittable object and it's bounding box by a vector offset'''
    def __init__(self, object: hittable, offset: Vector3):
        '''Creates the translated object from the original object and a vector offset'''
        self.offset = offset
        self.boundingBox = object.boundingBox + offset
        self.object = object
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        '''Checks if a ray has hit the translated object and returns the hit record information if it has'''
        offsetRay = Ray(ray.origin - self.offset, ray.direction, False, Vector3(0,0,0), ray.time)
        hitrec = self.object.hit(offsetRay, t)
        if hitrec.hit == False:
            return hitrec
        else:
            hitrec.point += self.offset
            return hitrec
