# This file handles the launcher options screen.

label options:

    python hide:

        screen()
        ui.vbox()

        title(_(u"Launcher Options"))

        editor = persistent.editor
        if not set_editor:
            editor = _(u"Using RENPY_EDITOR")
        
        text_variable(_("Text Editor"), editor, "editor",
                      _(u"Change the default text editor."))

        ui.null(height=15)

        button(_(u"Projects Directory"),
               ui.jumps("options_cpd"),
               _(u"Select the directory Ren'Py searches for projects."))

        ui.null(height=15)
        
        button(_(u"Return"), ui.jumps("top"), "")

        ui.close()

        act = interact()

        if act == "editor":
            renpy.jump("editor")


    jump options
        
label options_cpd:
    call choose_projects_directory
    jump options
    
