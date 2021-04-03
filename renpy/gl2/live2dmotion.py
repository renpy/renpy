# Copyright 2004-2021 Tom Rothamel <pytom@bishoujo.us>
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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals

import json
import renpy


class Linear(object):

    def __init__(self, x0, y0, x1, y1):
        self.duration = x1 - x0

        self.y0 = y0
        self.y1 = y1

    def get(self, t):
        done = t / self.duration
        return self.y0 + (self.y1 - self.y0) * done

    def wait(self, t):
        return 0


class Step(object):

    def __init__(self, x0, y0, x1, y1):
        self.duration = x1 - x0

        self.y0 = y0
        self.y1 = y1

    def get(self, t):
        return self.y0

    def wait(self, t):
        return max(self.duration - t, 0.0)


class InvStep(object):

    def __init__(self, x0, y0, x1, y1):
        self.duration = x1 - x0

        self.y0 = y0
        self.y1 = y1

    def get(self, t):
        return self.y1

    def wait(self, t):
        return max(self.duration - t, 0.0)


class Bezier(object):

    def __init__(self, x0, y0, x1, y1, x2, y2, x3, y3):
        self.duration = x3 - x0

        self.x0 = 0
        self.x1 = x1 - x0
        self.x2 = x2 - x0
        self.x3 = x3 - x0

        self.y0 = y0
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3

    def get(self, t):
        done = t / self.duration

        def lerp(a, b):
            return a + (b - a) * done

        p01 = lerp(self.y0, self.y1)
        p12 = lerp(self.y1, self.y2)
        p23 = lerp(self.y2, self.y3)

        p012 = lerp(p01, p12)
        p123 = lerp(p12, p23)

        return lerp(p012, p123)

    def wait(self, t):
        return 0


class Motion(object):

    def __init__(self, filename, fadein, fadeout):

        self.filename = filename

        with renpy.loader.load(filename) as f:
            j = json.load(f)

        self.duration = j["Meta"]["Duration"]
        self.curves = { }
        self.fades = { }

        for curve in j["Curves"]:
            target = curve["Target"]
            name = curve["Id"]
            s = curve["Segments"]

            x0 = s.pop(0)
            y0 = s.pop(0)

            segments = [ ]

            while s:

                kind = s.pop(0)

                if kind == 0:
                    x = s.pop(0)
                    y = s.pop(0)

                    segments.append(Linear(x0, y0, x, y))

                elif kind == 1:
                    x1 = s.pop(0)
                    y1 = s.pop(0)
                    x2 = s.pop(0)
                    y2 = s.pop(0)
                    x = s.pop(0)
                    y = s.pop(0)

                    segments.append(Bezier(x0, y0, x1, y1, x2, y2, x, y))

                elif kind == 2:
                    x = s.pop(0)
                    y = s.pop(0)

                    segments.append(Step(x0, y0, x, y))

                elif kind == 3:
                    x = s.pop(0)
                    y = s.pop(0)

                    segments.append(InvStep(x0, y0, x, y))

                else:
                    raise Exception("Unknown kind.")

                x0 = x
                y0 = y

            self.curves[target, name] = segments
            self.fades[target, name] = (
                curve.get("FadeInTime", fadein),
                curve.get("FadeOutTime", fadeout),
                )

    def get(self, st, fade_st, do_fade_in, do_fade_out):
        """
        Returns a dictionary where the keys are the type of parameter and the
        parameter name, and the values are the blend factor and value.
        """

        if st == self.duration:
            st = self.duration
        else:
            st = st % self.duration

        rv = { }

        for k, segments in self.curves.items():

            fadein, fadeout = self.fades[k]

            if not do_fade_in:
                fadein = 0.0

            if not do_fade_out:
                fadeout = 0.0

            factor = 1.0

            if st < fadein:
                factor = min(factor, st / fadein)

            if st > self.duration - fadeout:
                factor = min(factor, 1.0 - (st - (self.duration - fadeout)) / fadeout)

            if fade_st is not None:
                if fadeout > 0:
                    factor = min(factor, 1.0 - fade_st / fadeout)
                else:
                    factor = 0.0

            factor = max(factor, 0.0)

            t = st

            for i in segments:
                if t <= i.duration:
                    rv[k] = (factor, i.get(t))

                    break

                t -= i.duration

        return rv

    def wait(self, st, fade_st, do_fade_in, do_fade_out):
        """
        Returns how much time should pass until this displayable needs to be
        redrawn.
        """

        st = st % self.duration

        rv = 86400.0

        for k, segments in self.curves.items():

            fadeout = self.fades[k][1]

            if not do_fade_out:
                fadeout = 0

            factor = 1.0

            if st > self.duration - fadeout:
                factor = min(factor, 1.0 - (st - (self.duration - fadeout)) / fadeout)

            if fade_st is not None:
                if fadeout > 0:
                    factor = min(factor, 1.0 - fade_st / fadeout)
                else:
                    factor = 0.0

            factor = max(factor, 0.0)

            if factor == 0.0:
                continue

            t = st

            for i in segments:
                if t < i.duration:
                    rv = min(rv, i.wait(t))
                    break

                t -= i.duration

        if rv == 86400.0:
            rv = None

        return rv


class NullMotion(object):
    """
    A motion that is added by default,
    """

    duration = 1.0

    def get(self, st, fade_st, do_fade_in, do_fade_out):
        return { }

    def wait(self, st, fade_st, do_fade_in, do_fade_out):
        return max(1.0 - st, 0)
