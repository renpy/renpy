# Code that manages projects.

init python in project:
    from store import persistent, config, Action, renpy

    import sys
    import os.path
    import json
    import subprocess
    
    class Project(object):
    
        def __init__(self, path):
            
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

            try:
                f = open(os.path.join(path, "project.json"), "rb")
                self.data = json.load(f)
                f.close()
            except:
                self.data = { }
                
        def save(self):
            """
            Saves the project's data dictionary out to disk.
            """

            f = open(os.path.join(path, "project.json"), "rb")
            json.dump(self.data, f)
            f.close()
            
        def launch(self):

            if renpy.renpy.windows and sys.argv[0].endswith(".exe"):
                cmd = [ os.path.join(config.renpy_base, "renpy.exe") ]
            else:
                cmd = [ sys.executable, sys.argv[0] ]
            
            cmd.append(self.path)
            
            subprocess.Popen(cmd)

    
    class ProjectManager(object):
        """
        This maintains a list of the various types of projects that
        we know about.
        """
        
        def __init__(self):
           
           # The projects directory.
           self.projects_directory = persistent.projects_directory
            
           if self.projects_directory and not os.path.isdir(self.projects_directory):
               self.projects_directory = None
           
           # Normal projects, in alpabetical order by lowercase name.
           self.projects = [ ]
           
           # Template projects.
           self.templates = [ ]

           # All projects - normal, template, and hidden.
           self.all_projects = [ ]
           
           # Directories that have been scanned.
           self.scanned = set()
           
           self.scan_projects()
           
        def scan_projects(self):
            """
            Scans for projects.
            """
           
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

        def get(self, name):
            """
            Gets the built-in project with the given name. We search for this
            project relative to renpy_base.

            Returns None if the project doesn't exist.
            """
            
            path = os.path.join(os.path.abspath(config.renpy_base), name)
            
            for p in self.all_projects:
                if p.path == path:
                    return p
                    
            return None
                
                
    manager = ProjectManager()            

    # The current project.
    current = None
    

    # Actions
    class Select(Action):
        """
        An action that causes p to become the selected project when it was
        clicked.
        """
    
        def __init__(self, p):
            self.project = p
            
        def get_selected(self):
            if current is None:
                return False
                        
            return current.path == self.project.path
            
        def get_sensitive(self):
            return self.project is not None
            
        def __call__(self):
            global current
            current = self.project
            renpy.restart_interaction()
            
            
    class Launch(Action):
        """
        An action that launches the supplied project, or the current
        project if no project is supplied.
        """
        
        def __init__(self, p=None):
            if p is None:
                self.project = current
            else:
                self.project = p
            
        def get_sensitive(self):
            return self.project is not None
            
        def __call__(self):
            self.project.launch()
            renpy.notify("Launching {0}...".format(self.project.name))