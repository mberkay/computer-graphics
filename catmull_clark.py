# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
from mesh import Mesh
from winged_edge import WingedMesh
from vec3d import Vec3d


def get_face_points(mesh:WingedMesh):
    face_points = []
    for face in mesh.faces:
        face_points.append(face.face_point)
    return face_points

def get_edge_points(mesh: WingedMesh):
    edge_points = []
    for edge in mesh.edges:
        cp1 = edge.vertex.position
        cp2 = edge.next.vertex.position
        fp1 = edge.face.face_point
        if edge.sym is None:
            fp2 = fp1
        else:
            fp2 = edge.sym.face.face_point
        edge_point = (cp1 + cp2 + fp1 + fp2) / 4.0
        edge_points.append(edge_point)
    return edge_points

def create_face_points(mesh:WingedMesh):
    face_points = []
    for face in mesh.faces:
        face_points.append(face.face_point)

    return face_points

def create_edge_points(mesh: WingedMesh):
    edges = list(mesh.edges).copy()
    for edge in edges:
        cp1 = edge.vertex.position
        cp2 = edge.next.vertex.position
        fp1 = edge.face.face_point
        if edge.sym is None:
            fp2 = fp1
        else:
            fp2 = edge.sym.face.face_point
        edge_point = (cp1 + cp2 + fp1 + fp2)/4.0
        mesh.split_edge(edge, edge_point)
        # edge_points.append(sum((cp1,cp2,fp1,fp2))/4.0)


def get_avg_face_points(mesh: WingedMesh):
    avg_face_points = []
    total = Vec3d.zero()
    count = 0
    for vertex in mesh.vertices:
        for face in vertex.adjacent_faces:
            total += face.face_point
            count += 1
        avg_face_points.append(total/count)
    return avg_face_points


def get_avg_mid_edges(mesh: WingedMesh):
    avg_mid_edges = []
    total = Vec3d.zero()
    count = 0
    for vertex in mesh.vertices:
        for edge in vertex.edges:
            cp1 = edge.vertex.position
            cp2 = edge.next.vertex.position
            total += (cp1 + cp2) / 2.0
            count += 1
        avg_mid_edges .append(total/count)
    return avg_mid_edges


def create_new_points(mesh: WingedMesh):
    new_vertex_positions = []
    for vertex in mesh.vertices:
        total = Vec3d.zero()
        count = 0
        for face in vertex.adjacent_faces:
            total += face.face_point
            count += 1
        avg_face_points = total / count
        total = Vec3d.zero()
        count = 0

        for edge in vertex.edges:
            cp1 = edge.vertex.position
            cp2 = edge.next.vertex.position
            total += (cp1 + cp2) / 2.0
            count += 1
        avg_mid_edges = total / count
        n = len(list(vertex.adjacent_faces))
        m1 = (n - 3) * vertex.position
        m2 = 2 * avg_mid_edges
        new_vertex_positions.append((avg_face_points + m2 + m1) / n)
    for i, vertex in enumerate(mesh.vertices):
        vertex.position = new_vertex_positions[i]


def catmull_clark(mesh):
    create_new_points(mesh)
    create_edge_points(mesh)
    # for face in mesh.faces:
    #     mesh.triangulate_face(face)


def get_new_points(mesh: WingedMesh):
    new_points = []
    avg_face_points = get_avg_face_points(mesh)
    avg_mid_edges = get_avg_mid_edges(mesh)

    for vertex_index, vertex in enumerate(mesh.vertices):
        n = 0  #  Number of face points
        for face in vertex.adjacent_faces:
            n += 1

        m1 = (n - 3) / n
        m2 = 1 / n
        m3 = 2 / n

        old_vertex = vertex
        p1 = old_vertex.position * m1
        afp = avg_face_points[vertex_index]
        p2 = afp * m2
        ame = avg_mid_edges[vertex_index]
        p3 = ame * m3

        new_coords = p1 + p2 + p3

        new_points.append(new_coords)

    return new_points

    # add face points to new_points
def cmc_subdiv(mesh):
    new_points = get_new_points(mesh)
    face_points = get_face_points(mesh)
    edge_points = get_edge_points(mesh)
    # edges_faces = get_edges_faces(mesh)
    face_point_nums = []

    # point num after next append to new_points
    next_pointnum = len(new_points)

    for face_point in face_points:
        new_points.append(face_point)
        face_point_nums.append(next_pointnum)
        next_pointnum += 1

    # add edge points to new_points

    edge_point_nums = dict()

    for edgenum, edge in enumerate(mesh.edges):
        pointnum_1 = edge.edge.a
        pointnum_2 = edge.edge.b
        edge_point = edge_points[edgenum]
        new_points.append(edge_point)
        edge_point_nums[(pointnum_1, pointnum_2)] = next_pointnum
        next_pointnum += 1

    new_faces = []

    for oldfacenum in range(len(mesh.faces)):
        oldface = list(set(mesh.faces[oldfacenum].face.indexes))
        # mesh.faces.
        # 4 point face
        # vertices = oldface.vertices
        a = oldface[0]
        b = oldface[1]
        c = oldface[2]
        d = oldface[3]
        face_point_abcd = face_point_nums[oldfacenum]
        edge_point_ab = edge_point_nums[switch_nums((a, b))]
        edge_point_da = edge_point_nums[switch_nums((d, a))]
        edge_point_bc = edge_point_nums[switch_nums((b, c))]
        edge_point_cd = edge_point_nums[switch_nums((c, d))]
        new_faces.append((a, edge_point_ab, face_point_abcd, edge_point_da))
        new_faces.append((b, edge_point_bc, face_point_abcd, edge_point_ab))
        new_faces.append((c, edge_point_cd, face_point_abcd, edge_point_bc))
        new_faces.append((d, edge_point_da, face_point_abcd, edge_point_cd))

    return new_points, new_faces

def switch_nums(point_nums):
    """
    Returns tuple of point numbers
    sorted least to most
    """
    if point_nums[0] < point_nums[1]:
        return point_nums
    else:
        return (point_nums[1], point_nums[0])