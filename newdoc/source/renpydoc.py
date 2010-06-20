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

            if token == Token.Error and value == "$":
                yield index, Token.Keyword, value

            elif token in Name and value in KEYWORDS:
                yield index, Token.Keyword, value

            elif token in Name and value in PROPERTIES:
                yield index, Name.Attribute, value

            else:
                yield index, token, value

def setup(app):
    app.add_description_unit('property', 'propref')
    app.add_lexer('renpy', RenPyLexer())
    
