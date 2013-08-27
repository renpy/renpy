# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:
    ANDROID_NO_RAPT = 0
    ANDROID_NO_SDK = 1
    ANDROID_NO_KEY = 2
    ANDROID_NO_CONFIG = 3
    ANDROID_OK = 4


    NO_RAPT_TEXT = _("To build Android packages, please download RAPT (from {a=http://www.renpy.org/dl/android}here{/a}), unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")
    NO_SDK_TEXT = _("RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this.")
    NO_KEY_TEXT = _("RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore.")
    NO_CONFIG_TEXT = _("The current project has not been configured. Use \"Configure\" to configure it before building.")
    OK_TEXT = _("Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device.")

    PHONE_TEXT = _("Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    TABLET_TEXT = _("Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    OUYA_TEXT = _("Attempts to emulate an OUYA console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button.")

    INSTALL_SDK_TEXT = _("Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package.")
    CONFIGURE_TEXT = _("Configures the package name, version, and other information about this project.")
    PLAY_KEYS_TEXT = _("Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details.")
    BUILD_TEXT = _("Builds the Android package.")
    BUILD_AND_INSTALL_TEXT = _("Builds the Android package, and installs it on an Android device connected to your computer.")


    import subprocess

    def find_rapt():

        global RAPT_PATH

        candidates = [ ]

        for fn in os.listdir(config.renpy_base):
            if not fn.startswith("rapt-"):
                continue

            version = fn[5:]
            version = tuple(int(i) for i in version.split('.'))

            candidates.append((version, fn))

        if not candidates:
            RAPT_PATH = None
        else:
            RAPT_PATH = os.path.join(config.renpy_base, candidates[-1][1])

            import sys
            sys.path.insert(0, os.path.join(RAPT_PATH, "buildlib"))

    find_rapt()

    import threading

    if RAPT_PATH:
        import rapt
        import rapt.build
        import rapt.configure
        import rapt.install_sdk
        import rapt.plat
    else:
        rapt = None

    def AndroidState():
        """
        Determines the state of the android install, and returns it.
        """

        if RAPT_PATH is None:
            return ANDROID_NO_RAPT
        if not os.path.exists(os.path.join(RAPT_PATH, "android-sdk/extras/google/play_licensing")):
            return ANDROID_NO_SDK
        if not os.path.exists(os.path.join(RAPT_PATH, "android.keystore")):
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

    class AndroidInterface(object):

        def __init__(self):
            self.process = None
            self.filename = project.current.temp_filename("android.txt")

            self.info_msg = ""

            with open(self.filename, "w"):
                pass

        def info(self, prompt):
            self.info_msg = prompt
            interface.processing(prompt, pause=False)

        def yesno(self, prompt, submessage=None):
            return interface.yesno(prompt, submessage=submessage)

        def yesno_choice(self, prompt, default=None):
            choices = [ (True, "Yes"), (False, "No") ]
            return interface.choice(prompt, choices, default)

        def terms(self, url, prompt):
            submessage = _("{a=%s}%s{/a}") % (url, url)
            return interface.yesno(prompt, submessage=submessage)

        def input(self, prompt, empty=None):

            if empty is None:
                empty = ''

            while True:
                rv = interface.input(_("QUESTION"), prompt, default=empty, cancel=Jump("android"))

                rv = rv.strip()

                if rv:
                    return rv

        def choice(self, prompt, choices, default):
            return interface.choice(prompt, choices, default)

        def fail(self, prompt):
            interface.error(prompt, label="android")

        def success(self, prompt):
            interface.info(prompt, pause=False)

        def final_success(self, prompt):
            interface.info(prompt, label="android")

        def call(self, cmd, cancel=False):

            cmd = [ rapt.plat.path(cmd[0]) ] + list(cmd[1:])
            self.cmd = cmd

            f = open(self.filename, "a")

            f.write("\n\n\n")

            if cancel:
                cancel_action = self.cancel
            else:
                cancel_action = None

            startupinfo = None
            if renpy.windows:
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

            try:
                interface.processing(self.info_msg, show_screen=True, cancel=cancel_action)
                self.process = subprocess.Popen(cmd, cwd=RAPT_PATH, stdout=f, stderr=f, startupinfo=startupinfo)
                renpy.call_screen("android_process", interface=self)
            finally:
                f.close()
                interface.hide_screen()
                self.process = None

        def check_process(self):
            rv = self.process.poll()

            if rv is not None:
                if rv:
                    raise subprocess.CalledProcessError(rv, self.cmd)
                else:
                    return True

        def download(self, url, dest):
            try:
                d = Downloader(url, dest)
                cancel_action = [ d.cancel, Jump("android") ]
                interface.processing(self.info_msg, show_screen=True, cancel=cancel_action, bar_value=DownloaderValue(d))
                ui.timer(.1, action=d.check, repeat=True)
                ui.interact()
            finally:
                interface.hide_screen()

        def background(self, f):
            try:
                t = threading.Thread(target=f)
                t.start()

                interface.processing(self.info_msg, show_screen=True)

                while t.is_alive():
                    renpy.pause(0)
                    t.join(0.25)

            finally:
                interface.hide_screen()


        def cancel(self):
            if self.process:
                self.process.terminate()

            renpy.jump("android")


    class AndroidBuild(Action):
        """
        Activates an Android build process.
        """

        def __init__(self, label):
            self.label = label

        def __call__(self):
            renpy.jump(self.label)

    class LaunchEmulator(Action):

        def __init__(self, emulator, variants):
            self.emulator = emulator
            self.variants = variants

        def __call__(self):

            env = {
                "RENPY_EMULATOR" : self.emulator,
                "RENPY_VARIANT" : self.variants,
                }

            p = project.current
            p.launch(env=env)

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

                            has vbox

                            textbutton _("Phone"):
                                action LaunchEmulator("touch", "small phone touch android")
                                hovered tt.Action(PHONE_TEXT)

                            textbutton _("Tablet"):
                                action LaunchEmulator("touch", "medium tablet touch android")
                                hovered tt.Action(TABLET_TEXT)

                            textbutton _("Television / OUYA"):
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

                            python:
                                if RAPT_PATH:
                                    edit_action = editor.EditAbsolute(os.path.join(RAPT_PATH, "src/org/renpy/android/DownloaderService.java"), check=True)
                                else:
                                    edit_action = None

                            textbutton _("Install SDK & Create Keys"):
                                action Jump("android_installsdk")
                                hovered tt.Action(INSTALL_SDK_TEXT)

                            textbutton _("Configure"):
                                action AndroidIfState(state, ANDROID_NO_CONFIG, Jump("android_configure"))
                                hovered tt.Action(CONFIGURE_TEXT)

                            textbutton _("Edit Google Play Keys"):
                                action AndroidIfState(state, ANDROID_NO_CONFIG, edit_action)
                                hovered tt.Action(PLAY_KEYS_TEXT)

                            textbutton _("Build Package"):
                                action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build"))
                                hovered tt.Action(BUILD_TEXT)

                            textbutton _("Build & Install"):
                                action AndroidIfState(state, ANDROID_OK, AndroidBuild("android_build_and_install"))
                                hovered tt.Action(BUILD_AND_INSTALL_TEXT)



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
    call screen android


label android_installsdk:

    python:
        with interface.nolinks():
            rapt.install_sdk.install_sdk(AndroidInterface())

    jump android


label android_configure:

    python:
        rapt.configure.configure(AndroidInterface(), project.current.path)

    jump android


label android_build:

    python:
        with interface.nolinks():
            rapt.build.build(AndroidInterface(), project.current.path, [ 'release' ])

    jump android


label android_build_and_install:

    python:
        with interface.nolinks():
            rapt.build.build(AndroidInterface(), project.current.path, [ 'release', 'install' ])

    jump android
