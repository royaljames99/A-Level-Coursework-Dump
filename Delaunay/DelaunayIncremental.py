import math
import matplotlib.pyplot as plt

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.dualLine = None #Used for delaunay edges to keep track of accompanying voronoi edges

class Circle():
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius
    
class Triangle():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.edges = [Edge(a,b), Edge(a,c), Edge(b,c)]
        self.circumcircle = self.genCircumcircle()

    def genCircumcircle(self):
        #find perp bisectors of 2 sides and find the point where they meet
        #then radius is just distance to one of the points, see derivation
        x1 = self.a.x
        y1 = self.a.y
        x2 = self.b.x
        y2 = self.b.y
        x3 = self.c.x
        y3 = self.c.y
        xab = (x1+x2)/2
        xac = (x1+x3)/2
        yab = (y1+y2)/2
        yac = (y1+y3)/2

        #if two points have same y then x is directly in middle
        if y1 == y2:
            X = (x1 + x2) / 2
            #sub into line eq
            Y = ((-((x1-x3)/(y1-y3)))*(X-xac)+yac)
        elif y1 == y3:
            X = (x1 + x3)/2
            #sub into line eq
            Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
        elif y2 == y3:
            X = (x2 + x3)/2
            #sub into line eq
            Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
        else:
            X = ((((-x1*xab)+(xab*x2))/(y1-y2))+(((x1*xac)-(xac*x3))/(y1-y3))+yac-yab)/(((-x1+x2)/(y1-y2))+((x1-x3)/(y1-y3)))
            #sub into line eq
            Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
        #Assemble circle object
        centre = Point(X,Y)
        radius = math.sqrt((X-x2)**2 + (Y-y2)**2)
        circumcircle = Circle(centre, radius)
        return circumcircle

def checkEdgeEquality(e1, e2):
    if (e1.a == e2.a and e1.b == e2.b) or (e1.a == e2.b and e1.b == e2.a):
        return True
    return False

def checkIfSharesEdges(edge, currentTri, triangleSet):
    for tri in triangleSet:
        if tri != currentTri:
            for e in tri.edges:
                if checkEdgeEquality(edge, e):
                    return True
    return False

def addPoint(point, triangulation):
    btriangles = []
    #find all triangles that are no longer valid
    for tri in triangulation:
        distToCircumcentre = math.sqrt(((tri.circumcircle.centre.x - point.x)**2) + ((tri.circumcircle.centre.y - point.y)**2))
        if tri.circumcircle.radius > distToCircumcentre:
            btriangles.append(tri)
    #find boundary of polygonal hole
    polygon = []
    for tri in btriangles:
        for edge in tri.edges:
            if not checkIfSharesEdges(edge, tri, btriangles):
                polygon.append(edge)
    #remove bad triangles from triangulation
    for tri in btriangles:
        triangulation.remove(tri)
    #create new triangles
    for edge in polygon:
            triangulation.append(Triangle(edge.a, edge.b, point))
    return triangulation

def genDelaunay(points, supertriangle):
    triangulation = []
    triangulation.append(supertriangle)
    for point in points:
        triangulation = addPoint(point, triangulation)
    return triangulation

def addToVoronoi(triangle, triangles, voronoiLines):
    for tri in triangles:
        if triangle != tri:

            if checkEdgeEquality(triangle.edges[0], tri.edges[0]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[0].dualLine = newVEdge
                tri.edges[0].dualLine = newVEdge      

            elif checkEdgeEquality(triangle.edges[0], tri.edges[1]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[0].dualLine = newVEdge
                tri.edges[1].dualLine = newVEdge

            elif checkEdgeEquality(triangle.edges[0], tri.edges[2]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[0].dualLine = newVEdge
                tri.edges[2].dualLine = newVEdge 

            elif checkEdgeEquality(triangle.edges[1], tri.edges[0]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[1].dualLine = newVEdge
                tri.edges[0].dualLine = newVEdge

            elif checkEdgeEquality(triangle.edges[1], tri.edges[1]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[1].dualLine = newVEdge
                tri.edges[1].dualLine = newVEdge 

            elif checkEdgeEquality(triangle.edges[1], tri.edges[2]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[1].dualLine = newVEdge
                tri.edges[2].dualLine = newVEdge 

            elif checkEdgeEquality(triangle.edges[2], tri.edges[0]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[2].dualLine = newVEdge
                tri.edges[0].dualLine = newVEdge   

            elif checkEdgeEquality(triangle.edges[2], tri.edges[1]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[2].dualLine = newVEdge
                tri.edges[1].dualLine = newVEdge    

            elif checkEdgeEquality(triangle.edges[2], tri.edges[2]):
                newVEdge = Edge (triangle.circumcircle.centre, tri.circumcircle.centre)
                voronoiLines.append(newVEdge)
                triangle.edges[2].dualLine = newVEdge
                tri.edges[2].dualLine = newVEdge    

    return voronoiLines

def convertToVoronoi(delaunay):
    voronoiLines = []
    for triangle in delaunay:
        voronoiLines = addToVoronoi(triangle, delaunay, voronoiLines)

    #remove duplicates
    for line in voronoiLines[:]:
        for l in voronoiLines[:]:
            if line != l:
                if (line.a == l.a and line.b == l.b) or (line.a == l.b and line.b == l.a):
                    voronoiLines.remove(line)

    return voronoiLines

def findChangedTriangles(delaunay1, delaunay2):
    deletedTriangles = []
    newTriangles = delaunay2.copy()
    for triangle in delaunay1:
        try:
            newTriangles.remove(triangle)
        except:
            deletedTriangles.append(triangle)

    return newTriangles, deletedTriangles

def updateVoronoi(voronoiLines, delaunay, newTriangles, deletedTriangles):
    #add the new stuff
    for triangle in newTriangles:
        voronoiLines = addToVoronoi(triangle, delaunay, voronoiLines)
    #delete the old stuff
    for triangle in deletedTriangles:
        if triangle.edges[0].dualLine in voronoiLines:
            voronoiLines.remove(triangle.edges[0].dualLine)
        if triangle.edges[1].dualLine in voronoiLines:
            voronoiLines.remove(triangle.edges[1].dualLine)
        if triangle.edges[2].dualLine in voronoiLines:
            voronoiLines.remove(triangle.edges[2].dualLine)
    #remove duplicate lines
    for line in voronoiLines[:]:
        for l in voronoiLines[:]:
            if line != l:
                if (line.a == l.a and line.b == l.b) or (line.a == l.b and line.b == l.a):
                    voronoiLines.remove(line)
    return voronoiLines

def matPlotLib(points, voronoi, index):
    plt.subplot(1,3,index)
    for point in points:
        plt.plot(point.x, point.y, marker = "o", markersize = 1)
    for line in voronoi:
        plt.plot([line.a.x, line.b.x], [line.a.y, line.b.y])
    plt.xlim([-50,50])
    plt.ylim([-55,55])

#make original
supertriangle = Triangle(Point(-100000,-1000000), Point(0,1000000), Point(1000000,-1000000)) #bloody massive
#points = [Point(2,3), Point(4,9), Point(-1,-1), Point(-12, 3), Point(-5,-6), Point(5,7)]
import random
points = []
for i in range(300):
    points.append(Point(random.randint(-40,40), random.randint(-40,40)))
print(len(points))
delaunay = genDelaunay(points, supertriangle)
voronoi = convertToVoronoi(delaunay)
matPlotLib(points, voronoi, 1)

#add point
delaunay2 = delaunay.copy()
for i in range(20):
    newPoint = Point(random.randint(-40,40), random.randint(-40,40))
    delaunay2 = addPoint(newPoint, delaunay2.copy())
    points.append(newPoint)

import time

#remake voronoi entirely
t1 = time.time()
voronoi2 = convertToVoronoi(delaunay2)
t2 = time.time()

#remake voronoi by updating small section
t3 = time.time()
newLines, deletedLines = findChangedTriangles(delaunay, delaunay2)
voronoi3 = updateVoronoi(voronoi, delaunay2, newLines, deletedLines)
t4 = time.time()

matPlotLib(points, voronoi2, 2)
matPlotLib(points, voronoi3, 3)

#calc time differences
print("TIME TAKEN FOR FULL REDO = ", (t2 - t1))
print("TIME TAKEN FOR PARTIAL REDO = ", (t4 - t3))
diff = (t2-t1)-(t4-t3)
print(f"PARTIAL IS {diff} SECONDS FASTER")

#show output
plt.show()