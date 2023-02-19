from Object3DClasses import *
from MainClasses import *

g = Grid(50, round(50/16*9))
c = Camera(Transform3D(), g, 90)

p = Point3D(Transform3D(Vector3(0, 0, -1)))

p.Plot(c)

print(g, p.ConvertTo2D(c))