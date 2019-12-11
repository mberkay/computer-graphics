# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from typing import List

from mesh2 import Mesh2, FaceType
from transform import Transform
from vec3d import Vec3d
from mat3d import *
from mesh import Mesh
from OpenGL.GL import *


class Shape:
    def __init__(self, mesh: Mesh2, transform: Transform = None):
        if transform is None:
            transform = Transform()
        self.transform = transform
        self.mesh = mesh

    ''' There are two ways to draw: 
            First one: using mesh.faces:
                If mesh face type is Quad can convert face indexes to quad and draw that vertexes to screen
            Second one: using mesh.indices:
                It is already calculated respect to face type preference. Downside of it is cant use different colors 
     '''

    def draw(self, disable_face_color):
        self.transform.update()
        self.mesh.Normals()
        for face in self.mesh.faces:
            start_pos = self.mesh.positions[face.indexes[0]]
            start_pos = self.transform.transform_matrix.multiply_vector(start_pos)
            end_pos = start_pos + face.normal
            glBegin(GL_LINES)
            glVertex3f(start_pos.x, start_pos.y, start_pos.z)
            glVertex3f(end_pos.x, end_pos.y, end_pos.z)
            glEnd()
            glBegin(GL_POLYGON)

            if not disable_face_color:
                glColor3f(face.color.x, face.color.y, face.color.z)

            if self.mesh.face_type is FaceType.QUAD:
                face = face.to_quad()

            for index in face:  # face.indexes. Check __getitem__ of face.py
                pos = self.mesh.positions[index]
                pos = self.transform.transform_matrix.multiply_vector(pos)
                glVertex3f(pos.x, pos.y, pos.z)
            glEnd()

    def draw2(self):
        self.transform.update()
        if self.mesh.face_type is FaceType.TRIANGLE:
            glBegin(GL_TRIANGLES)
        else:
            glBegin(GL_QUADS)
        # glColor3f(0.5, 0, 0)
        for index in self.mesh.indexes:
            pos = self.mesh.positions[index]
            pos = self.transform.transform_matrix.multiply_vector(pos)
            glVertex3f(pos.x, pos.y, pos.z)
        glEnd()
