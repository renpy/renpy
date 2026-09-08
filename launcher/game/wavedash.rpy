# Copyright 2004-2026 Tom Rothamel <pytom@bishoujo.us>
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

    def find_wavedash():
        """Returns the path to the Wavedash CLI, or None if it is not installed."""

        import shutil

        rv = shutil.which("wavedash")

        if rv is not None:
            return rv

        executable = "wavedash.exe" if renpy.windows else "wavedash"

        candidates = [
            os.path.join(os.path.expanduser("~"), ".cargo", "bin", executable),
        ]

        if renpy.macintosh:
            candidates.extend([
                "/opt/homebrew/bin/wavedash",
                "/usr/local/bin/wavedash",
            ])

        for filename in candidates:
            if os.path.isfile(filename) and os.access(filename, os.X_OK):
                return filename

        return None


label wavedash_upload:

    call build_update_dump

    python hide:

        build = project.current.dump["build"]
        wavedash_id = build.get("wavedash_id")

        if not isinstance(wavedash_id, str) or not wavedash_id:
            interface.error(
                _("The Wavedash game ID has not been set."),
                _("Create a game at {a=https://wavedash.com/dev-portal}wavedash.com/dev-portal{/a}, then add a line like \n{vspace=5}define build.wavedash_id = \"YOUR_GAME_ID_HERE\"\n{vspace=5} to options.rpy."),
                label="build_distributions"
                )

        destination = get_web_destination(project.current)
        config_file = os.path.join(destination, "wavedash.toml")

        if not os.path.isfile(config_file):
            interface.error(
                _("The web distribution could not be found. Please choose 'Web', 'Build Web Application' and try again."),
                label="build_distributions"
                )

        wavedash = find_wavedash()

        if wavedash is None:
            interface.error(
                _("The Wavedash CLI was not found."),
                _("Please {a=https://docs.wavedash.com/cli/installation}install the Wavedash CLI{/a} and try again."),
                label="build_distributions"
                )

        cc = ConsoleCommand()
        cc.add(wavedash, "build", "push", "--config", config_file)
        cc.run()

    jump build_distributions
