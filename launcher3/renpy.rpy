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
        
        label "Settings"
        
        textbutton "Test" action Jump("test")

        text "Settings page."
        
        textbutton "Choose pantyshots?":
            style "checkbox"
            action ToggleField(persistent, "test")

        textbutton "Choose pantyshots?":
            style "checkbox"
            action ToggleField(persistent, "test")



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

screen choose_projects_directory:
    
    frame:
        label "Choose projects directory."    
        text "Please choose the directory containing your projects."

label choose_projects_directory:
    
    show screen choose_projects_directory
    pause 0
    hide screen choose_projects_directory
            
    python hide:
        
        path = persistent.projects_directory
        
        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=path, wanted=str)
            if choice is not None:
                path = choice                

        else:

            try:
                env = os.environ.copy()
    
                if 'RENPY_OLD_LD_LIBRARY_PATH' in env:
                    env['LD_LIBRARY_PATH'] = env['RENPY_OLD_LD_LIBRARY_PATH']
                
                zen = subprocess.Popen(
                    [ "zenity", "--title=Select Projects Directory", "--file-selection", "--directory", "--filename=" + path ],
                    env=env, stdout=subprocess.PIPE)

                choice = zen.stdout.read()        
                zen.wait()

                if choice:
                    path = choice[:-1]
            
            except:
                error(_(u"Could not run zenity. The projects directory has been set to the directory immediately above the directory containing Ren'Py."), None)

        persistent.projects_directory = path                    
    
    
    
    
    
    
    

