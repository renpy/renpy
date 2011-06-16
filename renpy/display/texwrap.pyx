# Copyright 2004-2011 Tom Rothamel <pytom@bishoujo.us>
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
from textsupport cimport Glyph, SPLIT_INSTEAD, SPLIT_BEFORE, SPLIT_NONE
from libc.stdlib cimport calloc, malloc, free

import collections
times = collections.defaultdict(float)

cdef struct Word:

    void *glyph

    # The index of the glyph in the list of glyphs.
    # int glyph_index

    # The x coordinate of the start of this word, not including preceding
    # whitespace.
    int start_x
    
    # The x coordinate of the end of this word.
    int end_x
        
        
cdef class WordWrapper(object):
    
    # The list of words created.
    cdef Word *words
    cdef int len_words
    cdef list glyphs
    cdef long long *scores
    cdef int *splits

    def __init__(self, list glyphs):
        if not glyphs:
            return
        
        self.glyphs = glyphs        
        self.make_word_list(glyphs)
        self.knuth_plass(800, 800, False)        
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
    
        cdef long long *scores
        cdef int *splits
        cdef Word *words = self.words
        cdef int len_words = self.len_words
        cdef int line_width
        
        cdef int i, j
        cdef long long score, min_score
        cdef int split
        cdef int j_x, width
        
        scores = <long long *> calloc(self.len_words + 1, sizeof(long long))
        self.scores = scores
        splits = <int *> calloc(self.len_words + 1, sizeof(int))
        self.splits = splits
        
        # Base case, for a list of 0 length.
        scores[0] = 0
        splits[0] = 0
        
        for 1 <= j <= self.len_words:
            
            j_x = words[j-1].end_x
            
            min_score = 1 << 63 - 1 # Max Long Long
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
                        score += 100000LL * (width - line_width) 
                                    
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
        cdef int start_x = 0, x = 0
        cdef Glyph g, start_glyph
        cdef list rv
        cdef int i, start_g
        
        cdef int len_glyphs = len(glyphs)
        cdef int len_words = 0
        
        
        words = <Word *> calloc(len_glyphs, sizeof(Word))        
        word = words
        
        start_glyph = glyphs[0]
        x = <int> start_glyph.advance
        
        for i from 1 <= i < len_glyphs:

            g = <Glyph> <object> glyphs[i]
                    
            if g.split == SPLIT_INSTEAD:
                word.glyph = <void *> start_glyph
                word.start_x = start_x
                word.end_x = x
                len_words += 1
                word += 1
                
                start_x = x + <int> g.advance
                start_glyph = g
        
            elif g.split == SPLIT_BEFORE:
                word.glyph = <void *> start_glyph
                word.start_x = start_x
                word.end_x = x
                len_words += 1
                word += 1
        
                start_x = x
                start_glyph = g
            
            x += <int> g.advance
        
        word.glyph = <void *> start_glyph
        word.start_x = start_x
        word.end_x = x        
        len_words += 1

        self.len_words = len_words
        self.words = words

   

#===============================================================================
# cdef int penalty(self, int i, int j):
#    
#    cdef int total
#    cdef int lw
#    cdef int width
#    cdef Word word_i, word_j
#    
#    if j > self.len_words:
#        return -i
#    
#    # Figure out the length of the line.
#    if i == 0:
#        lw = self.first_width
#    else:
#        lw = self.rest_width
#    
#    # The total cost, includes the cost for the new line.
#    total = self.value(i) + 100000
# 
#    # The width of the current words.
#    word_i = self.words[i]
#    word_j = self.words[j-1]
#    width = word_j.end_x - word_i.start_x
#    
#    # Figure out penalties to give.        
#    if width > lw:
#        total += 100000 * (width - lw)
# 
#    elif j < self.len_words or self.subtitle:
#        total += (lw - width) ** 2
#       
#    # This is more for testing than anything.
#    if i >= j:
#        return 0
#        
#    return total
# 
# cdef int word_width(list words, int i, int j):
# 
#    cdef int k
#    cdef Word w
#    cdef int rv = 0
#    
#    for k from i <= k < j:
#        w = words[k]
#        rv += w.width
# 
#        if k != i:
#            rv += w.not_first
# 
#    return rv
#===============================================================================

def linebreak_tex(glyphs, first_width, rest_width, subtitle):
    WordWrapper(glyphs)


#===============================================================================
# def linebreak_tex(list glyphs, int first_width, int rest_width, bint subtitle):    
#    cdef Word w
#    cdef Glyph g
#    cdef list words
#    cdef int i, start, pos
#    cdef OnlineConcaveMinima cost
# 
#    times.clear()
#    
#    words = make_word_list(glyphs)        
#===============================================================================
#===============================================================================
#    cost = OnlineConcaveMinima(0, words, first_width, rest_width, subtitle)
#    pos = len(words)
# 
#    while pos:
#        
#        start = cost.index(pos)
# 
#        for i from start + 1 <= i < pos:
#            w = words[i]
#            w.g.split = SPLIT_NONE
#        
#        pos = start
# 
#    for k, v in times.iteritems():
#        print k, v * 1000
#===============================================================================

    #===========================================================================
    # for i in range(0, len(words)):
    #    for j in range(0, len(words)):
    #        print "{:d}x{:d} {:d}  ".format(i, j, cost.penalty(i, j)),
    #        
    #    print 
    #    
    # print
    #===========================================================================
    
    #===========================================================================
    # for i in range(0, len(words)):
    #    for j in range(0, len(words)):
    #        print "{:d}x{:d} {:d}   ".format(i, j, word_width(i, j)),
    #        
    #    print
    # 
    # print
    #===========================================================================

    #===========================================================================
    # for i in range(0, len(words)):
    #    for j in range(0, len(words)):
    #        
    #        if j <= i:
    #            continue
    #        
    #        for iprime in range(i + 1, len(words)):
    #            for jprime in range(j + 1, len(words)):
    #         
    #                if cost.penalty(iprime, j) <= 0:
    #                    continue
    #                
    #                if iprime >= jprime:
    #                    continue
    #                
    #                if i >= jprime:
    #                    continue
    #                                    
    #                if cost.penalty(i, j) > cost.penalty(iprime, j) \
    #                    and not cost.penalty(i, jprime) > cost.penalty(iprime, jprime):
    #                        print "Fail", i, j, "vs", iprime, jprime
    #                        
    #                        print cost.penalty(i, j), cost.penalty(i, jprime)
    #                        print cost.penalty(iprime, j), cost.penalty(iprime, jprime)
    #===========================================================================
    
  
  #=============================================================================
  #  for j in range(0, len(words)):
  #      for i in range(0, len(words)):
  #          
  #          pen = penalty(i, j)
  #          print i, j, words[i:j], pen
  # 
  #=============================================================================
                        
