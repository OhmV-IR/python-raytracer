# P2.0 Final Project
# REDACTED(I <3 not doxing myself)
# Raytracer
from vector3 import Vector3
from abc import abstractmethod
from math import floor, fabs, sin
from interval import Interval
import rtutils
import PIL.Image
# Code to import image, and fetch colors from it
class RTImage:
    def __init__(self, path: str):
        self.image = PIL.Image.open(path)
        if self.image.width == 0 and self.image.height == 0:
            self.image = None
    def GetPixelColor(self, x: int, y: int):
        return self.image.getpixel((x, y))
    @staticmethod
    def Clamp(x: int, low: int, high: int):
        if x < low:
            return low
        if x < high:
            return x
        else:
            return high-1
# Class to generate perlin noise
class PerlinNoise:
    def __init__(self):
        # Create 256 random unit vectors between -1 and 1
        self.pointCount = 256
        self.randvec = []
        for i in range(0, self.pointCount):
            self.randvec.append(Vector3.RandomVectorRange(-1, 1).UnitVector())
        # Generate 256 strengths in each direction and shuffle them
        self.permX = PerlinNoise.PerlinGeneratePerm(self.pointCount)
        self.permY = PerlinNoise.PerlinGeneratePerm(self.pointCount)
        self.permZ = PerlinNoise.PerlinGeneratePerm(self.pointCount)
        
    def Noise(self, point: Vector3):
        # Pick a strength using the 3 lists of strengths and the point where the hit occurred
        u = point.x - floor(point.x)
        v = point.y - floor(point.y)
        w = point.z - floor(point.z)
        i = int(floor(point.x))
        j = int(floor(point.y))
        k = int(floor(point.z))
        if i < 0: 
            i = 0
        if j < 0:
            j = 0
        if k < 0:
            k = 0
        c = [[[0 for k in range(2)] for j in range(2)] for i in range(2)]
        for di in range(0, 2):
            for dj in range(0,2):
                for dk in range(0,2):
                    idi = i + di
                    if idi > 255:
                        idi = 255
                    jdj = j + dj
                    if jdj > 255:
                        jdj = 255
                    kdk = k + dk
                    if kdk > 255:
                        kdk = 255
                    c[di][dj][dk] = self.randvec[
                        self.permX[idi] ^
                        self.permY[jdj] ^
                        self.permZ[kdk]
                    ]
        # Interpolate the strength to make it appear less blocky and more smooth
        return PerlinNoise.PerlinInterpolation(c, u, v, w)
    # Repeadeately call the noise function to smooth out the texture even further
    def Turbulence(self, point: Vector3, depth: int):
        accum = 0.0
        tempPoint = point
        weight = 1.0
        for i in range(0,depth):
            accum += weight * self.Noise(tempPoint)
            weight *= 0.5
            tempPoint *= 2
        return fabs(accum)
    @staticmethod
    def PerlinGeneratePerm(pointcount: int):
        p = []
        # Generate an ascending list of numbers and then shuffle them
        for i in range(0, pointcount):
            p.append(i)
        p = PerlinNoise.Permute(p, pointcount)
        return p
    @staticmethod
    def Permute(p, pointcount: int):
        # Function to shuffle strength lists
        for i in range(pointcount-1, 1, -1):
            target = rtutils.RandomInteger(0, i)
            tmp = p[i]
            p[i] = p[target]
            p[target] = tmp
        return p
    @staticmethod
    def PerlinInterpolation(c, u, v, w):
        # Trilinear interpolation to smooth out the perlin texture
        uu = u*u*(3-2*u)
        vv = v*v*(3-2*v)
        ww = w*w*(3-2*w)
        accum = 0.0
        for i in range(0,2):
            for j in range(0,2):
                for k in range(0,2):
                    weight = Vector3(u-i, v-j, w-k)
                    accum += (i*uu + (1-i)*(1-uu)) * (j*vv + (1-j)*(1-vv)) * (k*ww + (1-k)*(1-ww)) * c[i][j][k].dot(weight)
        return accum
# Base texture class to define the Value method that each individual texture sets
class Texture:
    @abstractmethod
    def Value(self, u: float, v: float, point: Vector3) -> Vector3:
        pass
# Always return a specified RGB color through this texture
class SolidColor(Texture):
    def __init__(self, albedo: Vector3):
        self.albedo = albedo
    def Value(self, u: float, v: float, point: Vector3) -> Vector3:
        return self.albedo
# Combine 2 textures to make a checkered pattern and choose between the two based on the location of the hit
class CheckerTexture(Texture):
    def __init__(self, scale: float, even: Texture, odd: Texture):
        self.invScale = 1.0 / scale
        self.even = even
        self.odd = odd
    def Value(self, u: float, v: float, point: Vector3) -> Vector3:
        xInteger = int(floor(self.invScale * point.x))
        yInteger = int(floor(self.invScale * point.y))
        zInteger = int(floor(self.invScale * point.z))

        if (xInteger + yInteger + zInteger) % 2 == 0:
            return self.even.Value(u, v, point)
        else:
            return self.odd.Value(u, v, point)
# Use an image for the color values of the object
class ImageTexture(Texture):
    # Get the string path of the image to use
    def __init__(self, filepath: str):
        self.img = RTImage(filepath)
    # Map the 2D location on the object that was hit to pixel coordinates on the image and return the color value from the image
    def Value(self, u: float, v: float, point: Vector3) -> Vector3:
        if self.img.image.height <= 0:
            return Vector3(0,1,1)
        u = Interval(0,1).Clamp(u)
        v = 1.0 - Interval(0,1).Clamp(v)
        i = int(u * self.img.image.width)
        j = int(v * self.img.image.height)
        pixelColor = self.img.GetPixelColor(i, j)
        colorscale = 1.0 / 255.0
        return Vector3(colorscale * pixelColor[0], colorscale * pixelColor[1], colorscale * pixelColor[2])
# Create a texture from perlin noise(blocks of random color)
class NoiseTexture(Texture):
    # Use a scale value to define how large the blocks are
    def __init__(self, scale: float):
        self.noise = PerlinNoise()
        self.scale = scale
    # Return a heavily scrambled and interpolated random color from the perlin noise function
    def Value(self, u: float, v: float, point: Vector3) -> Vector3:
        return Vector3(0.5, 0.5, 0.5) * (1 + sin(self.scale * point.z + 10 * self.noise.Turbulence(point, 7)))