# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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
    import fnmatch
    import re
    import zipfile

    def install_from_zip(name, zipglob, patterns):

        # Determine the filename matching the zipglob, and put it into filename.
        filenames = [ i for i in os.listdir(config.renpy_base) if fnmatch.fnmatch(i.lower(), zipglob.lower()) ]

        if not filenames:
            interface.error(
                _("Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."),
                label="install",
                name=name,
                zipglob=zipglob,
            )

        filenames.sort(key=lambda a : a.lower())
        filename = filenames[-1]

        # The zipfile.
        zf = zipfile.ZipFile(os.path.join(config.renpy_base, filename))

        for fn in zf.namelist():
            matchfn = fn.replace("\\", "/")
            dstfn = None

            renpy.write_log(fn)

            for src, dst in patterns:
                if re.match(src, matchfn):
                    dstfn = re.sub(src, dst, matchfn)
                    break

            if not dstfn:
                continue

            dstfn = os.path.join(config.renpy_base, dstfn)

            if not os.path.exists(os.path.dirname(dstfn)):
                try:
                    os.makedirs(os.path.dirname(dstfn))
                except Exception:
                    pass

            renpy.write_log(fn + " -> " + dstfn)

            data = zf.read(fn)
            with open(dstfn, "wb") as f:
                f.write(data)

            try:
                os.chmod(dstfn, 0o755)
            except Exception:
                pass

        interface.info(_("Successfully installed [name!t]."), name=name)


label install_live2d:
    python hide:
        if PY2:
            _prefix = r"lib/py2-"
        else:
            _prefix = r"lib/py3-"

        patterns = [
            (r".*/Core/dll/linux/x86_64/(libLive2DCubismCore.so)", _prefix + r"linux-x86_64/\1"),
            (r".*/Core/dll/windows/x86_64/(Live2DCubismCore.dll)", _prefix + r"windows-x86_64/\1"),
            (r".*/Core/dll/macos/(libLive2DCubismCore.dylib)", _prefix + r"mac-universal/\1"),
            (r".*/Core/dll/experimental/rpi/(libLive2DCubismCore.so)", _prefix + r"linux-armv7l/\1"),

            (r".*/Core/dll/android/(armeabi-v7a/libLive2DCubismCore.so)", r"rapt/prototype/renpyandroid/src/main/jniLibs/\1"),
            (r".*/Core/dll/android/(arm64-v8a/libLive2DCubismCore.so)", r"rapt/prototype/renpyandroid/src/main/jniLibs/\1"),
            (r".*/Core/dll/android/(x86_64/libLive2DCubismCore.so)", r"rapt/prototype/renpyandroid/src/main/jniLibs/\1"),
        ]

        if PY2:
           patterns.extend([
                (r".*/Core/dll/windows/x86/(Live2DCubismCore.dll)", _prefix + r"windows-i686/\1"),
           ])

        install_from_zip("Live2D Cubism SDK for Native", "CubismSdkForNative-[45]-*.zip", patterns)

    jump front_page

screen install_preferences():

    frame:
        style "l_indent"
        has vbox

        text _("This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed.")

    add SPACER

    if not achievement.has_steam:

        textbutton _("Install Steam Support"):
            action Jump("install_steam")

        add HALF_SPACER

        frame:
            style "l_indent"
            has vbox

            text _("Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}.")

    else:

        textbutton _("Install Steam Support")

        add HALF_SPACER

        frame:
            style "l_indent"
            has vbox

            text _("Steam support has already been installed.")

    add SPACER

    textbutton _("Install Live2D Cubism SDK for Native"):
        action Jump("prompt_live2d")


screen install_live2d():

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Install Libraries")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    viewport:
                        scrollbars "vertical"
                        mousewheel True

                        has vbox

                        add SPACER

                        textbutton _("Install Live2D Cubism SDK for Native"):
                            action Jump("install_live2d")

                        add HALF_SPACER

                        frame:
                            style "l_indent"
                            has vbox

                            text _("The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc.")

                            add SPACER

                            text _("Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support.")



    textbutton _("Cancel") action Return(False) style "l_left_button"
    textbutton _("Open Ren'Py SDK Directory") action OpenDirectory(config.renpy_base, absolute=True) style "l_right_button"

    timer 2.0 action renpy.restart_interaction repeat True

label prompt_live2d:
    call screen install_live2d
    jump preferences

label install_steam:
    $ add_dlc("steam", restart=True)
    jump install
