from abc import ABC, abstractmethod
from rtutils import *
from vector3 import Vector3
from ray import Ray
from math import sqrt, log
import rtutils
from hittable import hittable, HitRecord
from texture import *
# Base abstract class, has blank methods that each class inheriting from this must define
class Material(ABC):
    @abstractmethod
    def Scatter(self, ray, rec) -> Ray:
        pass
    @abstractmethod
    def emitted(self, u: float, v: float, point: Vector3) -> Vector3:
        return Vector3(0,0,0)
# Matte material
class Lambertian(Material):
    # Creates a matte material from a texture
    def __init__(self, texture: Texture):
        self.tex = texture
    # This material does not emit any light
    def emitted(self, u: float, v: float, point: Vector3) -> Vector3:
        return Vector3(0,0,0)
    # Scatter reflected rays in a random direction outwards
    def Scatter(self, ray, rec) -> Ray:
        scatterDirection = rec.normal + Vector3.RandomUnitVector()
        if scatterDirection.NearZero():
            scatterDirection = rec.normal
        return Ray(rec.point, scatterDirection, True, self.tex.Value(rec.u, rec.v, rec.point), ray.time)
# Shiny material with hard reflections, depending on fuzz value
class Metal(Material):
    # Use a color and fuzz value to create the metal material
    def __init__(self, albedo: Vector3, fuzz: float):
        self.albedo = albedo
        if fuzz < 0:
            print("fuzz rounded up!")
            self.fuzz = 1
        else:
            self.fuzz = fuzz
    # This material does not emit any light
    def emitted(self, u: float, v: float, point: Vector3) -> Vector3:
        return Vector3(0,0,0)
    # Reflect rays more/less randomly based on fuzz value
    def Scatter(self, ray, rec) -> Ray:
        reflectedDir = Vector3.Reflect(ray.direction, rec.normal)
        reflectedDir = reflectedDir.UnitVector() + (Vector3.RandomUnitVector() * self.fuzz)
        if reflectedDir.dot(rec.normal) > 0:
            return Ray(rec.point, reflectedDir, True, self.albedo, ray.time)
        else:
            return Ray(rec.point, reflectedDir, False, self.albedo, ray.time)
# Material that refracts light
class Dielectric(Material):
    # Use a refraction index to create the material(how much the light is bent), use snell's law
    def __init__(self, refractionIndex: float):
        self.refractionIndex = refractionIndex
    # Shlick's approximation for reflectance
    def Reflectance(self, cosine, refractionIndex):
        r0 = (1 - refractionIndex) / (1 + refractionIndex)
        r0 = r0*r0
        return r0 + (1-r0)*pow((1-cosine), 5)
    def emitted(self, u: float, v: float, point: Vector3) -> Vector3:
        return Vector3(0,0,0)
    def Scatter(self, ray, rec) -> Ray:
        # Randomly choose between reflecting and refracting incoming rays of light
        if rec.frontface:
            refractionIndex = 1.0/self.refractionIndex
        else:
            refractionIndex = self.refractionIndex
        unitDir = ray.direction.UnitVector()
        cosTheta = fmin(unitDir.Negative().dot(rec.normal), 1.0)
        sinTheta = sqrt(1.0 - cosTheta*cosTheta)
        if refractionIndex * sinTheta > 1.0 or self.Reflectance(cosTheta, refractionIndex) > rtutils.RandomFloat():
            direction = Vector3.Reflect(unitDir, rec.normal)
        else:
            direction = unitDir.Refract(rec.normal, refractionIndex)
        return Ray(rec.point, direction, True, Vector3(1.0,1.0,1.0), ray.time)
# This material emits light into the scene
class DiffuseLight(Material):
    # Use a texture for the color values of the light to emit and their strength
    def __init__(self, tex: Texture):
        self.tex = tex
    # Emit the texture's color value for that point as light
    def emitted(self, u: float, v: float, point: Vector3) -> Vector3:
        return self.tex.Value(u, v, point)
    # Never reflect rays, other values here are just random placeholders
    def Scatter(self, ray, rec) -> Vector3:
        return Ray(Vector3(1,1,1), Vector3(1,1,1), False, Vector3(1,1,1), 1)
