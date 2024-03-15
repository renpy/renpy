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


from libc.stdlib cimport calloc, free
from libc.string cimport memcpy

from cpython.object cimport PyObject


DEF SUBCHANNELS = 16

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
cdef SampleBuffer *free_buffers[SUBCHANNELS]

cdef SampleBuffer *allocate_buffer(int subchannels, int length) nogil:
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


cdef void free_buffer(SampleBuffer *buf) nogil:
    """
    Frees a sample buffer, by putting it back on the free list.
    """

    buf.next = free_buffers[buf.subchannels]
    free_buffers[buf.subchannels] = buf


cdef class AudioFilter:

    def check_subchannels(self, int subchannels):
        """
        Checks if the filter can handle the given number of subchannels. This
        should raise an exception if the number of subchannels is not supported,
        and return the number of subchannels that the filter will return if is.
        """

        raise NotImplementedError("check_subchannels")

    cdef SampleBuffer *apply(self, SampleBuffer *samples) nogil:
        """
        Applies the filter to the given samples.
        """

        return allocate_buffer(samples.subchannels, samples.length)


cdef class SequenceFilter(AudioFilter):
    """
    A filter that applies a series of filters in sequence.
    """

    # The filters, in a Python list.
    cdef list filters

    # The filters, in a C array.
    cdef PyObject *cfilters[8]

    # The number of filter objects in the array.
    cdef int filter_count

    def __init__(self, filters):
        filters = [ to_audio_filter(f) for f in filters ]

        if len(filters) > 8:
            split = len(filters) // 2
            filters = [ SequenceFilter(filters[:split]), SequenceFilter(filters[split:]) ]

        self.filters = filters

        self.filter_count = len(filters)

        for i, f in enumerate(filters):
            self.filters[i] = f

    def check_subchannels(self, int subchannels):

        for f in self.filters:
            subchannels = f.check_subchannels(subchannels)

        return subchannels

    cdef SampleBuffer *apply(self, SampleBuffer *samples) nogil:

        cdef SampleBuffer *result = allocate_buffer(samples.subchannels, samples.length)
        cdef SampleBuffer *old_result = samples

        for i in range(self.filter_count):
            result = (<AudioFilter> self.cfilters[i]).apply(old_result)

            if result != samples:
                free_buffer(old_result)

            old_result = result

        return result


cdef class LowpassFilter(AudioFilter):
    """
    A simple lowpass filter, for test purposes. This will be replaced by
    BiQuadFilter.
    """

    cdef float last[SUBCHANNELS]

    def check_subchannels(self, subchannels):
        return subchannels

    cdef SampleBuffer *apply(self, SampleBuffer *samples) nogil:
        """
        Applies the filter to the given samples.
        """

        cdef int i, j, index
        cdef float *data
        cdef float v

        result = allocate_buffer(samples.subchannels, samples.length)

        for i in range(samples.length):
            for j in range(samples.subchannels):
                index = i * samples.subchannels + j

                v = self.last[j]
                v += (samples.samples[index] - v) * 0.05

                result.samples[index] = v
                self.last[j] = v

        return result


def to_audio_filter(o):
    """
    Converts a Python object to an AudioFilter. This expands lists into
    SequenceFilter objects, passes AudioFilter objects through, and raises
    an exception for anything else.
    """

    if isinstance(o, AudioFilter):
        return o

    if isinstance(o, list):
        return SequenceFilter(o)

    raise TypeError("Expected an AudioFilter, got {!r}.".format(o))



cdef void apply_audio_filter(AudioFilter af, float *samples, int subchannels, int length) nogil:

    cdef SampleBuffer *input_buffer
    cdef SampleBuffer *result_buffer
    cdef int i, j

    input_buffer = allocate_buffer(subchannels, length)

    memcpy(input_buffer.samples, samples, length * subchannels * sizeof(float))

    result_buffer = af.apply(input_buffer)

    memcpy(samples, result_buffer.samples, length * subchannels * sizeof(float))

    free_buffer(input_buffer)
    free_buffer(result_buffer)

    return


cdef apply_audio_filter_type *get_apply_audio_filter():
    return <apply_audio_filter_type *> apply_audio_filter
