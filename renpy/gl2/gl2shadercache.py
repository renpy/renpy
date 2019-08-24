import re
import io
import os

import renpy.display

# A map from shader part name to ShaderPart
shader_part = { }


def register_shader(name, **kwargs):
    """
    This registers a part of a shader. Shader parts have a name, and then

    `name`
        A string giving the name of the shader part. Names starting with an
        underscore or "renpy." are reserved for Ren'Py.

    `variables`
        The variables used by the shader part. These should be listed one per
        line, a storage (uniform, attribute, or varing) followed by a type,
        name, and semicolon. For example::

            variables='''
            uniform sampler2D uTex0;
            attribute vec2 aTexCoord;
            varying vec2 vTexCoord;
            '''

    `vertex_functions`
        If given, a string containing functions that will be included in the
        vertex shader.

    `fragment_functions`
        If given, a string containing functions that will be included in the
        fragment shader.

    Other keyword arguments should start with ``vertex_`` or ``fragment_``,
    and end with an integer priority. So "fragment_120" or "vertex_30". These
    give text that's placed in the appropriate shader at the given priority,
    with lower priority numbers inserted before higher priority numbers.
    """

    ShaderPart(name, **kwargs)


class ShaderPart(object):
    """
    Arguments are as for register_shader.

    """

    def __init__(self, name, variables="", vertex_functions="", fragment_functions="", **kwargs):

        if not re.match(r'^[\w\.]+$', name):
            raise Exception("The shader name {!r} contains an invalid character. Shader names are limited to ASCII alphanumeric characters, _, and .".format(name))

        self.name = name
        shader_part[name] = self

        self.vertex_functions = vertex_functions
        self.fragment_functions = fragment_functions

        # A list of priority, text pairs for each section of the vertex and fragment shaders.
        self.vertex_parts = [ ]
        self.fragment_parts = [ ]

        # Sets of (storage, type, name) tuples, where storage is one of 'uniform', 'attribute', or 'varying',
        self.vertex_variables = set()
        self.fragment_variables = set()

        # A sets of variable names used in the vertex and fragments shader.
        vertex_used = set()
        fragment_used = set()

        for k, v in kwargs.iteritems():

            shader, _, priority = k.partition('_')

            if not priority:
                # Trigger error handling.
                shader = None

            try:
                priority = int(priority)
            except:
                shader = None

            if shader == "vertex":
                parts = self.vertex_parts
                used = vertex_used
            elif shader == "fragment":
                parts = self.fragment_parts
                used = fragment_used
            else:
                raise Exception("Keyword arguments to ShaderPart must be of the form {vertex,fragment}_{priority}.")

            parts.append((priority, v))

            for m in re.finditer(r'\b\w+\b', v):
                used.add(m.group(0))

        for l in variables.split("\n"):
            l = l.strip(' ;')

            a = l.split()
            if not a:
                continue

            if len(a) != 3:
                print("Unknown shader variable line {!r}. Only the form '{{uniform,attribute,vertex}} {{type}} {{name}} is allowed.".format(l))

            a = tuple(a)
            name = a[2]

            if name in vertex_used:
                self.vertex_variables.add(a)

            if name in fragment_used:
                self.fragment_variables.add(a)


# A map from a tuple giving the parts that comprise a shader, to the Shader
# object. The same shader might appear multiple times, to optimize performance.
cache = { }


def source(variables, parts, functions, fragment, gles):
    """
    Given lists of variables and parts, converts them into textual source
    code for a shader.

    `fragment`
        Should be set to true to generate the code for a fragment shader.
    """

    rv = [ ]

    if gles:
        rv.append("""
#version 100 es
""")

        if fragment:
            rv.append("""
precision mediump float;
""")

    else:
        rv.append("""
#version 120
""")

    rv.extend(functions)

    for storage, type_, name in sorted(variables):
        rv.append("{} {} {};\n".format(storage, type_, name))

    rv.append("\nvoid main() {\n")

    parts.sort()

    for _, part in parts:
        rv.append(part)

    rv.append("}\n")

    return "".join(rv)


class ShaderCache(object):
    """
    This class caches shaders that were compiled. It's also responsible for
    recording shaders that have been used, persisting them to disk, and then
    loading the shaders back into the cache.
    """

    def __init__(self, filename, gles):

        # The filename that we'll load the list of shaders from, and
        # persist it to.
        self.filename = filename

        # Are we gles?
        self.gles = gles

        # A map from tuples of partnames to the shaders that have been
        # created.
        self.cache = { }

        # A set of tuples of partnames corresponding to shaders that existed
        # in the past, but do not exist now.
        self.missing = set()

    def get(self, partnames):
        """
        Gets a shader, creating it if necessary.

        `partnames`
            A tuple of strings, giving the names of the shader parts to include in
            the cache.
        """

        rv = self.cache.get(partnames, None)
        if rv is not None:
            return rv

        partnameset = set(partnames)
        partnameset.add(renpy.config.default_shader)
        sortedpartnames = tuple(sorted(partnameset))

        rv = self.cache.get(sortedpartnames, None)
        if rv is not None:
            self.cache[partnames] = rv
            return rv

        # If the cache missed entirely, we have to generate the source code for the
        # shaders.

        vertex_variables = set()
        vertex_parts = [ ]
        vertex_functions = [ ]

        fragment_variables = set()
        fragment_parts = [ ]
        fragment_functions = [ ]

        for i in sortedpartnames:

            p = shader_part.get(i, None)

            if p is None:
                raise Exception("{!r} is not a known shader part.".format(i))

            vertex_variables |= p.vertex_variables
            vertex_parts.extend(p.vertex_parts)
            vertex_functions.append(p.vertex_functions)

            fragment_variables |= p.fragment_variables
            fragment_parts.extend(p.fragment_parts)
            fragment_functions.append(p.fragment_functions)

        vertex = source(vertex_variables, vertex_parts, vertex_functions, False, self.gles)
        fragment = source(fragment_variables, fragment_parts, fragment_functions, True, self.gles)

        from renpy.gl2.gl2shader import Program

        rv = Program(sortedpartnames, vertex, fragment)
        rv.load()

        self.cache[partnames] = rv
        self.cache[sortedpartnames] = rv
        return rv

    def check(self, partnames):
        """
        Returns true if every part in partnames is a known part, or False
        otherwise.
        """

        for i in partnames:
            if i not in shader_part:
                return False

        return True

    def save(self):
        """
        Saves the list of shaders to the file.
        """

        fn = "<unknown>"

        try:
            fn = renpy.loader.get_path(self.filename)

            tmp = fn + ".tmp"

            with io.open(tmp, "w", encoding="utf-8") as f:
                shaders = set(self.cache.keys()) | self.missing

                for i in shaders:
                    f.write(u" ".join(i) + "\r\n")

            try:
                os.unlink(fn)
            except:
                pass

            os.rename(tmp, fn)

        except:
            renpy.display.log.write("Saving shaders to {!r}:".format(fn))
            renpy.display.log.exception()

    def load(self):
        """
        Loads the list of shaders from the file, and compiles all shaders
        for which the parts exist, and for which compilation can succeed.
        """

        try:
            f = renpy.loader.load(self.filename)
        except:
            renpy.display.log.write("Could not open {!r}:".format(self.filename))
            return

        for l in f:
            l = l.strip()
            partnames = tuple(l.strip().split())

            if not partnames:
                continue

            if not self.check(partnames):
                self.missing.add(partnames)
                continue

            try:
                self.get(partnames)
            except:
                renpy.display.log.write("Precompiling shader {!r}:".format(partnames))
                renpy.display.log.exception()
                self.missing.add(partnames)

        f.close()
