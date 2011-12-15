# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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

import os
import renpy


class Editor(object):
    """
    This class is intended to be subclassed by editor subclasses. It provides a
    number of editor related operations, which are called by Ren'Py (including
    the Ren'Py Launcher). 
    
    Editor operations are grouped into transactions. An editor transaction
    starts with a call to the begin() method. Ren'Py will then call some number
    of command methods, each causing an operation to occur in the editor. Ren'Py
    will call end() at the end of the transaction. 
    
    Although not required, it's reasonable than an implementation of this class
    will batch the files together and send them to the editor at once. It's also
    reasonable that an implementation will send the operations one at a time (and 
    do little-to-nothing in begin() and end().
    
    Each operation takes a path to operate on. If the editor has a buffer
    corresponding to that path, that buffer is used. Otherwise, the editor 
    is implicitly opened.
    """

    def open(self, path): #@ReservedAssignment
        """
        Ensures `path` is open in the editor.
        """
        
    def reopen(self, path):
        """
        Causes the editor to reopen the file at `path`.
        """
        
    def line(self, path, number):
        """
        Moves the cursor for `path` to `line`. Lines in a file are numbered
        starting with 1.
        """
        
    def focus(self, path):
        """
        Focuses `path`, which means that the buffer containing it should be
        presented to the user. Ideally, the window containing it will also 
        pop to the top of the OS's window stack.
        """
        
    def begin(self):
        """
        Begins an editor transaction.
        """
        
    def end(self):
        """
        Ends an editor transaction.
        """
        
# The editor that Ren'Py is using. It should be a subclass of the Editor
# class. 
editor = None

def init():
    """
    Creates the editor object, based on the contents of the RENPY_EDITOR 
    file.
    """
    
    global editor
    editor = None
    
    path = os.environ.get("RENPY_EDITOR_PY", None)
    if path is None:
        return
    
    try:
        f = file(path, "rU")
        code = f.read()
        f.close()
    except:
        raise Exception("{} could not be opened.".format(path))
    
    scope = { }    
    exec code in scope
            
    if "editor" in scope:
        editor = scope["editor"]
        return 
    
    raise Exception("{} does not create an editor variable.".format(path))

def launch_editor(filenames, line=1, transient=False):
    """
    Causes the editor to be launched.
    """
    
    if editor is None:
        return False
    
    filenames = [ renpy.parser.unelide_filename(i) for i in filenames ]
    
    try:
    
        editor.begin()
        
        for i in filenames:
            
            if transient:
                editor.open(i)
            else:
                editor.reopen(i)
            
        editor.line(filenames[0], line)
        editor.focus(filenames[0])
        
        editor.end()
        
        return True
    
    except:
        
        if renpy.config.debug:
            raise
        
        return False