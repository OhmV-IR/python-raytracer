from vector3 import Vector3
from ray import Ray
class HitRecord:
    def __init__(self, point: Vector3, normal: Vector3, t: float, frontface: bool, hit: bool, mat=None):
        self.point = point
        self.normal = normal
        self.t = t
        self.frontface = frontface
        self.hit = hit
        self.mat = mat
    def SetFaceNormal(self, ray: Ray, outwardNormal: Vector3):
        self.frontface = (ray.direction.dot(outwardNormal) < 0)
        if self.frontface:
            self.normal = outwardNormal
        else:
            self.normal = outwardNormal.Negative()