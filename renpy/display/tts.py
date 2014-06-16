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

import renpy

try:
    import pyttsx
except:
    pyttsx = None

class TTSRoot(Exception):
    """
    An exception that can be used to cause the TTS system to read the text
    of the root displayable, rather than text of the currently focused
    displayable.
    """

# The root of the scene.
root = None

# The last thing we said.
last = ""

# The engine.
engine = None

def set_root(d):
    global root
    root = d

def speak(s, translate=True):
    """
    Causes the TTS system to speak `s`, if the TTS system is enabled.
    """

    if not renpy.game.preferences.self_voicing:
        return

    if pyttsx is None:
        return

    global engine

    if engine is None:
        engine = pyttsx.init()
        engine.startLoop(False)

    if translate:
        s = renpy.translation.translate_string(s)

    engine.stop()
    engine.say(s)

def periodic():

    if engine is not None:
        engine.iterate()

def displayable(d):
    """
    Causes the TTS system to read the text of the displayable `d`.
    """

    if not renpy.game.preferences.self_voicing:
        return

    global last

    if d is None:
        d = root

    while True:
        try:
            s = d._tts_all()
            break
        except TTSRoot:
            if d is root:
                return
            else:
                d = root

    global last

    if s == last:
        return

    speak(s, False)

