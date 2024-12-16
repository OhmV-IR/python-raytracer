from vector3 import Vector3
from ray import Ray
from hitrecord import HitRecord
from math import acos, atan2, pi, sqrt
from hittable import hittable
from interval import Interval
from material import Material
from aabb import AABB
class Sphere(hittable):
    '''Sphere object'''
    __slots__ = 'radius', 'center', 'mat', 'isMoving', 'box1', 'box2', 'boundingBox', 'center2', 'centerVec'
    @staticmethod
    def CreateSphere(radius: float, center: Vector3, mat=None) -> 'Sphere':
        '''Creates a sphere using a radius and center.
        A material may also be provided to this function which will be applied to the object'''
        return Sphere(radius, center, mat)
    @staticmethod
    def CreateMovingSphere(radius: float, center1: Vector3, center2: Vector3, mat=None) -> 'Sphere':
        '''Creates a moving sphere from 2 centers and a radius. 
        A material may also be provided to this function which will be applied to the object.'''
        return Sphere(radius, center1, mat, True, center2)
    def __init__(self: 'Sphere', radius: float, center: Vector3, mat=None, isMoving=False, center2=None) -> 'Sphere':
        '''Sphere constructor'''
        self.radius = radius
        self.center = center
        self.mat = mat
        self.isMoving = isMoving
        if isMoving:
            rvec = Vector3(radius, radius, radius)
            self.box1 = AABB.CreateBoundingBoxFromPoints(center - rvec, center + rvec)
            self.box2 = AABB.CreateBoundingBoxFromPoints(center2 - rvec, center2 + rvec)
            self.boundingBox = AABB.CreateBoundingBoxFromBoxes(self.box1, self.box2)
            self.center2 = center2
            self.centerVec = center2 - center
        else:
            rvec = Vector3(radius, radius, radius)
            self.boundingBox = AABB.CreateBoundingBoxFromPoints(center - rvec, center + rvec)
    def SphereCenter(self: 'Sphere', time: float) -> 'Vector3':
        '''Returns the center of the sphere at a specified time.
        sphere.isMoving MUST be set to TRUE'''
        return self.center + Vector3.MultiplyScalar(self.centerVec, time)
    def hit(self: 'Sphere', ray: Ray, t: Interval) -> HitRecord:
        '''Checks whether or not a ray has hit the object at a specified time interval'''
        if self.isMoving:
            center = self.SphereCenter(ray.time)
        else:
            center = self.center
        oc = center - ray.origin
        a = ray.direction.LengthSquared()
        h = ray.direction.dot(oc)
        c = oc.LengthSquared() - self.radius*self.radius
        discriminant = h*h - a*c
        if discriminant < 0:
            return HitRecord.CreateFalseHit()
        sqrtd = sqrt(discriminant)
        root = (h - sqrtd) / a
        if not t.Surrounds(root):
            root = (h + sqrtd) / a
            if not t.Surrounds(root):
                return HitRecord.CreateFalseHit()
        record = HitRecord(ray.PointAtTime(root), Vector3.DivideScalar((ray.PointAtTime(root) - self.center), self.radius), root, True, True, self.mat)
        outwardNormal = Vector3.DivideScalar(record.point - self.center, self.radius)
        record.SetFaceNormal(ray, outwardNormal)
        uv = Sphere.GetSphereUV(outwardNormal)
        record.u = uv.min
        record.v = uv.max
        return record
    @staticmethod
    def GetSphereUV(point: Vector3) -> Interval:
        '''Get the 2D texture coordinate from a 3D point on the sphere'''
        theta = acos(-point.y)
        phi = atan2(-point.z, point.x) + pi
        return Interval(phi / (2*pi), theta / pi)
        