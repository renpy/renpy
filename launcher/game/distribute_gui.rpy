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
    class PackageToggle(Action):
        def __init__(self, name):
            self.name = name

        def get_selected(self):
            return self.name in project.current.data['packages']

        def __call__(self):
            packages = project.current.data['packages']

            if self.name in packages:
                packages.remove(self.name)
            else:
                packages.append(self.name)

            project.current.save_data()
            renpy.restart_interaction()

    class DataToggle(Action):
        def __init__(self, field):
            self.field = field

        def get_selected(self):
            return project.current.data[self.field]

        def __call__(self):
            project.current.data[self.field] = not project.current.data[self.field]

            project.current.save_data()
            renpy.restart_interaction()


    DEFAULT_BUILD_INFO = """

## This section contains information about how to build your project into
## distribution files.
init python:

    ## The name that's used for directories and archive files. For example, if
    ## this is 'mygame-1.0', the windows distribution will be in the
    ## directory 'mygame-1.0-win', in the 'mygame-1.0-win.zip' file.
    build.directory_name = "PROJECTNAME-1.0"

    ## The name that's uses for executables - the program that users will run
    ## to start the game. For example, if this is 'mygame', then on Windows,
    ## users can click 'mygame.exe' to start the game.
    build.executable_name = "PROJECTNAME"

    ## If True, Ren'Py will include update information into packages. This
    ## allows the updater to run.
    build.include_update = False

    ## File patterns:
    ##
    ## The following functions take file patterns. File patterns are case-
    ## insensitive, and matched against the path relative to the base
    ## directory, with and without a leading /. If multiple patterns match,
    ## the first is used.
    ##
    ##
    ## In a pattern:
    ##
    ## /
    ##     Is the directory separator.
    ## *
    ##     Matches all characters, except the directory separator.
    ## **
    ##     Matches all characters, including the directory separator.
    ##
    ## For example:
    ##
    ## *.txt
    ##     Matches txt files in the base directory.
    ## game/**.ogg
    ##     Matches ogg files in the game directory or any of its subdirectories.
    ## **.psd
    ##    Matches psd files anywhere in the project.

    ## Classify files as None to exclude them from the built distributions.

    build.classify('**~', None)
    build.classify('**.bak', None)
    build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## To archive files, classify them as 'archive'.

    # build.classify('game/**.png', 'archive')
    # build.classify('game/**.jpg', 'archive')

    ## Files matching documentation patterns are duplicated in a mac app
    ## build, so they appear in both the app and the zip file.

    build.documentation('*.html')
    build.documentation('*.txt')
    """

# A screen that displays a file or directory name, and
# lets the user change it,
#
# title
#     The title of the link.
# value
#     The value of the field.
screen distribute_name:

    add SEPARATOR2

    frame:
        style "l_indent"
        has vbox

        text title

        add HALF_SPACER

        frame:
            style "l_indent"
            text "[value!q]"

    add SPACER


screen build_distributions:

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Build Distributions: [project.current.display_name!q]")

            add HALF_SPACER

            hbox:

                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    use distribute_name(
                        title=_("Directory Name:"),
                        value=project.current.dump["build"]["directory_name"])

                    use distribute_name(
                        title=_("Executable Name:"),
                        value=project.current.dump["build"]["executable_name"])

                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Actions:")

                        add HALF_SPACER

                        frame style "l_indent":

                            has vbox

                            textbutton _("Edit options.rpy") action editor.Edit("game/options.rpy", check=True)
                            textbutton _("Add from clauses to calls, once") action Jump("add_from")
                            textbutton _("Update old-game") action Jump("start_update_old_game")
                            textbutton _("Refresh") action Jump("build_distributions")

                            add HALF_SPACER

                            textbutton _("Upload to itch.io") action Jump("itch")

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

                        text _("Build Packages:")

                        add HALF_SPACER

                        $ packages = project.current.dump["build"]["packages"]

                        for pkg in packages:
                            if not pkg["hidden"]:
                                $ description = pkg["description"]
                                button:
                                    action PackageToggle(pkg["name"]) style "l_checkbox"
                                    hbox:
                                        spacing 3
                                        text "[description!q]"
                                        if pkg["dlc"]:
                                            text _("(DLC)")

                    add SPACER
                    add HALF_SPACER
                    add SEPARATOR2

                    frame:
                        style "l_indent"
                        has vbox

                        text _("Options:")

                        add HALF_SPACER

                        if project.current.dump["build"]["include_update"]:
                            textbutton _("Build Updates") action DataToggle("build_update") style "l_checkbox"

                        textbutton _("Add from clauses to calls") action DataToggle("add_from") style "l_checkbox"
                        textbutton _("Force Recompile") action DataToggle("force_recompile") style "l_checkbox"


    textbutton _("Return") action Jump("front_page") style "l_left_button"
    textbutton _("Build") action Jump("start_distribute") style "l_right_button"

label add_from_common:
    python:
        interface.processing(_("Adding from clauses to call statements that do not have them."))
        project.current.launch([ "add_from" ], wait=True)

    return

label add_from:
    call add_from_common
    jump build_distributions

label start_update_old_game:
    call update_old_game
    jump build_distributions

label add_update_pem:

    python hide:
        interface.info("You're trying to build an update, but an update.pem file doesn't exist.\n\nThis file is used to sign updates, and will be automatically created in your projects's base directory.\n\nYou'll need to back up update.pem and keep it safe.", cancel=Jump("build_distributions"))

        import ecdsa
        key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p).to_pem()

        with open(os.path.join(project.current.path, "update.pem"), "wb") as f:
            f.write(key)

    return

label start_distribute:
    if project.current.dump["build"]["include_update"] and not os.path.exists(os.path.join(project.current.path, "update.pem")):
        call add_update_pem

    if project.current.data["add_from"]:
        call add_from_common

    jump distribute

label build_update_dump:
    python:
        project.current.update_dump(True)

        if project.current.dump.get("error", False):
            interface.error(_("Errors were detected when running the project. Please ensure the project runs without errors before building distributions."))

    return

label build_distributions:

    call build_update_dump

label post_build:

    if not project.current.dump["build"]["directory_name"]:
        jump build_missing

    call screen build_distributions

label build_missing:

    python hide:

        interface.yesno(_("Your project does not contain build information. Would you like to add build information to the end of options.rpy?"), yes=Return(True), no=Jump("front_page"))

        project_name = project.current.name
        project_name = project_name.replace(" ", "_")
        project_name = project_name.replace(":", "")
        project_name = project_name.replace(";", "")

        build_info = DEFAULT_BUILD_INFO.replace("PROJECTNAME", project_name)

        with open(os.path.join(project.current.path, "game", "options.rpy"), "a") as f:
            f.write(build_info)

    jump build_distributions
