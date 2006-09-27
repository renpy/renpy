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

        def text(name):
            ui.text(name, xalign=0.5, text_align=0.5, color="#559")


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
            


        def paged_menu(tit, choices, message):

            per_page = 8 

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

                ui.close()

                cmd, arg = interact()

                if cmd == "page":
                    page = arg
                    continue

                if cmd == "return":
                    return arg

        class Project(object):
            def __init__(self, name, desc, ro, path):
                # name
                self.name = name

                # description
                self.desc = desc

                # read only flag
                self.ro = ro

                # path to project
                self.path = path

        def load_project(dir, name):
            import os.path

            if not os.path.isdir(dir + "/game") and not os.path.isdir(dir + "/data"):
                return

            desc = u"Project found in " + dir + "."

            info = dict()
            info["description"] = desc
            info["readonly"] = False

            if os.path.exists(dir + "/launcherinfo.py"):
                execfile(dir + "/launcherinfo.py", info)

            store.projects.append(Project(name, info["description"], info["readonly"], dir))
                
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
        store.editor_proc = None

    scene background

label main:

    python:
        store.message = "What do you want to do?"

label top_menu:
    

    python hide:

        title(project.name.title())

        mid()

        text("This Project")


        if not game_proc or game_proc.poll() is not None:
            clicked = ui.jumps("launch")
        else:
            clicked = None

        button("Launch",
               "Starts the project running.",
               clicked=clicked)


        button("Edit Script")
        button("Game Directory")
        button("Tools")
        
        ui.add(Null(1, 22))

        text("Change Project")

        button("Select Project",
               "Select a project to work with.",
               clicked=ui.jumps("select_project"))

        button("New Project")

        ui.close()
        
        bottom()
        button("Quit", "Quit the Ren'Py Launcher.", clicked=ui.jumps("confirm_quit"))
        ui.close()


        ui.pausebehavior(.25)
        
        interact()

    jump top_menu

label select_project:

    python hide:

        choices = [ (p.name, p.desc, p) for p in projects ]

        store.project = paged_menu("Select a Project", choices, "Please select a project.")

        persistent.project = store.project.name

    jump main

label launch:

    python hide:
        import renpy.subprocess
        import sys

        if hasattr(sys, "winver") and sys.argv[0].lower().endswith(".exe"):
            proc = renpy.subprocess.Popen([sys.argv[0], project.path])
        
        else:
            proc = renpy.subprocess.Popen([sys.executable, sys.argv[0], project.path])


        store.message = project.name.title() + " has been launched."

        store.game_proc = proc
        

    jump top_menu

            
            

        
        
label confirm_quit:
    $ renpy.quit()
    
    
