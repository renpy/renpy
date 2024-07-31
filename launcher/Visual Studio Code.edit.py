import os
import subprocess
import sys

import renpy

class Editor(renpy.editor.Editor):

    has_projects = True

    system = __file__.endswith(" (System).edit.py")

    def get_code(self):
        """
        Returns the path to the code executable.
        """

        if self.system:

            if "RENPY_VSCODE" in os.environ:
                return os.environ["RENPY_VSCODE"]

            if renpy.windows:
                return "code.cmd"

            if renpy.macintosh and os.path.exists("/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"):
                return "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"

            return "code"

        else:

            RENPY_VSCODE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vscode"))

            if renpy.windows:
                code = os.path.join(RENPY_VSCODE, "VSCode-win32-x64", "bin", "code.cmd")
            elif renpy.macintosh:
                code = os.path.join(RENPY_VSCODE, "Visual Studio Code.app", "Contents", "Resources", "app", "bin", "code")
            elif renpy.linux:
                if renpy.arch == "aarch64":
                    arch = "arm64"
                elif renpy.arch == "armv7l":
                    arch = "arm"
                else:
                    arch = "x64"

                code = os.path.join(RENPY_VSCODE, "VSCode-linux-" + arch, "bin", "code")
            else:
                code = "code"

            return code

    def open(self, filename, line=None, **kwargs):
        if line:
            filename = "{}:{}".format(filename, line)
        self.args.append(filename)

    def open_project(self, project):
        self.args.append(project)

    def begin(self, new_window=False, **kwargs):
        self.args = [ ]

    def end(self, **kwargs):
        self.args.reverse()

        code = self.get_code()
        if self.system or not renpy.linux:
            args = [ code, "-g" ] + self.args
        else:
            args = [ code, "--no-sandbox", "-g" ] + self.args

        args = [ renpy.exports.fsencode(i) for i in args ]

        if renpy.windows:
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(args, creationflags=CREATE_NO_WINDOW)
        else:
            subprocess.Popen(args)



def main():
    e = Editor()
    e.begin()

    for i in sys.argv[1:]:
        e.open(i)

    e.end()

if __name__ == "__main__":
    main()
