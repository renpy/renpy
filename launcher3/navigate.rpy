screen secnav_navigate:

    frame:
        style_group "secnav"
        
        has hbox
        
        textbutton "Files" action page.Secondary("files")
        textbutton "Settings" action page.Secondary("settings")

screen files:    
    
    default dtt = Tooltip("Select a directory to open it.")
    
    frame:
        xfill True
        style "page"
        style_group ""
    
        has vbox
        
        label "Script Files"
        
        text "Click on the name of a file to open it in the editor."
        
        
        label "Open Directories"

        text "[dtt.value!q]"

        hbox:

            textbutton "Game Directory":
                action Return(True)
                hovered dtt.Action("Game assets should be placed in this directory.")
                size_group "directory"
                
            textbutton "Image Directory":
                action Return(True)
                hovered dtt.Action("Images in this directory will be auto-defined.")
                size_group "directory"
                
            textbutton "Base Directory":
                action Return(True)
                hovered dtt.Action("README files should be placed in this directory.")
                size_group "directory"
    
            textbutton "Save Directory":
                action Return(True)
                hovered dtt.Action("The directory that contains the project's save files.")
                size_group "directory"
                    
        