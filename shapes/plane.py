# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from mesh_deprecated import MeshDeprecated
from vec3d import *


class Plane(MeshDeprecated):
    def __init__(self, height=1, width=1, height_cuts=1, width_cuts=1,
                 look_up: Vec3d = Vec3d(0, 0, 1)):
        self.vertices = []
        self.height = height
        self.width = width
        self.height_cuts = height_cuts
        self.width_cuts = width_cuts
        w = width_cuts + 1
        h = height_cuts + 1
        points = []
        self.triangles = []
        i = 0
        for y in range(h):
            for x in range(w):
                x0 = x * (width / w) - (width / 2)
                x1 = (x + 1) * (width / w) - (width / 2)
                y0 = y * (height / h) - (height / 2)
                y1 = (y + 1) * (height / h) - (height / 2)

                points.append(Point(x0, y0, 0))
                points.append(Point(x1, y0, 0))
                points.append(Point(x0, y1, 0))
                points.append(Point(x1, y1, 0))
                # 2 3
                # 0 1
                self.triangles += [i + 0, i + 1, i + 2, i + 1, i + 3, i + 2]
                i += 4

        # TODO Create vertices respect to given look_up parameter
        for i in range(len(points)):
            # Adding width/4 and height/4 to fix center
            self.vertices.append(Point(points[i].x, points[i].y, 0))
        super().__init__(self.vertices, self.triangles)
        self.can_subdivide = True

    def subdivide(self):
        if self.width_cuts < 10 and self.height_cuts < 10:
            self.width_cuts += 1
            self.height_cuts += 1
            return Plane(self.height, self.width, self.height_cuts, self.width_cuts)
        else:
            return self

    def unsubdivide(self):
        if self.width_cuts > 0 and self.height_cuts > 0:
            self.width_cuts -= 1
            self.height_cuts -= 1
            return Plane(self.height, self.width, self.height_cuts, self.width_cuts)
        else:
            return self
