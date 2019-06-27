#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 
class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float)
    
    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Camera(object):
    def __init__(self, viewPoint, viewDir, viewUp,
                 viewProjNormal, projDistance, viewWidth, viewHeight, imgSize):
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.viewUp = viewUp
        self.viewProjNormal = viewProjNormal
        self.projDistance = projDistance
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight
        self.imgSize = imgSize
    
    # set the uvw
        vP = self.viewPoint
        vD = self.viewDir
        vD = vD/np.sqrt(vD @ vD)  #nomalized Dir vector
        a = self.viewUp
        a = a/np.sqrt(a @ a) # nomalized a(upvector)
        u = np.cross(vD, a)
        u = u/np.sqrt(u@u)
        v = np.cross(vD, u)
        #v = v/np.sqrt(v@v)
        w = np.cross(v,u) # -vD
        #w = w/np.sqrt(w@w)
        self.u = u
        self.v = v
        self.w = w
    
    #return nomalized viewing ray of (i,j) pixel
    def getRay(self,i,j):
        vP = self.viewPoint
        u = self.u
        v = self.v
        w = self.w
    
        width = self.viewWidth
        heigth = self.viewHeight
        xSize = self.imgSize[0]
        ySize = self.imgSize[1]
        center_view = vP - (self.projDistance) * w # center of view plane
        point_plane = center_view - (0.5) * width * u - (0.5) * heigth * v + (width /xSize * (i+0.5)) * u + (heigth/ySize * (j+0.5)) * v
        viewingRay = point_plane - vP
        viewingRay = viewingRay/np.sqrt(viewingRay @ viewingRay)
        return viewingRay
    def getPos(self,ray,t):
        pos = self.viewPoint + t * ray
        return pos

class Shader(object):
    def __init__(self, name, diffuseColor, specularColor, exponent, type):
        self.name = name
        self.diffuseColor = diffuseColor
        self.specularColor = specularColor
        self.exponent = exponent
        self.type = type


class Surface(object):
    def __init__(self,shader):
        self.shader = shader
    # ray = viewingray, point = point on box intersecting with ray,
    # normal = normal vector on point, light = light Class instance
    def diffuse(self, ray, point, normal, light):
        light_ray = light.position - point
        light_ray = light_ray / np.sqrt(light_ray @ light_ray)
        exceptKd = light.intensity * max(0, normal @ light_ray)
        return exceptKd
    
    def phong(self, ray, point, normal, light, exponent):
        light_ray = light.position - point
        light_ray = light_ray / np.sqrt(light_ray @ light_ray)
        # viewing ray와 반대 방향(v = -ray)
        h = light_ray - ray
        h = h / np.sqrt(h @ h)
        cosApowP = normal @ h
        cosApowP = pow(cosApowP, exponent)
        return light.intensity * max(0, cosApowP)

class Box(Surface) :
    def __init__(self, minPt, maxPt, shader):
        self.minPt = minPt
        self.maxPt = maxPt
        self.shader = shader
    def intersect(self, ray, tMin, tBest, viewPoint):
        d = ray
        (minPx, minPy, minPz) = (self.minPt[0], self.minPt[1], self.minPt[2])
        (maxPx, maxPy, maxPz) = (self.maxPt[0], self.maxPt[1], self.maxPt[2])
        tXmin = (minPx - viewPoint[0])/ray[0]
        tXmax = (maxPx - viewPoint[0])/ray[0]
        tYmin = (minPy - viewPoint[1])/ray[1]
        tYmax = (maxPy - viewPoint[1])/ray[1]
        tZmin = (minPz - viewPoint[2])/ray[2]
        tZmax = (maxPz - viewPoint[2])/ray[2]
        tInterMin = None
        tInterMax = None
        
        if tXmin <= 0 :
            tXmin = .000001
        if tXmax <= 0 :
            tXmax = .000001
        if tYmin <= 0 :
            tYmin = .000001
        if tYmax <= 0 :
            tYmax = .000001
        if tZmin <= 0 :
            tZmin = .000001
        if tZmax <= 0 :
            tZmax = .000001
        if ( (tXmin + tXmax == 0) or (tYmin + tYmax == 0) or (tZmin + tZmax == 0 ) ):
            return (None, None)
        
        if ( tXmax < tXmin ):
            temp = tXmax
            tXmax = tXmin
            tXmin = temp
        if ( tYmax < tYmin ):
            temp = tYmax
            tYmax = tYmin
            tYmin = temp
        if ( tZmax < tZmin ):
            temp = tZmax
            tZmax = tZmin
            tZmin = temp
        if (tXmin >= tMin and tYmin >= tMin and tZmin >= tMin):
            tInterMin = max(tXmin, tYmin, tZmin)
        else :
            #print (tMin, tXmin, tYmin, tZmin)
            return (None, None)
        if (tXmax >= tMin and tYmax >= tMin and tZmax >= tMin):
            tInterMax = min(tXmax, tYmax, tZmax)
        else:
            return (None, None)
#print (tMin, tXmax, tYmax, tZmax)
        if ( tInterMax > tInterMin and tInterMin < tBest):
            return (self,tInterMin)
        else :
            return (None, None)
    
    def normal(self,point, ray):
        x, y, z = point[0], point[1], point[2]
        (minPx, minPy, minPz) = (self.minPt[0], self.minPt[1], self.minPt[2])
        (maxPx, maxPy, maxPz) = (self.maxPt[0], self.maxPt[1], self.maxPt[2])
        normal = None
        dXmin, dXmax = abs(x - minPx), abs(x - maxPx)
        dYmin, dYmax = abs(y - minPy), abs(y - maxPy)
        dZmin, dZmax = abs(z - minPz), abs(z - maxPz)
        axis = min(dXmin, dXmax, dYmin, dYmax, dZmin, dZmax)
        
        if (axis == dXmin or axis == dXmax):
            if ray[0] < 0:
                normal = np.array([1,0,0])
            else:
                normal = np.array([-1,0,0])
        if (axis == dYmin or axis == dYmax):
            if ray[1] < 0:
                normal = np.array([0, 1, 0])
            else:
                normal = np.array([0, -1, 0])
        if (axis == dZmin or axis == dZmax):
            if ray[2] < 0:
                normal = np.array([0, 0, 1])
            else:
                normal = np.array([0, 0, -1])
        return normal

class Sphere(Surface):
    def __init__(self, center, radius, shader):
        self.center = center
        self.radius = radius
        self.shader = shader
    # 구의 point가 viewing ray와 만날 때, 구(Surface)와 작은
    def intersect(self, ray, tMin, tBest, viewPoint):
        d = ray
        p = viewPoint - self.center
        Det = pow( (d@p) ,2) - (p@p) + pow(self.radius,2)
        if Det >= 0:
            tA = - (d @ p) - np.sqrt(Det)
            tB = - (d @ p) + np.sqrt(Det)
            if (tA >= tMin) and (tA < tBest):
                return (self, tA)
            elif (tB >= tMin) and (tB < tBest):
                return (self, tB)
            else :
                return (None, None)
        else:
            return (None, None)
    
    def normal(self,point,ray):
        normal = point - self.center
        normal = normal/np.sqrt(normal@normal)
        return normal

class Light(object):
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

def main():

    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    
    # set default values
    viewPoint = [5,5,5]
    viewDir=np.array([0,0,-1]).astype(np.float)
    viewUp=np.array([0,1,0]).astype(np.float)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    projDistance=1.0
    viewWidth=1.0
    viewHeight=1.0
    lightPos = [10,10,10]
    diffuseColor_c = np.array([1.,1.,1.])
    specularColor_c = np.array([0.,0.,0.])
    exponent_c = .0
    intensity=np.array([1,1,1]).astype(np.float)  # how bright the light is.
    print(np.cross(viewDir, viewUp))

    #Surface 리스트, Light리스트, Shader리스트, Image사이즈(배열), Camera 인스턴스
    surfaceList : [Surface] = []
    lightList : [Light] = []
    shaderList : [Shader] = []
    imgSize=np.array(root.findtext('image').split()).astype(np.int)
    camera = Camera(viewPoint, viewDir, viewUp, viewProjNormal,
                    projDistance, viewWidth, viewHeight, imgSize)

    #camera의 파라미터 입력
    for c in root.findall('camera'):
        viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float)
        viewDir=np.array(c.findtext('viewDir').split()).astype(np.float)
        viewUp=np.array(c.findtext('viewUp').split()).astype(np.float)
        viewProjNormal=-1*viewDir
        if ( c.findtext('projDistance') != None):
            projDistance = (np.float)(c.findtext('projDistance'))
        viewWidth=(np.float)(c.findtext('viewWidth'))
        viewHeight=(np.float)(c.findtext('viewHeight'))
        camera = Camera(viewPoint, viewDir, viewUp,
                        viewProjNormal, projDistance, viewWidth, viewHeight, imgSize)
        print('viewpoint', viewPoint)
    
    #light의 파라미터 입력
    for c in root.findall('light'):
        lightPos=np.array(c.findtext('position').split()).astype(np.float)
        intensity=np.array(c.findtext('intensity').split()).astype(np.float)
        lightList.append(Light(lightPos,intensity))


    #shader의 파라미터 입력
    for c in root.findall('shader'):
        type_c = c.get('type')
        diffuseColor_c=np.array(c.findtext('diffuseColor').split()).astype(np.float)
        if (type_c == 'Phong'):
            specularColor_c=np.array(c.findtext('specularColor').split()).astype(np.float)
            exponent_c=(np.float)(c.findtext('exponent'))
        shaderList.append(Shader(c.get('name'), diffuseColor_c, specularColor_c, exponent_c, type_c))
        print('name', c.get('name'))
        print('diffuseColor', diffuseColor_c)

    #surface 파라미터 입력, surfaceList에 추가
    for c in root.findall('surface'):
        typ = c.get('type')
        shader = ''
        for d in c.findall('shader'):
            shader = d.get('ref')
        if typ == 'Sphere':
            center = np.array(c.findtext('center').split()).astype(np.float)
            radius = np.array(c.findtext('radius').split()).astype(np.float)
            surfaceList.append(Sphere(center, radius, shader))
        elif typ == 'Box':
            minPt = np.array(c.findtext('minPt').split()).astype(np.float)
            maxPt = np.array(c.findtext('maxPt').split()).astype(np.float)
            surfaceList.append(Box(minPt, maxPt, shader))

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!
    white = Color(1,1,1)
    for iy in np.arange(imgSize[1]):
        for ix in np.arange(imgSize[0]):
            tBest = float("inf")
            firstSurface = None
            ray = camera.getRay(ix, iy)
            for s in surfaceList:
                hitSurface, t = s.intersect(ray, 0, tBest, camera.viewPoint)
                if hitSurface != None:
                    tBest = t
                    firstSurface = hitSurface
            if firstSurface != None :
                point = camera.getPos(ray, tBest)
                normal = firstSurface.normal(point,ray)
                for s in shaderList:
                    if s.name == firstSurface.shader:
                        color_xy = np.array([.0 ,.0 ,.0])
                        for light in lightList:
                            shadSurface = None
                            isBlocked = False
                            shadRay = light.position - point
                            distance = np.sqrt(shadRay @ shadRay)
                            shadRay = shadRay/distance
                            #rPow2 = pow(distance,2)
                            Cons = 1.8
                            TMin = 0.00000001
                            for surfaceAll in surfaceList:
                                shadSurface, T = surfaceAll.intersect(shadRay, TMin, np.inf, point)
                                if(shadSurface != None):
                                    isBlocked = True
                            if isBlocked == False:
                                if s.type == 'Phong'  :
                                    color_xy += s.specularColor * firstSurface.phong(ray, point, normal, light, s.exponent) * 1
                                color_xy += s.diffuseColor * firstSurface.diffuse(ray,point, normal, light)
                        imgcolor = Color(color_xy[0],color_xy[1],color_xy[2])
                        imgcolor.gammaCorrect(2.3)
                        img[iy][ix] += imgcolor.toUINT8()
                        #img[iy][ix] = Color(s.diffuseColor[0],s.diffuseColor[1],
                        #s.diffuseColor[2]).toUINT8()
    print(len(surfaceList))
    #print (camera. viewPoint, camera.viewWidth, camera.viewHeight)
    #for x in np.arange(imgSize[0]):
        #img[5][x]=[255,255,255]

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')

if __name__=="__main__":
    main()   
