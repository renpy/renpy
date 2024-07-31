#@PydevCodeAnalysisIgnore
from __future__ import print_function
from pygments.lexers.agile import PythonLexer
from pygments.token import Token, Name, Operator
import sys

import keywords


KEYWORDS = set(keywords.keywords)
PROPERTIES = set(keywords.properties)


class RenPyLexer(PythonLexer):
    name = "Ren'Py"
    aliases = [ "renpy", "rpy" ]
    filenames = [ "*.rpy", "*.rpym" ]

    def get_tokens_unprocessed(self, text):
        for index, token, value in PythonLexer.get_tokens_unprocessed(self, text):

            if value.startswith("###"):
                continue

            if token == Token.Error and value == "$":
                yield index, Token.Keyword, value

            elif token in [ Name, Operator.Word ] and value in KEYWORDS:
                yield index, Token.Keyword, value

            elif token in Name and value in PROPERTIES:
                yield index, Name.Attribute, value

            else:
                yield index, token, value


import re
import sphinx.addnodes
import docutils.nodes
import sphinx.domains


def parse_var_node(env, sig, signode):
    m = re.match(r'(\S+)(.*)', sig)

    if m.group(1).split('.')[0] in [ "config", "gui" ]:
        signode += docutils.nodes.Text("define ", "define" )

    signode += sphinx.addnodes.desc_name(m.group(1), m.group(1))
    signode += docutils.nodes.Text(m.group(2), m.group(2))

    ref = m.group(1)
    return ref


style_seen_ids = set()

def parse_style_node(env, sig, signode):
    m = re.match(r'(\S+)(.*)', sig)

    name = m.group(1)
    desc = m.group(2)
    desc = " - " + desc

    signode += sphinx.addnodes.desc_name(name, name)
    signode += docutils.nodes.Text(desc, desc)

    ref = m.group(1)

    while ref in style_seen_ids:
        ref = ref + "_alt"

    style_seen_ids.add(ref)

    return ref


scpref_seen_ids = set()

def parse_scpref_node(env, sig, signode):
    m = re.match(r'(\S+)(.*)', sig)

    signode += sphinx.addnodes.desc_name(m.group(1), m.group(1))
    signode += docutils.nodes.Text(m.group(2), m.group(2))

    ref = m.group(1)

    while ref in scpref_seen_ids:
        ref = ref + "_alt"

    scpref_seen_ids.add(ref)

    return ref


class PythonIndex(sphinx.domains.Index):
    name = "function-class-index"
    localname = "Function and Class Index"
    shortname = ""

    def generate(self, docnames=None):


        if not isinstance(self.domain, sphinx.domains.python.PythonDomain):
            return [ ], False

        entries = [ ]

        for name, oe in self.domain.data['objects'].items():

            docname = oe.docname
            kind = oe.objtype

            if kind == "function" or kind == "class":
                entries.append((name, 0, docname, name, None, None, ''))

        print(len(entries), "entries")

        content = { }

        for name, subtype, docname, anchor, extra, qualifier, descr in entries:
            c = name[0].upper()

            if c not in content:
                content[c] = [ ]

            content[c].append((name, subtype, docname, anchor, extra, qualifier, descr))

        for i in content.values():
            i.sort()

        # self.domain.data['labels']["py-function-class-index"] = ("py-function-class-index", '', self.localname)

        return sorted(content.items()), False


class CustomIndex(sphinx.domains.Index):

    name = ""
    localname = ""
    shortname = ""
    kind = ""

    def generate(self, docnames=None):

        if not isinstance(self.domain, sphinx.domains.std.StandardDomain):
            return [ ], False

        entries = [ ]

        for (kind, name), (docname, anchor) in self.domain.data["objects"].items():

            if self.kind != kind:
                continue

            if docnames is not None and docname not in docnames:
                continue

            entries.append((name, 0, docname, anchor, None, None, ''))

        content = { }

        for name, subtype, docname, anchor, extra, qualifier, descr in entries:
            c = name[0].upper()

            if c not in content:
                content[c] = [ ]

            content[c].append((name, subtype, docname, anchor, extra, qualifier, descr))

        for i in content.values():
            i.sort()

        self.domain.data['labels'][self.kind + "-index"] = ("std-" + self.kind + "-index", '', self.localname)

        return sorted(content.items()), False


def add_index(app, domain, object_type, title):

    class MyIndex(CustomIndex):
        name = object_type + "-index"
        localname = title
        kind = object_type

    app.add_index_to_domain(domain, MyIndex)
    # app.domains[domain].indices.append(MyIndex)


def setup(app):
    # app.add_description_unit('property', 'propref')

    if sys.version_info[0] == 2:
        app.add_lexer("renpy", RenPyLexer())
    else:
        app.add_lexer('renpy', RenPyLexer)

    app.add_object_type("var", "var", "single: %s (variable)", parse_node=parse_var_node)
    app.add_object_type("style-property", "propref", "single: %s (style property)", parse_node=parse_style_node)
    app.add_object_type("transform-property", "tpref", "single: %s (transform property)")
    app.add_object_type("screen-property", "scpref", "single: %s (screen property)", parse_node=parse_scpref_node)
    app.add_object_type("text-tag", "tt", "single: %s (text tag)")
    app.add_object_type("textshader", "textshader" "single: %s (text shader)")

    add_index(app, "std", "style-property", "Style Property Index")
    add_index(app, "std", "transform-property", "Transform Property Index")
    add_index(app, "std", "var", "Variable Index")

    app.add_index_to_domain('py', PythonIndex)

    # app.domains['py'].indices.append(PythonIndex)
    # app.domains['std'].data['labels']['py-function-class-index'] = ('py-function-class-index', '', 'Function and Class Index')
