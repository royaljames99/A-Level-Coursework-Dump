import math
import time

#t1 = time.now()


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Edge():
    def __init__(self, a, b):
        self.a = a
        self.b = b

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

class Circle():
    def __init__(self, centre, radius):
        self.centre = centre
        self.radius = radius

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

def genDelaunay(points, supertriangle):
    triangulation = []
    triangulation.append(supertriangle)
    #add each point one by one
    for point in points:
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
    
    #cleanup
    #for tri in triangulation[:]:
     #   if tri.a == supertriangle.a or tri.a == supertriangle.b or tri.a == supertriangle.c or tri.b == supertriangle.a or tri.b == supertriangle.b or tri.b == supertriangle.c or tri.c == supertriangle.a or tri.c == supertriangle.b or tri.c == supertriangle.c:
      #      triangulation.remove(tri)
    return triangulation

supertriangle = Triangle(Point(-100000,-1000000), Point(0,1000000), Point(1000000,-1000000)) #bloody massive
#points = [Point(0,1), Point(4,3), Point(8,6), Point(2,7), Point(3,3)] #Voronoi seed coordinates
points = [Point(2,3), Point(4,9), Point(-1,-1), Point(-12, 3), Point(-5,-6), Point(5,7)]
#points = [Point(2,2), Point(4,7), Point(-1,-1), Point(-12, 9), Point(-2,-6), Point(5,7)]
#points = [Point(300,12), Point(260,850), Point(912,130), Point(420, 69), Point(0,0)]

print("POINTS")
for i in points:
    print(i.x, i.y)

delaunay = genDelaunay(points, supertriangle)
print("DELAUNAY TRIANGLES")
for i in delaunay:
    print(f"[{i.a.x},{i.a.y}] [{i.b.x},{i.b.y}] [{i.c.x},{i.c.y}]")


#######CONVERT TO VORONOI#######
"""
def calcOutLine(edge, voronoiLines, centreOfGraph, circumcentre):
    if edge.b.y == edge.a.y:
        gradOfLine = 999999999
    else:
        gradOfLine = -1 * ((edge.b.x - edge.a.x)/(edge.b.y - edge.a.y))
    
    if centreOfGraph.x > circumcentre.x:
        phantomPointX = -5000000
    else:
        phantomPointX = 5000000
    
    phantomPointY = (gradOfLine * (phantomPointX - circumcentre.x)) + circumcentre.y
    outLine = Edge(circumcentre, Point(phantomPointX, phantomPointY))
    voronoiLines.append(outLine)
    return voronoiLines

def calcOutLine(edge, voronoiLines, circumcentre):
    if edge.b.y == edge.a.y:
        gradOfLine = 999999999
    else:
        gradOfLine = -1 * ((edge.b.x - edge.a.x)/(edge.b.y - edge.a.y))
    
    if circumcentre.x > ((edge.a.x + edge.b.x) / 2):
        if gradOfLine > 0:
            phantomPointX = 5000000
        else:
            phantomPointX = 5000000
    else:
        if gradOfLine > 0:
            phantomPointX = -5000000
        else:
            phantomPointX = -5000000
    phantomPointY = (gradOfLine * (phantomPointX - circumcentre.x)) + circumcentre.y
    outLine = Edge(circumcentre, Point(phantomPointX, phantomPointY))
    voronoiLines.append(outLine)
    return voronoiLines
"""
centreOfGraphX = 0
centreOfGraphY = 0
for point in points:
    centreOfGraphX += point.x
    centreOfGraphY += point.y
centreOfGraph = Point(point.x/len(points), point.y/len(points))

voronoiLines = []
for triangle in delaunay:
    for tri in delaunay:
        if triangle != tri:
            if checkEdgeEquality(triangle.edges[0], tri.edges[0]) or checkEdgeEquality(triangle.edges[0], tri.edges[1]) or checkEdgeEquality(triangle.edges[0], tri.edges[2]) or checkEdgeEquality(triangle.edges[1], tri.edges[0]) or checkEdgeEquality(triangle.edges[1], tri.edges[1]) or checkEdgeEquality(triangle.edges[1], tri.edges[2]) or checkEdgeEquality(triangle.edges[2], tri.edges[0]) or checkEdgeEquality(triangle.edges[2], tri.edges[1]) or checkEdgeEquality(triangle.edges[2], tri.edges[2]):
                voronoiLines.append(Edge(triangle.circumcircle.centre, tri.circumcircle.centre))
                
    #get outer lines
    """
    edge0Found = False
    edge1Found = False
    edge2Found = False
    for tri in delaunay:
        if triangle != tri:
            if checkEdgeEquality(triangle.edges[0], tri.edges[0]) or checkEdgeEquality(triangle.edges[0], tri.edges[1]) or checkEdgeEquality(triangle.edges[0], tri.edges[2]):
                edge0Found = True
            elif checkEdgeEquality(triangle.edges[1], tri.edges[0]) or checkEdgeEquality(triangle.edges[1], tri.edges[1]) or checkEdgeEquality(triangle.edges[1], tri.edges[2]):
                edge1Found = True
            elif checkEdgeEquality(triangle.edges[2], tri.edges[0]) or checkEdgeEquality(triangle.edges[2], tri.edges[1]) or checkEdgeEquality(triangle.edges[2], tri.edges[2]):
                edge2Found = True
    if not edge0Found:
        voronoiLines = calcOutLine(triangle.edges[0], voronoiLines, triangle.circumcircle.centre)
    if not edge1Found:
        voronoiLines = calcOutLine(triangle.edges[1], voronoiLines, triangle.circumcircle.centre)
    if not edge2Found:
        voronoiLines = calcOutLine(triangle.edges[2], voronoiLines, triangle.circumcircle.centre)
    """
    
#remove duplicates
for line in voronoiLines[:]:
    for l in voronoiLines[:]:
        if line != l:
            if (line.a == l.a and line.b == l.b) or (line.a == l.b and line.b == l.a):
                voronoiLines.remove(line)


print("VORONOI LINES")
for i in voronoiLines:
    print("Segment((", i.a.x, ",", i.a.y, "),(", i.b.x, ",", i.b.y, "))")


supertriangle = Triangle(Point(-100000,-1000000), Point(0,1000000), Point(1000000,-1000000)) #bloody massive
points = [Point(3,6), Point(9,12), Point(19,3), Point(4,22), Point(9,15)]
delaunay = genDelaunay(points, supertriangle)
centreOfGraphX = 0
centreOfGraphY = 0
for point in points:
    centreOfGraphX += point.x
    centreOfGraphY += point.y
centreOfGraph = Point(point.x/len(points), point.y/len(points))

voronoiLines = []
for triangle in delaunay:
    for tri in delaunay:
        if triangle != tri:
            if checkEdgeEquality(triangle.edges[0], tri.edges[0]) or checkEdgeEquality(triangle.edges[0], tri.edges[1]) or checkEdgeEquality(triangle.edges[0], tri.edges[2]) or checkEdgeEquality(triangle.edges[1], tri.edges[0]) or checkEdgeEquality(triangle.edges[1], tri.edges[1]) or checkEdgeEquality(triangle.edges[1], tri.edges[2]) or checkEdgeEquality(triangle.edges[2], tri.edges[0]) or checkEdgeEquality(triangle.edges[2], tri.edges[1]) or checkEdgeEquality(triangle.edges[2], tri.edges[2]):
                voronoiLines.append(Edge(triangle.circumcircle.centre, tri.circumcircle.centre))
#remove duplicates
for line in voronoiLines[:]:
    for l in voronoiLines[:]:
        if line != l:
            if (line.a == l.a and line.b == l.b) or (line.a == l.b and line.b == l.a):
                voronoiLines.remove(line)


print("VORONOI LINES")
for i in voronoiLines:
    print("Segment((", i.a.x, ",", i.a.y, "),(", i.b.x, ",", i.b.y, "))")
input()
