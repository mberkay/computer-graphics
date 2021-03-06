# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from typing import List

from material import Material
from mesh import Mesh, FaceType
from transform import Transform
from vec3d import Vec3d
from mat3d import *
from mesh_deprecated import MeshDeprecated
from OpenGL.GL import *


class Shape:
    def __init__(self, name, mesh, transform: Transform = None, material: Material = None):
        self.name = name
        if transform is None:
            transform = Transform()
        self.transform = transform
        self.mesh = mesh
        if material is None:
            material = Material([0.2, 0.2, 0.2, 1.0], [0.8, 0.8, 0.8, 1.0], [0, 0.0, 0.0, 1.0], 0)  # Default
        self.material = material
        self.should_draw_normals = True

    ''' There are two ways to draw: 
            First one: using mesh.faces:
                If mesh face type is Quad can convert face indexes to quad and draw that vertexes to screen
            Second one: using mesh.indices:
                It is already calculated respect to face type preference. Downside of it is cant use different colors 
     '''

    def draw(self):
        self.transform.update()
        self.mesh.Normals()
        self.mesh.FacePoints()

        self.material.apply()
        for face in self.mesh.faces:
            if self.should_draw_normals:
                self.draw_normal(face)
            transformed_normal = self.transform.transform_matrix.multiply_vector(face.normal).normalized
            glBegin(GL_POLYGON)
            glNormal3f(transformed_normal.x, transformed_normal.y, transformed_normal.z)

            if self.mesh.face_type is FaceType.QUAD:
                face = face.to_quad()

            for index in face:  # face.indexes. Check __getitem__ of face.py
                pos = self.mesh.positions[index]
                pos = self.transform.transform_matrix.multiply_vector(pos)
                glVertex3f(pos.x, pos.y, pos.z)
            glEnd()

        # self.draw_directions()

    def draw_directions(self):
        glDisable(GL_LIGHTING)
        start_pos = self.transform.position
        end_pos = self.transform.position + self.transform.right * 5
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(start_pos.x, start_pos.y, start_pos.z)
        glVertex3f(end_pos.x, end_pos.y, end_pos.z)
        glEnd()

        end_pos = self.transform.position + self.transform.up * 5
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(start_pos.x, start_pos.y, start_pos.z)
        glVertex3f(end_pos.x, end_pos.y, end_pos.z)
        glEnd()

        end_pos = self.transform.position + self.transform.forward * 5
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex3f(start_pos.x, start_pos.y, start_pos.z)
        glVertex3f(end_pos.x, end_pos.y, end_pos.z)
        glEnd()

    def draw_normal(self, face):
        glDisable(GL_LIGHTING)
        start_pos = self.transform.transform_matrix.multiply_vector(face.face_point)
        end_pos = start_pos + self.transform.transform_matrix.multiply_vector(face.normal).normalized
        glBegin(GL_LINES)
        glVertex3f(start_pos.x, start_pos.y, start_pos.z)
        glVertex3f(end_pos.x, end_pos.y, end_pos.z)
        glEnd()
        glEnable(GL_LIGHTING)

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

    def draw_winged(self, disable_face_color):
        self.transform.update()
        # self.mesh.Normals()
        for face in self.mesh.faces:
            # self.draw_normal(face)

            glBegin(GL_POLYGON)
            # if not disable_face_color:
            #     glColor3f(face.color.x, face.color.y, face.color.z)

            for vertex in face.vertices:  # face.indexes. Check __getitem__ of face.py
                pos = vertex.position
                pos = self.transform.transform_matrix.multiply_vector(pos)
                glVertex3f(pos.x, pos.y, pos.z)
            glEnd()
