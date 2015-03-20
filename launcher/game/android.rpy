﻿# Copyright 2004-2015 Tom Rothamel <pytom@bishoujo.us>
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
    ANDROID_NO_RAPT = 0
    ANDROID_NO_JDK = 1
    ANDROID_NO_SDK = 2
    ANDROID_NO_KEY = 3
    ANDROID_NO_CONFIG = 4
    ANDROID_OK = 5

    NO_RAPT_TEXT = _("To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")
    NO_JDK_TEXT = _("A 32-bit Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/index.html}download and install the JDK{/a}, then restart the Ren'Py launcher.")
    NO_SDK_TEXT = _("RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this.")
    NO_KEY_TEXT = _("RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore.")
    NO_CONFIG_TEXT = _("The current project has not been configured. Use \"Configure\" to configure it before building.")
    OK_TEXT = _("Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device.")

    PHONE_TEXT = _("Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    TABLET_TEXT = _("Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    OUYA_TEXT = _("Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button.")

    INSTALL_SDK_TEXT = _("Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package.")
    CONFIGURE_TEXT = _("Configures the package name, version, and other information about this project.")
    PLAY_KEYS_TEXT = _("Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details.")
    BUILD_TEXT = _("Builds the Android package.")
    BUILD_AND_INSTALL_TEXT = _("Builds the Android package, and installs it on an Android device connected to your computer.")
    BUILD_INSTALL_AND_LAUNCH_TEXT = _("Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device.")

    CONNECT_TEXT = _("Connects to an Android device running ADB in TCP/IP mode.")
    DISCONNECT_TEXT = _("Disconnects from an Android device running ADB in TCP/IP mode.")


    import subprocess
    import re
    import os
    import json

    def find_rapt():

        global RAPT_PATH

        candidates = [ ]

        RAPT_PATH = os.path.join(config.renpy_base, "rapt")

        if os.path.isdir(RAPT_PATH):
            import sys
            sys.path.insert(0, os.path.join(RAPT_PATH, "buildlib"))
        else:
            RAPT_PATH = None

    find_rapt()

    import threading

    if RAPT_PATH:
        import rapt
        import rapt.build
        import rapt.configure
        import rapt.install_sdk
        import rapt.plat
        import rapt.interface

        rapt.plat.renpy = True
    else:
        rapt = None

    def AndroidState():
        """
        Determines the state of the android install, and returns it.
        """

        if RAPT_PATH is None:
            return ANDROID_NO_RAPT
        if renpy.windows and not "JAVA_HOME" in os.environ:
            return ANDROID_NO_JDK
        if not os.path.exists(rapt.plat.path("android-sdk/extras/google/play_licensing")):
            return ANDROID_NO_SDK
        if not os.path.exists(rapt.plat.path("android.keystore")):
            return ANDROID_NO_KEY
        if not os.path.exists(rapt.plat.path("local.properties")):
            return ANDROID_NO_KEY
        if not os.path.exists(os.path.join(project.current.path, ".android.json")):
            return ANDROID_NO_CONFIG
        return ANDROID_OK


    def AndroidStateText(state):
        """
        Returns text corresponding to the state.
        """

        if state == ANDROID_NO_RAPT:
            return NO_RAPT_TEXT
        if state == ANDROID_NO_JDK:
            return NO_JDK_TEXT
        if state == ANDROID_NO_SDK:
            return NO_SDK_TEXT
        if state == ANDROID_NO_KEY:
            return NO_KEY_TEXT
        if state == ANDROID_NO_CONFIG:
            return NO_CONFIG_TEXT
        if state == ANDROID_OK:
            return OK_TEXT

    def AndroidIfState(state, needed, action):
        """
        If `state` is `needed` or better, `action` is returned. Otherwise,
        returns None, disabling the button.
        """

        if state >= needed:
            return action
        else:
            return None


    class AndroidBuild(Action):
        """
        Activates an Android build process.
        """

        def __init__(self, label):
            self.label = label

        def __call__(self):
            renpy.jump(self.label)

    def update_android_json(p, gui):
        """
        Updates .android.json to include the google play information.

        `p`
            The project to update json for.
        """

        p.update_dump(True, gui=gui)

        build = p.dump["build"]

        filename = os.path.join(p.path, ".android.json")

        with open(filename, "r") as f:
            android_json = json.load(f)

        if "google_play_key" in build:
            android_json["google_play_key"] = build["google_play_key"]
        else:
            android_json.pop("google_play_key", None)

        if "google_play_salt" in build:

            if len(build["google_play_salt"]) != 20:
                raise Exception("build.google_play_salt must be exactly 20 bytes long.")

            android_json["google_play_salt"] = ", ".join(str(i) for i in build["google_play_salt"])
        else:
            android_json.pop("google_play_salt", None)


        with open(filename, "w") as f:
            json.dump(android_json, f)

    def android_build(command, p=None, gui=True, launch=False):
        """
        This actually builds the package.
        """

        if p is None:
            p = project.current

        update_android_json(p, gui)

        dist = p.temp_filename("android.dist")

        if os.path.exists(dist):
            shutil.rmtree(dist)

        if gui:
            reporter = distribute.GuiReporter()
            rapt_interface = MobileInterface("android")
        else:
            reporter = distribute.TextReporter()
            rapt_interface = rapt.interface.Interface()

        distribute.Distributor(p,
            reporter=reporter,
            packages=[ 'android' ],
            build_update=False,
            noarchive=True,
            packagedest=dist,
            report_success=False,
            )

        with interface.nolinks():
            rapt.build.build(rapt_interface, dist, command, launch=launch)

# The android support can stick unicode into os.environ. Fix that.
init 100 python:
    for k, v in list(os.environ.items()):
        if not isinstance(v, str):
            os.environ[k] = renpy.fsencode(v)

screen android_process(interface):

    zorder 100

    default ft = FileTail(interface.filename)

    text "[ft.text!q]":
        size 14
        color TEXT
        font "Roboto-Light.ttf"
        xpos 75
        ypos 350

    timer .1 action interface.check_process repeat True
    timer .2 action ft.update repeat True


screen android:

    default tt = Tooltip(None)
    $ state = AndroidState()

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Android: [project.current.name!q]")

            add HALF_SPACER

            hbox:

                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Emulation:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has hbox:
                                spacing 15

                            textbutton _("Phone"):
                                action LaunchEmulator("touch", "small phone touch android")
                                hovered tt.Action(PHONE_TEXT)

                            textbutton _("Tablet"):
                                action LaunchEmulator("touch", "medium tablet touch android")
                                hovered tt.Action(TABLET_TEXT)

                            textbutton _("Television"):
                                action LaunchEmulator("tv", "small tv ouya android")
                                hovered tt.Action(OUYA_TEXT)


                    add SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Build:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Install SDK & Create Keys"):
                                action AndroidIfState(state, ANDROID_NO_SDK, Jump("android_installsdk"))
                                hovered tt.Action(INSTALL_SDK_TEXT)

                            textbutton _("Configure"):
                                action AndroidIfState(state, ANDROID_NO_CONFIG, Jump("android_configure"))
                                hovered tt.Action(CONFIGURE_TEXT)

                            textbutton _("Build Package"):
                                action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build"))
                                hovered tt.Action(BUILD_TEXT)

                            textbutton _("Build & Install"):
                                action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build_and_install"))
                                hovered tt.Action(BUILD_AND_INSTALL_TEXT)

                            textbutton _("Build, Install & Launch"):
                                action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build_install_and_launch"))
                                hovered tt.Action(BUILD_INSTALL_AND_LAUNCH_TEXT)

                    add SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Other:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Remote ADB Connect"):
                                action AndroidIfState(state, ANDROID_OK, Jump("android_connect"))
                                hovered tt.Action(CONNECT_TEXT)

                            textbutton _("Remote ADB Disconnect"):
                                action AndroidIfState(state, ANDROID_OK, Jump("android_disconnect"))
                                hovered tt.Action(DISCONNECT_TEXT)


                # Right side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        add SPACER

                        if tt.value:
                            text tt.value
                        else:
                            text AndroidStateText(state)


    textbutton _("Back") action Jump("front_page") style "l_left_button"


label android:

    if RAPT_PATH is None:
        $ interface.yesno(_("Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"), no=Jump("front_page"))
        $ add_dlc("rapt", restart=True)

    call screen android


label android_installsdk:

    python:
        with interface.nolinks():
            rapt.install_sdk.install_sdk(MobileInterface("android"))

    jump android


label android_configure:

    python:
        rapt.configure.configure(MobileInterface("android", edit=False), project.current.path)

    jump android


label android_build:

    $ android_build([ 'release' ])

    jump android


label android_build_and_install:

    $ android_build([ 'release', 'install' ])

    jump android

label android_build_install_and_launch:

    $ android_build([ 'release', 'install' ], launch=True)

    jump android


label android_connect:

    python hide:

        if persistent.connect_address is not None:
            address = persistent.connect_address
        else:
            address = ""

        while True:
            address = interface.input(
                _("Remote ADB Address"),
                _("Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."),
                default=address,
                cancel=Jump("android"),
                )

            address = address.strip()

            try:
                host, port = address.split(":")
            except:
                interface.error(_("Invalid remote ADB address"), _("The address must contain one exactly one ':'."), label=None)
                continue

            if " " in host:
                interface.error(_("Invalid remote ADB address"), _("The host may not contain whitespace."), label=None)
                continue

            try:
                int(port)
            except:
                interface.error(_("Invalid remote ADB address"), _("The port must be a number."), label=None)
                continue

            break

        persistent.connect_address = address

        rapt_interface = MobileInterface("android")
        rapt.build.connect(rapt_interface, address)

    jump android

label android_disconnect:

    python hide:

        rapt_interface = MobileInterface("android")
        rapt.build.disconnect(rapt_interface)

    jump android

init python:

    def android_build_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("project", help="The path to the project directory.")
        ap.add_argument("command", help="Commands to pass to ant. (Try 'release' 'install'.)", nargs='+')
        ap.add_argument("--launch", action="store_true", help="Launches the app after build and install compete.")

        args = ap.parse_args()

        p = project.Project(args.project)

        android_build(args.command, p=p, gui=False, launch=args.launch)

        return False

    renpy.arguments.register_command("android_build", android_build_command)

