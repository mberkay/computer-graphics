# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from typing import List

from OpenGL.GL.VERSION.GL_4_6 import *


from material import Material
from mesh import Mesh, FaceType
from program import Program
from transform import Transform
from vec3d import Vec3d
from mat3d import *
from mesh_deprecated import MeshDeprecated
from OpenGL.GL import *
# from OpenGL.GLU import *
# from OpenGL.GLUT import *
# from OpenGL.GL.ARB.vertex_array_object import *
# from OpenGL.arrays.vbo import VBO
import numpy


class Shape:
    def __init__(self, name, mesh, transform: Transform = None, material: Material = None, color= None, program: Program = None):
        self.name = name
        if transform is None:
            transform = Transform()
        self.transform = transform
        self.mesh = mesh
        self.color = color
        if material is None:
            material = Material([0.2, 0.2, 0.2, 1.0], [0.8, 0.8, 0.8, 1.0], [0, 0.0, 0.0, 1.0], 0)  # Default
        self.material = material
        self.program = program
        self.should_draw_normals = True

        # Immediate mode stuff
        self.buffer_state_id = glGenVertexArrays(1)
        self.vertex_buffer_id = glGenBuffers(1)
        self.vertices, self.number_of_vertices = self.mesh.np_positions

        if self.color is not None:
            final_colors = [self.color.to_array() for i in range(self.number_of_vertices)]
            colors = numpy.asarray(final_colors).reshape(self.number_of_vertices * 4)
        self.vertex_VBO = self.vertices if self.color is None else numpy.concatenate((self.vertices, colors))
         # = len(self.mesh.positions)

        glBindVertexArray(self.buffer_state_id)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        element_size = numpy.dtype(numpy.float32).itemsize
        glBufferData(GL_ARRAY_BUFFER, len(self.vertex_VBO) * element_size,
                     (ctypes.c_float * len(self.vertex_VBO))(*self.vertex_VBO), GL_STATIC_DRAW)

        offset = 0
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, element_size * 4, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(0)

        if self.color is not None:
            offset += element_size * 4
            glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, element_size * 4, ctypes.c_void_p(offset))
            glEnableVertexAttribArray(1)

        glBindVertexArray(0)

    ''' There are two ways to draw: 
            First one: using mesh.faces:
                If mesh face type is Quad can convert face indexes to quad and draw that vertexes to screen
            Second one: using mesh.indices:
                It is already calculated respect to face type preference. Downside of it is cant use different colors 
     '''

    def draw_core(self, view_matrix, project_matrix):
        self.transform.update()
        program = self.program
        program.use()

        model_location = glGetUniformLocation(program.id, "model")
        glUniformMatrix4fv(model_location, 1, GL_FALSE, self.transform.transform_matrix.transpose.np_mat3d)

        view_location = glGetUniformLocation(program.id, "view")
        proj_location = glGetUniformLocation(program.id, "proj")

        # get matrices from view and object
        # they need to transposed because glsl expect column major and we are row major
        glUniformMatrix4fv(view_location, 1, GL_FALSE, view_matrix.transpose.np_mat3d)
        glUniformMatrix4fv(proj_location, 1, GL_FALSE, project_matrix.transpose.np_mat3d)

        glBindVertexArray(self.buffer_state_id)

        if self.mesh.face_type is FaceType.QUAD:
            glDrawArrays(GL_QUADS, 0, self.number_of_vertices)
        elif self.mesh.face_type is FaceType.TRIANGLE:
            glDrawArrays(GL_TRIANGLES, 0, self.number_of_vertices)
        # For grid
        elif self.mesh.face_type is FaceType.LINE:
            glDrawArrays(GL_LINES, 0, self.number_of_vertices)

        glBindVertexArray(0)

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
