# This file handles the launcher options screen.

label options:

    python hide:

        screen()
        ui.vbox()

        title(_(u"Launcher Options"))

        
        text_variable(_("Text Editor"), persistent.editor, "editor",
                      _(u"Change the default text editor."))

        ui.null(height=15)
        
        button(_(u"Return"), ui.jumps("top"), "")

        ui.close()

        act = interact()

        if act == "editor":
            renpy.jump("editor")


    jump options
        

                      
                                                       
