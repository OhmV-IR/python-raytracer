from vector3 import Vector3
from ray import Ray
from hitrecord import HitRecord
from math import acos, atan2, pi, sqrt
from hittable import hittable
from interval import Interval
from aabb import AABB
class Sphere(hittable):
    radius = float(0.0)
    center = Vector3(0,0,0)
    mat = None
    def __init__(self, radius: float, center: Vector3, mat=None, isMoving=False, center2=None):
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
    def SphereCenter(self, time):
        return self.center + self.centerVec * time
    def hit(self, ray: Ray, t: Interval) -> HitRecord:
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
            return HitRecord(Vector3(0,0,0), 0, 0, False, False, self.mat)
        sqrtd = sqrt(discriminant)
        root = (h - sqrtd) / a
        if not t.Surrounds(root):
            root = (h + sqrtd) / a
            if not t.Surrounds(root):
                return HitRecord(Vector3(0,0,0), Vector3(0,0,0), 0, False, False, self.mat)
        record = HitRecord(ray.PointAtTime(root), (ray.PointAtTime(root) - self.center) / self.radius, root, True, True, self.mat)
        outwardNormal = (record.point - self.center) / self.radius
        record.SetFaceNormal(ray, outwardNormal)
        uv = Sphere.GetSphereUV(outwardNormal)
        record.u = uv.min
        record.v = uv.max
        return record
    @staticmethod
    def GetSphereUV(point: Vector3):
        theta = acos(-point.y)
        phi = atan2(-point.z, point.x) + pi
        return Interval(phi / (2*pi), theta / pi)
        