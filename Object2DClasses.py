#This script contains all 2D primary objects

#Imports
from VectorMath import Vector2
from MainClasses import Grid, Primary2D
from Transforms import Transform2D
import math
from mathExt import div, mul, sum, sub


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
    m_X = 1 # Multiplier for X
    # m_Y = 1 # Multiplier for Y

    b_X = 0 # Offset for X
    # b_Y = 0 # Offset for Y

    # Get a coordinate by passing the opposite coordinate
    def GetCoord(self, oppCoord: float, isX = True, raw = False) -> float:
        coord = None # The wanted coordiante

        if isX: # If the passed coordinate is a x coordinate
            if self.m_X == 0:
                coord = self.b_X
            elif abs(self.m_X == float("INF")):
                if oppCoord == self.b_X:
                    coord = float("-INF")
                else:
                    coord = float("INF")
            else:
                coord = self.m_X * oppCoord + self.b_X
        else: # If the passed coordinate is a y coordinate
            if self.m_X == 0:
                if oppCoord == self.b_X:
                    coord = float("-INF")
                else:
                    coord = float("INF")
            elif self.m_X == float("INF"):
                coord = self.b_X
            else:
                coord = (oppCoord - self.b_X) / self.m_X
        # Round?
        # if not raw:
        #     if abs(coord) != float(" inf "):
        coord = round(coord) # Round the coordinate
                    
        return coord

    # Check if the line is steep (>45 degrees)
    def isSteep(self):
        '''
            Check if the line is steep (>45 degrees)
        '''
        return abs(self.m_X) > 1

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
        

        #------ Rasterization ---------
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
            plot_range =  range(loY, mxY+1) if bounded else range(grid.ySize) # Plot range for line
            
            for y in plot_range:
                # Get x coordinate
                xCoord = self.GetCoord(y, False)
                
                # If coord is at infinity
                if xCoord == float("INF"):
                    continue
                
                # Plot
                if xCoord == float("-INF"): # If coordinate is a horizontal line
                    for x in (range(min(a_gPos.x, b_gPos.x), max(a_gPos.x, b_gPos.x)+1) if bounded else grid.xSize): # Plot all coordinates in the line
                        grid.Plot(Vector2(x, y), self.fill)
                    break
                else: # Standard plot
                    grid.Plot(Vector2(xCoord, y), self.fill) #Plot coordinate
        else:
            mxX = max(a_gPos.x, b_gPos.x) #Point in line with highest x
            loX = min(a_gPos.x, b_gPos.x) #Point in line with lowest x
            plot_range =  range(loX, mxX+1) if bounded else range(grid.xSize) # Plot range for line

            for x in plot_range:
                # Get x coordinate
                yCoord = self.GetCoord(x, True)
                
                # If coord is at infinity
                if yCoord == float("INF"):
                    continue
                
                # Plot
                if yCoord == float("-INF"): # If coordinate is a horizontal line
                    for y in (range(min(a_gPos.y, b_gPos.y), max(a_gPos.y, b_gPos.y)+1) if bounded else grid.ySize): # Plot all coordinates in the line
                        grid.Plot(Vector2(x, y), self.fill)
                    break
                else: # Standard plot
                    grid.Plot(Vector2(x, yCoord), self.fill) #Plot coordinate
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

            # Multipliers
        if pointA.transform.globalPosition().x == pointB.transform.globalPosition().x: # If line is vertical
            self.m_X = float("INF")
            self.b_X = pointA.transform.globalPosition().x
        else:
            self.m_X = pA_pB_Vec.y / pA_pB_Vec.x
            # Offset
            self.b_X = self.m_X * -pointA.transform.globalPosition().x + pointA.transform.globalPosition().y
        # print(pointA.transform.globalPosition().x, self.m_X, pointA.transform.globalPosition().y)

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

            # ------------- Newest ----------------
            for x in range(grid.xSize):
                for y in range(grid.ySize):
                    if y >= lBase.GetCoord(x, True): # Check if point is above base
                        # Check if point is between side lines
                        if lLeft.m_X > 0: # If line is ascending
                            if not (y <= lLeft.GetCoord(x, True)): # If point ISN'T outside triangle 
                                continue
                        else:
                            if not (y >= x * lLeft.GetCoord(x, True)): # If point ISN'T outside triangle 
                                continue
                        
                        if lRight.m_X > 0: # If right line is ascending
                            if not (y >= lRight.GetCoord(x, True)): # If point ISN'T outside triangle 
                                continue
                        else:
                            if not (y <= lRight.GetCoord(x, True)): # If point ISN'T outside triangle 
                                continue
                        
                        # Plot
                        grid.Plot(Vector2(x, y), self.fill)
                            
                            
                        

            #-----------New, but Old-----------------
            # for x in range(grid.xSize):
            #     if x >= xLeft and x < xMid: #Fill left side
            #         llYs = leftXY_Dict[x]
            #         lbYs = baseXY_Dict[x]
            #         Ys = llYs + lbYs
            #         mxY = max(Ys)
            #         loY = min(Ys)
            #         yRange = range(loY, mxY+1)

            #         for y in yRange:
            #             grid.Plot(Vector2(x, y), self.fill)
            #     elif x >= xMid and x <= xRight: #Fill right side
            #         lrYs = rightXY_Dict[x]
            #         lbYs = baseXY_Dict[x]
            #         Ys = lrYs + lbYs
            #         mxY = max(Ys)
            #         loY = min(Ys)
            #         yRange = range(loY, mxY+1)

            #         for y in yRange:
            #             grid.Plot(Vector2(x, y), self.fill)

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

def round(num):
    if abs(num) != float(" inf "):
        if num - math.floor(num) < 0.5:
            return math.floor(num)
        else:
            return math.ceil(num)
    return num
            
if __name__ == "__main__":
    g = Grid(10, 10, "#", ".")

    p0 = Point2D(Transform2D(Vector2(7, 1)), "0")
    p1 = Point2D(Transform2D(Vector2(2, 2)), "1")
    p2 = Point2D(Transform2D(Vector2(7, 7)), "2")

    l1 = Line2D(p1, p2, "#")

    t1 = Triangle2D(p0, p1, p2, "#")

    t1.Plot(g)
    # l1.Plot(g)

    p0.Plot(g)
    p1.Plot(g)
    p2.Plot(g)

    g.FlipV()
    print(g)