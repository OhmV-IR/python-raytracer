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
    '''Abstract base class that all materials are derived from.
    Classes that inherit from this must implement the Scatter and emitted methods'''
    @abstractmethod
    def Scatter(self: 'Material', ray: Ray, rec: HitRecord) -> Ray:
        ''' Returns a ray scattered off the material given an inciting ray and hit record information'''
        pass
    @abstractmethod
    def emitted(self: 'Material', u: float, v: float, point: Vector3) -> Vector3:
        ''' Returns the light emitted from a material from a point and UV coordinates'''
        pass
# Matte material
class Lambertian(Material):
    '''Matte material with no light emittance and a random outwards direction scatter ray'''
    __slots__ = 'texture'
    # Creates a matte material from a texture
    def __init__(self: 'Lambertian', texture: Texture) -> 'Lambertian':
        '''Creates a lambertian(matte) material from a texture. '''
        self.tex = texture
    # This material does not emit any light
    def emitted(self: 'Lambertian', u: float, v: float, point: Vector3) -> Vector3:
        '''Returns the light emittance of the lambertian material for a point and UV coordinates.
        Lambertian materials do not emit light so this always returns 0,0,0'''
        return Vector3(0,0,0)
    # Scatter reflected rays in a random direction outwards
    def Scatter(self: 'Lambertian', ray, rec) -> Ray:
        '''This returns a scattered ray given an original inciting ray and hit information'''
        scatterDirection = rec.normal + Vector3.RandomUnitVector()
        if scatterDirection.NearZero():
            scatterDirection = rec.normal
        return Ray(rec.point, scatterDirection, True, self.tex.Value(rec.u, rec.v, rec.point), ray.time)
# Shiny material with hard reflections, depending on fuzz value
class Metal(Material):
    '''Shiny material with no light emittance and reflectance based on fuzz value(less fuzz, sharper reflection)'''
    __slots__ = 'albedo', 'fuzz'
    # Use a color and fuzz value to create the metal material
    def __init__(self: 'Metal', albedo: Vector3, fuzz: float) -> 'Metal':
        '''Creates a metal material from a color and a fuzz value between 0 and 1'''
        self.albedo = albedo
        if fuzz < 0:
            self.fuzz = 1
        else:
            self.fuzz = fuzz
    # This material does not emit any light
    def emitted(self: 'Metal', u: float, v: float, point: Vector3) -> Vector3:
        '''Returns the light emittance of the metal material for a point and UV coordinates. 
        Metal materials do not emit light so this always returns (0,0,0) / black'''
        return Vector3(0,0,0)
    # Reflect rays more/less randomly based on fuzz value
    def Scatter(self: 'Metal', ray: Ray, rec: HitRecord) -> Ray:
        ''' Returns the scattered ray reflecting off the metal material given the inciting ray and hit record information
        This should produce a sharp / fuzzy reflected ray based on the fuzz value given to the constructor. '''
        reflectedDir = Vector3.Reflect(ray.direction, rec.normal)
        reflectedDir = reflectedDir.UnitVector() + (Vector3.MultiplyScalar(Vector3.RandomUnitVector(), self.fuzz))
        if reflectedDir.dot(rec.normal) > 0:
            return Ray(rec.point, reflectedDir, True, self.albedo, ray.time)
        else:
            return Ray(rec.point, reflectedDir, False, self.albedo, ray.time)
# Material that refracts light
class Dielectric(Material):
    '''A material that does not emit any light and refracts rays inwards or reflects them outwards'''
    __slots__ = 'refractionIndex'
    # Use a refraction index to create the material(how much the light is bent), use snell's law
    def __init__(self: 'Dielectric', refractionIndex: float) -> 'Dielectric':
        '''Create a dielectric material from a refraction index'''
        self.refractionIndex = refractionIndex
    # Shlick's approximation for reflectance
    def Reflectance(self: 'Dielectric', cosine: float, refractionIndex: float) -> float:
        '''Reflect an incoming ray outwards'''
        r0 = (1 - refractionIndex) / (1 + refractionIndex)
        r0 = r0*r0
        return r0 + (1-r0)*pow((1-cosine), 5)
    def emitted(self: 'Dielectric', u: float, v: float, point: Vector3) -> Vector3:
        '''Return the light emittance of the dielectric material. The dielectric material does
        not emit light so this will always return (0,0,0)/black '''
        return Vector3(0,0,0)
    def Scatter(self: 'Dielectric', ray: Ray, rec: HitRecord) -> Ray:
        '''Scatters an initial ray by either reflecting it off the material or refracting it through the material
        based on the refraction index'''
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
    '''A material that emits light into the scene from a texture'''
    __slots__ = 'tex'
    # Use a texture for the color values of the light to emit and their strength
    def __init__(self: 'DiffuseLight', tex: Texture) -> 'DiffuseLight':
        '''Creates a diffuse light material from a texture'''
        self.tex = tex
    # Emit the texture's color value for that point as light
    def emitted(self: 'DiffuseLight', u: float, v: float, point: Vector3) -> Vector3:
        '''Emits the light of the color of the texture at the provided point and UV coordinates'''
        return self.tex.Value(u, v, point)
    # Never reflect rays, other values here are just random placeholders
    def Scatter(self: 'DiffuseLight', ray: Ray, rec: HitRecord) -> Ray:
        '''This material does not scatter light therefore this function will always return a ray with the scattered property set to false'''
        return Ray.CreateNullRay()
class Isotropic(Material):
    '''Picks a random uniform direction to scatter a ray in'''
    __slots__ = 'tex'
    def __init__(self: 'Isotropic', texture: Texture):
        '''Creates an isotropic material from a source texture'''
        self.tex = texture
    def emitted(self: 'Isotropic', u: float, v: float, point: Vector3) -> Vector3:
        '''This material does not emit light and therefore this function will always return 0,0,0 / black'''
        return Vector3(0,0,0)
    def Scatter(self: 'Isotropic', ray: Ray, rec: HitRecord) -> Ray:
        '''Takes an input ray and hitrecord information and scatters it in a random direction'''
        return Ray(rec.point, Vector3.RandomUnitVector(), True, self.tex.Value(rec.u, rec.v, rec.point), ray.time)