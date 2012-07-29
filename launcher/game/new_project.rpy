# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init python:
    import shutil
    import os
    import time
    import re

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
    
    if persistent.projects_directory is None:
        call choose_projects_directory
    
    python hide:
        
        project_name = interface.input(
            _("PROJECT NAME"), 
            _("Please enter the name of your project:"),
            filename=True,
            cancel=Jump("front_page"))
        
        project_name = project_name.strip()
        if not project_name:
            interface.error(_("The project name may not be empty."))

        project_dir = os.path.join(persistent.projects_directory, project_name)
        
        if project.manager.get(project_name) is not None:
            interface.error(_("[project_name!q] already exists. Please choose a different project name."), project_name=project_name)
        
        if os.path.exists(project_dir):
            interface.error(_("[project_dir!q] already exists. Please choose a different project name."), project_dir=project_dir)

        if len(project.manager.templates) == 1:
            template = project.manager.templates[0]
        else:
            template = renpy.call_screen("select_template")

        template_path = template.path
        
        with interface.error_handling("creating a new project"):
            shutil.copytree(template_path, project_dir)
        
            # Delete the tmp directory, if it exists.
            if os.path.isdir(os.path.join(project_dir, "tmp")):
                os.path.rmtree(os.path.join(project_dir, "tmp"))
            
            # Delete project.json, which must exist.
            os.unlink(os.path.join(project_dir, "project.json"))
                
            # Change the save directory in options.rpy
            fn = os.path.join(project_dir, "game/options.rpy")
            with open(fn, "rb") as f:
                options = f.read().decode("utf-8")

            save_dir = project_name + "-" + str(int(time.time()))
            options = re.sub(r'template-\d+', save_dir, options)
            
            with open(fn, "wb") as f:
                f.write(options.encode("utf-8"))

        # Activate the project.
        with interface.error_handling("activating the new project"):
            project.manager.scan()
            project.Select(project.manager.get(project_name))()
        
    call choose_theme_callable

    jump front_page
    
    
