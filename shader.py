# CENG 487 Assignment6 by
# Mustafa Berkay Özkan
# StudentId: 230201005
# 01 2020

from OpenGL.GL import *


class Program:
    def __init__(self, file_path, shader_type):
        self.id = glCreateShader(shader_type)
        with open(file_path, "r") as code:
            glShaderSource(self.id, code)

        glCompileShader(self.id)
        print(glGetShaderInfoLog(self.id))
