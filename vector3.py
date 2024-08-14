# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Define a 3 coordinate system that will be used for positions and RGB colors(using aliases)
from math import sqrt, fabs
from interval import Interval
import rtutils
from numpy import fmin
class Vector3:
    # Constructor
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    # Override for + operator
    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    # Override for - operator
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    # Override for * operator
    def __mul__(self, other):
        try:
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        except:
            return Vector3(self.x * other, self.y * other, self.z * other)
    # Override for / operator
    def __truediv__(self, other):
        try:
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        except:
            return Vector3(0,0,0)
    def __truediv__(self, other: float):
        try:
            return Vector3(self.x / other, self.y / other, self.z / other)
        except:
            return Vector3(0,0,0)
    def ToRgbString(self):
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
    def LengthSquared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z
    def Length(self):
        return sqrt(self.LengthSquared())
    def UnitVector(self):
        return self / self.Length()
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    def Negative(self):
        return Vector3(-self.x, -self.y, -self.z)
    def cross(self, other):
        return Vector3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)
    @staticmethod
    def RandomVector():
        return Vector3(rtutils.RandomFloat(), rtutils.RandomFloat(), rtutils.RandomFloat())
    @staticmethod
    def RandomVectorRange(min: float, max: float):
        return Vector3(rtutils.RandomFloatRange(min, max), rtutils.RandomFloatRange(min, max), rtutils.RandomFloatRange(min, max))
    @staticmethod
    def RandomVectorInUnitSphere():
        while True:
            p = Vector3.RandomVectorRange(-1, 1)
            if p.LengthSquared() < 1:
                return p
    @staticmethod
    def RandomUnitVector():
        return Vector3.RandomVectorInUnitSphere().UnitVector()
    @staticmethod
    def RandomOnHemisphere(normal):
        onUnitSphere = Vector3.RandomUnitVector()
        if onUnitSphere.dot(normal) > 0.0:
            return onUnitSphere
        else:
            return onUnitSphere.Negative()
    @staticmethod
    def RandomInUnitDisk():
        while True:
            point = Vector3(rtutils.RandomFloatRange(-1, 1), rtutils.RandomFloatRange(-1, 1), 0)
            if point.LengthSquared() < 1:
                return point
    @staticmethod
    def LinearToGamma(linearComponent: float):
        if linearComponent > 0:
            return sqrt(linearComponent)
        else:
            return 0
    @staticmethod
    def Reflect(v1, v2):
        return v1 - v2 * v1.dot(v2) * 2
    def NearZero(self) -> bool:
        almostzero = 0.5
        if fabs(self.x) < almostzero and fabs(self.y) < almostzero and fabs(self.z) < almostzero:
            return True
        else:
            return False
    def Refract(self, othervec, etaiOverEtat):
        cosTheta = fmin(self.Negative().dot(othervec), 1.0)
        rOutPerp = (self + othervec * cosTheta) * etaiOverEtat
        rOutParallel = othervec * -sqrt(fabs(1.0 - rOutPerp.LengthSquared()))
        return rOutPerp + rOutParallel