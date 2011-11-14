# Screens that make up the "Welcome" tab.

screen secnav_welcome:

    frame:
        style_group "secnav"
        
        has hbox
        
        textbutton "Projects" action nav.SecPage("projects")

screen projects:
    frame:
        style_group ""
        style "main_frame"

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
        
    
        