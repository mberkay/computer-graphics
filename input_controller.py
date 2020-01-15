# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from OpenGL.GLUT import *

from mesh import FaceType
from scene import DrawMode
from shapes import Shape
from vec3d import Vec3d, Point


class InputController:
    def __init__(self, scene):
        glutKeyboardFunc(self.process_keyboard_input)
        glutSpecialFunc(self.process_special_input)
        glutSpecialUpFunc(self.process_special_input_up)
        glutMouseFunc(self.process_mouse_input)
        glutMotionFunc(self.drag)

        self.scene = scene
        # self.on_arrow_clicked = None
        # self.on_plus_subtract_clicked = None
        # self.on_f_clicked = None
        # self.on_w_clicked = None
        # self.on_mouse_wheel_event = None
        # self.on_alt_left_event = None

        self.is_alt_pressed = False
        self.is_left_click_pressed = False
        self.is_right_click_pressed = False
        self.is_mouse_wheel_click_pressed = False

        self.previous_x = 0
        self.previous_y = 0
        self.camera_sensitivity = 1

    def drag(self, x, y):
        camera = self.scene.active_camera
        x_offset = x - self.previous_x
        y_offset = self.previous_y - y  # Reversed since window coordinates start from top left corner
        if self.is_mouse_wheel_click_pressed:
            up = camera.transform.up * self.camera_sensitivity * y_offset
            right = camera.transform.right * self.camera_sensitivity * x_offset
            camera.transform.position += (-up + right) / 100

        elif self.is_right_click_pressed:
            # alt + Right Click is Zoom
            if self.is_alt_pressed:
                if x > self.previous_x or y > self.previous_y:
                    camera.transform.position += camera.transform.forward / 10
                else:
                    camera.transform.position -= camera.transform.forward / 10
            # Right Click to look around
            else:
                right = x_offset / 10
                up = y_offset / 10
                camera.transform.rotate_axis(camera.transform.right, up)
                camera.transform.rotate_axis(camera.transform.up, right)

            # alt + Left Click is Rotate camera around focus shape
        elif self.is_left_click_pressed and self.is_alt_pressed:
            focus_point = self.find_focus_point()
            up = camera.transform.up * y_offset
            right = camera.transform.right * x_offset
            camera.transform.position += (-up + right) / 100
            camera.transform.look_at(focus_point)

        self.previous_x = x
        self.previous_y = y

    def process_keyboard_input(self, key, x, y):
        if key == b'+':
            # Subdivide
            self.subdivide_selected_shapes(1)
        elif key == b'-':
            # Revert subdivision
            self.subdivide_selected_shapes(-1)
        elif key == b'f':
            self.focus_active_shape()
        elif key == b'r':
            self.scene.active_camera.reset()
        elif key == b'w':
            self.change_draw_mode()
        elif key == b'q':
            self.change_face_type_of_selected_shapes(FaceType.QUAD)
        elif key == b't':
            self.change_face_type_of_selected_shapes(FaceType.TRIANGLE)
        elif key == b'a':
            # self.animate_light()
            self.scene.should_animate = not self.scene.should_animate
        elif key == b'g':
            for shape in self.scene.get_shapes():
                shape.should_draw_normals = not shape.should_draw_normals
        elif b'0' <= key <= b'9':
            self.change_selected_shapes(int(key))
        elif key == b'\x1b':
            sys.exit()

    def process_special_input(self, key, x, y):
        # Left Arrow
        if key == 100:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(0, -5)
            else:
                self.translate_selected_shapes(-1, 0)
        # Up Arrow
        elif key == 101:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(5, 0)
            else:
                self.translate_selected_shapes(0, 1)
        # Right Arrow
        elif key == 102:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(0, 5)
            else:
                self.translate_selected_shapes(1, 0)
        # Down Arrow
        elif key == 103:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(-5, 0)
            else:
                self.translate_selected_shapes(0, -1)
        # Alt
        elif key == 116:
            self.is_alt_pressed = True

    def process_special_input_up(self, key, x, y):
        if key == 116:
            # print("alt")
            self.is_alt_pressed = False

    def process_mouse_input(self, button, state, x, y):
        if button == 0:
            self.is_left_click_pressed = state is 0
            self.previous_x = x
            self.previous_y = y
        if button == 2:
            self.is_right_click_pressed = state is 0
            self.previous_x = x
            self.previous_y = y
        if button == 1:
            self.is_mouse_wheel_click_pressed = state is 0
            self.previous_x = x
            self.previous_y = y
        # Mouse wheel up
        if button == 3 and state == 1:
            pass
        # Mouse wheel down
        elif button == 4 and state == 1:
            pass

    def change_face_type_of_selected_shapes(self, face_type):
        for shape in self.scene.selected_shapes:
            if isinstance(shape, Shape):
                shape.mesh.face_type = face_type

    def change_draw_mode(self):
        draw_mode = self.scene.draw_mode
        self.scene.draw_mode = DrawMode.modes[(draw_mode + 1) % len(DrawMode.modes)]

    def translate_selected_shapes(self, x, z):
        for shape in self.scene.selected_shapes:
            shape.transform.translate(Vec3d(x, 0, z))

    def rotate_selected_shapes(self, up, right):
        for shape in self.scene.selected_shapes:
            shape.transform.rotate_axis(shape.transform.right, up)
            shape.transform.rotate_axis(shape.transform.up, right)

    def subdivide_selected_shapes(self, type):
        for shape in self.scene.selected_shapes:
            shape.mesh.subdivide(type)
            # shape.mesh.subdivide2(type)

    def focus_active_shape(self):
        focus_point = self.find_focus_point()
        self.scene.active_camera.transform.look_at(focus_point)

    def find_focus_point(self):
        selected_shapes = self.scene.selected_shapes
        focus_point = Point(0, 0, 0)
        if len(selected_shapes) is not 0:
            focus_point = selected_shapes[-1].transform.position
        return focus_point

    def change_selected_shapes(self, key):
        # Can select that shape
        if key > len(self.scene.shapes) - 1:
            return

        shape = self.scene.shapes[key]
        if self.is_alt_pressed:
            if shape in self.scene.selected_shapes:
                self.scene.remove_shape_from_selected_shapes(shape)
            else:
                self.scene.add_shape_to_selected_shapes(shape)
        else:
            if len(self.scene.selected_shapes) is 1 and self.scene.selected_shapes[0] is shape:
                self.scene.remove_shape_from_selected_shapes(shape)
            else:
                self.scene.selected_shapes = [shape]
