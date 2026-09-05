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

import itertools
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Never
from xml.etree.ElementTree import Element, parse

import requests
from Cython.Tempita import sub

type StrElement = "Element[str]"

UGUU_ROOT = Path(__file__).parent.resolve()

RENPY_UGUU_ROOT = UGUU_ROOT.parent.parent / "renpy" / "uguu"

XML_COMMIT_SHA = "1cdd228e34966dd6b95bd203e9f84faba0f371a1"
"""
The commit SHA of the gl.xml file used by this script.
Reference repository: https://github.com/KhronosGroup/OpenGL-Registry
"""

XML_URL = f"https://raw.githubusercontent.com/KhronosGroup/OpenGL-Registry/{XML_COMMIT_SHA}/xml/gl.xml"

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


def malformed_xml(message: str) -> Never:
    raise Exception(f"Malformed XML: {message}")


def type_and_name(node: StrElement):
    name = node.findtext("name")
    if name is None:
        malformed_xml("Type with no name found")

    text = "".join(node.itertext()).strip()
    type_ = text[: -len(name)]

    return type_, name


class Command:
    """
    Holds the XML-derived facts about a GL command. This is pure parse
    output - it knows nothing about how it will be rendered, and is
    shared between every alias name that maps to it (see `aliases`).
    """

    def __init__(self, node: StrElement):
        proto = node.find("proto")
        if proto is None:
            malformed_xml("Command with no prototype found")

        self.return_type = type_and_name(proto)[0].strip()

        self.parameters_to_type: dict[str, str] = {}

        for i in node.findall("param"):
            t, n = type_and_name(i)
            t = t.strip()
            n = n.strip()
            if n in self.parameters_to_type:
                malformed_xml(f"Duplicate parameter name: {n}")

            self.parameters_to_type[n] = t

        self.aliases: set[str] = set()


@dataclass
class CommandView:
    """
    The render-facing model for a single required command name.

    A `Command` object is shared across every alias that resolves to the
    same underlying GL function; a `CommandView` is per required *name*
    (the value that shows up in `Feature.commands` and therefore in the
    generated pxd/pyx). All decisions that require branching on parameter
    types or return types are made here, in Python - the templates only
    interpolate the results, they don't re-derive them.
    """

    name: str
    typedef: str
    load_names: list[bytes]
    param_list: str
    pointer_params: list[str]
    proxy_call: str
    call_kind: Literal["void *", "void", "string", "value"]

class Feature:
    def __init__(self):
        self.commands: set[str] = set()
        self.enums: set[str] = set()

    def from_node(self, node: StrElement):
        for i in node.findall("require/enum"):
            self.enums.add(i.attrib["name"])

        for i in node.findall("require/command"):
            self.commands.add(i.attrib["name"])

    def __or__(self, other: "Feature") -> "Feature":
        rv = Feature()
        rv.commands = self.commands | other.commands
        rv.enums = self.enums | other.enums
        return rv

    def __and__(self, other: "Feature") -> "Feature":
        rv = Feature()
        rv.commands = self.commands & other.commands
        rv.enums = self.enums & other.enums
        return rv


class XMLToPYX:
    def __init__(self, root: StrElement):
        self.root = root

        # A map from type name to its definition.
        self.types: dict[str, str] = {}

        self.convert_types()

        # A map from command name to command.
        self.commands: dict[str, Command] = {}

        self.find_commands()

        # A map from enum name to value.
        self.enums: dict[str, str] = {}

        self.find_enums()

        # A map from feature name to value.
        self.features: dict[str, Feature] = {}

        # The features, merged together.
        self.merged: Feature = Feature()

        self.find_features()
        self.select_features()

    def convert_types(self):
        types = self.root.find("types")
        if types is None:
            malformed_xml("No types found in XML")

        for t in types:
            if t.get("api", ""):
                continue

            name = t.find("name")
            if name is None:
                continue

            name = name.text
            if name is None:
                malformed_xml("Type with no name found")

            if name in BAD_TYPES:
                continue

            text = "".join(t.itertext())

            text = text.replace(";", "")
            text = text.replace("typedef", "ctypedef")

            self.types[name] = text

    def add_command(self, node: StrElement):
        proto = node.find("proto")
        if proto is None:
            malformed_xml("Command with no prototype found")

        name = type_and_name(proto)[1]
        if name in BAD_COMMANDS:
            return

        names = [name]

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
        if commands is None:
            malformed_xml("No commands found in XML")

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
        for i in itertools.chain(self.root.iterfind("feature"), self.root.iterfind("extensions/extension")):
            name = i.attrib["name"]

            f = Feature()
            f.from_node(i)
            self.features[name] = f

    def select_features(self):
        gl = Feature()

        for i in GL_FEATURES:
            gl = gl | self.features[i]

        gles = Feature()

        for i in GLES_FEATURES:
            gles = gles | self.features[i]

        self.merged = gl & gles

    def get_template_data(self) -> dict[str, Any]:
        enums: list[str] = sorted(self.merged.enums, key=lambda n: (int(self.enums[n], 0), n))
        commands: list[CommandView] = []

        for name in sorted(self.merged.commands):
            command = self.commands[name]

            names: list[str] = list(command.aliases)
            names.remove(name)
            names.sort()
            names.insert(0, name)

            if (name in FRAMEBUFFER_EXT_FUNCTIONS) and ((name + "EXT") not in names):
                names.append(name + "EXT")

            load_names = [n.encode("utf-8") for n in names]

            proxy: list[str] = []
            pointer_params: list[str] = []
            typedef_params: list[str] = []

            for p, t in command.parameters_to_type.items():
                typedef_params.append(f"{t} {p}")
                if "*" in t:
                    proxy.append(f"<{t}> {p}_ptr.ptr")
                    pointer_params.append(p)
                else:
                    proxy.append(p)

            rt = command.return_type.strip()
            typedef = f"ctypedef {rt} (__stdcall *{name}_type)({', '.join(typedef_params)}) noexcept nogil"

            if rt == "void *":
                call_kind = "void *"
            elif rt == "void":
                call_kind = "void"
            elif rt == "const GLubyte *":
                call_kind = "string"
            else:
                call_kind = "value"

            view = CommandView(
                name=name,
                typedef=typedef,
                load_names=load_names,
                call_kind=call_kind,
                param_list=", ".join(command.parameters_to_type),
                pointer_params=pointer_params,
                proxy_call=", ".join(proxy),
            )
            commands.append(view)

        return {
            "types": self.types,
            "enums": enums,
            "commands": commands,
        }


def get_gl_xml() -> StrElement:
    commit_file = UGUU_ROOT / "gl.xml.commit"
    xml_file = UGUU_ROOT / "gl.xml"
    if commit_file.exists() and xml_file.exists():
        current_commit = commit_file.read_text().strip()
    else:
        current_commit = None

    if current_commit != XML_COMMIT_SHA:
        with requests.get(XML_URL) as r:
            xml_file.write_text(r.text)

        commit_file.write_text(XML_COMMIT_SHA)

    return parse(xml_file).getroot()


def generate_uguu_gl_pxd(data: dict[str, Any]):
    template = (UGUU_ROOT / "gl.pxd.in").read_text(encoding="utf-8")
    output = sub(template, **data)
    (RENPY_UGUU_ROOT / "gl.pxd").write_text(output, encoding="utf-8")


def generate_uguu_gl_pyx(data: dict[str, Any]):
    template = (UGUU_ROOT / "gl.pyx.in").read_text(encoding="utf-8")
    output = sub(template, **data)
    (RENPY_UGUU_ROOT / "gl.pyx").write_text(output, encoding="utf-8")


def generate_uguu_uguu_pyx(data: dict[str, Any]):
    template = (UGUU_ROOT / "uguu.pyx.in").read_text(encoding="utf-8")
    output = sub(template, **data)
    (RENPY_UGUU_ROOT / "uguu.pyx").write_text(output, encoding="utf-8")


if __name__ == "__main__":
    root = get_gl_xml()

    data = XMLToPYX(root).get_template_data()

    generate_uguu_gl_pxd(data)
    generate_uguu_gl_pyx(data)
    generate_uguu_uguu_pyx(data)
