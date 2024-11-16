from math import tan
from hittable import hittable, hittableList
from ray import Ray
from interval import Interval
from vector3 import Vector3
from rtutils import *
class Camera:
    '''Point of view from which scenes are rendered to create an image output'''
    __slots__ = 'samplesPerPixel', 'cameraCenter', 'w', 'u', 'v', 'viewportHeightVector', 'sampleScale', 'maxDepth', 'outputLocation', 'aspectRatio', 'imageWidth', 'vfov', 'defocusAngle', 'focusDistance', 'backgroundColor', 'theta', 'h', 'focal_length', 'viewportHeight', 'imageHeight', 'viewportWidth', 'viewportWidthVector', 'pixelDeltaWidthVector', 'pixelDeltaHeightVector', 'viewportUpperLeft', 'pixel00Location', 'defocusRadius', 'defocusDiskU', 'defocusDiskV'
    def Render(self, world: hittableList):
        '''Renders a hittableList scene and outputs the image to a file in PPM format'''
        logFile = open('logfile.txt', 'w')
        outputFile = open(self.outputLocation, 'w')
        outputFile.write("P3\n" + str(self.imageWidth) + " " + str(self.imageHeight) + "\n255\n")
        for j in range(0, self.imageHeight):
            logFile.write('Lines remaining: ' + str(self.imageHeight - j))
            print('Lines remaining: ' + str(self.imageHeight - j))
            for i in range(0,self.imageWidth):
                color = Vector3(0,0,0)
                for s in range(0,self.samplesPerPixel):
                    ray = self.GetRay(i, j)
                    color += self.RayColor(ray, self.maxDepth, world)
                color = color * self.sampleScale
                outputFile.write(color.ToRgbString())
    def DefocusDiskSample(self):
        point = Vector3.RandomInUnitDisk()
        return self.cameraCenter + (self.defocusDiskU * point.x) + (self.defocusDiskV * point.y)
    def GetRay(self, i: int, j: int) -> Ray:
        '''Creates a ray from pixel coordinates of the image'''
        offset = self.SampleSquare()
        pixelSample = self.pixel00Location + (self.pixelDeltaWidthVector * (i + offset.x)) + (self.pixelDeltaHeightVector * (j + offset.y))
        if self.defocusAngle <= 0:
            rayOrigin = self.cameraCenter
        else:
            rayOrigin = self.DefocusDiskSample()
        rayDirection = pixelSample - self.cameraCenter
        rayTime = RandomFloat()
        return Ray(rayOrigin, rayDirection, False, Vector3(0,0,0), rayTime)
    def SampleSquare(self) -> Vector3:
        '''Creates a square from where samples will be taken to reduce noise / floating point errors and produce a clearer image'''
        return Vector3(RandomFloat() - 0.5, RandomFloat() - 0.5, 0)
    def __init__(self, aspectRatio=16/9, imageWidth=400, samplesPerPixel=10, maxDepth=10, vfov=90, lookfrom=Vector3(0,0,0), lookat=Vector3(0,0,-1), vup=Vector3(0,1,0), defocusAngle=0, focusDistance=10, backgroundColor=Vector3(0.0, 0.0, 1.0), outputLocation="output.ppm"):
        '''Creates a new camera from an aspect ratio, image width(height is determined from the width), sample count, maximum scatter rays, FOV, origin, look direction and camera upwards vector, defocus angle, focus distance, background color and output file location'''
        self.samplesPerPixel=samplesPerPixel
        self.sampleScale = 1.0 / samplesPerPixel
        self.maxDepth = maxDepth
        self.outputLocation = outputLocation
        self.aspectRatio = aspectRatio
        self.imageWidth = imageWidth
        self.vfov = vfov
        self.defocusAngle = defocusAngle
        self.focusDistance = focusDistance
        self.backgroundColor = backgroundColor
        self.theta = DegreesToRadians(vfov)
        self.h = tan(self.theta/2)
        self.focal_length = (lookfrom - lookat).Length()
        self.viewportHeight = 2.0 * self.h * self.focusDistance
        self.cameraCenter = lookfrom
        self.w = (lookfrom - lookat).UnitVector()
        self.u = vup.cross(self.w)
        self.v = self.w.cross(self.u)
        self.viewportHeightVector = self.v.Negative() * self.viewportHeight
        self.imageHeight = int(self.imageWidth / self.aspectRatio)
        if self.imageHeight < 1:
            self.imageHeight = 1
        self.viewportWidth = self.viewportHeight * (float(self.imageWidth)/self.imageHeight)
        self.viewportWidthVector = self.u * self.viewportWidth
        self.pixelDeltaWidthVector = self.viewportWidthVector / self.imageWidth
        self.pixelDeltaHeightVector = self.viewportHeightVector / self.imageHeight
        self.viewportUpperLeft = self.cameraCenter - (self.w * self.focusDistance) - self.viewportWidthVector / 2 - self.viewportHeightVector / 2
        self.pixel00Location = self.viewportUpperLeft + (self.pixelDeltaWidthVector + self.pixelDeltaHeightVector) * 0.5
        self.defocusRadius = self.focusDistance * tan(DegreesToRadians(self.defocusAngle / 2))
        self.defocusDiskU = self.u * self.defocusRadius
        self.defocusDiskV = self.v * self.defocusRadius
    def RayColor(self, ray: Ray, depth: int, world: hittableList) -> Vector3:
        '''Gets the color of a ray by setting it out into the scene with a depth(maximum number of scattered rays)
        Depth is a major performance factor to consider, if renders are taking too long consider lowering it'''
        if depth <= 0:
            return Vector3(0,0,0)
        rec = world.hit(ray, Interval(0.0001, infinity))
        if rec.hit == True:
            emissionColor = rec.mat.emitted(rec.u, rec.v, rec.point)
            scatteredRay = rec.mat.Scatter(ray, rec)
            if not scatteredRay.scattered:
                return emissionColor
            else:
                scatterColor = scatteredRay.attenuation * self.RayColor(scatteredRay, depth-1, world)
                return emissionColor + scatterColor
        else:
            return self.backgroundColor