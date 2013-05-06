import sys
import pysvg.parser
from pysvg.shape import *
from pysvg.builders import *
from pysvg.shape import *
from pysvg.script import *
from pysvg.structure import *
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
    
def combineD(dList, weight):
    numViews = len(dList)
    newD = []
    while True:
        temp = []    
        for i in range(0, numViews):
            if dList[i] != [] and dList[i] != ['']:
                temp.append(dList[i][0])
                dList[i] = dList[i][1:]

#        print temp
        if temp == []:
            return " ".join(newD)
        
        if allEqual(temp):
            newD.append(temp[0])
        else:
            sum = 0
            for j in range(0, len(temp)):
                sum += weight[j] * float(temp[j])
            newD.append(str(sum/numViews))
    
def allEqual(items):
    return all(x == items[0] for x in items)

def getWeighting(cameraPos, viewPos):
    weights = []
    # distance between two cameras in x
    # distance between view and cameraPos
    origin = Point(0, 0, 0)
    cameraRay = Vector(origin, viewPos)
    for view in cameraPos: 
        viewRay = Vector(origin, view)
        weights.append(max(0, viewRay.dot(cameraRay)))

    maxVal = max(weights)
    maxVal = max(1, maxVal)
#    print maxVal
    for i in range(0, len(weights)):
        weights[i] = weights[i] / maxVal
    
    return weights

if __name__ == '__main__':
    inputFile = sys.argv[1]
    numKeyViews, keyViews, cameraPos = readInput(inputFile)

    keyDicts = []

    outputFile = sys.argv[2]
    viewTempPos = map(float, sys.argv[3].split("_"))
    viewPos = Point(viewTempPos[0], viewTempPos[1], viewTempPos[2])
    
    weights = getWeighting(cameraPos, viewPos)
    print weights
    
    for svg in keyViews:
        dict = getSubElems(svg)
        print dict
        keyDicts.append(dict)
        
#    print keyDicts[1][u'leftEye'].getTopRight()

 #   print keyViews
#    print cameraPos

    svg = keyViews[0]
    svg._subElements = []
    
    strokes = []
    for stroke in keyDicts[0].keys():
        strokes.append(stroke)
  
    anchorPos = []
    for stroke in strokes:
        anchorPos.append(calcAnchorPos(keyDicts, cameraPos, stroke))

#    print anchorPos

    newSvg = pysvg.parser.svg()
    for stroke in strokes:
        dList = []
        if isinstance(keyDicts[0][stroke], path):
            for keyDict in keyDicts:
                if keyDict[stroke].get_d() != None:
                    dList.append(str(keyDict[stroke].get_d()).split(' '))
            newD = combineD(dList, weights)
#            print newD
            keyDict[stroke].set_d(newD)
            svg.addElement(keyDict[stroke])
    writeSVG(outputFile, svg)
