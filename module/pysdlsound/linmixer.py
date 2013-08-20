#@PydevCodeAnalysisIgnore
from ossaudiodev import * #@UnusedWildImport
mixer = openmixer()

def get_wave():
    if not mixer.controls() & 1 << SOUND_MIXER_PCM:
        return None

    l, r = mixer.get(SOUND_MIXER_PCM)

    return (l + r) / 200.0

def set_wave(vol):
    if not mixer.controls() & 1 << SOUND_MIXER_PCM:
        return None

    v = int(vol * 100)

    mixer.set(SOUND_MIXER_PCM, (v, v))


def get_midi():
    return None

def set_midi(vol):
    return
