from vector3 import Vector3
from ray import Ray
class HitRecord:
    __slots__ = 'point', 'normal', 't', 'frontface', 'hit', 'mat', 'u', 'v'
    def __init__(self, point: Vector3, normal: Vector3, t: float, frontface: bool, hit: bool, mat=None):
        '''Creates a HitRecord which stores some hit data'''
        self.point = point
        self.normal = normal
        self.t = t
        self.frontface = frontface
        self.hit = hit
        self.mat = mat
    @staticmethod
    def CreateFalseHit() -> 'HitRecord':
        '''Creates a HitRecord for no hit(blank values)'''
        return HitRecord(Vector3(0,0,0), Vector3(0,0,0), 0, False, False, None)
    def SetFaceNormal(self, ray: Ray, outwardNormal: Vector3):
        '''Sets the front face of the HitRecord and the normal from an outward normal vector and the hitting ray. '''
        self.frontface = (ray.direction.dot(outwardNormal) < 0)
        if self.frontface:
            self.normal = outwardNormal
        else:
            self.normal = outwardNormal.Negative()