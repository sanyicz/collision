INT_MAX = 10000
import tkinter as tk
from math import copysign, cos, sin, pi
import numpy as np


def orientation(P1, P2, P3):
    #slope of P1,P2 : m1
    #slope of P2,P3 : m2
    #if m1 > m2 : clockwise (right turn)
    val = ( (P2.y - P1.y) * (P3.x - P2.x) ) - ( (P2.x - P1.x) * (P3.y - P2.y) )
    if val > 0:
        return 1 #clockwise orientation
    elif val < 0:
        return 2 #counterclockwise orientation
    else:
        return 0 #colinear orientation

    
class Point(object):
    '''a point in 2D, represented by two coordinates'''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self, angle):
        R = [[cos(angle), -sin(angle)], [sin(angle), cos(angle)]]
        rotationMatrix = np.array(R)
        coordinates = np.array([self.x, self.y])
        rotated = rotationMatrix.dot(coordinates)
        self.x = rotated[0]
        self.y = rotated[1]
    
    def print(self):
        print('point x, y: ' + str(self.x) + ', ' + str(self.y))


class Segment(object):
    '''a segment in 2D, represented by two points'''
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.type = None
        #print(A.x, A.y)
        #print(B.x, B.y)
        if self.B.x == self.A.x and self.B.y == self.A.y:
            self.type = 'point'
            self.a = None
            self.b = None
        elif self.B.x == self.A.x and self.B.y != self.A.y:
            self.type = 'vertical'
            self.a = None
            self.b = None
        elif self.B.y == self.A.y and self.B.x != self.A.x:
            self.type = 'horizontal'
            self.a = 0
            self.b = self.B.y
        else:
            self.a = ( self.B.y - self.A.y ) / ( self.B.x - self.A.x )
            self.b = ( ( self.B.y + self.A.y ) - self.a * ( self.B.x + self.A.x ) ) / 2
            self.type = 'general'
        #print(self.type)
        
    def print(self):
        print('y = ' + str(self.a) + ' * x + ' + str(self.b))

    def contains(self, P):
        #P is a Point object
        contain = False
        if orientation(self.A, P, self.B) == 0:
            if ( P.x <= max(self.A.x, self.B.x) ) and ( P.x >= min(self.A.x, self.B.x) ) and ( P.y <= max(self.A.y, self.B.y) ) and ( P.y >= min(self.A.y, self.B.y) ):
                contain = True
        return contain

    def intersects(self, S):
        #S is a Segment object
        O1 = orientation(self.A, self.B, S.A)
        O2 = orientation(self.A, self.B, S.B)
        O3 = orientation(S.A, S.B, self.A)
        O4 = orientation(S.A, S.B, self.B)
        intersect = False
        #print(O1, O2, O3, O4)
        #general case
        if O1 != O2 and O3 != O4:
            if O1 != 0 and O2 != 0 and O3 != 0 and O4 != 0:
                intersect = True
##        #special cases
##        #self.A, self.B and S.A are colinear and S.A is on self
##        if O1 == 0 and self.contains(S.A):
##            intersect = True
##        #self.A, self.B and S.B are colinear and S.B is on self
##        if O2 == 0 and self.contains(S.B):
##            intersect = True
##        #S.A, S.B and self.A are colinear and self.A is on S
##        if O3 == 0 and S.contains(self.A):
##            intersect = True
##        #S.A, S.B and self.B are colinear and self.B is on S
##        if O4 == 0 and S.contains(self.B):
##            intersect = True
        return intersect


class Polygon(object):
    def __init__(self, vertices, color='red'):
        self.color = color
        self.vertices = vertices
        self.sides = []
        v = len(self.vertices)
        for i in range(v):
            P1, P2  = self.vertices[i % v], self.vertices[(i+1) % v]
            side = Segment(P1, P2)
            self.sides.append(side)
        self.area() #calculate area
        self.centroid() #calculate centroid
        
    def printVertices(self):
        for vertex in self.vertices:
            vertex.print()

    def printSides(self):
        for side in self.sides:
            side.print()

    def isInside(self, P):
        #P is a Point object
        inside = False
        extremeXmax = Segment(P, Point(INT_MAX, P.y))
        extremeXmin = Segment(P, Point(-INT_MAX, P.y))
        extremeYmax = Segment(P, Point(P.x, INT_MAX))
        extremeYmin = Segment(P, Point(P.x, -INT_MAX))
        extremes = [extremeXmax, extremeXmin, extremeYmax, extremeYmin]
        C = [0, 0, 0, 0]
        for side in self.sides:
            for i in range(len(extremes)):
                if side.intersects(extremes[i]):
                    C[i] += 1
        #print(P.x, P.y, C)
        counts = [c % 2 == 1 for c in C]
        inside = all(counts)
        return inside

    def intersects(self, polygon):
        intersect = False
        #print('self')
        for vertex in self.vertices:
            if polygon.isInside(vertex):
                return True
        #print('polygon')
        for vertex in polygon.vertices:
            if self.isInside(vertex):
                return True
        for selfside in self.sides:
            for polygonside in polygon.sides:
                if selfside.intersects(polygonside):
                    return True
        return intersect

    def draw(self, canvas):
        try:
            canvas.delete(self.figure)
        except:
            pass
        points = []
        for vertex in self.vertices:
            points.append(vertex.x)
            points.append(vertex.y)
        self.figure = canvas.create_polygon(*points, fill=self.color)

    def scale(self, center, factor):
        center = self.C
        for vertex in self.vertices:
            vertex.x = vertex.x + (vertex.x - center.x) * factor
            vertex.y = vertex.y + (vertex.y - center.y) * factor

    def translate(self, dx, dy):
        for vertex in self.vertices:
            vertex.translate(dx, dy)

    def area(self):
        summa = 0
        n = len(self.vertices)
        for i in range(0, n):
            xi = self.vertices[i%n].x
            yi = self.vertices[i%n].y
            xi1 = self.vertices[(i+1)%n].x
            yi1 = self.vertices[(i+1)%n].y
            summa += ( xi * yi1 -  xi1 * yi )
        self.A = summa / 2

    def centroid(self):
        summaX, summaY = 0, 0
        n = len(self.vertices)
        for i in range(0, n):
            xi = self.vertices[i%n].x
            yi = self.vertices[i%n].y
            xi1 = self.vertices[(i+1)%n].x
            yi1 = self.vertices[(i+1)%n].y
            summaX += (xi + xi1) * ( xi * yi1 - xi1 * yi)
            summaY += (yi + yi1) * ( xi * yi1 - xi1 * yi)
        Cx = summaX / (6 * self.A)
        Cy = summaY / (6 * self.A)
        self.C = Point(Cx, Cy)

    def rotate(self, center, angle, unit):
        #convert angle to radians (for math.cos and math.sin)
        if unit == 'rad':
            pass
        elif unit == 'deg':
            angle = pi * (angle / 180)
        else:
            print('unknown unit of angle')
        #translate to origin (0, 0)
        for vertex in self.vertices:
            vertex.translate(-center.x, -center.y)
        #rotate around origin
        R = [[cos(angle), -sin(angle)], [sin(angle), cos(angle)]]
        rotationMatrix = np.array(R)
        for vertex in self.vertices:
            vertex.rotate(angle)
        #translate back
        for vertex in self.vertices:
            vertex.translate(center.x, center.y)

    def move(self, event, dx, dy, canvas):
        self.translate(dx, dy)
        #self.debug()
        if self.intersects(objects[0]) or self.intersects(objects[1]):
            self.translate(-dx, -dy)
        self.draw(canvas)
        
    def debug(self):
        print('######################')
        print('self.vertices')
        for vertex in self.vertices:
            print(vertex.x, vertex.y, rectangle.isInside(vertex))
        print('rectangle.vertices')
        for vertex in rectangle.vertices:
            print(vertex.x, vertex.y, self.isInside(vertex))
        print('sides')
        for side in self.sides:
            print('----------------')
            print(side.A.x, side.A.y, side.B.x, side.B.y)
            for sidee in rectangle.sides:
                print(sidee.A.x, sidee.A.y, sidee.B.x, sidee.B.y)
                print(side.intersects(sidee))
        print('intersect?', self.intersects(rectangle))


class Object(Polygon):
    '''a polygon, etc.'''
    def __init__(self, vertices, color='red', name=None, typee=None):
        super().__init__(vertices, color)
        self.name = name
        self.type = typee #moving or static
        self.speed = 0 #[0, 0] #speed vector
        self.angle = 0

    def setSpeed(self, speed):
        self.speed += speed

    def setAngle(self, angle):
        self.angle += angle

    def intersects(self, polygon):
        intersect = False
        #print('self')
        for vertex in self.vertices:
            if polygon.isInside(vertex):
                return True
        #print('polygon')
        for vertex in polygon.vertices:
            if self.isInside(vertex):
                return True
        for selfside in self.sides:
            for polygonside in polygon.sides:
                if selfside.intersects(polygonside):
                    return True
        return intersect


class World(tk.Canvas):
    def __init__(self, frame, width, height):
        super().__init__(frame, width=width, height=height)
        self.focus_set()
        self.pack()
        self.speed = 0
        self.DX, self.DY = 0, 0
        self.bindMoveButtons()
        self.bind('<a>', self.increaseSpeed)
        self.bind('<y>', self.decreaseSpeed)
        self.objects = {}
        self.movingObject = None

    def bindMoveButtons(self):
##        self.bind('<Up>', lambda event, dx=0, dy=-self.DY: self.moveObject(event, dx, dy))
##        self.bind('<Down>', lambda event, dx=0, dy=self.DY: self.moveObject(event, dx, dy))
##        self.bind('<Left>', lambda event, dx=-self.DX, dy=0: self.moveObject(event, dx, dy))
##        self.bind('<Right>', lambda event, dx=self.DX, dy=0: self.moveObject(event, dx, dy))
        self.bind('<Up>', lambda event, distance=10: self.go(event, distance))
        self.bind('<Down>', lambda event, distance=-10: self.go(event, distance))
        self.bind('<Left>', lambda event, angle=-15, unit='deg': self.rotateObject(event, angle, unit))
        self.bind('<Right>', lambda event, angle=15, unit='deg': self.rotateObject(event, angle, unit))
        
    def increaseSpeed(self, event):
        self.setSpeed(1)
##        self.movingObject.setSpeed(1)
##        self.DX += 1
##        self.DY += 1
##        self.bindMoveButtons()
##        print('self.movingObject.speed:', self.movingObject.speed)

    def decreaseSpeed(self, event):
        self.setSpeed(-1)
##        self.movingObject.setSpeed(-1)
##        self.DX -= 1
##        self.DY -= 1
##        self.bindMoveButtons()
##        print('self.movingObject.speed:', self.movingObject.speed)

    def setSpeed(self, speed):
##        self.speed += speed
##        self.DX += speed
##        self.DY += speed
        self.movingObject.setSpeed(speed)
        self.DX = self.movingObject.speed
        self.DY = self.movingObject.speed
        self.bindMoveButtons()
        print('self.DY, self.DY:', self.DY, self.DY)

    def addObject(self, name, obj):
        obj.canvas = self
        self.objects[name] = obj
        if obj.type == 'moving':
            if self.movingObject == None:
                self.movingObject = obj
                self.setSpeed(self.movingObject.speed)
            else:
                print('more than one moving type object')

    def draw(self):
        for name, obj in self.objects.items():
            obj.draw(self)

    def intersection(self, movingObject):
        '''check if obj intersects with any other object in the world'''
        instersectionCount = 0
        for obj in self.objects.values():
            if obj is not movingObject:
                if movingObject.intersects(obj):
                    if obj.type == 'static':
                        instersectionCount += 1
                        return True
                    elif obj.type == 'collectible':
                        print(obj.name, 'collected')
        if instersectionCount > 0:
            return True

    def rotateObject(self, event, angle, unit):
        origin = self.movingObject.C
        degrees = 0
        delta = copysign(1, angle) #+1 or -1 degrees
        while degrees < abs(angle):
            self.movingObject.rotate(origin, delta, unit)
            if self.intersection(self.movingObject) == True:
                self.movingObject.rotate(origin, -delta, unit)
                break
            else:
                self.draw()
            degrees += 1
##        self.movingObject.rotate(origin, angle, unit)
        self.movingObject.setAngle(copysign(degrees, angle)) #angle?????
        self.draw()
        self.movingObject.centroid()
        
##    def moveObject(self, event, dx, dy):
##        '''move the self.movingObject object in the world'''
##        print('moveObject by dx, dy:', dx, dy)
##        self.movingObject.translate(dx, dy)
##        if self.intersection(self.movingObject) == True:
##            self.movingObject.translate(-dx, -dy)
##        self.draw()
        
##    def moveObject(self, event, dx, dy):
##        '''move the self.movingObject object in the world'''
##        print('moveObject')
##        n = self.DY #must be an integer integer
##        dX = 1 if self.DY == 1 else (self.DX - 1) // (self.DY - 1)
##        dY = 1 #always 1
##        print('self.DY, self.DY:', self.DY, self.DY)
##        print('number of steps:', n)
##        print('unit steps:', dX, dY)
##        for i in range(n):
##            self.movingObject.translate(dX, dY)
##            if self.intersection(self.movingObject) == True:
##                self.movingObject.translate(-dX, -dY)
##                break
##            else:
##                self.draw()
##        self.draw()
        
    def moveObject(self, event, dx, dy):
        '''move the self.movingObject object in the world'''
        #print('moveObject by dx, dy:', dx, dy)
        Xrange, Yrange = abs(int(dx)), abs(int(dy))
        for i in range(Xrange):
            dX = copysign(1, dx)
            self.movingObject.translate(dX, 0)
            if self.intersection(self.movingObject) == True:
                self.movingObject.translate(-dX, 0)
                break
            else:
                self.draw()
        for i in range(Yrange):
            dY = copysign(1, dy)
            self.movingObject.translate(0, dY)
            if self.intersection(self.movingObject) == True:
                self.movingObject.translate(0, -dY)
                break
            else:
                self.draw()
        self.draw()
        self.movingObject.centroid()

    def go(self, event, distance):
        '''go forward by distance'''
        angle = self.movingObject.angle
        angle = pi * (angle / 180) #angle is stored in units of degrees, but it must be in radians for math.cos and math.sin
        dx = distance * cos(angle)
        dy = distance * sin(angle)
        #print(distance, angle, dx, dy)
        self.moveObject(event, dx, dy)




A = Point(0, 200)
B = Point(0, 500)
C = Point(200, 500)
D = Point(200, 300)
E = Point(300, 300)
F = Point(300, 200)

G = Point(100, 0)
H = Point(100, 100)
I = Point(400, 100)
J = Point(400, 400)
K = Point(300, 400)
L = Point(300, 500)
M = Point(500, 500)
N = Point(500, 0)

corridor1 = Object([A, B, C, D, E, F], color='blue', name='corridor1', typee='static')
corridor2 = Object([G, H, I, J, K, L, M, N], color='blue', name='corridor2', typee='static')

P1 = Point(25, 25)
P2 = Point(25, 75)
P3 = Point(75, 75)
P4 = Point(75, 25)
polygon = Object([P1, P2, P3, P4], color='red', name='polygon', typee='moving')
print(polygon.A)
polygon.C.print()


P5 = Point(350, 250)
P6 = Point(350, 255)
P7 = Point(355, 255)
P8 = Point(355, 250)
collectible1 = Object([P5, P6, P7, P8], color='orange', name='collectible1', typee='collectible')


root = tk.Tk()
frame = tk.Frame(root, borderwidth=2, relief='groove')
frame.pack()
width, height = 500, 500
world = World(frame, width, height)
world.addObject('corridor1', corridor1)
world.addObject('corridor2', corridor2)
world.addObject('polygon', polygon)
world.addObject('collectible1', collectible1)
##world.rotateObject(30, 'deg')
world.draw()
world.setSpeed(10)
world.setSpeed(-9)
root.mainloop()




##root = tk.Tk()
##frame = tk.Frame(root, borderwidth=2, relief='groove')
##frame.pack()
##width, height = 500, 500
##canvas = tk.Canvas(frame, width=width, height=height)
##canvas.focus_set()
##canvas.pack()
##
##corridor1.draw(canvas)
##corridor2.draw(canvas)
##polygon.draw(canvas)
##
##DX, DY = 1, 1
##canvas.bind('<Up>', lambda event, dx=0, dy=-DY, canvas=canvas: polygon.move(event, dx, dy, canvas))
##canvas.bind('<Down>', lambda event, dx=0, dy=DY, canvas=canvas: polygon.move(event, dx, dy, canvas))
##canvas.bind('<Right>', lambda event, dx=DX, dy=0, canvas=canvas: polygon.move(event, dx, dy, canvas))
##canvas.bind('<Left>', lambda event, dx=-DX, dy=0, canvas=canvas: polygon.move(event, dx, dy, canvas))
##
##root.mainloop()
