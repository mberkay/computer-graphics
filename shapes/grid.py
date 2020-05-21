# CENG 487 Assignment6 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 01 2020
import numpy

from face import Face
from mesh import Mesh, FaceType
from vec3d import Point, Vec3d


class Grid(Mesh):
    def __init__(self, size=Vec3d.one(), pivot="center"):
        positions = []
        for i in range(-100, 100, 10):
            positions.append(Point(i, 0, 100))
            positions.append(Point(i, 0, -100))
            positions.append(Point(100, 0, i))
            positions.append(Point(-100, 0, i))

        faces = []
        super().__init__(positions, faces, face_type=FaceType.LINE)

    @property
    def np_positions(self):
        vertices = [vertex.to_array() for vertex in self.positions]
        size_vertices = len(vertices)
        return numpy.asarray(vertices).reshape(size_vertices * 4), size_vertices
