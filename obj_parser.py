# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from os.path import exists, splitext, isfile

from face import Face
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
        with open(file_path, "r") as file:
            for line in file:
                if line.startswith("o"):
                    name = line
                elif line.startswith("v"):
                    vertices.append(create_point(line))
                elif line.startswith("f"):
                    faces.append(create_face(line))
        return name, vertices, faces


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
    name, vertices, faces = ObjParser.parse("./tori.obj")
