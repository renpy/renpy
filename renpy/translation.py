# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
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

import renpy
import hashlib


def encode_say_string(s):
    """
    Encodes a string in the format used by Ren'Py say statements.
    """
    
    # TODO: Implement properly.
    
    return repr(s)

def create_translate(block):
    """
    Creates an ast.Translate that wraps `block`. The block may only contain
    translatable statements.
    """
    
    md5 = hashlib.md5()
    
    for i in block:
        code = i.get_code()
        md5.update(code + "\r\n")
        
    identifier = md5.hexdigest()
    loc = (block[0].filename, block[0].linenumber)

    rv = renpy.ast.Translate(loc, identifier, None, block)
    rv.name = block[0].name + ("translate",)
    return rv


def restructure(children):
    """
    This should be called with a list of statements. It restructures the statements
    in the list so that translatable statements are contained within translation blocks.
    """
    
    new_children = [ ]
    group = [ ]

    
    def finish_group():
        pass
    
    
    for i in children:
        
        if not isinstance(i, renpy.ast.Translate):
            i.restructure(restructure)
        
        if i.translatable:
            group.append(i)
        
        else:
            if group:
                tl = create_translate(group)
                new_children.append(tl)
                group = [ ]

            new_children.append(i)
                
    if group:
        tl = create_translate(group)
        new_children.append(tl)
        group = [ ]

    children[:] = new_children
    

                
                

            
            
    