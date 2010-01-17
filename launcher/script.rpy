init python:
    tutorial_path = config.renpy_base + "/tutorial"
    tutorial_exists = os.path.isdir(tutorial_path)

label main_menu:
    return

label start:
    python:
        choose_default_project()
        scan_editors()
        setup_editor()
        
    jump top

label top:
    python:

        if game_proc and game_proc.poll() is None:
            launch = None
            ui.add(ProcessBehavior(game_proc))
        else:
            launch = ui.jumps("launch")
            game_proc = None
            
        screen()
        
        ui.vbox()
        ui.viewport(draggable=True, ymaximum=47)
        title(project.name.capitalize())

        ui.grid(2, 4, transpose=True)
        
        button(_(u"Launch"),
               launch,
               _(u"Launches the project."))

        button(_(u"Edit Script"),
               ui.jumps("edit_script"),
               _(u"Edits the script of the project."))

        button(_(u"Game Directory"),
               ui.jumps("game_directory"),
               _(u"Opens the project's game directory."))
        
        button(_(u"Check Script (Lint)"),
               ui.jumps("call_lint"),
               _(u"Checks the script of the project for likely errors."))


        button(_(u"Choose Theme"),
               ui.jumps("choose_theme"),
               _(u"Changes the theme used by the project."))
        
        button(_(u"Delete Persistent"),
               ui.jumps("delete_persistent"),
               _(u"Deletes the persistent data associated with the project."))
        
        button(_(u"Archive Files"),
               ui.jumps("archiver"),
               _(u"Archives files found in the game and archived directories."))

        button(_(u"Build Distributions"),
               ui.jumps("distribute"),
               _(u"Builds distributions of the project."))
        
        ui.close()

        title(_(u"Ren'Py"))
        
        ui.grid(2, 4, transpose=True)
        
        button(_(u"Select Project"),
               ui.jumps("select_project"),
               _(u"Select a project to work with."))

        button(_(u"New Project"),
               ui.jumps("new_project"),
               _(u"Create a new project."))

        button(_(u"Ren'Py Games List"),
               ui.jumps("renpy_games_list"),
               _(u"Visit the Ren'Py games list, at http://games.renpy.org."))
        
        button(_(u"Quit"),
               renpy.quit,
               _(u"Causes the launcher to exit."))
        
        button(_(u"Options"),
               ui.jumps("options"),
               _(u"Change Ren'Py launcher options."))

        button(_(u"Ren'Py Help"),
               ui.jumps("documentation"),
               _(u"Open the Ren'Py documentation in a web browser."))

        if tutorial_exists:
        
            button(_(u"Tutorial Game"),
                   ui.jumps("launch_tutorial"),
                   _(u"Launches the Ren'Py tutorial game."))

        else:

            ui.null()

        ui.null()
        

        ui.close()
        ui.close()
        
        interact()

    # ProcessBehavior can return True, which sends us here.
    jump top


label documentation:

    python hide:
        import webbrowser
        webbrowser.open_new("file:///" + config.renpy_base + "/doc/index.html")
        set_tooltip(_(u"Now showing the Ren'Py documentation in your web browser."))

    jump top


label renpy_games_list:
    python hide:
        import webbrowser
        webbrowser.open_new("http://games.renpy.org")
        set_tooltip(_(u"Now showing the Ren'Py Games List in your web browser."))

    jump top
        
label confirm_quit:
    $ renpy.quit()
    
