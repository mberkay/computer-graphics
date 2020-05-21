# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from typing import List

from OpenGL.GL import *

from camera import Camera
from lights.light import Light
from shapes import Shape, Grid


class DrawMode:
    SHADED = 0
    WIRED = 1
    WIRED_SHADED = 2
    modes = [SHADED, WIRED, WIRED_SHADED]  # Is it necessary?


class Scene:
    def __init__(self):
        self.__cameras = []
        self.__shapes = []
        self.__lights = []
        self.__active_camera = None
        self.__selected_shapes = []
        self.__draw_mode = DrawMode.SHADED
        self.should_animate = True
        self.grid = None

    def display_core(self):
        self.active_camera.update()
        view_matrix = self.active_camera.view_matrix
        project_matrix = self.active_camera.project_matrix

        if self.grid is not None:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            self.grid.draw_core(view_matrix, project_matrix)

        if self.draw_mode is DrawMode.SHADED or self.draw_mode is DrawMode.WIRED_SHADED:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            for shape in self.__shapes:
                shape.draw_core(view_matrix, project_matrix)

        if self.draw_mode is DrawMode.WIRED or self.draw_mode is DrawMode.WIRED_SHADED:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            for shape in self.__shapes:
                shape.draw_core(view_matrix, project_matrix)


    def display(self):
        # glEnable(GL_NORMALIZE)
        # Update camera transform and render
        self.active_camera.update()
        glEnable(GL_LIGHTING)
        # Draw shapes respect to draw mode
        if self.draw_mode is DrawMode.SHADED or self.draw_mode is DrawMode.WIRED_SHADED:
            glPolygonMode(GL_FRONT, GL_FILL)
            for shape in self.__shapes:
                shape.draw()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self.draw_mode is DrawMode.WIRED or self.draw_mode is DrawMode.WIRED_SHADED:
            glDisable(GL_LIGHTING)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glLineWidth(2)
            for shape in self.__shapes:
                if shape in self.selected_shapes:
                    glColor3f(1, 1, 0)
                else:
                    glColor3f(0, 0, 0)
                shape.draw()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            # glEnable(GL_LIGHTING)

        for light in self.__lights:
            light.light()

        if self.should_animate:
            try:
                self.__lights[0].animate()
            except:
                self.should_animate = False

        #  Draw subdivision level to screen
        # # TODO fix positioning
        # a = glGetFloat(GL_CURRENT_RASTER_POSITION)
        # print(a)
        # glLoadIdentity()
        # if len(self.selected_shapes) > 0:
        #     glColor3f(0, 0, 0)
        #     glRasterPos3f(5, 5, 5)
        #     text = str(f"Subdivision Level: {self.selected_shapes[-1].mesh.subdivision_level}")
        #     # print(text)
        #     for character in text:
        #         glut.glutBitmapCharacter(glut.GLUT_BITMAP_HELVETICA_18, ord(character))

    def add_shape(self, shape):
        self.__shapes.append(shape)

    def remove_shape(self, shape: Shape):
        if shape in self.__shapes:
            self.__shapes.remove(shape)

    def get_shapes(self):
        return list(filter(lambda x: isinstance(x, Shape), self.__shapes))

    def add_light(self, light: Light):
        self.__lights.append(light)

    def remove_light(self, light: Light):
        if light in self.__lights:
            self.__lights.remove(Light)

    def get_lights(self):
        return self.__lights

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
