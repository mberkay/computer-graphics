# CENG 487 Assignment3 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 11 2019

# Note:
# -----
# This Uses PyOpenGL and PyOpenGL_accelerate packages.  It also uses GLUT for UI.
# To get proper GLUT support on linux don't forget to install python-opengl package using apt
import time

from OpenGL.GLU import *
from OpenGL.GLUT import *

from camera import Camera
from input_controller import InputController
from lights import *
from mat3d import *
from material import *
from obj_parser import ObjParser
from scene import Scene
from transform import Transform


# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
ESCAPE = '\033'

# Number of the glut window.
window = 0

old_time_since_start = 0

scene = Scene()
camera = Camera()
scene.add_camera(camera)

if len(sys.argv) > 1:
    shapes = ObjParser.parse(sys.argv[1])
    for shape in shapes:
        if shape.name == "ShortBox" or shape.name == "TallBox" or shape.name == "Ceiling" or shape.name == "Floor" or shape.name == "BackWall":
            shape.material = yellow_rubber
        elif shape.name == "RightWall":
            shape.material = red_rubber
        elif shape.name == "LeftWall":
            shape.material = green_rubber
        shape.transform = Transform(scale=Vec3d(0.1, 0.1, 0.1), rotation=Vec3d(0, 180, 0))
        scene.add_shape(shape)

# cube = Shape(Cube(), Transform(position=Vec3d(-10,-10,10), rotation=Vec3d(0, -0, 0), scale=Vec3d(1,1,1)))
# cube = Shape("cube", Cube())
# cube.material = green_rubber
# scene.add_shape(cube)
# light = DirectionalLight(ambient=[0.2, 0.2, 0.2, 1],
#                   diffuse=[1, 1, 1, 1],
#                   specular=[1, 1, 1, 1],
#                   transform=Transform(position=Vec3d(0, 0, -5), rotation=Vec3d(0, 0, 0)))

light = SpotLight(ambient=[0.2, 0.2, 0.2, 1],
                  diffuse=[1, 1, 1, 1],
                  specular=[1, 1, 1, 1],
                  angle=30,
                  distance=20,
                  transform=Transform(position=Vec3d(0, 0, -5), rotation=Vec3d(0, 0, 0)))
scene.add_shape(light)
scene.add_light(light)

light2 = SpotLight(ambient=[0.2, 0.2, 0.2, 1],
                   diffuse=[1, 1, 1, 1],
                   specular=[1, 1, 1, 1],
                   angle=15,
                   distance=20,
                   transform=Transform(position=Vec3d(0, 10, 1), rotation=Vec3d(100, 0, 0)))
scene.add_shape(light2)
scene.add_light(light2)


# light2 = DirectionalLight(ambient=[0.2, 0.2, 0.2, 1],
#               diffuse=[1, 0, 0, 1],
#               specular=[1, 1, 1, 1],
#               transform=Transform(position=Vec3d(0, 0, 0), rotation=Vec3d(0, 0, 0)))
# scene.add_shape(light2)
# scene.add_light(light2)

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
    # test7.draw(False)
    delta_time = elapsed_time()
    math.sin(time.time()) * 10
    mat_specular = [1.0, 1.0, 1.0, 1.0]

    mat_shininess = [50.0]

    time.time()
    # light_position = [math.sin(time.time()) *10, 0, math.cos(time.time()) *10, 0]
    light_position = [1, 0, 0, 0]
    # cube.transform.position = Vec3d(math.sin(time.time()) *10, 0, math.cos(time.time()) *10)
    # glClearColor(0.0, 0.0, 0.0, 0.0)
    # glShadeModel(GL_SMOOTH)

    # glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    # glMaterialfv(GL_BACK, GL_SHININESS, mat_shininess)
    # glLoadIdentity()

    scene.display()
    # glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    # glEnable(GL_LIGHT0)
    # glPolygonMode(GL_FRONT_FACE, GL_)
    # glEnable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
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
print(f"{bcolors.HEADER} Camera Controls:{bcolors.ENDC}")
print("Mouse wheel click to move camera to any direction")
print("Alt + Mouse Right Click to zoom in looking direction")
print("Mouse Right Click to rotate camera to look around")
print("Alt + Mouse Left Click to rotate camera around selected object")
print("F to focus camera on selected object")
print("R to reset camera")

print(f"{bcolors.HEADER} Shape Controls: {bcolors.ENDC}")
print(f"{bcolors.WARNING}Selected objects can bee seen in wired mode {bcolors.ENDC}")
print("0-9 Numbers to select/deselect shapes, using alt can select multiple shapes")
print("Arrow keys to move selected objects in x and z axises")
print(f"{bcolors.WARNING} [NEW] ALT + Arrow keys to rotate selected objects. {bcolors.ENDC}")
print("+ - to subdivide or undo subdivision of selected shapes")
print("'Q' to change face type of selected shapes to QUAD if shape supports")
print("'T' to change face type of selected shapes to TRIANGLE")
print(f"{bcolors.WARNING} [NEW] 'A' to start/stop animation of first light {bcolors.ENDC}")
print(f"{bcolors.WARNING} [NEW] 'G' to enable/disable normal drawing {bcolors.ENDC}")
print(f"{bcolors.HEADER} Scene Controls:{bcolors.ENDC}")
print("'W' to traverse between draw modes")

# print("\033[93m" + "***")
# print(
#     "READ ME: Implemented half edge and 'indexed face set' to 'half edge' converter, have a bug in catmull clark that i couldn't continue. I will fix and complete it asap")
# print("***")

# print("Bigger cube will follow him, bigger cube can not be selected")
main()
