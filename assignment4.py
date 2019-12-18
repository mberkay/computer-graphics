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
from catmull_clark import catmull_clark, cmc_subdiv
from obj_parser import ObjParser
from scene import Scene
from shapes import *
from input_controller import InputController
from mat3d import *
from transform import Transform
from mesh import *
from face import Face
from cube import Cube as cb
from experimentalplane import PlaneExperimental

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
from winged_edge.winged_edge_converter import indexed_face_set_to_winged_edge

ESCAPE = '\033'

# Number of the glut window.
window = 0

old_time_since_start = 0

scene = Scene()
camera = Camera()
scene.add_camera(camera)

if len(sys.argv) > 1:
    name, points, faces = ObjParser.parse(sys.argv[1])
    read_mesh = Mesh(points, faces)
    read_shape = Shape(read_mesh)

    winged_mesh = indexed_face_set_to_winged_edge(read_mesh)
    wiinged_shape = Shape(winged_mesh)

    catmull_clark(winged_mesh)
    # cmc_subdiv(winged_mesh)
    scene.add_shape(wiinged_shape)


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):  # We call this right after our OpenGL window is created.
    glClearColor(0.2, 0.2, 0.2, 0.0)  # This Will Clear The Background Color To Black
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
    scene.display()
    # test7.draw(False)
    delta_time = elapsed_time()

    # TODO fix Depth bug
    glBegin(GL_LINES)
    glColor(0, 0, 1)
    glVertex3f(0, 0, 100)
    glVertex3f(0, 0, -100)
    glColor(1, 0, 0)
    glVertex3f(100, 0, 0)
    glVertex3f(-100, 0, -0)
    glColor(0.3, 0.3, 0.3)
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

    glutSwapBuffers()


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
    input_controller = InputController(scene)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()


# Print message to console, and kick off the main to get it rolling.
print("Hit ESC key to quit.")
print("Camera Controls:")
print("Mouse wheel click to move camera to any direction")
print("Alt + Mouse Right Click to zoom in looking direction")
print("Mouse Right Click to rotate camera to look around")
print("Alt + Mouse Left Click to rotate camera around selected object")
print("F to focus camera on selected object")
print("R to reset camera")

print("Shape Controls:")
print("0-9 Numbers to select/deselect shapes, using alt can select multiple shapes")
print("Arrow keys to move selected objects in x and z axises")
print("+ - to subdivide or undo subdivision of selected shapes")
print("'Q' to change face type of selected shapes to QUAD if shape supports")
print("'T' to change face type of selected shapes to TRIANGLE")

print("Scene Controls:")
print("'W' to traverse between draw modes")
print("\033[93m" + "***")
print("READ ME: Implemented half edge and 'indexed face set' to 'half edge' converter, have a bug in catmull clark that i couldn't continue. I will fix and complete it asap")
print("***")

# print("Bigger cube will follow him, bigger cube can not be selected")
main()
