# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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

import sys
import os
import renpy.audio
import subprocess
import pygame

class TTSRoot(Exception):
    """
    An exception that can be used to cause the TTS system to read the text
    of the root displayable, rather than text of the currently focused
    displayable.
    """

# The root of the scene.
root = None

# The text of the last displayable.
last = ""

# The speech synthesis process.
process = None

def periodic():
    global process

    if process is not None:
        if process.poll() is not None:
            process = None


def default_tts_function(s):
    """
    Default function which speaks messages using an os-specific method.
    """

    global process

    # Stop the existing process.
    if process is not None:
        try:
            process.terminate()
            process.wait()
        except:
            pass

    process = None

    s = s.strip()

    if not s:
        return

    if renpy.game.preferences.self_voicing == "clipboard":
        try:
            pygame.scrap.put(pygame.SCRAP_TEXT, s.encode("utf-8"))
        except:
            pass

        return

    if renpy.linux:
        process = subprocess.Popen([ "espeak", s.encode("utf-8") ])
    elif renpy.macintosh:
        process = subprocess.Popen([ "say", renpy.exports.fsencode(s) ])
    elif renpy.windows:
        say_vbs = os.path.join(os.path.dirname(sys.executable), "say.vbs")
        s = s.replace('"', "")
        process = subprocess.Popen([ "wscript", renpy.exports.fsencode(say_vbs), renpy.exports.fsencode(s) ])


def tts(s):
    """
    Speaks the queued messages using the specified function.
    """

    global queue

    try:
        renpy.config.tts_function(s)
    except:
        pass

    queue = [ ]


def speak(s, translate=True, force=False):
    """
    This is called by the system to queue the speaking of message `s`.
    """

    if not force and not renpy.game.preferences.self_voicing:
        return

    if translate:
        s = renpy.translation.translate_string(s)

    tts(s)

def set_root(d):
    global root
    root = d

# The old value of the self_voicing preference.
old_self_voicing = False

def displayable(d):
    """
    Causes the TTS system to read the text of the displayable `d`.
    """

    global old_self_voicing
    global last

    self_voicing = renpy.game.preferences.self_voicing

    if not self_voicing:
        if old_self_voicing:
            old_self_voicing = self_voicing
            speak("Self-voicing disabled.", force=True)

        last = None

        return

    prefix = ""

    if not old_self_voicing:
        old_self_voicing = self_voicing

        if self_voicing == "clipboard":
            prefix = renpy.translation.translate_string("Clipboard voicing enabled. ")
        else:
            prefix = renpy.translation.translate_string("Self-voicing enabled. ")

    for i in renpy.config.tts_voice_channels:
        if not prefix and renpy.audio.music.get_playing(i):
            return

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

    if s != last:
        last = s
        tts(prefix + s)
