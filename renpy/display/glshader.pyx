# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# This file contains GLSL shader code, and code to load shaders.

import array
from gl cimport *

VERTEX_SHADER = """
void main() {
    gl_TexCoord[0] = gl_MultiTexCoord0;
    gl_TexCoord[1] = gl_MultiTexCoord1;
    gl_TexCoord[2] = gl_MultiTexCoord2;
    gl_ClipVertex = gl_ModelViewMatrix * gl_Vertex;
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    gl_FrontColor = gl_Color;
    gl_BackColor = gl_Color;
}
"""

BLIT_SHADER = """
uniform sampler2D tex0;
        
void main()
{
    vec4 color0 = texture2D(tex0, gl_TexCoord[0].st);

    gl_FragColor = color0 * gl_Color;
}
"""

BLEND_SHADER = """
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform float done;
        
void main()
{
    vec4 color0 = texture2D(tex0, gl_TexCoord[0].st);
    vec4 color1 = texture2D(tex1, gl_TexCoord[1].st);

    gl_FragColor = mix(color0, color1, done) * gl_Color;
}
"""

IMAGEBLEND_SHADER = """
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float offset;
uniform float multiplier;
        
void main()
{
    vec4 color0 = texture2D(tex0, gl_TexCoord[0].st);
    vec4 color1 = texture2D(tex1, gl_TexCoord[1].st);
    vec4 color2 = texture2D(tex2, gl_TexCoord[2].st);

    float a = clamp((color0.a + offset) * multiplier, 0.0, 1.0);

    gl_FragColor = mix(color1, color2, a) * gl_Color;
}
"""

def check_status(handle, type):
    """
    Checks the status of a shader or program. If it fails, then an
    exception is raised.
    """

    cdef GLint status = 0
    cdef GLint log_length = 0
    
    glGetObjectParameterivARB(handle, type, &status)

    if status == 1: # 0 for problems.
        return
        
    glGetObjectParameterivARB(handle, GL_OBJECT_INFO_LOG_LENGTH_ARB, &log_length)

    log = ' ' * log_length
    glGetInfoLogARB(handle, log_length, &log_length, <char *> log)

    raise Exception("Shader error: %s" % log)


def compile_shader(kind, source):
    """
    Allocates and compiles a shader.
    """

    cdef char *sourceptr = <char *> source
    cdef int lensource = len(source)
    
    handle = glCreateShaderObjectARB(kind)
    glShaderSourceARB(handle, 1, <GLcharARB **> &sourceptr, &lensource)
    glCompileShaderARB(handle)

    check_status(handle, GL_OBJECT_COMPILE_STATUS_ARB)

    return handle


def compile_program(vertex, fragment):
    """
    Compiles a pair of shaders into a program.
    """
    
    vertex_shader = compile_shader(GL_VERTEX_SHADER_ARB, vertex)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER_ARB, fragment)
    
    program = glCreateProgramObjectARB()

    glAttachObjectARB(program, vertex_shader)
    glAttachObjectARB(program, fragment_shader)

    glLinkProgramARB(program)

    check_status(program, GL_OBJECT_LINK_STATUS_ARB)

    glUseProgramObjectARB(program)
    
    glDeleteObjectARB(vertex_shader)
    glDeleteObjectARB(fragment_shader)
    
    return program


# These return the standard programs, compiled and ready to use.

def blit_program():
    return compile_program(VERTEX_SHADER, BLIT_SHADER)

def blend_program():
    return compile_program(VERTEX_SHADER, BLEND_SHADER)

def imageblend_program():
    return compile_program(VERTEX_SHADER, IMAGEBLEND_SHADER)
