import sys
import pysvg.parser
from pysvg.shape import *
from pysvg.builders import *


def readSVG(fname):
    return pysvg.parser.parse(fname)

def writeSVG(fname, svg):
    svg.save(fname)

if __name__ == '__main__':
    numKeyViews = int(sys.argv[1])
    keyViews = []
    for i in range(0, numKeyViews):
        keyViews.append(readSVG(sys.argv[2+i]))

    outputFile = sys.argv[1+numKeyViews]
    
    for svg in keyViews:
        print svg._subElements
        for elem in svg._subElements:
            if isinstance(elem, BaseElement):
                print elem._subElements

    writeSVG(outputFile, svg)
