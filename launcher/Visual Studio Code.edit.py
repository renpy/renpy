import os
import subprocess
import sys

import renpy


class Editor(renpy.editor.Editor):
    has_projects = True

    codium = __file__.endswith("VSCodium (System).edit.py")
    system = __file__.endswith(" (System).edit.py") and not codium

    def get_code(self):
        """
        Returns the path to the code executable.
        """

        if self.system:
            if "RENPY_VSCODE" in os.environ:
                return os.environ["RENPY_VSCODE"]

            if renpy.windows:
                return "code.cmd"

            if renpy.macintosh and os.path.exists(
                "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
            ):
                return "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"

            return "code"

        elif self.codium:
            if "RENPY_VSCODE" in os.environ:
                return os.environ["RENPY_VSCODE"]

            if renpy.windows:
                return "codium.cmd"

            if renpy.macintosh and os.path.exists("/Applications/VSCodium.app/Contents/Resources/app/bin/codium"):
                return "/Applications/VSCodium.app/Contents/Resources/app/bin/codium"

            return "codium"

        else:
            RENPY_VSCODE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vscode"))

            if renpy.windows:
                code = os.path.join(RENPY_VSCODE, "VSCode-win32-x64", "bin", "code.cmd")
            elif renpy.macintosh:
                code = os.path.join(
                    RENPY_VSCODE, "Visual Studio Code.app", "Contents", "Resources", "app", "bin", "code"
                )
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

    def get_settings_path(self):
        """
        Returns the path to the user settings.json of the VS Code that the launcher installed, or None if that
        VS Code is not installed in portable mode (or is not supported on this platform).
        """

        RENPY_VSCODE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "vscode"))

        if renpy.macintosh:
            data = os.path.join(RENPY_VSCODE, "code-portable-data")
        elif renpy.windows or renpy.linux:
            data = os.path.join(os.path.dirname(os.path.dirname(self.get_code())), "data")
        else:
            return None

        if not os.path.isdir(data):
            return None

        return os.path.join(data, "user-data", "User", "settings.json")

    def configure_renpy_executable(self):
        """
        Points the Ren'Py extension's renpy.renpyExecutableLocation setting at this Ren'Py's executable, in
        the user settings of the VS Code the launcher installed. Without it, the extension can't run Ren'Py,
        and its tasks fail with "Illegal argument: command can't be undefined or null".

        An existing value is kept if it names a file that exists. An empty settings file is treated as having no
        settings. A settings file that isn't plain JSON (for example, one with comments) is left unchanged.
        """

        import json

        settings_path = self.get_settings_path()
        if settings_path is None:
            return

        base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        executable = os.path.join(base, "renpy.exe" if renpy.windows else "renpy.sh")

        if not os.path.exists(executable):
            return

        settings = {}

        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r", encoding="utf-8-sig") as f:
                    text = f.read()

                if text.strip():
                    settings = json.loads(text)

            except ValueError:
                return

            if not isinstance(settings, dict):
                return

        current = settings.get("renpy.renpyExecutableLocation")
        if isinstance(current, str) and current and os.path.isfile(current):
            return

        settings["renpy.renpyExecutableLocation"] = executable

        os.makedirs(os.path.dirname(settings_path), exist_ok=True)

        new_path = settings_path + ".new"

        with open(new_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)
            f.write("\n")

        os.replace(new_path, settings_path)

    def open(self, filename, line=None, **kwargs):
        if line:
            filename = "{}:{}".format(filename, line)
        self.args.append(filename)

    def open_project(self, directory):
        self.args.append(directory)

    def begin(self, new_window=False, **kwargs):
        self.args = []

    def end(self, **kwargs):
        self.args.reverse()

        code = self.get_code()

        if not (self.system or self.codium):
            try:
                self.configure_renpy_executable()
            except Exception:
                import traceback

                traceback.print_exc()

        if self.system or not renpy.linux:
            args = [code, "-g"] + self.args
        else:
            args = [code, "--no-sandbox", "-g"] + self.args

        if renpy.windows:
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(args, creationflags=CREATE_NO_WINDOW)
        elif renpy.linux and self.system:
            try:
                subprocess.Popen(args)
            except FileNotFoundError as missingvscode:
                flatpak_code = [ "flatpak", "run", "com.visualstudio.code" ]
                flatpak_args = flatpak_code + ["-g"] + self.args
                try:
                    subprocess.Popen(flatpak_args)
                except Exception:
                    raise missingvscode
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
