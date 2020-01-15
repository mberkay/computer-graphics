# CENG 487 Assignment6 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 01 2020

from OpenGL.GL import *


class Program:
    def __init__(self, vertex_s, fragment_s):
        self.id = glCreateProgram()
        self.vertex_shader = vertex_s
        self.fragment_shader = fragment_s

        self.attach_shader(self.vertex_shader)
        self.attach_shader(self.fragment_shader)
        glLinkProgram(self.id)
        
    def attach_shader(self, shader):
        glAttachShader(self.id, shader.id)

    def use(self):
        try:

            glUseProgram(self.id)
        # https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glLinkProgram.xhtml
        except (GL_INVALID_VALUE, GL_INVALID_OPERATION) as e:
            print(e)
            print(glGetProgramInfoLog(self.id))
