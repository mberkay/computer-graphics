# CENG 487 Assignment1 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from typing import List

from transform import Transform
from vec3d import Vec3d
from mat3d import *
from mesh import Mesh
from OpenGL.GL import *


class Shape:
    def __init__(self, mesh: Mesh, transform: Transform = None):
        if transform is None:
            transform = Transform()
        self.transform = transform
        self.mesh = mesh

    def draw(self):
        self.transform.update()
        glBegin(GL_TRIANGLES)
        # print("transform matrix ", self.transform.transform_matrix)
        for i in range(0, len(self.mesh.triangles), 3):
            glColor3f(self.mesh.color[i].x, self.mesh.color[i].y, self.mesh.color[i].z)
            for j in range(3):
                vertex = self.mesh.vertices[self.mesh.triangles[i + j]]
                # print("vertex ", vertex)
                vertex_position = self.transform.transform_matrix.multiply_vector(vertex)
                vertex_position /= vertex_position.w
                # print("vertex position", vertex_position)
                # print(vertex, vertex_position)
                glVertex3f(vertex_position.x, vertex_position.y, vertex_position.z)
        glEnd()
