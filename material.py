# CENG 487 Assignment5 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 12 2019
from OpenGL.GL import *

from vec3d import Vec3d


class Material:
    def __init__(self, ambient, diffuse, specular, shine):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shine = shine

    def apply(self):
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, self.shine)


# Source: http://www.it.hiof.no/~borres/j3d/explain/light/p-materials.html
yellow_rubber = Material(ambient=[.05, .05, 0, 1],
                         diffuse=[.4, .5, .4, 1],
                         specular=[.7, .7, .04, 1],
                         shine=10)

green_rubber = Material(ambient=[0, .05, 0, 1],
                        diffuse=[.4, .5, .4, 1],
                        specular=[.04, .7, .04, 1],
                        shine=10)

red_rubber = Material(ambient=[.05, 0, 0, 1],
                      diffuse=[.5, .4, .4, 1],
                      specular=[.7, .04, .04, 1],
                      shine=10)

red = Material(ambient=[0, 0, 0, 1],
               diffuse=[1, 0, 0, 1],
               specular=[.0225, .0225, .0225, 1],
               shine=12.8)
# TODO add more material
