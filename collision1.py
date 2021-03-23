INT_MAX = 10000

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
        
    def print(self):
        print('point x, y: ' + str(self.x) + ', ' + str(self.y))


class Line(object):
    '''a line in 2D, represented by two points'''
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
        if self.type == 'vertical':
            if self.B.x == P.x:
                contain = True
        elif self.type == 'horizontal':
            y = self.a * P.x + self.b #a = 0, b!= 0
            if y == P.y:
                contain = True
        else:
            y = self.a * P.x + self.b #a, b != 0
            if y == P.y:
                contain = True
        return contain


class Segment(Line):
    '''a segment in 2D, represented by two points'''
    def __init__(self, A, B):
        super().__init__(A, B)

    def contains(self, P):
        #P is a Point object
        contain = False
        if self.type == 'vertical':
            if P.x == self.A.x and ( (P.y >= self.A.y and P.y <= self.B.y) or (P.y <= self.A.y and P.y >= self.B.y) ):
                contain = True
        elif self.type == 'horizontal':
            y = self.a * P.x + self.b #a = 0, b!= 0
            if y == P.y and ( (P.x >= self.A.x and P.x <= self.B.x) or (P.x <= self.A.x and P.x >= self.B.x) ):
                contain = True
        else:
            y = self.a * P.x + self.b #a, b != 0
            if y == P.y and P.x >= self.A.x and P.x <= self.B.x and P.y >= self.A.y and P.y <= self.B.y:
                contain = True
        return contain

    def intersects(self, S):
        #S is a Segment object
        O1 = orientation(self.A, self.B, S.A)
        O2 = orientation(self.A, self.B, S.B)
        O3 = orientation(S.A, S.B, self.A)
        O4 = orientation(S.A, S.B, self.B)
        intersect = False
        #general case
        if O1 != O2 and O3 != O4:
            intersect = True
        #special cases
        #self.A, self.B and S.A are colinear and S.A is on self
        if O1 == 0 and self.contains(S.A):
            intersect = True
        #self.A, self.B and S.B are colinear and S.B is on self
        if O2 == 0 and self.contains(S.B):
            intersect = True
        #S.A, S.B and self.A are colinear and self.A is on S
        if O3 == 0 and S.contains(self.A):
            intersect = True
        #S.A, S.B and self.B are colinear and self.B is on S
        if O4 == 0 and S.contains(self.B):
            intersect = True
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
            
    def printVertices(self):
        for vertex in self.vertices:
            vertex.print()

    def printSides(self):
        for side in self.sides:
            side.print()

    def isInside(self, P):
        #P is a Point object
        #print(P.x, P.y)
        n = len(self.vertices)
        extremePoint = Point(INT_MAX, P.y)
        extremeSegment = Segment(P, extremePoint)
        count = 0
        for side in self.sides:
            if side.intersects(extremeSegment):
                if orientation(side.A, side.B, P) == 0:
                    return side.contains(P)
                count += 1
        return (count % 2 == 1)

    def intersects(self, polygon):
        intersect = False
        for vertex in self.vertices:
            if polygon.isInside(vertex):
                return True
        for vertex in polygon.vertices:
            if self.isInside(vertex):
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

    def scale(self, origin, factor):
        pass

    def translate(self, dx, dy):
        for vertex in self.vertices:
            vertex.translate(dx, dy)

    def move(self, event, dx, dy, canvas):
        self.translate(dx, dy)
        if self.intersects(rectangle):
            self.translate(-dx, -dy)
        self.draw(canvas)


class Rectangle(object):
    def __init__(self, A, C):
        self.A = A
        self.C = C
        self.B = Point(self.C.x, self.A.y)
        self.D = Point(self.A.x, self.C.y)
        self.vertices = [self.A, self.B, self.C, self.D]
        self.sides = []
        v = len(self.vertices)
        for i in range(v):
            P1, P2  = self.vertices[i % v], self.vertices[(i+1) % v]
            side = Segment(P1, P2)
            self.sides.append(side)

    def printVertices(self):
        for vertex in self.vertices:
            vertex.print()

    def printSides(self):
        for side in self.sides:
            side.print()
            #print(side.type)

    def contains(self, P):
        #P is a Point object
        contains = True
        for side in self.sides:
            pass
        return contains


A = Point(2, 1)
B = Point(4, 4)
C = Point(3, 2.5)
D = Point(-2, -5)
E = Point(A.x, B.y)
F = Point(B.x, A.y)


##print(orientation(A, B, E)) #counterclockwise orientation, 2
##print(orientation(A, E, B)) #clockwise orientation, 1


##verticalLine = Segment(A, E) #vertical
##print(verticalLine.type)
##horizontalLine = Segment(E, B) #horizontal
##print(horizontalLine.type)
##generalLine = Segment(A, B) #general
##print(generalLine.type)


##line = Line(A, B)
##line.print()
##print(line.contains(A))
##print(line.contains(B))
##print(line.contains(C))
##print(line.contains(D))
##segment = Segment(A, B)
##segment.print()
##print(segment.contains(A))
##print(segment.contains(B))
##print(segment.contains(C))
##print(segment.contains(D))


##segment1 = Segment(A, B)
##segment2 = Segment(E, F)
##print(segment1.A.x, segment1.A.y, segment1.B.x, segment1.B.y)
##print(segment2.A.x, segment2.A.y, segment2.B.x, segment2.B.y)
##print(segment1.intersects(segment2))
##print(segment2.intersects(segment1))


##rectangle = Rectangle(A, B)
##rectangle.printVertices()
##rectangle.printSides()
##for side in rectangle.sides:
##    print(side.type)


rectangle = Polygon([A, F, B, E])
print(rectangle.isInside(C))
print(rectangle.isInside(E))
print(rectangle.isInside(A))
print(rectangle.isInside(D))
print(rectangle.isInside(Point(100, 100)))


##A = Point(150, 300)
##B = Point(150, 400)
##C = Point(300, 400)
##D = Point(300, 300)
####AB = Segment(A, B)
##rectangle = Polygon([A, B, C, D])
##E = Point(250, 300)
##F = Point(350, 300)
##G = Point(250, 100)
####EF = Segment(E, F)
##triangle = Polygon([E, F, G], color='blue')
####print(AB.intersects(EF))
##for side1 in rectangle.sides:
##    for side2 in triangle.sides:
##        print(side1.intersects(side2))
##        if side1.intersects(side2):
##            print('------------')
##            side1.A.print()
##            side1.B.print()
##            side2.A.print()
##            side2.B.print()



##import tkinter as tk
##
##root = tk.Tk()
##frame = tk.Frame(root, borderwidth=2, relief='groove')
##frame.pack()
##width, height = 500, 500
##canvas = tk.Canvas(frame, width=width, height=height)
##canvas.focus_set()
##canvas.pack()
##
##A = Point(150, 300)
##B = Point(150, 400)
##C = Point(300, 400)
##D = Point(300, 300)
##rectangle = Polygon([A, B, C, D])
##rectangle.draw(canvas)
##          
##E = Point(250, 300)
##F = Point(350, 300)
##G = Point(250, 100)
##triangle = Polygon([E, F, G], color='blue')
##triangle.translate(0, -50)
##triangle.draw(canvas)
##canvas.bind('<Down>', lambda event, dx=0, dy=10, canvas=canvas: triangle.move(event, dx, dy, canvas))
##
##root.mainloop()
