from geometry import *
from cartoonHelpers import *

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
    # distance between two cameras in x
    # distance between view and cameraPos
    origin = Point(0, 0, 0)
    cameraRay = Vector(origin, viewPos)
    viewDepths = []
    for view in cameraPos:
        viewRay = Vector(origin, view)
        weights.append(max(0, viewRay.dot(cameraRay)))
        viewDepths.append(max(abs(view.x), abs(view.y), abs(view.z)))
    maxVal = sum(weights)
    maxVal = max(1, maxVal)
    print viewDepths
    print maxVal
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
