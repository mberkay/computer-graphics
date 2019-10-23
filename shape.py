# CENG 487 Assignment1 by
# Erdem Taylan
# StudentId: 230201005
# 10 2019

from typing import List
from vec3d import Vec3d
from mat3d import Mat3d
from OpenGL.GL import *


class Shape:
    def __init__(self, position: Vec3d, vertices: List[Vec3d], color: Vec3d, size: float = 1.0):
        self.position = position
        self.vertices = vertices
        self.size = size
        self.color = color / 255

    def draw(self):
        glBegin(GL_POLYGON)
        glColor3f(self.color.x, self.color.y, self.color.z)
        for vertex in self.vertices:
            vertex_position = self.position + (vertex * self.size)
            glVertex3f(vertex_position.x, vertex_position.y, vertex_position.z)
        glEnd()

    def transform(self, transform_matrices: List[Mat3d]):
        for transform_matrix in transform_matrices:
            for i, vertex in enumerate(self.vertices):
                self.vertices[i] = transform_matrix.multiply(vertex)

