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


Filter Reuse
------------

When a filter is set on a channel, it will filter all audio played on
that channel. Specifically, the Comb, Delay, and Reverb filters will
continue to output information from old audio files for some time
after a new audio file has started playing, provided the filter is
not changed.

This means that Ren'Py is storing audio information inside the filter
object. Because of this, it is generally not a good idea to share filter
objects between channels, or to use a filter object multiple times with
a single channel.


Silence Padding
---------------

When an audio filter is active and the last queued sound on a channel finises
playing, Ren'Py will add 2 seconds of silence to the channel, to ensure that
delay and reverb filters have time to finish playing.

If you need more silence, it can be queued with::

    queue sound "<silence 10">


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
