#cython: profile=False
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

DEF ANGLE = False

from gl cimport *
from gldraw cimport *

cdef int round(double d):
    return <int> (d + .5)

VERTEX_SHADER = """\
uniform mat4 Projection;

attribute vec4 Vertex;
attribute vec2 VertexTexCoord0;
attribute vec2 VertexTexCoord1;
attribute vec2 VertexTexCoord2;

varying vec2 TexCoord0;
varying vec2 TexCoord1;
varying vec2 TexCoord2;

varying vec2 pos;

void main() {
    TexCoord0 = VertexTexCoord0;
    TexCoord1 = VertexTexCoord1;
    TexCoord2 = VertexTexCoord2;

    pos = Vertex.xy;
    gl_Position = Projection * Vertex;
}
"""

BLIT_SHADER = """
#ifdef GL_ES
precision highp float;
#endif

uniform vec4 Color;
uniform sampler2D tex0;

varying vec2 TexCoord0;

varying vec2 pos;
uniform vec2 clip0;
uniform vec2 clip1;
        
void main()
{
    if (pos.x < clip0.x || pos.y < clip0.y || pos.x >= clip1.x || pos.y >= clip1.y) {
        discard;
    }

    vec4 color0 = texture2D(tex0, TexCoord0.st);
    gl_FragColor = color0 * Color;
}
"""

BLEND_SHADER = """
#ifdef GL_ES
precision highp float;
#endif

uniform vec4 Color;
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform float done;

varying vec2 TexCoord0;
varying vec2 TexCoord1;

varying vec2 pos;
uniform vec2 clip0;
uniform vec2 clip1;

void main()
{
    if (pos.x < clip0.x || pos.y < clip0.y || pos.x >= clip1.x || pos.y >= clip1.y) {
        discard;
    }

    vec4 color0 = texture2D(tex0, TexCoord0.st);
    vec4 color1 = texture2D(tex1, TexCoord1.st);

    gl_FragColor = mix(color0, color1, done) * Color;
}
"""

IMAGEBLEND_SHADER = """
#ifdef GL_ES
precision highp float;
#endif

uniform vec4 Color;
uniform sampler2D tex0;
uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float offset;
uniform float multiplier;
        
varying vec2 TexCoord0;
varying vec2 TexCoord1;
varying vec2 TexCoord2;

varying vec2 pos;
uniform vec2 clip0;
uniform vec2 clip1;

void main()
{
    if (pos.x < clip0.x || pos.y < clip0.y || pos.x >= clip1.x || pos.y >= clip1.y) {
        discard;
    }

    vec4 color0 = texture2D(tex0, TexCoord0.st);
    vec4 color1 = texture2D(tex1, TexCoord1.st);
    vec4 color2 = texture2D(tex2, TexCoord2.st);

    float a = clamp((color0.a + offset) * multiplier, 0.0, 1.0);

    gl_FragColor = mix(color1, color2, a) * Color;
}
"""



def check_status(shader, handle, type):
    """
    Checks the status of a shader or program. If it fails, then an
    exception is raised.
    """

    cdef GLint status = 0
    cdef GLint log_length = 0
    
    if shader:
        glGetShaderiv(handle, type, &status)
    else:    
        glGetProgramiv(handle, type, &status)

    if status == 1: # 0 for problems.
        return
        
    if shader:
        glGetShaderiv(handle, GL_INFO_LOG_LENGTH, &log_length)
    else:
        glGetProgramiv(handle, GL_INFO_LOG_LENGTH, &log_length)

    log = ' ' * log_length
    
    if shader:
        glGetShaderInfoLog(handle, log_length, &log_length, <char *> log)
    else:
        glGetProgramInfoLog(handle, log_length, &log_length, <char *> log)

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

    check_status(True, handle, GL_OBJECT_COMPILE_STATUS_ARB)

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

    check_status(False, program, GL_OBJECT_LINK_STATUS_ARB)

    glUseProgramObjectARB(program)
    
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return program

cdef class Program(object):
    """
    Encapsulates a program.
    """

    cdef GLuint program

    # Attributes.
    cdef GLint Vertex
    cdef GLint VertexTex
    cdef GLint VertexTexCoord0
    cdef GLint VertexTexCoord1
    cdef GLint VertexTexCoord2
    
    # Uniforms.
    cdef GLint Projection
    cdef GLint Color    

    cdef GLint tex0
    cdef GLint tex1
    cdef GLint tex2
    
    cdef GLint clip0
    cdef GLint clip1
    
    cdef GLint offset
    cdef GLint multiplier
    cdef GLint done
    
    def __init__(self, vertex, fragment):
        self.program = compile_program(vertex, fragment)
        
        self.Vertex = glGetAttribLocationARB(self.program, "Vertex")
        self.VertexTex = glGetAttribLocationARB(self.program, "VertexTex")
        self.VertexTexCoord0 = glGetAttribLocationARB(self.program, "VertexTexCoord0")
        self.VertexTexCoord1 = glGetAttribLocationARB(self.program, "VertexTexCoord1")
        self.VertexTexCoord2 = glGetAttribLocationARB(self.program, "VertexTexCoord2")
        
        self.Projection = glGetUniformLocationARB(self.program, "Projection")
        self.tex0 = glGetUniformLocationARB(self.program, "tex0")
        self.tex1 = glGetUniformLocationARB(self.program, "tex1")
        self.tex2 = glGetUniformLocationARB(self.program, "tex2")
        self.offset = glGetUniformLocationARB(self.program, "offset")
        self.multiplier = glGetUniformLocationARB(self.program, "multiplier")
        self.done = glGetUniformLocationARB(self.program, "done")
        self.Color = glGetUniformLocationARB(self.program, "Color")
        self.clip0 = glGetUniformLocationARB(self.program, "clip0")
        self.clip1 = glGetUniformLocationARB(self.program, "clip1")

    def delete(self):
        glDeleteProgram(self.program)

        
cdef class ShaderEnviron(Environ):
    """
    This is an environment that uses shaders.
    """
    
    cdef Program program
    cdef float projection[16]

    cdef Program blit_program
    cdef Program blend_program
    cdef Program imageblend_program

    cdef double clip_x0
    cdef double clip_y0
    cdef double clip_x1
    cdef double clip_y1

    def init(self):

        self.blit_program = Program(VERTEX_SHADER, BLIT_SHADER)
        self.blend_program = Program(VERTEX_SHADER, BLEND_SHADER)
        self.imageblend_program = Program(VERTEX_SHADER, IMAGEBLEND_SHADER)

        # The current program.
        self.program = None        

    def deinit(self):
        """
        Called before changing the GL context.
        """

        self.blit_program.delete()
        self.blend_program.delete()
        self.imageblend_program.delete()
        
    def activate(self, Program program):
        self.program = program

        glUseProgramObjectARB(program.program)
        glUniformMatrix4fvARB(program.Projection, 1, GL_FALSE, self.projection)
        glUniform2fARB(program.clip0, self.clip_x0, self.clip_y0)
        glUniform2fARB(program.clip1, self.clip_x1, self.clip_y1)

    cdef void blit(self):

        program = self.blit_program

        if self.program is not program:
            self.activate(program)
            glUniform1iARB(program.tex0, 0)
        
    cdef void blend(self, double fraction):
        program = self.blend_program

        if self.program is not program:
            self.activate(program)
            glUniform1iARB(program.tex0, 0)
            glUniform1iARB(program.tex1, 1)

        glUniform1fARB(program.done, fraction)
        
    cdef void imageblend(self, double fraction, int ramp):

        program = self.imageblend_program

        if self.program is not program:
            self.activate(program)
            glUniform1iARB(program.tex0, 0)
            glUniform1iARB(program.tex1, 1)
            glUniform1iARB(program.tex2, 2)

        # Prevent a DBZ if the user gives us a 0 ramp.
        if ramp < 1:
            ramp = 1
            
        # Compute the offset to apply to the alpha.            
        start = -1.0
        end = ramp / 256.0        
        offset = start + ( end - start) * fraction

        # Setup the multiplier and the offset.
        glUniform1fARB(program.multiplier, 256.0 / ramp)
        glUniform1fARB(program.offset, offset)

    cdef void set_vertex(self, float *vertices):
        glVertexAttribPointerARB(self.program.Vertex, 2, GL_FLOAT, GL_FALSE, 0, <GLubyte *> vertices)
        glEnableVertexAttribArrayARB(self.program.Vertex)
        
    cdef void set_texture(self, int unit, float *coords):
        cdef tex
        
        if unit == 0:
            tex = self.program.VertexTexCoord0
        elif unit == 1:
            tex = self.program.VertexTexCoord1
        elif unit == 2 and RENPY_THIRD_TEXTURE:
            tex = self.program.VertexTexCoord2
        else:
            return

        if tex < 0:
            return

        if coords != NULL:           
            glVertexAttribPointerARB(tex, 2, GL_FLOAT, GL_FALSE, 0, <GLubyte *> coords)
            glEnableVertexAttribArrayARB(tex)
        else:
            glDisableVertexAttribArrayARB(tex)
            
    cdef void set_color(self, float r, float g, float b, float a):
        glUniform4fARB(self.program.Color, r, g, b, a)
            
    cdef void ortho(self, double left, double right, double bottom, double top, double near, double far):
        
        self.projection[ 0] = 2 / (right - left)
        self.projection[ 4] = 0
        self.projection[ 8] = 0
        self.projection[12] = -(right + left) / (right - left)
        
        self.projection[ 1] = 0
        self.projection[ 5] = 2 / (top - bottom)
        self.projection[ 9] = 0
        self.projection[13] = -(top + bottom) / (top - bottom)

        self.projection[ 2] = 0
        self.projection[ 6] = 0
        self.projection[10] = -2 / (far - near)
        self.projection[14] = -(far + near) / (far - near)

        self.projection[ 3] = 0
        self.projection[ 7] = 0
        self.projection[11] = 0
        self.projection[15] = 1
        
        self.program = None
        
    cdef void set_clip(self, tuple clip_box, GLDraw draw):
        
        cdef double minx, miny, maxx, maxy
        cdef double vwidth, vheight
        cdef double px, py, pw, ph
        cdef int cx, cy, cw, ch
        cdef int psw, psh
        
        minx, miny, maxx, maxy = clip_box
        psw, psh = draw.physical_size
      
        # The clipping box.  
        self.clip_x0 = minx
        self.clip_y0 = miny
        self.clip_x1 = maxx
        self.clip_y1 = maxy 
        
        # Set the scissor rectangle to be slightly larger than the 
        # clipping box. This ensures everything that needs to be drawn
        # is drawn, and we don't spend a lot of time shading clipped 
        # fragments.
        
        if draw.clip_rtt_box is None:
            
            vwidth, vheight = draw.virtual_size
            px, py, pw, ph = draw.physical_box

            minx = px + (minx / vwidth) * pw
            maxx = px + (maxx / vwidth) * pw

            miny = py + (miny / vheight) * ph
            maxy = py + (maxy / vheight) * ph

            miny = psh - miny
            maxy = psh - maxy

            # Increase the bounding box, to ensure every relevant pixel is 
            # in it. The shader will take care of enforcing the actual box.
            minx -= 1
            maxx += 1            
            miny += 1
            maxy -= 1

            glEnable(GL_SCISSOR_TEST)
            glScissor(<GLint> round(minx), <GLint> round(maxy), <GLint> round(maxx - minx), <GLsizei> round(miny - maxy))

        else:

            cx, cy, cw, ch = draw.clip_rtt_box

            glEnable(GL_SCISSOR_TEST)                            
            glScissor(<GLint> round(minx - cx), <GLint> round(miny - cy), <GLint> round(maxx - minx), <GLint> round(maxy - miny))

        self.program = None
  
    cdef void unset_clip(self, GLDraw draw):
        
        cdef int psw, psh
        psw, psh = draw.physical_size

        glDisable(GL_SCISSOR_TEST)
        
        self.clip_x0 = 0
        self.clip_y0 = 0
        self.clip_x1 = 0
        self.clip_x1 = 0
        
        self.program = None
        
        