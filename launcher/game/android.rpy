# Copyright 2004-2013 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:
    NO_RAPT_TEXT = _("To build Android packages, please download RAPT (from {a=http://www.renpy.org/dl/android}here{/a}), unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")

    PHONE_TEXT = _("Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    TABLET_TEXT = _("Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button.")
    OUYA_TEXT = _("Attempts to emulate an OUYA console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button.")

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

    find_rapt()


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

                            textbutton _("Install SDK & Create Keys")
                            textbutton _("Configure")
                            textbutton _("Build Package")
                            textbutton _("Build & Install")

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
    