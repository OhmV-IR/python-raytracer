# P2.0 Final Project
# REDACTED(I <3 not doxing myself)
from math import fabs
from hittable import hittable, hittableList
from vector3 import Vector3
from material import Material
from aabb import AABB
from hitrecord import HitRecord
from ray import Ray
from interval import Interval
from rtutils import fmin, fmax
class Quad(hittable):
    __slots__ = 'Q', 'u', 'v', 'mat'
    def __init__(self, Q: Vector3, u: Vector3, v: Vector3, mat: Material):
        '''Creates a 2D quadrilateral from the starting corner(Q), a vector representing the first side(u), 
        and a vector representing the second side(v)'''
        self.mat = mat
        self.Q = Q
        self.u = u
        self.v = v
        n = u.cross(v)
        self.w = Vector3.DivideScalar(n, n.dot(n))
        self.normal = n.UnitVector()
        self.D = self.normal.dot(Q)
        self = Quad.ComputeBoundingBox(self)
    @staticmethod
    def ComputeBoundingBox(self: 'Quad') -> 'Quad':
        '''Computes the bounding box of a quad and returns the quad with the bounding box attribute set'''
        bboxDiagonal1 = AABB.CreateBoundingBoxFromPoints(self.Q, self.Q + self.v + self.u)
        bboxDiagonal2 = AABB.CreateBoundingBoxFromPoints(self.Q + self.u, self.Q + self.v)
        self.boundingBox = AABB.CreateBoundingBoxFromBoxes(bboxDiagonal1, bboxDiagonal2)
        return self
    def hit(self: 'Quad', ray: Ray, t: Interval) -> HitRecord:
        '''Checks whether or not a ray hit the box and returns hit record information if it does'''
        denom = self.normal.dot(ray.direction)
        if fabs(denom) < 1e-8:
            return HitRecord.CreateFalseHit()
        hittime = (self.D - self.normal.dot(ray.origin)) / denom
        if not t.Contains(hittime):
            return HitRecord.CreateFalseHit()
        intersection = ray.PointAtTime(hittime)
        planarHitpointVector = intersection - self.Q
        alpha = self.w.dot(planarHitpointVector.cross(self.v))
        beta = self.w.dot(self.u.cross(planarHitpointVector))
        unitInterval = Interval(0,1)
        if not unitInterval.Contains(alpha) or not unitInterval.Contains(beta):
            return HitRecord.CreateFalseHit()
        else:
            hitrecord = HitRecord(intersection, Vector3(0,0,0), hittime, False, True, self.mat)
            hitrecord.u = alpha
            hitrecord.v = beta
            hitrecord.SetFaceNormal(ray, self.normal)
            return hitrecord
    @staticmethod
    def Box(bottomleftcorner: Vector3, toprightcorner: Vector3, mat: Material) -> hittableList:
        '''Creates a hittableList of 6 quadrilaterals forming a box from the bottom left and top right corner of the box'''
        sides = hittableList()
        mini = Vector3(fmin(bottomleftcorner.x, toprightcorner.x), fmin(bottomleftcorner.y, toprightcorner.y), fmin(bottomleftcorner.z, toprightcorner.z))
        maxi = Vector3(fmax(bottomleftcorner.x, toprightcorner.x), fmax(bottomleftcorner.y, toprightcorner.y), fmax(bottomleftcorner.z, toprightcorner.z))
        dx = Vector3(maxi.x - mini.x, 0, 0)
        dy = Vector3(0, maxi.y - mini.y, 0)
        dz = Vector3(0,0, maxi.z - mini.z)
        sides.add(Quad(Vector3(mini.x, mini.y, maxi.z), dx, dy, mat)) # Front side
        sides.add(Quad(Vector3(maxi.x, mini.y, maxi.z), dz.Negative(), dy, mat))# Right side
        sides.add(Quad(Vector3(maxi.x, mini.y, mini.z), dx.Negative(), dy, mat))# Back side
        sides.add(Quad(Vector3(mini.x, mini.y, mini.z), dz, dy, mat)) # Left side
        sides.add(Quad(Vector3(mini.x, maxi.y, maxi.z), dx, dz.Negative(), mat)) # Top side
        sides.add(Quad(Vector3(mini.x, mini.y, mini.z), dx, dz, mat)) # Bottom side
        return sides