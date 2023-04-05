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

default persistent.android_bundle = False

init python:
    ANDROID_NO_RAPT = 0
    ANDROID_NO_JDK = 1
    ANDROID_NO_SDK = 2
    ANDROID_NO_KEY = 3
    ANDROID_NO_BUNDLE_KEY = 4
    ANDROID_NO_CONFIG = 5
    ANDROID_NO_BUNDLE = 6
    ANDROID_OK = 7

    JDK_REQUIREMENT=8

    NO_RAPT_TEXT = _("To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")
    NO_JDK_TEXT = _("A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher.")
    NO_SDK_TEXT = _("RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this.")
    NO_KEY_TEXT = _("RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory.")
    NO_CONFIG_TEXT = _("The current project has not been configured. Use \"Configure\" to configure it before building.")
    NO_BUNDLE_TEXT = _("Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores).")
    OK_TEXT = _("Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device.")

    PHONE_TEXT = _("Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    TABLET_TEXT = _("Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    OUYA_TEXT = _("Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button.")

    INSTALL_SDK_TEXT = _("Downloads and installs the Android SDK and supporting packages.")
    GENERATE_KEYS_TEXT = _("Generates the keys required to sign the package.")
    CONFIGURE_TEXT = _("Configures the package name, version, and other information about this project.")
    BUILD_TEXT = _("Builds the Android package.")
    BUILD_AND_INSTALL_TEXT = _("Builds the Android package, and installs it on an Android device connected to your computer.")
    BUILD_INSTALL_AND_LAUNCH_TEXT = _("Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device.")

    LOGCAT_TEXT = _("Retrieves the log from the Android device and writes it to a file.")
    LIST_DEVICES_TEXT = _("Lists the connected devices.")
    PAIR_TEXT = _("Pairs with a device over Wi-Fi, on Android 11+.")
    CONNECT_TEXT = _("Connects to a device over Wi-Fi, on Android 11+.")
    DISCONNECT_TEXT = _("Disconnects a device connected over Wi-Fi.")

    CLEAN_TEXT = _("Removes Android temporary files.")

    PLAY_BUNDLE_TEXT = _("Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data.")
    UNIVERSAL_APK_TEXT = _("Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data.")

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
        import rapt.keys

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
        if not rapt.keys.keys_exist(project.current.path):
            return ANDROID_NO_KEY
        if not any([
            os.path.exists(os.path.join(project.current.path, "android.json")),
            os.path.exists(os.path.join(project.current.path, ".android.json"))
            ]):
            return ANDROID_NO_CONFIG
        if persistent.android_bundle is None:
            return ANDROID_NO_BUNDLE

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
        if state == ANDROID_NO_BUNDLE:
            return NO_BUNDLE_TEXT
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

        c = rapt.configure.Configuration(p.path)

        if "google_play_key" in build:
            c.google_play_key = build["google_play_key"]
        else:
            c.google_play_key = None

        if "google_play_salt" in build:

            if len(build["google_play_salt"]) != 20:
                raise Exception("build.google_play_salt must be exactly 20 bytes long.")

            c.google_play_salt = ", ".join(str(i) for i in build["google_play_salt"])
        else:
            c.google_play_salt = None

        c.save(p.path)


    def android_build(p=None, gui=True, bundle=False, install=False, launch=False, destination=None, opendir=False):
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

            except Exception:
                destination_dir = None

            dir_to_open = source_dir

            if destination_dir is not None:

                reporter.info(_("Copying Android files to distributions directory."))

                try:
                    os.makedirs(destination_dir)
                except Exception:
                    pass

                try:

                    for i in files:
                        shutil.copy(i, renpy.fsencode(destination_dir))

                    dir_to_open = destination_dir

                except Exception:
                    import traceback
                    traceback.print_exc()
                    pass

            if opendir:
                dir_to_open = os.path.join(p.path, dir_to_open)
                renpy.run(store.OpenDirectory(dir_to_open, absolute=True))


        with interface.nolinks():
            rapt.build.build(rapt_interface, dist, p.path, bundle=bundle, install=install, launch=launch, finished=finished, permissions=p.dump['build']['android_permissions'])


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
                            textbutton _("Install SDK"):
                                action AndroidIfState(state, ANDROID_NO_SDK, Jump("android_installsdk"))
                                hovered tt.Action(INSTALL_SDK_TEXT)

                            textbutton _("Generate Keys"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_keys"))
                                hovered tt.Action(GENERATE_KEYS_TEXT)

                            textbutton _("Configure"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_configure"))
                                hovered tt.Action(CONFIGURE_TEXT)

                            add SPACER

                            textbutton _("Play Bundle"):
                                action SetField(persistent, "android_bundle", True)
                                hovered tt.Action(PLAY_BUNDLE_TEXT)
                                style "l_checkbox"

                            textbutton _("Universal APK"):
                                action SetField(persistent, "android_bundle", False)
                                hovered tt.Action(UNIVERSAL_APK_TEXT)
                                style "l_checkbox"

                            add SPACER

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

                            textbutton _("Force Recompile") action DataToggle("force_recompile") style "l_checkbox"


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

                        text _("Other:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Logcat"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("logcat"))
                                hovered tt.Action(LOGCAT_TEXT)

                            textbutton _("List Devices"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_list_devices"))
                                hovered tt.Action(LIST_DEVICES_TEXT)

                            textbutton _("Wi-Fi Debugging Pair"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_pair"))
                                hovered tt.Action(PAIR_TEXT)

                            textbutton _("Wi-Fi Debugging Connect"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_connect"))
                                hovered tt.Action(CONNECT_TEXT)

                            textbutton _("Wi-Fi Debugging Disconnect"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_disconnect"))
                                hovered tt.Action(DISCONNECT_TEXT)

                            textbutton _("Clean"):
                                action AndroidIfState(state, ANDROID_NO_KEY, Jump("android_clean"))
                                hovered tt.Action(CLEAN_TEXT)

                    add SPACER
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


label android_keys:

    python:
        rapt.keys.generate_keys(MobileInterface("android"), project.current.path)

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

    $ android_build(bundle=persistent.android_bundle, opendir=True)

    jump android


label android_build_and_install:

    $ android_build(bundle=persistent.android_bundle, install=True, opendir=True)

    jump android

label android_build_install_and_launch:

    $ android_build(bundle=persistent.android_bundle, install=True, launch=True, opendir=True)

    jump android

label logcat:

    python hide:

        interface = MobileInterface("android", filename="logcat.txt")
        interface.info(_("Retrieving logcat information from device."))
        interface.call([ rapt.plat.adb, "logcat", "-d" ], cancel=True)
        interface.open_editor()

    jump android

label android_list_devices:

    python hide:
        cc = ConsoleCommand()
        cc.add(rapt.plat.adb, "devices")
        cc.run()

    jump android


label android_pair:

    python hide:
        pairing_code = interface.input(
            _("Wi-Fi Pairing Code"),
            _("If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."),
            sanitize=False,
            cancel=Jump("android"),
            )

        host = interface.input(
            _("Pairing Host & Port"),
            _("If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."),
            sanitize=False,
            cancel=Jump("android"),
            )

        cc = ConsoleCommand()
        cc.add(rapt.plat.adb, "pair", host, pairing_code)
        cc.run()

    jump android

label android_connect:

    python hide:
        host = interface.input(
            _("IP Address & Port"),
            _("If supported, this can be found in 'Developer options', 'Wireless debugging'."),
            sanitize=False,
            cancel=Jump("android"),
            )

        cc = ConsoleCommand()
        cc.add(rapt.plat.adb, "connect", host)
        cc.run()

    jump android

label android_disconnect:

    python hide:
        host = interface.input(
            _("IP Address & Port"),
            _("This can be found in 'List Devices'."),
            sanitize=False,
            cancel=Jump("android"),
            )

        cc = ConsoleCommand()
        cc.add(rapt.plat.adb, "disconnect", host)
        cc.run()

    jump android

label android_clean:

    python hide:
        import shutil
        import time

        interface = MobileInterface("android")
        interface.info(_("Cleaning up Android project."))

        # Get the android json file, for the update_always key.
        try:
            filename = os.path.join(project.current.path, ".android.json")
            with open(filename, "rb") as f:
                android_json = json.load(f)
        except Exception:
            android_json = {}

        # Clean up the files.
        def clean(path):
            if os.path.exists(path):
                shutil.rmtree(path)

        if android_json.get("update_always", True):

            try:
                with open(rapt.plat.path("project/local.properties"), "r") as f:
                    local_properties = f.read()
            except Exception:
                local_properties = None

            try:
                with open(rapt.plat.path("project/bundle.properties"), "r") as f:
                    bundle_properties = f.read()
            except Exception:
                bundle_properties = None

            try:
                with open(rapt.plat.path("project/gradle.properties"), "r") as f:
                    gradle_properties = f.read()
            except Exception:
                gradle_properties = None

            clean(rapt.plat.path("project"))

            if local_properties or bundle_properties or gradle_properties:

                os.mkdir(rapt.plat.path("project"))

            if local_properties:

                with open(rapt.plat.path("project/local.properties"), "w") as f:
                    f.write(local_properties)

            if bundle_properties:

                with open(rapt.plat.path("project/bundle.properties"), "w") as f:
                    f.write(bundle_properties)

            if gradle_properties:

                with open(rapt.plat.path("project/gradle.properties"), "w") as f:
                    f.write(gradle_properties)

        clean(rapt.plat.path("bin"))
        clean(project.current.temp_filename("android.dist"))

        # This can go really fast, so pause so it looks like something is happening.
        time.sleep(.5)


    jump android


init python:

    def android_build_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("android_project", help="The path to the project directory.")
        ap.add_argument("--bundle", action="store_true", help="Builds an android app bundle.")
        ap.add_argument("--install", action="store_true", help="Installs the app on a device.")
        ap.add_argument("--launch", action="store_true", help="Launches the app after build and install complete. Implies --install.")
        ap.add_argument("--destination", "--dest", default=None, action="store", help="The directory where the packaged files should be placed.")

        args = ap.parse_args()

        if args.launch:
            args.install = True

        p = project.Project(args.android_project)

        android_build(p=p, gui=False, bundle=args.bundle, install=args.install, launch=args.launch, destination=args.destination)

        return False

    renpy.arguments.register_command("android_build", android_build_command)
