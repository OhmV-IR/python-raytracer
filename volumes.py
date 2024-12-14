from hittable import hittableList, hittable
from texture import Texture
from material import Isotropic
from ray import Ray
from interval import Interval
from hitrecord import HitRecord
import rtutils
from vector3 import Vector3
class ConstantMedium(hittable):
    '''A volume that can represent smoke, fog, mist .etc'''
    __slots__ = 'boundingBox', 'boundary', 'negInverseDensity', 'phaseFunction'
    def __init__(self: 'ConstantMedium', density: float, boundary: hittable, texture: Texture):
        '''Creates a volume from a density, a boundary which the volume occupies and a texture'''
        self.boundary = boundary
        self.negInverseDensity = -1/density
        self.phaseFunction = Isotropic(texture)
        self.boundingBox = boundary.boundingBox
    def hit(self: 'ConstantMedium', ray: Ray, t: Interval) -> HitRecord:
        '''Checks if a ray hit the volume and return the hit record information if it does'''
        rec1 = self.boundary.hit(ray, Interval(float("-inf"), float("inf")))
        if rec1.hit == False:
            return HitRecord.CreateFalseHit()
        rec2 = self.boundary.hit(ray, Interval(ray.time+0.0001, float("inf")))
        if rec2.hit == False:
            return HitRecord.CreateFalseHit()
        if rec1.t < t.min:
            rec1.t = t.min
        if rec2.t > t.max:
            rec2.t = t.max
        if rec1.t >= rec2.t:
            return HitRecord.CreateFalseHit()
        if rec1.t < 0:
            rec1.t = 0
        raylen = ray.direction.Length()
        distInsideBoundary = (rec2.t - rec1.t) * raylen
        hitdistance = self.negInverseDensity * rtutils.RandomFloat()
        if hitdistance > distInsideBoundary:
            return HitRecord.CreateFalseHit()
        hitrec = HitRecord(ray.PointAtTime(rec1.t + hitdistance / raylen), Vector3(1,0,0), rec1.t + hitdistance / raylen, True, True, self.phaseFunction)
        hitrec.u = 0
        hitrec.v = 0 # arbitrary values for u, v, normal, only use SolidColor texture
        return hitrec