init:

    python:
        # Set up the window.
        config.screen_width = 400
        config.screen_height = 400
        config.window_title = "Ren'Py Launcher"

        # Choose ther roundrect_red theme for the buttons.
        theme.roundrect(
            widget="#559",
            widget_text="#eef",
            widget_hover="#77c",
            disabled="#888",
            disabled_text="#eee",
            )

        # Change the default text color, since we'll be using
        # white as a background.
        style.default.color = "#000"

        style.button.xminimum = 200

        # We don't want the user going into the game menu.
        def interact():
            ui.add(DynamicDisplayable("Text(store.message, size=14, color='#fff', xpos=5, ypos=340, xmaximum=350)"))
            return ui.interact(suppress_underlay=True)

        def title(name):
            ui.text(name, xpos=4, ypos=4, size=30, color="#559")

        def text(name, color="#559", size=18):
            ui.text(name, xalign=0.5, text_align=0.5, color=color, xmaximum=200, size=size)

        def spacer():
            ui.add(Null(1, 6))

        def mid(focus="mid"):
            ui.vbox(ypos=50, yanchor=0, xpos=293, xanchor=0.5, focus=focus)

        def bottom(focus="bottom"):
            ui.vbox(ypos=326, yanchor=1.0, xpos=293, xanchor=0.5, focus=focus)

        def button(text, hover_text="", clicked=None):
            if hover_text:
                def hovered(hover_text=hover_text):
                    if store.message != hover_text:
                        store.message = hover_text
                        renpy.restart_interaction()
            else:
                hovered=None
                        
            ui.button(clicked=clicked, hovered=hovered)
            ui.text(text, style="button_text")
            

        def prompt(name, message, cancel, default='', hint=''):
            store.message = hint

            # Creating the project.
            title(name)

            mid()

            text(message)

            ui.input(default, exclude='{}/\\', xmaximum=200, xalign=0.5, text_align=0.5, color="#000")

            ui.close()

            bottom()
            button("Cancel", clicked=ui.jumps("main"))
            ui.close()

            return interact()


        def paged_menu(tit, choices, message, per_page=7):

            page = 0
            pages = len(choices) / per_page


            while True:

                store.message = message

                title(tit)

                mid(focus="paged_menu")

                for name, desc, ret in choices[page * per_page:(page + 1) * per_page]:
                    button(name, desc, clicked=ui.returns(("return", ret)))
                    
                ui.close()

                bottom()

                if pages > 1:

                    if page < pages:
                        button("Next Page", "Go to the next page of projects.", clicked=ui.returns(("page", page + 1)))
                    else:
                        button("Next Page")

                    if page > 0:
                        button("Previous Page", "Go to the previous page of projects.", clicked=ui.returns(("page", page - 1)))
                    else:
                        button("Previous Page")

                button("Cancel", "Return to the top menu.", ui.jumps("main"))
                        
                ui.close()

                cmd, arg = interact()

                if cmd == "page":
                    page = arg
                    continue

                if cmd == "return":
                    return arg

        class ProcessBehavior(renpy.display.layout.Null):

            def __init__(self, proc):
                super(ProcessBehavior, self).__init__()

                self.proc = proc

            def event(self, ev, x, y, st):

                if self.proc.poll() is not None:
                    return True

                renpy.game.interface.timeout(.25)

        class Project(object):
            def __init__(self, name, path, gamedir, info):
                # name
                self.name = name

                # path to project
                self.path = path

                # gamedir
                self.gamedir = gamedir

                self.info = info

                import re

                def upper(m):
                    return m.group(0).upper()

                title = re.sub(r'^.', upper, name)
                title = re.sub(r'\s+\S', upper, title)
                self.title = title


        def load_project(dir, name):
            import os.path

            if os.path.isdir(dir + "/game"):
                gamedir = dir + "/game"
            elif os.path.isdir(dir + "/data"):
                gamedir = dir + "/data"
            else:
                return

            desc = u"Project found in " + dir + "."

            info = dict()
            info["description"] = desc

            if os.path.exists(dir + "/launcherinfo.py"):
                execfile(dir + "/launcherinfo.py", info)

            store.projects.append(Project(name, dir, gamedir, info))
                
        def load_projects():

            import os
            import os.path

            store.projects = [ ]
            
            cwd = os.getcwd()

            if cwd == config.renpy_base:
                dirs = [ cwd ]
            else:
                dirs = [ config.renpy_base, cwd ]

            for d in dirs:

                contents = os.listdir(d)
                contents.sort()

                for dd in contents:
                    dir = d + "/" + dd

                    if os.path.isdir(dd):
                        load_project(dir, dd)

            if not store.projects:
                raise Exception("The launcher will not function without any projects.")

        def lint():
            
            import renpy.subprocess as subprocess
            import sys

            store.message = "Lint in progress."
            title("Lint")
            ui.pausebehavior(0)
            interact()

            lf = file("lint.txt", "w")

            if hasattr(sys, "winver") and sys.argv[0].lower().endswith(".exe"):
                proc = subprocess.Popen([sys.argv[0], "--lint", project.path], stdout=lf)

            else:
                proc = subprocess.Popen([sys.executable, sys.argv[0], "--lint", project.path], stdout=lf)

            proc.wait()

            lf.close()

            renpy.launch_editor([ "lint.txt" ])



            
    # Set up images.
    image background = "launcher.png"

                




label main_menu:
    return

label start:
    python hide:
        load_projects()

        wanted = persistent.project or "demo"

        for p in projects:
            if p.name == wanted:
                store.project = p
                break
        else:
            store.project = projects[0]


        store.game_proc = None

    scene background

label main:

    python:
        store.message = "What do you want to do?"

label top_menu:
    

    python hide:

        while True:

            title(project.title)

            mid()

            text("This Project")

            if not game_proc or game_proc.poll() is not None:
                clicked = ui.jumps("launch")
            else:
                clicked = None

            button("Launch",
                   "Starts the project running.",
                   clicked=clicked)


            if config.editor:
                button("Edit Script",
                       "Edits the script files.",
                       clicked=ui.jumps("edit"))


            button("Game Directory",
                   "Opens the game directory.",
                   clicked=ui.jumps("game_directory"))



            button("Tools",
                   "Shows the tools menu.",
                   clicked=ui.jumps("tools"))

            spacer()

            text("Change Project")

            button("Select Project",
                   "Select a project to work with.",
                   clicked=ui.jumps("select_project"))

            button("New Project",
                   "Create a new project from a template.",
                   clicked=ui.jumps("new"))

            ui.close()

            bottom()
            button("Quit", "Quit the Ren'Py Launcher.", clicked=ui.jumps("confirm_quit"))
            ui.close()


            if game_proc and game_proc.poll() is None:
                ui.add(ProcessBehavior(game_proc))

            interact()

    jump top_menu

label select_project:

    python hide:

        choices = [ (p.name, p.info["description"], p) for p in projects ]

        store.project = paged_menu("Select a Project", choices, "Please select a project.")

        persistent.project = store.project.name

        store.game_proc = None

    jump main

label launch:

    python hide:
        import renpy.subprocess
        import sys

        if hasattr(sys, "winver") and sys.argv[0].lower().endswith(".exe"):
            proc = renpy.subprocess.Popen([sys.argv[0], project.path])
        
        else:
            proc = renpy.subprocess.Popen([sys.executable, sys.argv[0], project.path])


        store.message = project.title + " has been launched."

        store.game_proc = proc
        

    jump top_menu

            
            
label edit:

    python hide:
        import os

        
        files = [ project.gamedir + "/" + i for i in os.listdir(project.gamedir) if i.endswith(".rpy") if not i[0] == "."]

        files.sort()

        if "options.rpy" in files:
            files.remove("options.rpy")
            files.insert(0, "options.rpy")

        if "script.rpy" in files:
            files.remove("script.rpy")
            files.insert(0, "script.rpy")

        renpy.launch_editor(files)
        
        store.message = "Launched editor with %d script files." % len(files)

    jump top_menu

label game_directory:

    python hide:
        import os
        import os.path
        import platform

        gamedir = os.path.normpath(project.gamedir)

        store.message = "Opening game directory:\n%s" % gamedir

        if platform.win32_ver()[0]:
            os.startfile(gamedir)
        elif platform.mac_ver()[0]:
            import renpy.subprocess as subprocess
            subprocess.Popen([ "open", gamedir ])
        else:
            store.message = "Opening the game directory is not supported on this platform.\n%s" % gamedir

    jump top_menu
                     

label tools:

    $ store.message = "Please choose a tool you want to use with this project."

label tools_menu:

    python hide:

        title("Tools: " + project.title)

        mid()

        text("Anytime")

        button("Check Script (Lint)",
               "Checks the game's script for likely errors. This should be run before releasing.",
               clicked=ui.jumps("lint"))

        button("Quick Backup",
               "Makes a backup copy of the project. You also need to make backups somewhere other then this computer.",
               clicked=ui.jumps("backup"))

        spacer()

        text("Release Day")

        def ifrw(label):
            if project.info["ro"]:
                return None
            else:
                return ui.jumps(label)
            

        button("Add From to Calls",
               "Adds a from clause to each of the call statements in your script.", 
               clicked=ifrw("add_from_to_calls"))
        
        button("Archive Images",
               "Archive the images found under the game directory.",
               clicked=ifrw("archive_images"))
               
        button("Build Distributions",
               "Build distributions for the platforms supported by Ren'Py.",
               clicked=ui.jumps("distribute"))

        ui.close()

        bottom()

        button("Back",
               "Goes back to the top menu.",
               clicked=ui.jumps("main"))

        ui.close()

        interact()
        
label lint:

    python hide:
        lint()

        store.message = "A lint report should appear shortly."

    jump tools_menu
        

label new:

    python hide:

        import os
        import os.path

        choices = [ (p.name, p.info["description"], p) for p in projects if p.info.get("template", None)]

        template = paged_menu("Select a Template", choices, "Please select a project to use as a template for your project.")

        name = prompt("Project Name", "Type the name of your new project, and press enter.\n", "main")

        name = name.strip()

        error = None

        if not name:
            error = "Please enter a non-empty project name."
        elif os.path.exists(name):
            error = "A file or directory named '%s' already exists." % name

        if error:
            title("Error")

            mid()
            text(error)
            ui.close()

            bottom()
            button("Cancel", "Return to the top menu.", clicked=ui.jumps("main"))
            ui.close()

            interact()

            # Shouldn't ever happen.
            renpy.jump("main")

        # Tell the user we're creating the project.
        title("Creating Project")
        store.message = "Please wait while we create the project."
        ui.pausebehavior(0)
        interact()
                    
        # Here is where we actually create the project.

        import shutil

        shutil.copytree(template.path, name)

        unlink = template.info.get("unlink", [ ])
        unlink += [ 'launcherinfo.py' ]

        for i in unlink:
            if os.path.exists(name + "/" + i):
                os.unlink(name + "/" + i)

        persistent.project = name

    jump start

label archive_images:

    python hide:
        import os
        import os.path

        import renpy.tools.archiver as archiver


        # Tell the user we're archiving images.
        title("Archiving Images")
        store.message = "Please wait while we archive images."
        ui.pausebehavior(0)
        interact()


        gamedir = project.gamedir
        archived = project.path + "/archived"

        files = [ ]
        prefix = gamedir + "/images"

        def should_archive(fn):
            fn = fn.lower()

            if fn[0] == ".":
                return False

            if fn.endswith(".png") or fn.endswith(".jpg") or fn.endswith(".gif"):
                return True

            return False

        for bdir in gamedir, archived:

            for dirname, dirs, filenames in os.walk(bdir):

                # Ignore svn.
                dirs[:] = [ i for i in dirs if not i[0] == '.' ]

                for fn in filenames:
                    
                    fullfn = dirname + "/" + fn
                    shortfn = fullfn[len(bdir)+1:]

                    if not should_archive(shortfn):
                        continue

                    files.append((fullfn, shortfn))

        archiver.archive(prefix, files)

        f = file(gamedir + "/images.rpy", "w")
        print >>f, "init:"
        print >>f, "    $ config.archives.append('images')"
        f.close()
                    
        for fullfn, shortfn in files:
            afn = archived + "/" + shortfn

            if fullfn == afn:
                continue

            try:
                os.makedirs(os.path.dirname(afn))
            except:
                pass

            os.rename(fullfn, afn)

        store.message = "The images have been added to the archive, and moved into the archived directory."

    jump tools_menu

label backup:

    python hide:
        import os
        import time
        import shutil

        # Tell the user we're archiving images.
        title("Making Backup")
        store.message = "Please wait while we make a backup."
        ui.pausebehavior(0)
        interact()

        try:
            os.mkdir('backups')
        except:
            pass

        while True:

            btime = time.strftime("%04Y-%02m-%02d-%02H:%02M:%02S")
            bdir = "backups/%s.%s" % (project.name, btime)

            if not os.path.exists(bdir):
                break

            time.sleep(1)

        shutil.copytree(project.path, bdir)

        store.message = "The backup was placed into %s." % bdir

    jump tools_menu
                

label add_from_to_calls:

    python hide:
        import os
        import time
        import shutil

        title("Add From to Calls")
        store.message = "Please wait while we add from clauses to call statements."
        ui.pausebehavior(0)
        interact()

        import renpy.tools.add_from as add_from

        add_from.add_from(project.gamedir, config.commondir)

        store.message = "Done adding from clauses to call statements. You may want to remove the .bak files created."

    jump tools_menu
                
    
    
        
        
label confirm_quit:
    $ renpy.quit()
    
    
