# Fast texture loading experiment.


from libc.string cimport memcpy
from libc.stdlib cimport malloc, free

from uguugl cimport *

from pygame_sdl2 cimport *
import pygame_sdl2
import_pygame_sdl2()

from renpy.gl2.gl2geometry import Mesh
from renpy.gl2.gl2shader cimport Program

FTL_VERTEX_SHADER = b"""\
#ifdef GL_ES
precision highp float;
#endif

attribute vec4 aPosition;
attribute vec2 aTexCoord;

varying vec2 vTexCoord;

void main() {
    vTexCoord = aTexCoord;
    gl_Position = aPosition;
}
"""

FTL_FRAGMENT_SHADER = b"""\
#ifdef GL_ES
precision highp float;
#endif

uniform sampler2D uTex0;
varying vec2 vTexCoord;

void main() {
    gl_FragColor = texture2D(uTex0, vTexCoord.xy);
}
"""

cdef GLuint root_fbo
cdef GLuint texture_fbo

def set_rgba_masks():
    """
    This rebuilds the sample surfaces, to ones that use the given
    masks.
    """

    # Annoyingly, the value for the big mask seems to vary from
    # platform to platform. So we read it out of a surface.

    global sample_alpha

    # Create a sample surface.
    s = pygame_sdl2.Surface((10, 10), 0, 32)
    sample_alpha = s.convert_alpha()

    # Sort the components by absolute value.
    masks = list(sample_alpha.get_masks())
    masks.sort(key=lambda a : abs(a))

    # Choose the masks.
    import sys
    if sys.byteorder == 'big':
        masks = ( masks[3], masks[2], masks[1], masks[0] )
    else:
        masks = ( masks[0], masks[1], masks[2], masks[3] )

    # Create the sample surface.
    sample_alpha = pygame_sdl2.Surface((10, 10), 0, 32, masks)


def init_ftl():

    set_rgba_masks()

    global ftl_program
    ftl_program = Program(FTL_VERTEX_SHADER, FTL_FRAGMENT_SHADER)
    ftl_program.load()

    global root_fbo
    global texture_fbo

    glGetIntegerv(GL_FRAMEBUFFER_BINDING, <GLint *> &root_fbo);
    glGenFramebuffers(1, &texture_fbo)


cpdef GLuint load_texture(fn):
    """
    Loads a texture.
    """

    surf = pygame_sdl2.image.load(fn)
    surf = surf.convert_alpha(sample_alpha)

    cdef SDL_Surface *s
    s = PySurface_AsSurface(surf)

    cdef unsigned char *pixels = <unsigned char *> s.pixels
    cdef unsigned char *data = <unsigned char *> malloc(s.h * s.w * 4)
    cdef unsigned char *p = data

    for 0 <= i < s.h:
        memcpy(p, pixels, s.w * 4)

        pixels += s.pitch
        p += (s.w * 4)

    cdef GLuint tex

    glGenTextures(1, &tex)

    cdef GLuint premultiplied
    glGenTextures(1, &premultiplied)

    glBindTexture(GL_TEXTURE_2D, premultiplied)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, s.w, s.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, NULL)

    glBindFramebuffer(GL_FRAMEBUFFER, texture_fbo)

    glFramebufferTexture2D(
        GL_FRAMEBUFFER,
        GL_COLOR_ATTACHMENT0,
        GL_TEXTURE_2D,
        premultiplied,
        0)

    glViewport(0, 0, s.w, s.h)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    m = Mesh()
    m.add_attribute("aTexCoord", 2)
    m.add_polygon([
        -1.0, -1.0, 0.0, 1.0, 0.0, 0.0,
        -1.0,  1.0, 0.0, 1.0, 0.0, 1.0,
         1.0,  1.0, 0.0, 1.0, 1.0, 1.0,
         1.0, -1.0, 0.0, 1.0, 1.0, 0.0,
        ])

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, s.w, s.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    glEnable(GL_BLEND)
    glBlendFuncSeparate(GL_SRC_ALPHA, GL_ZERO, GL_ONE, GL_ZERO)

    ftl_program.draw(m, uTex0=0)
    glDeleteTextures(1, &tex)

    glBindTexture(GL_TEXTURE_2D, premultiplied)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindFramebuffer(GL_FRAMEBUFFER, root_fbo)

    free(data)

    return premultiplied


