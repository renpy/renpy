# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:
    NO_RAPT_TEXT = _("To build Android packages, please download RAPT (from {a=http://www.renpy.org/dl/android}here{/a}), unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")

    PHONE_TEXT = _("Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    TABLET_TEXT = _("Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    OUYA_TEXT = _("Attempts to emulate an OUYA console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button.")

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

    if RAPT_PATH:
        import rapt
        import rapt.build
        import rapt.configure
        import rapt.install_sdk
    else:
        rapt = None


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

            f = open(self.filename, "w")

            f.write("\n\n\n")

            if cancel:
                cancel_action = self.cancel
            else:
                cancel_action = None

            try:
                interface.processing(self.info_msg, show_screen=True, cancel=cancel_action)
                self.process = subprocess.Popen(cmd, cwd=RAPT_PATH, stdout=f, stderr=f)
                renpy.call_screen("android_process", interface=self)
            finally:
                f.close()
                interface.hide_screen()
                self.process = None

        def download(self, url, dest):
            try:
                d = Downloader(url, dest)
                cancel_action = [ d.cancel, Jump("android") ]
                interface.processing(self.info_msg, show_screen=True, cancel=cancel_action, bar_value=DownloaderValue(d))
                ui.timer(.1, action=d.check, repeat=True)
                ui.interact()
            finally:
                interface.hide_screen()

        def check_process(self):
            rv = self.process.poll()

            if rv is not None:
                if rv:
                    raise subprocess.CalledProcessError(rv)
                else:
                    return True

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
        color "#000"
        font "Roboto-Light.ttf"
        xpos 75
        ypos 350

    timer .1 action interface.check_process repeat True
    timer .2 action ft.update repeat True


screen android:

    default tt = Tooltip(NO_RAPT_TEXT)

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

                            textbutton _("Install SDK & Create Keys") action Jump("android_installsdk")
                            textbutton _("Configure") action Jump("android_configure")
                            textbutton _("Build Package") action AndroidBuild("android_build")
                            textbutton _("Build & Install") action AndroidBuild("android_build_and_install")

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

                        text tt.value

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
