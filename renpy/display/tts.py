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
import types
import subprocess

import renpy

try:
    import renpy.pygame as pygame
except Exception:
    try:
        import pygame  # type: ignore
    except Exception:
        pygame = None  # type: ignore

prism = None
try:
    import prism
except Exception:
    prism = None

if prism is None:
    try:
        import ctypes

        class _PrismConfig(ctypes.Structure):
            _fields_ = [
                ("registry", ctypes.c_void_p),
                ("availability_callback", ctypes.c_void_p),
                ("availability_userdata", ctypes.c_void_p),
                ("availability_poll_interval_ms", ctypes.c_uint32),
                ("availability_debounce_samples", ctypes.c_uint32),
                ("availability_backoff_max_ms", ctypes.c_uint32),
                ("availability_auto_power_manage", ctypes.c_bool),
            ]

        class _CtypesBackendFeatures(object):
            supports_set_volume = True
            supports_set_rate = True

        class _CtypesBackend(object):
            def __init__(self, dll, ptr):
                self.dll = dll
                self.ptr = ptr
                self.name = self.dll.prism_backend_name(self.ptr).decode("utf-8")
                self.features = _CtypesBackendFeatures()

            @property
            def speaking(self):
                try:
                    return bool(self.dll.prism_backend_is_speaking(self.ptr))
                except Exception:
                    return False

            @property
            def volume(self):
                v = ctypes.c_float()
                self.dll.prism_backend_get_volume(self.ptr, ctypes.byref(v))
                return v.value

            @volume.setter
            def volume(self, val):
                self.dll.prism_backend_set_volume(self.ptr, ctypes.c_float(val))

            @property
            def rate(self):
                r = ctypes.c_float()
                self.dll.prism_backend_get_rate(self.ptr, ctypes.byref(r))
                return r.value

            @rate.setter
            def rate(self, val):
                self.dll.prism_backend_set_rate(self.ptr, ctypes.c_float(val))

            def output(self, s, interrupt=True):
                if isinstance(s, str):
                    s = s.encode("utf-8")
                self.dll.prism_backend_output(self.ptr, s, bool(interrupt))

            def speak(self, s, interrupt=True):
                self.output(s, interrupt=interrupt)

            def stop(self):
                self.dll.prism_backend_stop(self.ptr)

            @property
            def voices_count(self):
                count = ctypes.c_size_t()
                if self.dll.prism_backend_count_voices(self.ptr, ctypes.byref(count)) == 0:
                    return count.value
                return 0

            def get_voice_name(self, idx):
                ptr = ctypes.c_char_p()
                if self.dll.prism_backend_get_voice_name(self.ptr, ctypes.c_size_t(idx), ctypes.byref(ptr)) == 0:
                    return ptr.value.decode("utf-8") if ptr.value else ""
                return ""

            def get_voice_language(self, idx):
                ptr = ctypes.c_char_p()
                if self.dll.prism_backend_get_voice_language(self.ptr, ctypes.c_size_t(idx), ctypes.byref(ptr)) == 0:
                    return ptr.value.decode("utf-8") if ptr.value else ""
                return ""

            @property
            def voice(self):
                idx = ctypes.c_size_t()
                if self.dll.prism_backend_get_voice(self.ptr, ctypes.byref(idx)) == 0:
                    return idx.value
                return 0

            @voice.setter
            def voice(self, idx):
                self.dll.prism_backend_set_voice(self.ptr, ctypes.c_size_t(idx))

        class _CtypesContext(object):
            def __init__(self, mod, ptr):
                self.mod = mod
                self.dll = mod.dll
                self.ptr = ptr

            @property
            def backends_count(self):
                return self.dll.prism_registry_count(self.ptr)

            def id_of(self, idx):
                return self.dll.prism_registry_id_at(self.ptr, ctypes.c_size_t(idx))

            def name_of(self, bid):
                ptr = self.dll.prism_registry_name(self.ptr, ctypes.c_uint64(bid))
                return ptr.decode("utf-8") if ptr else ""

            def acquire(self, bid):
                b = self.dll.prism_registry_acquire(self.ptr, ctypes.c_uint64(bid))
                if b:
                    self.dll.prism_backend_initialize(b)
                    return _CtypesBackend(self.dll, b)
                return None

            def acquire_best(self):
                b = self.dll.prism_registry_acquire_best(self.ptr)
                if b:
                    self.dll.prism_backend_initialize(b)
                    return _CtypesBackend(self.dll, b)
                return None

        class _CtypesPrismModule(types.ModuleType):
            def __init__(self, dll):
                super(_CtypesPrismModule, self).__init__("prism")
                self.dll = dll
                self.dll.prism_config_init.restype = _PrismConfig
                self.dll.prism_init.argtypes = [ctypes.POINTER(_PrismConfig)]
                self.dll.prism_init.restype = ctypes.c_void_p
                self.dll.prism_registry_count.argtypes = [ctypes.c_void_p]
                self.dll.prism_registry_count.restype = ctypes.c_size_t
                self.dll.prism_registry_id_at.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
                self.dll.prism_registry_id_at.restype = ctypes.c_uint64
                self.dll.prism_registry_name.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
                self.dll.prism_registry_name.restype = ctypes.c_char_p
                self.dll.prism_registry_acquire.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
                self.dll.prism_registry_acquire.restype = ctypes.c_void_p
                self.dll.prism_registry_acquire_best.argtypes = [ctypes.c_void_p]
                self.dll.prism_registry_acquire_best.restype = ctypes.c_void_p
                self.dll.prism_backend_initialize.argtypes = [ctypes.c_void_p]
                self.dll.prism_backend_name.argtypes = [ctypes.c_void_p]
                self.dll.prism_backend_name.restype = ctypes.c_char_p
                self.dll.prism_backend_is_speaking.argtypes = [ctypes.c_void_p]
                self.dll.prism_backend_is_speaking.restype = ctypes.c_bool
                self.dll.prism_backend_output.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_bool]
                self.dll.prism_backend_stop.argtypes = [ctypes.c_void_p]
                self.dll.prism_backend_get_volume.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float)]
                self.dll.prism_backend_set_volume.argtypes = [ctypes.c_void_p, ctypes.c_float]
                self.dll.prism_backend_get_rate.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_float)]
                self.dll.prism_backend_set_rate.argtypes = [ctypes.c_void_p, ctypes.c_float]
                self.dll.prism_backend_count_voices.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]
                self.dll.prism_backend_get_voice_name.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_size_t,
                    ctypes.POINTER(ctypes.c_char_p),
                ]
                self.dll.prism_backend_get_voice_language.argtypes = [
                    ctypes.c_void_p,
                    ctypes.c_size_t,
                    ctypes.POINTER(ctypes.c_char_p),
                ]
                self.dll.prism_backend_get_voice.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)]
                self.dll.prism_backend_set_voice.argtypes = [ctypes.c_void_p, ctypes.c_size_t]

            def Context(self):
                cfg = self.dll.prism_config_init()
                ctx_ptr = self.dll.prism_init(ctypes.byref(cfg))
                return _CtypesContext(self, ctx_ptr)

        def _find_and_load_prism():
            candidates = []
            base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            if sys.platform.startswith("win"):
                dll_name = "prism.dll"
                candidates.append(os.path.join(base, "lib", "py3-windows-x86_64", dll_name))
                candidates.append(os.path.join(base, "lib", "python3.12", "prism", "_native", dll_name))
                candidates.append(os.path.join(base, dll_name))
            elif sys.platform.startswith("darwin"):
                dll_name = "libprism.dylib"
                candidates.append(os.path.join(base, "lib", "py3-mac-universal", dll_name))
                candidates.append(os.path.join(base, dll_name))
            else:
                dll_name = "libprism.so"
                candidates.append(os.path.join(base, "lib", "py3-linux-x86_64", dll_name))
                candidates.append(os.path.join(base, dll_name))

            candidates.append(dll_name)

            for c in candidates:
                if os.path.isfile(c) or c == dll_name:
                    try:
                        dll_obj = ctypes.CDLL(c)
                        if hasattr(dll_obj, "prism_init"):
                            return _CtypesPrismModule(dll_obj)
                    except Exception:
                        continue
            return None

        prism = _find_and_load_prism()
    except Exception:
        prism = None


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

        amplitude = renpy.game.preferences.get_mixer("voice")
        amplitude_100 = int(amplitude * 100)

        speed = renpy.game.preferences.tts_speed
        speed_wpm = int(175 * speed)

        cmd = ["espeak", "-a", str(amplitude_100), "-s", str(speed_wpm)]

        if voice is not None:
            # Voice format is "lang: name", extract the language for espeak.
            if ": " in voice:
                voice = voice.split(": ", 1)[0]
            cmd.extend(["-v", voice])

        cmd.append(s)

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

        self.voices: dict[str, str] = {}

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

        self.process = subprocess.Popen(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                script,
            ],
            creationflags=subprocess.CREATE_NO_WINDOW,
        )
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
                ["powershell", "-NoProfile", "-Command", script],
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


SCREEN_READER_BACKENDS = {
    "nvda",
    "jaws",
    "voiceover",
    "orca",
    "zoomtext",
    "systemaccess",
    "windoweyes",
    "pctalker",
    "zdsr",
    "boypcreader",
    "sensereader",
    "supernova",
    "hal",
    "cobra",
    "dolphin",
    "narrator",
}


class PrismTTS(object):
    """
    Unified cross-platform TTS and Screen Reader backend using Prism.
    """

    def __init__(self):
        if prism is None:
            raise RuntimeError("Prism module is not available")

        self.context = prism.Context()
        self.sr_backend = None
        self.tts_backend = None
        self._init_backends()

    def __reduce__(self):
        return (PrismTTS, ())

    def _init_backends(self):
        # 1. Screen reader backend: look for an active screen reader
        self.sr_backend = None
        for i in range(self.context.backends_count):
            bid = self.context.id_of(i)
            name = self.context.name_of(bid)
            if name.lower() in SCREEN_READER_BACKENDS:
                try:
                    self.sr_backend = self.context.acquire(bid)
                    break
                except Exception:
                    continue

        if self.sr_backend is None:
            # Fallback for screen reader mode if none is currently active:
            try:
                self.sr_backend = self.context.acquire_best()
            except Exception:
                self.sr_backend = None

        # 2. TTS backend: look for OS synthesizers, explicitly excluding screen readers
        self.tts_backend = None
        preferred_tts = ["onecore", "avspeech", "avfoundation", "speech-dispatcher", "sapi", "espeak"]
        for pref in preferred_tts:
            for i in range(self.context.backends_count):
                bid = self.context.id_of(i)
                name = self.context.name_of(bid)
                if pref in name.lower() and name.lower() not in SCREEN_READER_BACKENDS:
                    try:
                        self.tts_backend = self.context.acquire(bid)
                        break
                    except Exception:
                        continue
            if self.tts_backend is not None:
                break

        if self.tts_backend is None:
            for i in range(self.context.backends_count):
                bid = self.context.id_of(i)
                name = self.context.name_of(bid)
                if name.lower() not in SCREEN_READER_BACKENDS:
                    try:
                        self.tts_backend = self.context.acquire(bid)
                        break
                    except Exception:
                        continue

        if self.tts_backend is None:
            self.tts_backend = self.sr_backend

    def get_backend(self, mode=None):
        if mode == "screenreader":
            # Dynamic re-check: Did user start NVDA or JAWS while game was running?
            for i in range(self.context.backends_count):
                bid = self.context.id_of(i)
                name = self.context.name_of(bid)
                if name.lower() in SCREEN_READER_BACKENDS:
                    try:
                        self.sr_backend = self.context.acquire(bid)
                        return self.sr_backend
                    except Exception:
                        continue
            if self.sr_backend is None:
                self._init_backends()
            return self.sr_backend
        else:
            if self.tts_backend is None:
                self._init_backends()
            return self.tts_backend

    def is_speaking(self):
        b = self.tts_backend or self.sr_backend
        if b is not None:
            try:
                return b.speaking
            except Exception:
                return False
        return False

    def speak(self, s, mode=None, interrupt=True):
        s = s.strip()
        if not s:
            return

        b = self.get_backend(mode)
        if b is None:
            return

        voice, s = get_voice(s)

        try:
            if b.features.supports_set_volume:
                amplitude = renpy.game.preferences.get_mixer("voice")
                b.volume = float(amplitude)
        except Exception:
            pass

        try:
            if b.features.supports_set_rate:
                speed = renpy.game.preferences.tts_speed
                # Map 1.0..3.0 to 0.5..1.0 (0.5 is normal speed in Prism)
                rate = min(1.0, max(0.0, 0.5 + (speed - 1.0) * 0.25))
                b.rate = float(rate)
        except Exception:
            pass

        if voice is not None:
            try:
                for i in range(b.voices_count):
                    vname = b.get_voice_name(i)
                    vlang = b.get_voice_language(i)
                    full_name = "{}: {}".format(vlang, vname)
                    if voice in (full_name, vname):
                        b.voice = i
                        break
            except Exception:
                pass

        try:
            b.output(s, interrupt=interrupt)
        except Exception:
            try:
                b.speak(s, interrupt=interrupt)
            except Exception:
                pass

    def stop(self):
        if self.sr_backend is not None:
            try:
                self.sr_backend.stop()
            except Exception:
                pass
        if self.tts_backend is not None and self.tts_backend is not self.sr_backend:
            try:
                self.tts_backend.stop()
            except Exception:
                pass

    def get_tts_voices(self):
        b = self.tts_backend or self.get_backend("tts")
        if b is None:
            return []
        voices = []
        try:
            for i in range(b.voices_count):
                vname = b.get_voice_name(i)
                vlang = b.get_voice_language(i)
                voices.append("{}: {}".format(vlang, vname))
        except Exception:
            pass
        return voices


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
        process = subprocess.Popen([os.environ["RENPY_TTS_COMMAND"], s])
        return

    if platform_tts is not None:
        if isinstance(platform_tts, PrismTTS):
            mode = "screenreader" if renpy.game.preferences.self_voicing == "screenreader" else "tts"
            platform_tts.speak(s, mode=mode)
        else:
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

    subs = getattr(getattr(renpy, "config", None), "tts_substitutions", [])
    for pattern, replacement in subs:
        if isinstance(pattern, str):
            pattern = r"\b" + re.escape(pattern) + r"\b"
            pattern = re.compile(pattern, re.IGNORECASE)
            replacement = replacement.replace("\\", "\\\\")

        tts_substitutions.append((pattern, replacement))

    if prism is not None:
        try:
            platform_tts = PrismTTS()
        except Exception:
            renpy.display.log.write("Failed to initialize Prism TTS, falling back to platform TTS.")
            renpy.display.log.exception()
            platform_tts = None

    if platform_tts is None:
        try:
            if getattr(renpy, "android", False):
                platform_tts = AndroidTTS()

            elif getattr(renpy, "ios", False) or getattr(renpy, "macintosh", False):
                platform_tts = AppleTTS()

            elif getattr(renpy, "linux", False):
                platform_tts = LinuxTTS()

            elif getattr(renpy, "windows", False) or sys.platform.startswith("win"):
                platform_tts = WindowsTTS()

            elif getattr(renpy, "emscripten", False):
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


VOICE_RE = re.compile(r"{voice=([^}]+)}")


def get_voice(text: str = ""):
    """
    :undocumented:

    Returns the self-voicing voice to use. If :var:`preferences.tts_voice` is set,
    it is used. If the selected voice is not in the list of available voices, returns None.
    """

    if m := VOICE_RE.search(text):
        voice = m.group(1)
        text = VOICE_RE.sub("", text)

    prefs = getattr(getattr(renpy, "game", None), "preferences", None)
    voice = prefs.tts_voice if prefs is not None else None

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
            mode_was = old_self_voicing
            old_self_voicing = self_voicing
            if mode_was == "screenreader":
                speak(renpy.translation.translate_string("Screen reader voicing disabled."), force=True)
            elif mode_was == "clipboard":
                speak(renpy.translation.translate_string("Clipboard voicing disabled."), force=True)
            else:
                speak(renpy.translation.translate_string("Self-voicing disabled."), force=True)

        last = ""

        return

    prefix = ""

    if old_self_voicing != self_voicing:
        old_self_voicing = self_voicing

        if self_voicing == "clipboard":
            prefix = renpy.translation.translate_string("Clipboard voicing enabled. ")
        elif self_voicing == "screenreader":
            prefix = renpy.translation.translate_string("Screen reader voicing enabled. ")
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
        last = get_voice(s)[1]
        tts(prefix + s)
