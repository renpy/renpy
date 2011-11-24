# Screens that make up the "Welcome" tab.

screen secnav_renpy:

    frame:
        style_group "secnav"
        
        has hbox
        
        textbutton "Projects" action page.Secondary("projects")
        textbutton "Settings" action page.Secondary("settings")

screen projects:
    frame:
        style_group ""
        style "page"

        has viewport: 
            scrollbars True
            mousewheel True

        has vbox

        text "Welcome to Ren'Py. Please select a project to work with."
        
        if project.manager.projects:
            label "My projects:"
        
            hbox:
                style_group "choice"
        
                box_wrap True
        
                for p in project.manager.projects:
                    textbutton "[p.name!q]":
                        size_group "project"
                        action project.Select(p)
                        right_padding 30                                            
      
        textbutton "Create a new project" action Return(None) 

        label "Example projects:"

        vbox:
            style_group "choice"
            
            $ p = project.manager.get("tutorial")
            if p:            

                hbox:
                    textbutton "Ren'Py Tutorial":
                        action project.Select(p)
                        size_group "project"
    
                    textbutton "(quick launch)":
                        style "link"
                        action project.Launch(p)


            $ p = project.manager.get("the_question")
            if p:

                hbox:
                    textbutton "The Question":
                        action project.Select(p)
                        size_group "project"
    
                    textbutton "(quick launch)":
                        style "link"
                        action project.Launch(p)
        

screen settings:

    frame:
        style_group ""
        style "page"

        has vbox
        
        label "My Projects"
        
        textbutton "Select 'My Projects' directory" action Jump("choose_projects_directory")
        
        label "Launcher Settings"
        
        textbutton "Launcher uses transitions":
            style "checkbox"
            action ToggleField(persistent, "launcher_uses_transitions")

# Projects directory handling.

init python:

    import os
    import subprocess

    try:
        import EasyDialogs
    except ImportError:
        try:
            import EasyDialogsWin as EasyDialogs
        except:
            EasyDialogs = None

    
    
    
    
    
    
    

