import math
import copy

#http://paul-reed.co.uk/fortune.htm
#http://paul-reed.co.uk/fortune.htm#findoccuranceofregion
#http://paul-reed.co.uk/fortune.htm#findycoord
#http://paul-reed.co.uk/fortune.htm#calctwoedgeintersection

class Point():#(x,y) point in 2D space
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Arc():#parabola represented by a point and a line
    def __init__(self, point, minX = None, maxX = None):
        self.point = point
        self.minX = minX
        self.maxX = maxX
        self.leftEdge = None
        self.rightEdge = None
    
    def calcVals(self, sweeplineY):
        k = (self.point.y + sweeplineY)/2
        p = (self.point.y - sweeplineY)/2

        self.a = 1/(4*p)
        self.b = (-1 * self.point.x) / (2*p)
        self.c = ((self.point.x**2) / (4*p)) + k
    
    def calcY(self, x):
        return ((self.a * (x**2)) + (self.b * x) + self.c)

class Edge():#linear line
    def __init__(self, start, directionVector, m = None, vertical = False, propDirection = None):
        self.start = start
        self.directionVector = directionVector #(dx,dy)
        self.propDirection = propDirection

        if m == None and not vertical:
            self.m = (directionVector[1]/directionVector[0]) #dy/dx
        else:
            self.m = m

        self.vertical = vertical

        if not self.vertical:
            self.c = start.y - (self.m * start.x)
            self.xVal = None
        else:
            self.xVal = start.x

        self.end = None
    
    def calcX(self, y):
        dy = y - self.start.y
        dx = dy * self.directionVector[0]
        x = self.start.x + dx
        return x
    def calcY(self, x):
        if self.vertical:
            return None
        dx = x - self.start.x
        dy = dx * self.directionVector[1]
        y = self.start.y + dy
        return y

class SiteEvent(Point):
    def __init__(self, x, y, site):
        self.eType = "site"
        self.x = x
        self.y = y
        self.site = site

class CircleEvent(Point):
    def __init__(self, x, y, arcs, side):
        self.eType = "circle"
        self.x = x
        self.y = y
        self.arcs = arcs
        self.side = side
        self.circumcentre = self.calcCircumcentre()

    def calcCircumcentre(self):
        point1 = self.arcs[0].point
        point2 = self.arcs[1].point
        point3 = self.arcs[2].point
        #find perp bisectors of 2 sides and find the point where they meet
        #then radius is just distance to one of the points, see derivation
        x1 = point1.x
        y1 = point1.y
        x2 = point2.x
        y2 = point2.y
        x3 = point3.x
        y3 = point3.y
        xab = (x1+x2)/2
        xac = (x1+x3)/2
        yab = (y1+y2)/2
        yac = (y1+y3)/2
        #if two points have same y then x is directly in middle
        if y1 == y2:
            X = (x1 + x2) / 2
            #sub into line eq
            if y1 - y3 == 0:
                Y = yac
            else:
                Y = ((-((x1-x3)/(y1-y3)))*(X-xac)+yac)
        elif y1 == y3:
            X = (x1 + x3)/2
            #sub into line eq
            if y1 - y2 == 0:
                Y = yab
            else:
                Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
        elif y2 == y3:
            X = (x2 + x3)/2
            #sub into line eq
            if y1 - y2 == 0:
                Y = yab
            else:
                Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
        else:
            X = ((((-x1*xab)+(xab*x2))/(y1-y2))+(((x1*xac)-(xac*x3))/(y1-y3))+yac-yab)/(((-x1+x2)/(y1-y2))+((x1-x3)/(y1-y3)))
            #sub into line eq
            if y1 - y2 == 0:
                Y = yab
            else:
                Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
        #Assemble circle object
        cc = Point(X,Y)
        return cc

class Queue():
    def __init__(self):
        self.queue = []

    def insert(self, pos, item):
        self.queue = self.queue[:pos] + [item] + self.queue[pos:]

    def append(self, item):
        self.queue.append(item)
    
    def pop(self):
        item = self.queue[0]
        self.queue = self.queue[1:]
        return item

    def delete(self, pos):
        self.queue = self.queue[:pos] + self.queue[pos + 1:]
 
class Sweepline():
    def __init__(self, y):
        self.y = y
        self.arcs = []
    
    def insert(self, pos, item):
        self.queue = self.queue[:pos] + [item] + self.queue[pos:]

def orderPoints(points):
    newPoints = []
    for point in points:
        y = point.y
        if len(newPoints) == 0:
            newPoints.append(point)
        else:
            for i in range(len(newPoints)):
                if y < newPoints[i].y:
                    newPoints = newPoints[:i] + [point] + newPoints[i:]
                    break
                else:
                    if i == len(newPoints) - 1:
                        newPoints.append(point)
                        break
    return newPoints

def intersectArcs(arc1, arc2):
    a1 = arc1.a
    b1 = arc1.b
    c1 = arc1.c
    a2 = arc2.a
    b2 = arc2.b
    c2 = arc2.c
    #a1x^2 + b1x + c1 = a2x^2 + b2x + c2
    a = (a1 - a2)
    b = (b1 - b2)
    c = (c1 - c2)
    #(a1-a2)x^2 + (b1-b2)x + (c1-c2) = 0
    discriminant = (b**2) - (4*a*c)
    if discriminant < 0:
        return None #no intersection
    x1 = (-b + math.sqrt(discriminant)) / (2*a)
    x2 = (-b - math.sqrt(discriminant)) / (2*a)
    print(x1, x2)
    av = (x1 + x2) / 2 #direct above
    return av

def arcEdgeIntersection(arc, edge):
    if edge.vertical:
        return edge.xVal
        
    a = arc.a
    b = arc.b - edge.m
    c = arc.c - edge.c
    try:
        x1 = (-b + math.sqrt(b**2 - (4*a*c))) / (2*a)
        x2 = (-b - math.sqrt(b**2 - (4*a*c))) / (2*a)
    except:
        print("oof")
        return None
    if edge.directionVector[0] < 0:
        if x1 > x2:
            return x1
        else:
            return x2
    else:
        if x1 < x2:
            return x1
        else:
            return x2

def intersectEdges(edge1, edge2):
    if edge1.vertical:
        X = edge1.xVal
        Y = edge2.calcY(X)
    elif edge2.vertical:
        X = edge2.xVal
        Y = edge1.calcY(X)
    else:
        X = (edge1.c - edge2.c) / (edge2.m + edge1.m)
        Y = edge1.calcY(X)
    return Point(X,Y)

def splitArc(sweep, queue, origArcIdx, newArc):
    origArc = sweep.arcs[origArcIdx]
    left = copy.deepcopy(origArc)
    right = copy.deepcopy(origArc)
    #update circle events
    for i in queue.queue:
        if i.eType == "circle":
            if origArc == i.arcs[0]:
                i.arcs[0] = right
            elif origArc == i.arcs[1]:
                del i
            elif origArc == i.arcs[2]:
                i.arcs[2] = left
    #remake sweepline
    sweep.arcs = sweep.arcs[:origArcIdx] + [left, newArc, right] + sweep.arcs[origArcIdx + 1:]
    #add new edges
    x = newArc.point.x
    start = Point(x, origArc.calcY(x))

    direction = ((-1 * (origArc.point.y - newArc.point.y), origArc.point.x - newArc.point.x))
    vertical = False
    if direction[0] == 0:
        vertical = True
    edge1 = Edge(start, direction, vertical = vertical, propDirection = "left")
    sweep.arcs[origArcIdx].rightEdge = edge1
    sweep.arcs[origArcIdx + 1].leftEdge = edge1

    direction = ((-1 * (newArc.point.y - origArc.point.y), newArc.point.x - origArc.point.x))
    vertical = False
    if direction[0] == 0:
        vertical = True
    edge2 = Edge(start, direction, vertical = vertical, propDirection = "right")
    sweep.arcs[origArcIdx + 1].rightEdge = edge2
    sweep.arcs[origArcIdx + 2].leftEdge = edge2
    
def getCircumcentreFrom3Arcs(Arcs):
    #find perp bisectors of 2 sides and find the point where they meet
    #then radius is just distance to one of the points, see derivation
    x1 = Arcs[0].point.x
    y1 = Arcs[0].point.y
    x2 = Arcs[1].point.x
    y2 = Arcs[1].point.y
    x3 = Arcs[2].point.x
    y3 = Arcs[2].point.y
    xab = (x1+x2)/2
    xac = (x1+x3)/2
    yab = (y1+y2)/2
    yac = (y1+y3)/2

    #if two points have same y then x is directly in middle
    if y1 == y2:
        X = (x1 + x2) / 2
        #sub into line eq
        if y1 - y3 == 0:
            Y = yac
        else:
            Y = ((-((x1-x3)/(y1-y3)))*(X-xac)+yac)
    elif y1 == y3:
        X = (x1 + x3)/2
        #sub into line eq
        if y1 - y2 == 0:
            Y = yab
        else:
            Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
    elif y2 == y3:
        X = (x2 + x3)/2
        #sub into line eq
        if y1 - y2 == 0:
            Y = yab
        else:
            Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
    else:
        X = ((((-x1*xab)+(xab*x2))/(y1-y2))+(((x1*xac)-(xac*x3))/(y1-y3))+yac-yab)/(((-x1+x2)/(y1-y2))+((x1-x3)/(y1-y3)))
        #sub into line eq
        if y1 - y2 == 0:
            Y = yab
        else:
            Y = ((-((x1-x2)/(y1-y2)))*(X - xab)+yab)
    #Assemble circle object
    centre = Point(X,Y)
    return centre

def checkNewCircleEvents(sweep, index, queue, subEvent = False):
    #doing it my way
    #to the left
    if index - 1>= 1:
        arcs = sweep.arcs[index - 2:index + 1]
        if (arcs[0].point.x != arcs[1].point.x or arcs[0].point.y != arcs[1].point.y) and (arcs[0].point.x != arcs[2].point.x or arcs[0].point.y != arcs[2].point.y)  and (arcs[1].point.x != arcs[2].point.x or arcs[1].point.y != arcs[2].point.y):#doesn't share 2 points
            circumcentre = getCircumcentreFrom3Arcs(arcs)
            if not circumcentre.x > arcs[2].point.x: #covered by other one
                radius = math.sqrt((arcs[0].point.y - circumcentre.y)**2 + (arcs[0].point.x - circumcentre.x)**2)
                if not circumcentre.y + radius <= sweep.y: #if above current sweep ignore
                    newEvent = CircleEvent(circumcentre.x, circumcentre.y + radius, arcs, "left")
                    if len(queue.queue) == 0:
                        queue.append(newEvent)
                    else:
                        added = False
                        for i in range(len(queue.queue)):
                            if queue.queue[i].y > newEvent.y:
                                queue.insert(i, newEvent)
                                added = True
                                break
                        if not added:
                            queue.append(newEvent)
    #to the right
    if index <= len(sweep.arcs) - 3:
        arcs = sweep.arcs[index : index + 3]
        if (arcs[0].point.x != arcs[1].point.x or arcs[0].point.y != arcs[1].point.y) and (arcs[0].point.x != arcs[2].point.x or arcs[0].point.y != arcs[2].point.y)  and (arcs[1].point.x != arcs[2].point.x or arcs[1].point.y != arcs[2].point.y):#doesn't share 2 points        
            circumcentre = getCircumcentreFrom3Arcs(arcs)
            if not circumcentre.x < arcs[0].point.x: #covered by other one
                radius = math.sqrt((arcs[0].point.y - circumcentre.y)**2 + (arcs[0].point.x - circumcentre.x)**2)
                if not circumcentre.y + radius <= sweep.y: #if above current sweep ignore
                    newEvent = CircleEvent(circumcentre.x, circumcentre.y + radius, arcs, "right")
                    if len(queue.queue) == 0:
                        queue.append(newEvent)
                    else:
                        added = False
                        for i in range(len(queue.queue)):
                            if queue.queue[i].y > newEvent.y: 
                                queue.insert(i, newEvent)
                                added = True
                                break
                        if not added:
                            queue.append(newEvent)

minX = -50
maxX = 50
leftMostEdge = Edge(Point(minX, -50), (0,1), vertical = True)
rightMostEdge = Edge(Point(maxX, -50), (0,1), vertical = True)
#points = [Point(3,6), Point(9,12), Point(19,3), Point(4,22), Point(9,15)]
points = [Point(0,0), Point(5,5), Point(0,12), Point(6,15)]
#points = [Point(7,11), Point(1,1), Point(4,4), Point(0.5,20), Point(9,3), Point(-2,9)]
#points = [Point(0,0), Point(-1,1), Point(1,1), Point(2,0)]
#points = [Point(0,0), Point(2,0)]
points = orderPoints(points)
queue = Queue()

for point in points:
    queue.append(SiteEvent(point.x, point.y, point))

#setup first arc with boundary edges
firstPoint = queue.pop()
sweep = Sweepline(firstPoint.y)
firstArc = Arc(firstPoint)
firstArc.leftEdge = leftMostEdge
firstArc.rightEdge = rightMostEdge
sweep.arcs.append(firstArc)

vertices = []
edges = []
while len(queue.queue) > 0:
    event = queue.pop()
    sweep.y = event.y + 0.0000001
    print(event.eType, event.x, event.y)
    if event.eType == "circle":
        print("circumcentre: ", event.circumcentre.x, event.circumcentre.y)

    #site events
    if event.eType == "site":
        arc = Arc(event.site)
        arc.calcVals(sweep.y)
        #add arc
        highest = [-1,-50000]
        for i in range(len(sweep.arcs)):
            otherArc = sweep.arcs[i]
            otherArc.calcVals(sweep.y)
            yIntersection = otherArc.calcY(event.site.x)
            if yIntersection > highest[1]:
                highest = [i, yIntersection]
        splitArc(sweep, queue, highest[0], arc)

        ###############add circle events###############
        checkNewCircleEvents(sweep, highest[0] + 1, queue)
        
                            

    #handling circle events
    if event.eType == "circle":
        #mark down the circumcentre and edge
        vertices.append(event.circumcentre)
        event.arcs[1].leftEdge.end = event.circumcentre
        event.arcs[1].rightEdge.end = event.circumcentre
        edges.append(event.arcs[1].leftEdge)
        edges.append(event.arcs[1].rightEdge)
        #remove arc
        arc1 = event.arcs[1]
        idx = sweep.arcs.index(arc1)
        del sweep.arcs[idx]
        #remove other circle events using that arc
        toRemove = []
        for i in range(len(queue.queue)):
            if queue.queue[i].eType == "circle":
                if arc1 in queue.queue[i].arcs:
                    toRemove.append(i)
        for i in range(len(toRemove)):
            del queue.queue[toRemove[i] - i]
        #assign new edge to left and right arc
        direction = (-1 * (event.arcs[0].point.y - event.arcs[2].point.y), event.arcs[0].point.x - event.arcs[2].point.x)
        newEdge = Edge(event.circumcentre, direction, propDirection = event.side)
        sweep.arcs[idx - 1].rightEdge = newEdge
        sweep.arcs[idx].leftEdge = newEdge

        #if adjacent arcs are same arc
        if idx != len(sweep.arcs) - 1:
            if sweep.arcs[idx - 1].point == sweep.arcs[idx + 1].point:
                sweep.arcs[idx - 1].rightEdge = sweep.arcs[idx + 1].rightEdge
                del sweep.arcs[idx + 1]
        
        
        if event.side == "left":
            checkNewCircleEvents(sweep, idx, queue, True)
        else:
            checkNewCircleEvents(sweep, idx - 2, queue, True)
        
        
        

print("\n\n\n")
for i in edges:
    print("Segment((", i.start.x, ",", i.start.y, "),(", i.end.x, ",", i.end.y, "))")
print("unfinished Edges")
for i in sweep.arcs:
    if i.leftEdge not in edges:
        if not i.leftEdge.vertical:
            if i.leftEdge.propDirection == "left":
                print(f"If(x<{i.leftEdge.start.x},{i.leftEdge.m}x + {i.leftEdge.c})")
            else:
                print(f"If(x>{i.leftEdge.start.x},{i.leftEdge.m}x + {i.leftEdge.c})")
        else:
            print("vertical", i.leftEdge.xVal)
    if i.rightEdge not in edges:
        if i.rightEdge != None:
            if not i.rightEdge.vertical:
                if i.rightEdge.propDirection == "left":
                    print(f"If(x<{i.rightEdge.start.x},{i.rightEdge.m}x + {i.rightEdge.c})")
                else:
                    print(f"If(x>{i.rightEdge.start.x},{i.rightEdge.m}x + {i.rightEdge.c})")
            else:
                print("vertical ", i.rightEdge.xVal)