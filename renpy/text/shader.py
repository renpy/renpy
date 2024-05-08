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


def combine_redraw(a, b):
    """
    Combine two redraw times, returning the smallest of the two.
    """

    if a is None:
        return b

    if b is None:
        return a

    return min(a, b)

class TextShader(object):
    """
    This stores information about a text shader.
    """

    def __init__(
            self,
            shader,
            extra_slow_time=0.0,
            extra_slow_duration=0.0,
            redraw=None,
            redraw_when_slow=0.0,
            include_default=True,
            default_uniform=None,
            **kwargs):
        """
        `shader`
            The shader to apply to the text. This can be a string, or a list of strings.
            The shader or shaders must be registered with :func:`renpy.register_shader`.

        `extra_slow_time`
            Extra time to add to the slow time effect beyond what Ren'Py will compute from
            the current characters per second. This is useful for shaders that
            might take more time to transition a character than the default time.
            If True, the shader is always updated.

        `extra_slow_duration`
            Added to `extra_slow_time`, but this is multiplied by the time
            per character to get the extra time to add to the slow time effect.
            (Time per character is 1 / characters per second.)

        `redraw`
            The amount in time in seconds before the text is redrawn, after
            all slow text has been show and `extra_slow_time` has passed.

        `redraw_when_slow`
            The amount of time in seconds before the text is redrawn when showing
            slow text.

        `include_default`
            If True, when this textshader is used directly, it will be combined
            with :var:`config.default_textshader`.

        `default_uniform`
            A uniform that is given the value of an argument if no uniform is
            specified as part of the argument.

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

        # The amount of extra time to add to the slow effect, multiplied by
        # the time per character.
        self.extra_slow_duration = extra_slow_duration

        # The redraw time.
        self.redraw = redraw

        # The redraw when showing slow text.
        self.redraw_when_slow = redraw_when_slow

        # If True, this shader is combined with the default shader.
        self.include_default = include_default

        # The default uniform.
        self.default_uniform = default_uniform

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
            self.extra_slow_duration,
            self.redraw,
            self.redraw_when_slow,
            self.include_default,
            self.default_uniform,
            self.uniforms,
            )

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        return self.key == other.key

    def combine(self, other):
        """
        Combine this text shader with another text shader.
        """

        if self is other:
            return self

        uniforms = dict(self.uniforms)
        uniforms.update(dict(other.uniforms))

        return TextShader(
            self.shader + other.shader,
            max(self.extra_slow_time, other.extra_slow_time),
            max(self.extra_slow_duration, other.extra_slow_duration),
            combine_redraw(self.redraw, other.redraw),
            combine_redraw(self.redraw_when_slow, other.redraw_when_slow),
            self.include_default or other.include_default,
            other.default_uniform,
            **uniforms
        )


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


def compute_times(shaders):
    """
    Given a list of shaders, compute the extra slow time and redraw times.
    """

    extra_slow_time = 0
    extra_slow_duration = 0
    redraw = None
    redraw_when_slow = None

    for shader in shaders:
        extra_slow_time = max(extra_slow_time, shader.extra_slow_time)
        extra_slow_duration = max(extra_slow_duration, shader.extra_slow_duration)
        redraw = combine_redraw(redraw, shader.redraw)
        redraw_when_slow = combine_redraw(redraw_when_slow, shader.redraw_when_slow)

    redraw_when_slow = combine_redraw(redraw_when_slow, redraw)

    return extra_slow_time, extra_slow_duration, redraw, redraw_when_slow


def create_textshader_args_dict(name, shader, s):
    """
    Given a string, create a textshader uniforms from it.
    """

    rv = { }

    for arg in s.split(":"):

        if "=" in arg:
            uniform, _, value = arg.partition("=")
        else:
            if shader.default_uniform:
                uniform = shader.default_uniform
                value = arg
            else:
                raise ValueError("No default uniform for %r." % name)

        uniform = uniform.strip()
        value = value.strip()

        if not uniform.startswith("u_"):
            uniform = "u_" + uniform

        for k, v in shader.uniforms:
            if k == uniform:
                break
        else:
            raise ValueError("Unknown uniform %r in %r." % (uniform, name))

        try:
            if value and (value[0] == "#"):
                numeric_value = renpy.easy.color(value).rgba
            else:
                value = value.lstrip("(").rstrip(")")
                numeric_value = tuple(float(i) for i in value.split(","))
        except Exception as e:
            raise ValueError("Error parsing %r as a uniform value: %s" % (value, e))

        if len(numeric_value) == 1:
            rv[uniform] = numeric_value[0]
        else:
            rv[uniform] = numeric_value

    return rv


def parse_textshader(o):
    """
    Given an object, returns a TextShader. This is mostly responsible for
    parsing the Text Shader mini-language.
    """

    if o is None:
        return o

    if isinstance(o, TextShader):
        return o

    if isinstance(o, basestring):

        # Combine multiple shaders separated by "|".
        if "|" in o:
            shaders = [ parse_textshader(i) for i in o.split("|") ]
            rv = shaders[0]
            for shader in shaders[1:]:
                rv = rv.combine(shader)

            return rv

        name, _, args = o.partition(":")

        name = name.strip()
        rv = renpy.config.textshaders.get(name, None)

        if rv is not None:
            if args:
                rv = rv.copy(create_textshader_args_dict(name, rv, args))

        else:
            raise Exception("Unknown text shader %r." % o)

        return rv

    raise Exception("Expected a TextShader, but got %r." % o)


parsed_shader_cache = { }

def get_textshader(o):
    """
    Tries to find a textshader. If found, then combines it with the default
    textshader, if needed, and returns the result.
    """

    def lookup(name):
        if name in renpy.config.textshader_callbacks:
            name = renpy.config.textshader_callbacks[name]()

        if name in parsed_shader_cache:
            return parsed_shader_cache[name]

        rv = parse_textshader(name)
        parsed_shader_cache[name] = rv
        return rv

    if o is None:
        return None

    rv = lookup(o)

    if not rv.include_default:
        return rv

    default = lookup(renpy.config.default_textshader)

    if default is None:
        return rv

    return default.combine(rv)


def register_textshader(
        name,
        shaders=tuple(),
        extra_slow_time=0.0,
        extra_slow_duration=0.0,
        redraw=None,
        redraw_when_slow=0.0,
        include_default=True,
        default_uniform=None,
        **kwargs):
    """
    :doc: textshader

    This creates a textshader and registers it with the name `name`.

    This function takes the following arguments:

    `name`
        This is the name of the textshader. It's also used to register a shader
        part named textshader.`name`.

    `shaders`
        Shader parts to apply to the text. This can be a string, or a list or tuple of strings.
        This should be a shader part registered with :func:`renpy.register_shader`, or this
        function. If a shader part begins with '-', then it is removed from the list of shader
        parts. (For example, '-textshader.typewriter' will remove that part.)

        Note that the shader parts registered with this function are prefixed
        with textshader., which needs to be supplied when used with this function.

    `extra_slow_time`
        Extra time to add to the slow time effect beyond what Ren'Py will compute from
        the current characters per second. This is useful for shaders that
        might take more time to transition a character than the default time.
        If True, the shader is always updated.

    `extra_slow_duration`
        Added to `extra_slow_time`, but this is multiplied by the time
        per character to get the extra time to add to the slow time effect.
        (Time per character is 1 / characters per second.)

    `redraw`
        The amount in time in seconds before the text is redrawn, after
        all slow text has been show and `extra_slow_time` has passed.

    `redraw_when_slow`
        The amount of time in seconds before the text is redrawn when showing
        slow text.

    `include_default`
        If True, when this textshader is used directly, it will be combined
        with :var:`config.default_textshader`.

    `default_uniform`
        A uniform that is given the value of an argument if no uniform is
        specified as part of the argument.

    Keyword argument beginning with ``u_`` are passed as uniforms to the shader,
    with strings beginning with ``#`` being interpreted as colors.

    A keyword argument named `variables` and all keyword arguments that begin
    with `fragment_` or `vertex_` are passed to :func:`renpy.register_shader`,
    when registering the shader part.
    """

    textshader_kwargs = { }
    part_kwargs = { }

    for k, v in kwargs.items():
        if k == "variables":
            part_kwargs[k] = v
        elif k.startswith("fragment_"):
            part_kwargs[k] = v
        elif k.startswith("vertex_"):
            part_kwargs[k] = v
        elif k.startswith("u_"):
            textshader_kwargs[k] = v
        else:
            raise TypeError("renpy.register_textshader got an unknown keyword argument %r." % (k,))

    if isinstance(shaders, str):
        shaders = ( shaders, )

    shaders = tuple(shaders) + ( "textshader." + name, )

    renpy.exports.register_shader(
        "textshader." + name,
        **part_kwargs)

    renpy.config.textshaders[name] = TextShader(
        shaders,
        extra_slow_time=extra_slow_time,
        extra_slow_duration=extra_slow_duration,
        redraw=redraw,
        redraw_when_slow=redraw_when_slow,
        include_default=include_default,
        default_uniform=default_uniform,
        **textshader_kwargs
    )
