#Python file for testing stuff

import math

from VectorMath import Vector2, Vector3

x = 56.5
y = 26.1
z = 25.2

x = math.radians(x)
y = math.radians(y)
z = math.radians(z)

xUp = math.cos(y) * math.sin(z)

y0yUp = math.sin(x + math.pi / 2) * math.sin(z + math.pi / 2)
y90yUp = math.cos(x + z)
yUp = y0yUp + (y90yUp - y0yUp) * math.sin(y)

y0zUp = math.cos(x + math.pi/2) * math.cos(z)
y90zUp = math.cos(x + z + math.pi/2)
zUp = y0zUp + (y90zUp - y0zUp) * math.sin(y)



class testParent:
    x=0
    def __init__(self) -> None:
        self.x=1

class test(testParent):
    def __init__(self) -> None:
        super().__init__()

t = test()
print(t.__bases__)