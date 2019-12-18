# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from mesh_deprecated import MeshDeprecated
from vec3d import *


class Cube(MeshDeprecated):
    def __init__(self, size=Vec3d.one(), pivot="center"):
        self.vertices = [
            Point(0, 0, 0),  # 0
            Point(1, 0, 0),  # 1
            Point(1, 1, 0),  # 2
            Point(0, 1, 0),  # 3

            Point(0, 1, 1),  # 4
            Point(1, 1, 1),  # 5
            Point(1, 0, 1),  # 6
            Point(0, 0, 1)]  # 7

        self.triangles = [
            0, 2, 1,  # face front
            0, 3, 2,
            2, 3, 4,  # face top
            2, 4, 5,
            1, 2, 5,  # face right
            1, 5, 6,
            0, 7, 4,  # face left
            0, 4, 3,
            5, 4, 7,  # face back
            5, 7, 6,
            0, 6, 7,  # face bottom
            0, 1, 6
        ]
        if pivot == "center":
            self.center_pivot()
        for vertex in self.vertices:
            vertex * size

        super().__init__(self.vertices, self.triangles)

    def center_pivot(self):
        sum = self.vertices[0]
        count = 0
        for vertex in self.vertices:
            sum += vertex
            count += 1
        center = sum / count
        center = Vec3d(center.x, center.y, center.z, 0)

        for i, vertex in enumerate(self.vertices):
            self.vertices[i] -= center



