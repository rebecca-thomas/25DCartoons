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
        return Vector(newX, newY, newZ)

    def __mul__(self, num):
        return Vector(Point(self.x, self.y, self.z), 
                      Point(self.x * num, self.y * num, self.z * num))

class Ray(object):
    
    def __init__(self, pos, dir):
        self.pos, self.dir = pos, dir
    
    def __repr__(self):
        return 'Pos:%s Dir:%s' % (self.pos, self.dir)

    def __mul__(self, num):
        return self.pos + self.dir * num
