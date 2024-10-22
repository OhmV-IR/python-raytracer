# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Basic raytracing algorithm
from camera import Camera
from rtutils import *
from material import Dielectric, Lambertian, Metal, DiffuseLight, Material
from texture import SolidColor, CheckerTexture, ImageTexture, Texture, NoiseTexture
from Quadrilateral import Quad, Box
from sphere import Sphere
from hittable import *
world = hittableList(True)
def RenderCornellEmpty(filePath: str):
    rtworld = hittableList(True)
    red = Lambertian(SolidColor(Vector3(.65, .05, .05)))
    white = Lambertian(SolidColor(Vector3(.73, .73, .73)))
    green = Lambertian(SolidColor(Vector3(.12, .45, .15)))
    light = DiffuseLight(SolidColor(Vector3(21,21,21)))
    rtworld.add(Quad(Vector3(555,0,0), Vector3(0,555,0), Vector3(0,0,555), green))
    rtworld.add(Quad(Vector3(0,0,0), Vector3(0,555,0), Vector3(0,0,555), red))
    rtworld.add(Quad(Vector3(343,554,332), Vector3(-130, 0, 0), Vector3(0, 0, -105), light))
    rtworld.add(Quad(Vector3(0,0,0), Vector3(555,0,0), Vector3(0,0,555), white))
    rtworld.add(Quad(Vector3(555,555,555), Vector3(-555,0,0), Vector3(0,0,-555), white))
    rtworld.add(Quad(Vector3(0,0,555), Vector3(555,0,0), Vector3(0,555,0), white))
    camera = Camera(1,600, 200, 50, 40, Vector3(278,278, -800), Vector3(278, 278, 0), Vector3(0,1,0), 0, 10, Vector3(0,0,0), filePath)
    camera.Render(rtworld)
def RenderCornellBoxes(filePath: str):
    rtworld = hittableList(True)
    red = Lambertian(SolidColor(Vector3(.65, .05, .05)))
    white = Lambertian(SolidColor(Vector3(.73, .73, .73)))
    green = Lambertian(SolidColor(Vector3(.12, .45, .15)))
    light = DiffuseLight(SolidColor(Vector3(21,21,21)))
    rtworld.add(Quad(Vector3(555,0,0), Vector3(0,555,0), Vector3(0,0,555), green))
    rtworld.add(Quad(Vector3(0,0,0), Vector3(0,555,0), Vector3(0,0,555), red))
    rtworld.add(Quad(Vector3(343,554,332), Vector3(-130, 0, 0), Vector3(0, 0, -105), light))
    rtworld.add(Quad(Vector3(0,0,0), Vector3(555,0,0), Vector3(0,0,555), white))
    rtworld.add(Quad(Vector3(555,555,555), Vector3(-555,0,0), Vector3(0,0,-555), white))
    rtworld.add(Quad(Vector3(0,0,555), Vector3(555,0,0), Vector3(0,555,0), white))
    rtworld.add(Box(Vector3(130,0,65), Vector3(295, 165, 230), white))
    rtworld.add(Box(Vector3(265, 0, 295), Vector3(430, 330, 460), white))
    camera = Camera(1,600, 200, 50, 40, Vector3(278,278, -800), Vector3(278, 278, 0), Vector3(0,1,0), 0, 10, Vector3(0,0,0), filePath)
    camera.Render(rtworld)
def RenderCornellBoxesTranslate(filePath: str):
    rtworld = hittableList(True)
    red = Lambertian(SolidColor(Vector3(.65, .05, .05)))
    white = Lambertian(SolidColor(Vector3(.73, .73, .73)))
    green = Lambertian(SolidColor(Vector3(.12, .45, .15)))
    light = DiffuseLight(SolidColor(Vector3(21,21,21)))
    rtworld.add(Quad(Vector3(555,0,0), Vector3(0,555,0), Vector3(0,0,555), green))
    rtworld.add(Quad(Vector3(0,0,0), Vector3(0,555,0), Vector3(0,0,555), red))
    rtworld.add(Quad(Vector3(343,554,332), Vector3(-130, 0, 0), Vector3(0, 0, -105), light))
    rtworld.add(Quad(Vector3(0,0,0), Vector3(555,0,0), Vector3(0,0,555), white))
    rtworld.add(Quad(Vector3(555,555,555), Vector3(-555,0,0), Vector3(0,0,-555), white))
    rtworld.add(Quad(Vector3(0,0,555), Vector3(555,0,0), Vector3(0,555,0), white))
    rtworld.add(Translate(Box(Vector3(130,0,65), Vector3(295, 165, 230), white), Vector3(0, 0, 100)))
    rtworld.add(Translate(Box(Vector3(265, 0, 295), Vector3(430, 330, 460), white), Vector3(0,0,100)))
    camera = Camera(1,600, 100, 50, 40, Vector3(278,278, -800), Vector3(278, 278, 0), Vector3(0,1,0), 0, 10, Vector3(0,0,0), filePath)
    camera.Render(rtworld)
def RenderEarth(filePath: str):
    rtworld = hittableList(True)
    earthtex = ImageTexture("earthmap.jpg")
    earthsurface = Lambertian(earthtex)
    rtworld.add(Sphere(2, Vector3(0,0,0), earthsurface))
    camera = Camera(16/9, 400, 100, 50, 20, Vector3(0,0,12), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderPerlin(filePath: str):
    rtworld = hittableList(True)
    pertext = NoiseTexture(4)
    rtworld.add(Sphere(1000, Vector3(0, -1000, 0), Lambertian(pertext)))
    rtworld.add(Sphere(2, Vector3(0,2,0), Lambertian(pertext)))
    camera = Camera(16/9, 400, 100, 50, 20, Vector3(13,2,3), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderDielectric(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matcenter = Lambertian(SolidColor(Vector3(0.1, 0.2, 0.5)))
    matleft = Dielectric(1.5)
    matbubble = Dielectric(1/1.5)
    matright = Metal(Vector3(0.8, 0.6, 0.2), 0)
    rtworld.add(Sphere(100, Vector3(0, -100.5, -1), matground))
    rtworld.add(Sphere(0.5, Vector3(0,0,-1.2), matcenter))
    rtworld.add(Sphere(0.5, Vector3(-1,0,-1), matleft))
    rtworld.add(Sphere(0.4, Vector3(-1,0,-1), matbubble))
    rtworld.add(Sphere(0.5, Vector3(1.0, 0, -1), matright))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderMetals(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matcenter = Lambertian(SolidColor(Vector3(0.1, 0.2, 0.5)))
    matleft = Metal(Vector3(0.8, 0.8, 0.8), 0.3)
    matright = Metal(Vector3(0.8, 0.6, 0.2), 1.0)
    rtworld.add(Sphere(100.0, Vector3(0.0, -100.5, -1.0), matground))
    rtworld.add(Sphere(0.5, Vector3(0, 0, -1.2), matcenter))
    rtworld.add(Sphere(0.5, Vector3(-1, 0, -1), matleft))
    rtworld.add(Sphere(0.5, Vector3(1, 0, -1), matright))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderRTOneWeekend(filePath: str):
    rtworld = hittableList(True)
    groundmat = Lambertian(SolidColor(Vector3(0.5, 0.5, 0.5)))
    for a in range(-11, 11):
        for b in range(-11, 11):
            choosemat = RandomFloat()
            center = Vector3(a + 0.9*RandomFloat(), 0.2, b+ 0.9*RandomFloat())
            if (center - Vector3(4, 0.2, 0)).Length() > 0.9:
                if choosemat < 0.8:
                    albedo = Vector3.RandomVector()
                    spheremat = Lambertian(SolidColor(albedo))
                    rtworld.add(Sphere(0.2, center, spheremat))
                elif choosemat < 0.95:
                    albedo = Vector3.RandomVectorRange(0.5, 1)
                    fuzz = RandomFloatRange(0, 0.5)
                    spheremat = Metal(albedo, fuzz)
                    rtworld.add(Sphere(0.2, center, spheremat))
                else:
                    spheremat = Dielectric(1.5)
                    world.add(Sphere(0.2, center, spheremat))
    mat1 = Dielectric(1.5)
    rtworld.add(Sphere(1.0, Vector3(0,1,0), mat1))
    mat2 = Lambertian(SolidColor(Vector3(0.4, 0.2, 0.1)))
    rtworld.add(Sphere(1.0, Vector3(-4, 1, 0), mat2))
    mat3 = Metal(Vector3(0.7, 0.6, 0.5), 0.0)
    rtworld.add(Sphere(1.0, Vector3(4,1,0), mat3))
    camera = Camera(16/9, 1200, 250, 50, 20, Vector3(13,2,3), Vector3(0,0,0), Vector3(0,1,0), 0.6, 10.0, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderLambertianCheckered(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matright = Lambertian(SolidColor(Vector3(0.1, 0.1, 0.8)))
    matleft = Lambertian(SolidColor(Vector3(0.9, 0.2, 0.1)))
    matcenter = Lambertian(CheckerTexture(0.5, SolidColor(Vector3(0.1, 0.9, 0.1)), SolidColor(Vector3(0.1, 0.1, 0.9))))
    rtworld.add(Sphere(100.0, Vector3(0.0, -100.5, -1.0), matground))
    rtworld.add(Sphere(0.5, Vector3(0, 0, -1.2), matcenter))
    rtworld.add(Sphere(0.5, Vector3(-1, 0, -1), matleft))
    rtworld.add(Sphere(0.5, Vector3(1, 0, -1), matright))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderMovingSpheres(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matleft = Lambertian(SolidColor(Vector3(0.9, 0.2, 0.1)))
    rtworld.add(Sphere(100.0, Vector3(0.0, -100.5, -1.0), matground))
    rtworld.add(Sphere(0.5, Vector3(-1, 0, -1), matleft, True, Vector3(1,0,-1)))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)    
def TextureSelector(isDiffuseLight=False) -> Texture:
    while True:
        texturetype = input("Please enter a texture type:\nSolid Color\nCheckered\nImage\nNoise\n")
        if texturetype == "Solid color" or texturetype == "Solid Color":
            while True:
                try:
                    if isDiffuseLight:
                        r = float(input("Please enter red color value(ex: 8): "))
                        g = float(input("Please enter green color value(ex: 15): "))
                        b = float(input("Please enter blue color value(ex: 23): "))
                    else:
                        r = float(input("Please enter red color value as a percentage(ex: 0.59): "))
                        g = float(input("Please enter green color value as a percentage(ex: 0.23): "))
                        b = float(input("Please enter blue color value as a percentage(ex: 0.99): ")) 
                    if isDiffuseLight:
                        if r > 0 and g > 0 and b > 0:
                            return SolidColor(Vector3(r,g,b))
                    if r > 0 and r < 1 and g > 0 and g < 1 and b > 0 and b < 1:
                        return SolidColor(Vector3(r,g,b))
                except:
                    pass
        elif texturetype == "Checkered" or texturetype == "checkered":
            print("Please select the even texture:")
            t1 = TextureSelector()
            print("Please select the odd texture")
            t2 = TextureSelector()
            while True:
                try:
                    scale = float(input("Please enter the scale of the texture: "))
                except:
                    pass
                else:
                    break
            return CheckerTexture(scale, t1, t2)
        elif texturetype == "Image" or texturetype == "image":
            return ImageTexture(input("Please enter the path of the image texture: "))
        elif texturetype == "Noise":
            while True:
                try:
                    scale = float(input("Please enter the scale of the noise texture: "))
                except:
                    pass
                else:
                    break
            return NoiseTexture(scale)
        else:
            print("Command not recognized")
def SelectMaterial() -> Material:
    while True:
        mattype = input("Please enter a material type:\nLambertian\nMetal\nDiffuse Light\nDielectric\n")
        if mattype == "Lambertian" or mattype == "lambertian":
            return Lambertian(TextureSelector())
        elif mattype == "Metal" or mattype == "metal":
            while True:
                try:
                    r = float(input("Please enter the red color value as a percentage(ex: 0.59): "))
                    g = float(input("Please enter the green color value in the same format: "))
                    b = float(input("Please enter the blue color value in the same format: "))
                    fuzz = float(input("Please enter the fuzziness of the reflection in the same format: "))
                    if r > 0 and r < 1 and g > 0 and g < 1 and b > 0 and b < 1 and fuzz > 0 and fuzz < 1:
                        albedo = Vector3(r,g,b)
                        break
                except:
                    pass
            return Metal(albedo, fuzz)
        elif mattype == "Diffuse Light" or mattype == "diffuse light":
            return DiffuseLight(TextureSelector(True))
        elif mattype == "Dielectric" or mattype == "dielectric":
            while True:
                try:
                    return Dielectric(float(input("Enter the refraction index of the material: ")))
                except:
                    pass
def SelectTransform(obj: hittable) -> hittable:
    while True:
        transformtype = input("Please enter a type of transformation to perform:\nTranslation\n")
        if transformtype == "Translation" or transformtype == "translation":
            while True:
                try:
                    x = float(input("Enter the x offset: "))
                    y = float(input("Enter the y offset: "))
                    z = float(input("Enter the z offset: "))
                    offset = Vector3(x,y,z)
                    return Translate(obj, offset)
                except:
                    pass
        else:
            print("Command not recognized")
RenderCornellBoxes("cornellrender.ppm")
RenderCornellBoxesTranslate("cornellrendertranslated.ppm")
RenderCornellEmpty("cornellempty.ppm")
RenderDielectric("dielectric.ppm")
RenderEarth("earth.ppm")
RenderLambertianCheckered("lambertiancheckered.ppm")
RenderPerlin("perlinspheres.ppm")
RenderMetals("metals.ppm")
RenderMovingSpheres("movespheres.ppm")