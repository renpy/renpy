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

# Code that manages projects.

init python:
    try:
        import EasyDialogsWin as EasyDialogs
    except:
        EasyDialogs = None

    import os

init python in project:
    from store import persistent, config, Action, renpy
    import store.util as util
    import store.interface as interface

    import sys
    import os.path
    import json
    import subprocess
    import re
    import tempfile

    if persistent.blurb is None:
        persistent.blurb = 0

    LAUNCH_BLURBS = [
        _("After making changes to the script, press shift+R to reload your game."),
        _("Press shift+O (the letter) to access the console."),
        _("Press shift+D to access the developer menu."),
        _("Have you backed up your projects recently?"),
    ]

    class Project(object):

        def __init__(self, path):

            while path.endswith("/"):
                path = path[:-1]

            if not os.path.exists(path):
                raise Exception("{} does not exist.".format(path))

            # The name of the project.
            if path.endswith(".app/Contents/Resources/autorun"):
                self.name = os.path.basename(path[:-len(".app/Contents/Resources/autorun")])
            else:
                self.name = os.path.basename(path)

            # The path to the project.
            self.path = path

            # The path to the game directory.
            gamedir = os.path.join(path, "game")
            if os.path.isdir(gamedir):
                self.gamedir = gamedir
            else:
                self.gamedir = path

            # Load the data.
            self.load_data()

            # The project's temporary directory.
            self.tmp = None

            # This contains the result of dumping information about the game
            # to disk.
            self.dump = { }

            # The mtime of the last dump file loaded.
            self.dump_mtime = 0

        def get_dump_filename(self):
            self.make_tmp()
            return os.path.join(self.tmp, "navigation.json")

        def load_data(self):
            try:
                f = open(os.path.join(self.path, "project.json"), "rb")
                self.data = json.load(f)
                f.close()
            except:
                self.data = { }

            self.update_data()


        def save_data(self):
            """
            Saves the project data.
            """

            try:
                with open(os.path.join(self.path, "project.json"), "wb") as f:
                    json.dump(self.data, f)
            except:
                self.load_data()

        def update_data(self):
            data = self.data

            data.setdefault("build_update", False)
            data.setdefault("packages", [ "all" ])
            data.setdefault("add_from", True)

        def make_tmp(self):
            """
            Makes the project's temporary directory, if it doesn't exist
            yet.
            """

            if self.tmp and os.path.isdir(self.tmp):
                return

            tmp = os.path.join(self.path, "tmp")

            try:
                os.mkdir(tmp)
            except:
                pass

            if os.path.isdir(tmp):
                self.tmp = tmp
                return

            self.tmp = tempfile.mkdtemp()

        def temp_filename(self, filename):
            """
            Returns a filename in the temporary directory.
            """

            self.make_tmp()
            return os.path.join(self.tmp, filename)

        def launch(self, args=[], wait=False, env={}):
            """
            Launches the project.

            `args`
                Additional arguments to give to the project.

            `wait`
                If true, waits for the launched project to terminate before
                continuing.

            `env`
                Additional variables to include in the environment.
            """

            self.make_tmp()

            # Find the python executable to run.
            executable_path = os.path.dirname(sys.executable)

            if renpy.renpy.windows:
                extension = ".exe"
            else:
                extension = ""

            if persistent.windows_console:
                executables = [ "python" + extension ]
            else:
                executables = [ "pythonw" + extension ]

            executables.append(sys.executable)

            for i in executables:
                executable = os.path.join(executable_path, i)
                if os.path.exists(executable):
                    break
            else:
                raise Exception("Python interpreter not found: %r", executables)

            # Put together the basic command line.
            cmd = [ executable, "-EO", sys.argv[0] ]

            cmd.append(self.path)
            cmd.extend(args)

            # Add flags to dump game info.
            cmd.append("--json-dump")
            cmd.append(self.get_dump_filename())

            if persistent.navigate_private:
                cmd.append("--json-dump-private")

            if persistent.navigate_library:
                cmd.append("--json-dump-common")

            environ = dict(os.environ)
            environ.update(env)

            for k in environ:
                environ[k] = renpy.fsencode(environ[k])

            # Launch the project.
            cmd = [ renpy.fsencode(i) for i in cmd ]

            p = subprocess.Popen(cmd, env=environ)

            if wait:
                if p.wait():
                    interface.error(_("Launching the project failed."), _("Please ensure that your project launches normally before running this command."))

        def update_dump(self, force=False, gui=True):
            """
            If the dumpfile does not exist, runs Ren'Py to create it. Otherwise,
            loads it in iff it's newer than the one that's already loaded.
            """

            dump_filename = self.get_dump_filename()

            if force or not os.path.exists(dump_filename):

                if gui:
                    interface.processing(_("Ren'Py is scanning the project..."))

                self.launch(["quit"], wait=True)

            if not os.path.exists(dump_filename):
                self.dump["error"] = True
                return

            file_mtime = os.path.getmtime(dump_filename)
            if file_mtime == self.dump_mtime:
                return

            self.dump_mtime = file_mtime

            try:
                with open(dump_filename, "r") as f:
                    self.dump = json.load(f)
                # add todo list to dump data
                self.update_todos()

            except:
                self.dump["error"] = True

        def update_todos(self):
            """
            Scans the scriptfiles for lines TODO comments and add them to
            the dump data.
            """

            todos = self.dump.setdefault("location", {})["todo"] = {}

            files = self.script_files()

            for f in files:

                data = file(self.unelide_filename(f))

                for l, line in enumerate(data):
                    l += 1

                    try:
                        line = line.decode("utf-8")
                    except:
                        continue

                    m = re.search(ur".*#\s*TODO(\s*:\s*|\s+)(.*)", line, re.I)

                    if m is None:
                        continue

                    raw_todo_text = m.group(2).strip()
                    todo_text = raw_todo_text

                    index = 0

                    while not todo_text or todo_text in todos:
                        index += 1
                        todo_text = u"{0} ({1})".format(raw_todo_text, index)

                    todos[todo_text] = [f, l]


        def unelide_filename(self, fn):
            """
            Unelides the filename relative to the project base.
            """

            fn1 = os.path.join(self.path, fn)
            if os.path.exists(fn1):
                return fn1

            fn2 = os.path.join(config.renpy_base, fn)
            if os.path.exists(fn2):
                return fn2

            return fn

        def script_files(self):
            """
            Return a list of the script files that make up the project. These
            are elided, and so need to be passed to unelide_filename before they
            can be included in the project.
            """

            rv = [ ]
            rv.extend(i for i, isdir in util.walk(self.path)
                if (not isdir) and (i.endswith(".rpy") or i.endswith(".rpym")) and (not i.startswith("tmp/")) )

            return rv


    class ProjectManager(object):
        """
        This maintains a list of the various types of projects that
        we know about.
        """

        def __init__(self):

           # The projects directory.
           self.projects_directory = ""

           # Normal projects, in alphabetical order by lowercase name.
           self.projects = [ ]

           # Template projects.
           self.templates = [ ]

           # All projects - normal, template, and hidden.
           self.all_projects = [ ]

           # Directories that have been scanned.
           self.scanned = set()

           self.scan()

        def scan(self):
            """
            Scans for projects.
            """

            if (persistent.projects_directory is not None) and not os.path.isdir(persistent.projects_directory):
                persistent.projects_directory = None

            self.projects_directory = persistent.projects_directory

            self.projects = [ ]
            self.templates = [ ]
            self.all_projects = [ ]
            self.scanned = set()

            if self.projects_directory is not None:
                self.scan_directory(self.projects_directory)

            self.scan_directory(config.renpy_base)
            self.scan_directory(os.path.join(config.renpy_base, "templates"))

            self.projects.sort(key=lambda p : p.name.lower())
            self.templates.sort(key=lambda p : p.name.lower())

        def scan_directory(self, d):
            """
            Scans for projects in directories directly underneath `d`.
            """

            global current

            d = os.path.abspath(d)

            if not os.path.isdir(d):
                return

            for pdir in util.listdir(d):

                ppath = os.path.join(d, pdir)

                # A project must be a directory.
                if not os.path.isdir(ppath):
                    continue

                autorun = os.path.join(ppath, "Contents", "Resources", "autorun")
                if os.path.exists(autorun):
                    ppath = autorun

                # A project has either a game/ directory, or a project.json
                # file.
                if (not os.path.isdir(os.path.join(ppath, "game"))) and (not os.path.exists(os.path.join(ppath, "project.json"))):
                    continue

                if ppath in self.scanned:
                    continue
                self.scanned.add(ppath)

                # We have a project directory, so create a Project.
                p = Project(ppath)

                project_type = p.data.get("type", "normal")

                if project_type == "hidden":
                    pass
                elif project_type == "template":
                    self.templates.append(p)
                else:
                    self.projects.append(p)

                self.all_projects.append(p)

            # Select the default project.
            if persistent.active_project is not None:
                p = self.get(persistent.active_project)

                if p is not None:
                    current = p
                    return

            p = self.get("tutorial")
            if p is not None:
                current = p
                return

            current = None


        def get(self, name):
            """
            Gets the project with the given name.

            Returns None if the project doesn't exist.
            """

            for p in self.all_projects:
                if p.name == name:
                    return p

            return None

    manager = ProjectManager()

    # The current project.
    current = None

    # Actions
    class Select(Action):
        """
        An action that causes p to become the selected project when it was
        clicked. If label is not None, jumps to the given label.
        """

        def __init__(self, p, label=None):
            """
            `p`
                Either a project object, or a string giving the name of a
                project.

            `label`
                The label to jump to when clicked.
            """

            if isinstance(p, basestring):
                p = manager.get(p)

            self.project = p
            self.label = label

        def get_selected(self):
            if self.project is None:
                return False

            if current is None:
                return False

            return current.path == self.project.path

        def get_sensitive(self):
            return self.project is not None

        def __call__(self):
            global current

            current = self.project
            persistent.active_project = self.project.name

            renpy.restart_interaction()

            if self.label is not None:
                renpy.jump(self.label)


    class Launch(Action):
        """
        An action that launches the supplied project, or the current
        project if no project is supplied.
        """

        def __init__(self, p=None):
            if p is None:
                self.project = current
            elif isinstance(p, basestring):
                self.project = manager.get(p)
            else:
                self.project = p

        def get_sensitive(self):
            return self.project is not None

        def post_launch(self):
            blurb = LAUNCH_BLURBS[persistent.blurb % len(LAUNCH_BLURBS)]
            persistent.blurb += 1

            interface.interaction(_("Launching"), blurb, pause=2.5)


        def __call__(self):
            self.project.launch()
            renpy.invoke_in_new_context(self.post_launch)

    class Rescan(Action):
        def __call__(self):
            """
            Rescans the projects directory.
            """

            manager.scan()
            renpy.restart_interaction()


    manager.scan()

    if isinstance(persistent.projects_directory, str):
        persistent.projects_directory = renpy.fsdecode(persistent.projects_directory)

###############################################################################
# Code to choose the projects directory.

label choose_projects_directory:

    python hide:

        interface.interaction(_("PROJECTS DIRECTORY"), _("Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"), _("This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."),)

        path, is_default = choose_directory(persistent.projects_directory)

        if is_default:
            interface.info(_("Ren'Py has set the projects directory to:"), "[path!q]", path=path)

        persistent.projects_directory = path

        project.manager.scan()

    return

init python:

    def set_projects_directory_command():
        ap = renpy.arguments.ArgumentParser()
        ap.add_argument("projects", help="The path to the projects directory.")

        args = ap.parse_args()

        persistent.projects_directory = args.projects
        renpy.save_persistent()

        return False

    renpy.arguments.register_command("set_projects_directory", set_projects_directory_command)

    def get_projects_directory_command():
        ap = renpy.arguments.ArgumentParser()
        args = ap.parse_args()

        print persistent.projects_directory

        return False

    renpy.arguments.register_command("get_projects_directory", get_projects_directory_command)
