import svgwrite
import pysvg.parser
from pysvg.shape import *
from pysvg.builders import *

from svgwrite import cm, mm   
    
def readSVG(fname):
    return pysvg.parser.parse(fname)

def writeSVG(fname, svg):
    svg.save(fname)

if __name__ == '__main__':
    #basic_shapes('test.svg')
    svg = readSVG('SVG_exact_pentagon.svg')
    style = StyleBuilder()
    circle = circle(cx=10, cy=100, r=5, stroke='blue', stroke_width=0.1,fill='green')
    style.setStroke('black')
    style.setStrokeWidth(100)
#    svg.addElement(circle)
    circle.set_style(style.getStyle())
    print svg._subElements
    for elem in svg._subElements:
        if isinstance(elem, BaseElement):
            print elem._elementName
    writeSVG('test.svg', svg)
