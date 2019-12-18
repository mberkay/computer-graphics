# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from typing import List

from face import Face
from vec3d import Point, Vec3d
from copy import deepcopy


class FaceType:
    TRIANGLE = 0
    QUAD = 1
    types = [TRIANGLE, QUAD]


# TODO encapsulate face and position
class Mesh:
    def __init__(self, positions: List[Point], faces: List[Face], face_type=FaceType.QUAD):
        self.positions = positions
        # if faces is None:
        #     faces = Mesh.create_faces(positions)
        self.faces = faces
        self.__indexes, self.__face_type = self.create_indexes(faces, face_type)
        self.subdivision_level = 0
        self.subdivisions = []

    # def Normals(self):
    #     # sum = Vec3d.zero()
    #     for face in self.faces:
    #         # for edge in face.edges:
    #         #    sum += self.positions[edge.a] + self.positions[edge.b]
    #         # start_point = sum / (len(face.edges) * 2)
    #
    #         first_edge = face.edges[0]
    #         for edge in face.edges:
    #             if first_edge.contains_edge(edge) and edge is not first_edge:
    #                 second_edge = edge
    #                 break
    #
    #         # connected_edges = [edge for edge in face.edges if first_edge.contains_edge(edge) and edge is not first_edge]
    #
    #         vector_a = (self.positions[first_edge.b] - self.positions[first_edge.a]).to_vector()
    #         vector_b = (self.positions[second_edge.b] - self.positions[second_edge.a]).to_vector()
    #
    #         face.normal = vector_a.cross(vector_b).normalized

    def Normals(self):
        # sum = Vec3d.zero()
        for face in self.faces:
            # for edge in face.edges:
            #    sum += self.positions[edge.a] + self.positions[edge.b]
            # start_point = sum / (len(face.edges) * 2)

            first_edge = face.edges[0]
            for edge in face.edges:
                if first_edge.contains_edge(edge) and edge is not first_edge:
                    second_edge = edge
                    break

            # connected_edges = [edge for edge in face.edges if first_edge.contains_edge(edge) and edge is not first_edge]

            vector_a = (self.positions[first_edge.b] - self.positions[first_edge.a]).to_vector()
            vector_b = (self.positions[second_edge.b] - self.positions[second_edge.a]).to_vector()

            face.normal = vector_a.cross(vector_b).normalized

    def subdivide2(self, type):
        pass


    def subdivide(self, type):
        # Subdivide if type is 1 and subdivision level is max 3
        if type is 1 and self.subdivision_level < 4:
            next_subdivision_level = self.subdivision_level + 1
            # If current mesh is not stored in subdivisions, store it
            if len(self.subdivisions) < next_subdivision_level:
                self.subdivisions.append(deepcopy(self))
            # If stored and next subdivision is not created, create it, store it
            if len(self.subdivisions) == next_subdivision_level:
                can_subdivide, subdivided = self.create_subdivided_mesh(deepcopy(self.positions), deepcopy(self.faces),
                                                                        self.face_type)
                if can_subdivide:
                    self.subdivisions.append(deepcopy(subdivided))
            # If there are created subdivisions then update subdivision level
            if len(self.subdivisions) > next_subdivision_level:
                self.subdivision_level += 1
        # Revert subdivision if type is -1
        elif type is -1 and self.subdivision_level > 0:
            self.subdivision_level -= 1
        if len(self.subdivisions) is 0:
            return
        # If subdivision level changed then update position and face
        mesh = self.subdivisions[self.subdivision_level]
        self.faces = mesh.faces
        self.positions = mesh.positions
        self.__invalidate_indexes()

    # TODO support triangle subdivision too
    def create_subdivided_mesh(self, positions, faces, face_type):
        if face_type == FaceType.QUAD:
            faces_to_delete = []
            faces_to_append = []
            for face in faces:
                faces_to_delete.append(face)

                sum_of_points = Point(0, 0, 0)
                corner_indexes = face.to_quad()
                for corner_index in corner_indexes:
                    sum_of_points += positions[corner_index]
                face_center = p3 = sum_of_points / 4
                positions.append(face_center)
                i3 = positions.index(p3)

                # c0 xx c3
                # xx p3 xx
                # c1 xx c2
                for i in range(4):
                    p0 = positions[corner_indexes[i]]
                    p1 = (positions[corner_indexes[i]] + positions[corner_indexes[(i + 1) % 4]]) / 2
                    p2 = (positions[corner_indexes[i]] + positions[corner_indexes[(i - 1) % 4]]) / 2

                    if p1 not in positions:
                        positions.append(p1)
                    if p2 not in positions:
                        positions.append(p2)
                    i0 = positions.index(p0)
                    i1 = positions.index(p1)
                    i2 = positions.index(p2)
                    faces_to_append.append(Face([i2, i0, i1,
                                                 i2, i1, i3]))

            for face in faces_to_delete:
                faces.remove(face)
            for face in faces_to_append:
                faces.append(face)
            return True, Mesh(positions, faces, face_type)
        return False, None

    @property
    def indexes(self):
        if self.__indexes is None:
            self.__indexes, self.__face_type = self.create_indexes(self.faces, self.__face_type)
        return self.__indexes

    @property
    def face_type(self):
        return self.__face_type

    @face_type.setter
    def face_type(self, face_type: FaceType):
        if self.__face_type == face_type:
            return
        else:
            self.__indexes, self.__face_type = self.create_indexes(self.faces, face_type)

    @staticmethod
    def create_indexes(faces, face_type):
        make_quad = face_type is FaceType.QUAD

        quads = []
        triangles = []

        for face in faces:
            if face.indexes is None or len(face.indexes) < 1:
                continue
            if make_quad and face.is_quad():
                quads += face.to_quad()
            else:
                triangles += face.indexes

        if make_quad:
            if len(triangles) > 0:
                quads_count = len(quads)
                for i in range(0, quads_count, 4):
                    triangles.append(quads[i + 0])
                    triangles.append(quads[i + 1])
                    triangles.append(quads[i + 2])

                    triangles.append(quads[i + 2])
                    triangles.append(quads[i + 3])
                    triangles.append(quads[i + 0])
                return triangles, FaceType.TRIANGLE
            else:
                return quads, FaceType.QUAD
        else:
            return triangles, FaceType.TRIANGLE

    def __invalidate_indexes(self):
        self.__indexes = None
