import os
import subprocess
import sys

import renpy.editor

class Editor(renpy.editor.Editor):

    has_projects = True

    def get_code(self):
        """
        Returns the path to the code executable, if None.
        """

        DIR = os.path.abspath(os.path.dirname(__file__))

        if renpy.windows:
            code = "Code.exe"
        elif renpy.macintosh:
            DIR = os.path.abspath("/Applications")
            code = os.path.join(DIR, "Visual Studio Code.app", "Contents", "Resources", "app", "bin", "code")
        else:
            code = "code"

        return code

    def open(self, filename, line=None, **kwargs):
        if line:
            filename = "{}:{}".format(filename, line)
        self.args.append(filename)

    def open_project(self, project):
        if renpy.windows:
            project = '"{}"'.format(project)
        elif renpy.macintosh:
            project = project.replace(' ', '\ ')
        self.args.append(project)

    def begin(self, new_window=False, **kwargs):
        self.args = [ ]

    def end(self, **kwargs):
        self.args.reverse()

        if renpy.macintosh:
            code = self.get_code()
            args = [ code ] + self.args
            args = [ renpy.exports.fsencode(i) for i in args ]
            subprocess.Popen(args)
        else:
            args = self.args
            args = [ renpy.exports.fsencode(i) for i in args ]
            subprocess.call(["code", "-g", args], shell=True)

def main():
    e = Editor()
    e.begin()

    for i in sys.argv[1:]:
        e.open(i)

    e.end()

if __name__ == "__main__":
    main()
