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

# This file contains support for string translation and string formatting
# operations.

import renpy
import string
import os

update_translations = "RENPY_UPDATE_TRANSLATIONS" in os.environ

class Formatter(string.Formatter):
    """
    A string formatter that uses Ren'Py's formatting rules. Ren'Py uses 
    square brackets to introduce formatting, and it supports a q conversion
    that quotes the text being shown to the user.
    """
    
    def parse(self, s):
        """
        Parses s according to Ren'Py string formatting rules. Returns a list
        of (literal_text, field_name, format, replacement) tuples, just like
        the method we're overriding. 
        """

        # States for the parse state machine.
        LITERAL = 0
        OPEN_BRACKET = 1
        VALUE = 3
        FORMAT = 4
        CONVERSION = 5
        
        # The depth of brackets we've seen.
        bracket_depth = 0
        
        # The parts we've seen.
        literal = ''
        value = ''
        format = '' #@ReservedAssignment
        conversion = None
        
        state = LITERAL
        
        for c in s:
            
            if state == LITERAL:
                if c == '[':
                    state = OPEN_BRACKET
                    continue
                else:
                    literal += c
                    continue
                
            elif state == OPEN_BRACKET:
                if c == '[':
                    literal += c
                    state = LITERAL
                    continue
                
                else:
                    value = c
                    state = VALUE
                    bracket_depth = 0
                    continue
                                
            elif state == VALUE:
                
                if c == '[':
                    bracket_depth += 1
                    value += c
                    continue

                elif c == ']':
                    
                    if bracket_depth:
                        bracket_depth -= 1
                        value += c
                        continue
                    
                    else:
                        yield (literal, value, format, conversion)
                        state = LITERAL
                        literal = ''
                        value = ''
                        format = '' #@ReservedAssignment
                        conversion = None
                        continue
                    
                elif c == ':':
                    state = FORMAT
                    continue
                
                elif c == '!':
                    state = CONVERSION
                    conversion = ''
                    continue
                
                else:
                    value += c
                    continue
                
            elif state == FORMAT:
                
                if c == ']':
                    yield (literal, value, format, conversion)
                    state = LITERAL
                    literal = ''
                    value = ''
                    format = '' #@ReservedAssignment
                    conversion = None
                    continue

                elif c == '!':
                    state = CONVERSION
                    conversion = ''
                    continue
                
                else:
                    format += c
                    continue
                
                    
            elif state == CONVERSION:
                if c == ']':
                    yield (literal, value, format, conversion)
                    state = LITERAL
                    literal = ''
                    value = ''
                    format = '' #@ReservedAssignment
                    conversion = None
                    continue

                else:
                    conversion += c
                    continue

        if state != LITERAL:
            raise Exception("String {0!r} ends with an open format operation.".format(s))
        
        if literal:
            yield (literal, None, None, None)

    def convert_field(self, value, conversion):
        
        if not conversion:
            return value
        
        if "r" in conversion:
            value = repr(value)
        elif "s" in conversion:
            value = str(value)

        if "q" in conversion:
            value = value.replace("{", "{{")
            
        return value
            
# The instance of Formatter we use.
formatter = Formatter()

class MultipleDict(object):
    def __init__(self, *dicts):
        self.dicts = dicts
        
    def __getitem__(self, key):
        for d in self.dicts:
            if key in d:
                return d[key]
            
        raise KeyError(key)

def substitute(s, scope=None, force=False):
    """
    Performs translation and formatting on `s`, as necessary.
    
    `scope`
        The scope which is used in formatting, in addition to the default
        store.
        
    `force`
        Force substitution to occur, even if it's disabled in the config.
    """
    
    # Translate.
    if renpy.config.translator is not None:
        s = renpy.config.translator.translate(s) #@UndefinedVariable

    # Substitute.
    if not renpy.config.new_substitutions and not force:
        return s
    
    if "[" in s:
        
        if scope is not None:
            kwargs = MultipleDict(scope, renpy.store.__dict__) #@UndefinedVariable
        else:
            kwargs = renpy.store.__dict__ #@UndefinedVariable
            
        s = formatter.vformat(s, (), kwargs)

    return s
        

class Translator(renpy.object.Object):
    
    def unquote(self, s):
        s = s.replace("\\n", "\n")
        s = s.replace("\\\\", "\\")
        return s
    
    def quote(self, s):
        s = s.replace("\\", "\\\\")
        s = s.replace("\n", "\\n")
        return s
    
    def __init__(self, language):
        """
        Loads the translation from the file `language`.rpt
        """

        self.language = language
        self.translations = { }
        
        f = renpy.loader.load(language + ".rpt")
        
        old = None
        
        for l in f:
            l = l.decode("utf-8")
            l = l.rstrip()
            
            if not l:
                continue
            
            if l[0] == '#':
                continue
            
            s = self.unquote(l[2:])
            
            if l[0] == '<':
                if old:
                    raise Exception("String {0!r} does not have a translation.".format(old))
                
                old = s
                
            if l[0] == ">":
                if old is None:
                    raise Exception("Translation {0!r} doesn't belong to a string.".format(s))
                
                if old in self.translations:
                    raise Exception("Multiple translations for {0!r}.".format(old))

                self.translations[old] = s        
                old = None
        
        f.close()
        
        if old is not None:
            raise Exception("String {0!r} does not have a translation.".format(old))
         
    def update_translations(self, s):
        """
        Update the translations file.
        """
        
        f = file(os.path.join(renpy.config.gamedir, self.language + ".rpt"), "ab")
        
        encoded = self.quote(s).encode("utf-8")
        
        f.write("\r\n")
        f.write("< " + encoded + "\r\n")
        f.write("> " + encoded + "\r\n")
        f.close()
        
        self.translations[s] = s
                
    def translate(self, s):
        """
        Looks up `s` in the translation database. Returns the translation, or
        `s` if no translation is found.
        """
        
        old = s.rstrip()
        
        if not old:
            return s
        
        new = self.translations.get(old, None)
        
        if new is not None:
            return new
        
        if update_translations:        
            self.update_translations(old)
        
        return s
  
        
        