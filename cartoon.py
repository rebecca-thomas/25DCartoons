import sys
import pysvg.parser
from pysvg.shape import *
from pysvg.builders import *
from geometry import *

def readSVG(fname):
    return pysvg.parser.parse(fname)

def writeSVG(fname, svg):
    svg.save(fname)

def getSubElems(elem):
    strokes = {}
    subs(elem, strokes)
    return strokes
    
def subs(elem, dict):
    if isinstance(elem, BaseElement) and elem.getAttribute('id') != None:
        dict[elem.getAttribute('id')] = elem
    for sub in elem._subElements:
        if isinstance(sub, BaseElement):
            subs(sub, dict)
   
def readInput(filename):
    f = open(filename, 'r')
    numViews = int(f.readline())
    keyViews = []
    cameraPos = []
    for i in range(0, numViews):
        keyViews.append(readSVG(f.readline()[:-1]))
        cameraPos.append(Point(float(f.readline()), 
                          float(f.readline()), 
                          float(f.readline())))
    return numViews, keyViews, cameraPos

def calcRays(keyViews, cameraPos, stroke):
    pos = Point(100, 120, 0)
    rays = []
    for i in range(len(keyViews)):
        rays.append(Ray(pos, Vector(pos, cameraPos[i])))
    return rays
    
def calcAnchorPos(keyViews, cameraPos, stroke):
    rays = calcRays(keyViews, cameraPos, stroke)
    anchorPos = Point(0, 0, 0)
    for i in range(0, 10):
        tempPos = Point(0, 0, 0)
        for r in rays:
            tempVec = Vector(r.pos, anchorPos)
            tempPos += r * (tempVec.dot(r.dir) / r.dir.dot(r.dir))
        anchorPos = tempPos/3
    return anchorPos
    
if __name__ == '__main__':
    inputFile = sys.argv[1]
    numKeyViews, keyViews, cameraPos = readInput(inputFile)

    keyDicts = []

    outputFile = sys.argv[2]
    
    for svg in keyViews:
        dict = getSubElems(svg)
        print dict
        keyDicts.append(dict)
        
    print keyDicts[1][u'leftEye'].getTopRight()

    print keyViews
    print cameraPos

    svg = keyViews[0]
    
    strokes = []
    for stroke in keyDicts[0].keys():
        strokes.append(stroke)
  
    anchorPos = []
    for stroke in strokes:
        anchorPos.append(calcAnchorPos(keyDicts, cameraPos, stroke))

    print anchorPos
    writeSVG(outputFile, svg)
