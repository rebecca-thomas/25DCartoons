import copy
from string import upper, replace, letters
from pysvg.builders import *
from geometry import *
from cartoonHelpers import *

def changeView(oldView):
    """ shifts the viewBox to be centered aat 0,0"""
    if oldView._attributes.has_key('viewBox'):
        viewBox = oldView.get_viewBox().split(' ')
    else:
        viewBox = [0, 0, oldView.get_width(), oldView.get_height()]

    newViewBox = [float(viewBox[2]) * -.5, float(viewBox[3]) * -.5,
                  float(viewBox[2]) * 1, float(viewBox[3]) * 1]

    xOffset = float(newViewBox[0])
    yOffset = float(newViewBox[1])

    newViewBox = ' '.join(map(str, newViewBox))
    return newViewBox, xOffset, yOffset

def calcRays(keyViews, cameraPos, stroke):
    """ calculates the rays from the center of the stroke in all views
        to the camera"""
    rays = []
    for i in range(len(keyViews)):
        if keyViews[i]. has_key(stroke):
            if isinstance(keyViews[i][stroke], path):
                pos = calcStrokeCenter(keyViews[i][stroke].get_d(), cameraPos[i])
                rays.append(Ray(pos, Vector(pos, cameraPos[i])))
    return rays

def calcAnchorPos(keyViews, cameraPos, stroke):
    """ calculates the anchor position based on the rays in all views"""
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
    """ Combines the data for a path element. Assumes same order of 
        control commands."""
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
                if temp[j] in letters:
                    break
                sum += weight[j] * float(temp[j])
            newD.append(str(sum))

def getWeighting(cameraPos, viewPos):
    """ gets the weighting for each view to be used when interpolating"""
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
    """ gets the index of the max weight"""
    max = 0
    maxInd = 0
    for i in range(0, len(weights)):
        if weights[i] > max:
            max = weights[i]
            maxInd = i
    return maxInd

def reverseTransform(origView, xOffset, yOffset):
    """creates a transform matrix for the derived views"""
    reverseMatrix = TransformBuilder()
    xVal = 1
    yVal = 1
    val2 = 0
    val3 = 0
    if origView.x != 0:
        xVal = -1
    elif origView.y != 0:
        yVal = -1

    reverseMatrix.setMatrix(xVal, 0, 0, yVal, xOffset * xVal, yOffset * yVal)
    return reverseMatrix.getTransform()

def combineTransforms(matrix1, matrix2):
    """ combines to transformation matrices"""
    matrix1 = matrix1[7:-2]
    matrix1 = matrix1.split(' ')
    matrix2 = matrix2[7:-2]
    matrix2 = matrix2.split(' ')
    matrix3 = [0,0,0,0,0,0]
    xNeg = 1
    yNeg = 1
    if float(matrix1[0]) == -1 or float(matrix2[0]) == -1:
        xNeg = -1
    if float(matrix1[3]) == -1 or float(matrix2[3]) == -1:
        yNeg = -1
        xNeg = 1
    matrix3[0] = float(matrix1[0]) * float(matrix2[0])
    matrix3[3] = float(matrix1[3]) * float(matrix2[3])
    matrix3[4] = xNeg * (float(matrix1[4])*float(matrix1[0]) + float(matrix2[4])*float(matrix2[0])) / 2
    matrix3[5] = yNeg * (float(matrix1[5])*float(matrix1[3]) + float(matrix2[5])*float(matrix2[3])) / 2
    
    newMatrix = TransformBuilder()
    newMatrix.setMatrix(matrix3[0], matrix3[1], matrix3[2], matrix3[3], matrix3[4], matrix3[5])
    return newMatrix.getTransform()

def getDerivedViews(keyViews, numKeyViews, cameraPos, xOffset, yOffset):
    """ creates the derived views for all key views"""
    offsetMatrix = TransformBuilder()
    offsetMatrix.setMatrix(1, 0, 0, 1, xOffset, yOffset)
    for i in range(0, numKeyViews):
        keyViews[i].set_transform(offsetMatrix.getTransform())
        keyViews.append(copy.deepcopy(keyViews[i]))
        keyViews[i + numKeyViews].set_transform(reverseTransform(cameraPos[i], xOffset, yOffset))
        cameraPos.append(cameraPos[i] * -1)
    numKeyViews *= 2
    return keyViews, numKeyViews, cameraPos

def createKeyDicts(keyViews):
    """ creates dictionaries for all views to access strokes by id"""
    keyDicts = []
    for svg in keyViews:
        dict = getSubElems(svg)
        keyDicts.append(dict)
    return keyDicts

def getStrokeNames(keyDicts):
    """gets the names of all strokes"""
    strokes = []
    for stroke in keyDicts[1].keys():
        allHave = True
        for dict in keyDicts:
            if not dict.has_key(stroke):
                allHave = False
        if allHave:
            strokes.append(stroke)
    return strokes

def getZOrdering(anchorPos, viewPos):
    """ gets the z-ordering based on the camera position"""
    zOrder = []
    origin = Point(0, 0, 0)
    toView = Vector(origin, viewPos)
    for stroke in anchorPos:
        toStroke = Vector(origin, stroke[0])
        zOrder.append((toStroke.dot(toView), stroke[1]))
    zOrder.sort()
    return zOrder

def calcStrokeCenter(data, cameraPos):
    """ calculates the center of a stroke"""
    minX = float('inf')
    minY = float('inf')
    maxX = 0 
    maxY = 0
    XorY = True
    data = replace(data, ',', ' ')
    d = data.split(" ")
    
    while d != [] and d != ['']:        
        if d[0] in ['A', 'M', 'Z', 'C', 'L']:
            d = d[1:]
        else:
            if XorY:
                if float(d[0]) < minX:
                    minX = float(d[0])
                elif float(d[0]) > maxX:
                    maxX = float(d[0])
            else:    
                if float(d[0]) < minY:
                    minY = float(d[0])
                elif float(d[0]) > maxY:
                    maxY = float(d[0])            
            d = d[1:]
            XorY = not XorY
    
    x = (maxX - minX) / 2
    y = (maxY - minY) / 2
    return transTo3D(cameraPos, x, y)
    
def transTo3D(cameraPos, x, y):
    """ translates a 2D coordinate into a point in 3D space"""
    dist = Vector(cameraPos, Point(0,0,0)).length()
    towards = Vector(cameraPos, Point(0, 0, 0))
    right = towards.cross(Vector(cameraPos, Point(1, 0, 0)))
    up = towards.cross(Vector(cameraPos, Point(0, 1, 0)))

    vecToPoint = cameraPos + towards.norm() * dist + right.norm() * x + up.norm() * y
    return vecToPoint

