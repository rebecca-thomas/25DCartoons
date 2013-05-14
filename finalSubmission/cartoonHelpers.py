from pysvg.shape import *

def getSubElems(elem):
    """ adds path elements to a dictionary"""
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
    """ checks if all elements in a list are equal"""
    return all(x == items[0] for x in items)
