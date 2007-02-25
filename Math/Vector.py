from Numeric import *

class Vector:
    def __init__(self, *contents):
        self._v = array(contents, Float)
    def __len__(self):
        return len(self._v)
    def __getitem__(self, i):
        return self._v[i]
    def __setitem__(self, key, value):
        self._v[key] = value
    def __repr__(self):
        return self._v.__repr__()
    def __str__(self):
        return self._v.__repr__()
    def __add__(self, other):
        return Vector(*(self._v + other._v))
    def __sub__(self, other):
        return Vector(*(self._v - other._v))
    def __mul__(self, other):
        return Vector(*(self._v * other))
    def __div__(self, other):
        return Vector(*(self._v / other))
    def norm(self):
        return sqrt(add.reduce(self._v ** 2))
    def normalize(self):
        return self / self.norm()
    def dot(self, other):
        return Vector(*(dot(self._v, other._v)))
        
    def _move_axis_to_0(a, axis):
        if axis == 0:
            return a
        n = a.ndim
        if axis < 0:
            axis += n
        axes = range(1, axis+1) + [0,] + range(axis+1, n)
        return a.transpose(axes)
    
    def cross(self, other, axisa=-1, axisb=-1, axisc=-1):
        # Swiped from Scipy
        """Return the cross product of two (arrays of) vectors.

        The cross product is performed over the last axis of a and b by default,
        and can handle axes with dimensions 2 and 3. For a dimension of 2,
        the z-component of the equivalent three-dimensional cross product is
        returned.
        """
        a = self._v
        b = other._v
        a = self._move_axis_to_0(asarray(a), axisa)
        b = self._move_axis_to_0(asarray(b), axisb)
        msg = "incompatible dimensions for cross product\n"\
              "(dimension must be 2 or 3)"
        if (a.shape[0] not in [2,3]) or (b.shape[0] not in [2,3]):
            raise ValueError(msg)
        if a.shape[0] == 2:
            if (b.shape[0] == 2):
                cp = a[0]*b[1] - a[1]*b[0]
                if cp.ndim == 0:
                    return cp
                else:
                    return cp.swapaxes(0,axisc)
            else:
                x = a[1]*b[2]
                y = -a[0]*b[2]
                z = a[0]*b[1] - a[1]*b[0]
        elif a.shape[0] == 3:
            if (b.shape[0] == 3):
                x = a[1]*b[2] - a[2]*b[1]
                y = a[2]*b[0] - a[0]*b[2]
                z = a[0]*b[1] - a[1]*b[0]
            else:
                x = -a[2]*b[1]
                y = a[2]*b[0]
                z = a[0]*b[1] - a[1]*b[0]
        cp = array([x,y,z])
        if cp.ndim == 1:
            return cp
        else:
            return cp.swapaxes(0,axisc)