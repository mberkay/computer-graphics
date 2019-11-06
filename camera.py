# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from OpenGL.raw.GLU import gluLookAt

from transform import Transform
from vec3d import Vec3d


class Camera:
    def __init__(self):
        self.transform = Transform(Vec3d(0, 4, -15))
        # self.transform.position.z = 12
        self.target_object = Vec3d.zero()

    def reset(self):
        self.transform = Transform()
        self.transform.position.z = -10
        self.target_object = Vec3d.zero()

    def update(self):
        self.transform.update()
        self.render()

    def render(self):
        pos = self.transform.position
        forward = self.transform.forward
        # print("pos: ", pos, "forward: ", forward, "rotation: ", self.transform.rotation)
        target = pos + forward

        gluLookAt(pos.x, pos.y, pos.z, target.x, target.y, target.z, 0, 1, 0)
        # gluLookAt(0, 5, 12, 0, 0, 0, 0, 1, 0)
