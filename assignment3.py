# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from camera import Camera
from shapes import *
from input_controller import InputController
from mat3d import *
from transform import Transform

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.

ESCAPE = '\033'

# Number of the glut window.
window = 0

old_time_since_start = 0

cube2 = Shape(Cube(Vec3d(3, 2, 1)), transform=Transform(Vec3d(4, 0, 4)))
cube = Shape(Cube(Vec3d(1, 1, 1)))
sphere = Shape(IcoSphere(), transform=Transform(Vec3d(-4, 0, -1)))
plane = Shape(Plane(2, 2, 2, 2), transform=Transform(Vec3d(3, 0, -2), Vec3d(45, 0, 0)))
cylinder = Shape(Cylinder(), transform=Transform(Vec3d(2, 0, 0)))
camera = Camera()

shapes = [cube, cylinder, plane, sphere]
active_shape = shapes[0]
target_y = 0


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)  # This Will Clear The Background Color To Black
    glClearDepth(1.0)  # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)  # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)  # Enables Depth Testing
    glShadeModel(GL_SMOOTH)  # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()  # Reset The Projection Matrix
    # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:  # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)  # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width) / float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


def elapsed_time():
    time_since_start = glutGet(GLUT_ELAPSED_TIME)
    global old_time_since_start
    delta_time = time_since_start - old_time_since_start
    old_time_since_start = time_since_start
    return delta_time


# The main drawing function.
def DrawGLScene():
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset The View

    # glEnable(GL_DEPTH_TEST);
    # glDepthFunc(GL_LESS);
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
    # glMatrixMode(GL_MODELVIEW)

    delta_time = elapsed_time()
    camX = math.sin(time.time()) * 12
    camZ = math.cos(time.time()) * 12
    # gluLookAt(0, 5, -10, 0, target_y, 0, 0, 1, 0)
    camera.update()
    for shape in shapes:
        shape.draw()
    cube2.transform.look_at(cube.transform.position)
    cube2.draw()

    # triangle2.draw()
    # triangle.draw()
    # cube.draw()
    # sphere.draw()
    # cylinder.draw()

    # modelViewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    # glLoadMatrixf(modelViewMatrix)

    glColor(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(-100, 100, 1):
        glVertex3f(i, 0, 100)
        glVertex3f(i, 0, -100)
        glVertex3f(100, 0, i)
        glVertex3f(-100, 0, i)
        # glVertex3f(0, 100, i)
        # glVertex3f(0, -100, i)
        # glVertex3f(0, i, -100)
        # glVertex3f(0, i, 100)
    glEnd()

    # glRasterPos2f(-6,4)
    # print(delta_time)
    # for character in str("FPS:" + str((int(1 /(delta_time / 1000))))):
    #     glutBitmapCharacter(GLUT.GLUT_BITMAP_9_BY_15, ord(character))
    glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(*args):
    # If escape is pressed, kill everything.
    print(args[0])
    if args[0] == ESCAPE:
        sys.exit()


def change_active_shape(type):
    if type == "up":
        inc = 1
    else:
        inc = -1
    global active_shape
    index = shapes.index(active_shape)
    active_shape = shapes[(index + inc) % len(shapes)]


def translate_target(x, z):
    active_shape.transform.translate(Vec3d(x, 0, z))


def focus_active_shape():
    camera.transform.look_at(active_shape.transform.position)


def subdivide_active_object(type):
    print("pressed")
    if active_shape.mesh.can_subdivide:
        if type == "subdivide":
            new_mesh = active_shape.mesh.subdivide()
        else:
            new_mesh = active_shape.mesh.unsubdivide()
        active_shape.mesh = new_mesh


def rotation_around_object(x_offset, y_offset):
    up = camera.transform.up * y_offset
    right = camera.transform.right * x_offset
    camera.transform.position += (-up + right) / 100
    camera.transform.look_at(active_shape.transform.position)


def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    # Alpha components supported
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)
    window = glutCreateWindow("CENG487 Template")

    # Display Func
    glutDisplayFunc(DrawGLScene)

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    input_controller = InputController(camera)
    input_controller.on_arrow_clicked = translate_target
    input_controller.on_mouse_wheel_event = change_active_shape
    input_controller.on_f_clicked = focus_active_shape
    input_controller.on_plus_subtract_clicked = subdivide_active_object
    input_controller.on_alt_left_event = rotation_around_object

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
print("Mouse wheel click to move camera to any direction")
print("Alt + Mouse Right Click to zoom in looking direction")
print("Mouse Right Click to rotate camera to look around")
print("Alt + Mouse Left Click to rotate around selected object")
print("F to focus camera on selected object")
print("Mouse Wheel Down and Up to change selected object")
print("Arrow keys to move selected object in x and z axises")
print("+ - to subdivide selected object if object supports. ")
print("Bigger cube will follow him, bigger cube can not be selected")
main()
