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
    ANDROID_NO_RAPT = 0
    ANDROID_NO_JDK = 1
    ANDROID_NO_SDK = 2
    ANDROID_NO_KEY = 3
    ANDROID_NO_CONFIG = 4
    ANDROID_OK = 5

    NO_RAPT_TEXT = _("To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")
    NO_JDK_TEXT = _("A 64-bit/x64 Java 8 Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher.")
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

    LOGCAT_TEXT = _("Retrieves the log from the Android device and writes it to a file.")

    DEBUG_TEXT = _("Selects the Debug build, which can be accessed through Android Studio. Changing between debug and release builds requires an uninstall from your device.")
    RELEASE_TEXT = _("Selects the Release build, which can be uploaded to stores. Changing between debug and release builds requires an uninstall from your device.")


    import subprocess
    import re
    import os
    import json
    import glob

    def find_rapt():

        global RAPT_PATH

        candidates = [ ]

        RAPT_PATH = os.path.join(config.renpy_base, "rapt")

        if os.path.isdir(RAPT_PATH) and check_hash_txt("rapt"):
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
        rapt.plat.translate = __

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
        if not os.path.exists(rapt.plat.adb):
            return ANDROID_NO_SDK
        if not os.path.exists(rapt.plat.path("project/local.properties")):
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

        old_android_json = dict(android_json)

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

        if android_json != old_android_json:

            with open(filename, "w") as f:
                json.dump(android_json, f)


    def android_build(command, p=None, gui=True, launch=False, destination=None, opendir=False):
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

        def finished(files, destination=destination):

            source_dir = rapt.plat.path("bin")

            try:

                destination_dir = destination

                # Use default destination if not configured
                if gui and destination is None:
                    build = p.dump['build']
                    destination = build["destination"]

                    if destination != "-dists":
                        parent = os.path.dirname(p.path)
                        destination_dir = os.path.join(parent, destination)

            except:
                destination_dir = None

            dir_to_open = source_dir

            if destination_dir is not None:

                reporter.info(_("Copying Android files to distributions directory."))

                try:
                    os.makedirs(destination_dir)
                except:
                    pass

                try:

                    for i in files:
                        shutil.copy(i, renpy.fsencode(destination_dir))

                    dir_to_open = destination_dir

                except:
                    import traceback
                    traceback.print_exc()
                    pass

            if opendir:
                store.OpenDirectory(dir_to_open)()


        with interface.nolinks():
            rapt.build.build(rapt_interface, dist, command, launch=launch, finished=finished)


    def android_build_argument(cmd):
        return cmd + project.current.data["android_build"]



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
        font gui.LIGHT_FONT
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

            label _("Android: [project.current.display_name!q]")

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
                                action LaunchEmulator("touch", "small phone touch android mobile")
                                hovered tt.Action(PHONE_TEXT)

                            textbutton _("Tablet"):
                                action LaunchEmulator("touch", "medium tablet touch android mobile")
                                hovered tt.Action(TABLET_TEXT)

                            textbutton _("Television"):
                                action LaunchEmulator("tv", "small tv android mobile")
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

                            hbox:
                                spacing 15

                                textbutton _("Debug"):
                                    action SetDict(project.current.data, "android_build", "Debug")
                                    hovered tt.Action(DEBUG_TEXT)

                                textbutton _("Release"):
                                    action SetDict(project.current.data, "android_build", "Release")
                                    hovered tt.Action(RELEASE_TEXT)


                            add HALF_SPACER

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

                            textbutton _("Logcat"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("logcat"))
                                hovered tt.Action(LOGCAT_TEXT)


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


    textbutton _("Return") action Jump("front_page") style "l_left_button"


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
        project.current.update_dump(force=True)

        rapt.configure.configure(
            MobileInterface("android", edit=False),
            project.current.path,
            default_name=project.current.dump.get("name", None),
            default_version=project.current.dump.get("version", None))

    jump android


label android_build:

    $ android_build([ android_build_argument("assemble") ], opendir=True)

    jump android


label android_build_and_install:

    $ android_build([ android_build_argument("install") ])

    jump android

label android_build_install_and_launch:

    $ android_build([android_build_argument("install") ], launch=True)

    jump android

label logcat:

    python hide:

        interface = MobileInterface("android", filename="logcat.txt")
        interface.info(_("Retrieving logcat information from device."))
        interface.call([ rapt.plat.adb, "logcat", "-d" ], cancel=True)
        interface.open_editor()

    jump android

init python:

    def android_build_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("android_project", help="The path to the project directory.")
        ap.add_argument("gradle_commands", help="Commands to pass to gradle. (Try 'installDebug' or 'assembleRelease'.)", nargs='+')
        ap.add_argument("--launch", action="store_true", help="Launches the app after build and install compete.")
        ap.add_argument("--destination", "--dest", default=None, action="store", help="The directory where the packaged files should be placed.")

        args = ap.parse_args()

        p = project.Project(args.android_project)

        android_build(args.gradle_commands, p=p, gui=False, launch=args.launch, destination=args.destination)

        return False

    renpy.arguments.register_command("android_build", android_build_command)

