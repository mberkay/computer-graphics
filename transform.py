# CENG 487 Assignment1 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from mat3d import *


class Transform:
    def __init__(self, position: Vec3d = Vec3d.zero(), rotation: Vec3d = Vec3d.zero(), scale: Vec3d = Vec3d.one()):
        self.position = position
        self._rotation = rotation
        self.scale = scale
        self.transform_matrix = IdentityMatrix()
        self.transform_matrix_stack = []
        self.rotation_matrix = ZeroMatrix()

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = Vec3d(round(value.x, 3), round(value.y, 3), round(value.z, 3))

    def translate(self, translation: Vec3d):
        self.position += translation

    def rotate(self, x_angle, y_angle, z_angle):
        self.rotation += Vec3d(x_angle, y_angle, z_angle)

    def rotate_axis(self, axis: Vec3d, angle):
        """
        Rotate object angle in given axis
        :param axis:  Vec3d
        :param angle: In degrees
        """
        angle = math.radians(angle)
        rm = ArbitraryRotationAxis(axis, angle)
        rm = rm.transpose
        euler_angles = Mat3d.rotation_matrix_to_euler_angles(rm)
        euler_angles = Vec3d(round(euler_angles.x, 5), round(euler_angles.y, 5), round(euler_angles.z, 5))
        self.rotate(euler_angles.x, euler_angles.y, euler_angles.z)

    def look_at(self, target_position):
        target = target_position - self.position

        angle = target.normalized.angle(self.forward.normalized)  # In radian
        axis = target.normalized.cross(self.forward.normalized)
        self.rotate_axis(axis, math.degrees(angle))

    # Add stack in order S R T so T * R * S * V will scale first then rotate then transform
    def update(self):
        self.rotation_matrix = Mat3d.rotation_matrix(self.rotation * (math.pi / 180))
        self.transform_matrix_stack.insert(0, ScalingMatrix(self.scale))
        self.add_matrix_to_stack(self.rotation_matrix)
        self.add_matrix_to_stack(TranslationMatrix(self.position))
        self.transform_matrix = IdentityMatrix()
        self.calculate_transform_matrix()
        self.transform_matrix_stack = []

    def add_matrix_to_stack(self, matrix):
        self.transform_matrix_stack.append(matrix)

    # Calculations are done in ... third second first
    def calculate_transform_matrix(self):
        for transform_matrix in self.transform_matrix_stack:
            self.transform_matrix = transform_matrix.multiply_matrix(self.transform_matrix)
        return self.transform_matrix

    @property
    def forward(self):
        return self.rotation_matrix.multiply_vector(Vec3d.forward())  # TODO use quaternions

    @property
    def right(self):
        return Vec3d.up().cross(self.forward).normalized

    @property
    def up(self):
        return self.forward.cross(self.right).normalized


def is_small(vector):
    if abs(vector.x) + abs(vector.y) + abs(vector.z) < 3e-6:
        return True
    else:
        return False
