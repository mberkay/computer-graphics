# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from os.path import exists, splitext, isfile

from face import Face
from mesh import Mesh
from shapes import Shape
from vec3d import Point


class ObjParser(object):

    @staticmethod
    def parse(file_path):
        if not exists(file_path):
            raise FileNotFoundError(f"No such file or directory: {file_path}")
        if not isfile(file_path):
            raise ValueError(f"{file_path} is not a file")
        _, extension = splitext(file_path)
        if extension != ".obj":
            raise ValueError(f"Expected .obj file but get {extension} file")

        name = None
        vertices = []
        faces = []
        groups = {}
        current_group = []
        groups["default"] = current_group
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("o"):
                    name = line
                elif line.startswith("g"):
                    values = line.split()
                    group_name = values[1]
                    if group_name not in groups:
                        current_group = []  # Create new group
                        groups[group_name] = current_group  # Save group to groups
                    else:
                        current_group = groups[group_name]

                elif line.startswith("v"):
                    # current_group["vertices"].append(create_point(line))
                    vertices.append(create_point(line))

                elif line.startswith("f"):
                    current_group.append(create_face(line))
                    # faces.append(create_face(line))
        # return name, vertices, faces
        shapes = []
        for group in groups:
            if len(groups[group]) is not 0:
                mesh = Mesh(vertices.copy(), groups[group])
                min_index = min(mesh.indexes)
                max_index = max(mesh.indexes)
                mesh.positions = mesh.positions[min_index:max_index + 1]
                for face in mesh.faces:
                    face.indexes = list(map(lambda x: x - min_index, face.indexes))
                mesh.invalidate_indexes()

                shapes.append(Shape(group, mesh))
        return shapes


# TODO more error checking
def create_point(line):
    values = line.split()
    if len(values) is not 4:
        raise ValueError(f"Invalid vertex definition {line}")
    return Point(float(values[1]), float(values[2]), float(values[3]))


def create_face(line):
    values = line.split()

    if len(values) is 5:  # Quads
        return Face([int(values[4]) - 1, int(values[3]) - 1, int(values[2]) - 1,
                     int(values[4]) - 1, int(values[2]) - 1, int(values[1]) - 1])
    elif len(values) is 4:  # Triangles
        return Face([int(values[1]) - 1, int(values[2]) - 1, int(values[3]) - 1])
    else:
        raise ValueError(f"Invalid face definition {line}")


if __name__ == '__main__':
    # name, vertices, faces = ObjParser.parse("./cornell.obj")
    # shapes = ObjParser.parse("./cornell.obj")
    shapes = ObjParser.parse("./tori2.obj")

    print(shapes)
