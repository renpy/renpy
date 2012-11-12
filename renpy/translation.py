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
import collections
import os
import codecs
import time

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

        # A map from filename to a list of (label, translate) pairs found in 
        # that file.
        self.file_translates = collections.defaultdict(list)

    def take_translates(self, nodes):
        """
        Takes the translates out of the flattened list of statements, and stores
        them into the dicts above.
        """

        label = None
        filename = None
    
        for n in nodes:

            if isinstance(n.name, basestring):
                label = n.name

            if not isinstance(n, renpy.ast.Translate):
                continue

            if filename is None:
                filename = renpy.exports.unelide_filename(n.filename)
                filename = os.path.normpath(os.path.abspath(filename))
            
            if n.language is None:
                self.default_translates[n.identifier] = n
                self.file_translates[filename].append((label, n))
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


class TranslateFile(object):
    
    def __init__(self, filename, language):
        self.filename = filename
        self.language = language
        
        commondir = os.path.normpath(renpy.config.commondir)
        gamedir = os.path.normpath(renpy.config.gamedir)
            
        if filename.startswith(commondir):
            self.tl_filename = os.path.join(renpy.config.gamedir, "tl", language, "common.rpy")
        elif filename.startswith(gamedir):
            fn = os.path.relpath(filename, gamedir)
            self.tl_filename = os.path.join(renpy.config.gamedir, "tl", language, fn)
        
        self.f = None

        # ...
       
        self.close()
            
    def open(self):
        """
        Opens a translation file.
        """
        
        if self.f is not None:
            return
        
        if not os.path.exists(self.tl_filename):
            dn = os.path.dirname(self.tl_filename)

            try:
                os.makedirs(dn)
            except:
                pass

            f = open(self.tl_filename, "a")
            f.write(codecs.BOM_UTF8)
        
        else:
            f = open(self.tl_filename, "a")

        self.f = codecs.EncodedFile(f, "utf-8")
        
        self.f.write(u"# Translation updated at {}\n".format(time.strftime("%Y-%m-%d %H:%M")))
        self.f.write(u"\n")

    def close(self):
        if self.f is not None:
            return self.f

    def write_translates(self):
        
        translator = renpy.game.script.translator

        for label, t in translator.file_translates[self.filename]:
            print label, t

def translate_command():
    """
    The translate command. When called from the command line, this generates
    the translations.
    """
    
    ap = renpy.arguments.ArgumentParser(description="Generates or updates translations.")
    ap.add_argument("language", help="The language to generate translations for.")
    args = ap.parse_args()
    
    for dirname, filename in renpy.loader.listdirfiles():
        if dirname is None:
            continue

        filename = os.path.join(dirname, filename)
        
        if not (filename.endswith(".rpy") or filename.endswith(".rpym")):
            continue
        
        filename = os.path.normpath(filename)
        TranslateFile(filename, args.language)

    return False

renpy.arguments.register_command("translate", translate_command)
    