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


init python:


    class FileTail(object):

        def __init__(self, filename, lines=8):
            self.filename = filename
            self.text = ""
            self.lines = lines

        def update(self):

            def filter_text(s):
                if "Unknown chunk type '200'" in s:
                    return False
                return True

            try:
                with open(self.filename) as f:
                    text = f.read()

                    try:
                        text = renpy.fsdecode(text)
                    except Exception:
                        text = text.decode("latin-1")

                    text = text.strip()
                    text = text.split("\n")

                    newtext = [ ]
                    for l in text:

                        if "\r" in l:
                            _head, _sep, l = l.rpartition("\r")

                        if not filter_text(l):
                            continue

                        while l:
                            newtext.append(l[:100])
                            l = l[100:]

                    text = newtext
                    text = text[-self.lines:]
                    text = "\n".join(text)

                    if text != self.text:
                        self.text = text
                        renpy.restart_interaction()

            except Exception:
                pass
