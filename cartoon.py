import sys
from string import replace
from geometry import *
from pysvg.builders import *
from cartoonParsing import *
from cartoonHelpers import *
from cartoonCalc import *

if __name__ == '__main__':
    anchorPos = []

    inputFile = sys.argv[1]    
    outputFile = sys.argv[2]
    viewTempPos = map(float, sys.argv[3].split("_"))
    viewPos = Point(viewTempPos[0], viewTempPos[1], viewTempPos[2])


    numKeyViews, keyViews, cameraPos = readInput(inputFile)

    newSvg = pysvg.parser.svg()
    
    newViewBox, xOffset, yOffset = changeView(keyViews[0])

    newSvg.set_viewBox(newViewBox)

    keyViews, numKeyViews, cameraPos = getDerivedViews(keyViews, numKeyViews, 
                                                       cameraPos, xOffset, yOffset)
    
    
    weights = getWeighting(cameraPos, viewPos)
    viewNum = getViewNum(weights)
    
    keyDicts = createKeyDicts(keyViews)
    
    strokes = getStrokeNames(keyDicts)
    print strokes
    
    for stroke in strokes:
        anchorPos.append((calcAnchorPos(keyDicts[:numKeyViews/2], cameraPos[:numKeyViews/2], stroke), stroke))

    zOrder = getZOrdering(anchorPos, viewPos)
    print zOrder
    for z, stroke in zOrder:
        dList = []
        if keyDicts[0].has_key(stroke) and isinstance(keyDicts[0][stroke], path):
            for keyDict in keyDicts:
                if keyDict.has_key(stroke) and isinstance(keyDict[stroke], path):
                    if keyDict[stroke].get_d() != None:
                        dList.append(replace(str(keyDict[stroke].get_d()), ',', ' ').split(' '))

            newD = combineD(dList, weights)
            if isinstance(keyDicts[viewNum][stroke], path):
                tempStroke = copy.deepcopy(keyDicts[viewNum][stroke])
                tempStroke.set_d(newD)
                tempStroke.set_transform(keyViews[viewNum].get_transform())
                newSvg.addElement(tempStroke)
    
#    newSvg.set_transform(offsetMatrix.getTransform())
    
    writeSVG(outputFile, newSvg)
