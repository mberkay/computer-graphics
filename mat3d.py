# CENG 487 Assignment1 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from vec3d import Vec3d
import math


class Mat3d:
    def __init__(self, a: Vec3d, b: Vec3d, c: Vec3d, d: Vec3d):
        self.matrix = [a, b, c, d]

    def multiply_vector(self, other: Vec3d):
        return Vec3d(self.matrix[0].dot(other),
                     self.matrix[1].dot(other),
                     self.matrix[2].dot(other),
                     self.matrix[3].dot(other))

    def multiply_matrix(self, other):
        other = other.transpose
        rows = []
        for i in range(4):
            columns = []
            for j in range(4):
                columns.append(self.matrix[i].dot(other.matrix[j]))
            rows.append(Vec3d(columns[0], columns[1], columns[2], columns[3]))
        return Mat3d(rows[0], rows[1], rows[2], rows[3])

    # Rotate around x axis then y then z
    @staticmethod
    def rotation_matrix(euler_angles: Vec3d, order="XYZ"):
        return RotationXMatrix(euler_angles.x).multiply_matrix(
            RotationYMatrix(euler_angles.y).multiply_matrix(RotationZMatrix(euler_angles.z)))
        # rotation_dict = {"X": RotationXMatrix, "Y": RotationYMatrix, "Z": RotationZMatrix}
        # return rotation_dict[order[0]].multiply_matrix(rotation_dict[order[1]].multiply_matrix(rotation_dict[order[2]]()))

    # Is valid rotation matrix
    def is_rotation_matrix(self):
        rt = self.transpose
        should_be_identity = rt.multiply_matrix(self)
        identity = IdentityMatrix()
        return identity == should_be_identity

    # https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    @staticmethod
    def rotation_matrix_to_euler_angles(rotation_matrix):
        """
        :returns euler angles in degrees
        :rtype: Vec3d
        """
        R = rotation_matrix.matrix
        if rotation_matrix.is_rotation_matrix:
            sy = math.sqrt(rotation_matrix[0][0] ** 2 + rotation_matrix[1][0] ** 2)
            singular = sy < 1e-6

            if not singular:
                x = math.atan2(rotation_matrix[2][1], rotation_matrix[2][2])
                y = math.atan2(-rotation_matrix[2][0], sy)
                z = math.atan2(rotation_matrix[1][0], rotation_matrix[0][0])
            else:
                x = math.atan2(-rotation_matrix[1][2], rotation_matrix[1][1])
                y = math.atan2(-rotation_matrix[2][0], sy)
                z = 0
            return Vec3d(x, y, z) * (180 / math.pi)


    @staticmethod
    def rotation_matrix_to_euler_angles2(rotation_matrix):
        """
        :returns euler angles in degrees
        :rtype: Vec3d
        """
        R = rotation_matrix.matrix
        if rotation_matrix.is_rotation_matrix:
            if rotation_matrix[1][0] > 0.998:
                y = math.atan2(rotation_matrix[0][2], rotation_matrix[2][2])
                z = math.pi / 2
                x = 0
            elif rotation_matrix[1][0] < -0.998:
                y = math.atan2(rotation_matrix[0][2], rotation_matrix[2][2])
                z = - math.pi / 2
                x = 0
            else:
                y = math.atan2(-rotation_matrix[2][0], -rotation_matrix[0][0])
                x = math.atan2(-rotation_matrix[1][2], rotation_matrix[1][1])
                z = math.asin(rotation_matrix[1][0])

            return Vec3d(x, y, z) * (180 / math.pi)

    @property
    def transpose(self):
        return Mat3d(Vec3d(self.matrix[0].x, self.matrix[1].x, self.matrix[2].x, self.matrix[3].x),
                     Vec3d(self.matrix[0].y, self.matrix[1].y, self.matrix[2].y, self.matrix[3].y),
                     Vec3d(self.matrix[0].z, self.matrix[1].z, self.matrix[2].z, self.matrix[3].z),
                     Vec3d(self.matrix[0].w, self.matrix[1].w, self.matrix[2].w, self.matrix[3].w))

    def __mul__(self, scalar):
        return Mat3d(self.matrix[0] * scalar,
                     self.matrix[1] * scalar,
                     self.matrix[2] * scalar,
                     self.matrix[3] * scalar)

    __rmul__ = __mul__

    def __eq__(self, other):
        return self.matrix == other.matrix

    def __str__(self):
        return f"{self.matrix[0]}\n{self.matrix[1]}\n{self.matrix[2]}\n{self.matrix[3]}"

    def __getitem__(self, item):
        if item is 0:
            return self.matrix[0]
        elif item is 1:
            return self.matrix[1]
        elif item is 2:
            return self.matrix[2]
        elif item is 3:
            return self.matrix[3]


# https://learnopengl.com/Getting-started/Transformation rotation section
class ArbitraryRotationAxis(Mat3d):
    def __init__(self, axis: Vec3d, angle):
        axis = axis.normalized
        rx = axis.x
        ry = axis.y
        rz = axis.z
        super().__init__(
            Vec3d(math.cos(angle) + rx ** 2 * (1 - math.cos(angle)), rx * ry * (1 - math.cos(angle)) - rz * math.sin(angle), rx * rz * (1 - math.cos(angle)) + ry * math.sin(angle), 0),
            Vec3d(ry * rx * (1 - math.cos(angle)) + rz * math.sin(angle), math.cos(angle) + ry ** 2 * (1 - math.cos(angle)), ry * rz * (1 - math.cos(angle)) - rx * math.sin(angle), 0),
            Vec3d(rz * rx * (1 - math.cos(angle)) - ry * math.sin(angle), rz * ry * (1 - math.cos(angle)) + rx * math.sin(angle), math.cos(angle) + rz ** 2 * (1 - math.cos(angle)), 0),
            Vec3d(0, 0, 0, 1))


class IdentityMatrix(Mat3d):
    def __init__(self):
        super().__init__(Vec3d(1, 0, 0, 0),
                         Vec3d(0, 1, 0, 0),
                         Vec3d(0, 0, 1, 0),
                         Vec3d(0, 0, 0, 1))


class ZeroMatrix(Mat3d):
    def __init__(self):
        super().__init__(Vec3d(0, 0, 0, 0),
                         Vec3d(0, 0, 0, 0),
                         Vec3d(0, 0, 0, 0),
                         Vec3d(0, 0, 0, 1))


class TranslationMatrix(Mat3d):
    def __init__(self, vector: Vec3d):
        super().__init__(Vec3d(1, 0, 0, vector.x),
                         Vec3d(0, 1, 0, vector.y),
                         Vec3d(0, 0, 1, vector.z),
                         Vec3d(0, 0, 0, 1))


class ScalingMatrix(Mat3d):
    def __init__(self, vector: Vec3d):
        super().__init__(Vec3d(vector.x, 0, 0, 0),
                         Vec3d(0, vector.y, 0, 0),
                         Vec3d(0, 0, vector.z, 0),
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
