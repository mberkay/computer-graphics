# CENG 487 Assignment4 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
from face import Face
from mesh import Mesh
from vec3d import Vec3d, Point


# https://www.youtube.com/watch?v=sLEIpmPEDAY
class PlaneExperimental(Mesh):
    def __init__(self, resolution, local_up):
        positions = []
        faces = []

        axis_a = Vec3d(local_up.y, local_up.z, local_up.x)
        axis_b = local_up.cross(axis_a)
        for y in range(resolution):
            for x in range(resolution):
                i = x + y * resolution
                percent = Vec3d(x, y, 0) / (resolution - 1)
                vector_on_unit_cube = local_up + (axis_a * (percent.x - .5) * 2) + (percent.y - .5) * 2 * axis_b
                point_on_unit_cube = Point(vector_on_unit_cube.x, vector_on_unit_cube.y, vector_on_unit_cube.z)

                point_on_unit_sphere = point_on_unit_cube.normalized
                positions.append(point_on_unit_sphere)
                if x is not resolution - 1 and y is not resolution - 1:
                    faces.append(Face([i, i + resolution + 1, i + resolution,
                                       i, i + 1, i + resolution + 1]))

        super().__init__(positions, faces)
