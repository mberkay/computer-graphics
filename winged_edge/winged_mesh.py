# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
# from winged_edge.edge import Edge
from winged_edge import WingedEdge
from winged_edge.winged_vertex import WingedVertex
from winged_edge.winged_face import WingedFace


class WingedMesh:
    def __init__(self, faces, edges, vertices):
        self.faces = faces
        self.edges = edges
        self.vertices = vertices

    def split_edge(self, edge, pos):
        e0 = WingedEdge(edge.edge)
        e1 = WingedEdge(edge.edge)
        v0 = WingedVertex()

        self.edges.append(e0)
        self.edges.append(e1)
        self.vertices.append(v0)

        v0.position = pos
        v0.edge = e0
        e0.set(v0, edge.face, edge, edge.next, edge.sym)
        e1.set(v0, edge.sym.face, edge.sym, edge.sym.next, edge)

        edge.next.prev = e0
        edge.sym.next.prev = e1
        edge.next = e0
        edge.sym.next = e1
        edge.sym.sym = e0
        edge.sym = e1

    def divide_face(self, face):
        e = face.edge
        e1 = e.next
        e3 = e1.next.next
        e5 = e3.next.next
        e7 = e5.next.next

        v1 = e1.vertex
        v3 = e3.vertex
        v5 = e5.vertex
        v7 = e7.vertex

        face_point = face.face_point()

        enew1 = WingedEdge()
        esym1 = WingedEdge()
        fnew1 = WingedFace()
        # enew1.set(v1, f)



    def triangulate_face(self, face):
        while True:
            e = face.edge
            e1 = e.next
            e2 = e1.next
            e3 = e2.next

            if e is e3:
                break

            v1 = e1.vertex
            v3 = e3.vertex
            enew = WingedEdge(e.edge)
            esym = WingedEdge(e.edge)
            fnew = WingedFace(face.face)

            enew.set(v1, face, e, e3, esym)
            esym.set(v3, fnew, e2, e1, enew)
            fnew.edge = e1
            e1.prev = e2.next = esym
            e3.prev = e.next = enew
            e1.face = e2.face = fnew
            self.faces.append(fnew)
            self.edges.append(enew)
            self.edges.append(esym)
