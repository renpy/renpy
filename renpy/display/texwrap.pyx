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

from textsupport cimport Glyph, SPLIT_INSTEAD, SPLIT_NONE

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

cdef class Word(object):
    
    cdef public list glyphs
        
    # The width of this, always.
    cdef public short width

    # Additional width iff this is not the first word in a line.
    cdef public short not_first

    def __init__(self, list glyphs):
        cdef Glyph g
        
        self.glyphs = glyphs
        
        self.width = 0 
        self.not_first = 0
        
        if not glyphs:
            return
                
        for g in glyphs:
            
            if g.split == SPLIT_INSTEAD:
                self.not_first += <short> g.advance
            else:            
                self.width += <short> g.advance
              
    def __repr__(self):
        
        rv = u""
        
        for g in self.glyphs:
            rv += unichr(g.character)
            
        return "<Word: {!r}>".format(rv)
      
            
def make_word_list(list glyphs):
    """
    Break the list of words into a list of glyphs, on the 
    split points.
    """
    
    cdef Glyph g
    cdef list rv
    cdef list line
    
    rv = [ ]
    line = [ ]
    
    for g in glyphs:

        if line and g.split:
            rv.append(Word(line))
            line = [ ]
            
        line.append(g)
            
    if line:
        rv.append(Word(line))
        
    return rv
        
            


def ConcaveMinima(RowIndices,ColIndices,Matrix):
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

    # Base case of recursion
    if not ColIndices: return {}
    
    # Reduce phase: make number of rows at most equal to number of cols
    stack = []
    for r in RowIndices:
        while len(stack) >= 1 and \
                Matrix(stack[-1], ColIndices[len(stack)-1]) \
                > Matrix(r, ColIndices[len(stack)-1]):
            stack.pop()
        if len(stack) != len(ColIndices):
            stack.append(r)
    RowIndices = stack
    
    # Recursive call to search for every odd column
    minima = ConcaveMinima(RowIndices,
                [ColIndices[i] for i in xrange(1,len(ColIndices),2)],
                Matrix)

    # Go back and fill in the even rows
    r = 0
    for c in xrange(0,len(ColIndices),2):
        col = ColIndices[c]
        row = RowIndices[r]
        if c == len(ColIndices) - 1:
            lastrow = RowIndices[-1]
        else:
            lastrow = minima[ColIndices[c+1]][1]
        pair = (Matrix(row,col),row)
        while row != lastrow:
            r += 1
            row = RowIndices[r]
            pair = min(pair,(Matrix(row,col),row))
        minima[col] = pair

    return minima

class OnlineConcaveMinima:
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
    
    def __init__(self,Matrix,initial):
        """Initialize a OnlineConcaveMinima object."""

        # State used by self.value(), self.index(), and iter(self)
        self._values = [initial]    # tentative solution values...
        self._indices = [None]      # ...and their indices
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
        self._matrix = Matrix
        self._base = 0
        self._tentative = 0

    def value(self,j):
        """Return min { Matrix(i,j) | i < j }."""
        while self._finished < j:
            self._advance()
        return self._values[j]

    def index(self,j):
        """Return argmin { Matrix(i,j) | i < j }."""
        while self._finished < j:
            self._advance()
        return self._indices[j]

    def _advance(self):
        """Finish another value,index pair."""
        # First case: we have already advanced past the previous tentative
        # value.  We make a new tentative value by applying ConcaveMinima
        # to the largest square submatrix that fits under the base.
        i = self._finished + 1
        if i > self._tentative:
            rows = range(self._base,self._finished+1)
            self._tentative = self._finished+len(rows)
            cols = range(self._finished+1,self._tentative+1)
            minima = ConcaveMinima(rows,cols,self._matrix)
            for col in cols:
                if col >= len(self._values):
                    self._values.append(minima[col][0])
                    self._indices.append(minima[col][1])
                elif minima[col][0] < self._values[col]:
                    self._values[col],self._indices[col] = minima[col]
            self._finished = i
            return
        
        # Second case: the new column minimum is on the diagonal.
        # All subsequent ones will be at least as low,
        # so we can clear out all our work from higher rows.
        # As in the fourth case, the loss of tentative is
        # amortized against the increase in base.
        diag = self._matrix(i-1,i)
        if diag < self._values[i]:
            self._values[i] = diag
            self._indices[i] = self._base = i-1
            self._tentative = self._finished = i
            return
        
        # Third case: row i-1 does not supply a column minimum in
        # any column up to tentative. We simply advance finished
        # while maintaining the invariant.
        if self._matrix(i-1,self._tentative) >= self._values[self._tentative]:
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


def texwrap(lines,                 # lines of string or unicode to be wrapped
         target = 76,           # maximum length of a wrapped line
         longlast = False,      # True if last line should be as long as others
         frenchspacing = False, # Single space instead of double after periods
         measure = len,         # how to measure the length of a word
         overpenalty = 1000,    # penalize long lines by overpen*(len-target)
         nlinepenalty = 1000,   # penalize more lines than optimal
         onewordpenalty = 25,   # penalize really short last line
         hyphenpenalty = 25):   # penalize breaking hyphenated words
    """Wrap the given text, returning a sequence of lines."""

    # Make sequence of tuples (word, spacing if no break, cum.measure).
    words = []
    total = 0
    spacings = [0, measure(' '), measure('  ')]
    for line in lines:
        for hyphenword in line.split():
            if words:
                total += spacings[words[-1][1]]
            parts = hyphenword.split('-')
            for word in parts[:-1]:
                word += '-'
                total += measure(word)
                words.append((word,0,total))
            word = parts[-1]
            total += measure(word)
            spacing = 1
            if word.endswith('.') and (len(hyphenword) > 2 or
                                       not hyphenword[0].isupper()):
                spacing = 2 - frenchspacing
            words.append((word,spacing,total))

    # Define penalty function for breaking on line words[i:j]
    # Below this definition we will set up cost[i] to be the
    # total penalty of all lines up to a break prior to word i.
    def penalty(i,j):
        if j > len(words): return -i    # concave flag for out of bounds
        total = cost.value(i) + nlinepenalty
        prevmeasure = i and words[i-1][2]
        linemeasure = words[j-1][2] - prevmeasure

        if linemeasure > target:
            total += overpenalty * (linemeasure - target)
        elif j < len(words) or longlast:
            total += (target - linemeasure)**2
        elif i == j-1:
            total += onewordpenalty
        if not words[j-1][1]:
            total += hyphenpenalty
        
        if i >= j:
            return 0

        return total

    # Apply concave minima algorithm and backtrack to form lines
    cost = OnlineConcaveMinima(penalty,0)
    pos = len(words)
    lines = []
    while pos:
        breakpoint = cost.index(pos)
        line = []
        for i in range(breakpoint,pos):
            line.append(words[i][0])
            if i < pos-1 and words[i][1]:
                line.append(' '*words[i][1])
        lines.append(''.join(line))
        pos = breakpoint

    # lines.reverse()
    # return lines
    
    for i in range(0, len(words)):
        for j in range(0, len(words)):
            print "{:d}x{:d} {:d}  ".format(i, j, penalty(i, j)),
            
        print 

    if True:
        return
    
    for i in range(0, len(words)):
        for j in range(0, len(words)):
            
            print i, j
            
            if j <= i:
                continue
            
            for iprime in range(i + 1, len(words)):
                for jprime in range(j + 1, len(words)):
                    
                    if iprime >= jprime:
                        continue
                    
                    if i >= jprime:
                        continue
                                        
                    if penalty(i, j) > penalty(iprime, j) \
                        and not penalty(i, jprime) > penalty(iprime, jprime):
                            print "Double Fail", i, j, "vs", iprime, jprime
                            
                            print penalty(i, j), penalty(i, jprime)
                            print penalty(iprime, j), penalty(iprime, jprime)


def linebreak_tex(glyphs, first_width, rest_width, bint subtitle):    
    cdef Word w
    cdef Glyph g
    cdef list words
    cdef int i

    words = make_word_list(glyphs)        
    len_words = len(words)

    def word_width(i, j):

        cdef Word w
        cdef int rv = 0
        
        for w in words[i:j]:
            rv += w.width
            rv += w.not_first

        # print words[i:j], rv / 10.0

        return rv

    def penalty(i, j):
        
        if j > len_words:
            return -i
        
        # Figure out the lenght of the line.
        if i == 0:
            lw = first_width
        else:
            lw = rest_width
        
        # The total cost, includes the cost for the new line.
        total = cost.value(i) + 100000

        # The width of the current words.
        width = word_width(i, j)
        
        # Figure out penalties to give.        
        if width > lw:
            total += 100000 * (width - lw)

        elif j < len_words or subtitle:
            total += (lw - width) ** 2
            
        # This is more for testing than anything.
        if i >= j:
            return 0
            
        return total
        
    cost = OnlineConcaveMinima(penalty, 0)
    pos = len_words

    while pos:
        
        start = cost.index(pos)

        for i from start + 1 <= i < pos:

            w = words[i]
            if w.glyphs:
                g = w.glyphs[0]
                g.split = SPLIT_NONE
        
        pos = start

    #===========================================================================
    # for i in range(0, len(words)):
    #    for j in range(0, len(words)):
    #        print "{:d}x{:d} {:d}  ".format(i, j, penalty(i, j)),
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

    IF 0:

         for i in range(0, len(words)):
            for j in range(0, len(words)):
                
                if j <= i:
                    continue
                
                for iprime in range(i + 1, len(words)):
                    for jprime in range(j + 1, len(words)):
                 
                        if penalty(iprime, j) <= 0:
                            continue
                        
                        if iprime >= jprime:
                            continue
                        
                        if i >= jprime:
                            continue
                                            
                        if penalty(i, j) > penalty(iprime, j) \
                            and not penalty(i, jprime) > penalty(iprime, jprime):
                                print "Fail", i, j, "vs", iprime, jprime
                                
                                print penalty(i, j), penalty(i, jprime)
                                print penalty(iprime, j), penalty(iprime, jprime)
    
  
  #=============================================================================
  #  for j in range(0, len(words)):
  #      for i in range(0, len(words)):
  #          
  #          pen = penalty(i, j)
  #          print i, j, words[i:j], pen
  # 
  #=============================================================================
                        
