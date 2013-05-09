from pysvg.shape import *

def getSubElems(elem):
    strokes = {}
    subs(elem, strokes)
    return strokes

def subs(elem, dict):
    if isinstance(elem, path) and elem.getAttribute('id') != None:
        dict[elem.getAttribute('id')] = elem
    for sub in elem._subElements:
        if isinstance(sub, BaseElement):
            subs(sub, dict)

def allEqual(items):
    return all(x == items[0] for x in items)
