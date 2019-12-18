# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019

from mesh import Mesh as IndexedMesh
from winged_edge.winged_mesh import WingedMesh as WingedMesh
from winged_edge.winged_edge import WingedEdge
from winged_edge.winged_vertex import WingedVertex
from winged_edge.winged_face import WingedFace


def indexed_face_set_to_winged_edge(indexed_mesh: IndexedMesh):
    winged_vertices = []
    for position in indexed_mesh.positions:
        vertex = WingedVertex()
        vertex.position = position
        winged_vertices.append(vertex)

    winged_edges = []
    winged_faces = []
    for k, face in enumerate(indexed_mesh.faces):
        faces_winged_edges = []
        winged_face = WingedFace(face)
        for i, edge in enumerate(face.edges):
            winged_edge = WingedEdge(edge)
            vertex_index = edge.a
            winged_edge.vertex = winged_vertices[vertex_index]
            winged_edges.append(winged_edge)
            faces_winged_edges.append(winged_edge)
            if i is 0:
                winged_face.edge = winged_edge
                winged_faces.append(winged_face)
            winged_edge.face = winged_face
        for winged_edge in faces_winged_edges:
            # index = faces_winged_edges.index(winged_edge)
            # winged_edge.prev = faces_winged_edges[index - 1]
            # winged_edge.next = faces_winged_edges[(index + 1) % len(faces_winged_edges)]
            winged_edge.prev, winged_edge.next = find_previous_and_next(winged_edge, faces_winged_edges)
    # Find edge of vertex
    for i, winged_vertex in enumerate(winged_vertices):
        for winged_edge in winged_edges:
            if winged_edge.vertex is winged_vertex:
                winged_vertex.edge = winged_edge
                break
    # Find sym of edges
    for winged_edge_first in winged_edges:
        for winged_edge_second in winged_edges:
            if winged_edge_first.is_symmetric(winged_edge_second):
                winged_edge_first.sym = winged_edge_second
                winged_edge_second.sym = winged_edge_first
    for edge in winged_vertices[0].adjacent_faces:
        print(edge)
    print("god")
    return WingedMesh(winged_faces, winged_edges, winged_vertices)

def find_previous_and_next(winged_edge, winged_edges):
    a = winged_edge.edge.a
    b = winged_edge.edge.b

    for other_winged_edge in winged_edges:
        if other_winged_edge.edge.a is b:
            previous = other_winged_edge
        elif other_winged_edge.edge.b is a:
            next = other_winged_edge
    return previous, next
