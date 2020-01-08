# CENG 487 Assignment5 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
import math

from OpenGL.GL import *

from lights import Light
from transform import Transform
from vec3d import Point


class DirectionalLight(Light):
    def __init__(self, ambient, diffuse, specular, transform: Transform):
        super().__init__(ambient, diffuse, specular, transform)

    def draw(self):
        if not self.is_enabled:
            return
        self.transform.update()
        glDisable(GL_LIGHTING)
        glColor(self.diffuse[0], self.diffuse[1], self.diffuse[2])
        glBegin(GL_LINE_LOOP)
        for i in range(36):
            theta = 2 * math.pi * i / 36
            x = 0.5 * math.cos(theta)
            y = 0.5 * math.sin(theta)
            z = 0
            pos = self.transform.transform_matrix.multiply_vector(Point(x, y, z))
            glVertex3f(pos.x, pos.y, pos.z)
        glEnd()

        start_pos = self.transform.position
        end_pos = start_pos + self.transform.forward * 5

        glBegin(GL_LINES)
        glVertex3f(start_pos.x, start_pos.y, start_pos.z)
        glVertex3f(end_pos.x, end_pos.y, end_pos.z)
        glEnd()

    def light(self):
        if not self.is_enabled:
            return
        glEnable(GL_LIGHTING)
        self.enable()
        glLightfv(self.gl_light, GL_AMBIENT, self.ambient)
        glLightfv(self.gl_light, GL_DIFFUSE, self.diffuse)
        glLightfv(self.gl_light, GL_SPECULAR, self.specular)
        glLightfv(self.gl_light, GL_POSITION, (-self.direction).to_array())
