from unittest import TestCase

from converters import RotationConverter
from mat3d import Mat3d
from transform import Transform
from vec3d import Vec3d
from numpy.testing import assert_almost_equal


class TestRotationConverter(TestCase):
    def check_elements(self, a, b):
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(a[i][j], b[i][j])

    def check_vectors(self, a, b):
        self.assertAlmostEqual(a.x, b.x, 5)
        self.assertAlmostEqual(a.y, b.y, 5)
        self.assertAlmostEqual(a.z, b.z, 5)

    # region rotation_to_euler
    def test_rotation_to_euler_45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 0, 0)
        self.check_vectors(RotationConverter.rotation_to_euler(transform.rotation_matrix), Vec3d(45, 0, 0))

    def test_rotation_to_euler_90_90_90(self):
        transform = Transform()
        transform.rotation = Vec3d(90, 90, 90)
        self.check_vectors(RotationConverter.rotation_to_euler(transform.rotation_matrix), Vec3d(0, 180, 90))
    # endregion

    # region euler_to_rotation_matrix
    def test_euler_to_rotation_45_0_0(self):
        a = RotationConverter.euler_to_rotation_matrix(45, 0, 0)
        b = Mat3d(Vec3d(1, 0, 0, 0),
                  Vec3d(0, 0.7071068, -0.7071068, 0),
                  Vec3d(0, 0.7071068, 0.7071068, 0),
                  Vec3d(0, 0.0, 0, 1))
        self.check_elements(a, b)

    def test_euler_to_rotation_45_90_0(self):
        a = RotationConverter.euler_to_rotation_matrix(45, 90, 0)
        b = Mat3d(Vec3d(0, 0.7071068, 0.7071068, 0),
                  Vec3d(0, 0.7071068, -0.7071068, 0),
                  Vec3d(-1, 0, 0, 0),
                  Vec3d(0, 0.0, 0, 1))
        self.check_elements(a, b)

    def test_euler_to_rotation_90_90_90(self):
        a = RotationConverter.euler_to_rotation_matrix(90, 90, 90)
        b = Mat3d(Vec3d(0, 1, 0, 0),
                  Vec3d(1, 0, 0, 0),
                  Vec3d(0, 0, -1, 0),
                  Vec3d(0, 0.0, 0, 1))
        self.check_elements(a, b)

    def test_euler_to_rotation_45_90_0_rounded(self):
        a = RotationConverter.euler_to_rotation_matrix(45, 90, 0)
        a = round(a, 7)
        b = Mat3d(Vec3d(0, 0.7071068, 0.7071068, 0),
                  Vec3d(0, 0.7071068, -0.7071068, 0),
                  Vec3d(-1, 0, 0, 0),
                  Vec3d(0, 0.0, 0, 1))
        self.check_elements(a, b)

    def test_euler_to_rotation_45_45_45(self):
        a = RotationConverter.euler_to_rotation_matrix(45, 45, 45)
        b = Mat3d(Vec3d(0.5, 0.1464466, 0.8535534, 0),
                  Vec3d(0.7071068, 0.5, -0.5),
                  Vec3d(-0.5, 0.8535534, 0.1464466, 0),
                  Vec3d(0, 0.0, 0, 1))
        self.check_elements(a, b)

    # endregion

    # region axis_angle_to_euler

    def test_axis_angle_to_euler_1_0_0_45(self):
        m = RotationConverter.axis_angle_to_euler(Vec3d(1, 0, 0), 45)
        self.check_vectors(m, Vec3d(45, 0, 0))

    def test_axis_angle_to_euler_1_1_1_45(self):
        m = RotationConverter.axis_angle_to_euler(Vec3d(1, 1, 1), 45)
        self.check_vectors(m, Vec3d(21.105869, 21.105869, 30.3897425))

    def test_axis_angle_to_euler_1_0_1_90(self):
        m = RotationConverter.axis_angle_to_euler(Vec3d(1, 0, 1), 90)
        self.check_vectors(m, Vec3d(90, -45, 45))

    # endregion
