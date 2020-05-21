from unittest import TestCase

from mat3d import IdentityMatrix
from transform import Transform, Vec3d, Mat3d


class TestTransform(TestCase):
    def check_elements(self, a, b):
        for i in range(4):
            for j in range(4):
                self.assertAlmostEqual(a[i][j], b[i][j])

    def check_vectors(self, a, b):
        self.assertAlmostEqual(a.x, b.x, 5)
        self.assertAlmostEqual(a.y, b.y, 5)
        self.assertAlmostEqual(a.z, b.z, 5)

    def test_up(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 20, 52)
        self.check_vectors(transform.forward.cross(transform.right), transform.up)

    def test_rotate_45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 0, 0)
        self.assertEquals(transform.rotation, Vec3d(45, 0, 0))

    def test_rotate_90_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(90, 0, 0)
        self.assertEquals(transform.rotation, Vec3d(90, 0, 0))

    def test_rotate_45_0_0_after_45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 0, 0)
        transform.rotation = Vec3d(45, 0, 0)
        self.assertEquals(transform.rotation, Vec3d(90, 0, 0))

    def test_rotation_matrix_0_0_0(self):
        transform = Transform()
        print(transform.rotation_matrix)
        print(IdentityMatrix())
        self.assertEquals(transform.rotation_matrix, IdentityMatrix())

    def test_forward_0_0_0(self):
        transform = Transform()
        self.assertEquals(transform.forward, Vec3d.forward())

    def test_forward_45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 0, 0)
        self.assertAlmostEqual(transform.forward.x, .0, 4)
        self.assertAlmostEqual(transform.forward.y, -.7071068, 4)
        self.assertAlmostEqual(transform.forward.z, .7071068, 4)

    def test_forward_negative45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(-45, 0, 0)
        self.assertAlmostEqual(transform.forward.x, .0, 4)
        self.assertAlmostEqual(transform.forward.y, .7071068, 4)
        self.assertAlmostEqual(transform.forward.z, .7071068, 4)


    def test_up_45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 0, 0)
        self.assertAlmostEqual(transform.up.x, .0, 4)
        self.assertAlmostEqual(transform.up.y, .7071068, 4)
        self.assertAlmostEqual(transform.up.z, -.7071068, 4)

    def test_right_0_0_90(self):
        transform = Transform()
        transform.rotation = Vec3d(0, 0, 90)
        self.check_vectors(transform.right, Vec3d(0,1,0))

    def test_right_45_0_0(self):
        transform = Transform()
        transform.rotation = Vec3d(45, 0, 0)
        self.assertAlmostEqual(transform.right.x, 1, 4)
        self.assertAlmostEqual(transform.right.y, 0, 4)
        self.assertAlmostEqual(transform.right.z, 0, 4)

    def test_axes_90_90_90(self):
        transform = Transform()
        transform.rotation = Vec3d(90, 90, 90)
        print(transform.forward)
        self.assertAlmostEqual(transform.forward.x, 0, 4)
        self.assertAlmostEqual(transform.forward.y, 0, 4)
        self.assertAlmostEqual(transform.forward.z, -1, 4)
        self.assertAlmostEqual(transform.right.x, 0, 4)
        self.assertAlmostEqual(transform.right.y, 1, 4)
        self.assertAlmostEqual(transform.right.z, 0, 4)
        self.assertAlmostEqual(transform.up.x, -1, 4)
        self.assertAlmostEqual(transform.up.y, 0, 4)
        self.assertAlmostEqual(transform.up.z, 0, 4)

    def test_rotate_order(self):
        t1 = Transform()
        t2 = Transform()
        t1.rotation = Vec3d(90, 90, 90)
        t2.rotation = Vec3d(0, 180, 90)
        self.check_elements(t2.rotation_matrix, t1.rotation_matrix)
        self.check_vectors(t1.forward, t2.forward)
        self.check_vectors(t1.right, t2.right)
        self.check_vectors(t1.up, t2.up)
