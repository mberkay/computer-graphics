# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

import random

from vec3d import Vec3d


class Mesh:
    def __init__(self, vertices, triangles):
        self.vertices = vertices
        self.triangles = triangles
        self.color = []
        self.create_colors()
        self.can_subdivide = False

    def create_colors(self):
        for i in range(len(self.triangles)):
            self.color.append(Vec3d(random.randint(0,255),random.randint(0,255),random.randint(0,255)) / 255)
