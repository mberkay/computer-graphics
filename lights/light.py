# CENG 487 Assignment5 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
import math

from OpenGL.GL import *

from transform import Transform
from vec3d import Vec3d


class Light:
    count = 0  # Static light counter

    def __init__(self, ambient, diffuse, specular, transform: Transform):
        if Light.count is 7:
            raise Exception("Can not create more than 8 light")
        else:
            self.gl_light = getattr(OpenGL.GL, f"GL_LIGHT{Light.count}")
            Light.count += 1
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.transform = transform
        self.is_enabled = True
        self.animation_count = 0

    def animate(self):
        # self.transform.position = Vec3d(10 * math.cos(time.time()), 3, 10 * math.sin(time.time()))
        self.transform.position = Vec3d(10 * math.cos(self.animation_count), 3, 10 * math.sin(self.animation_count))
        self.animation_count = (self.animation_count + 0.005) % 360
        self.transform.look_at(Vec3d(0, 0, 0))
        # self.transform.rotate(0, time.time(), 0)

    @property
    def direction(self):
        return self.transform.forward

    def enable(self):
        glEnable(self.gl_light)

    def disable(self):
        glDisable(self.gl_light)

    # TODO Maybe make Light Abstract Using abc library
    def draw(self):
        pass

    def light(self):
        pass
