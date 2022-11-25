#This script contains all 3D primary objects

import math

from MainClasses import *
from Object2DClasses import *
from Transforms import *
from VectorMath import Vector2, Vector3
from RotationMatrix import *

#Basic camera to hold FOV and Grid variables
class Camera(Primary3D):
    #Basic variables
    fov = None
    fovAt1 = None #Fov horizontal size from center at 1ut from camera
    grid = None

    # Sort objects by distance from camera from farthest to closest
    def sortObjByDist(self, objects: list, uselocalPos = False) -> list:
        arr = objects.copy()
        sortedArr = [arr[0]]
        arr.pop(0)
        for obj in arr:
            if type(obj).__bases__[0] == Primary3D:
                for i in range(len(arr)):
                    if uselocalPos:
                        if abs(sortedArr[i].transform.localPosition) <= abs(obj.transform.localPosition):
                            sortedArr.insert(i, obj)
                            break
                    else:
                        if abs(sortedArr[i].transform.globalPosition()) <= abs(obj.transform.globalPosition()):
                            sortedArr.insert(i, obj)
                            break
        return sortedArr


    # Render the whole scene
    def renderObjects(self, objects = [], wireframe = False):
        if wireframe:
            for object in objects:
                if type(object).__bases__[0] == Primary3D:
                    object.Plot(self, True) # plot object on cameras grid
        else:
            for object in objects:
                if type(object).__bases__[0] == Primary3D:
                    object.Plot(self, False) # plot object on cameras grid


    #Initialization
    def __init__(self, transform: Transform3D, grid: Grid, FOV: float) -> None:
        #Set variables
        self.fov = FOV
        self.grid = grid

        #Calculate fov at 1ut
        fovRad = math.radians(FOV / 2)
        unitVec = Vector2(math.cos(fovRad), math.sin(fovRad))
        self.fovAt1 = unitVec.y / unitVec.x

        if self.fovAt1 > 0.99: #Round the fov to 1 if its close enough
            self.fovAt1 = 1

        #Setup transform
        transform.primary = self

        #Set primary transform variable
        super().__init__(transform, " ")

#A basic point with just a transform
class Point3D(Primary3D):

    #Calculate point coordinates from 3D space to 2D space
    def ConvertTo2D(self, camera: Camera) -> Point2D:
        #Calculate camera's vertical FOV
        camYX_ratio = camera.grid.ySize / camera.grid.xSize
        verticalFovAt1 = camera.fovAt1 * camYX_ratio

        # Get basic variables
        cp_vec = camera.transform.globalPosition().vectorTo(self.transform.globalPosition()) #Vector from camera to point
        cpF_Dist = cp_vec.dot(camera.transform.forward()) #Camera forward distance to closest coordinate to point
        screenCenterAtP = camera.transform.globalPosition() + camera.transform.forward() * cpF_Dist # Get the screen center coordinates at point

        screenSizeX_atP = camera.fovAt1 * cpF_Dist #Screen Y size from center at point distance
        screenSizeY_atP = verticalFovAt1 * cpF_Dist #Screen Y size from center at point distance

        pixelPerUnit = camera.grid.xSize / (screenSizeX_atP * 2) # Pixels in one unit at point

        # Calculate the screen's left-bottom corner position. Called -- (Negative-Negative) corner
        screenCorner_NN = screenCenterAtP - (camera.transform.right() * screenSizeX_atP) - (camera.transform.up() * screenSizeY_atP)

        # Calculate point position in world screen
        NN_point_vec = screenCorner_NN.vectorTo(self.transform.globalPosition())
        pointWorldX = NN_point_vec.dot(camera.transform.right())
        pointWorldY = NN_point_vec.dot(camera.transform.up())

        #Convert world coordinates to grid coordinates
        pointGridX = round(pointWorldX * pixelPerUnit)
        pointGridY = round(pointWorldY * pixelPerUnit)
        pointGridPos = Vector2(pointGridX, pointGridY)
        # print(pointGridPos)

        return Point2D(Transform2D(pointGridPos), fill=self.fill)

        
        # --Old conversion code--

        # cp_vec = camera.transform.globalPosition().vectorTo(self.transform.globalPosition()) #Vector from camera to point
        # cpF_Dist = cp_vec.dot(camera.transform.forward()) #Camera forward distance to closest coordinate to point
        # screenSizeAtPoint = cpF_Dist * camera.fovAt1 * 2
        # px_in_ut_at_point = camera.grid.xSize / screenSizeAtPoint

        # #Calculate screen -- (3rd quadrant) corner coords at point
        # cpF_vec = camera.transform.globalPosition() + camera.transform.forward() * cpF_Dist #Screen center coordinate at point
        # screen_MM_vec = cpF_vec + -camera.transform.right() * camera.fovAt1 * cpF_Dist + -camera.transform.up() * camera.fovAt1 * cpF_Dist
        # MM_p_vec = screen_MM_vec.vectorTo(self.transform.globalPosition())
        
        # #Calculate point position in ut
        # p2Dpos_ut = Vector2(MM_p_vec.dot(camera.transform.right()), MM_p_vec.dot(camera.transform.up()))

        # #Calculate point position in px
        # p2Dpos_px = p2Dpos_ut * px_in_ut_at_point

        # return Point2D(Transform2D(Vector2(round(p2Dpos_px.x) - 1, round(p2Dpos_px.y) - 1)), self.fill)


    #Plotting the point on a grid
    def Plot(self, camera: Camera, wireframe = False):
        p2D = self.ConvertTo2D(camera)
        camera.grid.Plot(p2D.transform.globalPosition(), self.fill)

    #Initialization
    def __init__(self, transform = Transform3D(), fill = "#") -> None:
        #Setup transform
        transform.primary = self

        transform.primary = self
        super().__init__(transform, fill)


#A basic line from a to b
class Line3D(Primary3D):
    #Basic variables
    a = None
    b = None

    #Geometry
    m_X = None #X multiplier
    m_Y = None #Y multiplier
    m_Z = None #Z multiplier

    b_X = None #X offset
    b_Y = None #Y offset
    b_Z = None #Z offset

    # Plot the line to a grid
    def Plot (self, camera: Camera, wireframe = False):
        twoD_a = self.a.ConvertTo2D(camera)
        twoD_b = self.b.ConvertTo2D(camera)
        lineTwoD = Line2D(twoD_a, twoD_b, self.fill)
        lineTwoD.Plot(camera.grid, True)

    #Initialization
    def __init__(self, pointA: Point3D, pointB: Point3D, fill = "#$#") -> None:
        #Set a and b points
        self.a = pointA
        self.b = pointB

        #Set geometry variables
        pA_pB_Vec = pointA.transform.globalPosition().vectorTo(pointB.transform.globalPosition()) #Direction vector from a to b

            #Set multipliers
        self.m_X = pA_pB_Vec.x
        self.m_Y = pA_pB_Vec.y
        self.m_Z = pA_pB_Vec.z

            #Set offsets
        self.b_X = 2 * pointA.transform.globalPosition().x
        self.b_Y = -(2 * pointA.transform.globalPosition().y)
        self.b_Z = pointA.transform.globalPosition().z

        if fill == "#$#":
            fill = pointA.fill

        #Set the line's transform to the average of the points
        tAvg = (pointA.transform + pointB.transform) / 2
        tAvg.primary = self
        super().__init__(tAvg, fill)


#A basic tringle between 3 points
class Triangle3D(Primary3D):
    # Points
    a = None
    b = None
    c = None

    # Lines
    l_ab = None
    l_bc = None
    l_cd = None

    #Plotting
    def Plot (self, camera: Camera, wireframe = False):
        twoD_a = self.a.ConvertTo2D(camera)
        twoD_b = self.b.ConvertTo2D(camera)
        twoD_c = self.c.ConvertTo2D(camera)
        tri2D = Triangle2D(twoD_a, twoD_b, twoD_c, self.fill)

        if wireframe:
            tri2D.Plot(camera.grid, True)
        else:
            tri2D.Plot(camera.grid)

    #Initialization
    def __init__(self, pointA: Point3D, pointB: Point3D, pointC: Point3D, fill = "#$#") -> None:
        # Setting points
        self.a = pointA
        self.b = pointB
        self.c = pointC

        # Setting lines
        self.l_ab = Line3D(pointA, pointB, fill)
        self.l_bc = Line3D(pointB, pointC, fill)
        self.l_cd = Line3D(pointC, pointA, fill)

        if fill == "#$#":
            fill = pointA.fill

        #Set origin transform to average of all points
        tAvg = (pointA.transform + pointB.transform + pointC.transform) / 3
        tAvg.primary = self
        super().__init__(tAvg, fill)

# Test code
# ...

g = Grid(9, 9, "#", ".")
camera = Camera(Transform3D(Vector3.zero(), RMatrix3.zero()), g, 90)

a = Point3D(Transform3D(Vector3(0, 0, 10)))

a.Plot(camera)
camera.grid.FlipH()
camera.grid.FlipV()
print(camera.grid)