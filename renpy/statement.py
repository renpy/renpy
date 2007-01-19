# Copyright 2004-2007 PyTom <pytom@bishoujo.us>
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

# This module contains code to support user-defined statements.

class StatementRegistry(object):

    def __init__(self):
        # Map from sub-names to methods.
        self.methods = { }

    def parse(self, l):
        name = self.word()
        if name not in self.methods:
            # Signal an error.
            pass

        return name, self.methods[name]["parse"](l)
        
    def call(method, parse, *args, **kwargs):
        name, rest = parse

        if method not in self.methods[name]:
            return None

        return self.methods[name](rest, *args, **kwargs)

    def execute(self):
        return self.call("execute")

    def check(self):
        return self.call("check")

    def lint(self):
        return self.call("lint")

registry = StatementRegistry()
        
def parse(node, line):

    block = [ (node.loc[0], node.loc[1], line, [ ]) ]
    lexer = renpy.parser.Lexer(block)
    l.advance()

def call(method, parse, *args, **kwargs):
    return registry.call(method, parse, *args, **kwargs)
