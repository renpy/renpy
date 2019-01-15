# Copyright 2004-2019 Tom Rothamel <pytom@bishoujo.us>
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

init -1 python in util:
    import os

    def listdir(d):
        """
        Returns a list of files and directories in `d` that are accessible with
        the filesystem encoding.
        """

        try:
            d = renpy.fsdecode(d)

            if not os.path.isdir(d):
                return [ ]

            return [ i for i in os.listdir(d) if isinstance(i, unicode) ]

        except:
            return [ ]

    def walk(directory, base=None):
        """
        Walks through the directories and files underneath `directory`,
        yielding (name, isdir) tuples. The names are given relative to
        `base`, which defaults to `directory` if None.
        """

        directory = renpy.fsdecode(directory)

        if base is None:
            base = directory
        else:
            base = renpy.fsdecode(base)

        for subdir, directories, files in os.walk(directory):
            for fn in directories:
                if not isinstance(fn, unicode):
                    continue

                fullfn = os.path.join(subdir, fn)
                relfn = os.path.relpath(fullfn, base)

                relfn = relfn.replace("\\", "/")

                yield relfn, True

            for fn in files:
                if not isinstance(fn, unicode):
                    continue

                fullfn = os.path.join(subdir, fn)
                relfn = os.path.relpath(fullfn, base)

                relfn = relfn.replace("\\", "/")

                yield relfn, False

