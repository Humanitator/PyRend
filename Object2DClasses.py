#This script contains all 2D primary objects

#Imports
from VectorMath import Vector2
from MainClasses import Grid, Primary2D
from Transforms import Transform2D


#A basic 2D point
class Point2D(Primary2D):
    #Plot the point on a grid
    def Plot(self, grid: Grid) -> Grid:
        grid.Plot(self.transform.globalPosition(), self.fill)
        return grid

    #Initialization
    def __init__(self, transform = Transform2D(), fill = "#") -> None:
        transform.primary = self
        super().__init__(transform, fill)


#A basic 2D line from a to b
class Line2D(Primary2D):
    #Basic
    a = None
    b = None

    #Geometry
    m_X = None #Multiplier for X
    m_Y = None #Multiplier for Y

    b_Y = None #Offset for Y

    # Get a coordinate by passing the opposite coordinate
    def GetCoord(self, oppCoord: float, isX = True, raw = False) -> float:
        coord = None #The wanted coordiante

        if isX: #If the passed coordinate is a x coordinate
            if (self.m_X == 0): #If x multiplier is 0
                coord = -self.b_Y
            else:
                coord = (self.m_X * oppCoord - self.b_Y) / self.m_Y
        else: #If the passed coordinate is a y coordinate
            if (self.m_Y == 0): #If y multiplier is 0
                coord = self.b_Y
            else:
                coord = (self.m_Y * oppCoord + self.b_Y) / self.m_X
        coord = round(coord) #Round the coordinate
        return coord

    # Check if the line is steep (>45 degrees)
    def isSteep(self):
        return abs(self.m_X) >= abs(self.m_Y)

    # Get all plottable positions
    def GetPlotXYPosDict (self) -> dict:
        posXDict = {} #Array to hold all plottable positions

        #Get global positions of points
        a_gPos = self.a.transform.globalPosition()
        b_gPos = self.b.transform.globalPosition()

        #Check if points aren't in the same place
        if a_gPos == b_gPos:
            posXDict[a_gPos.x] = [a_gPos.y]
            return posXDict

        if self.isSteep():
            mxY = max(a_gPos.y, b_gPos.y) #Point in line with highest y
            loY = min(a_gPos.y, b_gPos.y) #Point in line with lowest y
            yRange = range(loY, mxY+1) #Range with all of lines Y's

            for y in yRange:
                x = self.GetCoord(y, False)
                if x in posXDict:
                    posXDict[x].append(y) #Add coordinate to array
                else:
                    posXDict[x] = [y] #Make new array for coordinate
        else:
            mxX = max(a_gPos.x, b_gPos.x) #Point in line with highest x
            loX = min(a_gPos.x, b_gPos.x) #Point in line with lowest x
            xRange = range(loX, mxX+1) #Range with all of lines X's

            for x in xRange:
                y = self.GetCoord(x)
                if x in posXDict:
                    posXDict[x].append(y) #Add coordinate to array
                else:
                    posXDict[x] = [y] #Make new array for coordinate
        return posXDict
        

        #------Rasterization---------
    #Plot the line on a grid
    def Plot(self, grid: Grid, bounded = True) -> Grid:
        #Get global positions of points
        a_gPos = self.a.transform.globalPosition()
        b_gPos = self.b.transform.globalPosition()

        #Check if points aren't in the same place
        if a_gPos == b_gPos:
            grid.Plot(a_gPos, self.fill)
            return grid

        if self.isSteep():
            mxY = max(a_gPos.y, b_gPos.y) #Point in line with highest y
            loY = min(a_gPos.y, b_gPos.y) #Point in line with lowest y

            if not bounded:
                for y in range(grid.ySize):
                    grid.Plot(Vector2(self.GetCoord(y, False), y), self.fill) #Plot coordinate
            else:
                for y in range(loY, mxY+1):
                    grid.Plot(Vector2(self.GetCoord(y, False), y), self.fill) #Plot coordinate
        else:
            mxX = max(a_gPos.x, b_gPos.x) #Point in line with highest x
            loX = min(a_gPos.x, b_gPos.x) #Point in line with lowest x

            if not bounded:
                for x in range(grid.xSize):
                    grid.Plot(Vector2(x, self.GetCoord(x)), self.fill) #Plot coordinate
            else:
                for x in range(loX, mxX+1):
                    grid.Plot(Vector2(x, self.GetCoord(x)), self.fill) #Plot coordinate
        return grid

    #Stringifies
    def __str__(self) -> str:
        return f"({self.a.transform.globalPosition()}, {self.b.transform.globalPosition()})"

    #Initialization
    def __init__(self, pointA: Point2D, pointB: Point2D, fill = "#$#") -> None:
        #Basic
        self.a = pointA
        self.b = pointB

        #Geometry
        pA_pB_Vec = pointA.transform.globalPosition().vectorTo(pointB.transform.globalPosition())

            #Multipliers
        self.m_X = pA_pB_Vec.y
        self.m_Y = pA_pB_Vec.x

            #Offsets
        b_Y = -(pointA.transform.globalPosition().y * self.m_Y)
        b_X = -(pointA.transform.globalPosition().x * self.m_X)
        self.b_Y = b_Y - b_X

        #If both points are in the same place, set offset to a big number, so that the line cant ever be used
        if self.m_X == 0 and self.m_Y == 0:
            self.m_Y = 1
            self.b_Y = 10 ** 1000
        elif self.m_X == 0: #If the x multiplier is 0 (line is horizontal), divide offset by y multiplier
            self.b_Y /= self.m_Y
        elif self.m_Y == 0: #If the y multiplier is 0 (line is vertical), divide offset by x multiplier
            self.b_Y /= self.m_X

        #Default fill
        if fill == "#$#":
            fill = pointA.fill

        #Set transform
        tAvg = (pointA.transform + pointB.transform) / 2
        tAvg.primary = self
        super().__init__(tAvg, fill) #Set the origin transform to the average of points


#A basic 2D triangle between 3 points
class Triangle2D(Primary2D):
    #Basic
    a = None
    b = None
    c = None

    #Lines
    l_ab = None
    l_bc = None
    l_ca = None

    #Plot the triangle on a grid
    def Plot (self, grid: Grid, wireframe = False) -> Grid:
        if wireframe: #Only draw wreframe of triangle
            self.l_ab.Plot(grid)
            self.l_bc.Plot(grid)
            self.l_ca.Plot(grid)
        else: #Draw full triangle
            #Get global positions of points
            a_gPos = self.a.transform.globalPosition()
            b_gPos = self.b.transform.globalPosition()
            c_gPos = self.c.transform.globalPosition()

            #Setup arrays
            xArr = [a_gPos.x, b_gPos.x, c_gPos.x] #Array of point x positions
            lArr = [self.l_ab, self.l_bc, self.l_ca] #Array of lines

            #Get X's
            xRight = max(xArr)
            xLeft = min(xArr)
            xArr.remove(xRight)
            xArr.remove(xLeft)
            xMid = xArr[0]

            #Get lines
            lBase = next(l for l in lArr if (l.a.transform.globalPosition().x == xLeft and l.b.transform.globalPosition().x == xRight) or (l.a.transform.globalPosition().x == xRight and l.b.transform.globalPosition().x == xLeft))
            lArr.remove(lBase)
            lLeft = next(l for l in lArr if (l.a.transform.globalPosition().x == xLeft and l.b.transform.globalPosition().x == xMid) or (l.a.transform.globalPosition().x == xMid and l.b.transform.globalPosition().x == xLeft))
            lArr.remove(lLeft)
            lRight = lArr[0]

            #Get line positions
            baseXY_Dict = lBase.GetPlotXYPosDict()
            leftXY_Dict = lLeft.GetPlotXYPosDict()
            rightXY_Dict = lRight.GetPlotXYPosDict()

            # print(lLeft.a.transform.globalPosition(), lLeft.b.transform.globalPosition())

            #-----------New-----------------
            for x in range(grid.xSize):
                if x >= xLeft and x < xMid: #Fill left side
                    llYs = leftXY_Dict[x]
                    lbYs = baseXY_Dict[x]
                    Ys = llYs + lbYs
                    mxY = max(Ys)
                    loY = min(Ys)
                    yRange = range(loY, mxY+1)

                    for y in yRange:
                        grid.Plot(Vector2(x, y), self.fill)
                elif x >= xMid and x <= xRight: #Fill right side
                    lrYs = rightXY_Dict[x]
                    lbYs = baseXY_Dict[x]
                    Ys = lrYs + lbYs
                    mxY = max(Ys)
                    loY = min(Ys)
                    yRange = range(loY, mxY+1)

                    for y in yRange:
                        grid.Plot(Vector2(x, y), self.fill)

            #-----------Old-----------------
            # #Fill triangle
            # for x in range(grid.xSize):
            #     if x >= xLeft and x < xMid:
            #         #Get Y ranges
            #         y_MxLo = [lLeft.GetCoord(x), lBase.GetCoord(x)] #Array of base line y and left line y
            #         yRange = range(min(y_MxLo), max(y_MxLo))

            #         for y in yRange:
            #             grid.plot(Vector2(x, y))
            #     elif x >= xMid and x <= xRight:
            #         #Get Y ranges
            #         y_MxLo = [lRight.GetCoord(x), lBase.GetCoord(x)] #Array of base line y and right line y
            #         yRange = range(min(y_MxLo), max(y_MxLo))

            #         for y in yRange:
            #             grid.plot(Vector2(x, y))


        return grid

    #Initialization
    def __init__(self, pointA: Point2D, pointB: Point2D, pointC: Point2D, fill = "#$#") -> None:
        #Basic
        self.a = pointA
        self.b = pointB
        self.c = pointC

        #Lines
        self.l_ab = Line2D(pointA, pointB, fill)
        self.l_bc = Line2D(pointB, pointC, fill)
        self.l_ca = Line2D(pointC, pointA, fill)

        #Default fill
        if fill == "#$#":
            fill = pointA.fill

        #Set origin transform to average of all points
        tAvg = (pointA.transform + pointB.transform + pointC.transform) / 3
        tAvg.primary = self
        super().__init__(tAvg, fill)
    

#----------------------------Some test code------------------
g = Grid(10, 10, "#", ".")

p0 = Point2D(Transform2D(Vector2(0, 0)))
p1 = Point2D(Transform2D(Vector2(2, 2)))
p2 = Point2D(Transform2D(Vector2(4, 5)))

l1 = Line2D(p2, p1)

l1.Plot(g)
# p0.Plot(g)

g.FlipV()
# print(g)