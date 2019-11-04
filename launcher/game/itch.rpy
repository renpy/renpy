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

    def find_itch_butler():

        if renpy.windows:
            platform = "windows-amd64"
            exe = "butler.exe"
        elif renpy.macintosh:
            platform = "darwin-amd64"
            exe = "butler"
        else:
            platform = "linux-amd64"
            exe = "butler"

        dn = os.path.join(config.renpy_base, "tmp", "butler-" + platform)
        zip = os.path.join(dn, "butler.zip")
        exe = os.path.join(dn, exe)

        if os.path.exists(exe):
            return exe

        interface.processing(_("Downloading the itch.io butler."))

        try:
            os.makedirs(dn)
        except:
            pass

        import urllib2
        import ssl

        with interface.error_handling(_("Downloading the itch.io butler.")):
            context = ssl._create_unverified_context()
            response = urllib2.urlopen("https://broth.itch.ovh/butler/{}/LATEST/archive/default".format(platform), context=context)

            with open(zip, "wb") as f:
                while True:
                    data = response.read(1024 * 1024)
                    if not data:
                        break

                    f.write(data)

        import zipfile

        with zipfile.ZipFile(zip) as zf:
            zf.extractall(dn)

        try:
            os.chmod(exe, 0o755)
        except:
            pass

        return exe


label itch:

    call build_update_dump


    python hide:

        butler = find_itch_butler()

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
                channel = "win-osx-linux"

            elif fn.endswith("-market.zip"):
                channel = "win-osx-linux"

            elif fn.endswith("-pc.zip"):
                channel = "win-linux"

            elif fn.endswith("-win.zip"):
                channel = "win"

            elif fn.endswith("-mac.zip"):
                channel = "osx"

            elif fn.endswith("-linux.tar.bz2"):
                channel = "linux"

            elif fn.endswith("-release.apk"):
                channel = "android"

            else:
                continue

            files.append((fn, channel))

        if not os.path.exists(destination):
            interface.error(
                _("No uploadable files were found. Please choose 'Build' and try again."),
                label="build_distributions"
                )

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
                itch_project + ":" + channel,
                "--userversion",
                build["version"],
                )

        cc.run()




    jump build_distributions
