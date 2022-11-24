#This script is a host to the quaternion class
#The quaternion class is not implemented yet

from typing_extensions import Self
from VectorMath import Vector3, Vector2
import math

#Thanks to José Matos for this class
#Find out more at https://www.fep.up.pt/docentes/jamatos/listings/Quaternion.py.html

class Quaternion:
    # Quaternions are a generalization of complex numbers that instead of a single imaginary part _i_ have two other _j_ and _k_.
    # The rule for the product of imaginary parts is:
    # 	i*i = j*j = k*k = -1
    #     i*j = k   j*i = -k
    #     j*k = i   k*j = -i
    #     k*i = j   i*k = -j

    # From the rules above we see that i*j*k = -1

    def __init__(self, w= 0, x=0, y=0, z=0):
        # The verbose of this part comes from the need to test each
        # type. To follow the same convention as complex numbers each
        # argument can either be a real number, a complex number or a
        # quaternion.

        # scalar component
        if type(w) == type(self):
            self.w = w.w
            self.x = w.x
            self.y = w.y
            self.z = w.z
        elif type(w) == complex:
            self.w = w.real
            self.x = w.imag
            self.y = 0
            self.z = 0
        else:
            self.w = w
            self.x = 0
            self.y = 0
            self.z = 0

        # imaginary _i_ component
        if type(x) == type(self):
            self.w -= x.x
            self.x += x.w
            self.y += x.z
            self.z -= x.y
        elif type(x) == complex:
            self.w -= x.imag
            self.x += x.real
        else:
            self.x += x

        # imaginary _j_ component
        if type(y) == type(self):
            self.w -= y.y
            self.x -= y.z
            self.y += y.w
            self.z += y.x
        elif type(y) == complex:
            self.y += y.real
            self.z += y.imag
        else:
            self.y += y

        # imaginary _k_ component
        if type(z) == type(self):
            self.w -= z.z
            self.x += z.y
            self.y -= z.x
            self.z += z.w
        elif type(z) == complex:
            self.y -= z.imag
            self.z += z.real
        else:
            self.z += z

        # simpler unused version of the constructor
        # here all arguments of the constructor are real numbers
        #    def __init__(self, r= 0, i=0, j=0, k=0):
        #        self.w = r
        #        self.x = i
        #        self.y = j
        #        self.z = k

    # ----Extra math---

    #Imaginary part of quaternion as Vector3
    def imaginary(self):
        return Vector3(self.x, self.y, self.z)

    #Magnitude of the quaternion
    def magnitude(self):
        return math.sqrt(self.w * self.w + 
                        self.x * self.x + 
                        self.y * self.y + 
                        self.z * self.z)

    #Unit quaternion
    def unit(self):
        return self / self.magnitude()

    #Convert euler angles to quatrnion
    def Euler(angles: Vector3, radians = False):
        if not radians:
            angles.radians()

        # Abbreviations for the various angular functions
        cy = math.cos(angles.y * 0.5)
        sy = math.sin(angles.y * 0.5)
        cp = math.cos(angles.z * 0.5)
        sp = math.sin(angles.z * 0.5)
        cr = math.cos(angles.x * 0.5)
        sr = math.sin(angles.x * 0.5)

        q = Quaternion()
        q.w = cr * cp * cy + sr * sp * sy
        q.x = sr * cp * cy - cr * sp * sy
        q.y = cr * sp * cy + sr * cp * sy
        q.z = cr * cp * sy - sr * sp * cy
        return q

    def ToEulerAngles(self):
        pass


    # ---Special functions---

    # x.__neg__() <==> -x
    def __neg__(self):
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    # x.__add__(y) <==> x+y
    def __add__(self, other):
        other = Quaternion(other)
        return Quaternion(self.w + other.w,
                          self.x + other.x,
                          self.y + other.y,
                          self.z + other.z)

    # x.__mul__(y) <==> x*y
    def __mul__(self, other):
        other = Quaternion(other)
        return Quaternion(self.w*other.w - self.x*other.x - self.y*other.y - self.z*other.z,
                          self.w*other.x + self.x*other.w + self.y*other.z - self.z*other.y,
                          self.w*other.y + self.y*other.w + self.z*other.x - self.x*other.z,
                          self.w*other.z + self.z*other.w + self.x*other.y - self.y*other.x)

    # x.__rmul__(y) <==> y*x
    def __rmul__(self, other):
        other = Quaternion(other)
        return other*self

    # x.__abs__() <==> abs(x)
    def __abs__(self):
        return math.sqrt(self.w*self.w +
                         self.x*self.x +
                         self.y*self.y +
                         self.z*self.z)

    # x.__radd__(y) <==> y+x
    def __radd__(self, other):
        return self + other

    #  x.__div__(y) <==> x/y
    def __truediv__(self, other):
        # Quaternion division is essentially the reverse multiplication.
        # If the multiplication rules are:   
        # 	  i*i = j*j = k*k = -1
        #
        #     i*j = k   j*i = -k
        #     j*k = i   k*j = -i
        #     k*i = j   i*k = -j

        # Then the devision rules are:
        #   -1 / i = i
        #   -1 / j = j
        #   -1 / k = k
        #
        #   i / j = k   i / k = -j
        #   j / k = i   j / i = -k
        #   k / i = j   k / j = -i

        # And so the division table is:
        #   /   1  i  j  k
        #      __ __ __ __
        #   1 | 1 -i -j -k
        #   i | i  1  k -j
        #   j | j -k  1  i
        #   k | k  j -i  1

        # We need to check if other is a number or a complex or a quaternion
        if type(other) == float or type(other) == int:
            return Quaternion(  self.w / other, 
                                self.x / other, 
                                self.y / other, 
                                self.z / other)
        elif type(other) == complex:
            return Quaternion(  self.w / other.real + self.x / other.imag,
                                self.x / other.real + self.w / -other.imag,
                                self.y / other.real + self.z / other.imag,
                                self.z / other.real + self.y / -other.x)
        else:
            other = Quaternion(other)
            return Quaternion(  self.w / other.w + self.x / other.x + self.y / other.y + self.z / other.z,
                                self.x / other.w + self.w / -other.x + self.y / other.z + self.z / -other.y,
                                self.y / other.w + self.w / -other.y + self.x / -other.z + self.z / other.x,
                                self.z / other.w + self.w / -other.z + self.x / other.y + self.y / -other.x)
        
        # otherSquareSum = other.w*other.w + other.x*other.x + other.y*other.y + other.z*other.z
        # return Quaternion(  self.w*other.w + self.x*other.x + self.y*other.y + self.z*other.z / otherSquareSum, 
        #                     self.x*other.w - self.w*other.x - self.z*other.y + self.y*other.z / otherSquareSum,
        #                     self.y*other.w + self.z*other.x - self.w*other.y - self.x*other.z / otherSquareSum,
        #                     self.z*other.w - self.y*other.x + self.x*other.y - self.w*other.z / otherSquareSum)

    # x.__rdiv__(y) <==> y/x
    def __rtruediv__(self, other):
        return Quaternion(other) * self.conjugate() / (abs(self) ** 2)

    # x.__sub__(y) <==> x-y
    def __sub__(self, other):
        return self + (-other)

    # x.__rsub__(y) <==> y-x
    def __rsub__(self, other):
        return other + (-self)

    # x.__eq__(y) <==> x==y
    def __eq__(self, other):
        other = Quaternion(other)
        return (self.w == other.w and self.x == other.x and
                self.y == other.y and self.z == other.z)

    # x.__ne__(y) <==> x!=y
    def __ne__(self, other):
        return not (self == other)

    # x.__str__() <==> str(x)
    def __str__(self):
        return "Quaternion(%g, %g, %g, %g)" % (self.w, self.x, self.y, self.z)

    # x.__repr__() <==> repr(x)
    def __repr__(self):
        return "Quaternion(%g, %g, %g, %g)" % (self.w, self.x, self.y, self.z)

    # Returns the complex part of the quaternion. Quaternion(1,2,3,4) == 1+2j.
    def __complex__(self):
        return complex(self.w, self.x)

    # Returns the Quaternion conjugate of its argument. (3-4j).conjugate() == 3+4j.
    def conjugate(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    # Pretty print the quaternion
    def prettyprint(self):
        return "Quaternion: (%g + %g i+ %g j+ %g k)" % (self.w, self.x, self.y, self.z)

    # ------Some presets------
    # Makes all components 0
    def zero():
        return Quaternion()
    # Makes all components 1
    def one():
        return Quaternion(1, 1, 1, 1)
    



#Test code

q = Quaternion(0, 1, 0, 0)
q2 = Quaternion(0, -1, 0, 0)

print(q2.ToEulerAngles())