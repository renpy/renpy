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

# Editor Support.
#
# This contains code for scanning for editors, and for allowing the user to
# select an editor.

init 1 python in editor:

    from store import Action, renpy, config, persistent
    import store.project as project
    import store.updater as updater
    import store.interface as interface
    import store.util as util
    import store

    import glob
    import re
    import traceback
    import os
    import os.path

    # Should we set up the editor?
    set_editor = "RENPY_EDIT_PY" not in os.environ

    # A map from editor name to EditorInfo object.
    editors = { }

    class EditorInfo(object):
        def __init__(self, filename):
            # The path to the editor info file.
            self.filename = filename

            # The name of the editor.
            self.name = os.path.basename(filename)[:-len(".edit.py")]

            # The time the editor file was last modified. We use this
            # to decide if we should update the editors mat when we
            # have multiple versions of an editor in contention.
            self.mtime = os.path.getmtime(filename)

    def scan_editor(filename):
        """
        Inserts an editor into editors if there isn't a newer
        editor there already.
        """

        ei = EditorInfo(filename)

        if ei.name in editors:
           if editors[ei.name].mtime >= ei.mtime:
               return

        editors[ei.name] = ei

    def scan_all():
        """
        Finds all *.edit.py files, and uses them to populate the list
        of editors.
        """

        editors.clear()

        for d in [ config.renpy_base, persistent.projects_directory ]:
            if d is None:
                continue

            if not os.path.isdir(d):
                continue

            for i in util.listdir(d):
                i = os.path.join(d, i)
                if not os.path.isdir(d):
                    continue

                for j in util.listdir(i):
                    j = os.path.join(i, j)

                    if j.endswith(".edit.py"):
                        scan_editor(j)

    ########################################################################

    # A list of fancy_editor_info objects.
    fancy_editors = [ ]

    # The error message to display if an editor failed to start.
    error_message = None

    class FancyEditorInfo(object):
        """
        Represents an editor in the selection screen. A FEI knows if the
        editor is installed or not.
        """

        def __init__(self, priority, name, description=None, dlc=None, dldescription=None, error_message=None):
            # The priority of the editor. Lower priorities will come later
            # in the list.
            self.priority = priority

            # The name of the editor.
            self.name = name

            # Is the editor installed?
            self.installed = name in editors

            # The dlc needed to install the editor.
            self.dlc = dlc

            # A description of the editor.
            self.description = description

            # A description of the download.
            self.dldescription = dldescription

            # An error message to display if the editor failed to start.
            self.error_message = error_message

    def fancy_scan_editors():
        """
        Creates the list of FancyEditorInfo objects.
        """

        import platform

        global fancy_editors

        scan_all()

        fei = fancy_editors = [ ]

        # Atom.
        AD = _("(Recommended) A modern and approachable text editor.")

        if renpy.windows:
            dlc = "atom-windows"
            installed = os.path.exists(os.path.join(config.basedir, "atom/atom-windows"))
        elif renpy.macintosh:
            dlc = "atom-mac"
            installed = os.path.exists(os.path.join(config.basedir, "atom/Atom.app"))
        else:
            dlc = "atom-linux"
            installed = os.path.exists(os.path.join(config.basedir, "atom/atom-linux-" + platform.machine()))

        e = FancyEditorInfo(
            0,
            "Atom",
            AD,
            dlc,
            _("Up to 150 MB download required."),
            None)

        e.installed = e.installed and installed

        fei.append(e)


        # Editra.
        ED  = _("A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input.")
        EDL  = _("A mature editor. Editra lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython.")

        if renpy.windows:
            dlc = "editra-windows"
            installed = os.path.exists(os.path.join(config.basedir, "editra/editra.exe"))
            description = ED
            error_message = None
        elif renpy.macintosh:
            dlc = "editra-mac"
            installed = os.path.exists(os.path.join(config.basedir, "editra/Editra-mac.app"))
            description = ED
            error_message = None
        else:
            dlc = "editra-linux"
            installed = os.path.exists(os.path.join(config.basedir, "editra/Editra"))
            description = EDL
            error_message = _("This may have occured because wxPython is not installed on this system.")

        e = FancyEditorInfo(
            1,
            "Editra",
            description,
            dlc,
            _("Up to 22 MB download required."),
            error_message)

        e.installed = e.installed and installed

        fei.append(e)

        # jEdit
        fei.append(FancyEditorInfo(
            2,
            "jEdit",
            _("A mature editor that requires Java."),
            "jedit",
            _("1.8 MB download required."),
            _("This may have occured because Java is not installed on this system."),
            ))

        fei.append(FancyEditorInfo(
            3,
            _("System Editor"),
            _("Invokes the editor your operating system has associated with .rpy files."),
            None))

        for k in editors:
            if k in [ "Atom", "Editra", "jEdit", "System Editor", "None" ]:
                continue

            fei.append(FancyEditorInfo(
                4,
                k,
                None,
                None))

        fei.append(FancyEditorInfo(
            5,
            _("None"),
            _("Prevents Ren'Py from opening a text editor."),
            None))

        fei.sort(key=lambda e : (e.priority, e.name.lower()))

        # If we're in a linux distro or something, assume all editors work.
        if not updater.can_update():
            for i in fei:
                i.installed = True

    def fancy_activate_editor(default=False):
        """
        Activates the editor in persistent.editor, if it's installed.

        `default`

        """

        global error_message

        fancy_scan_editors()

        if default and not set_editor:
            renpy.editor.init()
            return

        for i in fancy_editors:

            if i.name == persistent.editor:
                if i.installed and i.name in editors:
                    ei = editors[i.name]
                    os.environ[b"RENPY_EDIT_PY"] = renpy.fsencode(os.path.abspath(ei.filename))
                    error_message = i.error_message
                    break

        else:
            persistent.editor = None
            os.environ.pop(b"RENPY_EDIT_PY", None)

        renpy.editor.init()

    def fancy_select_editor(name):
        """
        Selects the editor with the given name, installing it if it
        doesn't already exist.
        """

        for fe in fancy_editors:
            if fe.name == name:
                break
        else:
            return

        if not fe.installed:

            # We don't check the status of this because fancy_activate_editor
            # will fail if the editor is not installed.
            store.add_dlc(fe.dlc)

        persistent.editor = fe.name
        fancy_activate_editor()

        return persistent.editor is not None

    # Call fancy_activate_editor on startup.
    fancy_activate_editor(True)

    class SelectEditor(Action):
        def __init__(self, name):
            self.name = name

        def get_selected(self):
            return persistent.editor == self.name

        def __call__(self):
            return fancy_select_editor(self.name)


    def check_editor():
        """
        Checks to see if an editor is set. If one isn't asks the user to
        select one.

        Returns True if the editor is set and editing can proceed, and
        False otherwise.
        """

        if not set_editor:
            return True

        if persistent.editor and persistent.editor != "None":
            return True

        return renpy.invoke_in_new_context(renpy.call_screen, "editor")

    ##########################################################################
    # Editing actions.


    class Edit(Action):
        alt = _("Edit [text].")

        def __init__(self, filename, line=None, check=False):
            """
            An action that opens the given line of the given file in a
            text editor.

            `filename`
                The filename to open.

            `line`
                The line in the file to jump to.

            `check`
                If true, we will check to see if the file exists, and gray
                out the box if it does not.
            """

            self.filename = filename
            self.line = line
            self.check = check

        def get_sensitive(self):
            if not self.check:
                return True

            fn = project.current.unelide_filename(self.filename)
            return os.path.exists(fn)

        def __call__(self):

            if not self.get_sensitive():
                return

            if not check_editor():
                return

            fn = project.current.unelide_filename(self.filename)

            try:

                e = renpy.editor.editor

                e.begin()
                e.open(fn, line=self.line)
                e.end()

            except Exception, e:
                exception = traceback.format_exception_only(type(e), e)[-1][:-1]
                renpy.invoke_in_new_context(interface.error, _("An exception occured while launching the text editor:\n[exception!q]"), error_message, exception=exception)

    class EditAbsolute(Action):
        def __init__(self, filename, line=None, check=False):
            """
            An action that lets us edit an absolutely-specified filename.

            `filename`
                The filename to open.

            `line`
                The line in the file to jump to.

            `check`
                If true, we will check to see if the file exists, and gray
                out the box if it does not.
            """

            self.filename = filename
            self.line = line
            self.check = check

        def get_sensitive(self):
            if not self.check:
                return True

            return os.path.exists(self.filename)

        def __call__(self):

            if not self.get_sensitive():
                return

            if not check_editor():
                return

            try:

                e = renpy.editor.editor

                e.begin()
                e.open(self.filename, line=self.line)
                e.end()

            except Exception, e:
                exception = traceback.format_exception_only(type(e), e)[-1][:-1]
                renpy.invoke_in_new_context(interface.error, _("An exception occured while launching the text editor:\n[exception!q]"), error_message, exception=exception)


    class EditAll(Action):
        """
        Opens all scripts that are part of the current project in a web browser.
        """

        def __init__(self):
            return

        def __call__(self):

            if not check_editor():
                return

            scripts = project.current.script_files()
            scripts = [ i for i in scripts if not i.startswith("game/tl/") ]
            scripts.sort(key=lambda fn : fn.lower())

            for fn in [ "game/screens.rpy", "game/options.rpy", "game/script.rpy" ]:
                if fn in scripts:
                    scripts.remove(fn)
                    scripts.insert(0, fn)

            try:

                e = renpy.editor.editor
                e.begin()

                for fn in scripts:
                    fn = project.current.unelide_filename(fn)
                    e.open(fn)

                e.end()

            except Exception, e:
                exception = traceback.format_exception_only(type(e), e)[-1][:-1]
                renpy.invoke_in_new_context(interface.error, _("An exception occured while launching the text editor:\n[exception!q]"), error_message, exception=exception)


    class EditProject(Action):
        """
        Opens the project's base directory in an editor.
        """

        def __call__(self):

            if not check_editor():
                return

            try:

                e = renpy.editor.editor

                e.begin()
                e.open_project(project.current.path)
                e.end()

            except Exception, e:
                exception = traceback.format_exception_only(type(e), e)[-1][:-1]
                renpy.invoke_in_new_context(interface.error, _("An exception occured while launching the text editor:\n[exception!q]"), error_message, exception=exception)


    def CanEditProject():
        """
        Returns True if EditProject can be used.
        """

        try:
            e = renpy.editor.editor
            return e.has_projects
        except:
            return False


screen editor:

    frame:
        style_group "l"
        style "l_root"

        window:

            has vbox

            label _("Select Editor")

            add HALF_SPACER

            hbox:
                frame:
                    style "l_indent"
                    xfill True

                    viewport:
                        scrollbars "vertical"
                        mousewheel True

                        has vbox

                        text _("A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed.") style "l_small_text"

                        for fe in editor.fancy_editors:

                            add SPACER

                            textbutton fe.name action editor.SelectEditor(fe.name)

                            add HALF_SPACER

                            frame:
                                style "l_indent"
                                has vbox

                                if fe.description:
                                    text fe.description style "l_small_text"

                                if not fe.installed:
                                    add HALF_SPACER
                                    text fe.dldescription style "l_small_text"


    textbutton _("Cancel") action Return(False) style "l_left_button"

label editor_preference:
    call screen editor
    jump preferences
