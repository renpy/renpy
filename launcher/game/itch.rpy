# Copyright 2004-2017 Tom Rothamel <pytom@bishoujo.us>
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

    def find_itch_butler():

        import os

        if renpy.windows:
            rv = os.path.join(os.environ.get("APPDATA", ""), "Roaming", "itch", "bin", "butler.exe")

            if not os.path.exists(rv):
                rv = os.path.join(os.environ.get("APPDATA", ""), "itch", "bin", "butler.exe")

        elif renpy.macintosh:
            rv = os.path.join(os.environ.get("HOME", ""), "Library", "Application Support", "itch", "bin", "butler")
        else:
            rv = os.path.join(os.environ.get("HOME", ""), ".config", "itch", "bin", "butler")

        if not os.path.exists(rv):
            return None

        return rv

label itch:

    call build_update_dump


    python hide:

        build = project.current.dump["build"]

        destination = build["destination"]
        parent = os.path.dirname(project.current.path)
        destination = os.path.join(parent, destination)

        version = build["version"]

        if not os.path.exists(destination):
            interface.error(
                _("The built distributions could not be found. Please choose 'Build' and try again."),
                label="build_distributions"
                )

        # A list of full filename, channel tuples.
        files = [ ]

        for fn in os.listdir(destination):
            fn = os.path.join(destination, fn)

            if fn.endswith("-all.zip"):
                channel = "all"

            elif fn.endswith("-win.zip"):
                channel = "win"

            elif fn.endswith("-mac.zip"):
                channel = "mac"

# Butler doesn't seem to support .bz2s yet.

#             elif fn.endswith("-linux.tar.bz2"):
#                 channel = "linux"

            else:
                continue

            files.append((fn, channel))

        if not os.path.exists(destination):
            interface.error(
                _("No uploadable files were found. Please choose 'Build' and try again."),
                label="build_distributions"
                )

        butler = find_itch_butler()

        if not butler:
            interface.error(
                _("The butler program was not found."),
                _("Please install the itch.io app, which includes butler, and try again."),
                label="build_distributions"
                )

        itch_project = project.current.dump["build"].get("itch_project", None)

        if itch_project is None or ("/" not in itch_project):
            interface.error(
                _("The name of the itch project has not been set."),
                _("Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."),
                label="build_distributions"
                )

        cc = ConsoleCommand()

        for filename, channel in files:

            cc.add(
                butler,
                "push",
                filename,
                itch_project + ":" + build["version"] + "-" + channel,
                )

        cc.run()




    jump build_distributions
