# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019
from face import Face
from mesh import Mesh, FaceType
from vec3d import Point, Vec3d


class Cube(Mesh):
    def __init__(self, size=Vec3d.one(), pivot="center", face_type=FaceType.TRIANGLE):
        positions = [position * 2 for position in Cube.__positions]
        faces = [Face(Cube.__triangles[i:i + 6]) for i in range(0, 36, 6)]
        super().__init__(positions, faces, face_type)

    __positions = [
        Point(0, 0, 0),  # 0
        Point(1, 0, 0),  # 1
        Point(1, 1, 0),  # 2
        Point(0, 1, 0),  # 3

        Point(0, 1, 1),  # 4
        Point(1, 1, 1),  # 5
        Point(1, 0, 1),  # 6
        Point(0, 0, 1)]  # 7

    __triangles = [
        0, 2, 1,  # face front
        0, 3, 2,
        2, 3, 4,  # face top
        2, 4, 5,
        1, 2, 5,  # face right
        1, 5, 6,
        0, 7, 4,  # face left
        0, 4, 3,
        5, 4, 7,  # face back
        5, 7, 6,
        0, 6, 7,  # face bottom
        0, 1, 6
    ]
