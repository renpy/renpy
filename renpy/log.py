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

# This module handles the logging of messages to a file.

import os.path
import codecs
import traceback
import platform
import time

import renpy

# The file events are logged to.
log_file = None

class LogFile(object):
    """
    This manages one of our logfiles.
    """
    
    def __init__(self, name, append=False, developer=False):
        """
        `name`
            The name of the logfile, without the .txt extension.
        `append`
            If true, we will append to the logfile. If false, we will truncate
            it to an empty file the first time we write to it.
        `developer`
            If true, nothing happens if config.developer is not set to True.
        """
        
        self.name = name
        self.append = append
        self.developer = developer
        self.file = None
        
    def open(self):

        if self.file:
            return True

        if self.developer and not renpy.config.developer:
            return False
        
        if not renpy.config.log_enable:
            return False

        try:
            base = os.environ.get("RENPY_LOG_BASE", renpy.config.renpy_base)
            fn = os.path.join(base, self.name + ".txt")
        
            if self.append:
                self.file = codecs.open(fn, "a", "utf-8")
                print >>self.file
                print >>self.file, "=" * 78
                print >>self.file
            else:
                self.file = codecs.open(fn, "w", "utf-8")

            print >>self.file, time.ctime()                
            print >>self.file, platform.platform()
            print >>self.file, renpy.version #@UndefinedVariable
            print >>self.file, renpy.config.name + " " + renpy.config.version
            print >>self.file
            
            return True

        except:
            return False

    def write(self, msg, *args):
        """
        Formats msg with args, and writes it to the logfile.
        """

        if self.open():
            s = msg % args
            self.file.write(s + "\n")
            
    def exception(self):
        """
        Writes the exception to the logfile.
        """

        if self.open():
            traceback.print_exc(None, self.file)

# A map from the log name to a log object.
log_cache = { }

def open(name, append=False, developer=False):
    rv = log_cache.get(name, None)
    
    if rv is None:
        rv = LogFile(name, append=append, developer=developer)
        log_cache[name] = rv
        
    return rv

    
    
