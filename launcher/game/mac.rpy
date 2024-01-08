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

init python hide:
    import os

    macapp = os.path.join(config.renpy_base, "renpy.app/Contents/MacOS")
    maclib = os.path.join(config.renpy_base, distribute.py("lib/py{major}-mac-universal"))

    if os.path.exists(maclib):

        for fn in os.listdir(maclib):
            try:

                fn = os.path.join(maclib, fn)

                if fn.endswith(".macho"):
                    nfn = fn.rpartition(".")[0]

                    with open(fn, "rb") as f:
                        f.read(5)
                        data = f.read()

                    with open(nfn, "wb") as f:
                        f.write(data)

                    os.chmod(nfn, 0o755)
                    os.unlink(fn)

            except Exception:
                pass


        macpython = os.path.join(maclib, "python")

        if sys.executable.startswith(macapp) and os.path.exists(macpython):
            sys.executable = macpython
