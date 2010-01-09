# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
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

import renpy

# The statement registry. It's a map from tuples giving the prefixes of
# statements to dictionaries giving the methods used for that statement.
registry = { }

def register(name, parse=None, lint=None, execute=None, predict=None, next=None, scry=None):

    if name == "":
        name = ()
    else:
        name = tuple(name.split())
    
    if registry.get(name) is not None:
        renpy.exports.error("The statement '%s' has already been registered." % (" ".join(name)))

    registry[name] = dict(parse=parse,
                          lint=lint,
                          execute=execute,
                          predict=predict,
                          next=next,
                          scry=scry)

    while True:
        name = name[:-1]
        if not name:
            break

        if name not in registry:
            registry[name] = None
        
def parse(node, line):

    block = [ (node.filename, node.linenumber, line, [ ]) ]
    l = renpy.parser.Lexer(block)
    l.advance()

    renpy.exports.push_error_handler(l.error)
    try:

        name = ()

        while True:

            cpt = l.checkpoint()
            word = l.word()

            if word is None:
                break

            newname = name + (word,)
            if newname not in registry:
                break

            name = newname

        l.revert(cpt)

        if registry[name] is None:
            renpy.exports.error("'%s' is the prefix of a statement, but not a statement." % (" ".join(name)))
            return None

        return ( name, registry[name]["parse"](l) )

    finally:
        renpy.exports.pop_error_handler()
        
        
def call(method, parsed, *args, **kwargs):
    name, parsed = parsed

    method = registry[name].get(method)
    if method is None:
        return None
    
    return method(parsed, *args, **kwargs)
