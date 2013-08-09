# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.


init python:

    class FileTail(object):

        def __init__(self, filename, lines=8):
            self.filename = filename
            self.text = ""
            self.lines = lines

        def update(self):

            try:
                with open(self.filename) as f:
                    text = f.read()
                    text = text.strip()
                    text = text.split("\n")
                    text = text[-self.lines:]
                    text = "\n".join(text)

                    if text != self.text:
                        self.text = text
                        renpy.restart_interaction()
            except:
                pass



