# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Define a 3 coordinate system that will be used for positions, directions, and RGB colors(using aliases)
from math import sqrt, fabs, cos, sin
from interval import Interval
import rtutils
class Vector3:
    '''Class containing 3 floats in a xyz structure. Can be used to represent positions, directions, RGB colors .etc'''
    __slots__ = 'x','y','z'
    # Constructor
    def __init__(self: 'Vector3', x: float, y: float, z: float) -> 'Vector3':
        '''Creates a Vector3 from the x y and z float values'''
        self.x = x
        self.y = y
        self.z = z
    # Override for + operator
    def __add__(self: 'Vector3', v2: 'Vector3') -> 'Vector3':
        '''Returns the addition of two vectors by adding each coordinate'''
        return Vector3(self.x + v2.x, self.y + v2.y, self.z + v2.z)
    def __sub__(self: 'Vector3', v2: 'Vector3') -> 'Vector3':
        '''Returns the subtraction of two vectors by subtracting each coordinate'''
        return Vector3(self.x - v2.x, self.y - v2.y, self.z - v2.z)
    @staticmethod
    def Multiply(v1: 'Vector3', v2: 'Vector3') -> 'Vector3':
        '''Returns the multiplication of a vector and a vector by multiplying each coordinate'''
        return Vector3(v1.x * v2.x, v1.y * v2.y, v1.z * v2.z)
    @staticmethod
    def MultiplyScalar(v1: 'Vector3', f: float) -> 'Vector3':
        '''Returns the multiplication of a vector and a scalar by multiplying each coordinate'''
        return Vector3(v1.x * f, v1.y * f, v1.z * f)
    @staticmethod
    def Divide(v1: 'Vector3', v2: 'Vector3') -> 'Vector3':
        '''Returns the division of 2 vectors by dividing each coordinate'''
        return Vector3(v1.x / v2.x, v1.y / v2.y, v1.z / v2.z)
    @staticmethod
    def DivideScalar(v1: 'Vector3', f: float) -> 'Vector3':
        '''Returns the division of a vector by a scalar by dividing each coordinate'''
        return Vector3(v1.x / f, v1.y / f, v1.z / f)
    def ToRgbString(self: 'Vector3'):
        '''Converts an RGB color vector to a string in PPM format that can be written to the image file'''
        intensity = Interval(0.000, 0.999)
        r = self.x
        g = self.y
        b = self.z
        r = Vector3.LinearToGamma(r)
        g = Vector3.LinearToGamma(g)
        b = Vector3.LinearToGamma(b)
        rbyte = int(256 * intensity.Clamp(self.x))
        gbyte = int(256 * intensity.Clamp(self.y))
        bbyte = int(256 * intensity.Clamp(self.z))
        return str(rbyte) + " " + str(gbyte) + " " + str(bbyte) + "\n"  
    def LengthSquared(self: 'Vector3') -> float:
        '''Returns the length of the vector squared by squaring each coordinate, adding them and returning the result'''
        return self.x * self.x + self.y * self.y + self.z * self.z
    def Length(self: 'Vector3') -> float:
        ''' Returns the length of the vector by taking the square root of the LengthSquared operation'''
        return sqrt(self.LengthSquared())
    def UnitVector(self: 'Vector3') -> 'Vector3':
        '''Turns the vector into a unit vector with a magnitude of 1'''
        return Vector3.DivideScalar(self,self.Length())
    def dot(self: 'Vector3', other: 'Vector3') -> float:
        '''Multiplies the vector by another vector and returns the addition of the coordinates of the result'''
        return self.x * other.x + self.y * other.y + self.z * other.z
    def Negative(self: 'Vector3') -> 'Vector3':
        '''Returns the inverse vector(flips +- on each coordinate)'''
        return Vector3(-self.x, -self.y, -self.z)
    def cross(self: 'Vector3', other: 'Vector3') -> 'Vector3':
        return Vector3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    @staticmethod
    def RandomVector():
        '''Creates a random vector with each coordinate between 0 and 1'''
        return Vector3(rtutils.RandomFloat(), rtutils.RandomFloat(), rtutils.RandomFloat())
    @staticmethod
    def RandomVectorRange(min: float, max: float):
        '''Creates a random vector with each coordinate a random value between a minimum and maximum'''
        return Vector3(rtutils.RandomFloatRange(min, max), rtutils.RandomFloatRange(min, max), rtutils.RandomFloatRange(min, max))
    @staticmethod
    def RandomVectorInUnitSphere() -> 'Vector3':
        '''Creates a random vector inside of a unit sphere'''
        while True:
            p = Vector3.RandomVectorRange(-1, 1)
            if p.LengthSquared() < 1:
                return p
    @staticmethod
    def RandomCosineDirection() -> 'Vector3':
        '''Creates a random vector weighted by PDF'''
        r1 = rtutils.RandomFloat()
        r2 = rtutils.RandomFloat()
        phi = 2*rtutils.pi*r1
        x = cos(phi) * sqrt(r2)
        y = sin(phi) * sqrt(r2)
        z = sqrt(1-r2)
        return Vector3(x,y,z)
    @staticmethod
    def RandomUnitVector() -> 'Vector3':
        '''Returns a random unit vector'''
        return Vector3.RandomVectorInUnitSphere().UnitVector()
    @staticmethod
    def RandomOnHemisphere(normal: 'Vector3') -> 'Vector3':
        '''Returns a random vector on a hemisphere'''
        onUnitSphere = Vector3.RandomUnitVector()
        if onUnitSphere.dot(normal) > 0.0:
            return onUnitSphere
        else:
            return onUnitSphere.Negative()
    @staticmethod
    def RandomInUnitDisk() -> 'Vector3':
        '''Returns a random vector in a unit disk'''
        while True:
            point = Vector3(rtutils.RandomFloatRange(-1, 1), rtutils.RandomFloatRange(-1, 1), 0)
            if point.LengthSquared() < 1:
                return point
    @staticmethod
    def LinearToGamma(linearComponent: float) -> float:
        '''If the linear component is > 0, then the sqrt of the linear component is returned otherwise return 0'''
        if linearComponent > 0:
            return sqrt(linearComponent)
        else:
            return 0
    @staticmethod
    def Reflect(v1: 'Vector3', v2: 'Vector3') -> 'Vector3':
        '''Reflects a vector v1 along a normal v2'''
        return v1 - Vector3.MultiplyScalar(v2, v1.dot(v2) * 2)
    def NearZero(self: 'Vector3') -> bool:
        '''Returns true if the vector is close to 0(prone to floating point errors)'''
        almostzero = 0.0001
        if fabs(self.x) < almostzero and fabs(self.y) < almostzero and fabs(self.z) < almostzero:
            return True
        else:
            return False
    def Refract(self: 'Vector3', normal: 'Vector3', etaiOverEtat: float) -> 'Vector3':
        '''Refracts the vector using a normal and a refraction index'''
        cosTheta = rtutils.fmin(self.Negative().dot(normal), 1.0)
        rOutPerp = Vector3.MultiplyScalar((self + Vector3.MultiplyScalar(normal, cosTheta)), etaiOverEtat)
        rOutParallel = Vector3.MultiplyScalar(normal, -sqrt(fabs(1.0 - rOutPerp.LengthSquared())))
        return rOutPerp + rOutParallel
    
class OrthonormalBasis:
    def __init__(self: 'OrthonormalBasis', n: Vector3):
        if(n.x == 0):
            n.x = 1e-8
        if(n.y == 0):
            n.y = 1e-8
        if(n.z == 0):
            n.z = 1e-8
        self.axis = [Vector3(0,0,0), Vector3(0,0,0), Vector3(0,0,0)]
        self.axis[2] = n.UnitVector()
        if fabs(self.axis[2].x > 0.9):
            a = Vector3(0,1,0)
        else:
            a = Vector3(1,0,0)
        self.axis[1] = self.axis[2].cross(a).UnitVector()
        self.axis[0] = self.axis[2].cross(self.axis[1])
    def u(self: 'OrthonormalBasis') -> Vector3:
        return self.axis[0]
    def v(self: 'OrthonormalBasis') -> Vector3:
        return self.axis[1]
    def w(self: 'OrthonormalBasis') -> Vector3:
        return self.axis[2]
    def Transform(self: 'OrthonormalBasis', v: Vector3) -> Vector3:
        return Vector3.MultiplyScalar(self.axis[0], v.x) + Vector3.MultiplyScalar(self.axis[1], v.y) + Vector3.MultiplyScalar(self.axis[2], v.z)