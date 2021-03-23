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
        self.speed = [0, 0]
        
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
        print(P.x, P.y, C)
        counts = [c % 2 == 1 for c in C]
        inside = all(counts)
        return inside

    def intersects(self, polygon):
        intersect = False
        print('self')
        for vertex in self.vertices:
            if polygon.isInside(vertex):
                return True
        print('polygon')
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

    def scale(self, origin, factor):
        for vertex in self.vertices:
            vertex.x = vertex.x + (vertex.x - origin.x) * factor
            vertex.y = vertex.y + (vertex.y - origin.y) * factor

    def translate(self, dx, dy):
        for vertex in self.vertices:
            vertex.translate(dx, dy)

    def rotate(self, origin, angle):
        pass

    def move(self, event, dx, dy, canvas):
        self.translate(dx, dy)
        #self.debug()
        if self.intersects(rectangle):
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



##A = Point(0, 100)
##B = Point(400, 100)
##C = Point(200, 100)
##D = Point(200, 50)
##E = Point(300, 80)
##F = Point(300, 50)
##G = Point(100, 50)
##H = Point(100, 200)
##I = Point(D.x, D.y)
##J = Point(500, D.y)
##AB = Segment(A, B)
##CD = Segment(C, D)
##EF = Segment(E, F)
##GH = Segment(G, H)
##IJ = Segment(I, J)
##print('AB contains C?', AB.contains(C)) #True, de False legyen
##print('AB intersects CD?', AB.intersects(CD)) #True, de False legyen
##print('AB intersects EF?', AB.intersects(EF)) #False
##print('AB intersects GH?', AB.intersects(GH)) #True
##print('CD intersects IJ?', CD.intersects(IJ)) #False



##A = Point(150, 300)
##B = Point(150, 400)
##C = Point(300, 400)
##D = Point(300, 300)
##rectangle = Polygon([A, B, C, D])
##E = Point(250, 300)
##F = Point(350, 300)
##G = Point(250, 100)
##triangle = Polygon([E, F, G], color='blue')
##triangle.translate(50, 30)
####print(triangle.isInside(D))
##for vertex in triangle.vertices:
##    print(vertex.x, vertex.y)
##for vertex in rectangle.vertices:
##    print(vertex.x, vertex.y, triangle.isInside(vertex))
##insidePoint = Point(200, 350)
##outsidePoint = Point(140, 350)
##edgePoint = Point(200, 400)
##print(rectangle.isInside(A))
##print(rectangle.isInside(B))
##print(rectangle.isInside(C))
##print(rectangle.isInside(D))
##print(rectangle.isInside(insidePoint))
##print(rectangle.isInside(outsidePoint))
##print(rectangle.isInside(edgePoint))


import tkinter as tk

root = tk.Tk()
frame = tk.Frame(root, borderwidth=2, relief='groove')
frame.pack()
width, height = 500, 500
canvas = tk.Canvas(frame, width=width, height=height)
canvas.focus_set()
canvas.pack()

A = Point(150, 300)
B = Point(150, 400)
C = Point(300, 400)
D = Point(300, 300)
rectangle = Polygon([A, B, C, D])
rectangle.draw(canvas)

E = Point(250, 300)
F = Point(350, 300)
G = Point(250, 150)
##triangle = Polygon([E, F, G], color='blue')
##triangle.translate(40, -20)
##triangle.draw(canvas)
H = Point(350, 150)
##polygon = Polygon([E, F, H, G], color='blue')
##polygon.draw(canvas)

P1 = Point(250, 100)
P2 = Point(200, 120)
P3 = Point(200, 250)
P4 = Point(300, 250)
P5 = Point(350, 150)
polygon = Polygon([P1, P2, P3, P4, P5], color='blue')
polygon.draw(canvas)
##polygon.scale(P1, 0.5)
##polygon.draw(canvas)

canvas.bind('<Up>', lambda event, dx=0, dy=-10, canvas=canvas: polygon.move(event, dx, dy, canvas))
canvas.bind('<Down>', lambda event, dx=0, dy=10, canvas=canvas: polygon.move(event, dx, dy, canvas))
canvas.bind('<Right>', lambda event, dx=10, dy=0, canvas=canvas: polygon.move(event, dx, dy, canvas))
canvas.bind('<Left>', lambda event, dx=-10, dy=0, canvas=canvas: polygon.move(event, dx, dy, canvas))

root.mainloop()
