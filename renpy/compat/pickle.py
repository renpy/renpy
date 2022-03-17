# Copyright 2004-2022 Tom Rothamel <pytom@bishoujo.us>
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
import pickle
import io

# Protocol 2 can be loaded on Python 2 and Python 3.
PROTOCOL = 2

if PY2:

    import cPickle # type: ignore

    def load(f): # type: ignore
        if renpy.config.use_cpickle:
            return cPickle.load(f)
        else:
            return pickle.load(f)

    def loads(s): # type: ignore
        if renpy.config.use_cpickle:
            return cPickle.loads(s)
        else:
            return pickle.loads(s)

    def dump(o, f, highest=False):
        if renpy.config.use_cpickle:
            cPickle.dump(o, f, PROTOCOL)
        else:
            pickle.dump(o, f,PROTOCOL)

    def dumps(o, highest=False): # type: ignore
        if renpy.config.use_cpickle:
            return cPickle.dumps(o, PROTOCOL)
        else:
            return pickle.dumps(o, PROTOCOL)

else:

    import functools
    import datetime

    def make_datetime(cls, *args, **kwargs):
        """
        Makes a datetime.date, datetime.time, or datetime.datetime object
        from a surrogateescaped str. This is used when unpickling a datetime
        object that was first created in Python 2.
        """

        if (len(args) == 1) and isinstance(args[0], str):
            data = args[0].encode("utf-8", "surrogateescape")
            return cls.__new__(cls, data.decode("latin-1"))

        return cls.__new__(cls, *args, **kwargs)

    class Unpickler(pickle.Unpickler):
        date = functools.partial(make_datetime, datetime.date)
        time = functools.partial(make_datetime, datetime.time)
        datetime = functools.partial(make_datetime, datetime.datetime)

        def find_class(self, module, name):
            if module == "datetime":
                if name == "date":
                    return self.date
                elif name == "time":
                    return self.time
                elif name == "datetime":
                    return self.datetime

            return super().find_class(module, name)

    def load(f):
        up = Unpickler(f, fix_imports=True, encoding="utf-8", errors="surrogateescape")
        return up.load()

    def loads(s):
        return load(io.BytesIO(s))

    def dump(o, f, highest=False):
        pickle.dump(o, f, pickle.HIGHEST_PROTOCOL if highest else PROTOCOL)

    def dumps(o, highest=False):
        return pickle.dumps(o, pickle.HIGHEST_PROTOCOL if highest else PROTOCOL)
