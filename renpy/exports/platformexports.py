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

from __future__ import division, absolute_import, with_statement, print_function, unicode_literals # type: ignore
from renpy.compat import PY2, basestring, bchr, bord, chr, open, pystr, range, round, str, tobytes, unicode # *

import renpy
from renpy.exports.commonexports import renpy_pure

@renpy_pure
def variant(name):
    """
    :doc: screens

    Returns true if `name` is a screen variant that corresponds to the
    context in which Ren'Py is currently executing. See :ref:`screen-variants`
    for more details. This function can be used as the condition in an
    if statement to switch behavior based on the selected screen variant.

    `name` can also be a list of variants, in which case this function
    returns True if any of the variants would.
    """

    if isinstance(name, basestring):
        return name in renpy.config.variants
    else:
        for n in name:
            if n in renpy.config.variants:
                return True

        return False


def vibrate(duration):
    """
    :doc: other

    Causes the device to vibrate for `duration` seconds. Currently, this
    is only supported on Android.
    """

    if duration < 0.01:
        duration = 0.01

    if renpy.android:
        import android # @UnresolvedImport
        android.vibrate(duration)
