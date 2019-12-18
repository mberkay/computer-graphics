# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019


class WingedEdge:
    # sym Symmetric edge
    # def __init__(self):
    #     self.vertex = None
    #     self.face = None
    #     self.prev = None
    #     self.next = None
    #     self.sym = None

    def __init__(self, edge):
        self.edge = edge
        self.vertex = None
        self.face = None
        self.prev = None
        self.next = None
        self.sym = None

    def set(self, vertex, face, prev, next_e, sym):
        self.vertex = vertex
        self.face = face
        self.prev = prev
        self.next = next_e
        self.sym = sym

    def is_symmetric(self, other):
        return self.vertex is other.next.vertex and self.next.vertex is other.vertex

    def __str__(self):
        # return f"[Vertex: {self.vertex}]"
        return f"[Edge: {self.edge}, Vertex: {self.vertex}]"

    def __repr__(self):
        return f"WingedEdge{str(self)}"
