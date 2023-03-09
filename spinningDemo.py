#Define grid and camera
from Transforms import *
from Object3DClasses import *
import time
import curses
from curses import wrapper

# xSize = 30
# ySize = round(xSize / 16 * 9)

xSize = round(float(input(f"Enter width (Default: ): ")))
ySize = round(xSize / 16 * 9)

# g = Grid(52, 52, "#", " ") # For smaller terminal
g = Grid(xSize, ySize, "#", " ") # For small letters
cOrigin = Point3D(Transform3D(Vector3(0, 0, 0)))
c = Camera(Transform3D(Vector3(0, 2.5, -4), RMatrix3(-30, 0, 0), parent=cOrigin), g, 90)

#Define points
pOrigin = Point3D(Transform3D(Vector3(0, 0, 0), RMatrix3(0, 0, 0), Vector3.one() * 1.3), "|")

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
l2 = Line3D(p1, p3, "#")
l3 = Line3D(p1, p5, "#")
l4 = Line3D(p2, p4, "#")
l5 = Line3D(p2, p6, "#")
l6 = Line3D(p3, p4, "#")
l7 = Line3D(p3, p7, "#")
l8 = Line3D(p8, p6, "#")
l9 = Line3D(p8, p7, "#")
l10 = Line3D(p8, p4, "#")
l11 = Line3D(p6, p5, "#")
l12 = Line3D(p7, p5, "#")


lines = [
    l1,
    l2,
    l3,
    l4,
    l5,
    l6,
    l7,
    l8,
    l9,
    l10,
    l11,
    l12
]

for line in lines:
    line.fill = "●"

# c.renderObjects(tris, False)

pA = Point3D(Transform3D(Vector3(0, 0, -3)))
# pA.Plot(c)

def main(stdscr):
    stdscr.nodelay(True)
    for i in range(800):
        # ---Input---
        # try:
        #     key = stdscr.getkey()
        # except:
        #     key = "None"
        
        #---Code---
        # prints = ""
        # sensitivity = 0.1
        # rotMul = 10
        # if key == "w":
        #     c.transform.localPosition += c.transform.up() * sensitivity
        # elif key == "a":
        #     c.transform.localPosition += c.transform.right() * sensitivity
        # elif key == "s":
        #     c.transform.localPosition -= c.transform.up() * sensitivity
        # elif key == "d":
        #     c.transform.localPosition -= c.transform.right() * sensitivity
        # elif key == "q":
        #     c.transform.localPosition -= c.transform.forward() * sensitivity
        # elif key == "e":
        #     c.transform.localPosition += c.transform.forward() * sensitivity
        # elif key == "KEY_LEFT":
        #     cOrigin.transform.localRotation.y += sensitivity * rotMul
        # elif key == "KEY_RIGHT":
        #     cOrigin.transform.localRotation.y -= sensitivity * rotMul
        
        # ---Clear screen---
        stdscr.clear()
        
        # ---Wait---
        time.sleep(0.02)
        
        # ---Render---
        t = time.time()
        pOrigin.transform.localRotation += Vector3.one() * 1
        # pOrigin.transform.localPosition.y = math.sin(t) * 2
        c.grid.Clear()
        c.renderObjects(lines, True)
        c.grid.FlipH()
        c.grid.FlipV()
        
        # ---Add text---
        try:
            stdscr.addstr(str(c.grid))
        except:
            stdscr.clear()
            stdscr.addstr("Window too small! Please choose a smaller width or make the window bigger!")
        # stdscr.addstr(key + "; " + prints)
        
        # ---Refresh---
        stdscr.refresh()
    
wrapper(main)