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
    @abstractmethod
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        pass
class hittableList(hittable): 
    def __init__(self, root=False):
        self.root = root
        self.hittablelist = []
        self.boundingBox = None
    def add(self, obj: hittable):
        self.hittablelist.append(obj)
        if self.boundingBox == None:
            self.boundingBox = obj.boundingBox
        else:
            self.boundingBox = AABB.CreateBoundingBoxFromBoxes(self.boundingBox, obj.boundingBox)
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        closest = t.max
        currentreturn = HitRecord(Vector3(0,0,0), Vector3(0,0,0), 0, False, False)
        for i in range(0,len(self.hittablelist)):
            hitrecord = self.hittablelist[i].hit(ray, Interval(t.min, closest))
            if hitrecord.hit == True:
                closest = hitrecord.t
                currentreturn = hitrecord
        return currentreturn

class BVHNode(hittable):
    def __init__(self, hittableArr, startIndex, endIndex):
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
        boundingBoxHit = self.boundingBox.hit(ray, t)
        if boundingBoxHit.hit == False:
            return HitRecord(Vector3(0,0,0), Vector3(0,0,0), float('inf'), False, False, None)
        hitleft = self.left.hit(ray, t)
        if hitleft.hit:
            hitright = self.right.hit(ray, hitleft.t)
        else:
            hitright = self.right.hit(ray, t.max)
        if hitleft.hit == True:
            return hitleft
        elif hitright.hit == True:
            return hitright
        else:
            return HitRecord(Vector3(0,0,0), Vector3(0,0,0), float('inf'), False, False, None)
    @staticmethod
    def BoxCompare(hittable1, hittable2, axisIndex):
        hittable1AxisInterval = hittable1.boundingBox.AxisInterval(axisIndex)
        hittable2AxisInterval = hittable2.boundingBox.AxisInterval(axisIndex)
        return hittable1AxisInterval.min < hittable2AxisInterval.min
    @staticmethod
    def BoxCompareX(hittable1, hittable2):
        return BVHNode.BoxCompare(hittable1, hittable2, 0)
    @staticmethod
    def BoxCompareY(hittable1, hittable2):
        return BVHNode.BoxCompare(hittable1, hittable2, 1)
    @staticmethod
    def BoxCompareZ(hittable1, hittable2):
        return BVHNode.BoxCompare(hittable1, hittable2, 2)

class Translate(hittable):
    def __init__(self, object: hittable, offset: Vector3):
        self.offset = offset
        self.boundingBox = object.boundingBox + offset
        self.object = object
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
        offsetRay = Ray(ray.origin - self.offset, ray.direction, False, Vector3(0,0,0), ray.time)
        hitrec = self.object.hit(offsetRay, t)
        if hitrec.hit == False:
            return hitrec
        else:
            hitrec.point += self.offset
            return hitrec
