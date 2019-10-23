import math


class Vec3d:
    def __init__(self, x: float, y: float, z: float, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    @property
    def magnitude(self):
        return math.sqrt(self.dot(self))

    length = magnitude  # Alias length and magnitude

    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z + self.w * vector.w

    def cross(self, vector):
        return Vec3d(self.y * vector.z - self.z * vector.y, self.z * vector.x - self.x * vector.z,
                     self.x * vector.y - self.y * vector.x)

    def project(self, on_vector):
        magnitude_square = on_vector.dot(on_vector)
        dot = self.dot(on_vector)
        return on_vector * (dot / magnitude_square)  # TODO check zero division

    def angle(self, vector):
        return math.acos(self.dot(vector) / (self.magnitude() * vector.magnitude()))  # TODO check zero division

    def angle_degree(self, vector):
        return self.angle(vector) * (180 / math.pi)

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"Vector3{str(self)}"

    def __add__(self, vector):
        if isinstance(vector, Vec3d):
            return Vec3d(self.x + vector.x, self.y + vector.y, self.z + vector.z)
        else:
            raise Exception(f"Can't add vector3 to type {type(vector)}")

    def __sub__(self, vector):
        if isinstance(vector, Vec3d):
            return self + (-vector)
        else:
            raise Exception(f"Can't subtract vector3 to type {type(vector)}")

    def __mul__(self, scalar: int):
        return Vec3d(self.x * scalar, self.y * scalar, self.z * scalar)

    __rmul__ = __mul__  # Alias to calculate both (scalar * vector) and (vector * scalar)

    def __truediv__(self, scalar: int):
        return self * scalar ** -1

    def __neg__(self, ):
        return self * -1
