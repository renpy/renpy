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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy

class TextShader(object):
    """
    This stores information about a text shader.
    """

    def __init__(self, shader, extra_slow_time=0, redraw=None, redraw_when_slow=0, **kwargs):
        """
        `shader`
            The shader to apply to the text. This can be a string, or a list of strings.
            The shader or shaders must be registered with :func:`renpy.register_shader`.

        `extra_slow_time`
            Extra time to add to the slow time effect beyond what Ren'Py will compute from
            the current characters per second. This is useful for shaders that
            might take more time to transition a character than the default time.
            If True, the shader is always updated.

        `redraw`
            The amount in time in seconds before the text is redrawn, after
            all slow text has been show and `extra_slow_time` has passed.

        `redraw_when_slow`
            The amount of time in seconds before the text is redrawn when showing
            slow text.

        Keyword argument beginning with ``u_`` are passed as uniforms to the shader.
        """

        # A tuple of shaders to apply to text.
        if isinstance(shader, basestring):
            self.shader = (shader,)
        else:
            self.shader = tuple(shader)

        # The amount of extra time to add to the slow effect, in addition
        # to the time Ren'Py would normally take to display the text.
        self.extra_slow_time = extra_slow_time

        # The redraw time.
        self.redraw = redraw

        # The redraw when showing slow text.
        self.redraw_when_slow = redraw_when_slow

        # A tuple of uniform name, value pairs.
        uniforms = { }

        for k, v in kwargs.items():
            if k.startswith("u_"):

                if v and v[0] == "#":
                    v = renpy.easy.color(v).rgba

                uniforms[k] = v
            else:
                raise ValueError("Unknown keyword argument %r." % (k,))

        self.uniforms = tuple(sorted(uniforms.items()))

        self.key = (
            self.shader,
            self.extra_slow_time,
            self.redraw,
            self.redraw_when_slow,
            self.uniforms
            )

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def copy(self, new_uniforms):
        """
        Create a copy of this TextShader, with the uniforms updated with
        the new uniforms.
        """

        rv = TextShader(self.shader)
        rv.__dict__.update(self.__dict__)

        uniforms = dict(self.uniforms)
        uniforms.update(new_uniforms)
        rv.uniforms = tuple(sorted(uniforms.items()))

        return rv

def create_textshader_args_dict(s):
    """
    Given a string, create a textshader uniforms from it.
    """

    rv = { }

    for arg in s.split(":"):
        try:
            uniform, _, value = arg.partition("=")

            uniform = uniform.strip()
            value = value.strip()

            if not uniform.startswith("u_"):
                raise ValueError()

            if value and (value[0] == "#"):
                numeric_value = renpy.easy.color(value).rgba
            else:
                value = value.lstrip("(").rstrip(")")
                numeric_value = tuple(float(i) for i in value.split(","))

            if len(numeric_value) == 1:
                rv[uniform] = numeric_value[0]
            else:
                rv[uniform] = numeric_value

        except Exception as e:
            raise ValueError("Expected a uniform assignment, but got %r." % arg)

    return rv


def check_textshader(o):
    if o is None:
        return o

    if isinstance(o, TextShader):
        return o

    if isinstance(o, basestring):
        name, _, args = o.partition(":")

        rv = renpy.config.text_shaders.get(name, None)

        if rv is not None:
            if args:
                rv = rv.copy(create_textshader_args_dict(args))

        else:
            raise Exception("Unknown text shader %r." % o)

        return rv

    raise Exception("Expected a TextShader, but got %r." % o)
