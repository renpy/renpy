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
    else:
        rapt = None


    class AndroidInterface(object):

        def info(self, prompt):
            interface.info(prompt, pause=False)

        def yesno(self, prompt, default=None):
            choices = [ (True, "Yes"), (False, "No") ]
            return interface.choice(prompt, choices, default)

        def terms(self, url, prompt):
            submessage = _("{a=%s}%s{/a}") % (url, url)
            return interface.yesno(prompt, submessage)

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

        def call(self, cmd):
            subprocess.check_call(cmd, cwd=RAPT_PATH)


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
    $ interface.choice("Can I ask you a question?", [ (1, "Yes, you can."), (2, "No, way.") ], 1)
    jump android

label android_configure:

    python:

        rapt.configure.configure(
            AndroidInterface(),
            project.current.path,
            )

    jump android

label android_build:

    python:
        rapt.build.build(AndroidInterface(), project.current.path, [ 'release' ])

    jump android

label android_build_and_install:

    python:
        rapt.build.build(AndroidInterface(), project.current.path, [ 'release', 'install' ])

    jump android
