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
    "wave",
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
    The wave text shader makes text appear slowly, as if it were a wave moving
    across the text.

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
    uniform float u_text_to_virtual;
    """,

    vertex_60="""
    vec2 l__jitter = u__jitter / u_text_to_virtual;
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

# TODO: Wave.
# TODO: Per-line texture.
