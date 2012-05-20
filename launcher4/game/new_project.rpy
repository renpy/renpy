screen select_template:

    default result = project.manager.get("template")

    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox

            label _("Choose Project Template")

            hbox:

                frame:
                    style "l_indent"
                    xmaximum ONETHIRD
                    
                    viewport:
                        scrollbars "vertical"
                        vbox:
                            for p in project.manager.templates:
                                textbutton "[p.name!q]" action SetScreenVariable("result", p) style "l_list"
                    
                frame:
                    style "l_indent"
                    xmaximum TWOTHIRDS
                    
                    text _("Please select a template to use for your new project. Ren'Py ships with a default template that creates an English-language game with standard screens.")


    textbutton _("Back") action Jump("front_page") style "l_left_button"
    textbutton _("Continue") action Return(result) style "l_right_button"


label new_project:
    
    $ print persistent.projects_directory
    
    if persistent.projects_directory is None:
        call choose_projects_directory
    
    python hide:
        
        project_name = ""
        
        while True:
        
            project_name = interface.input(
                _("PROJECT NAME"), 
                _("Please enter the name of your project:"),
                filename=True,
                cancel=Jump("front_page"),
                default=project_name)
            

            project_dir = os.path.join(persistent.projects_directory, project_name)
            
            if os.path.exists(project_dir):
                pass
                

        template = renpy.call_screen("select_template")
            
    jump front_page
    
    