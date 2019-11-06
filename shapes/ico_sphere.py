# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from mesh import Mesh
from vec3d import *


class IcoSphere(Mesh):
    def __init__(self, subdivision=1, radius=1):
        t = (1 + math.sqrt(5)) / 2  # Golden Ratio

        self.vertices = [
            Point(-1, t, 0),
            Point(1, t, 0),
            Point(-1, -t, 0),
            Point(1, -t, 0),

            Point(0, -1, t),
            Point(0, 1, t),
            Point(0, -1, -t),
            Point(0, 1, -t),

            Point(t, 0, -1),
            Point(t, 0, 1),
            Point(-t, 0, -1),
            Point(-t, 0, 1)]

        self.triangles = [
            0, 11, 5,
            0, 5, 1,
            0, 1, 7,
            0, 7, 10,
            0, 10, 11,

            1, 5, 9,
            5, 11, 4,
            11, 10, 2,
            10, 7, 6,
            7, 1, 8,

            3, 9, 4,
            3, 4, 2,
            3, 2, 6,
            3, 6, 8,
            3, 8, 9,

            4, 9, 5,
            2, 4, 11,
            6, 2, 10,
            8, 6, 7,
            9, 8, 1
        ]
        self.subdivision = subdivision
        self.radius = radius
        self.create()
        super().__init__(self.vertices, self.triangles)
        self.can_subdivide = True

    def create(self):
        v = [None] * len(self.triangles)
        for i in range(0, len(self.triangles), 3):
            v[i + 0] = self.vertices[self.triangles[i + 0]].normalized * self.radius
            v[i + 1] = self.vertices[self.triangles[i + 1]].normalized * self.radius
            v[i + 2] = self.vertices[self.triangles[i + 2]].normalized * self.radius

        for i in range(self.subdivision):
            v = self.subdivide_icosahedron(v)

        t = [None] * len(v)
        for i in range(len(v)):
            t[i] = i

        self.vertices = v
        self.triangles = t

    def subdivide_icosahedron(self, vertices):
        #   5
        #  3 4
        # 0 1 2
        v = [None] * len(vertices) * 4
        index = 0
        for i in range(0, len(vertices), 3):
            p0 = vertices[i + 0]
            p2 = vertices[i + 1]
            p5 = vertices[i + 2]
            p1 = ((p0 + p2) / 2).normalized * self.radius
            p3 = ((p0 + p5) / 2).normalized * self.radius
            p4 = ((p2 + p5) / 2).normalized * self.radius

            v[index] = p0
            v[index + 1] = p1
            v[index + 2] = p3

            v[index + 3] = p1
            v[index + 4] = p2
            v[index + 5] = p4

            v[index + 6] = p1
            v[index + 7] = p4
            v[index + 8] = p3

            v[index + 9] = p3
            v[index + 10] = p4
            v[index + 11] = p5
            index += 12
        return v

    def subdivide(self):
        if self.subdivision < 4:
            self.subdivision += 1
            return IcoSphere(self.subdivision, self.radius)
        else:
            return self

    def unsubdivide(self):
        if self.subdivision > 0:
            self.subdivision -= 1
            return IcoSphere(self.subdivision, self.radius)
        else:
            return self
