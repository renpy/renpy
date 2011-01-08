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

# This module handles the logging of messages to a file.

import sys
import os
import time as _time
import codecs
import traceback
import platform

import renpy

# The file events are logged to.
log_file = None

def init(renpy_base):
    global log_file
    global last_startup_time


    log_filename = os.environ.get("RENPY_LOG_FILE", os.path.join(renpy_base, "log.txt"))

    if log_filename == "-":
        log_file = sys.stdout
    else:
        try:
            log_file = codecs.open(log_filename, "w", "utf-8")
        except:
            log_file = None

    info("%s", renpy.version)

    try:
        # platform.platform fails on android.
        info("running on %s", platform.platform())
    except:
        pass
    
def info_exception():
    if log_file is None:
        return None

    traceback.print_exc(None, log_file)
            
def info(msg, *args):
    if log_file is None:
        return

    log_file.write(msg % args + "\n")
    
def debug_exception():
    if renpy.config.developer:
        info_exception()

def debug(msg, *args):
    if renpy.config.developer:
        info(msg, *args)

# The time at which time was last called.
last_time = 0

def time(event):
    global last_time

    now = _time.time()
    length = now - last_time
    last_time = now
    
    info("%s took %.3f seconds.", event, length)
    
