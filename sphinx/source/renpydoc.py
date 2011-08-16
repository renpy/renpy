#@PydevCodeAnalysisIgnore
from pygments.lexers.agile import PythonLexer
from pygments.token import Token, Name

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

            elif token in Name and value in KEYWORDS:
                yield index, Token.Keyword, value

            elif token in Name and value in PROPERTIES:
                yield index, Name.Attribute, value

            else:
                yield index, token, value

import re
import sphinx.addnodes
import docutils.nodes

def parse_var_node(env, sig, signode):
    m = re.match(r'(\S+)(.*)', sig)

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
        print "duplicate id:", ref
        ref = ref + "_alt"

    style_seen_ids.add(ref)
        
    return ref


def setup(app):
    # app.add_description_unit('property', 'propref')
    app.add_lexer('renpy', RenPyLexer())
    app.add_object_type("var", "var", "single: %s (variable)",  parse_node=parse_var_node)
    app.add_object_type("style-property", "propref", "single: %s (style property)", parse_node=parse_style_node)
    app.add_object_type("transform-property", "tpref", "single: %s (transform property)")
    app.add_object_type("text-tag", "tt", "single: %s (text tag)")
    
