#!/usr/bin/env python3

from __future__ import print_function
from xml.etree.ElementTree import parse, tostring
import collections
import itertools
import os
import sys

os.chdir(os.path.dirname(sys.argv[0]))

# Bad/weird types we don't need or want to generate.
BAD_TYPES = {
    "GLVULKANPROCNV",
    "GLvdpauSurfaceNV",
    "GLhalfNV",
    "struct _cl_event",
    "struct _cl_context",
    "GLDEBUGPROCAMD",
    "GLDEBUGPROCKHR",
    "GLDEBUGPROCARB",
    "GLDEBUGPROC",
    "GLsync",
}


BAD_COMMANDS = {
    "glAttachObjectARB",
    "glDetachObjectARB",
}

def snarf(fn):
    with open(os.path.join(os.path.dirname(__file__), fn)) as f:
        return f.read() + "\n"


UGUUGL_PXD_HEADER = snarf("uguugl_pxd_header.pxd")
UGUUGL_PYX_HEADER = snarf("uguugl_pyx_header.pyx")
UGUU_PYX_HEADER = snarf("uguu_pyx_header.pyx")

FRAMEBUFFER_EXT_FUNCTIONS = {
    "glBindFramebuffer",
    "glBindRenderbuffer",
    "glDeleteFramebuffers",
    "glDeleteRenderbuffers",
    "glFramebufferRenderbuffer",
    "glFramebufferTexture2D",
    "glGenFramebuffers",
    "glGenRenderbuffers",
    "glRenderbufferStorage",
}

GL_FEATURES = [
    "GL_VERSION_1_0",
    "GL_VERSION_1_1",
    "GL_VERSION_1_2",
    "GL_VERSION_1_3",
    "GL_VERSION_1_4",
    "GL_VERSION_1_5",
    "GL_VERSION_2_0",
    "GL_VERSION_2_1",
    "GL_VERSION_3_0",
    ]

GLES_FEATURES = [
    "GL_ES_VERSION_2_0",
    "GL_ES_VERSION_3_0",
    ]


def type_and_name(node):
    name = node.findtext("name")
    text = "".join(node.itertext()).strip()
    type_ = text[:-len(name)]

    return type_, name


def python_type(t):
    """
    Converts the OpenGL type t into a Python type.
    """

    if not "*" in t:
        return t

    print("Weird type", t)


class Command:

    def __init__(self, node):
        self.return_type = type_and_name(node.find("proto"))[0].strip()

        self.parameters = [ ]
        self.parameter_types = [ ]

        for i in node.findall("param"):
            t, n = type_and_name(i)
            self.parameters.append(n)
            self.parameter_types.append(t)

        self.aliases = set()

    def format_param_list(self):
        l = [ ]

        for name, type_ in zip(self.parameters, self.parameter_types):
            l.append(f"{type_} {name}")

        return "(" + ", ".join(l) + ")"

    def format_proxy_call(self):
        return "(" + ", ".join(self.parameters) + ")"

    def typedef(self, name):
        return "ctypedef {} (__stdcall *{}){} nogil".format(self.return_type, name, self.format_param_list())


class Feature:

    def __init__(self):
        self.commands = set()
        self.enums = set()

    def from_node(self, node):

        for i in node.findall("require/enum"):
            self.enums.add(i.attrib["name"])

        for i in node.findall("require/command"):
            self.commands.add(i.attrib["name"])

    def __or__(self, other):
        rv = Feature()
        rv.commands = self.commands | other.commands
        rv.enums = self.enums | other.enums
        return rv

    def __and__(self, other):
        rv = Feature()
        rv.commands = self.commands & other.commands
        rv.enums = self.enums & other.enums
        return rv


class XMLToPYX:

    def __init__(self):
        self.root = parse("gl.xml").getroot()

        self.types = [ ]
        self.type_names = [ ]

        self.convert_types()

        # A map from command name to command.
        self.commands = { }

        self.find_commands()

        # A map from enum name to value.
        self.enums = collections.OrderedDict()

        self.find_enums()

        # A map from feature name to value.
        self.features = { } 

        # The features, merged together.
        self.merged = None # type:Feature|None

        self.find_features()
        self.select_features()

        with open("../../renpy/uguu/gl.pxd", "w") as f:
            self.generate_uguugl_pxd(f)

        with open("../../renpy/uguu/gl.pyx", "w") as f:
            self.generate_uguugl_pyx(f)

        with open("../../renpy/uguu/uguu.pyx", "w") as f:
            self.generate_uguu_pyx(f)

    def convert_types(self):
        types = self.root.find('types')

        for t in types:
            if t.get("api", ""):
                continue

            name = t.find("name")
            if name is None:
                continue

            name = name.text
            if name in BAD_TYPES:
                continue

            self.type_names.append(name)

            text  = "".join(t.itertext())

            text = text.replace(";", "")
            text = text.replace("typedef", "ctypedef")

            self.types.append(text)

    def add_command(self, node):
        name = type_and_name(node.find("proto"))[1]

        if name in BAD_COMMANDS:
            return

        names = [ name ]

        for i in node.findall("alias"):
            names.append(i.attrib["name"])

        for i in names:
            c = self.commands.get(i, None)
            if c is not None:
                break
        else:
            c = Command(node)

        for i in names:
            c.aliases.add(i)
            self.commands[i] = c

    def find_commands(self):
        commands = self.root.find("commands")

        for c in commands.findall("command"):
            self.add_command(c)

    def find_enums(self):

        for enums in self.root.findall("enums"):
            for i in enums.findall("enum"):
                value = i.attrib["value"]
                name = i.attrib["name"]

                self.enums[name] = value

                alias = i.attrib.get("alias", None)

                if alias is not None:
                    self.enums[alias] = value

    def find_features(self):

        for i in itertools.chain(
                self.root.findall("feature"),
                self.root.findall("extensions/extension")
                ):

            name = i.attrib["name"]

            f = Feature()
            f.from_node(i)
            self.features[name] = f

            # print(name)

    def select_features(self):

        gl = Feature()

        for i in GL_FEATURES:
            gl = gl | self.features[i]

        gles = Feature()

        for i in GLES_FEATURES:
            gles = gles | self.features[i]

        f = gl & gles

        self.merged = f

    def generate_uguugl_pxd(self, f):

        f.write(UGUUGL_PXD_HEADER)

        def w(s):
            f.write(s + "\n")

        w('cdef extern from "renpygl.h":')
        w('')

        for l in self.types:
            w(f"    {l}")

        enums = list(self.merged.enums)
        enums.sort(key=lambda n : (int(self.enums[n], 0), n))

        w(f'')

        for i in enums:
            w(f"    GLenum {i}")

        for i in sorted(self.merged.commands):
            typename = i + "_type"
            c = self.commands[i]

            w("")
            w(c.typedef(typename))
            w(f"cdef {typename} {i}")

    def generate_uguugl_pyx(self, f):

        f.write(UGUUGL_PYX_HEADER)

        def w(s):
            f.write(s + "\n")

        for i in sorted(self.merged.commands):
            c = self.commands[i]

            w("")
            w(f"cdef {i}_type {i}")

            w("")

        w("")
        w("def load():")

        for i in sorted(self.merged.commands):

            names = list(self.commands[i].aliases)
            names.remove(i)
            names.sort()
            names.insert(0, i)

            if (i in FRAMEBUFFER_EXT_FUNCTIONS) and ((i + "EXT") not in names):
                names.append(i + "EXT")
                print(names)

            names = [ i.encode("utf-8") for i in names ]

            w(f"")
            w(f"    global {i}")
            w(f"    {i} = <{i}_type> find_gl_command({names!r})")

    def generate_uguu_pyx(self, f):

        def w(s):
            f.write(s + "\n")

        for l in self.type_names:
            w(f"from renpy.uguu.gl cimport {l}")

        w(f'')
        f.write(UGUU_PYX_HEADER)

        for l in self.type_names:
            w(f"from renpy.uguu.gl cimport {l}")

        for i in sorted(self.merged.commands):
            c = self.commands[i]

            if c.return_type.strip() == "void *":
                continue

            params = list(zip(c.parameters, c.parameter_types))
            param_list = ", ".join(c.parameters)

            w(f'')
            w(f"def {i}({param_list}):")

            for param, type_ in params:
                if "*" in type_:
                    w(f"    cdef ptr {param}_ptr = get_ptr({param})")

            proxy = [ ]

            for param, type_ in params:
                if "*" in type_:
                    proxy.append(f"<{type_}> {param}_ptr.ptr")
                else:
                    proxy.append(param)

            proxy = ", ".join(proxy)

            rt = c.return_type.strip()

            if rt == "void":
                w(f'    renpy.uguu.gl.{i}({proxy})')
            elif rt == "const GLubyte *":
                w(f'    return proxy_return_string(renpy.uguu.gl.{i}({proxy}))')
            else:
                w(f'    return renpy.uguu.gl.{i}({proxy})')

        # Expose the enums to python.

        enums = list(self.merged.enums)
        enums.sort(key=lambda n : (int(self.enums[n], 0), n))

        w(f'')

        for i in enums:
            w(f'{i} = renpy.uguu.gl.{i}')


if __name__ == "__main__":
    XMLToPYX()
