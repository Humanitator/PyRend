#This script is a host to the rotation matrix class
import math

from typing_extensions import Self

from VectorMath import Vector2, Vector3

class RMatrix3:
    x = 0
    y = 0
    z = 0

    #---Exclusive math---

    #Local rotation between 2 rotations
    def local(self, other):
        return other - self

    #Round matrix
    def round(self, round_to = 0):
        return RMatrix3(round(self.x * 10 ** round_to) / 10 ** round_to, round(self.y * 10 ** round_to) / 10 ** round_to, round(self.z * 10 ** round_to) / 10 ** round_to)

    #Convert rotation from degrees to radians
    def radians(self):
        return RMatrix3(math.radians(self.x), math.radians(self.y), math.radians(self.z))

    #Convert to a 3D unit vector
    def toNormalV3 (self, roundVector = True, round_to = 10) -> Vector3:
        vX = Vector3(0, math.sin(math.radians(self.x)), math.cos(math.radians(self.x))) # Calculate vector rotated around X axis
        vY = Vector3(math.sin(math.radians(self.y)), math.cos(math.radians(self.y)) * vX.y, math.cos(math.radians(self.y)) * vX.z) # Calculate vector that's also rotated around it's local Y axis
        if roundVector:
            vY = vY.round(round_to)
        return vY

    #-----Specials-----

        #---Math---

    # Add
    def __add__ (self, other: Self) -> Self:
        return RMatrix3(self.x + other.x, self.y + other.y, self.z + other.z)

    # Subtract
    def __sub__ (self, other: Self) -> Self:
        return RMatrix3(self.x - other.x, self.y - other.y, self.z - other.z)

    # Multiply
    def __mul__ (self, other) -> Self:
        if type(other) == RMatrix3:
            return RMatrix3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return RMatrix3(self.x * other, self.y * other, self.z * other)

    # Divide
    def __truediv__ (self, other) -> Self:
        if type(other) == Vector3:
            return RMatrix3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return RMatrix3(self.x / other, self.y / other, self.z / other)

    # Floor divide
    def __floordiv__ (self, other) -> Self:
        if type(other) == Vector3:
            return RMatrix3(self.x // other.x, self.y // other.y, self.z // other.z)
        else:
            return RMatrix3(self.x // other, self.y // other, self.z // other)

    # Power
    def __pow__ (self, other) -> Self:
        if type(other) == Vector3:
            return RMatrix3(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        else:
            return RMatrix3(self.x ** other, self.y ** other, self.z ** other)

    # Negative
    def __neg__ (self) -> Self:
        return RMatrix3(-self.x, -self.y, -self.z)

    # Absolute
    def __abs__ (self) -> Self:
        return RMatrix3(abs(self.x), abs(self.y), abs(self.z))
    
        #---Comparison---

    # Less
    def __lt__ (self, other: Self) -> bool:
        if self.x < other.x and self.y < other.y and self.z < other.z:
            return True
        else:
            return False
    
    # Less or equal
    def __le__ (self, other: Self) -> bool:
        if self.x <= other.x and self.y <= other.y and self.z <= other.z:
            return True
        else:
            return False

    # Greater
    def __gt__ (self, other: Self) -> bool:
        if self.x > other.x and self.y > other.y and self.z > other.z:
            return True
        else:
            return False

    # Greater or equal
    def __gt__ (self, other: Self) -> bool:
        if self.x >= other.x and self.y >= other.y and self.z >= other.z:
            return True
        else:
            return False
    
    # Equal
    def __eq__ (self, other: Self) -> bool:
        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True
        else:
            return False

    # Not equal
    def __ne__(self, other: Self) -> bool:
        if self.x != other.x and self.y != other.y and self.z != other.z:
            return True
        else:
            return False


    #---Other---

    # Convert to string
    def __str__(self) -> str:
        return f"({self.x}; {self.y}; {self.z})"

    #Initialization
    def __init__(self, x = 0.0, y = 0.0, z = 0.0, in_degrees = True) -> None:
        if in_degrees:
            self.x = x
            self.y = y
            self.z = z
        else:
            self.x = math.degrees(x)
            self.y = math.degrees(y)
            self.z = math.degrees(z)

    #---Special initialization presets---

    #Create rotation matrix from vector
    def fromV3(vector : Vector3, roundMatrix = True, round_to = 10) -> Self:
        vector = vector.normalized()
        mrY = math.degrees(math.asin(vector.x))
        mrX = math.degrees(math.asin(vector.y / math.cos(math.radians(mrY))))
        
        if roundMatrix:
            mrY = round(mrY * 10 ** round_to) / 10 ** round_to
            mrX = round(mrX * 10 ** round_to) / 10 ** round_to
            
        return RMatrix3(mrX, mrY, 0)

    def zero ():
        return RMatrix3(0, 0, 0)
    def right ():
        return RMatrix3(0, 90, 0)
    def up ():
        return RMatrix3(90, 0, 0)
    def front ():
        return RMatrix3(0, 0, 0)

#Test code
r3 = RMatrix3(45, 35.2643896828, 0)
v3 = r3.toNormalV3()

vA = Vector3(1, 0, 0)
rA = RMatrix3.up().toNormalV3()
# print(rA)

'''
1. sin(r3.y) = 0.5773502691896257
2. 
'''
