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

    WAVEDASH_CLI_OVERRIDES = (
        "WAVEDASH_ENTRYPOINT",
        "WAVEDASH_GAME_ID",
        "WAVEDASH_GODOT_VERSION",
        "WAVEDASH_UNITY_VERSION",
        "WAVEDASH_UPDATE_REPO_NAME",
        "WAVEDASH_UPDATE_REPO_OWNER",
        "WAVEDASH_UPLOAD_DIR",
        )

    def find_wavedash():
        """Returns the path to the Wavedash CLI, downloading it if necessary."""

        import hashlib
        import hmac
        import platform
        import shutil
        import tarfile
        import zipfile

        import requests

        machine = platform.machine().lower()

        if renpy.windows:
            target = "x86_64-pc-windows-msvc"
            archive_format = "zip"
            executable = "wavedash.exe"
        elif renpy.macintosh:
            if machine in ("aarch64", "arm64"):
                target = "aarch64-apple-darwin"
            elif machine in ("amd64", "x86_64"):
                target = "x86_64-apple-darwin"
            else:
                return None

            archive_format = "tar.gz"
            executable = "wavedash"
        elif renpy.linux:
            if machine in ("aarch64", "arm64"):
                target = "aarch64-unknown-linux-gnu"
            elif machine in ("amd64", "x86_64"):
                target = "x86_64-unknown-linux-gnu"
            else:
                return None

            archive_format = "tar.gz"
            executable = "wavedash"
        else:
            return None

        directory = os.path.join(config.renpy_base, "tmp", "wavedash-" + target)
        executable = os.path.join(directory, executable)

        if os.path.isfile(executable) and os.access(executable, os.X_OK):
            return executable

        interface.processing(_("Downloading the Wavedash CLI."))

        archive_name = f"wavedash-{target}.{archive_format}"
        archive = os.path.join(directory, archive_name)
        url = "https://github.com/wvdsh/cli/releases/latest/download/" + archive_name

        with interface.error_handling(_("Downloading the Wavedash CLI."), label="web"):
            os.makedirs(directory, exist_ok=True)

            response = requests.get(
                url,
                headers={ "User-Agent" : "Renpy" },
                proxies=renpy.proxies,
                timeout=60,
                )
            response.raise_for_status()

            checksum_response = requests.get(
                url + ".sha256",
                headers={ "User-Agent" : "Renpy" },
                proxies=renpy.proxies,
                timeout=60,
                )
            checksum_response.raise_for_status()

            expected_checksum = checksum_response.text.split()[0].lower()
            actual_checksum = hashlib.sha256(response.content).hexdigest()

            if not hmac.compare_digest(actual_checksum, expected_checksum):
                raise Exception("The Wavedash CLI download failed checksum verification.")

            with open(archive, "wb") as f:
                f.write(response.content)

            if archive_format == "zip":
                with zipfile.ZipFile(archive) as zf:
                    zf.extractall(directory)
            else:
                with tarfile.open(archive, "r:gz") as tf:
                    tf.extractall(directory, filter="data")

            extracted_executable = os.path.join(directory, "wavedash-" + target, os.path.basename(executable))

            if os.path.isfile(extracted_executable):
                shutil.move(extracted_executable, executable)

            if not os.path.isfile(executable):
                raise Exception("The Wavedash CLI executable was not found in the downloaded archive.")

            os.chmod(executable, 0o755)

        return executable


    def wavedash_status(wavedash):
        """Returns whether the CLI is authenticated and has an update."""

        import subprocess

        creationflags = 0

        if renpy.windows:
            creationflags = subprocess.CREATE_NO_WINDOW

        try:
            completed = subprocess.run(
                [ wavedash, "auth", "status" ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                creationflags=creationflags,
                )
        except (OSError, subprocess.TimeoutExpired):
            return False, False

        if completed.returncode != 0:
            return False, False

        # The CLI exits successfully even when no credentials are available.
        authenticated = "Not authenticated." not in completed.stdout
        update_available = "Update available:" in completed.stdout

        return authenticated, update_available


    def clear_wavedash_cli_overrides(cc):
        """Makes the generated manifest authoritative for an upload."""

        if renpy.windows:
            for variable in WAVEDASH_CLI_OVERRIDES:
                cc.write("set", '"{}="'.format(variable))
        else:
            cc.write("unset", *WAVEDASH_CLI_OVERRIDES)


    def read_generated_wavedash_game_id(filename):
        """Returns the game ID from a wavedash.toml generated by Ren'Py."""

        import json

        with open(filename, encoding="utf-8") as f:
            line = f.readline()

        prefix = "game_id = "

        if not line.startswith(prefix):
            raise ValueError("The first line of wavedash.toml does not contain game_id.")

        game_id = json.loads(line[len(prefix):])

        if not isinstance(game_id, str):
            raise ValueError("The game_id in wavedash.toml is not a string.")

        return game_id


label wavedash:

    call build_update_dump

    python hide:

        build = project.current.dump["build"]
        wavedash_id = build.get("wavedash_id")

        if not isinstance(wavedash_id, str) or not wavedash_id:
            interface.error(
                _("The Wavedash game ID has not been set."),
                _("Create a game at {a=https://wavedash.com/dev-portal}wavedash.com/dev-portal{/a}, then add a line like \n{vspace=5}define build.wavedash_id = \"YOUR_GAME_ID_HERE\"\n{vspace=5} to options.rpy."),
                label="web"
                )

        destination = get_web_destination(project.current)
        config_file = os.path.join(destination, "wavedash.toml")
        built_wavedash_id = None
        needs_web_build = False

        if not os.path.isfile(config_file):
            if not interface.yesno(_("The web distribution could not be found. Would you like to build it now and upload it to Wavedash?")):
                renpy.jump("web")

            needs_web_build = True
        else:
            try:
                built_wavedash_id = read_generated_wavedash_game_id(config_file)
            except Exception:
                interface.error(
                    _("The Wavedash configuration in the web distribution could not be read."),
                    _("Please choose 'Web', 'Build Web Application' and try again."),
                    label="web"
                    )

            if built_wavedash_id != wavedash_id:
                if not interface.yesno(_("The Wavedash game ID changed after the web distribution was built. Would you like to rebuild it now and upload it to Wavedash?")):
                    renpy.jump("web")

                needs_web_build = True

        if needs_web_build:
            if WEB_PATH is None:
                if not interface.yesno(_("Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?")):
                    renpy.jump("web")

                # Web support only contains build files, so it can be used
                # immediately after refreshing WEB_PATH.
                add_dlc("web", restart=False)
                find_web()

                if WEB_PATH is None:
                    interface.error(
                        _("RenPyWeb could not be installed."),
                        label="web"
                        )

            build_web(project.current, gui=True, launch=False)

            try:
                built_wavedash_id = read_generated_wavedash_game_id(config_file)
            except Exception:
                interface.error(
                    _("The Wavedash configuration in the web distribution could not be read."),
                    _("Please choose 'Web', 'Build Web Application' and try again."),
                    label="web"
                    )

        if built_wavedash_id != wavedash_id:
            interface.error(
                _("The web distribution was built for a different Wavedash game."),
                label="web"
                )

        wavedash = find_wavedash()

        if wavedash is None:
            interface.error(
                _("The Wavedash CLI is not available for this platform."),
                label="web"
                )

        authenticated, update_available = wavedash_status(wavedash)
        cc = ConsoleCommand()

        # The generated config is authoritative for launcher uploads. Keep the
        # authentication token, but prevent CLI environment overrides from
        # selecting a different game, directory, entrypoint, or update source.
        clear_wavedash_cli_overrides(cc)

        if update_available:
            cc.add(wavedash, "update")

        if not authenticated:
            cc.add(wavedash, "auth", "login")

            # Only upload when browser authentication succeeds.
            if renpy.windows:
                cc.write("if", "not", "errorlevel", "1", "(")
            else:
                cc.write("if", "[", "$?", "-eq", "0", "];", "then")

            cc.add(wavedash, "build", "push", "--config", config_file)

            if renpy.windows:
                cc.write(")")
            else:
                cc.write("fi")
        else:
            cc.add(wavedash, "build", "push", "--config", config_file)

        cc.run()

    jump web
