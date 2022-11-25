#Define grid and camera
from Transforms import *
from Object3DClasses import *
import time


g = Grid(52, 52, "#", " ")
c = Camera(Transform3D(Vector3(0, 4, -1), RMatrix3(-30, 0, 0)), g, 90)

#Define points
pOrigin = Point3D(Transform3D(Vector3(0, 1, 3), RMatrix3(0, 0, 0), Vector3.one() * 2), "|")

p1 = Point3D(Transform3D(Vector3(1, 1, 1), parent=pOrigin, pos_is_global=False), "1")
p2 = Point3D(Transform3D(Vector3(-1, 1, 1), parent=pOrigin, pos_is_global=False), "2")
p3 = Point3D(Transform3D(Vector3(1, -1, 1), parent=pOrigin, pos_is_global=False), "3")
p4 = Point3D(Transform3D(Vector3(-1, -1, 1), parent=pOrigin, pos_is_global=False), "4")
p5 = Point3D(Transform3D(Vector3(1, 1, -1), parent=pOrigin, pos_is_global=False), "5")
p6 = Point3D(Transform3D(Vector3(-1, 1, -1), parent=pOrigin, pos_is_global=False), "6")
p7 = Point3D(Transform3D(Vector3(1, -1, -1), parent=pOrigin, pos_is_global=False), "7")
p8 = Point3D(Transform3D(Vector3(-1, -1, -1), parent=pOrigin, pos_is_global=False), "8")

points = [
    p1,
    p2,
    p3,
    p4,
    p5,
    p6,
    p7,
    p8,
    pOrigin,
]

tris = [
    Triangle3D(p1, p2, p3, "■"),
    Triangle3D(p2, p3, p4, "■"),
    Triangle3D(p4, p6, p2, "■"),
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

for tri in tris:
    tri.fill = "●"

l1 = Line3D(p1, p2, "#")
l2 = Line3D(p2, p4, "#")
l3 = Line3D(p4, p3, "#")
l4 = Line3D(p3, p1, "#")

lines = [
    l1,
    l2,
    l3,
    l4,
]

# c.renderObjects(tris, False)

pA = Point3D(Transform3D(Vector3(0, 0, -3)))
# pA.Plot(c)

for i in range(800):
    pOrigin.transform.localRotation += Vector3.one() * 1
    c.grid.Clear()
    c.renderObjects(tris, True)
    c.grid.FlipH()
    c.grid.FlipV()
    print(c.grid)
    time.sleep(0.01666)