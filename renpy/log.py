# Copyright 2004-2014 Tom Rothamel <pytom@bishoujo.us>
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
import tempfile

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

        # File-like attributes.
        self.softspace = 0
        self.newlines = None

        # Should we emulate file's write method? We do so if this is True.
        self.raw_write = False

    def open(self): #@ReservedAssignment

        if self.file:
            return True

        if self.developer and not renpy.config.developer:
            return False

        if not renpy.config.log_enable:
            return False

        try:
            base = os.environ.get("RENPY_LOG_BASE", renpy.config.logdir)
            fn = os.path.join(base, self.name + ".txt")

            altfn = os.path.join(tempfile.gettempdir(), "renpy-" + self.name + ".txt")


            if renpy.android:
                print "Logging to", fn

            if self.append:
                mode = "a"
            else:
                mode = "w"

            try:
                self.file = codecs.open(fn, mode, "utf-8")
            except:
                self.file = codecs.open(altfn, mode, "utf-8")

            if self.append:
                self.write('')
                self.write('=' * 78)
                self.write('')

            self.write("%s", time.ctime())
            self.write("%s", platform.platform())
            self.write("%s", renpy.version)
            self.write("%s %s", renpy.config.name, renpy.config.version)
            self.write("")

            return True

        except:
            return False

    def write(self, s, *args):
        """
        Formats `s` with args, and writes it to the logfile.
        """

        if self.open():

            if not self.raw_write:
                s = s % args
                s += "\n"

            if not isinstance(s, unicode):
                s = s.decode("latin-1")

            s = s.replace("\n", "\r\n")

            self.file.write(s)
            self.file.flush()

    def exception(self):
        """
        Writes the exception to the logfile.
        """

        self.raw_write = True
        traceback.print_exc(None, self)
        self.raw_write = False

# A map from the log name to a log object.
log_cache = { }

def open(name, append=False, developer=False): #@ReservedAssignment
    rv = log_cache.get(name, None)

    if rv is None:
        rv = LogFile(name, append=append, developer=developer)
        log_cache[name] = rv

    return rv
