import subprocess

import renpy.editor

class Editor(renpy.editor.Editor):

    def open(self, filename, line=None, **kwargs):
        filename = renpy.exports.fsencode(filename)
        address = filename if line is None else "%s:%d" % (filename, line)
        subprocess.call(["code", "-g", address], shell=True)