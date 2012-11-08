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
import re

class ScriptTranslator(object):

    def __init__(self):

        # A map from the translate identifier to the translate object used when the
        # language is None.
        self.default_translates = { }
        
        # A map from (identifier, language) to the translate object used for that
        # language.
        self.language_translates = { }

        # A list of (identifier, language) tuples that we need to chain together.
        self.chain_worklist = [ ]

    def take_translates(self, nodes):
        """
        Takes the translates out of the flattened list of statements, and stores
        them into the dicts above.
        """
    
        for n in nodes:
            if not isinstance(n, renpy.ast.Translate):
                continue
            
            if n.language is None:
                self.default_translates[n.identifier] = n
            else:
                self.language_translates[n.identifier, n.language] = n
                self.chain_worklist.append((n.identifier, n.language))
        
    def chain_translates(self):
        """
        Chains nodes in non-default translates together.
        """
        
        unchained = [ ]
        
        for identifier, language in self.chain_worklist:

            if identifier not in self.default_translates:
                unchained.append((identifier, language))
                continue

            translate = self.language_translates[identifier, language]            
            next_node = self.default_translates[identifier].next
            
            renpy.ast.chain_block(translate.block, next_node)

        self.chain_worklist = unchained

    def lookup_translate(self, identifier):
         
        language = renpy.game.preferences.language

        if language is not None:
            tl = self.language_translates.get((identifier, language), None)
        else:
            tl = None
            
        if tl is None:
            tl = self.default_translates[identifier]
        
        return tl.block[0]

def encode_say_string(s):
    """
    Encodes a string in the format used by Ren'Py say statements.
    """
    
    s = s.replace("\\", "\\\\")
    s = s.replace("\n", "\\n")
    s = s.replace("\"", "\\\"")
    s = re.sub(r'(?<= ) ', '\\ ', s)

    return "\"" + s + "\""

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

    tl = renpy.ast.Translate(loc, identifier, None, block)
    tl.name = block[0].name + ("translate",)
    
    ed = renpy.ast.EndTranslate(loc)
    ed.name = block[0].name + ("end_translate",)
    
    return [ tl, ed ]


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
                new_children.extend(tl)
                group = [ ]

            new_children.append(i)
                
    if group:
        nodes = create_translate(group)
        new_children.extend(nodes)
        group = [ ]

    children[:] = new_children
    

                
                

            
            
    