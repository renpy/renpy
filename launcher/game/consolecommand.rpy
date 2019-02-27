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
                nl = "\n"
                prefix = "#!/bin/bash"
            elif renpy.windows:
                fn = "console.bat"
                nl = "\r\n"
                prefix = "@echo off"
            else:
                fn = "console.sh"
                nl = "\n"
                prefix = "#!/bin/bash"


            self.fn = project.current.temp_filename(fn)
            self.f = open(self.fn, "wb")
            self.nl = nl


            self.f.write(renpy.fsencode(prefix) + nl)

        def add(self, *args):
            """
            Adds a command to be run.
            """

            args = [ '"{}"'.format(renpy.fsencode(i)) for i in args]
            self.f.write(" ".join(args) + self.nl)

        def run(self):
            """
            Runs the queued up commands.
            """

            if renpy.windows:
                self.add("pause")
            elif renpy.linux:
                self.add("echo", "Press enter to close this window...")
                self.add("read")

            self.f.close()
            os.chmod(self.fn, 0o755)

            if renpy.windows:
                subprocess.Popen([ renpy.fsencode(self.fn) ], shell=True)
            elif renpy.macintosh:
                subprocess.Popen([ "open", "-a", "Terminal", renpy.fsencode(self.fn) ])
            else:
                subprocess.Popen([ "x-terminal-emulator", "-e", renpy.fsencode(self.fn) ])

            interface.interaction(_("INFORMATION"), _("The command is being run in a new operating system console window."), pause=2.5)
