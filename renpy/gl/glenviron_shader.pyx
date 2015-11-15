#cython: profile=False
# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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


VERTEX_SHADER1 = """\
#ifdef GL_ES
precision highp float;
#endif

uniform mat4 Projection;

attribute vec4 Vertex;
attribute vec2 VertexTexCoord0;

varying vec2 TexCoord0;

varying vec2 pos;

void main() {
    TexCoord0 = VertexTexCoord0;

    pos = Vertex.xy;
    gl_Position = Projection * Vertex;
}
"""

VERTEX_SHADER2 = """\
#ifdef GL_ES
precision highp float;
#endif

uniform mat4 Projection;

attribute vec4 Vertex;
attribute vec2 VertexTexCoord0;
attribute vec2 VertexTexCoord1;

varying vec2 TexCoord0;
varying vec2 TexCoord1;

varying vec2 pos;

void main() {
    TexCoord0 = VertexTexCoord0;
    TexCoord1 = VertexTexCoord1;

    pos = Vertex.xy;
    gl_Position = Projection * Vertex;
}
"""

VERTEX_SHADER3 = """\
#ifdef GL_ES
precision highp float;
#endif

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
    vec4 color0 = texture2D(tex0, TexCoord0.st);
    gl_FragColor = color0 * Color;
}
"""

BLIT_CLIP_SHADER = """
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
    vec4 color0 = texture2D(tex0, TexCoord0.st);
    vec4 color1 = texture2D(tex1, TexCoord1.st);

    gl_FragColor = mix(color0, color1, done) * Color;
}
"""


BLEND_CLIP_SHADER = """
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
    vec4 color0 = texture2D(tex0, TexCoord0.st);
    vec4 color1 = texture2D(tex1, TexCoord1.st);
    vec4 color2 = texture2D(tex2, TexCoord2.st);

    float a = clamp((color0.a + offset) * multiplier, 0.0, 1.0);

    gl_FragColor = mix(color1, color2, a) * Color;
}
"""

IMAGEBLEND_CLIP_SHADER = """
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

    def disable_attribs(self):
        # Disable the vertex attributes used by this program.

        if self.Vertex != -1:
            glDisableVertexAttribArrayARB(self.Vertex)

        if self.VertexTexCoord0 != -1:
            glDisableVertexAttribArrayARB(self.VertexTexCoord0)

        if self.VertexTexCoord1 != -1:
            glDisableVertexAttribArrayARB(self.VertexTexCoord1)

        if self.VertexTexCoord2 != -1:
            glDisableVertexAttribArrayARB(self.VertexTexCoord2)

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

    cdef Program blit_clip_program
    cdef Program blend_clip_program
    cdef Program imageblend_clip_program

    cdef bint clipping
    cdef double clip_x0
    cdef double clip_y0
    cdef double clip_x1
    cdef double clip_y1

    cdef int viewport_x
    cdef int viewport_y
    cdef int viewport_w
    cdef int viewport_h


    def init(self):

        self.blit_program = Program(VERTEX_SHADER1, BLIT_SHADER)
        self.blit_clip_program = Program(VERTEX_SHADER1, BLIT_CLIP_SHADER)

        self.blend_program = Program(VERTEX_SHADER2, BLEND_SHADER)
        self.blend_clip_program = Program(VERTEX_SHADER2, BLEND_CLIP_SHADER)

        self.imageblend_program = Program(VERTEX_SHADER3, IMAGEBLEND_SHADER)
        self.imageblend_clip_program = Program(VERTEX_SHADER3, IMAGEBLEND_CLIP_SHADER)

        # The current program.
        self.program = None

    def deinit(self):
        """
        Called before changing the GL context.
        """

        if self.program is not None:
            self.program.disable_attribs()
            self.program = None

        self.blit_program.delete()
        self.blend_program.delete()
        self.imageblend_program.delete()

    def activate(self, Program program):

        if self.program is not None:
            self.program.disable_attribs()

        self.program = program

        glUseProgramObjectARB(program.program)
        glUniformMatrix4fvARB(program.Projection, 1, GL_FALSE, self.projection)

        if self.clipping:
            glUniform2fARB(program.clip0, self.clip_x0, self.clip_y0)
            glUniform2fARB(program.clip1, self.clip_x1, self.clip_y1)

    cdef void blit(self):

        if self.clipping:
            program = self.blit_clip_program
        else:
            program = self.blit_program

        if self.program is not program:
            self.activate(program)
            glUniform1iARB(program.tex0, 0)

    cdef void blend(self, double fraction):
        if self.clipping:
            program = self.blend_clip_program
        else:
            program = self.blend_program

        if self.program is not program:
            self.activate(program)
            glUniform1iARB(program.tex0, 0)
            glUniform1iARB(program.tex1, 1)

        glUniform1fARB(program.done, fraction)

    cdef void imageblend(self, double fraction, int ramp):

        if self.clipping:
            program = self.imageblend_clip_program
        else:
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
        glEnableVertexAttribArrayARB(self.program.Vertex)
        glVertexAttribPointerARB(self.program.Vertex, 2, GL_FLOAT, GL_FALSE, 0, <GLubyte *> vertices)

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

        if self.program is not None:
            self.program.disable_attribs()

        self.program = None

    cdef void project(self, x, y, z, double *rv_x, double *rv_y, double *rv_z):
        """
        Given a point, projects it using the projection.
        """

        rv_x[0] = x * self.projection[0] + y * self.projection[4] + z * self.projection[8] + self.projection[12]
        rv_y[0] = x * self.projection[1] + y * self.projection[5] + z * self.projection[9] + self.projection[13]
        rv_z[0] = x * self.projection[2] + y * self.projection[6] + z * self.projection[10] + self.projection[14]

    cdef void set_clip(self, tuple clip_box, GLDraw draw):

        cdef double minx, miny, maxx, maxy, z
        cdef double vwidth, vheight
        cdef double px, py, pw, ph
        cdef int cx, cy, cw, ch
        cdef int psw, psh

        if clip_box == draw.default_clip:
            self.unset_clip(draw)
            return

        minx, miny, maxx, maxy = clip_box
        psw, psh = draw.physical_size

        # The clipping box.
        self.clipping = True
        self.clip_x0 = minx
        self.clip_y0 = miny
        self.clip_x1 = maxx
        self.clip_y1 = maxy

        # Set the scissor rectangle to be slightly larger than the
        # clipping box. This ensures everything that needs to be drawn
        # is drawn, and we don't spend a lot of time shading clipped
        # fragments.

        if draw.clip_rtt_box is None:

            z = 0

            # Project to normalized coordinates.
            self.project(minx, miny, z, &minx, &miny, &z)
            self.project(maxx, maxy, z, &maxx, &maxy, &z)

            # Convert to window coordinates.
            minx = (minx + 1) * self.viewport_w / 2 + self.viewport_x
            maxx = (maxx + 1) * self.viewport_w / 2 + self.viewport_x
            miny = (miny + 1) * self.viewport_h / 2 + self.viewport_y
            maxy = (maxy + 1) * self.viewport_h / 2 + self.viewport_y

            # Increase the bounding box, to ensure every relevant pixel is
            # in it. The shader will take care of enforcing the actual box.
            minx -= 1
            maxx += 1
            miny += 1
            maxy -= 1

            if minx < 0:
                minx = 0
            if miny < 0:
                miny = 0

            glEnable(GL_SCISSOR_TEST)
            glScissor(<GLint> round(minx), <GLint> round(maxy), <GLint> round(maxx - minx), <GLsizei> round(miny - maxy))

        else:

            cx, cy, cw, ch = draw.clip_rtt_box

            glEnable(GL_SCISSOR_TEST)
            glScissor(<GLint> round(minx - cx), <GLint> round(miny - cy), <GLint> round(maxx - minx), <GLint> round(maxy - miny))

        if self.program is not None:
            self.program.disable_attribs()

        self.program = None

    cdef void unset_clip(self, GLDraw draw):

        glDisable(GL_SCISSOR_TEST)

        self.clipping = False
        self.clip_x0 = 0
        self.clip_y0 = 0
        self.clip_x1 = 65535
        self.clip_y1 = 65535

        if self.program is not None:
            self.program.disable_attribs()

        self.program = None

    cdef void viewport(self, int x, int y, int width, int height):
        glViewport(x, y, width, height)
        self.viewport_x = x
        self.viewport_y = y
        self.viewport_w = width
        self.viewport_h = height
