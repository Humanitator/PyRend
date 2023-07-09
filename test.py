import math

from Object3DClasses import *
from MainClasses import *

g = Grid(50, round(50/16*9))
c = Camera(Transform3D(Vector3(0, 0, -3), rotation=RMatrix3(0, 0, 0)), g, 100)

pC = Point3D(Transform3D(Vector3(0, 0, 3), RMatrix3(0, 0, 0)))
p = Point3D(Transform3D(Vector3(1, -1, -1), parent=pC), fill="0")
p1 = Point3D(Transform3D(Vector3(-1, -1, -1), parent=pC), fill="1")
p2 = Point3D(Transform3D(Vector3(-1, -1, 1), parent=pC), fill="2")
p3 = Point3D(Transform3D(Vector3(1, -1, 1), parent=pC), fill="3")

pv = Point3D(Transform3D(), "0")
pv1 = Point3D(Transform3D(Vector3(0, 1, 0)), "1")
lv = Line3D(pv, pv1, "#")

l = Line3D(p, p1)
l1 = Line3D(p1, p2)
l2 = Line3D(p2, p3)
l3= Line3D(p3, p)

points = [
    p, p1, p2, p3
]

lines = [
    l, l1, l2, l3
]

v_points = [
    pv, pv1
]
v_line = [
    lv
]

cube = Mesh.cube(scale=1)
cube.Render(c, render_type=1, wireframe=False)
# c.renderObjects(points, True)

g.FlipV()
print(g)