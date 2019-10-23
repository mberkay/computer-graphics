from vec3d import Vec3d
import math


class Mat3d:
    def __init__(self, a: Vec3d, b: Vec3d, c: Vec3d, d: Vec3d):
        self.matrix = [a, b, c, d]

    def multiply(self, other: Vec3d):
        return Vec3d(self.matrix[0].dot(other),
                     self.matrix[1].dot(other),
                     self.matrix[2].dot(other),
                     self.matrix[3].dot(other))

    @property
    def transpose(self):
        return Mat3d(Vec3d(self.matrix[0].x, self.matrix[1].x, self.matrix[2].x, self.matrix[3].x),
                     Vec3d(self.matrix[0].y, self.matrix[1].y, self.matrix[2].y, self.matrix[3].y),
                     Vec3d(self.matrix[0].z, self.matrix[1].z, self.matrix[2].z, self.matrix[3].z),
                     Vec3d(self.matrix[0].w, self.matrix[1].w, self.matrix[2].w, self.matrix[3].w))


class TransformMat3d(Mat3d):
    def __init__(self, x, y, z):
        super().__init__(Vec3d(1, 0, 0, x),
                         Vec3d(0, 1, 0, y),
                         Vec3d(0, 0, 1, z),
                         Vec3d(0, 0, 0, 1))


class ScalingMat3d(Mat3d):
    def __init__(self, x, y, z):
        super().__init__(Vec3d(x, 0, 0, 0),
                         Vec3d(0, y, 0, 0),
                         Vec3d(0, 0, z, 0),
                         Vec3d(0, 0, 0, 1))


class RotationXMatrix(Mat3d):
    def __init__(self, angle):
        super().__init__(Vec3d(1, 0, 0, 0),
                         Vec3d(0, math.cos(angle), -math.sin(angle), 0),
                         Vec3d(0, math.sin(angle), math.cos(angle), 0),
                         Vec3d(0, 0, 0, 1))


class RotationYMatrix(Mat3d):
    def __init__(self, angle):
        super().__init__(Vec3d(math.cos(angle), 0, math.sin(angle), 0),
                         Vec3d(0, 1, 0, 0),
                         Vec3d(-math.sin(angle), 0, math.cos(angle), 0),
                         Vec3d(0, 0, 0, 1))


class RotationZMatrix(Mat3d):
    def __init__(self, angle):
        super().__init__(Vec3d(math.cos(angle), -math.sin(angle), 0, 0),
                         Vec3d(math.sin(angle), math.cos(angle), 0, 0),
                         Vec3d(0, 0, 1, 0),
                         Vec3d(0, 0, 0, 1))
