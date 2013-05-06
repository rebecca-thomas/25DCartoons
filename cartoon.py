import sys
from geometry import *
from pysvg.builders import *
from cartoonParsing import *
from cartoonHelpers import *
from cartoonCalc import *

if __name__ == '__main__':
    keyDicts = []
    strokes = []
    anchorPos = []

    inputFile = sys.argv[1]    
    outputFile = sys.argv[2]
    viewTempPos = map(float, sys.argv[3].split("_"))
    viewPos = Point(viewTempPos[0], viewTempPos[1], viewTempPos[2])


    numKeyViews, keyViews, cameraPos = readInput(inputFile)

    newSvg = pysvg.parser.svg()
    
    newViewBox, xOffset, yOffset = changeView(keyViews[0])

    offsetMatrix = TransformBuilder()
    offsetMatrix.setMatrix(1, 0, 0, 1, xOffset, yOffset)

    newSvg.set_viewBox(newViewBox)

    keyViews, numKeyViews, cameraPos = getDerivedViews(keyViews, numKeyViews, 
                                                       cameraPos, xOffset, yOffset)
    
    
    weights = getWeighting(cameraPos, viewPos)
    viewNum = getViewNum(weights)
    
    keyDicts = createKeyDicts(keyViews)
    
    strokes = getStrokeNames(keyDicts[0])

    for stroke in strokes:
        anchorPos.append((calcAnchorPos(keyDicts, cameraPos, stroke), stroke))
    print anchorPos

    for stroke in strokes:
        dList = []
        if isinstance(keyDicts[0][stroke], path):
            count = 0
            for keyDict in keyDicts:
                if keyDict[stroke].get_d() != None:
                    dList.append(str(keyDict[stroke].get_d()).split(' '))

            newD = combineD(dList, weights)
            tempStroke = copy.deepcopy(keyDicts[viewNum][stroke])
            tempStroke.set_d(newD)
            tempStroke.set_transform(keyViews[viewNum].get_transform())
            newSvg.addElement(tempStroke)
    
#    newSvg = keyViews[3]
    newSvg.set_transform(offsetMatrix.getTransform())
    
    writeSVG(outputFile, newSvg)
