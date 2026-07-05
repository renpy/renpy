# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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
import json
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode  # *


import sys
import os
import re
import subprocess

import renpy
import renpy.pygame as pygame


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
                if get_voice(last_spoken)[0] is not None:
                    renpy.game.preferences.tts_voice = None
                    renpy.config.tts_function(last_spoken)

            process = None


def is_active():
    if platform_tts is not None:
        return platform_tts.is_speaking()

    return process is not None


class LinuxTTS(object):
    """
    TTS backend for Linux using espeak via subprocess.
    """

    def __init__(self):
        self.process = None

    def is_speaking(self):
        return self.process is not None

    def speak(self, s):
        global process

        voice, s = get_voice(s)

        # Stop any existing speech.
        if self.process is not None:
            try:
                self.process.terminate()
                self.process.wait()
            except Exception:
                pass

        self.process = None
        process = None

        s = s.strip()

        if not s:
            return

        fsencode = renpy.exports.fsencode
        amplitude = renpy.game.preferences.get_mixer("voice")
        amplitude_100 = int(amplitude * 100)

        speed = renpy.game.preferences.tts_speed
        speed_wpm = int(175 * speed)

        cmd = ["espeak", "-a", fsencode(str(amplitude_100)), "-s", fsencode(str(speed_wpm))]

        if voice is not None:
            # Voice format is "lang: name", extract the language for espeak.
            if ": " in voice:
                voice = voice.split(": ", 1)[0]
            cmd.extend(["-v", fsencode(voice)])

        cmd.append(fsencode(s))

        self.process = subprocess.Popen(cmd)
        process = self.process

    def stop(self):
        if self.process is not None:
            try:
                self.process.terminate()
                self.process.wait()
            except Exception:
                pass

            self.process = None

    def get_tts_voices(self):
        """
        Returns a list of available self-voicing voices via espeak.
        """

        try:
            output = subprocess.check_output(["espeak", "--voices"], universal_newlines=True)
        except Exception:
            return []

        voices = []

        for line in output.splitlines():
            line = line.strip()

            if not line or line.startswith("Pty") or line.startswith("---"):
                continue

            parts = line.split(None, 4)

            if len(parts) < 5:
                continue

            language = parts[1].strip()
            name = parts[3].strip()

            voices.append("{}: {}".format(language, name))

        return voices


class AndroidTTS(object):
    def __init__(self):
        from jnius import autoclass

        PythonSDLActivity = autoclass("org.renpy.android.PythonSDLActivity")
        self.TextToSpeech = autoclass("android.speech.tts.TextToSpeech")
        self.tts = self.TextToSpeech(PythonSDLActivity.mActivity, None)
        self._voices = None

    @property
    def voices(self):
        if self._voices is not None:
            return self._voices

        self._voices = {}

        for voice in self.tts.getVoices():
            locale = voice.getLocale()
            language = locale.toString().replace("_", "-")
            name = voice.getName()
            key = "{}: {}".format(language, name)
            self._voices[key] = voice

        return self._voices

    def is_speaking(self):
        return self.tts.isSpeaking()

    def speak(self, s):
        voice, s = get_voice(s)

        if voice is not None:
            if voice in self.voices:
                self.tts.setVoice(self.voices[voice])
            else:
                # Voice format is "lang-CC: name", try extracting just the name.
                if ": " in voice:
                    voice = voice.split(": ", 1)[1]
                if voice in self.voices:
                    self.tts.setVoice(self.voices[voice])
                else:
                    self.tts.setVoice(self.tts.getDefaultVoice())
        else:
            self.tts.setVoice(self.tts.getDefaultVoice())

        speed = renpy.game.preferences.tts_speed
        self.tts.setSpeechRate(speed)

        self.tts.speak(s, self.TextToSpeech.QUEUE_FLUSH, None)

    def stop(self):
        self.tts.stop()

    def get_tts_voices(self):
        """
        Returns a list of available self-voicing voices on Android.
        """

        return list(sorted(k for k in self.voices.keys() if ": " in k))


class AppleTTS(object):
    def __init__(self):
        from pyobjus import autoclass, objc_str  # type: ignore
        from pyobjus.dylib_manager import load_framework  # type: ignore

        self.objc_str = objc_str

        load_framework("/System/Library/Frameworks/AVFoundation.framework")
        self.AVSpeechUtterance = autoclass("AVSpeechUtterance")
        self.AVSpeechSynthesisVoice = autoclass("AVSpeechSynthesisVoice")
        AVSpeechSynthesizer = autoclass("AVSpeechSynthesizer")

        self.synth = AVSpeechSynthesizer.alloc().init()

        self.voices: dict[str, str] = { }

        speech_voices = self.AVSpeechSynthesisVoice.speechVoices()
        count = speech_voices.count

        for i in range(count):
            voice = speech_voices.objectAtIndex_(i)

            name = voice.name.UTF8String()
            if isinstance(name, bytes):
                name = name.decode("utf-8")

            language = voice.language.UTF8String()
            if isinstance(language, bytes):
                language = language.decode("utf-8")

            identifier = voice.identifier.UTF8String()
            if isinstance(identifier, bytes):
                identifier = identifier.decode("utf-8")

            key = "{}: {}".format(language, name)
            self.voices[key] = identifier

    def is_speaking(self):
        return self.synth.isSpeaking()

    def speak(self, s):
        voice, s = get_voice(s)

        utterance = self.AVSpeechUtterance.alloc().initWithString_(self.objc_str(s))

        amplitude = renpy.game.preferences.get_mixer("voice")
        utterance.setVolume_(float(amplitude))

        speed = renpy.game.preferences.tts_speed
        utterance.setRate_(min(1.0, 0.5 + (speed - 1.0) / 4.0))

        if voice is not None:

            identifier = self.voices.get(voice, voice)
            av_voice = self.AVSpeechSynthesisVoice.voiceWithIdentifier_(identifier)

            if av_voice is None:
                # Voice format is "lang: name", extract the language.
                if ": " in voice:
                    voice = voice.split(": ", 1)[0]
                av_voice = self.AVSpeechSynthesisVoice.voiceWithLanguage_(voice)

            if av_voice is not None:
                utterance.setVoice_(av_voice)

        self.synth.speakUtterance_(utterance)

    def stop(self):
        self.synth.stopSpeakingAtBoundary_(0)  # AVSpeechBoundaryImmediate

    def get_tts_voices(self):
        """
        Returns a list of available self-voicing voices on iOS/macOS via AVFoundation.
        """

        return list(self.voices.keys())


class WindowsTTS(object):
    """
    TTS backend for Windows using SAPI via PowerShell.
    """

    def __init__(self):
        self.process = None

    def is_speaking(self):
        return self.process is not None

    def speak(self, s):
        global process

        voice, s = get_voice(s)

        # Stop any existing speech.
        if self.process is not None:
            try:
                self.process.terminate()
                self.process.wait()
            except Exception:
                pass

        self.process = None
        process = None

        s = s.strip()

        if not s:
            return

        amplitude = renpy.game.preferences.get_mixer("voice")
        amplitude_100 = int(amplitude * 100)

        speed = renpy.game.preferences.tts_speed
        rate = max(-10, min(10, int(5 * (speed - 1))))

        if voice is not None:
            # Voice format is "lang: name", extract the name for SAPI.
            if ": " in voice:
                voice = voice.split(": ", 1)[1]
            voice = voice.replace("'", "''")
            script = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Volume = {volume}
$synth.Rate = {rate}
try {{ $synth.SelectVoice('{voice}') }} catch {{ }}
$synth.Speak('{text}')
""".format(volume=amplitude_100, rate=rate, voice=voice, text=s)
        else:
            script = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Volume = {volume}
$synth.Rate = {rate}
$synth.Speak('{text}')
""".format(volume=amplitude_100, rate=rate, text=s)

        self.process = subprocess.Popen([
            "powershell", "-NoProfile", "-Command", script,
        ], creationflags=subprocess.CREATE_NO_WINDOW)
        process = self.process

    def stop(self):
        if self.process is not None:
            try:
                self.process.terminate()
                self.process.wait()
            except Exception:
                pass

            self.process = None

    def get_tts_voices(self):
        """
        Returns a list of SAPI self-voicing voices available on Windows.
        """

        script = """
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
foreach ($v in $synth.GetInstalledVoices()) {
    Write-Output ($v.VoiceInfo.Culture.Name + "|" + $v.VoiceInfo.Name)
}
"""

        try:
            output = subprocess.check_output(
                ["powershell", "-NoProfile",  "-Command", script],
                universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
        except Exception:
            return []

        voices = []
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            if "|" in line:
                language, name = line.split("|", 1)
                voices.append("{}: {}".format(language, name))
            else:
                voices.append(line)

        return voices


class WebTTS(object):
    """
    TTS backend for Web using the Web Audio API.
    """

    def is_speaking(self):
        return False

    def speak(self, s):
        voice, s = get_voice(s)

        from renpy.audio.webaudio import call
        amplitude = renpy.game.preferences.get_mixer("voice")
        speed = renpy.game.preferences.tts_speed

        # Chrome has problems with speed > 2.0, so limit it.
        speed = min(speed, 1.99)

        # This calls renpyAudio.tts, which is defined in renpy/common/_audio.js.
        call("tts", s, amplitude, speed, voice)

    def stop(self):
        from renpy.audio.webaudio import call
        amplitude = renpy.game.preferences.get_mixer("voice")

        call("tts", "", 1.0, 1.0, None)

    def get_tts_voices(self):
        from renpy.audio.webaudio import call_str

        voices = call_str("get_tts_voices")
        return json.loads(voices) if voices else []



platform_tts = None  # The platform-specific TTS object.


def default_tts_function(s):
    """
    Default function which speaks messages using the platform-specific TTS object.
    """

    if platform_tts is not None:
        platform_tts.stop()

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

    if "RENPY_TTS_COMMAND" in os.environ:
        global process
        fsencode = renpy.exports.fsencode
        process = subprocess.Popen([os.environ["RENPY_TTS_COMMAND"], fsencode(s)])
        return

    if platform_tts is not None:
        platform_tts.speak(s)


def stop_tts():
    """
    :undocumented:

    Stops any currently playing TTS.
    """

    global process
    if process is not None:
        try:
            process.terminate()
            process.wait()
        except Exception:
            pass

        process = None

    if platform_tts is not None:
        platform_tts.stop()
        return


# A List of (regex, string) pairs.
tts_substitutions = []


def init():
    """
    Initializes the TTS system.
    """

    global platform_tts

    for pattern, replacement in renpy.config.tts_substitutions:
        if isinstance(pattern, str):
            pattern = r"\b" + re.escape(pattern) + r"\b"
            pattern = re.compile(pattern, re.IGNORECASE)
            replacement = replacement.replace("\\", "\\\\")

        tts_substitutions.append((pattern, replacement))

    try:
        if renpy.android:
            platform_tts = AndroidTTS()

        elif renpy.ios:
            platform_tts = AppleTTS()

        elif renpy.macintosh:
            platform_tts = AppleTTS()

        elif renpy.linux:
            platform_tts = LinuxTTS()

        elif renpy.windows:
            platform_tts = WindowsTTS()

        elif renpy.emscripten and renpy.config.webaudio:
            platform_tts = WebTTS()

    except Exception as e:
        renpy.display.log.write("Failed to initialize TTS.")
        renpy.display.log.exception()

# Cache for get_tts_voices.
_tts_voices_cache = None


def get_tts_voices():
    """
    :doc: self_voicing

    Returns a list of available text-to-speech voice names. Returns an
    empty list if no voices are available, or if the platform does not support voice
    enumeration.
    """

    global _tts_voices_cache

    if _tts_voices_cache is not None:
        return _tts_voices_cache

    try:

        if platform_tts is not None:
            voices = platform_tts.get_tts_voices()

        else:
            voices = []

    except Exception:
        voices = []

    voices.sort(key=lambda v: v.lower())

    _tts_voices_cache = voices
    return voices


VOICE_RE = re.compile(r'{voice=([^}]+)}')

def get_voice(text:str = ""):
    """
    :undocumented:

    Returns the self-voicing voice to use. If :var:`preferences.tts_voice` is set,
    it is used. If the selected voice is not in the list of available voices, returns None.
    """

    if m := VOICE_RE.search(text):
        voice = m.group(1)
        text = VOICE_RE.sub("", text)

        if voice in get_tts_voices():
            return voice, text

    voice = renpy.game.preferences.tts_voice

    if voice is not None and voice in get_tts_voices():
            return voice, text

    return None, text


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
tts_queue = []


# The last text spoken.
last_spoken = ""


def tick():
    if not tts_queue:
        return

    s = " ".join(tts_queue)
    tts_queue[:] = []

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

    if not renpy.config.tts_queue:
        tts_queue[:] = []

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

    if not renpy.config.tts_queue:
        tts_queue[:] = []

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
            s = d._tts_all(raw=False)
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
