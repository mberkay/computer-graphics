# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from mesh import Mesh
from vec3d import *


class Cylinder(Mesh):
    def __init__(self, axis_division=8, radius=1, height=1, height_cuts=0):
        # Cylinder sides should be less than 64, even positive int
        self.axis_division = axis_division
        self.radius = radius
        self.height = height
        self.height_cuts = height_cuts

        if axis_division % 2 is not 0:
            axis_division += 1
        if axis_division > 64:
            axis_division = 64

        step_angle = 360 / axis_division
        step_height = height / (height_cuts + 1)

        circle = []
        for i in range(axis_division):
            angle0 = math.radians(step_angle * i)
            x = math.cos(angle0) * radius
            z = math.sin(angle0) * radius
            circle.append(Point(x, 0, z))

        self.vertices = []
        for i in range(height_cuts + 1):
            y = i * step_height
            y2 = (i + 1) * step_height

            for n in range(axis_division):
                self.vertices.append(Point(circle[n].x, y, circle[n].z))
                self.vertices.append(Point(circle[n].x, y2, circle[n].z))
                if n is not axis_division - 1:
                    self.vertices.append(Point(circle[n + 1].x, y, circle[n + 1].z))
                    self.vertices.append(Point(circle[n + 1].x, y2, circle[n + 1].z))
                else:
                    self.vertices.append(Point(circle[0].x, y, circle[0].z))
                    self.vertices.append(Point(circle[0].x, y2, circle[0].z))

        # wind side triangles
        self.triangles = []
        for i in range(height_cuts + 1):
            for n in range(0, axis_division * 4, 4):
                index = (i * axis_division * 4) + n
                zero = index
                one = index + 1
                two = index + 2
                three = index + 3
                self.triangles += [zero, one, two, one, three, two]

        ind = (axis_division * (height_cuts + 1) * 4)
        for n in range(axis_division):
            # Bottom faces
            self.vertices.append(Point(circle[n].x, 0, circle[n].z))
            self.vertices.append(Point(0, 0, 0))
            if n is not axis_division - 1:
                self.vertices.append(Point(circle[n + 1].x, 0, circle[n + 1].z))
            else:
                self.vertices.append(Point(circle[0].x, 0, circle[0].z))
            self.triangles += [ind + 2, ind + 1, ind + 0]
            ind += 3

            # Top faces
            self.vertices.append(Point(circle[n].x, height, circle[n].z))
            self.vertices.append(Point(0, height, 0))
            if n is not axis_division - 1:
                self.vertices.append(Point(circle[n + 1].x, height, circle[n + 1].z))
            else:
                self.vertices.append(Point(circle[0].x, height, circle[0].z))
            self.triangles += [ind, ind + 1, ind + 2]
            ind += 3

        super().__init__(self.vertices, self.triangles)
        self.can_subdivide = True

    def subdivide(self):
        if self.axis_division < 64:
            self.axis_division += 2
            return Cylinder(self.axis_division, self.radius, self.height, self.height_cuts)
        else:
            return self

    def unsubdivide(self):
        if self.axis_division > 4:
            self.axis_division -= 2
            return Cylinder(self.axis_division, self.radius, self.height, self.height_cuts)
        else:
            return self
