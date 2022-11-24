# This script contains all needed classes for complex and unusual math like vectors and functions

#Imports
import math
from typing_extensions import Self


# -----------------Vector2-----------------
class Vector2:
    x = None
    y = None

    #-----Exclusive math------
   #Round vector
    def round(self, round_to = 0) -> Self:
        return Vector2(round(self.x * 10 ** round_to) / 10 ** round_to, round(self.y * 10 ** round_to) / 10 ** round_to)

    #Vector from self to other
    def vectorTo (self, other: Self) -> Self:
        return other - self

    #Length of vector
    def magnitude (self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    #Unit vector
    def normalized (self) -> Self:
        m = self.magnitude()
        if m > 0:
            return Vector2(self.x / m, self.y / m)

    #Dot product
    def dot (self, vec: Self) -> float:
        return self.x * vec.x + self.y * vec.y

    #Angle between self and other vector
    def angle(self, other: Self):
        return math.acos(self.dot(other) / self.magnitude() * other.magnitude())

    #Convert from radians to degrees
    def degrees(self):
        return Vector2(math.degrees(self.x), math.degrees(self.y))

    #Convert from degrees to radians
    def radians(self):
        return Vector2(math.radians(self.x), math.radians(self.y))

    #-----Specials-----

        #---Math---

    # Add
    def __add__ (self, other: Self) -> Self:
        return Vector2(self.x + other.x, self.y + other.y)

    # Subtract
    def __sub__ (self, other: Self) -> Self:
        return Vector2(self.x - other.x, self.y - other.y)

    # Multiply
    def __mul__ (self, other) -> Self:
        if type(other) == Vector2:
            return Vector2(self.x * other.x, self.y * other.y)
        else:
            return Vector2(self.x * other, self.y * other)

    # Divide
    def __truediv__ (self, other) -> Self:
        if type(other) == Vector2:
            return Vector2(self.x / other.x, self.y / other.y)
        else:
            return Vector2(self.x / other, self.y / other)

    # Floor divide
    def __floordiv__ (self, other) -> Self:
        if type(other) == Vector2:
            return Vector2(self.x // other.x, self.y // other.y)
        else:
            return Vector2(self.x // other, self.y // other)

    # Power
    def __pow__ (self, other) -> Self:
        if type(other) == Vector2:
            return Vector2(self.x ** other.x, self.y ** other.y)
        else:
            return Vector2(self.x ** other, self.y ** other)

    # Negative
    def __neg__ (self) -> Self:
        return Vector2(-self.x, -self.y)

    # Absolute
    def __abs__ (self) -> Self:
        return Vector2(abs(self.x), abs(self.y))
    
        #---Comparison---

    # Less
    def __lt__ (self, other: Self) -> bool:
        if self.x < other.x and self.y < other.y:
            return True
        else:
            return False
    
    # Less or equal
    def __le__ (self, other: Self) -> bool:
        if self.x <= other.x and self.y <= other.y:
            return True
        else:
            return False

    # Greater
    def __gt__ (self, other: Self) -> bool:
        if self.x > other.x and self.y > other.y:
            return True
        else:
            return False

    # Greater or equal
    def __ge__ (self, other: Self) -> bool:
        if self.x >= other.x and self.y >= other.y:
            return True
        else:
            return False
    
    # Equal
    def __eq__ (self, other: Self) -> bool:
        if (self.x == other.x and self.y == other.y):
            return True
        else:
            return False

    # Not equal
    def __ne__(self, other: Self) -> bool:
        if self.x != other.x and self.y != other.y:
            return True
        else:
            return False

        #---Other---

    # Convert to string
    def __str__(self) -> str:
        return f"({self.x}; {self.y})"

    #---Initialization---
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

        #---Special initialization presets---
    def zero ():
        return Vector2(0, 0)
    def one ():
        return Vector2(1, 1)
    def right ():
        return Vector2(1, 0)
    def up ():
        return Vector2(0, 1)



# ----------------Vector3----------------
class Vector3:
    x = None
    y = None
    z = None

    #-----Exclusive math------

    #Round vector
    def round(self, round_to = 0) -> Self:
        return Vector3(round(self.x * 10 ** round_to) / 10 ** round_to, round(self.y * 10 ** round_to) / 10 ** round_to, round(self.z * 10 ** round_to) / 10 ** round_to)

    #Vector between self and other
    def vectorTo (self, other: Self) -> Self:
        return other - self

    #Length of vector
    def magnitude (self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    #Unit vector
    def normalized (self) -> Self:
        m = self.magnitude()
        if m > 0:
            return Vector3(self.x / m, self.y / m, self.z / m)

    #Dot product
    def dot (self, vec: Self) -> float:
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    #Angle between self and other
    def angle(self, other: Self):
        return math.acos(self.dot(other) / self.magnitude() * other.magnitude())

    #Cross product
    def cross(self, other: Self):
        return Vector3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x)

    #Convert from radians to degrees
    def degrees(self):
        return Vector3(math.degrees(self.x), math.degrees(self.y), math.degrees(self.z))

    #Convert from degrees to radians
    def radians(self):
        return Vector3(math.radians(self.x), math.radians(self.y), math.radians(self.z))

    #-----Specials-----

        #---Math---

    # Add
    def __add__ (self, other: Self) -> Self:
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    # Subtract
    def __sub__ (self, other: Self) -> Self:
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    # Multiply
    def __mul__ (self, other) -> Self:
        if type(other) == Vector3:
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector3(self.x * other, self.y * other, self.z * other)

    # Divide
    def __truediv__ (self, other) -> Self:
        if type(other) == Vector3:
            return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector3(self.x / other, self.y / other, self.z / other)

    # Floor divide
    def __floordiv__ (self, other) -> Self:
        if type(other) == Vector3:
            return Vector3(self.x // other.x, self.y // other.y, self.z // other.z)
        else:
            return Vector3(self.x // other, self.y // other, self.z // other)

    # Power
    def __pow__ (self, other) -> Self:
        if type(other) == Vector3:
            return Vector3(self.x ** other.x, self.y ** other.y, self.z ** other.z)
        else:
            return Vector3(self.x ** other, self.y ** other, self.z ** other)

    # Negative
    def __neg__ (self) -> Self:
        return Vector3(-self.x, -self.y, -self.z)

    # Absolute
    def __abs__ (self) -> Self:
        return Vector3(abs(self.x), abs(self.y), abs(self.z))
    
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
    def __ge__ (self, other: Self) -> bool:
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

    #---Initialization---
    def __init__(self, x, y, z) -> None:
        self.x = x
        self.y = y
        self.z = z

    #---Special initialization presets---
    def zero ():
        return Vector3(0, 0, 0)
    def one ():
        return Vector3(1, 1, 1)
    def right ():
        return Vector3(1, 0, 0)
    def up ():
        return Vector3(0, 1, 0)
    def front ():
        return Vector3(0, 0, 1)

# Test code
# ...