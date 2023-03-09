#This script contains all stuff asociated with 3D transforms (position, forward(), etc.).

#Imports
import math
import sys

from typing_extensions import Self

from RotationMatrix import RMatrix3
from VectorMath import Vector2, Vector3


#A basic 3D transform with position and rotation
class Transform2D:
    #Basic variables
    localPosition = Vector2.zero()
    localRotation = 0.0
    localScale = Vector2.one()

    #Hierarchy variables
    primary = None
    parent = None

    #---------Exclusive math----------------

    #The global position of the transform
    def globalPosition(self, MaxIterations = 5000, ignoreTimeout = False, gPos = Vector2.zero(), iteration = 0, start = None) -> Vector2:
        if start == None:
            start = self

        # Check if too many recursions
        if not ignoreTimeout:
            iteration += 1
            if iteration > MaxIterations:
                sys.exit(f"Iteration limit reached! Too many iterations when getting global position for {start.primary} ({start}). Maybe a loop in parents...")

        if self.parent == None: # return start position
            return self.localPosition
        else: # Recurse
            gPos += self.parent.globalPosition(MaxIterations, ignoreTimeout, gPos, iteration, start) + (self.parent.right() * self.localPosition.x +                        # Add relative global x position
                                                                                                        self.parent.up() * self.localPosition.y) * self.parent.localScale   # Add relative global y position
        return gPos

    #The global rotation of the transform
    def globalRotation(self, MaxIterations = 5000, ignoreTimeout = False) -> float:        
        gRot = self.localRotation
        parent = self.parent
        iteration = 0
        while True:
            if parent == None:
                return gRot

            gRot += parent.localRotation
            parent = parent.parent
            if not ignoreTimeout:
                iteration += 1
                if iteration > MaxIterations:
                    sys.exit(f"Iteration limit reached! Too many iterations when getting global rotation for {self.primary} ({self}). Maybe a loop in parents...")


    # The unit vector of the rotation
    def up(self):
        # EZ
        return Vector2(math.cos(self.localRotation), math.sin(self.localRotation))

    #The right perpendicular unit vector of this transform
    def right(self):
        # EZ
        # 2D on top
        fwd = self.forward()
        return Vector2(fwd.y, -fwd.x)

    #---------Specials------------
        #---Math---
     # Add
    def __add__ (self, other: Self) -> Self:
        return Transform2D(self.localPosition + other.localPosition, self.localRotation + other.localRotation)

    # Subtract
    def __sub__ (self, other: Self) -> Self:
        return Transform2D(self.localPosition - other.localPosition, self.localRotation - other.localRotation)

    # Multiply
    def __mul__ (self, other) -> Self:
        if type(other) == Transform2D:
            return Transform2D(self.localPosition * other.localPosition, self.localRotation * other.localRotation)
        else:
            return Transform2D(self.localPosition * other, self.localRotation * other)

    # Divide
    def __truediv__ (self, other) -> Self:
        if type(other) == Transform2D:
            return Transform2D(self.localPosition / other.localPosition, self.localRotation / other.localRotation)
        else:
            return Transform2D(self.localPosition / other, self.localRotation / other)

    # Floor divide
    def __floordiv__ (self, other) -> Self:
        if type(other) == Transform2D:
            return Transform2D(self.localPosition // other.localPosition, self.localRotation // other.localRotation)
        else:
            return Transform2D(self.localPosition // other, self.localRotation // other)

    # Power
    def __pow__ (self, other) -> Self:
        if type(other) == Transform2D:
            return Transform2D(self.localPosition ** other.localPosition, self.localRotation ** other.localRotation)
        else:
            return Transform2D(self.localPosition ** other, self.localRotation ** other)

    # Negative
    def __neg__ (self) -> Self:
        return Transform2D(-self.localPosition, -self.localRotation)

    # Absolute
    def __abs__ (self) -> Self:
        return Transform2D(abs(self.localPosition), abs(self.localRotation))
    
        #---Comparison---

    # Smaller
    def __lt__ (self, other: Self):
        if self.localPosition < other.localPosition and self.localRotation < other.localRotation:
            return True
        else:
            return False
    
    # Smaller or equal
    def __le__ (self, other: Self) -> bool:
        if self.localPosition <= other.localPosition and self.localRotation <= other.localRotation:
            return True
        else:
            return False

    # Greater
    def __gt__ (self, other: Self) -> bool:
        if self.localPosition > other.localPosition and self.localRotation > other.localRotation:
            return True
        else:
            return False

    # Greater or equal
    def __ge__ (self, other: Self) -> bool:
        if self.localPosition >= other.localPosition and self.localRotation >= other.localRotation:
            return True
        else:
            return False
    
    # Equal
    def __eq__ (self, other: Self) -> bool:
        if self.localPosition == other.localPosition and self.self.localRotation == other.localRotation:
            return True
        else:
            return False

    # Not equal
    def __ne__(self, other: Self) -> bool:
        if self.localPosition == other.localPosition and self.self.localRotation == other.localRotation:
            return True
        else:
            return False

        #---Other---
    def __str__(self) -> str:
        return f"({self.localPosition}; {self.forward()})"
    
    #---Presets---
    def zero():
        return Transform3D()

    #---Initialization---
    def __init__(self, position = Vector2.zero(), rotationDegrees = 0.0, localScale = Vector2.one(), primary = None, parent = None) -> None:
        #Basics
        self.localPosition = position
        self.localRotation = rotationDegrees
        self.localScale = localScale

        # Hierarchy
        self.parent = parent
        self.primary = primary



#A basic 3D transform with position and rotation
class Transform3D:
    #Basic variables
    localPosition = Vector3.zero()
    localRotation = RMatrix3.zero()
    localScale = Vector3.one()

    #Hierarchy variables
    primary = None
    parent = None

    #-----------------Exclusive math----------------------

    #The global position of the transform
    def globalPosition(self, MaxIterations = 5000, ignoreTimeout = False, gPos = Vector3.zero(), iteration = 0, start = None) -> Vector3:
        if start is not None:
            start = self

        # Check if too many recursions
        if not ignoreTimeout:
            iteration += 1
            if iteration > MaxIterations:
                sys.exit(f"Iteration limit reached! Too many iterations when getting global position for {start.primary} ({start}). Maybe a loop in parents...")

        if self.parent is None: # return start position if world is parent
            return self.localPosition
        else: # Recurse
            gPos += self.parent.globalPosition(MaxIterations, ignoreTimeout, gPos, iteration, start) + (self.parent.right() * self.localPosition.x +                            # Add relative global x position
                                                                                                        self.parent.up() * self.localPosition.y +                               # Add relative global y position
                                                                                                        self.parent.forward() * self.localPosition.z) * self.parent.localScale  # Add relative global z position
        return gPos
        

    #The global rotation of the transform
    def globalRotation(self, MaxIterations = 5000, ignoreTimeout = False) -> RMatrix3:        
        gRot = self.localRotation
        parent = self.parent
        iteration = 0
        while True:
            if type(parent) == type(None):
                return gRot

            gRot += parent.localRotation
            parent = parent.parent
            if not ignoreTimeout:
                iteration += 1
                if iteration > MaxIterations:
                    sys.exit(f"Iteration limit reached! Too many iterations when getting global rotation for {self.primary} ({self}). Maybe a loop in parents...")


    #The unit vector of the rotation
    def forward(self) -> Vector3:
        if type(self.localRotation) == RMatrix3:
            # Easy enough
            return self.globalRotation().toNormalV3()

    # The up perpendicular unit vector
    def up(self, round_to = 10, roundVector = True) -> Vector3:
        if type(self.localRotation) == RMatrix3:
            # This shit took way too long.
            # Fuck gimball lock

            gRot = self.globalRotation()
            gRot = gRot.radians()

            #Calculate X coordinate
            Vx = math.cos(gRot.y) * math.sin(gRot.z)

            # Calculate Y coordinate 
            SinX_SinZ = math.cos(gRot.x) * math.cos(gRot.z)
            Cos_xz = math.cos(gRot.x + gRot.z)
            Vy = SinX_SinZ + math.sin(gRot.y) * (Cos_xz - SinX_SinZ)

            # Calculate Z coordinate
            Cos_xp90_z = math.cos(gRot.x + math.pi/2) * math.cos(gRot.z)
            Cos_xzp90 = math.cos(gRot.x + gRot.z + math.pi/2)
            Vz = Cos_xp90_z + math.sin(gRot.y) * (Cos_xzp90 - Cos_xp90_z)

            vUp = Vector3(Vx, Vy, Vz)

            if roundVector:
                vUp = vUp.round(round_to)

            #Return vector
            return vUp

    # The right perpendicular unit vector
    def right(self, round_to = 10, roundVector = True) -> Vector3:
        if type(self.localRotation) == RMatrix3:
            # The right perpendicular vector is just the up perpendicular vector rotated by 90 degrees on Z axis
            # Well this was easy...
            rightTransform = Transform3D(Vector3.zero(), RMatrix3(self.localRotation.x, self.localRotation.y, self.localRotation.z + 90))
            return rightTransform.up()


    #---------Specials------------
        #---Math---
    # Add
    def __add__ (self, other: Self) -> Self:
        return Transform3D(self.localPosition + other.localPosition, self.localRotation + other.localRotation)

    # Subtract
    def __sub__ (self, other: Self) -> Self:
        return Transform3D(self.localPosition - other.localPosition, self.localRotation - other.localRotation)

    # Multiply
    def __mul__ (self, other) -> Self:
        if type(other) == Transform3D:
            return Transform3D(self.localPosition * other.localPosition, self.localRotation * other.localRotation)
        else:
            return Transform3D(self.localPosition * other, self.localRotation * other)

    # Divide
    def __truediv__ (self, other) -> Self:
        if type(other) == Transform3D:
            return Transform3D(self.localPosition / other.localPosition, self.localRotation / other.localRotation)
        else:
            return Transform3D(self.localPosition / other, self.localRotation / other)

    # Floor divide
    def __floordiv__ (self, other) -> Self:
        if type(other) == Transform3D:
            return Transform3D(self.localPosition // other.localPosition, self.localRotation // other.localRotation)
        else:
            return Transform3D(self.localPosition // other, self.localRotation // other)

    # Power
    def __pow__ (self, other) -> Self:
        if type(other) == Transform3D:
            return Transform3D(self.localPosition ** other.localPosition, self.localRotation ** other.localRotation)
        else:
            return Transform3D(self.localPosition ** other, self.localRotation ** other)

    # Negative
    def __neg__ (self) -> Self:
        return Transform3D(-self.localPosition, -self.localRotation)

    # Absolute
    def __abs__ (self) -> Self:
        return Transform3D(abs(self.localPosition), abs(self.localRotation))
    
        #---Comparison---

    # Smaller
    def __lt__ (self, other: Self):
        if self.localPosition < other.localPosition and self.localRotation < other.localRotation:
            return True
        else:
            return False
    
    # Smaller or equal
    def __le__ (self, other: Self) -> bool:
        if self.localPosition <= other.localPosition and self.localRotation <= other.localRotation:
            return True
        else:
            return False

    # Greater
    def __gt__ (self, other: Self) -> bool:
        if self.localPosition > other.localPosition and self.localRotation > other.localRotation:
            return True
        else:
            return False

    # Greater or equal
    def __ge__ (self, other: Self) -> bool:
        if self.localPosition >= other.localPosition and self.localRotation >= other.localRotation:
            return True
        else:
            return False
    
    # Equal
    def __eq__ (self, other: Self) -> bool:
        if self.localPosition == other.localPosition and self.localRotation == other.localRotation:
            return True
        else:
            return False

    # Not equal
    def __ne__(self, other: Self) -> bool:
        if self.localPosition != other.localPosition and self.localRotation != other.localRotation:
            return True
        else:
            return False

        #---Other---
    def __str__(self) -> str:
        return f"({self.localPosition}; {self.localRotation})"
    
    
    #---Presets---
    def zero():
        return Transform3D()

    #---Initialization---
    def __init__(self, position = Vector3.zero(), rotation = RMatrix3.front(), scale = Vector3.one(), primary = None, parent = None, pos_is_global = False, rot_is_global = False) -> None:
        # Basics
        self.localPosition = position
        self.localRotation = rotation
        self.localScale = scale

        # Hierarchy
        self.primary = primary

        # Set parent
        if type(parent) == Transform3D:
            self.parent = parent
        elif parent:
            self.parent = parent.transform
        else:
            self.parent = parent

        # Set position and rotation
        if pos_is_global and type(parent) != type(None):
            self.localPosition = parent.globalPosition().vectorTo(position)
            # print(parent.transform.globalPosition().vectorTo(position), "; ", position, "; ", parent.transform)
        if rot_is_global and type(parent) != type(None):
            self.localRotation = rotation.local(parent.globalRotation())

#Some test code

r1 = RMatrix3(0, 0, 30)
t1 = Transform3D(Vector3.zero(), r1)
# print(t1.up())