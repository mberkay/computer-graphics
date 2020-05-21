# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019
from converters import RotationConverter
from mat3d import *
from vec3d import Point


class Transform:
    def __init__(self, position: Point = Vec3d.zero(), rotation: Vec3d = Vec3d.zero(), scale: Vec3d = Vec3d.one()):
        self.position: Point = position
        self._rotation = rotation
        self.scale = scale
        self.transform_matrix = IdentityMatrix()
        self.transform_matrix_stack = []

    @property
    def rotation_matrix(self):
        return RotationConverter.euler_to_rotation_matrix(self.rotation.x, self.rotation.y, self.rotation.z)

    @property
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = Vec3d(value.x, value.y, value.z)

    def translate(self, translation: Vec3d):
        self.position += translation

    def rotate_axis(self, axis: Vec3d, angle):
        """
        Rotate object angle in given axis
        :param axis:  Vec3d
        :param angle: In degrees
        """
        rm = ArbitraryAxisRotationMatrix(axis, angle)
        ultimate_rotation = rm.multiply_matrix(self.rotation_matrix)
        euler_angles = RotationConverter.rotation_to_euler(ultimate_rotation)
        euler_angles = euler_angles
        self.rotation = Vec3d(euler_angles.x, euler_angles.y, euler_angles.z)

    def rotate_around(self, point: Point, axis: Vec3d, angle):
        position = self.position
        reverse_target = point - position
        rm = ArbitraryAxisRotationMatrix(axis, -angle)
        new_direction = rm.multiply_vector(reverse_target)
        self.position = point - new_direction
        self.rotate_axis(axis, -angle)

    def look_at(self, target_position: Point):
        target = (target_position - self.position).to_vector()
        angle = target.normalized.angle(self.forward)  # In radian
        if angle < 0.01:
            return
        target_on_xy = target.project_on_plane(Vec3d.up())
        forward_on_xy = self.forward.project_on_plane(Vec3d.up())
        angle = target_on_xy.angle_degree(forward_on_xy)
        axis = target_on_xy.cross(forward_on_xy)
        direction = 1 if axis.y > 0 else -1
        self.rotate_axis(Vec3d.up(), direction * -angle)
        # phase 2
        angle = target.angle_degree(self.forward)
        if angle < 0.01:
            return
        axis = target.cross(self.forward)
        diff = abs(axis.normalized - self.right)
        diff_sum = diff.x + diff.y + diff.z < 0.2
        direction = 1 if diff_sum else -1
        self.rotate_axis(self.right, direction * -angle)

    # Add stack in order S R T so T * R * S * V will scale first then rotate then transform
    def update(self):
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
    def forward(self) -> Vec3d:
        return self.rotation_matrix.multiply_vector(Vec3d.forward()).normalized

    @property
    def right(self) -> Vec3d:
        return self.rotation_matrix.multiply_vector(Vec3d.right()).normalized

    @property
    def up(self) -> Vec3d:
        return self.rotation_matrix.multiply_vector(Vec3d.up()).normalized
