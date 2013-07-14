# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
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
#
# cython: boundscheck=False, wraparound=False

import time
from textsupport cimport Glyph, SPLIT_INSTEAD, SPLIT_BEFORE, SPLIT_NONE, RUBY_TOP
from libc.stdlib cimport calloc, malloc, free

import collections
times = collections.defaultdict(float)

DEF INFINITY = float("+inf")

cdef struct Word:

    void *glyph

    # The index of the glyph in the list of glyphs.
    # int glyph_index

    # The x coordinate of the start of this word, not including preceding
    # whitespace.
    double start_x

    # The x coordinate of the end of this word.
    double end_x


cdef class WordWrapper(object):

    # The list of words created.
    cdef Word *words
    cdef int len_words
    cdef list glyphs
    cdef double *scores
    cdef int *splits

    def __init__(self, list glyphs, first_width, rest_width, subtitle):

        if not glyphs:
            return

        self.glyphs = glyphs
        self.make_word_list(glyphs)
        self.knuth_plass(first_width, rest_width, subtitle)
        self.unmark_splits()

    def __dealloc__(self):
        if self.words:
            free(self.words)
        if self.scores:
            free(self.scores)
        if self.splits:
            free(self.splits)


    cdef void unmark_splits(self):

        cdef list glyphs = self.glyphs
        cdef Glyph g
        cdef Word *words = self.words

        cdef int start
        cdef int end = self.len_words
        cdef int i

        while end:

            start = self.splits[end]

            # Note that we start iteration at start+1, so we don't unmark the
            # first character.
            for i from start < i < end:
                (<Glyph> words[i].glyph).split = SPLIT_NONE

            end = start


    cdef void knuth_plass(self, int first_width, int rest_width, bint subtitle):

        cdef double *scores
        cdef int *splits
        cdef Word *words = self.words
        cdef int len_words = self.len_words
        cdef double line_width

        cdef int i, j
        cdef double score, min_score
        cdef int split
        cdef double j_x, width

        scores = <double *> calloc(self.len_words + 1, sizeof(double))
        self.scores = scores
        splits = <int *> calloc(self.len_words + 1, sizeof(int))
        self.splits = splits

        # Base case, for a list of 0 length.
        scores[0] = 0.0
        splits[0] = 0

        for 1 <= j <= self.len_words:

            j_x = words[j-1].end_x

            min_score = INFINITY
            split = j - 1
            i = j

            while i > 0:

                i -= 1

                # The score taken from the previous line.
                score = scores[i] + 100000

                # The width of the current line.
                width = j_x - words[i].start_x

                if i:
                    line_width = first_width
                else:
                    line_width = rest_width

                if width > line_width:
                    # Only accept single-word long lines. Otherwise, give up and
                    # stop looping.
                    if i < j - 1:
                        break
                    else:
                        score += 100000.0 * (width - line_width)

                elif subtitle or j != len_words:

                    # Add a penalty proportional to the space left on the line.
                    score += (line_width - width) * (line_width - width)

                # If we beat the last score, use it.
                if score < min_score:
                    min_score = score
                    split = i

            scores[j] = min_score
            splits[j] = split


    cdef void make_word_list(self, list glyphs):
        """
        Break the list of words into a list of glyphs, on the
        split points.
        """

        cdef Word *words, *word
        cdef double start_x = 0, x = 0
        cdef Glyph g, start_glyph
        cdef list rv
        cdef int i, start_g

        cdef int len_glyphs = len(glyphs)
        cdef int len_words = 0


        words = <Word *> calloc(len_glyphs, sizeof(Word))
        word = words

        start_glyph = glyphs[0]
        x = start_glyph.advance

        for i from 1 <= i < len_glyphs:

            g = <Glyph> <object> glyphs[i]

            if g.ruby == RUBY_TOP:
                continue

            if g.split == SPLIT_INSTEAD:
                word.glyph = <void *> start_glyph
                word.start_x = start_x
                word.end_x = x
                len_words += 1
                word += 1

                start_x = x + g.advance
                start_glyph = g

            elif g.split == SPLIT_BEFORE:
                word.glyph = <void *> start_glyph
                word.start_x = start_x
                word.end_x = x
                len_words += 1
                word += 1

                start_x = x
                start_glyph = g

            x += g.advance

        word.glyph = <void *> start_glyph
        word.start_x = start_x
        word.end_x = x
        len_words += 1

        self.len_words = len_words
        self.words = words



def linebreak_tex(glyphs, first_width, rest_width, subtitle):
    WordWrapper(glyphs, first_width, rest_width, subtitle)
