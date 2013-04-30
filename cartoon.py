import sys
import pysvg.parser
from pysvg.shape import *
from pysvg.builders import *


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
        cameraPos.append([float(f.readline()), 
                          float(f.readline()), 
                          float(f.readline())])
    return numViews, keyViews, cameraPos

if __name__ == '__main__':
    inputFile = sys.argv[1]
    numKeyViews, keyViews, cameraPos = readInput(inputFile)

    keyDicts = []

    outputFile = sys.argv[0]
    
    for svg in keyViews:
        dict = getSubElems(svg)
        print dict
        keyDicts.append(dict)
        
    print keyDicts[1][u'leftEye'].getTopRight()

    print keyViews
    print cameraPos

    

    writeSVG(outputFile, svg)
