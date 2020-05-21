from unittest import TestCase

from converters import RotationConverter
from mat3d import *
from vec3d import Point


class TestMat3d(TestCase):
    def check_elements(self, a, b):
        print(a)
        print(b)
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(a[i][j], b[i][j])

    def check_vectors(self, a, b):
        print(a , b)
        self.assertAlmostEqual(a.x, b.x, 5)
        self.assertAlmostEqual(a.y, b.y, 5)
        self.assertAlmostEqual(a.z, b.z, 5)

    def test_add(self):
        self.assertEquals(IdentityMatrix() + IdentityMatrix(), 2 * IdentityMatrix())

    def test_sub(self):
        self.assertEquals(IdentityMatrix() - IdentityMatrix(), ZeroMatrix())

    def test_unary(self):
        self.assertEquals(-IdentityMatrix(), -1 * IdentityMatrix())

    def test_arbitrary_axis_rotation_matrix(self):
        m = ArbitraryAxisRotationMatrix(Vec3d(1, 0, 0), 45)
        m = m.multiply_matrix(m)
        # vec1 = RotationConverter.axis_angle_to_euler(Vec3d(1, 0, 0), 45)
        # vec2 = RotationConverter.rotation_to_euler(m)
        # self.check_vectors(vec1, vec2)
        n = RotationConverter.euler_to_rotation_matrix(90, 0, 0)
        self.check_elements(m, n)



