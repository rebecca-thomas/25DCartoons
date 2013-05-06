import sys
import copy
from geometry import *
from pysvg.builders import *
from cartoonParsing import *
from cartoonHelpers import *
from cartoonCalc import *

if __name__ == '__main__':
    inputFile = sys.argv[1]
    numKeyViews, keyViews, cameraPos = readInput(inputFile)

    newSvg = pysvg.parser.svg()
    
    newViewBox, xOffset, yOffset = changeView(keyViews[0])

    offsetMatrix = TransformBuilder()
    offsetMatrix.setMatrix(1, 0, 0, 1, xOffset, yOffset)

    reverseMatrix = TransformBuilder()
    reverseMatrix.setMatrix(-1, 0, 0, 1, xOffset * -1, yOffset * 1) 

    print newViewBox
    newSvg.set_viewBox(newViewBox)

    for i in range(0, numKeyViews):
        keyViews[i].set_transform(offsetMatrix.getTransform())
        keyViews.append(copy.deepcopy(keyViews[i]))
        keyViews[i + numKeyViews].set_transform(reverseMatrix.getTransform())
        cameraPos.append(cameraPos[i] * -1)
    numKeyViews *= 2

    keyDicts = []

    outputFile = sys.argv[2]
    viewTempPos = map(float, sys.argv[3].split("_"))
    viewPos = Point(viewTempPos[0], viewTempPos[1], viewTempPos[2])
    
    weights = getWeighting(cameraPos, viewPos)
    print weights
    viewNum = getViewNum(weights)
    print viewNum

    for svg in keyViews:
        dict = getSubElems(svg)
#        print dict
        keyDicts.append(dict)

    #print
    #print keyDicts[0][u'mouth']._attributes
    #print
    #print keyDicts[3][u'mouth']._attributes
        
#    print keyDicts[1][u'leftEye'].getTopRight()

 #   print keyViews
#    print cameraPos

    strokes = []
    for stroke in keyDicts[0].keys():
        strokes.append(stroke)
  
    anchorPos = []
    for stroke in strokes:
        anchorPos.append(calcAnchorPos(keyDicts, cameraPos, stroke))

#    print anchorPos


#    print keyDicts[4][strokes[0]]._attributes['fill'] 
#    keyDicts[0][u'mouth']._attributes['stroke'] = unicode('#ffff00')

#    keyDicts[5][u'mouth']._attributes['fill'] = unicode('#6F0')
#    print keyDicts[4][strokes[0]]._attributes['fill'] 
    
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
#            print keyViews[viewNum].get_transform()
            tempStroke.set_transform(keyViews[viewNum].get_transform())
            newSvg.addElement(tempStroke)
            print tempStroke.get_transform()
    
    print xOffset
#    newSvg = keyViews[3]
#    newSvg.set_viewBox(newViewBox)
    newSvg.set_transform(offsetMatrix.getTransform())
    print newSvg._attributes
    writeSVG(outputFile, newSvg)
