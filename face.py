# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019
import random
from typing import List

from edge import Edge
from vec3d import Vec3d


class Face:
    def __init__(self, indexes):
        self.__indexes = None
        self.__edges = None
        self.normal = None
        self.face_point = None
        self.indexes = indexes
        self.color = Vec3d(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) / 255

    def to_quad(self):
        if not self.is_quad():
            raise Exception("Face is not a quad.")

        quads = [self.edges[0].a, self.edges[0].b, -1, -1]
        if self.edges[1].a is quads[1]:
            quads[2] = self.edges[1].b
        elif self.edges[2].a is quads[1]:
            quads[2] = self.edges[2].b
        elif self.edges[3].a is quads[1]:
            quads[2] = self.edges[3].b

        if self.edges[1].a is quads[2]:
            quads[3] = self.edges[1].b
        elif self.edges[2].a is quads[2]:
            quads[3] = self.edges[2].b
        elif self.edges[3].a is quads[2]:
            quads[3] = self.edges[3].b
        return quads

    def is_quad(self):
        return self.edges is not None and len(self.edges) is 4

    # @property
    # def normal(self):
    #     if self.__normal is None:
    #         self.__calculate_normal()
    #     return self.__normal
    #
    # def __calculate_normal(self):
    #     first_edge = self.edges[0]
    #     second_edge = self.edges[1]
    #
    #     vector_a = self
    #     self.__normal =

    @property
    def indexes(self):
        return self.__indexes

    @indexes.setter
    def indexes(self, indexes: List[int]):
        length = len(indexes)
        if length % 3 != 0:
            raise ValueError("Face indexes must be multiple of 3.")
        self.__indexes = indexes
        self.__invalidate_edges()

    # To prevent getting old edges when indexes are change
    def __invalidate_edges(self):
        self.__edges = None

    @property
    def edges(self):
        if self.__edges is None:
            self.__create_edges()
        return self.__edges

    def __create_edges(self):
        if self.__indexes is None:
            return None

        dist = set()
        dup = set()

        for i in range(0, len(self.indexes), 3):
            a = Edge(self.indexes[i + 0], self.indexes[i + 1])
            b = Edge(self.indexes[i + 1], self.indexes[i + 2])
            c = Edge(self.indexes[i + 2], self.indexes[i + 0])

            if a in dist:
                dup.add(a)
            else:
                dist.add(a)
            if b in dist:
                dup.add(b)
            else:
                dist.add(b)
            if c in dist:
                dup.add(c)
            else:
                dist.add(c)

        dist = dist.difference(dup)
        dist = list(dist)
        self.__edges = dist

    def __getitem__(self, item):
        return self.indexes[item]

    def __str__(self):
        return f"[Indexes: {self.indexes}, Edges: {self.edges}]"

    def __repr__(self):
        return f"Face: {str(self)}"
