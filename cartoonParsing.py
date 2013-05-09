import pysvg.parser
from geometry import *

def readSVG(fname):
    return pysvg.parser.parse(fname)

def writeSVG(fname, svg):
    svg.save(fname)

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
        print
    return numViews, keyViews, cameraPos
