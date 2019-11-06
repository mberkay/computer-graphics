# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

from OpenGL.GLUT import *


class InputController:
    def __init__(self, camera):
        glutKeyboardFunc(self.process_keyboard_input)
        glutSpecialFunc(self.process_special_input)
        glutSpecialUpFunc(self.process_special_input_up)
        glutMouseFunc(self.process_mouse_input)
        glutMotionFunc(self.drag)

        self.camera = camera
        self.on_arrow_clicked = None
        self.on_plus_subtract_clicked = None
        self.on_f_clicked = None
        self.on_mouse_wheel_event = None
        self.on_alt_left_event = None

        self.is_alt_pressed = False
        self.is_left_click_pressed = False
        self.is_right_click_pressed = False
        self.is_mouse_wheel_click_pressed = False

        self.previous_x = 0
        self.previous_y = 0
        self.camera_sensitivity = 1

    def drag(self, x, y):
        x_offset = x - self.previous_x
        y_offset = self.previous_y - y  # Reversed since window coordinates start from top left corner
        if self.is_mouse_wheel_click_pressed:
            up = self.camera.transform.up * self.camera_sensitivity * y_offset
            right = self.camera.transform.right * self.camera_sensitivity * x_offset
            self.camera.transform.position += (-up + right) / 100

        elif self.is_right_click_pressed:
            # alt + Right Click
            if self.is_alt_pressed:
                if x > self.previous_x or y > self.previous_y:
                    self.camera.transform.position += self.camera.transform.forward / 10
                else:
                    self.camera.transform.position -= self.camera.transform.forward / 10
            else:
                right = x_offset / 10
                up = y_offset / 10
                self.camera.transform.rotate_axis(self.camera.transform.right, up)
                self.camera.transform.rotate_axis(self.camera.transform.up, right)

            # alt + Left Click
        elif self.is_left_click_pressed and self.is_alt_pressed:
            self.on_alt_left_event(x_offset, y_offset)
            # focus = Vec3d(0, 0, 0)
            # up = self.camera.transform.up * self.camera_sensitivity * y_offset
            # right = self.camera.transform.right * self.camera_sensitivity * x_offset
            # self.camera.transform.position += (-up + right) / 100
            # self.camera.transform.look_at(focus)
            # # print("left", x - self.previous_x, y - self.previous_y)

        self.previous_x = x
        self.previous_y = y

    def process_keyboard_input(self, key, x, y):
        if key == b'+':
            self.on_plus_subtract_clicked("subdivide")
        elif key == b'-':
            self.on_plus_subtract_clicked("unsubdivide")
        elif key == b'f':
            self.on_f_clicked()
        elif key == b'r':
            self.camera.reset()

    def process_special_input(self, key, x, y):
        if key == 100:
            self.on_arrow_clicked(-1, 0)
            # print("left")
        elif key == 101:
            # print("up")
            self.on_arrow_clicked(0, 1)
        elif key == 102:
            # print("right")
            self.on_arrow_clicked(1, 0)
        elif key == 103:
            # print("down")
            self.on_arrow_clicked(0, -1)
        elif key == 116:
            # print("alt")
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
        if button == 3 and state == 1:
            self.on_mouse_wheel_event("up")
        elif button == 4 and state == 1:
            self.on_mouse_wheel_event("down")
