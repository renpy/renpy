# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# Code that manages projects.

init python:
    try:
        import EasyDialogs
    except ImportError:
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
    
    class Project(object):
    
        def __init__(self, path):

            while path.endswith("/"):
                path = path[:-1]

            if not os.path.exists(path):
                raise Exception("{} does not exist.".format(path))
            
            # The name of the project.
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
            self.tmp = os.path.join(self.path, "tmp")
                
            # The path to the json dumpfile.
            self.dump_filename = os.path.join(self.tmp, "navigation.json")
                
            # This contains the result of dumping information about the game
            # to disk.
            self.dump = { }
                
            # The mtime of the last dump file loaded.
            self.dump_mtime = 0

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

        def make_tmp(self):
            """
            Makes the project's temporary directory, if it doesn't exist 
            yet.
            """
            
            try:
                os.mkdir(self.tmp)
            except:
                pass
            
        def temp_filename(self, filename):
            """
            Returns a filename in the temporary directory.
            """
            
            self.make_tmp()
            return os.path.join(self.tmp, filename)
            
        def launch(self, args=[], wait=False):

            self.make_tmp()

            if renpy.renpy.windows and sys.argv[0].endswith(".exe"):
                if persistent.windows_console:
                    cmd = [ os.path.join(config.renpy_base, "console.exe") ]
                else:
                    cmd = [ os.path.join(config.renpy_base, "renpy.exe") ]
            else:
                cmd = [ sys.executable, "-OO", sys.argv[0] ]
 
            cmd.append(self.path)
            cmd.extend(args)
            
            cmd.append("--json-dump")
            cmd.append(self.dump_filename)

            if persistent.navigate_private:
                cmd.append("--json-dump-private")
                
            if persistent.navigate_library:
                cmd.append("--json-dump-common")
                

            with interface.error_handling("launching the project"):
                cmd = [ renpy.fsencode(i) for i in cmd ]
                
                p = subprocess.Popen(cmd)
                
                if wait:
                    p.wait()
                
        def update_dump(self, force=False, gui=True):
            """
            If the dumpfile does not exist, runs Ren'Py to create it. Otherwise, 
            loads it in iff it's newer than the one that's already loaded.
            """

            if force or not os.path.exists(self.dump_filename):
                self.make_tmp()
                
                if gui:
                    interface.processing(_("Ren'Py is scanning the project..."))
                
                self.launch(["quit"], wait=True)
            
            if not os.path.exists(self.dump_filename):
                self.dump["error"] = True
                return
            
            file_mtime = os.path.getmtime(self.dump_filename)
            if file_mtime == self.dump_mtime:
                return

            self.dump_mtime = file_mtime

            try:
                with open(self.dump_filename, "r") as f:
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
    
                    m = re.search(r".*#\s*TODO(\s*:\s*|\s+)(.*)", line, re.I)
    
                    if m is None:
                        continue
                        
                    raw_todo_text = m.group(2).strip()
                    todo_text = raw_todo_text

                    index = 0

                    while not todo_text or todo_text in todos:
                        index += 1
                        todo_text = "{0} ({1})".format(raw_todo_text, index)
                        
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
            rv.extend(i for i, isdir in util.walk(self.path) if (not isdir) and (i.endswith(".rpy") or i.endswith(".rpym")) )

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
            
            for pdir in os.listdir(d):
                ppath = os.path.join(d, pdir)
                
                # A project must be a directory.
                if not os.path.isdir(ppath):
                    continue
                    
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
            
        def __call__(self):
            self.project.launch()

    manager.scan()

    if isinstance(persistent.projects_directory, str):
        persistent.projects_directory = renpy.fsdecode(persistent.projects_directory)

###############################################################################
# Code to choose the projects directory.
            
label choose_projects_directory:
    
    python hide:

        interface.interaction(_("PROJECTS DIRECTORY"), _("Please choose the projects directory."), _("This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."))
            
        path = persistent.projects_directory

        if path:
            
            default_path = path
            
        else:

            try:
                default_path = os.path.dirname(os.path.abspath(config.renpy_base))
            except:
                default_path = os.path.abspath(config.renpy_base)
        

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=default_path, wanted=unicode)

            if choice is not None:
                path = choice                
            else:
                path = None

        else:

            try:
                env = os.environ.copy()
    
                if 'RENPY_ORIGINAL_LD_LIBRARY_PATH' in env:
                    env['LD_LIBRARY_PATH'] = env['RENPY_ORIGINAL_LD_LIBRARY_PATH']

                cmd = [ "zenity", "--title=Select Projects Directory", "--file-selection", "--directory", "--filename=" + renpy.fsencode(default_path) ]

                zen = subprocess.Popen(cmd, env=env, stdout=subprocess.PIPE)

                choice = zen.stdout.read()        
                zen.wait()

                if choice:
                    path = renpy.fsdecode(choice[:-1])
            
            except:
                import traceback
                traceback.print_exc()
                
                path = None
                interface.error(_("Ren'Py was unable to run zenity to choose the projects directory."), label=None)

        if path is None:
            path = default_path
            interface.info(_("Ren'Py has set the projects directory to:"), "[path!q]", path=path)

        path = renpy.fsdecode(path)

        persistent.projects_directory = path                    
        project.manager.scan()
    
    return
