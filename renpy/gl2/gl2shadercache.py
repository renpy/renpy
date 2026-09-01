# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

import re
import os

import renpy

# A map from shader part name to ShaderPart
shader_part = {}

# The name of the variable a fragment shader writes its color to, when the
# modern dialect is being emitted (for legacy support, as GLSL ES 3.00 removed
# gl_FragColor).
FRAGMENT_OUTPUT = "fragment_color"

# The GLSL versions each dialect is emitted as.
DIALECT_VERSIONS = {
    100: (100, 120),
    300: (300, 330),
}

# The GLSL dialects a shader part can be authored in, from oldest to newest.
DIALECTS = tuple(sorted(DIALECT_VERSIONS))

# A map from a GLSL version to the dialect it belongs to. A part can declare
# either spelling.
GLSL_DIALECTS = {version: dialect for dialect, versions in DIALECT_VERSIONS.items() for version in versions}

# The GLSL versions shaders can be emitted in.
GLSL_VERSIONS = tuple(sorted(GLSL_DIALECTS))

# The names below are only rewritten when they stand alone.
STANDALONE = r"(?<![\w.]){}\b"

# Rewrites applied to a shader part authored in the legacy dialect.
LEGACY_TO_MODERN = [
    (re.compile(STANDALONE.format("texture2DProjLod")), "textureProjLod"),
    (re.compile(STANDALONE.format("texture2DLod")), "textureLod"),
    (re.compile(STANDALONE.format("texture2DProj")), "textureProj"),
    (re.compile(STANDALONE.format("texture2D")), "texture"),
    (re.compile(STANDALONE.format("textureCubeLod")), "textureLod"),
    (re.compile(STANDALONE.format("textureCube")), "texture"),
    (re.compile(STANDALONE.format("gl_FragColor")), FRAGMENT_OUTPUT),
]

# The reverse. Note that a part that uses a feature the legacy dialect lacks
# will fail to compile with an error and source code.
MODERN_TO_LEGACY = [
    (re.compile(STANDALONE.format(FRAGMENT_OUTPUT)), "gl_FragColor"),
    (re.compile(r"(?<![\w.])textureProj\s*\("), "texture2DProj("),
    (re.compile(r"(?<![\w.])texture\s*\("), "texture2D("),
]


# Strip comments so they can't cause errors in parsing.
GLSL_COMMENTS = re.compile(r"//[^\n]*|/\*.*?\*/", re.S)

# Builtins that only exist in the legacy dialect, used to check for version
# errors.
LEGACY_MARKERS = [
    (re.compile(STANDALONE.format("gl_FragColor")), "gl_FragColor", FRAGMENT_OUTPUT),
    (re.compile(STANDALONE.format("gl_FragData")), "gl_FragData", FRAGMENT_OUTPUT),
    (re.compile(STANDALONE.format("texture2DProjLod")), "texture2DProjLod", "textureProjLod"),
    (re.compile(STANDALONE.format("texture2DLod")), "texture2DLod", "textureLod"),
    (re.compile(STANDALONE.format("texture2DProj")), "texture2DProj", "textureProj"),
    (re.compile(STANDALONE.format("texture2D")), "texture2D", "texture"),
    (re.compile(STANDALONE.format("textureCubeLod")), "textureCubeLod", "textureLod"),
    (re.compile(STANDALONE.format("textureCube")), "textureCube", "texture"),
]

# The modern spelling of each legacy storage qualifier.
LEGACY_STORAGE = {
    "attribute": "in",
    "varying": "out",
}

# The constructs each dialect introduced that are only spelled differently in an
# older one.
TRANSLATED_MARKERS = {
    300: [
        (re.compile(STANDALONE.format(FRAGMENT_OUTPUT)), FRAGMENT_OUTPUT),
        (re.compile(r"(?<![\w.])texture\s*\("), "texture"),
    ],
}

# The constructs each dialect introduced that an older one has no equivalent
# for, which hold a part to the dialect that introduced them.
UNTRANSLATED_MARKERS = {
    300: [
        (re.compile(STANDALONE.format("textureSize")), "textureSize"),
        (re.compile(STANDALONE.format("texelFetch")), "texelFetch"),
        (re.compile(STANDALONE.format("textureGrad")), "textureGrad"),
        (re.compile(STANDALONE.format("textureLod")), "textureLod"),
        (re.compile(STANDALONE.format("textureProjLod")), "textureProjLod"),
        (re.compile(STANDALONE.format("switch")), "switch"),
        (re.compile(r"%"), "the % operator"),
        (re.compile(r"<<|>>"), "a bitwise shift"),
        (re.compile(r"(?<!&)&(?!&)|(?<!\|)\|(?!\|)|(?<!\^)\^(?!\^)"), "a bitwise operator"),
    ],
}

# The variable types each dialect introduced.
UNTRANSLATED_TYPES = {
    300: {"int", "ivec2", "ivec3", "ivec4", "bool", "bvec2", "bvec3", "bvec4"},
}

# Varying types that GLSL ES 3.00 and GLSL 3.30 refuse to interpolate.
FLAT_TYPES = UNTRANSLATED_TYPES[300]


def dialect_name(dialect):
    return "GLSL ES {}.{:02d}".format(dialect // 100, dialect % 100)


def newer_markers(dialect):
    for d in DIALECTS:
        if d <= dialect:
            continue

        for pattern, name in TRANSLATED_MARKERS.get(d, []) + UNTRANSLATED_MARKERS.get(d, []):
            yield d, pattern, name


def config_dialect():
    """
    The dialect selected by config.glsl_version, used by shader parts that
    don't declare one of their own.
    """

    version = renpy.config.glsl_version

    if version not in GLSL_DIALECTS:
        raise Exception(
            "config.glsl_version is {!r}, which is not a known GLSL dialect. Use {}.".format(
                version, ", or ".join("{} for {}".format(d, dialect_name(d)) for d in DIALECTS)
            )
        )

    return GLSL_DIALECTS[version]


def parse_glsl_version(s):
    """
    Parses the string returned by glGetString(GL_SHADING_LANGUAGE_VERSION).
    """

    if s is None:
        return None

    m = re.search(r"(\d+)\.(\d+)", s)

    if m is None:
        return None

    return int(m.group(1)) * 100 + int(m.group(2).ljust(2, "0"))


def dialect_version(gles, dialect):
    gles_version, desktop_version = DIALECT_VERSIONS[dialect]

    return gles_version if gles else desktop_version


def emit_version(gles, glsl_version):
    """
    Given the GLSL version the current context reports supporting, returns
    the version Ren'Py will actually emit shaders in.
    """

    if glsl_version is None:
        glsl_version = 0

    rv = dialect_version(gles, DIALECTS[0])

    for dialect in DIALECTS:
        version = dialect_version(gles, dialect)

        if glsl_version >= version:
            rv = version

    return rv


def translate(text, source_version, target_version):
    """
    Translates a chunk of shader source between dialects, if it wasn't authored
    in the one being emitted.

    `source_version`
        The dialect the text was authored in, one of DIALECTS.

    `target_version`
        The GLSL version being emitted, one of GLSL_VERSIONS.
    """

    target_dialect = GLSL_DIALECTS[target_version]

    if source_version == target_dialect:
        return text

    if source_version > target_dialect:
        rules = MODERN_TO_LEGACY
    else:
        rules = LEGACY_TO_MODERN

    for pattern, replacement in rules:
        text = pattern.sub(replacement, text)

    return text


def merge_variables(variables):
    merged = {}

    for v in variables:
        key = (v.storage, v.type, v.name, v.array)
        old = merged.get(key, None)

        merged[key] = v if old is None else old.merge(v)

    return sorted(merged.values(), key=lambda x: (x.name, x.storage, x.type))


def link_variables(vertex_variables, fragment_variables):
    """
    Merges the two stages' variables, unifying the qualifiers of each varying that
    appears in both.
    """

    vertex = merge_variables(vertex_variables)
    fragment = merge_variables(fragment_variables)

    linked = {}

    for v in vertex + fragment:
        if v.storage != "varying":
            continue

        if v.name not in linked:
            linked[v.name] = v
            continue

        old = linked[v.name]

        # None for any name the stages disagree about
        if old is None:
            continue
        elif (old.type, old.array) == (v.type, v.array):
            linked[v.name] = old.merge(v)
        else:
            linked[v.name] = None

    def relink(variables):
        return [ linked.get(v.name) or v if v.storage == "varying" else v for v in variables ]

    return relink(vertex), relink(fragment)


def register_shader(name, **kwargs):
    """
    :doc: register_shader

    This registers a shader part. This takes `name`, and then
    keyword arguments.

    `name`
        A string giving the name of the shader part. Names starting with an
        underscore or "renpy." are reserved for Ren'Py.

    `glsl`
        The GLSL dialect this shader part is written in: 300 for GLSL ES 3.00
        or 100 for GLSL ES 1.00.

        This defaults to None, meaning the part follows
        :var:`config.glsl_version`: 300 for new games and 100 for games that
        declare compatibility with Ren'Py 8.5 or earlier.

        Ren'Py translates between the two dialects as needed, so a ``glsl=300``
        part still runs on a device that only provides GLSL ES 1.00 unless it
        uses a feature not present in the older version.

        A part that doesn't declare a dialect, and would be treated as GLSL ES
        3.00, is checked for constructs that only exist in GLSL ES 1.00 - such
        as ``gl_FragColor``, ``texture2D``, ``attribute``, and ``varying``.
        Finding one is an error, since it means the part was written for the
        older dialect but did not declare as much.

        Layout qualifiers are reserved for declaring additional fragment outputs
        once multiple render targets are supported: location 0 is Ren'Py's
        ``fragment_color``, and outputs declared by a shader part will start at 1.
        A plain ``out`` will continue to mean a value passed from the vertex shader
        to the fragment shader.

    `variables`
        The variables used by the shader part. These should be listed one per
        line, a storage class followed by a type, name, and semicolon.

        With ``glsl=300``, the storage class is ``uniform``, ``in`` for a
        value that comes from the mesh, or ``out`` for a value the vertex
        shader passes to the fragment shader::

            variables='''
            uniform sampler2D tex0;
            in vec2 a_tex_coord;
            out vec2 v_tex_coord;
            '''

        With ``glsl=100``, it is ``uniform``, ``attribute``, or ``varying``::

            variables='''
            uniform sampler2D tex0;
            attribute vec2 a_tex_coord;
            varying vec2 v_tex_coord;
            '''

    `vertex_functions`
        If given, a string containing functions that will be included in the
        vertex shader.

    `fragment_functions`
        If given, a string containing functions that will be included in the
        fragment shader.

    Other keyword arguments should start with ``vertex_`` or ``fragment_``,
    and end with an integer priority. So "fragment_200" or "vertex_300". These
    give text that's placed in the appropriate shader at the given priority,
    with lower priority numbers inserted before higher priority numbers.
    """

    return ShaderPart(name, **kwargs)


class ShaderPart(object):
    """
    Arguments are as for register_shader.

    """

    def __init__(
        self,
        name,
        variables="",
        vertex_functions="",
        fragment_functions="",
        private_uniforms=False,
        glsl=None,
        **kwargs,
    ):
        if not re.match(r"^[\w\.]+$", name):
            raise Exception(
                "The shader name {!r} contains an invalid character. Shader names are limited to ASCII alphanumeric characters, _, and .".format(
                    name
                )
            )

        if (glsl is not None) and (glsl not in GLSL_DIALECTS):
            options = ", or ".join(
                "glsl={} (or the equivalent glsl={}) for {}".format(gles, desktop, dialect_name(d))
                for d, (gles, desktop) in sorted(DIALECT_VERSIONS.items())
            )

            raise Exception("In shader {}: glsl={!r} is not a known GLSL dialect. Use {}.".format(name, glsl, options))

        self.name = name
        shader_part[name] = self

        self.declared_glsl = GLSL_DIALECTS[glsl] if (glsl is not None) else None

        # True once this part has been checked for legacy constructs.
        self.checked_glsl = False

        # The oldest dialect this part can be emitted in and the construct that
        # requires it.
        self.found_dialect = None
        self.found_feature = None

        # The legacy storage qualifier this part declared a variable with, if
        # any.
        self.legacy_storage = None

        self.vertex_functions = self.substitute_name(vertex_functions)
        self.fragment_functions = self.substitute_name(fragment_functions)

        # A list of priority, text pairs for each section of the vertex and fragment shaders.
        self.vertex_parts = []
        self.fragment_parts = []

        # Sets of (storage, type, name) tuples, where storage is one of 'uniform', 'attribute', or 'varying',
        self.vertex_variables = set()
        self.fragment_variables = set()

        # A map from variable name to type.
        self.variable_types = {}

        # A sets of variable names used in the vertex and fragments shader.
        vertex_used = set()
        fragment_used = set()

        for m in re.finditer(r"\b\w+\b", self.vertex_functions):
            vertex_used.add(m.group(0))

        for m in re.finditer(r"\b\w+\b", self.fragment_functions):
            fragment_used.add(m.group(0))

        self.uniforms = []

        for k, v in kwargs.items():
            shader, _, priority = k.partition("_")

            v = self.substitute_name(v)

            if not priority:
                # Trigger error handling.
                shader = None

            try:
                priority = int(priority)
            except Exception:
                shader = None

            if shader == "vertex":
                parts = self.vertex_parts
                used = vertex_used
            elif shader == "fragment":
                parts = self.fragment_parts
                used = fragment_used
            else:
                raise Exception("Keyword arguments to ShaderPart must be of the form {vertex,fragment}_{priority}.")

            parts.append((priority, name, v))

            for m in re.finditer(r"\b\w+\b", v):
                used.add(m.group(0))

        variables = self.substitute_name(variables)

        for l in variables.split("\n"):
            l = l.partition("//")[0]
            l = l.strip()
            if not l:
                continue

            if self.legacy_storage is None:
                m = re.search(r"\b(attribute|varying)\b", l)

                if m is not None:
                    self.legacy_storage = m.group(1)

            v = renpy.gl2.gl2shader.Variable(self.name, l)

            if v.storage not in {"uniform", "attribute", "varying"}:
                raise Exception(
                    "In shader {}: Unknown shader variable line {!r}. Only the form '{{uniform,in,out}} {{type}} {{name}};' is allowed, or the equivalent '{{uniform,attribute,varying}} {{type}} {{name}};'.".format(
                        self.name, l
                    )
                )

            if v.array:
                self.variable_types[v.name] = v.type + "[]"
            else:
                self.variable_types[v.name] = v.type

            if v.name in vertex_used:
                self.vertex_variables.add(v)

            if v.name in fragment_used:
                self.fragment_variables.add(v)

            if v.storage == "uniform" and not private_uniforms:
                renpy.display.transform.add_uniform(v.name, v.type)

            if v.storage == "uniform":
                self.uniforms.append(v.name)

        self.raw_variables = variables

    @property
    def glsl(self):
        """
        The dialect this part is written in, one of DIALECTS.

        A part that didn't declare one follows config.glsl_version.
        """

        if self.declared_glsl is not None:
            return self.declared_glsl

        rv = config_dialect()

        # A part that says nothing is checked against the dialect it's been
        # given, in whichever direction that is.
        if not self.checked_glsl:
            if rv > DIALECTS[0]:
                self.check_legacy_syntax(rv)
            else:
                self.check_modern_syntax(rv)

            self.checked_glsl = True

        return rv

    @property
    def minimum_dialect(self):
        if self.found_dialect is None:
            self.find_minimum_dialect()

        return self.found_dialect

    @property
    def minimum_feature(self):
        if self.found_dialect is None:
            self.find_minimum_dialect()

        return self.found_feature

    def find_minimum_dialect(self):
        text = self.part_source()

        found = DIALECTS[0]
        feature = None

        for dialect in DIALECTS:
            if dialect <= found:
                continue

            name = next((n for pattern, n in UNTRANSLATED_MARKERS.get(dialect, []) if pattern.search(text)), None)

            if name is None:
                name = self.untranslated_interpolation(dialect)

            if name is None:
                name = self.untranslated_type(dialect)

            if name is not None:
                found = dialect
                feature = name

        self.found_dialect = found
        self.found_feature = feature

    def untranslated_type(self, dialect):
        types = UNTRANSLATED_TYPES.get(dialect, ())

        for v in self.vertex_variables | self.fragment_variables:
            if (v.storage != "uniform") and (v.type in types):
                return "{} {}".format(v.type, v.name)

        return None

    def untranslated_interpolation(self, dialect):
        if dialect < 300:
            return None

        for v in self.vertex_variables | self.fragment_variables:
            interpolation = getattr(v, "interpolation", None)

            if interpolation in {"flat", "noperspective"}:
                return f"{interpolation} interpolation on {v.name}"

        return None

    def part_source(self):
        """
        Every chunk of GLSL this part supplies, with comments stripped.
        """

        sources = [self.vertex_functions, self.fragment_functions]
        sources.extend(i[2] for i in self.vertex_parts)
        sources.extend(i[2] for i in self.fragment_parts)

        return GLSL_COMMENTS.sub(" ", "\n".join(i for i in sources if i))

    def check_modern_syntax(self, dialect):
        """
        Raises if this part uses a construct from a dialect newer than
        `dialect`, the one it's being treated as being written in.
        """

        # A part that also uses the legacy dialect is legacy
        if self.legacy_storage is not None:
            return

        text = self.part_source()

        for pattern, _legacy, _modern in LEGACY_MARKERS:
            if pattern.search(text):
                return

        for newer, pattern, name in newer_markers(dialect):
            if pattern.search(text):
                raise Exception(
                    f"Shader part {self.name} uses {name}, which needs {dialect_name(newer)}, but doesn't "
                    f"declare a dialect. Pass glsl={newer} to renpy.register_shader or rewrite it for "
                    f"{dialect_name(dialect)}."
                )

    def check_legacy_syntax(self, dialect):
        """
        Raises if this part uses a construct that only exists in the oldest
        dialect, but is being treated as being written in `dialect`.
        """

        found = None

        if self.legacy_storage is not None:
            found = (self.legacy_storage, LEGACY_STORAGE[self.legacy_storage])
        else:
            text = self.part_source()

            for pattern, legacy, modern in LEGACY_MARKERS:
                if pattern.search(text):
                    found = (legacy, modern)

                    break

        if found is not None:
            legacy, modern = found
            oldest = DIALECTS[0]

            raise Exception(
                f"Shader part {self.name} uses {legacy}, which only exists in {dialect_name(oldest)}, and "
                f"doesn't declare a dialect. Pass glsl={oldest} to renpy.register_shader or rewrite it for "
                f"{dialect_name(dialect)} ({legacy} becomes {modern}) and pass glsl={dialect}."
            )

    def expand_name(self, s):
        """
        Expands names starting with u__, a__, and v__ to include the shader part name.
        """

        name = self.name.replace(".", "_")

        if s.startswith("u__"):
            return "u_" + name + "_" + s[3:]
        elif s.startswith("a__"):
            return "a_" + name + "_" + s[3:]
        elif s.startswith("v__"):
            return "v_" + name + "_" + s[3:]
        elif s.startswith("l__"):
            return "l_" + name + "_" + s[3:]
        else:
            return s

    def expand_match(self, m):
        """
        Expands a match object using expand_name.
        """

        return self.expand_name(m.group(0))

    def expand_operation(self, m):
        """
        Expands an operation match object using expand_name.
        """

        return "u_{}_OP_{}".format(m.group(1), m.group(2))

    def substitute_name(self, s):
        rv = re.sub(r"\b[uavl]__\w+", self.expand_match, s)
        rv = re.sub(r"\bu_(\w+)__(\w+)", self.expand_operation, rv)
        return rv


# A map from a tuple giving the parts that comprise a shader, to the Shader
# object. The same shader might appear multiple times, to optimize performance.
cache = {}


def source(variables, parts, functions, fragment, gles, version):
    """
    Given lists of variables and parts, converts them into textual source
    code for a shader.

    `fragment`
        Should be set to true to generate the code for a fragment shader.

    `gles`
        True if this is an OpenGL ES context.

    `version`
        The GLSL version to emit, one of 100, 120, 300, or 330.
    """

    rv = []

    # The es suffix is what distinguishes GLSL ES from desktop GLSL, and it's
    # required from GLSL ES 3.00 on.
    if gles and version >= 300:
        rv.append("#version {} es\n".format(version))
    else:
        rv.append("#version {}\n".format(version))

    # Fragment shaders below GLSL ES 3.00 have to declare a default precision.
    if fragment and gles:
        if version >= 300:
            rv.append("""\
precision highp float;
precision highp int;
""")
        else:
            rv.append("""\
#ifdef GL_FRAGMENT_PRECISION_HIGH
    precision highp float;
    precision highp int;
#else
    precision mediump float;
    precision mediump int;
#endif
""")

    # gl_FragColor does not exist in the modern dialect.
    if fragment and version >= 300:
        rv.append("layout(location = 0) out vec4 {};\n".format(FRAGMENT_OUTPUT))

    for v in merge_variables(variables):
        rv.append(v.declaration(fragment, gles, version) + ";\n")

    for text, glsl in functions:
        rv.append(translate(text, glsl, version))

    rv.append("\nvoid main() {\n")

    parts.sort()

    for _, _, part, glsl in parts:
        rv.append(translate(part, glsl, version))

    rv.append("}\n")

    return "".join(rv)


shader_part_filter_cache = {}


class ShaderCache(object):
    """
    This class caches shaders that were compiled. It's also responsible for
    recording shaders that have been used, persisting them to disk, and then
    loading the shaders back into the cache.
    """

    def __init__(self, filename, gles, glsl_version=None):
        # The filename that we'll load the list of shaders from, and
        # persist it to.
        self.filename = filename

        # Are we gles?
        self.gles = gles

        # The GLSL version the context reports supporting, or None if it
        # couldn't be determined.
        self.glsl_version = glsl_version

        # The version shaders are emitted in. This may be lowered later, if a
        # shader turns out not to compile at the version we picked.
        forced = os.environ.get("RENPY_GLSL_VERSION", None)

        if forced is not None:
            if forced.strip() not in [str(i) for i in GLSL_VERSIONS]:
                raise Exception(
                    "RENPY_GLSL_VERSION is {!r}, which is not one of {}.".format(
                        forced, ", ".join(str(i) for i in GLSL_VERSIONS)
                    )
                )

            self.version = dialect_version(gles, GLSL_DIALECTS[int(forced)])

            self.pinned = True
        else:
            self.version = emit_version(gles, glsl_version)

            self.pinned = False

        # Part names that have been reported as being downgraded out of the
        # modern dialect, so that it's only reported once per part.
        self.downgraded = set()

        # A map from tuples of partnames to the shaders that have been
        # created.
        self.cache = {}

        # A set of tuples of partnames corresponding to shaders that existed
        # in the past, but do not exist now.
        self.missing = set()

        # True if this is dirty, and should be saved to the cache.
        self.dirty = False

    def get(self, partnames):
        """
        Gets a shader, creating it if necessary.

        `partnames`
            A tuple of strings, giving the names of the shader parts to include in
            the cache.
        """

        if renpy.config.shader_part_filter is not None:
            new_partnames = shader_part_filter_cache.get(partnames, None)
            if new_partnames is None:
                new_partnames = renpy.config.shader_part_filter(partnames)
                shader_part_filter_cache[partnames] = new_partnames

            partnames = new_partnames

        rv = self.cache.get(partnames, None)
        if rv is not None:
            return rv

        partnameset = set()
        partnamenotset = set()

        for i in partnames:
            if i.startswith("-"):
                partnamenotset.add(i[1:])
            else:
                partnameset.add(i)

        partnameset -= partnamenotset

        if "renpy.ftl" not in partnameset:
            partnameset.add(renpy.config.default_shader)

        sortedpartnames = tuple(sorted(partnameset))

        rv = self.cache.get(sortedpartnames, None)
        if rv is not None:
            self.cache[partnames] = rv
            return rv

        # If the cache missed entirely, we have to generate the source code for the
        # shaders.

        vertex_variables = []
        vertex_parts = []
        vertex_functions = []

        fragment_variables = []
        fragment_parts = []
        fragment_functions = []

        for i in sortedpartnames:
            p = shader_part.get(i, None)

            if p is None:
                raise Exception("{!r} is not a known shader part.".format(i))

            glsl = p.glsl

            if p.minimum_dialect > GLSL_DIALECTS[self.version] and i not in self.downgraded:
                self.downgraded.add(i)

                renpy.display.log.write(
                    "Shader part %r uses %s, which needs %s, but shaders are being emitted as GLSL %s "
                    "(this system reports GLSL %s). It will be translated, but may not compile.",
                    i,
                    p.minimum_feature,
                    dialect_name(p.minimum_dialect),
                    self.version,
                    self.glsl_version,
                )

            vertex_variables.extend(p.vertex_variables)
            vertex_parts.extend((prio, nm, text, glsl) for prio, nm, text in p.vertex_parts)
            vertex_functions.append((p.vertex_functions, glsl))

            fragment_variables.extend(p.fragment_variables)
            fragment_parts.extend((prio, nm, text, glsl) for prio, nm, text in p.fragment_parts)
            fragment_functions.append((p.fragment_functions, glsl))

        # A varying's two halves come from different parts, so its qualifiers are only
        # consistent once both stages have been considered together.
        vertex_variables, fragment_variables = link_variables(vertex_variables, fragment_variables)

        from renpy.gl2.gl2shader import Program, ShaderError

        def build(version):
            vertex = source(vertex_variables, vertex_parts, vertex_functions, False, self.gles, version)
            fragment = source(fragment_variables, fragment_parts, fragment_functions, True, self.gles, version)

            self.log_shader("vertex", sortedpartnames, vertex)
            self.log_shader("fragment", sortedpartnames, fragment)

            rv = Program(sortedpartnames, vertex, fragment)
            rv.load()

            return rv

        try:
            rv = build(self.version)

        except ShaderError as e:
            # The context claimed to support the version we picked, but this
            # shader didn't survive being emitted in it. Drop back to the oldest
            # dialect every part in it can be emitted in, for the rest of the
            # session.

            dialect = max(shader_part[i].minimum_dialect for i in sortedpartnames)

            fallback = dialect_version(self.gles, dialect)

            if self.pinned or (fallback >= self.version):
                raise

            failed_version = self.version
            rv = build(fallback)
            self.version = fallback

            renpy.display.log.write(
                "Shader %r did not compile as GLSL %s, so shaders will be emitted as GLSL %s "
                "for the rest of this session. This system reports supporting GLSL %s. The error was: %s",
                sortedpartnames,
                failed_version,
                fallback,
                self.glsl_version,
                e,
            )

        self.cache[partnames] = rv
        self.cache[sortedpartnames] = rv

        self.dirty = True

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

        if not self.dirty:
            return

        if not renpy.config.developer:
            return

        fn = "<unknown>"

        try:
            fn = os.path.join(renpy.config.gamedir, renpy.loader.get_path(self.filename))

            tmp = fn + ".tmp"

            with open(tmp, "w", encoding="utf-8") as f:
                shaders = set(self.cache.keys()) | self.missing

                for i in sorted(shaders):
                    f.write(" ".join(i) + "\n")

            try:
                os.unlink(fn)
            except Exception:
                pass

            os.rename(tmp, fn)

            self.dirty = False

        except Exception:
            renpy.display.log.write("Saving shaders to {!r}:".format(fn))
            renpy.display.log.exception()

    def load(self):
        """
        Loads the list of shaders from the file, and compiles all shaders
        for which the parts exist, and for which compilation can succeed.
        """

        try:
            with renpy.loader.load(self.filename) as f:
                for l in f:
                    l = l.strip().decode("utf-8")
                    partnames = tuple(l.strip().split())

                    if not partnames:
                        continue

                    if not self.check(partnames):
                        self.missing.add(partnames)
                        continue

                    try:
                        self.get(partnames)
                    except Exception:
                        renpy.display.log.write("Precompiling shader {!r}:".format(partnames))
                        renpy.display.log.exception()
                        self.missing.add(partnames)
        except Exception:
            renpy.display.log.write("Could not open {!r}:".format(self.filename))
            return

    def clear(self):
        """
        Clears the shader cache and the shaders inside it.
        """

        self.cache.clear()
        self.missing.clear()

    def log_shader(self, kind, partnames, text):
        """
        Logs the shader text to the log.
        """

        if not renpy.config.log_gl_shaders:
            return

        name = kind + " " + ", ".join(partnames) + " "
        name = name + "-" * max(0, 80 - len(name))

        renpy.display.log.write("%s", name)
        renpy.display.log.write("%s", text)
        renpy.display.log.write("-" * 80)
