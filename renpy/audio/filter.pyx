1#
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


from libc.stdlib cimport calloc, free
from libc.string cimport memcpy

from cpython.object cimport PyObject

from libc.math cimport M_PI
from libc.stdio cimport printf

import math

import renpy

DEF SUBCHANNELS = 2

# A list of samples that are being passed around through the filter system.
# Sample i of channel j is at data[i * subchannels + j].
#
# An AudioFilter should always return a new SampleBuffer, or one that is
# returned to it. It should deallocate any SampleBuffer that are returned
# to it, that it does not return. It should not deallocate its input.
cdef struct SampleBuffer:

    # The number of subchannels.
    int subchannels

    # The number of samples allocated in the buffer.
    int allocated_length

    # The number of samples in the buffer actually used.
    int length

    # The samples themselves.
    float *samples

    # A linked list of sample buffers with the same number of subchannels.
    SampleBuffer *next

# A linked list of sample buffers with 0-16 subchannels.
cdef SampleBuffer *free_buffers[SUBCHANNELS+1]

cdef SampleBuffer *allocate_buffer(int subchannels, int length) noexcept nogil:
    """
    Allocates a sample buffer.
    """

    cdef SampleBuffer *buf
    cdef int size

    if free_buffers[subchannels] is not NULL:
        buf = free_buffers[subchannels]
        free_buffers[subchannels] = buf.next
    else:
        buf = <SampleBuffer *> calloc(1, sizeof(SampleBuffer))
        buf.subchannels = subchannels
        buf.allocated_length = 0
        buf.samples = NULL

    if buf.allocated_length < length:
        size = length * subchannels * sizeof(float)

        if buf.samples is not NULL:
            free(buf.samples)

        buf.samples= <float *> calloc(1, size)
        buf.allocated_length = length

    buf.length = length

    return buf


cdef void free_buffer(SampleBuffer *buf) noexcept nogil:
    """
    Frees a sample buffer, by putting it back on the free list.
    """

    buf.next = free_buffers[buf.subchannels]
    free_buffers[buf.subchannels] = buf


cdef class AudioFilter:

    def __dealloc__(self):
        """
        Deallocates the filter.
        """

        try:
            renpy.audio.renpysound.deallocate_audio_filter(self)
        except Exception:
            pass

    def prepare(self, samplerate):
        """
        Prepares the filter for use at the given samplerate. This should be
        called before apply. It should be called for all children of the filter.

        Prepare may be called on the same filter multiple times, with the same
        samplerate. It should be safe to call prepare multiple times.
        """

        raise NotImplementedError("prepare")

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:
        """
        Applies the filter to the given samples.
        """

        return allocate_buffer(samples.subchannels, samples.length)

    def __repr__(self):
        args = self.__reduce__()[1]

        arg_repr = [ ]

        for i in args:
            arg_repr.append(repr(i))

        return "renpy.audio.filter.{}({})".format(self.__class__.__name__, ", ".join(arg_repr))


cdef class Null(AudioFilter):
    """
    :doc: audio_filter

    An audio filter that passes it's input through to its output unchanged.
    """

    def __reduce__(self):
        return (Null, ())

    def prepare(self, int samplerate):
        pass

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:
        cdef SampleBuffer *result = allocate_buffer(samples.subchannels, samples.length)
        memcpy(result.samples, samples.samples, samples.length * samples.subchannels * sizeof(float))
        return result


cdef class FilterList:
    """
    This is a list that stores some number of audio filters.
    """

    # A list of the filters, as python objects.
    cdef list list

    # The filters.
    cdef PyObject **filters

    # The length of the list.
    cdef int length

    def __init__(self, filters):
        self.list = list(filters)
        self.length = len(filters)
        self.filters = <PyObject **> calloc(self.length, sizeof(PyObject *))

        for i, f in enumerate(filters):
            self.filters[i] = <PyObject *> f

    def __dealloc__(self):
        free(self.filters)

    cdef SampleBuffer *apply(self, int index, SampleBuffer *samples) noexcept nogil:
        return (<AudioFilter> self.filters[index]).apply(samples)

    def __iter__(self):
        return iter(self.list)


cdef class Sequence(AudioFilter):
    """
    :doc: audio_filter

    An AudioFilter that applies its input to a sequence of filters, in order.
    This is used internally when a list of audiofilters is given, so it should
    be rare to use this directly.
    """

    cdef FilterList filters

    def __init__(self, *filters):

        if not filters:
            filters = [ Null() ]
        else:
            filters = [ to_audio_filter(f) for f in filters ]

        self.filters = FilterList(filters)

    def __reduce__(self):
        return (Sequence, tuple(self.filters.list))

    def prepare(self, int samplerate):

        for f in self.filters:
            f.prepare(samplerate)

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

        cdef SampleBuffer *result
        cdef SampleBuffer *old_result = samples

        for i in range(self.filters.length):
            result = self.filters.apply(i, old_result)

            if old_result != samples:
                free_buffer(old_result)

            old_result = result

        return old_result


cdef class Biquad(AudioFilter):
    """
    :undocumented:

    Used internally to implement many filters.
    """


    # Based on:

    # https://webaudio.github.io/Audio-EQ-Cookbook/Audio-EQ-Cookbook.txt

    # In this, x_0 is the input, x_1 is the input from the previous sample, and
    # x_2 is the input from two samples ago. y_0, y_1, and y_2 are the same for
    # the output.

    cdef public object kind
    cdef public float frequency
    cdef public float q
    cdef public float gain

    # The last two samples of input data.
    cdef float last_x_1[SUBCHANNELS]
    cdef float last_x_2[SUBCHANNELS]

    # The last two samples of output data.
    cdef float last_y_1[SUBCHANNELS]
    cdef float last_y_2[SUBCHANNELS]

    # The coefficients.
    cdef float cx0, cx1, cx2, cy1, cy2

    cdef bint prepared

    def __init__(self, kind, frequency=350, q=1.0, gain=0):

        if kind not in { "lowpass", "highpass", "bandpass", "lowshelf", "highshelf", "peaking", "notch", "allpass" }:
            raise ValueError("Invalid kind {!r}.".format(kind))

        if q < 0.01:
            q = 0.01

        if frequency < 1:
            frequency = 1

        self.kind = kind
        self.frequency = frequency
        self.q = q
        self.gain = gain

    def __reduce__(self):
        return (Biquad, (self.kind, self.frequency, self.q, self.gain))

    def prepare(self, samplerate):

        if self.prepared:
            return

        self.prepared = True

        # The provided variables.
        Fs = samplerate
        f0 = self.frequency
        dBgain = self.gain
        Q = self.q

        # Intermediates.
        A = 10 ** (dBgain / 40)

        w0 = 2 * M_PI * self.frequency / Fs

        cos_w0 = math.cos(w0)
        sin_w0 = math.sin(w0)

        alpha = sin_w0 / (2 * Q)

        two_sqrt_A_alpha = 2 * math.sqrt(A) * alpha

        # The coefficients.
        if self.kind == "lowpass":
            b0 =  (1 - cos_w0)/2
            b1 =   1 - cos_w0
            b2 =  (1 - cos_w0)/2
            a0 =   1 + alpha
            a1 =  -2*cos_w0
            a2 =   1 - alpha

        elif self.kind == "highpass":

            b0 =  (1 + cos_w0)/2
            b1 = -(1 + cos_w0)
            b2 =  (1 + cos_w0)/2
            a0 =   1 + alpha
            a1 =  -2*cos_w0
            a2 =   1 - alpha

        elif self.kind == "bandpass":

            # (constant skirt gain, peak gain = Q)

            b0 =   sin_w0/2
            b1 =   0
            b2 =  -sin_w0/2
            a0 =   1 + alpha
            a1 =  -2*cos_w0
            a2 =   1 - alpha

            # (constant 0 dB peak gain)

            # b0 =   alpha
            # b1 =   0
            # b2 =  -alpha
            # a0 =   1 + alpha
            # a1 =  -2*cos_w0
            # a2 =   1 - alpha

        elif self.kind == "notch":

            b0 =   1
            b1 =  -2*cos_w0
            b2 =   1
            a0 =   1 + alpha
            a1 =  -2*cos_w0
            a2 =   1 - alpha

        elif self.kind == "allpass":

            b0 =   1 - alpha
            b1 =  -2*cos_w0
            b2 =   1 + alpha
            a0 =   1 + alpha
            a1 =  -2*cos_w0
            a2 =   1 - alpha

        elif self.kind == "peaking":

            b0 =   1 + alpha*A
            b1 =  -2*cos_w0
            b2 =   1 - alpha*A
            a0 =   1 + alpha/A
            a1 =  -2*cos_w0
            a2 =   1 - alpha/A

        elif self.kind == "lowshelf":

            b0 =    A*( (A+1) - (A-1)*cos_w0 + two_sqrt_A_alpha )
            b1 =  2*A*( (A-1) - (A+1)*cos_w0                   )
            b2 =    A*( (A+1) - (A-1)*cos_w0 - two_sqrt_A_alpha )
            a0 =        (A+1) + (A-1)*cos_w0 + two_sqrt_A_alpha
            a1 =   -2*( (A-1) + (A+1)*cos_w0                   )
            a2 =        (A+1) + (A-1)*cos_w0 - two_sqrt_A_alpha

        elif self.kind == "highshelf":

            b0 =    A*( (A+1) + (A-1)*cos_w0 + two_sqrt_A_alpha )
            b1 = -2*A*( (A-1) + (A+1)*cos_w0                   )
            b2 =    A*( (A+1) + (A-1)*cos_w0 - two_sqrt_A_alpha )
            a0 =        (A+1) - (A-1)*cos_w0 + two_sqrt_A_alpha
            a1 =    2*( (A-1) - (A+1)*cos_w0                   )
            a2 =        (A+1) - (A-1)*cos_w0 - two_sqrt_A_alpha

        self.cx0 = b0 / a0
        self.cx1 = b1 / a0
        self.cx2 = b2 / a0

        self.cy1 = a1 / a0
        self.cy2 = a2 / a0


    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

        cdef SampleBuffer *result = allocate_buffer(samples.subchannels, samples.length)
        cdef int i, j
        cdef float x0, x1, x2, y0, y1, y2


        for j in range(samples.subchannels):

            x1 = self.last_x_1[j]
            x2 = self.last_x_2[j]

            y1 = self.last_y_1[j]
            y2 = self.last_y_2[j]

            for i in range(samples.length):
                x0 = samples.samples[i * samples.subchannels + j]
                y0 = self.cx0 * x0 + self.cx1 * x1 + self.cx2 * x2 - self.cy1 * y1 - self.cy2 * y2

                result.samples[i * samples.subchannels + j] = y0

                x2 = x1
                x1 = x0

                y2 = y1
                y1 = y0

            self.last_x_1[j] = x1
            self.last_x_2[j] = x2

            self.last_y_1[j] = y1
            self.last_y_2[j] = y2

        return result


def Lowpass(frequency=350, q=1.0):
    """
    :doc: audio_filter

    A lowpass filter with 12/dB octave rolloff.

    `frequency`
        The cutoff frequency.

    `q`
        Controls how peaked the response will be in decibels. For this filter
        type, this value is not a traditional Q, but is a resonance value in decibels.
    """

    return Biquad("lowpass", frequency=frequency, q=q)

def Highpass(frequency=350, q=1.0):
    """
    :doc: audio_filter

    A highpass filter with 12/dB octave rolloff.

    `frequency`
        The cutoff frequency.

    `q`
        Controls how peaked the response will be in decibels. For this filter
        type, this value is not a traditional Q, but is a resonance value in decibels.
    """

    return Biquad("highpass", frequency=frequency, q=q)

def Bandpass(frequency=350, q=1.0):
    """
    :doc: audio_filter

    A bandpass filter.


    `frequency`
        The center frequency.

    `q`
        Controls the width of the band. The width becomes narrower as the
        value of Q increases.
    """


    return Biquad("bandpass", frequency=frequency, q=q)


def Lowshelf(frequency=350, gain=0):
    """
    :doc: audio_filter

    A lowshelf filter that allows all frequencies through, but boosts those
    below a certain frequency by a certain amount.

    `frequency`
        The upper frequency.

    `gain`
        The amount to boost the frequencies below the upper frequency,
        in decibels.
    """

    return Biquad("lowshelf", frequency=frequency, gain=gain)


def Highshelf(frequency=350, gain=0):
    """
    :doc: audio_filter

    A highshelf filter that allows all frequencies through, but boosts those
    above a certain frequency by a certain amount.

    `frequency`
        The lower frequency.

    `gain`
        The amount to boost the frequencies above the lower frequency,
        in decibels.
    """

    return Biquad("highshelf", frequency=frequency, gain=gain)


def Peaking(frequency=350, q=1.0, gain=0):
    """
    :doc: audio_filter

    A peaking filter that allows all frequencies through, but boosts those
    around a certain frequency by a certain amount.

    `frequency`
        The center frequency.

    `q`
        Controls the sharpness of the peak. The higher the value, the sharper
        the peak.

    `gain`
        The amount to boost the frequencies around the center frequency,
        in decibels.
    """

    return Biquad("peaking", frequency=frequency, q=q, gain=gain)


def Notch(frequency=350, q=1.0):
    """
    :doc: audio_filter

    The opposite of a bandpass filter. Frequencies inside a range surrounding
    `frequency` are suppressed, while other frequences are passed through.

    `frequency`
        The center frequency.

    `q`
        Controls the width of the notch. The width becomes narrower as the
        value of q increases.
    """

    return Biquad("notch", frequency=frequency, q=q)


def Allpass(frequency=350, q=1.0):
    """
    :doc: audio_filter

    An allpass filter allows all frequencies through, but changes the phase
    relationship between the various frequencies.


    `frequency`
        The frequency at the center of the phase change.

    `q`
        Controls the sharpness of the phase shift. The higher the value, the
        sharper the phase shift.
    """

    return Biquad("allpass", frequency=frequency, q=q)


cdef class Crossfade(AudioFilter):
    """
    :undocumented:

    This is intended for internal use. It crossfades between two filters
    over the course of multiple samples.

    The crossfade filter takes two filters, and crossfades between them. The
    `position` parameter controls the position of the crossfade, with 0 being
    the first filter, and 1 being the second filter. The `position` parameter
    can be any value, and the filter will interpolate between the two filters
    as needed.

    This is useful for creating smooth transitions between two filters, such as
    when changing the volume of a sound, or changing the pitch of a sound.
    """

    cdef public AudioFilter filter1
    cdef public AudioFilter filter2

    cdef public float duration

    cdef int duration_samples
    cdef int complete_samples

    def __init__(self, filter1, filter2, duration=0.05):

        self.filter1 = to_audio_filter(filter1)
        self.filter2 = to_audio_filter(filter2)

        self.duration = duration

        self.duration_samples = 0
        self.complete_samples = 0

    def __reduce__(self):
        return (Crossfade, (self.filter1, self.filter2, self.duration))

    def prepare(self, int samplerate):
        self.filter1.prepare(samplerate)
        self.filter2.prepare(samplerate)

        self.duration_samples = int(self.duration * samplerate)

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

        cdef SampleBuffer *result1
        cdef SampleBuffer *result2
        cdef SampleBuffer *result
        cdef int i, j
        cdef float done, s1, s2

        result2 = self.filter2.apply(samples)

        # Shortcut things if the fade is complete.
        if self.complete_samples >= self.duration_samples:
            return result2

        result1 = self.filter1.apply(samples)

        result = allocate_buffer(samples.subchannels, samples.length)

        for i in range(samples.length):
            done = 1.0 * self.complete_samples / self.duration_samples

            for j in range(samples.subchannels):
                s1 = result1.samples[i * samples.subchannels + j]
                s2 = result2.samples[i * samples.subchannels + j]

                result.samples[i * samples.subchannels + j] = s1 + (s2 - s1) * done

            if self.complete_samples < self.duration_samples:
                self.complete_samples += 1

        free_buffer(result1)
        free_buffer(result2)

        return result


cdef class Mix(AudioFilter):
    """
    :doc: audio_filter

    An audio filter that splits its input into multiple streams, applies
    each of its arguments to a stream, and mixes those streams by summing
    them together.

    For example::

        init python:

            import renpy.audio.filter as af

            # This mixes the unchanged input with a delay.
            $ echo = af.Mix(af.Null(), af.Delay(.3))
    """

    cdef FilterList filters

    def __init__(self, *filters):
        filters = [ to_audio_filter(f) for f in filters ]

        if not filters:
            filters = [ Null() ]

        self.filters = FilterList(filters)

    def __reduce__(self):
        return (Mix, tuple(self.filters.list))

    def prepare(self, int samplerate):
        for f in self.filters:
            f.prepare(samplerate)

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

            cdef SampleBuffer *result = NULL
            cdef SampleBuffer *temp
            cdef int i, j

            for i in range(self.filters.length):

                temp = self.filters.apply(i, samples)

                if result == NULL:
                    result = temp
                else:
                    for j in range(result.length * result.subchannels):
                        result.samples[j] += temp.samples[j]

                    free_buffer(temp)

            return result


cdef class Multiply(AudioFilter):
    """
    :doc: audio_filter

    An audio filter that multiplies its input by `multiplier`.
    """

    cdef float multiplier

    def __init__(self, multiplier):
        self.multiplier = multiplier

    def __reduce__(self):
        return (Multiply, (self.multiplier,))

    def prepare(self, int samplerate):
        return

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

            cdef SampleBuffer *result
            cdef int i, j

            result = allocate_buffer(samples.subchannels, samples.length)

            for j in range(result.length * result.subchannels):
                result.samples[j] = samples.samples[j] * self.multiplier

            return result


def Gain(db):
    """
    An audio filter that adjusts the gain of the input by `db` decibels.
    """

    return Multiply(10 ** (db / 20))


cdef class DelayBuffer:
    """
    :undocumented:

    This implements a buffer that delays its input by a certain number of samples.
    It expects that the same number of samples will be added and removed each time
    a filter is applied, but it doesn't enforce an order.
    """

    # The number of samples in the buffer.
    cdef int length

    # The samples stored in this buffer.
    cdef float *buffer

    # The write index.
    cdef int write_index[SUBCHANNELS]

    # The read index.
    cdef int read_index[SUBCHANNELS]

    def __init__(self, delay, sample_rate, subchannels):

        if not isinstance(delay, (list, tuple)):
            delay = [ delay ] * subchannels
        else:
            if len(delay) != subchannels:
                raise ValueError("Delay must be a single value or a list of values with the same length as the number of subchannels.")


        samples = int((max(delay) + 1) * sample_rate)
        self.length = samples

        self.buffer = <float *> calloc(samples * subchannels, sizeof(float))

        for j in range(subchannels):
            self.write_index[j] = int(delay[j] * sample_rate)
            self.read_index[j] = 0

    def __dealloc__(self):
        free(self.buffer)

    cdef void queue(self, SampleBuffer *samples) noexcept nogil:

        cdef int i, j

        for i in range(samples.length):
            for j in range(samples.subchannels):
                self.buffer[self.write_index[j]] = samples.samples[i * samples.subchannels + j]
                self.write_index[j] = (self.write_index[j] + 1) % self.length

    cdef SampleBuffer * dequeue(self, int subchannels, int length) noexcept nogil:

        cdef SampleBuffer *result = allocate_buffer(subchannels, length)
        cdef int i, j

        for i in range(length):
            for j in range(subchannels):
                result.samples[i * subchannels + j] = self.buffer[self.read_index[j]]
                self.read_index[j] = (self.read_index[j] + 1) % self.length

        return result


cdef class Delay(AudioFilter):
    """
    :doc: audio_filter

    This filter implements a delay. Samples that are provided to the input
    emerge from the output after `delay` seconds.

    `delay`
        The delay, in seconds. If a list of delays is provided, each subchannel
        will be delayed by the corresponding amount. Each delay must be at least
        0.01 seconds.
    """

    cdef DelayBuffer buffer
    cdef object delay
    cdef float max_delay

    def __cinit__(self):
        self.buffer = None

    def __init__(self, delay):
        self.delay = delay

        if not isinstance(delay, (list, tuple)):
            self.max_delay = delay
        else:
            self.max_delay = max(delay)

    def __reduce__(self):
        return (Delay, (self.delay,))

    def prepare(self, int samplerate):

        if self.buffer is None and self.max_delay >= 0.01:
            self.buffer = DelayBuffer(self.delay, samplerate, SUBCHANNELS)

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:
        cdef SampleBuffer *result

        if self.max_delay < 0.01:
            result = allocate_buffer(samples.subchannels, samples.length)
            memcpy(result.samples, samples.samples, samples.length * samples.subchannels * sizeof(float))
            return result

        self.buffer.queue(samples)
        return self.buffer.dequeue(samples.subchannels, samples.length)


cdef class Comb(AudioFilter):
    """
    :doc: audio_filter

    A comb filter. A comb filter consists of a delay that is filtered and
    mutiplied, mixed with its input, and then fed back into the delay,
    causing the filter to be applied multiple times.

    `delay`
        The delay, in seconds. If a list of delays is provided, each subchannel
        will be delayed by the corresponding amount. Each delay must be at least
        0.01 seconds.

    `filter`
        The filter to apply to the delayed signal. If None, the Null filter
        is used.

    `multiplier`
        The amount to multiply the filtered signal by.

    `wet`
        If True, the output of the filter is the sum of the input and the
        filtered and multiplied signal.  If False, the output is just the filtered
        and muliplied signal.
    """

    cdef DelayBuffer buffer
    cdef AudioFilter filter
    cdef object delay
    cdef float max_delay
    cdef float multiplier
    cdef bint wet

    def __init__(self, delay, filter=None, multiplier=1.0, wet=True):

        self.delay = delay

        if not isinstance(delay, (list, tuple)):
            self.max_delay = delay
        else:
            self.max_delay = max(delay)

        self.multiplier = multiplier
        self.wet = False

        if filter is None:
            filter = Null()

        self.filter = to_audio_filter(filter)

    def __reduce__(self):
        return (Comb, (self.delay, self.filter, self.multiplier, self.wet))

    def prepare(self, int samplerate):
        if self.buffer is None and self.max_delay >= 0.01:
            self.buffer = DelayBuffer(self.delay, samplerate, SUBCHANNELS)

        self.filter.prepare(samplerate)

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

        cdef SampleBuffer *delayed
        cdef SampleBuffer *result
        cdef SampleBuffer *with_wet
        cdef int i, j

        if self.max_delay < 0.01:
            result = allocate_buffer(samples.subchannels, samples.length)
            memcpy(result.samples, samples.samples, samples.length * samples.subchannels * sizeof(float))
            return result

        delayed = self.buffer.dequeue(samples.subchannels, samples.length)
        filtered = self.filter.apply(delayed)
        with_wet = allocate_buffer(samples.subchannels, samples.length)

        for i in range(samples.length * samples.subchannels):
            filtered.samples[i] = filtered.samples[i] * self.multiplier
            with_wet.samples[i] = filtered.samples[i] + samples.samples[i]

        self.buffer.queue(with_wet)

        free_buffer(delayed)

        if self.wet:
            free_buffer(filtered)
            return with_wet
        else:
            free_buffer(with_wet)
            return filtered


cdef class WetDry(AudioFilter):
    """
    :doc: audio_filter

    A filter that mixes its input with the output of a filter.

    `filter`
        The filter to apply to the input.

    `wet`
        A multiplier, generally between 0.0 and 1.0, that controls the amount
        of the filter that is mixed in.

    `dry`
        A multiplier, generally between 0.0 and 1.0, that controls the amount
        of the input that is mixed in.
    """

    cdef AudioFilter filter
    cdef float wet
    cdef float dry

    def __init__(self, filter, wet=1.0, dry=1.0):
        self.filter = to_audio_filter(filter)
        self.wet = wet
        self.dry = dry

    def __reduce__(self):
        return (WetDry, (self.filter, self.wet, self.dry))

    def prepare(self, int samplerate):
        self.filter.prepare(samplerate)

    cdef SampleBuffer *apply(self, SampleBuffer *samples) noexcept nogil:

        cdef SampleBuffer *result
        cdef SampleBuffer *filtered
        cdef int i, j

        filtered = self.filter.apply(samples)
        result = allocate_buffer(samples.subchannels, samples.length)

        for i in range(samples.length * samples.subchannels):
            result.samples[i] = samples.samples[i] * self.dry + filtered.samples[i] * self.wet

        free_buffer(filtered)

        return result


def Reverb(
    resonance=.5,
    dampening=880,
    wet=1.0,
    dry=1.0,
    delay_multiplier=1.0,
    delay_times=[0.0253, 0.0269, 0.029, 0.0307, 0.0322, 0.0338, 0.0353, 0.0367],
    delay_subchannel=0.001,
    allpass_frequences=[225, 556, 441, 341],
    ):
    """
    :doc: audio_filter

    An artificial reverb filter that simulates the sound of a room or hall,
    somewhat inspired by Freeverb.

    `resonance`
        The amount of feedback in the reverb. This should be between 0 and 1.
        Larger numbers make the reverb last longer. Too large values will
        cause the reverb to go out of control.

    `dampening`
        This applies a lowpass filter to each reverberation, simulating
        the lost of high frequences as sound passes through the air.

    `wet`
        A multiplier that is applied to the reverb signal before it is passed
        to the output.

    `dry`
        A multiplier that is applied to the input signal before it is passed
        to the output. Set this to 0.0 to only hear the reverb, not the original
        sound.

    `delay_multiplier`
        A multiplier that is applied to the delay times. This can be used to
        adjust the length of the reverb.

    `delay_times`
        A list of delay times, in seconds, that are used to create the early
        reflections. These are used to create comb filters.

    `delay_subchannel`
        The amount of time, in seconds, that is added to each delay time to
        create a second subchannel. This is used to create a stereo effect.

    `allpass_frequences`
        A list of frequences, in hertz, that are used to create allpass filters
        that simulate late reflections.
    """


    # This prevents the reverb from going out of control.
    resonance *= .85

    # Apply delay_multiplier to the delay times.
    delay_times = [ d * delay_multiplier for d in delay_times ]

    comb_filters = [ ]

    for i in delay_times:
        comb_filters.append(Comb([ i, i + delay_subchannel ], Biquad('lowpass', dampening), resonance, False))

    rv = [ Mix(*comb_filters) ]

    for i in allpass_frequences:
        rv.append( Biquad("allpass", i) )

    return WetDry(rv, wet, dry)


def to_audio_filter(o):
    """
    :undocumented:

    Converts a Python object to an AudioFilter. This expands lists into
    Sequence objects, passes AudioFilter objects through, and raises
    an exception for anything else.
    """

    if isinstance(o, AudioFilter):
        return o

    if isinstance(o, list):
        return Sequence(*o)

    raise TypeError("Expected an AudioFilter, got {!r}.".format(o))


cdef void apply_audio_filter(AudioFilter af, float *samples, int subchannels, int length, int samplerate) noexcept nogil:
    """
    :undocumented:
    """


    cdef SampleBuffer *input_buffer
    cdef SampleBuffer *result_buffer
    cdef int i, j

    # We process data in 10ms chunks.
    cdef int remaining = length

    while remaining > 0:
        length = min(remaining, samplerate // 100)

        input_buffer = allocate_buffer(subchannels, length)

        memcpy(input_buffer.samples, samples, length * subchannels * sizeof(float))

        result_buffer = af.apply(input_buffer)

        memcpy(samples, result_buffer.samples, length * subchannels * sizeof(float))

        free_buffer(result_buffer)
        free_buffer(input_buffer)

        samples += length * subchannels
        remaining -= length

    return


cdef apply_audio_filter_type *get_apply_audio_filter() noexcept:
    return <apply_audio_filter_type *> apply_audio_filter
