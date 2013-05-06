import sys
from geometry import *
from pysvg.builders import *
from cartoonParsing import *
from cartoonHelpers import *
from cartoonCalc import *

if __name__ == '__main__':
    inputFile = sys.argv[1]
    numKeyViews, keyViews, cameraPos = readInput(inputFile)
    
    reverseMatrix = TransformBuilder()
    reverseMatrix.setMatrix(-1, 0, 0, -1, 0, 0) 
    for i in range(0, numKeyViews):
        keyViews.append(keyViews[i])
        keyViews[i].set_transform(reverseMatrix)
        cameraPos.append(cameraPos[i] * -1)
    numKeyViews *= 2

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
    print keyDicts[4][strokes[0]]._attributes['fill'] 
#    keyDicts[0][u'mouth']._attributes['stroke'] = unicode('#ffff00')

    keyDicts[5][u'mouth']._attributes['fill'] = unicode('#6F0')
    print keyDicts[4][strokes[0]]._attributes['fill'] 
    
    for stroke in strokes:
        dList = []
        if isinstance(keyDicts[0][stroke], path):
            count = 0
            for keyDict in keyDicts:
                if keyDict[stroke].get_d() != None:
                    dList.append(str(keyDict[stroke].get_d()).split(' '))

            newD = combineD(dList, weights)
            keyDict[stroke].set_d(newD)
            svg.addElement(keyDicts[0][stroke])
    writeSVG(outputFile, svg)
