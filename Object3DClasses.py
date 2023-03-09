#This script contains all 3D primary objects

import math

from MainClasses import *
from Object2DClasses import *
from Transforms import *
from VectorMath import *
from RotationMatrix import *

# A class to hold a list of primaries
class Mesh:
    # Basics
    transform = None
    fill = None
    
    # Ponts, lines and tris
    points = []
    lines = []
    tris = []
    
    #---Presets---
    def cube():
        p1 = Point3D(Transform3D(Vector3(1, 1, 1)), "1")
        p2 = Point3D(Transform3D(Vector3(-1, 1, 1)), "2")
        p3 = Point3D(Transform3D(Vector3(1, -1, 1)), "3")
        p4 = Point3D(Transform3D(Vector3(-1, -1, 1)), "4")
        p5 = Point3D(Transform3D(Vector3(1, 1, -1)), "5")
        p6 = Point3D(Transform3D(Vector3(-1, 1, -1)), "6")
        p7 = Point3D(Transform3D(Vector3(1, -1, -1)), "7")
        p8 = Point3D(Transform3D(Vector3(-1, -1, -1)), "8")
        
        points = [
            p1,
            p2,
            p3,
            p4,
            p5,
            p6,
            p7,
            p8,
        ]
        
        tris = [
            Triangle3D(p1, p2, p3, "#"),
            Triangle3D(p2, p3, p4, "#"),
            Triangle3D(p4, p6, p2, "#"),
            Triangle3D(p4, p6, p8, "#"),
            Triangle3D(p5, p6, p8, "#"),
            Triangle3D(p5, p7, p8, "#"),
            Triangle3D(p1, p5, p7, "#"),
            Triangle3D(p1, p3, p7, "#"),
            Triangle3D(p3, p4, p8, "#"),
            Triangle3D(p3, p7, p8, "#"),
            Triangle3D(p1, p2, p6, "#"),
            Triangle3D(p1, p5, p6, "#"),
        ]
        
        lines = [
            tris[0].l_ab, tris[0].l_bc, tris[0].l_ca,
            tris[1].l_ab, tris[1].l_bc, tris[1].l_ca,
            tris[2].l_ab, tris[2].l_bc, tris[2].l_ca,
            tris[3].l_ab, tris[3].l_bc, tris[3].l_ca,
            tris[4].l_ab, tris[4].l_bc, tris[4].l_ca,
            tris[5].l_ab, tris[5].l_bc, tris[5].l_ca,
            tris[6].l_ab, tris[6].l_bc, tris[6].l_ca,
            tris[7].l_ab, tris[7].l_bc, tris[7].l_ca,
            tris[8].l_ab, tris[8].l_bc, tris[8].l_ca,
            tris[9].l_ab, tris[9].l_bc, tris[9].l_ca,
            tris[10].l_ab, tris[10].l_bc, tris[10].l_ca,
            tris[11].l_ab, tris[11].l_bc, tris[11].l_ca,
        ]
        
        
        return Mesh(Transform3D(), points + lines + tris, check_primary_lists=False)
        
    def sphere():
        pass
    
    #---Initialization---
    def __init__(self, transform = Transform3D.zero(), primaries = [], fill = "#", check_primary_lists = True) -> None:
        self.transform = transform
        self.fill = fill
        for primary in primaries:
            if type(primary).__bases__[0] == Primary3D:
                if type(primary) == Point3D: # If point
                    self.points.append(primary)
                    primary.transform = Transform3D(primary.transform.globalPosition(), primary.transform.globalRotation(), primary.transform.localScale, primary, self.transform, True, True)
                    
                elif type(primary) == Line3D: #If line
                    self.lines.append(primary)
                    
                    if check_primary_lists:
                        #Check if points has all line points
                        if not (primary.a in self.points) and primary.a != None:
                            self.points.append(primary.a)
                            primary.a.transform = Transform3D(primary.a.transform.globalPosition(), primary.a.transform.globalRotation(), primary.a.transform.localScale, primary.a, self.transform, True, True)
                        if not (primary.b in self.points) and primary.b != None: 
                            self.points.append(primary.b)
                            primary.b.transform = Transform3D(primary.b.transform.globalPosition(), primary.b.transform.globalRotation(), primary.b.transform.localScale, primary.b, self.transform, True, True)
                elif type(primary) == Triangle3D: #If triangle
                    self.tris.append(primary)
                    
                    if check_primary_lists:
                        #Check if points has all triangle points
                        if not (primary.l_ab in self.lines) and primary.l_ab != None:
                            self.lines.append(primary.l_ab)
                        if not (primary.l_bc in self.lines) and primary.l_bc != None: 
                            self.lines.append(primary.l_bc)
                        if not (primary.l_ca in self.lines) and primary.l_ca != None: 
                            self.lines.append(primary.l_ca)
                        
                        #Check if lines has all triangle lines
                        if not (primary.a in self.points) and primary.a != None:
                            self.points.append(primary.a)
                            primary.a.transform = Transform3D(primary.a.transform.globalPosition(), primary.a.transform.globalRotation(), primary.a.transform.localScale, primary.a, self.transform, True, True)
                        if not (primary.b in self.points) and primary.b != None: 
                            self.points.append(primary.b)
                            primary.b.transform = Transform3D(primary.b.transform.globalPosition(), primary.b.transform.globalRotation(), primary.b.transform.localScale, primary.b, self.transform, True, True)
                        if not (primary.c in self.points) and primary.c != None: 
                            self.points.append(primary.c)
                            primary.c.transform = Transform3D(primary.c.transform.globalPosition(), primary.c.transform.globalRotation(), primary.c.transform.localScale, primary.c, self.transform, True, True)

#Basic camera to hold FOV and Grid variables
class Camera(Primary3D):
    #Basic variables
    fov = None
    fovAt1 = None #Fov horizontal size from center at 1ut from camera
    grid = None
    minDist = 0.001

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
            for obj in objects:
                if type(obj).__bases__[0] == Primary3D:
                    obj.Plot(self, True) # plot object on cameras grid
        else:
            for obj in objects:
                if type(obj).__bases__[0] == Primary3D:
                    obj.Plot(self, False) # plot object on cameras grid


    #Initialization
    def __init__(self, transform: Transform3D, grid: Grid, FOV: float) -> None:
        #Set variables
        self.fov = FOV
        self.grid = grid

        #Calculate fov at 1ut
        fovRad = math.radians(FOV / 2)
        unitVec = Vector2(math.cos(fovRad), math.sin(fovRad))
        self.fovAt1 = unitVec.y / unitVec.x

        # Round fov at one
        self.fovAt1 = round(self.fovAt1 * 10 ** 10) / 10 ** 10

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
        
        # Vector from camera to point
        cp_vec = camera.transform.globalPosition().vectorTo(self.transform.globalPosition())
        
        # Camera forward vector distance to closest coordinate to point
        cpF_Dist = cp_vec.dot(camera.transform.forward())
        
        # Get the screen center coordinates at point
        screenCenterAtP = camera.transform.globalPosition() + camera.transform.forward() * cpF_Dist

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

        return Point2D(Transform2D(pointGridPos), fill=self.fill), cpF_Dist

        
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
        p2D, zDist = self.ConvertTo2D(camera)
        if zDist >= camera.minDist:
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
        twoD_a, zDist_a = self.a.ConvertTo2D(camera)
        twoD_b, zDist_b = self.b.ConvertTo2D(camera)
        if zDist_a >= camera.minDist and zDist_b >= camera.minDist:
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
    l_ca = None

    #Plotting
    def Plot (self, camera: Camera, wireframe = False):
        twoD_a, zDist_a = self.a.ConvertTo2D(camera)
        twoD_b, zDist_b = self.b.ConvertTo2D(camera)
        twoD_c, zDist_c = self.c.ConvertTo2D(camera)
        
        # Check if a, b and c are not behind the camera
        if zDist_a >= camera.minDist and zDist_b >= camera.minDist and zDist_c >= camera.minDist:
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
        self.l_ca = Line3D(pointC, pointA, fill)

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
# print(camera.grid)