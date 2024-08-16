# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import sys
import os
import re
import subprocess

import pygame_sdl2 as pygame
import renpy


class TTSDone(str):
    """
    A subclass of string that is returned from a tts function to stop
    further TTS processing.
    """


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

# The text of the last displayable, before config.tts_dictionary was applied.
last_raw = ""

# The speech synthesis process.
process = None


def periodic():
    global process

    if process is not None:
        if process.poll() is not None:

            if process.returncode:
                if renpy.config.tts_voice is not None:
                    renpy.config.tts_voice = None
                    renpy.config.tts_function(last_spoken)

            process = None


def is_active():

    return process is not None


class AndroidTTS(object):

    def __init__(self):

        from jnius import autoclass
        PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
        self.TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
        self.tts = self.TextToSpeech(PythonSDLActivity.mActivity, None)


    def speak(self, s):
        self.tts.speak(s, self.TextToSpeech.QUEUE_FLUSH, None)


class AppleTTS(object):

    def __init__(self):

        from pyobjus import autoclass, objc_str # type: ignore
        from pyobjus.dylib_manager import load_framework # type: ignore

        self.objc_str = objc_str

        load_framework('/System/Library/Frameworks/AVFoundation.framework')
        self.AVSpeechUtterance = autoclass('AVSpeechUtterance')
        AVSpeechSynthesizer = autoclass('AVSpeechSynthesizer')

        self.synth = AVSpeechSynthesizer.alloc().init()


    def speak(self, s):
        utterance = self.AVSpeechUtterance.alloc().initWithString_(self.objc_str(s))
        self.synth.speakUtterance_(utterance)



platform_tts = None # The platform-specific TTS object, used on Android or iOS.


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
        except Exception:
            pass

    process = None

    s = s.strip()

    if not s:
        return

    if renpy.game.preferences.self_voicing == "clipboard":
        try:
            pygame.scrap.put(pygame.scrap.SCRAP_TEXT, s.encode("utf-8"))
        except Exception:
            pass

        return

    if renpy.game.preferences.self_voicing == "debug":
        renpy.exports.restart_interaction()
        return

    fsencode = renpy.exports.fsencode

    amplitude = renpy.game.preferences.get_mixer("voice")
    amplitude_100 = int(amplitude * 100)

    if "RENPY_TTS_COMMAND" in os.environ:

        process = subprocess.Popen([ os.environ["RENPY_TTS_COMMAND"], fsencode(s) ])

    elif renpy.linux:

        cmd = [ "espeak", "-a", fsencode(str(amplitude_100)) ]

        if renpy.config.tts_voice is not None:
            cmd.extend([ "-v", fsencode(renpy.config.tts_voice) ])

        cmd.append(fsencode(s))

        process = subprocess.Popen(cmd)

    elif renpy.macintosh:

        s = "[[volm {:.02f}]]".format(amplitude) + s

        if renpy.config.tts_voice is None:
            process = subprocess.Popen([ "say", fsencode(s) ])
        else:
            process = subprocess.Popen([ "say", "-v", fsencode(renpy.config.tts_voice), fsencode(s) ])

    elif renpy.windows:

        if renpy.config.tts_voice is None:
            voice = "default voice" # something that is unlikely to match.
        else:
            voice = renpy.config.tts_voice

        say_vbs = os.path.join(os.path.dirname(sys.executable), "say.vbs")
        s = s.replace('"', "")
        process = subprocess.Popen([ "wscript", fsencode(say_vbs), fsencode(s), fsencode(voice), fsencode(str(amplitude_100)) ])

    elif renpy.emscripten and renpy.config.webaudio:

        from renpy.audio.webaudio import call
        call("tts", s, amplitude)

    elif platform_tts is not None:
        platform_tts.speak(s)

# A List of (regex, string) pairs.
tts_substitutions = [ ]




def init():
    """
    Initializes the TTS system.
    """

    global platform_tts

    for pattern, replacement in renpy.config.tts_substitutions:

        if isinstance(pattern, basestring):
            pattern = r'\b' + re.escape(pattern) + r'\b'
            pattern = re.compile(pattern, re.IGNORECASE)
            replacement = replacement.replace("\\", "\\\\")

        tts_substitutions.append((pattern, replacement))

    try:

        if renpy.android:
            platform_tts = AndroidTTS()

        if renpy.ios:
            platform_tts = AppleTTS()

    except Exception as e:
        renpy.display.log.write("Failed to initialize TTS.")
        renpy.display.log.exception()


def apply_substitutions(s):
    """
    Applies the TTS dictionary to `s`, returning the result.
    """

    def replace(m):
        old = m.group(0)
        if old.istitle():
            template = replacement.title()
        elif old.isupper():
            template = replacement.upper()
        elif old.islower():
            template = replacement.lower()
        else:
            template = replacement

        return m.expand(template)

    for pattern, replacement in tts_substitutions:
        s = pattern.sub(replace, s)

    return s


# A queue of tts utterances.
tts_queue = [ ]


# The last text spoken.
last_spoken = ""

def tick():
    if not tts_queue:
        return

    s = " ".join(tts_queue)
    tts_queue[:] = [ ]

    global last_spoken
    last_spoken = s


    try:
        renpy.config.tts_function(s)
    except Exception:
        pass


def tts(s):
    """
    Causes `s` to be spoken.
    """

    if not renpy.game.preferences.self_voicing:
        return

    tts_queue.append(s)


def speak(s, translate=True, force=False):
    """
    :doc: self_voicing

    This queues `s` to be spoken. If `translate` is true, then the string
    will be translated before it is spoken. If `force` is true, then the
    string will be spoken even if self-voicing is disabled.

    This is intended for accessibility purposes, and should not be used
    for gameplay purposes.
    """

    if not force and not renpy.game.preferences.self_voicing:
        return

    if translate:
        s = renpy.translation.translate_string(s)

    s = apply_substitutions(s)
    tts_queue.append(s)


def speak_extra_alt():
    """
    :undocumented:

    If the current displayable has the extra_alt property, and self-voicing
    is enabled, then this will speak the extra_alt property.
    """

    d = renpy.display.focus.get_focused()

    if d is None:
        return

    s = d.style.extra_alt
    if s is None:
        return

    speak(s)


def set_root(d):
    global root
    root = d


# The old value of the self_voicing preference.
old_self_voicing = False

# The text used to show a notification.
notify_text = None

# The last group_alt value used.
last_group_alt = None


def displayable(d):
    """
    Causes the TTS system to read the text of the displayable `d`.
    """

    global old_self_voicing
    global last
    global last_raw
    global notify_text
    global last_group_alt

    self_voicing = renpy.game.preferences.self_voicing

    if not self_voicing:
        if old_self_voicing:
            old_self_voicing = self_voicing
            speak(renpy.translation.translate_string("Self-voicing disabled."), force=True)

        last = ""

        return

    prefix = ""

    if not old_self_voicing:
        old_self_voicing = self_voicing

        if self_voicing == "clipboard":
            prefix = renpy.translation.translate_string("Clipboard voicing enabled. ")
        else:
            prefix = renpy.translation.translate_string("Self-voicing enabled. ")

        last_raw = None

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

    group_alt = d.style.group_alt
    if group_alt and group_alt != last_group_alt:
        group = renpy.translation.translate_string(group_alt)
        s = group + ": " + s

    last_group_alt = group_alt

    if notify_text and not s.startswith(notify_text):
        s = notify_text + ": " + s
        notify_text = None

    if s != last_raw:
        last_raw = s
        s = apply_substitutions(s)
        last = s
        tts(prefix + s)
