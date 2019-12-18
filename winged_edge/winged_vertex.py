# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
from vec3d import Vec3d


class WingedVertex:
    def __init__(self):
        self.position = None
        self.edge = None

    @property
    def normal(self):
        normal = Vec3d.zero()
        e = start = self.edge
        while True:
            normal += e.face.normal
            e = e.prev.sys
            if e is start:
                break
        return normal.normalized

    @property
    def edges(self):
        start = self.edge
        edge = start
        while True:
            yield edge
            edge = edge.prev.sym
            if edge is start:
                break

    @property
    def adjacent_faces(self):
        start = self.edge
        edge = start
        while True:
            yield edge.face
            edge = edge.prev.sym
            if edge is start:
                break

    def __str__(self):
        return f"[Position: {self.position}]"

    def __repr__(self):
        return f"WingedVertex{str(self)}"
