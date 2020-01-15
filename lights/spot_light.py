# CENG 487 Assignment5 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
import math

from OpenGL.GL import *

from lights import Light
from transform import Transform
from vec3d import Point


# https://learnopengl.com/Lighting/Light-casters
# Distance related attenuation coefficients
# 7	1.0	0.7	1.8
# 13	1.0	0.35	0.44
# 20	1.0	0.22	0.20
# 32	1.0	0.14	0.07
# 50	1.0	0.09	0.032
# 65	1.0	0.07	0.017
# 100	1.0	0.045	0.0075
# 160	1.0	0.027	0.0028
# 200	1.0	0.022	0.0019
# 325	1.0	0.014	0.0007
# 600	1.0	0.007	0.0002
# 3250	1.0	0.0014	0.000007


class SpotLight(Light):
    def __init__(self, ambient, diffuse, specular, angle, distance, transform: Transform):
        super().__init__(ambient, diffuse, specular, transform)
        self.angle = angle
        self.distance = distance
        # TODO look up coefficients given distance
        self.constant_attenuation = 1
        self.linear_attenuation = 0
        self.quadratic_attenuation = 0

    def draw(self):
        if not self.is_enabled:
            return
        self.transform.update()
        glDisable(GL_LIGHTING)
        glColor(self.diffuse[0], self.diffuse[1], self.diffuse[2])
        start_pos = self.transform.position
        size = math.tan(math.radians(self.angle)) * self.transform.forward
        glBegin(GL_LINE_LOOP)
        r = size.magnitude * self.distance
        for i in range(36):
            theta = 2 * math.pi * i / 36
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            z = 0
            pos = self.transform.transform_matrix.multiply_vector(Point(x, y, z))
            pos += self.transform.forward * self.distance
            glVertex3f(pos.x, pos.y, pos.z)
        glEnd()

        self.draw_border(self.transform.right, start_pos, size)
        self.draw_border(-self.transform.right, start_pos, size)
        self.draw_border(self.transform.up, start_pos, size)
        self.draw_border(-self.transform.up, start_pos, size)

    def draw_border(self, direction, start_pos, size):
        end_pos = (start_pos + (self.transform.forward + direction * size.magnitude) * self.distance)
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
        pos = self.transform.position.to_array()
        pos[3] = 1
        glLightfv(self.gl_light, GL_POSITION, pos)

        glLightf(self.gl_light, GL_CONSTANT_ATTENUATION, self.constant_attenuation)
        glLightf(self.gl_light, GL_LINEAR_ATTENUATION, self.linear_attenuation)
        glLightf(self.gl_light, GL_QUADRATIC_ATTENUATION, self.quadratic_attenuation)
        #
        glLightf(self.gl_light, GL_SPOT_CUTOFF, self.angle)
        # glLightfv(self.gl_light, GL_SPOT_DIRECTION,[0,0,-1,0])
        glLightfv(self.gl_light, GL_SPOT_DIRECTION, self.transform.forward.to_array())
        # glLightfv(self.gl_light, GL_SPOT_EXPONENT, 1)
        # glLightfv(self.gl_light, GL_SPOT_EXPONENT)
