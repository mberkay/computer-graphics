# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
from vec3d import Vec3d


class WingedFace:
    # def __init__(self):
    #     self.edge = None

    def __init__(self, face):
        self.face = face  # Just for debug purposes
        self.edge = None

    @property
    def face_point(self):
        total = Vec3d.zero()
        size = 0
        for vertex in self.vertices:
            total += vertex.position
            size += 1
        return total/size

    @property
    def normal(self):
        normal = Vec3d.zero()
        e = start = self.edge
        while True:
            v = e.vertex.position
            vnext = e.next.vertex.position
            normal += vnext.cross(v)
            if e is start:
                break
        return normal.normalized


    """
    Edge *start = f->e;
    Edge *e = start;
    do {
    visit(e);
    e = e->next; // CCW order
    } while (e != start);
    """
    @property
    def edges(self):
        edge = start = self.edge
        while True:
            yield edge
            edge = edge.next
            if edge is start:
                break

    @property
    def vertices(self):
        edge = start = self.edge
        while True:
            yield edge.vertex
            edge = edge.next
            if edge is start:
                break

    @property
    def neighboring_faces(self):
        edge = start = self.edge
        while True:
            yield edge.sym.face
            edge = edge.next
            if edge is start:
                break

    def __str__(self):
        # return f"[Edge: {self.edge}]"
        return f"[Face: {self.face}, Edge: {self.edge}]"

    def __repr__(self):
        return f"Winged Face: {str(self)}"
