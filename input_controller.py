# CENG 488 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 05 2020

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

        self.is_alt_pressed = False
        self.is_ctrl_pressed = False
        self.is_left_click_pressed = False
        self.is_right_click_pressed = False
        self.is_mouse_wheel_click_pressed = False

        self.previous_x = 0
        self.previous_y = 0
        self.camera_sensitivity = 1
        self.camera_zoom_sensitivity = 1

    def drag(self, x, y):
        camera = self.scene.active_camera
        x_offset = x - self.previous_x
        y_offset = self.previous_y - y  # Reversed since window coordinates start from top left corner

        # Middle mouse click control
        if self.is_mouse_wheel_click_pressed:
            up = camera.transform.up * self.camera_sensitivity * y_offset
            right = camera.transform.right * self.camera_sensitivity * -x_offset
            camera.transform.position += (-up + -right) / 100

        elif self.is_right_click_pressed:
            # alt + Right Click is Zoom
            if self.is_alt_pressed:
                if x > self.previous_x or y > self.previous_y:
                    self.zoom_active_camera(1)  # Forward
                else:
                    self.zoom_active_camera(-1)  # Back
            # Right Click to look around
            else:
                right = x_offset / 10
                up = y_offset / 10
                self.rotate_active_camera(up, right)

            # alt + Left Click is Rotate camera around focus shape
        elif self.is_left_click_pressed and self.is_alt_pressed:
            focus_point = self.find_focus_point()
            camera.transform.rotate_around(focus_point, camera.transform.right, -y_offset)
            camera.transform.rotate_around(focus_point, Vec3d.up(), x_offset)

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
        elif key == b'k':
            # self.scene.active_camera.transform.rotate_around(Vec3d(0,0,0), self.scene.active_camera.transform.right, 1)
            self.scene.shapes[0].transform.rotate_around(Point(0,0,0), self.scene.shapes[0].transform.right, 5)
            self.scene.shapes[0].transform.look_at(Point(0,0,0))
        elif key == b'l':
            self.scene.shapes[0].transform.rotate_around(Point(0, 0, 0), Vec3d.up(), 5)
            self.scene.shapes[0].transform.look_at(Point(0,0,0))
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
            elif self.is_ctrl_pressed:
                self.rotate_active_camera(0, -5)
            else:
                self.translate_selected_shapes(-1, 0)
        # Up Arrow
        elif key == 101:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(5, 0)
            elif self.is_ctrl_pressed:
                self.rotate_active_camera(5, 0)
            else:
                self.translate_selected_shapes(0, 1)
        # Right Arrow
        elif key == 102:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(0, 5)
            elif self.is_ctrl_pressed:
                self.rotate_active_camera(0, 5)
            else:
                self.translate_selected_shapes(1, 0)
        # Down Arrow
        elif key == 103:
            if self.is_alt_pressed:
                self.rotate_selected_shapes(-5, 0)
            elif self.is_ctrl_pressed:
                self.rotate_active_camera(-5, 0)
            else:
                self.translate_selected_shapes(0, -1)
        # Alt
        elif key == 116:
            self.is_alt_pressed = True
        # LCtrl
        elif key == 114:
            self.is_ctrl_pressed = True

    def process_special_input_up(self, key, x, y):
        if key == 116:
            # print("alt")
            self.is_alt_pressed = False
        if key == 114:
            self.is_ctrl_pressed = False

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
            self.zoom_active_camera(1)
            pass
        # Mouse wheel down
        elif button == 4 and state == 1:
            self.zoom_active_camera(-1)
            pass

    def change_face_type_of_selected_shapes(self, face_type):
        for shape in self.scene.selected_shapes:
            if isinstance(shape, Shape):
                shape.mesh.face_type = face_type

    def change_draw_mode(self):
        draw_mode = self.scene.draw_mode
        self.scene.draw_mode = DrawMode.modes[(draw_mode + 1) % len(DrawMode.modes)]

    def translate_selected_shapes(self, right, forward):
        for shape in self.scene.selected_shapes:
            shape.transform.translate(shape.transform.forward * forward + shape.transform.right * right)

    def rotate_active_camera(self, up, right):
        cam = self.scene.active_camera.transform
        cam.rotate_axis(cam.right, up)
        cam.rotate_axis(Vec3d.up(), -right)

    def zoom_active_camera(self, direction):
        cam = self.scene.active_camera.transform
        cam.position += direction * cam.forward * self.camera_zoom_sensitivity

    def rotate_selected_shapes(self, up, right):
        for shape in self.scene.selected_shapes:
            shape.transform.rotate_axis(shape.transform.right, up)
            shape.transform.rotate_axis(shape.transform.up, -right)

    def subdivide_selected_shapes(self, type):
        for shape in self.scene.selected_shapes:
            shape.mesh.subdivide(type)

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
