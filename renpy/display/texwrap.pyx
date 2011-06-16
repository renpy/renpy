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

# This code was originally public domain, as described below. I've 

import time
from textsupport cimport Glyph, SPLIT_INSTEAD, SPLIT_BEFORE, SPLIT_NONE

"""wordwrap.py -- public domain code from David Eppstein

http://www.ics.uci.edu/~eppstein/software.html

Break paragraphs into lines, attempting to avoid short lines.

We use the dynamic programming idea of Knuth-Plass to find the
optimal set of breaks according to a penalty function that
penalizes short lines quadratically; this can be done in linear
time via the OnlineConcaveMinima algorithm in SMAWK.py.

D. Eppstein, August 2005.


SMAWK.py

Totally monotone matrix searching algorithms.

The offline algorithm in ConcaveMinima is from Agarwal, Klawe, Moran,
Shor, and Wilbur, Geometric applications of a matrix searching algorithm,
Algorithmica 2, pp. 195-208 (1987).

The online algorithm in OnlineConcaveMinima is from Galil and Park,
A linear time algorithm for concave one-dimensional dynamic programming,
manuscript, 1989, which simplifies earlier work on the same problem
by Wilbur (J. Algorithms 1988) and Eppstein (J. Algorithms 1990).

D. Eppstein, March 2002, significantly revised August 2005
"""

import collections
times = collections.defaultdict(float)

cdef class Word(object):

    cdef Glyph g
    cdef int start_x
    cdef int end_x
    
    def __init__(self, Glyph g, int start_x, int end_x):
        self.start_x = start_x
        self.end_x = end_x
        self.g = g
        
            
cdef make_word_list(list glyphs):
    """
    Break the list of words into a list of glyphs, on the 
    split points.
    """
    
    cdef int start_x = 0, x = 0
    cdef Glyph g, start_g = None
    cdef list rv
    
    rv = [ ]

    if not glyphs:
        return rv
    
    for g in glyphs:

        if start_g is None:
            start_g = g
            continue

        if g.split == SPLIT_INSTEAD:
            rv.append(Word(start_g, start_x, x))
            
            start_x = x + <int> g.advance
            start_g = g

        elif g.split == SPLIT_BEFORE:

            rv.append(Word(start_g, start_x, x))
            
            start_x = x
            start_g = g
        
        x += <int> g.advance

    rv.append(Word(start_g, start_x, x))
        
    return rv

cdef class OnlineConcaveMinima:
    """
    Online concave minimization algorithm of Galil and Park.
    
    OnlineConcaveMinima(Matrix,initial) creates a sequence of pairs
    (self.value(j),self.index(j)), where
        self.value(0) = initial,
        self.value(j) = min { Matrix(i,j) | i < j } for j > 0,
    and where self.index(j) is the value of j that provides the minimum.
    Matrix(i,j) must be concave, in the same sense as for ConcaveMinima.
    
    We never call Matrix(i,j) until value(i) has already been computed,
    so that the Matrix function may examine previously computed values.
    Calling value(i) for an i that has not yet been computed forces
    the sequence to be continued until the desired index is reached.
    Calling iter(self) produces a sequence of (value,index) pairs.
    
    Matrix(i,j) should always return a value, rather than raising an
    exception, even for j larger than the range we expect to compute.
    If j is out of range, a suitable value to return that will not
    violate concavity is Matrix(i,j) = -i.  It will not work correctly
    to return a flag value such as None for large j, because the ties
    formed by the equalities among such flags may violate concavity.
    """

    cdef:
        list _values
        list _indices
        int _finished    
        object _matrix
        int _base
        int _tentative
    
        int first_width
        int rest_width
        bint subtitle
        list words
        int len_words
        
        int len_values
    
    def __init__(self, initial, list words, int first_width, int rest_width, bint subtitle):
        """Initialize a OnlineConcaveMinima object."""

        self.words = words
        self.len_words = len(words)
        self.first_width = first_width
        self.rest_width = rest_width
        self.subtitle = subtitle

        # State used by self.value(), self.index(), and iter(self)
        self._values = [ initial ]   # tentative solution values...
        self.len_values = 1
        self._indices = [ None ]     # ...and their indices
        self._finished = 0          # index of last non-tentative value

        # State used by the internal algorithm
        #
        # We allow self._values to be nonempty for indices > finished,
        # keeping invariant that
        # (1) self._values[i] = Matrix(self._indices[i], i),
        # (2) if the eventual correct value of self.index(i) < base,
        #     then self._values[i] is nonempty and correct.
        #
        # In addition, we keep a column index self._tentative, such that
        # (3) if i <= tentative, and the eventual correct value of
        #     self.index(i) <= finished, then self._values[i] is correct.
        #
        self._base = 0
        self._tentative = 0

    cdef dict concave_minima(self, list RowIndices, list ColIndices):
        """
        Search for the minimum value in each column of a matrix.
        The return value is a dictionary mapping ColIndices to pairs
        (value,rowindex). We break ties in favor of earlier rows.
        
        The matrix is defined implicitly as a function, passed
        as the third argument to this routine, where Matrix(i,j)
        gives the matrix value at row index i and column index j.
        The matrix must be concave, that is, satisfy the property
            Matrix(i,j) > Matrix(i',j) => Matrix(i,j') > Matrix(i',j')
        for every i<i' and j<j'; that is, in every submatrix of
        the input matrix, the positions of the column minima
        must be monotonically nondecreasing.
        
        The rows and columns of the matrix are labeled by the indices
        given in order by the first two arguments. In most applications,
        these arguments can simply be integer ranges.
        """
    
        cdef list stack
        cdef int len_stack
        cdef int len_colindices = len(ColIndices)
        cdef dict minima
        cdef int c, row, col, lastrow, r
        cdef int pen, min_pen, min_row
    
        start = time.time()
    
        # Base case of recursion
        if not ColIndices: 
            return {}
        
        # Reduce phase: make number of rows at most equal to number of cols
        stack = []
        len_stack = 0
        
        for r in RowIndices:
            while len_stack >= 1 and self.penalty(stack[-1], ColIndices[len_stack - 1]) > self.penalty(r, ColIndices[len_stack - 1]):
                stack.pop()
                len_stack -= 1
           
            if len_stack != len_colindices:
                stack.append(r)
                len_stack += 1
        
        RowIndices = stack
        
        # Recursive call to search for every odd column
        minima = self.concave_minima(RowIndices, ColIndices[1::2])
    
        # Go back and fill in the even rows
        r = 0

        for c in range(0, len_colindices ,2):
            
            col = ColIndices[c]
            row = RowIndices[r]
            
            if c == len_colindices - 1:
                lastrow = RowIndices[-1]
            else:
                lastrow = minima[ColIndices[c+1]][1]
            
            min_pen = self.penalty(row, col)
            min_row = row

            while row != lastrow:
                r += 1
                row = RowIndices[r]

                pen = self.penalty(row, col)
                if pen < min_pen:
                    min_row = row
                    min_pen = pen

            minima[col] = (min_pen, min_row)
    
        times["minima"] += time.time() - start
    
        return minima
    
    cdef int value(self, int j):
        """Return min { Matrix(i,j) | i < j }."""
        while self._finished < j:
            self._advance()
        return self._values[j]

    cdef int index(self, int j):
        """Return argmin { Matrix(i,j) | i < j }."""
        while self._finished < j:
            self._advance()
        return self._indices[j]

    cdef _advance(self):
        cdef int i
                
        """Finish another value,index pair."""
        # First case: we have already advanced past the previous tentative
        # value.  We make a new tentative value by applying ConcaveMinima
        # to the largest square submatrix that fits under the base.
        i = self._finished + 1
        if i > self._tentative:
            rows = range(self._base,self._finished+1)
            
            self._tentative = self._finished+len(rows)
            
            cols = range(self._finished+1,self._tentative+1)
            
            minima = self.concave_minima(rows, cols)
            
            for col in cols:
                val, idx = minima[col]
            
                if col >= self.len_values:
                    
                    self._values.append(val)
                    self._indices.append(idx)
                    self.len_values += 1                

                elif val < self._values[col]:
                    self._values[col] = val
                    self._indices[col] = idx

            self._finished = i
            return
        
        # Second case: the new column minimum is on the diagonal.
        # All subsequent ones will be at least as low,
        # so we can clear out all our work from higher rows.
        # As in the fourth case, the loss of tentative is
        # amortized against the increase in base.
        diag = self.penalty(i-1,i)
        if diag < self._values[i]:
            self._values[i] = diag
            self._indices[i] = self._base = i-1
            self._tentative = self._finished = i
            return
        
        # Third case: row i-1 does not supply a column minimum in
        # any column up to tentative. We simply advance finished
        # while maintaining the invariant.
        if self.penalty(i-1,self._tentative) >= self._values[self._tentative]:
            self._finished = i
            return
        
        # Fourth and final case: a new column minimum at self._tentative.
        # This allows us to make progress by incorporating rows
        # prior to finished into the base.  The base invariant holds
        # because these rows cannot supply any later column minima.
        # The work done when we last advanced tentative (and undone by
        # this step) can be amortized against the increase in base.
        self._base = i-1
        self._tentative = self._finished = i
        return

    cdef int penalty(self, int i, int j):
        
        cdef int total
        cdef int lw
        cdef int width
        cdef Word word_i, word_j
        
        if j > self.len_words:
            return -i
        
        # Figure out the length of the line.
        if i == 0:
            lw = self.first_width
        else:
            lw = self.rest_width
        
        # The total cost, includes the cost for the new line.
        total = self.value(i) + 100000

        # The width of the current words.
        word_i = self.words[i]
        word_j = self.words[j-1]
        width = word_j.end_x - word_i.start_x
        
        # Figure out penalties to give.        
        if width > lw:
            total += 100000 * (width - lw)

        elif j < self.len_words or self.subtitle:
            total += (lw - width) ** 2
           
        # This is more for testing than anything.
        if i >= j:
            return 0
            
        return total

cdef int word_width(list words, int i, int j):

    cdef int k
    cdef Word w
    cdef int rv = 0
    
    for k from i <= k < j:
        w = words[k]
        rv += w.width

        if k != i:
            rv += w.not_first

    return rv


def linebreak_tex(list glyphs, int first_width, int rest_width, bint subtitle):    
    cdef Word w
    cdef Glyph g
    cdef list words
    cdef int i, start, pos
    cdef OnlineConcaveMinima cost

    times.clear()
    
    words = make_word_list(glyphs)        

    cost = OnlineConcaveMinima(0, words, first_width, rest_width, subtitle)
    pos = len(words)

    while pos:
        
        start = cost.index(pos)

        for i from start + 1 <= i < pos:
            w = words[i]
            w.g.split = SPLIT_NONE
        
        pos = start

    for k, v in times.iteritems():
        print k, v * 1000

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
                        
