# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019


class Edge:
    def __init__(self, a: int, b: int):
        self.a = a
        self.b = b

    def is_valid(self):
        return self.a > -1 and self.b > -1 and self.a is not self.b

    def contains_index(self, index: int):
        """
        Does this edge contain an index
        :return: True if a or b is equal to index
        """
        return self.a is index or self.b is index

    def contains_edge(self, other):
        """
        Does this edge contain any index of edge
        :return: True if a or b is equal to a or b of edge
        """
        if isinstance(other, Edge):
            return self.contains_index(other.a) or self.contains_index(other.b)

    @staticmethod
    def get_indexes(edges):
        if type(edges) is not list:
            raise ValueError("Edges should be list of Edge ")
        indexes = []
        for edge in edges:
            if type(edge) is not Edge:
                raise ValueError("Edges should contain only Edge ")
            indexes.append(edge.a)
            indexes.append(edge.b)

    def __add__(self, other):
        if type(other) is Edge:
            return Edge(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        if type(other) is Edge:
            return Edge(self.a - other.a, self.b - other.b)

    def __eq__(self, other):
        return type(other) is Edge and (self.a is other.a and self.b is other.b) or (
                    self.a is other.b and self.b is other.a)

    def __hash__(self):
        # Overriding __eq__ brokes the __hash__
        # https: // stackoverflow.com / questions / 1608842 / types - that - define - eq - are - unhashable
        # Solution
        # http://stackoverflow.com/questions/263400/what-is-the-best-algorithm-for-an-overridden-system-object-gethashcode/263416#263416
        # (1,2) and (2,1) hash should be same so first multiply with the small one then bigger
        if self.a < self.b:
            first = self.a
            second = self.b
        else:
            first = self.b
            second = self.a
        h = 13 * 7 + first
        h = h * 7 + second
        return h

    def __str__(self):
        return f"[{self.a}, {self.b}]"

    def __repr__(self):
        return f"Edge{str(self)}"

    @staticmethod
    def empty():
        return Edge(-1, -1)
