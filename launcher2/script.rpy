label main_menu:
    return

label start:
    python:
        choose_default_project()
    
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
        
        button(_("Launch"),
               launch,
               _("Launches the project."))

        button(_("Edit Script"),
               ui.jumps("edit_script"),
               _("Edits the script of the project."))

        button(_("Game Directory"),
               ui.jumps("game_directory"),
               _("Opens the project's game directory."))
        
        button(_("Check Script (Lint)"),
               ui.jumps("call_lint"),
               _("Checks the script of the project for likely errors."))


        button(_("Choose Theme"),
               ui.jumps("choose_theme"),
               _("Changes the theme used by the project."))
        
        button(_("Delete Persistent"),
               ui.jumps("delete_persistent"),
               _("Deletes the persistent data associated with the project."))
        
        button(_("Archive Files"),
               ui.jumps("archiver"),
               _("Archives files found in the game and archived directories."))

        button(_("Build Distributions"),
               ui.jumps("distribute"),
               _("Builds distributions of the project."))
               
        ui.close()

        title("Change Project")
        
        ui.grid(2, 1, transpose=True)
        
        button(_("Select Project"),
               ui.jumps("select_project"),
               _("Select a project to work with."))

        button(_("New Project"),
               ui.jumps("new_project"),
               _("Create a new project."))

        ui.close()

        title("Options & Help")

        ui.grid(2, 2, transpose=True)
        
        button(_("Project Directory"),
               ui.jumps("Project directory"),
               _("Select the directory in which the project can be found."))

        button(_("Select Editor"),
               ui.jumps("select_editor"),
               _("Select the text editor to use."))

        button(_("Add-ons"),
               ui.jumps("addons"),
               _("Download additional components for use with Ren'Py."))

        button(_("Ren'Py Help"),
               ui.jumps("documentation"),
               _("Open the Ren'Py documentation in a web browser."))



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


label confirm_quit:
    $ renpy.quit()
    
