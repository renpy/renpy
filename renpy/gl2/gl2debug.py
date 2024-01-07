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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *



import renpy


def geometry(mesh, transform, width, height):
    """
    Debugs the drawing of geometry by applying `transform` to `mesh`, and
    then projecting it onto the screen.
    """

    points = mesh.get_points()
    triangles = mesh.get_triangles()

    l = ["Mesh:"]

    for a, b, c in triangles:
        l.append("{}-{}-{}".format(a, b, c))

    print(" ".join(l))

    sxlist = [ ]
    sylist = [ ]

    for i, p in enumerate(points):

        px, py, pz, pw = p
        tx, ty, tz, tw = transform.transform(px, py, pz, pw, components=4)

        dtx = tx / tw
        dty = ty / tw

        sx = width * (dtx + 1.0) / 2.0
        sy = height * (1.0 - dty) / 2.0

        print("{:3g}: {: >9.4f} {: >9.4f} {: >3.1f} {: >3.1f} | {: >9.6f} {: >9.6f} {:>3.1f} {:>3.1f} | {:> 9.4f} {:< 9.4f}".format(
            i,
            px, py, pz, pw,
            tx, ty, tz, tw,
            sx, sy))

        sxlist.append(sx)
        sylist.append(sy)

    if sxlist:
        minsx = min(sxlist)
        minsy = min(sylist)
        maxsx = max(sxlist)
        maxsy = max(sylist)

        print("     ({:> 9.4f}, {:< 9.4f}) - ({:> 9.4f}, {:< 9.4f})".format(minsx, minsy, maxsx, maxsy))
