Audio Filters
==============

Audio filters allow a game to change the sound on a channel from what is
present in an audio file. This can be used to add effects to the sound,
including reverb, delay/echo, and high-pass/low-pass filters.

Audio filters are placed in the renpy.audio.filter module. Although
not strictly required, it is recommended that module be aliased to something
shorter, like ``af``, using::

    define af = renpy.audio.filter

The filters can then be invoked using the :func:`renpy.music.set_audio_filter`
function, like::

    $ renpy.music.set_audio_filter("music", af.Reverb(0.5))

By default, the filter takes effect at the start of the next audio file
queued or played. If you want to apply the filter to the currently playing
and queued audio, you can use the `replace` argument::

    $ renpy.music.set_audio_filter("music", af.Lowpass(440), replace=True)

This will apply the filter to the audio as soon as possible.

Finally, you can remove a filter from a channel by passing None as the filter::

    $ renpy.music.set_audio_filter("music", None)

(It's also possible to give None with `replace` set to True.)


Audio Filters
-------------

Whenever a filter is accepted, a list may be given instead, to represent a
:class:`renpy.audio.filter.Sequence` of those filters. So writing::

    renpy.music.set_audio_filter("music", [af.Reverb(0.5), af.Lowpass(440)])

is equivalent to::

    renpy.music.set_audio_filter("music",
        af.Sequence([
            af.Reverb(0.5),
            af.Lowpass(440),
            ]))

Apart from that, the audio filters consist of the following classes. It's not
possible to define your own, for performance reasons.

.. include:: inc/audio_filter
