# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019
import numpy
from OpenGL.raw.GLU import gluLookAt

from mat3d import Mat3d
from transform import Transform
from vec3d import Vec3d, Point


class Camera:
    def __init__(self):
        self.transform: Transform = Transform(Point(0, 4, 15), Vec3d(0, 180, 0))
        # self.transform.position.z = 12
        self.target_object = Vec3d.zero()
        self.near = 1.0
        self.far = 1000
        self.fov = 45.0
        self.aspect = 640 / 480
        self.project_matrix = self.calculate_project_matrix()
        self.view_matrix = self.calculate_view_matrix

    def reset(self):
        self.transform = Transform(Vec3d(0, 4, -15))
        # self.transform.position.z = -10
        self.target_object = Vec3d.zero()

    def update(self):
        self.transform.update()
        self.render()

    # https://learnopengl.com/Getting-started/Camera
    def calculate_view_matrix(self):
        rotation = Mat3d(self.transform.right,
                         self.transform.up,
                         -self.transform.forward,
                         Vec3d(0.0, 0.0, 0.0, 1))

        translation = Mat3d(Vec3d(1, 0, 0, -self.transform.position.x),
                            Vec3d(0, 1, 0, -self.transform.position.y),
                            Vec3d(0, 0, 1, -self.transform.position.z),
                            Vec3d(0.0, 0.0, 0.0, 1))

        # return self.transform.rotation_matrix.multiply_matrix(translation)
        return rotation.multiply_matrix(translation)

    # https://www.scratchapixel.com/lessons/3d-basic-rendering/perspective-and-orthographic-projection-matrix/building-basic-perspective-projection-matrix
    def calculate_project_matrix(self):
        f = numpy.reciprocal(numpy.tan(numpy.divide(numpy.deg2rad(self.fov), 2.0)))
        base = self.near - self.far
        term_0_0 = numpy.divide(f, self.aspect)
        term_2_2 = numpy.divide(self.far + self.near, base)
        term_2_3 = numpy.divide(numpy.multiply(numpy.multiply(2, self.near), self.far), base)

        return Mat3d(Vec3d(term_0_0, 0.0, 0.0, 0.0),
                     Vec3d(0.0, f, 0.0, 0.0),
                     Vec3d(0.0, 0.0, term_2_2, term_2_3),
                     Vec3d(0.0, 0.0, -1.0, 0.0))

    def render(self):
        self.view_matrix = self.calculate_view_matrix()
