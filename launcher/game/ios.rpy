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

init python:
    IOS_NO_RENIOS = 0
    IOS_NO_DIRECTORY = 1
    IOS_NO_PROJECT = 2
    IOS_OK = 3

    IOS_NO_RENIOS_TEXT = _("To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher.")
    IOS_NO_DIRECTORY_TEXT = _("The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it.")
    IOS_NO_PROJECT_TEXT = _("There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one.")
    IOS_OK_TEXT = _("An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it.")

    IPHONE_TEXT = _("Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down.")
    IPAD_TEXT = _("Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down.")

    IOS_SELECT_DIRECTORY_TEXT = _("Selects the directory where Xcode projects will be placed.")
    IOS_CREATE_PROJECT_TEXT = _("Creates an Xcode project corresponding to the current Ren'Py project.")
    IOS_UPDATE_PROJECT_TEXT = _("Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes.")
    IOS_XCODE_TEXT = _("Opens the Xcode project in Xcode.")

    IOS_OPEN_DIRECTORY_TEXT = _("Opens the directory containing Xcode projects.")

    def find_renios():

        global RENIOS_PATH

        candidates = [ ]

        RENIOS_PATH = os.path.join(config.renpy_base, "renios")

        if os.path.isdir(RENIOS_PATH) and check_hash_txt("renios"):
            import sys
            sys.path.insert(0, os.path.join(RENIOS_PATH, "buildlib"))
        else:
            RENIOS_PATH = None

    find_renios()

    if RENIOS_PATH:
        import renios.create
        import renios.image

    def IOSState():
        if not RENIOS_PATH:
            return IOS_NO_RENIOS
        elif not persistent.xcode_projects_directory:
            return IOS_NO_DIRECTORY
        elif not os.path.exists(xcode_project()):
            return IOS_NO_PROJECT
        else:
            return IOS_OK

    def IOSStateText(state):
        if state == IOS_NO_RENIOS:
            return IOS_NO_RENIOS_TEXT
        elif state == IOS_NO_DIRECTORY:
            return IOS_NO_DIRECTORY_TEXT
        elif state == IOS_NO_PROJECT:
            return IOS_NO_PROJECT_TEXT
        else:
            return IOS_OK_TEXT

    def IOSIfState(state, needed, action):
        """
        If `state` is `needed` or better, `action` is returned. Otherwise,
        returns None, disabling the button.
        """

        if state >= needed:
            return action
        else:
            return None

    xcode_name_cache = { }

    def xcode_name(s):
        """
        Returns a version of `s` that's safe to use in Xcode.
        """

        if s in xcode_name_cache:
            return xcode_name_cache[s]

        s = re.sub(r'[^\w\-\.]', '', s)
        xcode_name_cache[s] = s
        return s

    def xcode_project(p=None, target=None):
        """
        Return the path to the Xcode project corresponding to `p`, or the current
        project if `p` is None
        """

        if target is not None:
            return target

        if p is None:
            p = project.current

        if persistent.xcode_projects_directory is None:
            raise Exception("The Xcode projects directory has not been set.")

        return os.path.join(persistent.xcode_projects_directory, xcode_name(p.name))

    def ios_create(p=None, gui=True, target=None):
        project.current.update_dump(force=True, gui=gui)

        name = project.current.dump.get("name", None)
        version = project.current.dump.get("version", None)

        dest = xcode_project(p, target)

        if gui:
            iface = MobileInterface("ios")
        else:
            iface = rapt.interface.Interface()

        if os.path.exists(dest):
            if not iface.yesno(_("The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?")):
                return

            i = 0
            while True:
                i += 1
                backup = dest + "." + str(i)
                if not os.path.exists(backup):
                    break

            os.rename(dest, backup)

        renios.create.create_project(iface, dest, name, version)

        ios_populate(p, gui=gui, target=target)


    def eliminate_pycache(directory):
        """
        Eliminates the __pycache__ directory, and moves the files in it up a level,
        renaming them to remove the cache tag.
        """

        print("Eliminating __pycache__...")

        if PY2:
            return

        import pathlib
        import sys

        paths = list(pathlib.Path(directory).glob("**/__pycache__/*.pyc"))

        for p in paths:
            name = p.stem.partition(".")[0]
            p.rename(p.parent.parent / (name + ".pyc"))

        paths = list(pathlib.Path(directory).glob("**/__pycache__"))

        for p in paths:
            p.rmdir()


    def ios_populate(p=None, gui=True, target=None):
        """
        This actually builds the package.
        """

        import shutil

        if p is None:
            p = project.current

        dist = os.path.join(xcode_project(p, target), "base")

        if os.path.exists(dist):
            shutil.rmtree(dist)

        if gui:
            reporter = distribute.GuiReporter()
        else:
            reporter = distribute.TextReporter()

        distribute.Distributor(p,
            reporter=reporter,
            packages=[ 'ios' ],
            build_update=False,
            noarchive=True,
            packagedest=dist,
            report_success=False,
            )

        eliminate_pycache(dist)

        main_fn = os.path.join(dist, "main.py")

        for fn in os.listdir(dist):
            if fn.endswith(".py"):
                py_fn = os.path.join(dist, fn)
                break
        else:
            raise Exception("Could not find a .py file.")

        with open(py_fn, "r") as py_f:
            with open(main_fn, "w") as main_f:
                for l in py_f:
                    if l.startswith("#!"):
                        continue

                    main_f.write(l)

        os.unlink(py_fn)

        ios_image(p, "ios-icon.png", "Media.xcassets/AppIcon.appiconset", True, target)
        # ios_image(p, "ios-launchimage.png", "Media.xcassets/LaunchImage.launchimage", False, target)

    def ios_image(p, source, destination, scale, target):
        source = os.path.join(p.path, source)
        destination = os.path.join(xcode_project(p, target), destination)

        renios.image.generate(source, destination, scale)


    def launch_xcode():
        dist = xcode_project(None)

        if not os.path.exists(dist):
            return

        for fn in os.listdir(dist):
            if fn.endswith(".xcodeproj"):
                xcodeproj = os.path.join(dist, fn)
                subprocess.call([ 'open', renpy.fsencode(xcodeproj) ])

                break


screen ios:

    default tt = Tooltip(None)
    $ state = IOSState()

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("iOS: [project.current.display_name!q]")

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

                            textbutton _("iPhone"):
                                action LaunchEmulator("ios-touch", "small phone touch ios mobile")
                                hovered tt.Action(IPHONE_TEXT)

                            textbutton _("iPad"):
                                action LaunchEmulator("ios-touch", "medium tablet touch ios mobile")
                                hovered tt.Action(IPAD_TEXT)


                    add SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Build:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Select Xcode Projects Directory"):
                                action IOSIfState(state, IOS_NO_DIRECTORY, Jump("select_xcode_projects_directory"))
                                hovered tt.Action(IOS_SELECT_DIRECTORY_TEXT)

                            textbutton _("Create Xcode Project"):
                                action IOSIfState(state, IOS_NO_PROJECT, Jump("create_xcode_project"))
                                hovered tt.Action(IOS_CREATE_PROJECT_TEXT)

                            textbutton _("Update Xcode Project"):
                                action IOSIfState(state, IOS_NO_PROJECT, Jump("update_xcode_project"))
                                hovered tt.Action(IOS_UPDATE_PROJECT_TEXT)

                            if renpy.macintosh:
                                textbutton _("Launch Xcode"):
                                    action IOSIfState(state, IOS_OK, launch_xcode)
                                    hovered tt.Action(IOS_XCODE_TEXT)

                            add SPACER

                            textbutton _("Force Recompile") action DataToggle("force_recompile") style "l_checkbox"

                    add SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Other:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Open Xcode Projects Directory"):
                                action IOSIfState(state, IOS_NO_PROJECT, OpenDirectory(persistent.xcode_projects_directory, absolute=True))
                                hovered tt.Action(IOS_OPEN_DIRECTORY_TEXT)


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

                        text _("There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices.")

                        add SPACER

                        if tt.value:
                            text tt.value
                        else:
                            text IOSStateText(state)


    textbutton _("Return") action Jump("front_page") style "l_left_button"


label ios:

    if RENIOS_PATH is None:
        $ interface.yesno(_("Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"), no=Jump("front_page"))
        $ add_dlc("renios", restart=True)

    call screen ios

label select_xcode_projects_directory:

    python hide:

        interface.interaction(_("XCODE PROJECTS DIRECTORY"), _("Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"))

        path, is_default = choose_directory(persistent.xcode_projects_directory)

        if is_default:
            interface.info(_("Ren'Py has set the Xcode Projects Directory to:"), "[path!q]", path=path)

        persistent.xcode_projects_directory = path

    jump ios

label create_xcode_project:

    $ ios_create(None, True)

    jump ios

label update_xcode_project:
    $ ios_populate(None, True)

    jump ios

init python:

    def ios_create_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("project", help="The path to the Ren'Py project.")
        ap.add_argument("destination", help="The path the iOS project that will be created.")

        args = ap.parse_args()

        p = project.Project(args.project)

        ios_create(p, False, args.destination)

        return False

    renpy.arguments.register_command("ios_create", ios_create_command)


    def ios_populate_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("project", help="The path to the Ren'Py project.")
        ap.add_argument("destination", help="The path the iOS project that will be created.")

        args = ap.parse_args()

        p = project.Project(args.project)

        ios_populate(p, False, args.destination)

        return False

    renpy.arguments.register_command("ios_populate", ios_populate_command)
