from math import sqrt
class Point(object):

    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    def __repr__(self):
        return 'Point(x=%s, y=%s, z=%s)' % (self.x, self.y, self.z)
    
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __div__(self, num):
        return Point(self.x / num, self.y / num, self.z / num)

    def __mul__(self, num):
        return Point(-1 * self.x,
                     -1 * self.y,
                     -1 * self.z)

class Vector(object):
    
    def __init__(self, start, end):
        self.x = end.x - start.x
        self.y = end.y - start.y
        self.z = end.z - start.z

    def __repr__(self):
        return 'Point(x=%s, y=%s, z=%s)' % (self.x, self.y, self.z)
    
    def dot(self, toDot):
        dotProduct = self.x * toDot.x
        dotProduct += self.y * toDot.y
        dotProduct += self.z * toDot.z
        return dotProduct

    def cross(self, toCross):
        newX = self.y * toCross.z - self.z * toCross.y
        newY = self.z * toCross.x - self.x * toCross.z
        newZ = self.x * toCross.y - self.y * toCross.x
        newVec = Vector(Point(0,0,0), Point(0,0,0))
        newVec.x = newX
        newVec.y = newY
        newVec.z = newZ
        return newVec

    def __mul__(self, num):
        return Vector(Point(self.x, self.y, self.z), 
                      Point(self.x * num, self.y * num, self.z * num))
    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def __add__(self, other):
        return Vector(self, other)
    
    def norm(self):
        mag = self.length()
        if mag == 0:
            mag = 1
        self.x = self.x / mag
        self.y = self.y / mag
        self.z = self.z / mag
        return self

class Ray(object):
    
    def __init__(self, pos, dir):
        self.pos, self.dir = pos, dir
    
    def __repr__(self):
        return 'Pos:%s Dir:%s' % (self.pos, self.dir)

    def __mul__(self, num):
        return self.pos + self.dir * num
