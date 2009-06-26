init python:
    import os
    import os.path
    import sys
    import platform
    import subprocess
    

    ZWSP = u"\u200B"

    game_proc = None
    
    class ProcessBehavior(renpy.display.layout.Null):

        def __init__(self, proc):
            super(ProcessBehavior, self).__init__()
            
            self.proc = proc

        def event(self, ev, x, y, st):

            if self.proc.poll() is not None:
                return True
                
            renpy.game.interface.timeout(.25)

    def quote_char(c):
        n = ord(c)
        if 0x20 <= n <= 0x7f:
            return c
        else:
            return "\\x%02x" % n

    # Quotes an arbitrary string (without knowing the encoding) for display.
    def quote(s):
        s ="".join(quote_char(i) for i in s)
        s = s.replace("/", "/" + ZWSP)
        s = s.replace("\\", "\\" + ZWSP)
        return s
        
    class Project(object):

        def __init__(self, path):
            # The name of the project.
            self.name = os.path.basename(path) 
            
            # The full path to the project.
            self.path = path

        def __repr__(self):
            return "<Project %r>" % (self.path)

        def select(self):
            """
             Select this project as the one that we're working on.
             """

            global project
            global game_proc
            
            persistent.project_path = self.path
            project = self
            game_proc = None
            
            
    def scan_projects():
        
        rv = [ ]
        
        project_dirs = [ config.renpy_base ]

        if persistent.projects_directory:
            project_dirs.append(persistent.projects_directory)

        for d in project_dirs:

            if not os.path.isdir(d):
                continue
            
            for pd in os.listdir(d):
                path = os.path.join(d, pd)

                if not os.path.isdir(path):
                    continue
                
                gamedir = os.path.join(path, "game")

                if not os.path.isdir(gamedir):
                    continue

                rv.append(Project(path))

        return rv
    

    def choose_default_project():

        project = None
        projects = scan_projects()

        for i in projects:
            if i.path == persistent.project_path:
                i.select()
                return

        for i in projects:
            if i.name == "demo":
                i.select()
                return

        if projects:
            projects[0].select()
            return

        
    def select_project(p):
        p.select()
        renpy.jump("top")
        
    curried_select_project = renpy.curry(select_project)
        
label select_project:

    python:

        screen()

        ui.vbox()

        title(_("Select Project"))
        scrolled("top")

        ui.vbox()
        
        projects = scan_projects()

        for i in projects:

            button(i.name,
                   curried_select_project(i),
                   quote(i.path))

        ui.close() # vbox            
        ui.close() # scrolled
        ui.close() # vbox

        interact()

label launch:
    
    python hide:

        
        if sys.platform == "win32" and sys.argv[0].lower().endswith(".exe"):
            proc = subprocess.Popen([sys.argv[0], project.path])
        else:
            proc = subprocess.Popen([sys.executable, sys.argv[0], project.path])

        set_tooltip(_("%s has been launched.") % project.name.capitalize())

        store.game_proc = proc

    jump top


label game_directory:

    python hide:
        gamedir = os.path.normpath(os.path.join(project.path, "game"))

        if sys.platform == "win32":
            os.startfile(gamedir)
        elif platform.mac_ver()[0]:
            subprocess.Popen([ "open", gamedir ])
        else:
            subprocess.Popen([ "xdg-open", gamedir ])

        gamedir = quote(gamedir)
        set_tooltip(_(u"Opening game directory:\n%s") % gamedir)
            
    jump top
