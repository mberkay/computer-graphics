# CENG 488 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 05 2020
from mat3d import Mat3d
from math import cos, sin, radians, degrees, atan2, asin, pi, acos
from vec3d import Vec3d


class RotationConverter:
    @staticmethod
    def rotation_to_euler(matrix: Mat3d) -> Vec3d:

        if matrix[1][0] > 0.998:
            x = 0
            y = atan2(matrix[0][2], matrix[2][2])
            z = pi / 2

        elif matrix[1][0] < -0.998:
            x = 0
            y = atan2(matrix[0][2], matrix[2][2])
            z = -pi / 2
        else:
            x = atan2(-matrix[1][2], matrix[1][1])
            y = atan2(-matrix[2][0], matrix[0][0])
            z = asin(matrix[1][0])
        return Vec3d(degrees(x), degrees(y), degrees(z))

    @staticmethod
    def euler_to_rotation_matrix(x, y, z) -> Mat3d:
        """
        Takes euler angles in degrees and returns rotation matrix type of Matrix4x4
        :type z: float
        :type y: float
        :type x: float
        :rtype Mat3d
        """
        x = radians(x)
        y = radians(y)
        z = radians(z)
        cos_y = cos(y)
        sin_y = sin(y)
        cos_z = cos(z)
        sin_z = sin(z)
        cos_x = cos(x)
        sin_x = sin(x)
        m00 = cos_y * cos_z
        m01 = sin_y * sin_x - cos_y * sin_z * cos_x
        m02 = cos_y * sin_z * sin_x + sin_y * cos_x
        m10 = sin_z
        m11 = cos_z * cos_x
        m12 = -cos_z * sin_x
        m20 = -sin_y * cos_z
        m21 = sin_y * sin_z * cos_x + cos_y * sin_x
        m22 = -sin_y * sin_z * sin_x + cos_y * cos_x
        return Mat3d(Vec3d(m00, m01, m02, 0),
                           Vec3d(m10, m11, m12, 0),
                           Vec3d(m20, m21, m22, 0),
                           Vec3d(0, 0, 0, 1))

    @staticmethod
    def axis_angle_to_euler(axis: Vec3d, angle: float) -> Vec3d:
        """
        Calculate euler angles for given axis. Y Z X, heading = y, z = attitude, bank=x
        :param axis: axis
        :param angle: angle in degree
        :return: euler angles
        :rtype Vec3d:
        """
        angle = radians(angle)
        s = sin(angle)
        c = cos(angle)
        t = 1 - c
        axis = axis.normalized
        x = axis.x
        y = axis.y
        z = axis.z
        if (x * y * t + z * s) > 0.998:  # north pole singularity detected
            heading = 2 * atan2(x * sin(angle / 2), cos(angle / 2))
            attitude = pi / 2
            bank = 0
            bank = degrees(bank)
            heading = degrees(heading)
            attitude = degrees(attitude)
            return Vec3d(bank, heading, attitude)

        if (x * y * t + z * s) < -0.998:  # south pole singularity detected
            heading = -2 * atan2(x * sin(angle / 2), cos(angle / 2))
            attitude = -pi / 2
            bank = 0
            bank = degrees(bank)
            heading = degrees(heading)
            attitude = degrees(attitude)
            return Vec3d(bank, heading, attitude)

        heading = atan2(y * s - x * z * t, 1 - (y * y + z * z) * t)
        attitude = asin(x * y * t + z * s)
        bank = atan2(x * s - y * z * t, 1 - (x * x + z * z) * t)
        bank = degrees(bank)
        heading = degrees(heading)
        attitude = degrees(attitude)
        return Vec3d(bank, heading, attitude)

    @staticmethod
    def euler_to_axis_angle(euler_angles: Vec3d) -> (Vec3d, float):
        bank = radians(euler_angles.x)
        heading = radians(euler_angles.y)
        attitude = radians(euler_angles.z)
        c1 = cos(heading / 2)
        s1 = sin(heading / 2)
        c2 = cos(attitude / 2)
        s2 = sin(attitude / 2)
        c3 = cos(bank / 2)
        s3 = sin(bank / 2)
        c1c2 = c1 * c2
        s1s2 = s1 * s2
        w = c1c2 * c3 - s1s2 * s3
        x = c1c2 * s3 + s1s2 * c3
        y = s1 * c2 * c3 + c1 * s2 * s3
        z = c1 * s2 * c3 - s1 * c2 * s3
        angle = 2 * acos(w)
        try:
            return Vec3d(x, y, z).normalized, angle
        except ZeroDivisionError:
            return Vec3d(1, 0, 0), angle
