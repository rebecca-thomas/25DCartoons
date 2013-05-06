import copy
from pysvg.builders import *
from geometry import *
from cartoonHelpers import *

def changeView(oldView):
    viewBox = oldView.get_viewBox().split(' ')
    newViewBox = [float(viewBox[2]) * -.5, float(viewBox[3]) * -.5,
                  float(viewBox[2]) * 1, float(viewBox[3]) * 1]

    xOffset = float(newViewBox[0])
    yOffset = float(newViewBox[1])

    newViewBox = ' '.join(map(str, newViewBox))
    return newViewBox, xOffset, yOffset

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

        if temp == []:
            return " ".join(newD)

        if allEqual(temp):
            newD.append(temp[0])
        else:
            sum = 0
            for j in range(0, len(temp)):
                sum += weight[j] * float(temp[j])
            newD.append(str(sum))

def getWeighting(cameraPos, viewPos):
    weights = []
    origin = Point(0, 0, 0)
    cameraRay = Vector(origin, viewPos)
    viewDepths = []
    for view in cameraPos:
        viewRay = Vector(origin, view)
        weights.append(max(0, viewRay.dot(cameraRay)))
        viewDepths.append(max(abs(view.x), abs(view.y), abs(view.z)))
    
    maxVal = sum(weights)
    maxVal = max(1, maxVal)
    
    for i in range(0, len(weights)):
        weights[i] = weights[i] / maxVal

    return weights

def getViewNum(weights):
    max = 0
    maxInd = 0
    for i in range(0, len(weights)):
        if weights[i] > max:
            max = weights[i]
            maxInd = i
    return maxInd

def reverseTransform(origView, xOffset, yOffset):
    reverseMatrix = TransformBuilder()
    xVal = 1
    yVal = 1
    if origView.x != 0:
        xVal = -1
    if origView.y != 0:
        yVal = -1
    reverseMatrix.setMatrix(xVal, 0, 0, yVal, xOffset * xVal, yOffset * yVal)
    return reverseMatrix.getTransform()

def getDerivedViews(keyViews, numKeyViews, cameraPos, xOffset, yOffset):
    for i in range(0, numKeyViews):
        keyViews.append(copy.deepcopy(keyViews[i]))
        keyViews[i + numKeyViews].set_transform(reverseTransform(cameraPos[i], xOffset, yOffset))
        cameraPos.append(cameraPos[i] * -1)
    numKeyViews *= 2
    return keyViews, numKeyViews, cameraPos

def createKeyDicts(keyViews):
    keyDicts = []
    for svg in keyViews:
        dict = getSubElems(svg)
        keyDicts.append(dict)
    return keyDicts

def getStrokeNames(dict):
    strokes = []
    for stroke in dict.keys():
        strokes.append(stroke)
    return strokes

def getZOrdering(anchorPos, viewPos):
    zOrder = []
    origin = Point(0, 0, 0)
    toView = Vector(origin, viewPos)
    for stroke in anchorPos:
        toStroke = Vector(origin, stroke[0])
        zOrder.append((toStroke.dot(toView), stroke[1]))
    zOrder.sort()
    return zOrder
