# P2.0 Final project
# REDACTED(I <3 not doxing myself)
# Basic raytracing algorithm
from camera import Camera
from rtutils import *
from material import Dielectric, Lambertian, Metal, DiffuseLight, Material
from texture import SolidColor, CheckerTexture, ImageTexture, Texture, NoiseTexture
from Quadrilateral import Quad, Triangle, Ellipse, Annulus
from sphere import Sphere
from hittable import *
from multiprocessing import *
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
    rtworld.add(Quad.Box(Vector3(130,0,65), Vector3(295, 165, 230), white))
    rtworld.add(Quad.Box(Vector3(265, 0, 295), Vector3(430, 330, 460), white))
    camera = Camera(1,600, 200, 50, 40, Vector3(278,278, -800), Vector3(278, 278, 0), Vector3(0,1,0), 0, 10, Vector3(0,0,0), filePath)
    camera.Render(rtworld)
def RenderCornellBoxesTransforms(filePath: str):
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
    rtworld.add(Rotate(15, Translate(Quad.Box(Vector3(130,0,65), Vector3(295, 165, 230), white), Vector3(0, 0, 100))))
    rtworld.add(Rotate(-18, Translate(Quad.Box(Vector3(265, 0, 295), Vector3(430, 330, 460), white), Vector3(0,0,100))))
    camera = Camera(1,600, 100, 50, 40, Vector3(278,278, -800), Vector3(278, 278, 0), Vector3(0,1,0), 0, 10, Vector3(0,0,0), filePath)
    camera.Render(rtworld)
def RenderEarth(filePath: str):
    rtworld = hittableList(True)
    earthtex = ImageTexture("imagetex.jpeg")
    earthsurface = Lambertian(earthtex)
    rtworld.add(Sphere.CreateSphere(2, Vector3(0,0,0), earthsurface))
    camera = Camera(16/9, 400, 100, 50, 20, Vector3(0,0,12), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderPerlin(filePath: str):
    rtworld = hittableList(True)
    pertext = NoiseTexture(4)
    rtworld.add(Sphere.CreateSphere(1000, Vector3(0, -1000, 0), Lambertian(pertext)))
    rtworld.add(Sphere.CreateSphere(2, Vector3(0,2,0), Lambertian(pertext)))
    camera = Camera(16/9, 400, 100, 50, 20, Vector3(13,2,3), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderDielectric(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matcenter = Lambertian(SolidColor(Vector3(0.1, 0.2, 0.5)))
    matleft = Dielectric(1.5)
    matbubble = Dielectric(1/1.5)
    matright = Metal(Vector3(0.8, 0.6, 0.2), 0)
    rtworld.add(Sphere.CreateSphere(100, Vector3(0, -100.5, -1), matground))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(0,0,-1.2), matcenter))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(-1,0,-1), matleft))
    rtworld.add(Sphere.CreateSphere(0.4, Vector3(-1,0,-1), matbubble))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(1.0, 0, -1), matright))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderMetals(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matcenter = Lambertian(SolidColor(Vector3(0.1, 0.2, 0.5)))
    matleft = Metal(Vector3(0.8, 0.8, 0.8), 0.3)
    matright = Metal(Vector3(0.8, 0.6, 0.2), 1.0)
    rtworld.add(Sphere.CreateSphere(100.0, Vector3(0.0, -100.5, -1.0), matground))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(0, 0, -1.2), matcenter))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(-1, 0, -1), matleft))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(1, 0, -1), matright))
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
                    rtworld.add(Sphere.CreateSphere(0.2, center, spheremat))
                elif choosemat < 0.95:
                    albedo = Vector3.RandomVectorRange(0.5, 1)
                    fuzz = RandomFloatRange(0, 0.5)
                    spheremat = Metal(albedo, fuzz)
                    rtworld.add(Sphere.CreateSphere(0.2, center, spheremat))
                else:
                    spheremat = Dielectric(1.5)
                    world.add(Sphere.CreateSphere(0.2, center, spheremat))
    mat1 = Dielectric(1.5)
    rtworld.add(Sphere.CreateSphere(1.0, Vector3(0,1,0), mat1))
    mat2 = Lambertian(SolidColor(Vector3(0.4, 0.2, 0.1)))
    rtworld.add(Sphere.CreateSphere(1.0, Vector3(-4, 1, 0), mat2))
    mat3 = Metal(Vector3(0.7, 0.6, 0.5), 0.0)
    rtworld.add(Sphere.CreateSphere(1.0, Vector3(4,1,0), mat3))
    camera = Camera(16/9, 1200, 250, 50, 20, Vector3(13,2,3), Vector3(0,0,0), Vector3(0,1,0), 0.6, 10.0, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderLambertianCheckered(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matright = Lambertian(SolidColor(Vector3(0.1, 0.1, 0.8)))
    matleft = Lambertian(SolidColor(Vector3(0.9, 0.2, 0.1)))
    matcenter = Lambertian(CheckerTexture(0.5, SolidColor(Vector3(0.1, 0.9, 0.1)), SolidColor(Vector3(0.1, 0.1, 0.9))))
    rtworld.add(Sphere.CreateSphere(100.0, Vector3(0.0, -100.5, -1.0), matground))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(0, 0, -1.2), matcenter))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(-1, 0, -1), matleft))
    rtworld.add(Sphere.CreateSphere(0.5, Vector3(1, 0, -1), matright))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderMovingSpheres(filePath: str):
    rtworld = hittableList(True)
    matground = Lambertian(SolidColor(Vector3(0.8, 0.8, 0)))
    matleft = Lambertian(SolidColor(Vector3(0.9, 0.2, 0.1)))
    rtworld.add(Sphere.CreateSphere(100.0, Vector3(0.0, -100.5, -1.0), matground))
    rtworld.add(Sphere.CreateMovingSphere(0.5, Vector3(-1, 0, -1), Vector3(1,0,-1), matleft))
    camera = Camera(16/9, 400, 100, 50, 90, Vector3(0,0,0), Vector3(0,0,-1), Vector3(0,1,0), 0, 10, Vector3(0.8, 0.8,1), filePath)
    camera.Render(rtworld)
def RenderTriangle(filePath: str):
    rtworld = hittableList(True)
    objMat = Lambertian(SolidColor(Vector3(0.75, 0, 0.5)))
    rtworld.add(Triangle(Vector3(-2, -1, 0), Vector3(4,0,0), Vector3(0,2,0), objMat))
    camera = Camera(1, 400, 4, 4, 20, Vector3(0,0,12), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.9, 0.9, 0.9), filePath)
    camera.Render(rtworld)
def RenderEllipse(filePath: str):
    rtworld = hittableList(True)
    objMat = Lambertian(SolidColor(Vector3(0.75, 0, 0.5)))
    rtworld.add(Ellipse(Vector3(0,0,0), Vector3(-2,0,0), Vector3(0,1,0), objMat))
    camera = Camera(1, 400, 4, 4, 20, Vector3(0,0,12), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.9, 0.9, 0.9), filePath)
    camera.Render(rtworld)
def RenderAnnulus(filePath: str):
    rtworld = hittableList(True)
    objMat = Lambertian(SolidColor(Vector3(0.75, 0, 0.5)))
    rtworld.add(Annulus(Vector3(0,0,0), Vector3(-2,0,0), Vector3(0,1,0), 0.6, objMat))
    camera = Camera(1, 400, 4, 4, 20, Vector3(0,0,12), Vector3(0,0,0), Vector3(0,1,0), 0, 10, Vector3(0.9, 0.9, 0.9), filePath)
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
if __name__ == "__main__":
    while True:
        cmdinput = input("Please enter a command:\nadd - add a shape to the scene\nexit - exit the program\nrender - render the scene\npredefined - render a predefined scene\n")
        if cmdinput == "help":
            print("add - add a shape to the scene\nexit - exit the program\nrender - render the scene\npredefined - render a predefined scene\n")
        elif cmdinput == "add":
            shapetype = input("Please enter one of the following shapes to add to the scene:\nQuad - 2D Quadrilateral shape\n Sphere\nBox\n")
            if shapetype == "Sphere" or shapetype == "sphere":
                while True:
                    try:
                        radius = float(input("Please enter the radius of the sphere: "))
                        center = Vector3(float(input("Please enter the x coordinate of the sphere's center: ")), float(input("Please enter the y coordinate of the sphere's center: ")), float(input("Please enter the z coordinate of the sphere's center: ")))
                    except:
                        pass
                    else:
                        sphere = Sphere.CreateSphere(radius, center, SelectMaterial())
                        break
                inspheremenu = True
                while inspheremenu:
                    spherecmd = input("Please enter a valid entity altering command to modify the sphere, or type done to add it to the scene:\ndone - add the sphere to the scene\ntransform - transform the shape of the sphere and add it to the scene\nmove - add a motion blur effect to the sphere as if it was moving to a location\n")
                    if spherecmd == "done":
                        world.add(sphere)
                        inspheremenu = False
                    elif spherecmd == "transform":
                        world.add(SelectTransform(sphere))
                    elif spherecmd == "move":
                        inmenuspheremove = True
                        while inmenuspheremove:
                            try:
                                endcenter = Vector3(float(input("Please enter the x coordinate of where the sphere will stop moving: ")), float(input("Please enter the y coordinate of where the sphere will stop moving: ")), float(input("Please enter the z coordinate of where the sphere will stop moving: ")))
                            except:
                                pass
                            else:
                                inmenuspheremove = False
                    sphere = Sphere.CreateSphere(sphere.radius, sphere.center, sphere.mat, True, endcenter)
                else:
                    print("Command not recognized")
            elif shapetype == "quad" or shapetype == "Quad":
                inquadmenu = True
                while inquadmenu:
                    try:
                        qx = float(input("Please enter the x coordinate of the bottom left corner: "))
                        qy = float(input("Please enter the y coordinate of the bottom left corner: "))
                        qz = float(input("Please enter the z coordinate of the bottom left corner: "))
                        ux = float(input("Please enter the x coordinate change of the side going up from the bottom left corner: "))
                        uy = float(input("Please enter the y coordinate change of the side going up from the bottom left corner: "))
                        uz = float(input("Please enter the z coordinate change of the side going up from the bottom left corner: "))
                        vx = float(input("Please enter the x coordinate change of the side going right from the bottom left corner: "))
                        vy = float(input("Please enter the y coordinate change of the side going right from the bottom left corner: "))
                        vz = float(input("Please enter the z coordinate change of the side going right from the bottom left corner: "))
                    except:
                        pass
                    else:
                        break
                quad = Quad(Vector3(qx,qy,qz), Vector3(ux, uy, uz), Vector3(vx, vy, vz), SelectMaterial())
                quadcmd = input("Please enter a valid entity altering command to modify the quad, or type done to add it to the scene:\ndone - add the quad to the scene\ntransform - transform the shape of the quad and add it to the scene\n")
                if quadcmd == "done" or quadcmd == "Done":
                    world.add(quad)
                    inquadmenu = False
                elif quadcmd == "transform" or quadcmd == "Transform":
                    world.add(SelectTransform(quad))
                else:
                    print("Command not recognized")
            elif shapetype == "box" or shapetype == "Box":
                inboxmenu = True
                while inboxmenu:
                    try:
                        c1x = float(input("Please enter the x coordinate of the bottom left corner of the box: "))
                        c1y = float(input("Please enter the y coordinate of the bottom left corner of the box: "))
                        c1z = float(input("Please enter the z coordinate of the bottom left corner of the box: "))
                        c2x = float(input("Please enter the x coordinate of the top right corner of the box: "))
                        c2y = float(input("Please enter the y coordinate of the top right corner of the box: "))
                        c2z = float(input("Please enter the z coordinate of the top right corner of the box: "))
                    except:
                        pass
                    else:
                        break
                box = Quad.Box(Vector3(c1x, c1y, c1z), Vector3(c2x, c2y, c2z), SelectMaterial())
                boxcmd = input("Please enter a valid entity altering command to modify the box, or type done to add it to the scene:\ndone - add the box to the scene\ntransform - transform the shape of the box and add it to the scene\n")
                if boxcmd == "done" or boxcmd == "Done":
                    world.add(box)
                    inboxmenu = False
                elif boxcmd == "transform" or boxcmd == "Transform":
                    world.add(SelectTransform(box))
                else:
                    print("Command not recognized")
            else:
                print("Shape type not recognized")
        elif cmdinput == "render" or cmdinput == "Render":
            while True:
                try:
                    aspectRatio = float(input("Please enter the aspect ratio(ex: 16/9 = 1.7778): "))
                    imgWidth = int(input("Please enter the width of the image: "))
                    samplesPerPixel = int(input("Please enter the number of samples per pixel: "))
                    maxrayrecursion = int(input("Please enter the max number of recurring rays(reflections of reflections): "))
                    fov = int(input("Please enter the field of view angle of the camera: "))
                    camposx = float(input("Please enter the x coordinate location of the camera: "))
                    camposy = float(input("Please enter the y coordinate location of the camera: "))
                    camposz = float(input("Please enter the z coordinate location of the camera: "))
                    camerapos = Vector3(camposx, camposy, camposz)
                    camlookx = float(input("Please enter the x coordinate of where the camera is looking: "))
                    camlooky = float(input("Please enter the y coordinate of where the camera is looking: "))
                    camlookz = float(input("Please enter the z coordinate of where the camera is looking: "))
                    cameralookpoint = Vector3(camlookx, camlooky, camlookz)
                    camupx = float(input("Please enter the x coordinate of the camera's up vector(normally 0): "))
                    camupy = float(input("Please enter the y coordinate of the camera's up vector(normally 1): "))
                    camupz = float(input("Please enter the z coordinate of the camera's up vector(normally 0): "))
                    cameraup = Vector3(camupx, camupy, camupz)
                    defocusAngle = float(input("Please enter the defocusing angle of the camera: "))
                    focusDist = float(input("Please enter the focusing distance of the camera(also known as depth of field): "))
                    bgr = float(input("Please enter the red value of the background color as a percentage(ex: 0.59): "))
                    bgg = float(input("Please enter the green value of the background color as a percentage(ex: 0.19): "))
                    bgb = float(input("Please enter the blue value of the background color as a percentage(ex: 0.99): "))
                    if bgr < 0 or bgr > 1 or bgg < 0 or bgg > 1 or bgb < 0 or bgb > 1:
                        raise ValueError
                    bgcolor = Vector3(bgr, bgg, bgb)
                    outputFile = input("Please enter the path of the file to output the result to: ")
                except:
                    pass
                else:
                    break
            camera = Camera(aspectRatio, imgWidth, samplesPerPixel, maxrayrecursion, fov, camerapos, cameralookpoint, cameraup, defocusAngle, focusDist, bgcolor, outputFile)
            camera.Render(world)
        elif cmdinput == "predefined" or cmdinput == "Predefined":
            predefinedtype = input("Please choose from the list of predefined scenes to render:\nEmpty Cornell Box\nEarth\nPerlin Sphere\nMetals\nRTOneWeekend Final\nDielectrics\nBoxes in Cornell Box\nBoxes in Cornell Box Transformed\nLambertian Checkered Spheres\nMoving Spheres\nTriangle\nEllipse\nAnnulus\n")
            if predefinedtype == "empty cornell box" or predefinedtype == "Empty Cornell box" or predefinedtype == "Empty Cornell Box":
                filePath = input("Please enter the location to output the cornell box render to: ")
                RenderCornellEmpty(filePath)
                break
            elif predefinedtype == "Boxes in Cornell Box" or predefinedtype == "boxes in cornell box":
                filePath = input("Please enter the location to output the boxes in cornell box render to: ")
                RenderCornellBoxes(filePath)
                break
            elif predefinedtype == "Earth":
                filePath = input("Please enter the location to output the earth render to: ")
                RenderEarth(filePath)
                break
            elif predefinedtype == "Perlin Sphere" or predefinedtype == "perlin sphere" or predefinedtype == "Perlin sphere":
                filePath = input("Please enter the location to output the perlin sphere render to: ")
                RenderPerlin(filePath)
                break
            elif predefinedtype == "Moving Spheres" or predefinedtype == "Moving spheres" or predefinedtype == "moving spheres":
                filePath = input("Please enter the location to output the render to: ")
                RenderMovingSpheres(filePath)
                break
            elif predefinedtype == "Metals" or predefinedtype == "metals":
                filePath = input("Please enter the location to output the metals render to: ")
                RenderMetals(filePath)
                break
            elif predefinedtype == "Dielectrics" or predefinedtype == "dielectrics":
                filePath = input("Please enter the location to output the dielectrics render to: ")
                RenderDielectric(filePath)
                break
            elif predefinedtype == "RTOneWeekend Final" or predefinedtype == "RTOneWeekend final":
                filePath = input("Please enter the location to output the ray tracing in one weekend final render to: ")
                RenderRTOneWeekend(filePath)
                break
            elif predefinedtype == "Boxes in Cornell Box Transformed":
                filePath = input("Please enter the location to output the render to: ")
                RenderCornellBoxesTransforms(filePath)
                break
            elif predefinedtype == "Lambertian Checkered Spheres":
                filePath = input("Please enter the location to output the render to: ")
                RenderLambertianCheckered(filePath)
                break
            elif predefinedtype == "Triangle":
                filePath = input("Please enter the location to output the render to: ")
                RenderTriangle(filePath)
                break
            elif predefinedtype == "Ellipse":
                filePath = input("Please enter the location to output the render to: ")
                RenderEllipse(filePath)
                break
            elif predefinedtype == "Annulus":
                filePath = input("Please enter the location to output the render to: ")
                RenderAnnulus(filePath)
                break
            else:
                print("Predefined scene not found")
        elif cmdinput == "exit":
            break
        else:
            print("Command not recognized, please enter a valid command or type exit to exit the program")