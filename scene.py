# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019


import OpenGL.GLUT as glut
from camera import Camera
from OpenGL.GL import *

from shapes import Shape
from typing import List


class DrawMode:
    SHADED = 0
    WIRED = 1
    WIRED_SHADED = 2
    modes = [SHADED, WIRED, WIRED_SHADED]  # Is it necessary?


class Scene:
    def __init__(self):
        self.__cameras = []
        self.__shapes = []
        self.__active_camera = None
        self.__selected_shapes = []
        self.__draw_mode = DrawMode.SHADED

    def display(self):
        # Update camera transform and render
        self.active_camera.update()

        # Draw shapes respect to draw mode
        if self.draw_mode is DrawMode.SHADED or self.draw_mode is DrawMode.WIRED_SHADED:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            for shape in self.__shapes:
                shape.draw_winged(False)

        if self.draw_mode is DrawMode.WIRED or self.draw_mode is DrawMode.WIRED_SHADED:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(2)
            for shape in self.__shapes:
                if shape in self.selected_shapes:
                    glColor3f(1, 1, 0)
                else:
                    glColor3f(0, 0, 0)
                shape.draw_winged(True)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # # TODO fix positioning
        # a = glGetFloat(GL_CURRENT_RASTER_POSITION)
        # # print(a)
        # if len(self.selected_shapes) > 0:
        #     glColor3f(0, 0, 0)
        #     glRasterPos3f(0, 0, 0)
        #     text = str(f"Subdivision Level: {self.selected_shapes[-1].mesh.subdivision_level}")
        #     # print(text)
        #     for character in text:
        #         glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(character))

    def add_shape(self, shape: Shape):
        self.__shapes.append(shape)

    def remove_shape(self, shape: Shape):
        if shape in self.__cameras:
            self.__shapes.remove(shape)

    def add_camera(self, camera: Camera):
        self.__cameras.append(camera)

    def remove_camera(self, camera: Camera):
        if camera in self.__cameras:
            self.__cameras.remove(camera)

    def add_shape_to_selected_shapes(self, shape: Shape):
        self.__selected_shapes.append(shape)

    def remove_shape_from_selected_shapes(self, shape: Shape):
        if shape in self.__selected_shapes:
            self.__selected_shapes.remove(shape)

    @property
    def shapes(self):
        if len(self.__shapes) is 0:
            raise Exception("There are no shape in scene")
        return self.__shapes

    @property
    def selected_shapes(self) -> List[Shape]:
        return self.__selected_shapes

    @selected_shapes.setter
    def selected_shapes(self, value: List[Shape]):
        self.__selected_shapes = value

    @property
    def draw_mode(self):
        return self.__draw_mode

    @draw_mode.setter
    def draw_mode(self, draw_mode):
        if draw_mode in DrawMode.modes:
            self.__draw_mode = draw_mode

    @property
    def active_camera(self) -> Camera:
        if self.__active_camera is None:
            if len(self.__cameras) is 0:
                raise Exception("There are no camera to render, please add a camera to scene")
            self.__active_camera = self.__cameras[0]
        return self.__active_camera
