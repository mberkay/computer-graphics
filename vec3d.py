# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

import math


class Vec3d:
    def __init__(self, x: float, y: float, z: float, w: float = 0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def to_array(self):
        return [self.x, self.y, self.z, self.w]

    @property
    def magnitude(self):
        return math.sqrt(self.dot(self))

    length = magnitude  # Alias length and magnitude

    @property
    def normalized(self):
        if self.magnitude == 0:
            return self
        return self / self.magnitude

    def dot(self, vector):
        x = self.x * vector.x
        y = self.y * vector.y
        z = self.z * vector.z
        w = self.w * vector.w
        dot = x + y + z + w
        dot = 0 if abs(dot) < 1e-6 else dot
        return dot

    def cross(self, vector):
        return Vec3d(self.y * vector.z - self.z * vector.y, self.z * vector.x - self.x * vector.z,
                     self.x * vector.y - self.y * vector.x, self.w)

    def scale(self, scale_vector):
        """
        Multiplies every component of this vector by the same component of scale.
        """
        self.x *= scale_vector.x
        self.y *= scale_vector.y
        self.z *= scale_vector.z

    def project(self, on_vector):
        magnitude_square = on_vector.dot(on_vector)
        dot = self.dot(on_vector)
        return on_vector * (dot / magnitude_square)  # TODO check zero division

    def angle(self, vector):
        if self.magnitude == 0 or vector.magnitude == 0:
            return 0
        try:
            return math.acos(self.dot(vector) / (self.magnitude * vector.magnitude))
        except:
            return 0

    def angle_degree(self, vector):
        return self.angle(vector) * (180 / math.pi)

    # Helps to do some_vector[0] etc or some_matrix[0][0]
    def __getitem__(self, item):
        if item is 0:
            return self.x
        elif item is 1:
            return self.y
        elif item is 2:
            return self.z
        elif item is 3:
            return self.w

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

    def __repr__(self):
        return f"Vector3{str(self)}"

    def __add__(self, vector):
        if isinstance(vector, Vec3d):
            return Vec3d(self.x + vector.x, self.y + vector.y, self.z + vector.z, self.w + vector.w)
        else:
            raise Exception(f"Can't add vector3 to type {type(vector)}")

    __radd__ = __add__

    def __sub__(self, vector):
        if isinstance(vector, Vec3d):
            return self + (-vector)
        else:
            raise Exception(f"Can't subtract vector3 to type {type(vector)}")

    def __mul__(self, scalar: float):
        return Vec3d(self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar)

    __rmul__ = __mul__  # Alias to calculate both (scalar * vector) and (vector * scalar)

    def __truediv__(self, scalar: float):
        return self * scalar ** -1

    def __neg__(self, ):
        return self * -1

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    @staticmethod
    def zero():
        return Vec3d(0, 0, 0)

    @staticmethod
    def one():
        return Vec3d(1, 1, 1)

    @staticmethod
    def up():
        return Vec3d(0, 1, 0)

    @staticmethod
    def down():
        return Vec3d(0, -1, 0)

    @staticmethod
    def left():
        return Vec3d(-1, 0, 0)

    @staticmethod
    def right():
        return Vec3d(1, 0, 0)

    @staticmethod
    def forward():
        return Vec3d(0, 0, 1)

    @staticmethod
    def backward():
        return Vec3d(0, 0, -1)


class Point(Vec3d):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z, 1)

    def to_vector(self):
        return Vec3d(self.x, self.y, self.z, 0)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, scalar):
        return Point(scalar * self.x, scalar * self.y, scalar * self.z)
