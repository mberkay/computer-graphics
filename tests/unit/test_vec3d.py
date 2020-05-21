from unittest import TestCase

from vec3d import Vec3d


class TestTransform(TestCase):
    def check_vectors(self, a, b):
        self.assertAlmostEqual(a.x, b.x, 5)
        self.assertAlmostEqual(a.y, b.y, 5)
        self.assertAlmostEqual(a.z, b.z, 5)

    def test_project_on_plane(self):
        self.check_vectors((Vec3d.forward() + Vec3d.up()).project_on_plane(Vec3d.up()), Vec3d(0,0,1))
