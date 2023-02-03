# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
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

    class ConsoleCommand():
        """
        This runs a series of console commands in an OS-provided
        console window. This is done by creating a shell script
        or batch file as appropriate, then using an OS-approved
        method to run that file.
        """

        def __init__(self):

            if renpy.macintosh:
                fn = "console.command"
                nl = b"\n"
                prefix = "#!/bin/sh"
            elif renpy.windows:
                fn = "console.bat"
                nl = b"\r\n"
                prefix = "@echo off"
            else:
                fn = "console.sh"
                nl = b"\n"
                prefix = "#!/bin/bash"


            self.fn = project.current.temp_filename(fn)
            self.f = open(self.fn, "wb")
            self.nl = nl

            self.f.write(renpy.fsencode(prefix, force=True) + nl)

        def add(self, *args):
            """
            Adds a command to be run.
            """

            args = [ b'"' + renpy.fsencode(i, force=True) + b'"' for i in args]
            self.f.write(b" ".join(args) + self.nl)

        def write(self, *args):
            """
            Adds a command to be run.
            """

            args = [ renpy.fsencode(i, force=True) for i in args]
            self.f.write(b" ".join(args) + self.nl)

        def run(self):
            """
            Runs the queued up commands.
            """

            if renpy.windows:
                self.write("pause")
            elif renpy.linux:
                self.add("echo", "Press enter to close this window...")
                self.write("read")

            self.f.close()
            os.chmod(self.fn, 0o755)

            if renpy.linux:
                command = renpy.fsencode('"{}"'.format(self.fn.replace("\"", "\\\"")))
                subprocess.Popen([ "x-terminal-emulator", "-e", command ])
            else:
                command = renpy.fsencode(self.fn)
                os.startfile(command)

            interface.interaction(_("INFORMATION"), _("The command is being run in a new operating system console window."), pause=2.5)
