# Copyright 2014-2026 Tom Rothamel <pytom@bishoujo.us>
# Copyright 2014 Patrick Dawson <pat@dw.is>
#
# This software is provided 'as-is', without any express or implied
# warranty.  In no event will the authors be held liable for any damages
# arising from the use of this software.
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely, subject to the following restrictions:
#
# 1. The origin of this software must not be misrepresented; you must not
#    claim that you wrote the original software. If you use this software
#    in a product, an acknowledgment in the product documentation would be
#    appreciated but is not required.
# 2. Altered source versions must be plainly marked as such, and must not be
#    misrepresented as being the original software.
# 3. This notice may not be removed or altered from any source distribution.

import collections

def flatten(*args):
    if len(args) == 1:
        return args[0]
    else:
        return args

cdef class Rect:

    def __init__(self, *args):

        cdef int x, y, w, h
        cdef int len_args
        cdef Rect rect

        len_args = len(args)

        if len_args == 1 and isinstance(args[0], Rect):
            rect = args[0]
            x = rect.x
            y = rect.y
            w = rect.w
            h = rect.h

        elif len_args == 1 and len(args[0]) == 4:
            x, y, w, h = args[0]

        elif len_args == 1 and len(args[0]) == 2:
            x, y = args[0]
            w = 0
            h = 0

        elif len_args == 2:
            x, y = args[0]
            w, h = args[1]

        elif len_args == 4:
            x, y, w, h = args

        else:
            raise TypeError("Argument must be a rect style object.")

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __reduce__(self):
        return (Rect, (self.x, self.y, self.w, self.h))

    def __repr__(self):
        return "<rect(%d, %d, %d, %d)>" % (self.x, self.y, self.w, self.h)

    def __len__(self):
        return 4

    def __iter__(self):
        return iter((self.x, self.y, self.w, self.h))

    def __richcmp__(Rect a, b, int op):
        if not isinstance(b, Rect):
            b = Rect(b)
        if op == 2:
            return a.x == b.x and a.y == b.y and a.w == b.w and a.h == b.h

    def __getitem__(self, key):
        return (self.x, self.y, self.w, self.h)[key]

    def __setitem__(self, key, val):
        if key == 0:
            self.x = val
        elif key == 1:
            self.y = val
        elif key == 2:
            self.w = val
        elif key == 3:
            self.h = val
        else:
            raise IndexError(key)

    property left:
        def __get__(self):
            return self.x
        def __set__(self, val):
            self.x = val

    property top:
        def __get__(self):
            return self.y
        def __set__(self, val):
            self.y = val

    property width:
        def __get__(self):
            return self.w
        def __set__(self, val):
            self.w = val

    property height:
        def __get__(self):
            return self.h
        def __set__(self, val):
            self.h = val

    property right:
        def __get__(self):
            return self.x + self.width
        def __set__(self, val):
            self.x += val - self.right

    property bottom:
        def __get__(self):
            return self.y + self.height
        def __set__(self, val):
            self.y += val - self.bottom

    property size:
        def __get__(self):
            return (self.w, self.h)
        def __set__(self, val):
            self.w, self.h = val

    property topleft:
        def __get__(self):
            return (self.left, self.top)
        def __set__(self, val):
            self.left, self.top = val

    property topright:
        def __get__(self):
            return (self.right, self.top)
        def __set__(self, val):
            self.right, self.top = val

    property bottomright:
        def __get__(self):
            return (self.right, self.bottom)
        def __set__(self, val):
            self.right, self.bottom = val

    property bottomleft:
        def __get__(self):
            return (self.left, self.bottom)
        def __set__(self, val):
            self.left, self.bottom = val

    property centerx:
        def __get__(self):
            return self.x + (self.w / 2)
        def __set__(self, val):
            self.x += val - self.centerx

    property centery:
        def __get__(self):
            return self.y + (self.h / 2)
        def __set__(self, val):
            self.y += val - self.centery

    property center:
        def __get__(self):
            return (self.centerx, self.centery)
        def __set__(self, val):
            self.centerx, self.centery = val

    property midtop:
        def __get__(self):
            return (self.centerx, self.top)
        def __set__(self, val):
            self.centerx, self.top = val

    property midleft:
        def __get__(self):
            return (self.left, self.centery)
        def __set__(self, val):
            self.left, self.centery = val

    property midbottom:
        def __get__(self):
            return (self.centerx, self.bottom)
        def __set__(self, val):
            self.centerx, self.bottom = val

    property midright:
        def __get__(self):
            return (self.right, self.centery)
        def __set__(self, val):
            self.right, self.centery = val

    def copy(self):
        return Rect(self)

    def move(self, *args):
        r = self.copy()
        r.move_ip(*args)
        return r

    def move_ip(self, *args):
        x, y = flatten(args)
        self.x += x
        self.y += y

    def inflate(self, *args):
        r = self.copy()
        r.inflate_ip(*args)
        return r

    def inflate_ip(self, *args):
        x, y = flatten(args)
        c = self.center
        self.w += x
        self.h += y
        self.center = c

    def clamp(self, other):
        r = self.copy()
        r.clamp_ip(other)
        return r

    def clamp_ip(self, other):
        if not isinstance(other, Rect):
            other = Rect(other)

        if self.w > other.w or self.h > other.h:
            self.center = other.center
        else:
            if self.left < other.left:
                self.left = other.left
            elif self.right > other.right:
                self.right = other.right
            if self.top < other.top:
                self.top = other.top
            elif self.bottom > other.bottom:
                self.bottom = other.bottom

    def clip(self, other, y=None, w=None, h=None):
        if type(other) == int:
            other = Rect(other, y, w, h)

        if not isinstance(other, Rect):
            other = Rect(other)

        if not self.colliderect(other):
            return Rect(0,0,0,0)

        r = self.copy()

        # Remember that (0,0) is the top left.
        if r.left < other.left:
            d = other.left - r.left
            r.left += d
            r.width -= d
        if r.right > other.right:
            d = r.right - other.right
            r.width -=d
        if r.top < other.top:
            d = other.top - r.top
            r.top += d
            r.height -= d
        if r.bottom > other.bottom:
            d = r.bottom - other.bottom
            r.height -= d

        return r

    def union(self, other):
        r = self.copy()
        r.union_ip(other)
        return r

    def union_ip(self, other):
        if not isinstance(other, Rect):
            other = Rect(other)

        x = min(self.x, other.x)
        y = min(self.y, other.y)
        self.w = max(self.right, other.right) - x
        self.h = max(self.bottom, other.bottom) - y
        self.x = x
        self.y = y

    def unionall(self, other_seq):
        r = self.copy()
        r.unionall_ip(other_seq)
        return r

    def unionall_ip(self, other_seq):
        for other in other_seq:
            self.union_ip(other)

    def fit(self, other):
        if not isinstance(other, Rect):
            other = Rect(other)

        # Not sure if this is entirely correct. Docs and tests are ambiguous.
        r = self.copy()
        r.topleft = other.topleft
        w_ratio = other.w / float(r.w)
        h_ratio = other.h / float(r.h)
        factor = min(w_ratio, h_ratio)
        r.w *= factor
        r.h *= factor
        return r

    def normalize(self):
        if self.w < 0:
            self.x += self.w
            self.w = -self.w
        if self.h < 0:
            self.y += self.h
            self.h = -self.h

    def contains(self, other):
        if not isinstance(other, Rect):
            other = Rect(other)

        return other.x >= self.x and other.right <= self.right and \
               other.y >= self.y and other.bottom <= self.bottom and \
               other.left < self.right and other.top < self.bottom

    def collidepoint(self, x, y=None):
        if type(x) == tuple:
            x, y = x
        return x >= self.x and y >= self.y and \
               x < self.right and y < self.bottom

    def colliderect(self, other):
        if not isinstance(other, Rect):
            other = Rect(other)

        return self.left < other.right and self.top < other.bottom and \
               self.right > other.left and self.bottom > other.top

    def collidelist(self, other_list):
        for n, other in zip(range(len(other_list)), other_list):
            if self.colliderect(other):
                return n
        return -1

    def collidelistall(self, other_list):
        ret = []
        for n, other in zip(range(len(other_list)), other_list):
            if self.colliderect(other):
                ret.append(n)
        return ret

    def collidedict(self, other_dict, rects_values=0):
        # What is rects_values supposed to do? Not in docs.
        for key, val in other_dict.items():
            if self.colliderect(val):
                return key, val
        return None

    def collidedictall(self, other_dict, rects_values=0):
        ret = []
        for key, val in other_dict.items():
            if self.colliderect(val):
                ret.append((key,val))
        return ret


cdef int to_sdl_rect(rectlike, SDL_Rect *rect, argname=None) except -1:
    """
    Converts `rectlike` to the SDL_Rect `rect`.

    `rectlike` may be a Rect or a (x, y, w, h) tuple.
    """

    cdef int x, y, w, h
    cdef Rect rl

    try:
        if isinstance(rectlike, Rect):
            rl = rectlike

            rect.x = rl.x
            rect.y = rl.y
            rect.w = rl.w
            rect.h = rl.h

            return 0

        elif len(rectlike) == 4:
            rect.x, rect.y, rect.w, rect.h = rectlike
            return 0

        elif len(rectlike) == 2:
            rect.x, rect.y = rectlike
            rect.w, rect.h = rectlike
            return 0

    except:
        pass

    if argname:
        raise TypeError("Argument {} must be a rect style object.".format(argname))
    else:
        raise TypeError("Argument must be a rect style object.")
