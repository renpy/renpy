# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

import renpy.exports as renpy
import renpy.config as config
import renpy.defaultstore.style as style

"""renpy
init -1500 python in textshader:
"""

# This module does not participate in rollback.
_constant = True


def adjust_duration(ts, u__duration, **kwargs):
    """
    Adjusts extra_slow_duration to the value of u__duration.
    """
    ts.extra_slow_duration = u__duration


renpy.register_textshader(
    "typewriter",
    include_default=False,

    variables="""
    uniform float u_text_slow_time;
    attribute float a_text_min_time;
    varying float v_text_min_time;
    """,

    vertex_500="""
    v_text_min_time = a_text_min_time;
    """,
    fragment_500="""
    float l__done = v_text_min_time <= u_text_slow_time ? 1.0 : 0.0;
    gl_FragColor = gl_FragColor * l__done;
    """,

    doc="""
    The typewriter text shader makes text appear slowly, as if it were being
    type out by a typewriter.
    """
)


renpy.register_textshader(
    "dissolve",
    include_default=False,
    adjust_function=adjust_duration,

    variables="""
    uniform float u__duration;
    uniform float u_text_slow_duration;
    uniform float u_text_slow_time;
    attribute float a_text_time;
    varying float v_text_time;
    """,

    vertex_500="""
    v_text_time = a_text_time;
    """,
    fragment_500="""
    float l__duration = u__duration * u_text_slow_duration;
    float l__done;
    if (l__duration > 0.0) {
        l__done = clamp((u_text_slow_time - v_text_time) / l__duration, 0.0, 1.0);
    } else {
        l__done = v_text_time <= u_text_slow_time ? 1.0 : 0.0;
    }
    gl_FragColor = gl_FragColor * l__done;
    """,

    u__duration=10.0,

    doc="""
    The dissolve text shader makes text appear slowly, dissolving in from
    the start to the end.

    `u__duration`
        The number of characters that will be changing alpha at a time.  If set to
        0, the wave will move across the text one pixel at a time.
    """
)

renpy.register_textshader(
    "slowalpha",
    include_default=False,

    variables="""
    uniform float u__alpha
    """,

    fragment_475="""
vec4 l__color = gl_FragColor;
""",

    fragment_525="""
    gl_FragColor = mix(gl_FragColor, l__color, u__alpha);
    """,

    u__alpha=0.2,

    doc="""
    The slowalpha shows slow text that has yet to be revealed with a non-zero alpha.
    This is generally used in combination with other text shaders, typewriter
    or wave, that reveal text slowly.

    `u__alpha`
        The alpha value of the text that has not been revealed yet.
    """
)


renpy.register_textshader(
    "flip",
    include_default=False,
    adjust_function=adjust_duration,

    variables="""
    uniform float u__duration;
    uniform float u_text_slow_duration;
    uniform float u_text_slow_time;
    attribute vec2 a_text_center;
    attribute float a_text_min_time;
    """,

    vertex_50="""
    float l__duration = u__duration * u_text_slow_duration;
    float l__done;

    if (l__duration > 0.0) {
        l__done = clamp((u_text_slow_time - a_text_min_time) / l__duration, 0.0, 1.0);
    } else {
        l__done = a_text_min_time <= u_text_slow_time ? 1.0 : 0.0;
    }

    gl_Position.x = mix(a_text_center.x - (gl_Position.x - a_text_center.x), gl_Position.x, l__done);
    """,

    u__duration=10.0,

    doc="""
    The flip text shader flips the text around its center, revealing it slowly

    `u__duration`
        The number of characters that will be changing alpha at a time.  If set to
        0, the characters will instantly flip.
    """
)

renpy.register_textshader(
    "zoom",
    include_default=True,
    adjust_function=adjust_duration,

    variables="""
    uniform float u__zoom;
    uniform float u__duration;
    uniform float u_text_slow_duration;
    uniform float u_text_slow_time;
    attribute vec2 a_text_center;
    attribute float a_text_min_time;
    """,

    vertex_55="""
    float l__duration = u__duration * u_text_slow_duration;

    if (l__duration > 0.0) {
        float l__done = clamp((u_text_slow_time - a_text_min_time) / l__duration, 0.0, 1.0);
        gl_Position.xy = mix(a_text_center + (gl_Position.xy - a_text_center) * u__zoom, gl_Position.xy, l__done);
    }
    """,

    u__zoom=0.0,
    u__duration=10.0,

    doc="""
    The zoom text shader zooms in on the text.

    `u__zoom`
        The initial amount of zoom to apply to a character when it first starts
        showing.

    `u__duration`
        The number of characters that will be changing alpha at a time.  If set to
        0, the characters will instantly flip.
    """
)


renpy.register_textshader(
    "jitter",

    variables="""
    uniform vec2 u__jitter;
    uniform vec4 u_random;
    uniform float u_text_to_drawable;
    """,

    vertex_60="""
    vec2 l__jitter = u__jitter * u_text_to_drawable;
    gl_Position.xy += l__jitter * u_random.xy - l__jitter / 2;
    """,

    u__jitter=(3.0, 3.0),
    redraw=0.0,

    doc="""
    The jitter text shader jitters moves the text to random positions
    relative to where it would be normally drawn. The position changes
    once per frame.

    `u__jitter`
        The amount of jitter to apply to the text, in pixels.
    """
)


renpy.register_textshader(
    "offset",

    variables="""
    uniform vec2 u__offset;
    uniform float u_text_to_drawable;
    """,

    vertex_65="""
    gl_Position.xy += u__offset * u_text_to_drawable;
    """,

    u__offset=(0.0, 0.0),

    doc="""
    The offset text shader moves the text by a fixed amount.

    `u__offset`
        The amount to move the text by, in virtual pixels.
    """
)


renpy.register_textshader(
    "wave",

    variables="""
    uniform float u__amplitude;
    uniform float u__frequency
    uniform float u__wavelength;

    uniform float u_time;
    uniform float u_text_to_drawable;
    attribute float a_text_index;
    """,

    vertex_70="""
    gl_Position.y += cos(2 * 3.14159265359 * (a_text_index / u__wavelength + u_time * u__frequency)) * u__amplitude * u_text_to_drawable;
    """,

    u__amplitude=5.0,
    u__frequency=2.0,
    u__wavelength=20.0,

    redraw=0.0,

    doc="""
    The wave text shader makes the text bounce up and down in a wave.

    `u__amplitude`
        The number of pixels up and down the text will move.

    `u__frequency`
        The number of waves per second.

    `u__wavelength`
        The number of characters between peaks in the wave.
    """
)

renpy.register_textshader(
    "texture",

    variables="""
    uniform sampler2D u__texture;
    uniform vec2 u__texture_res;

    uniform float u_text_to_virtual;
    uniform float u_text_main;
    varying vec2 v__coord;
    """,

    vertex_95="""
    v__coord = u_text_to_virtual * gl_Position.xy / u__texture_res;
    """,

    fragment_300="""
    if (u_text_main == 1.0) {
        gl_FragColor = texture2D(u__texture, v__coord) * gl_FragColor;
    }
    """,

    u__texture="#800080",

    doc="""
    The texture text shader multiplies the text with a shader. This not
    done to outlined or offset text. The texture is aligned with the top
    left of the text.

    `u__texture`
        The texture to multiply the text by.
    """
)

renpy.register_textshader(
    "linetexture",

    variables="""
    uniform sampler2D u__texture;
    uniform vec2 u__scale;
    uniform vec2 u__texture_res;

    uniform float u_text_to_virtual;
    uniform float u_text_main;

    attribute vec2 a_text_center;
    varying vec2 v__coord;
    """,

    vertex_95="""

    v__coord = vec2( gl_Position.x, (gl_Position.y - a_text_center.y)) / u__scale * u_text_to_virtual / u__texture_res;
    v__coord.y += 0.5;
    """,

    fragment_300="""
    if (u_text_main == 1.0) {
        gl_FragColor = texture2D(u__texture, v__coord) * gl_FragColor;
    }
    """,

    u__texture="#800080",
    u__scale=(1.0, 1.0),

    doc="""
    Applys a texture to the text, one line at a time. The texture is aligned with
    the left sideo of the text. The vertical center of the texture is aligned with
    the baseline of the text - this meas that most of the texture will not
    be visible.

    `u__texture`
        The texture to multiply the text by.

    `u__scale`
        A factor to scale the texture by. For example (1.0, 0.5) will make the
        texture half as tall as it otherwise would be.
    """
)


"""renpy
init 1500 python hide:
"""

if config.default_textshader is not None:
    style.default.setdefault(textshader=config.default_textshader)
