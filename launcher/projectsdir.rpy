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


label choose_projects_directory:

    python hide:

        set_tooltip("")
        
        info(_(u"Choose Projects Directory"),
             _(u"Please choose the directory containing your projects."))


        path = persistent.projects_directory
        
        if path is None:
            path = os.path.dirname(config.renpy_base)
            path = os.environ.get("RENPY_DEFAULT_PROJECTS_DIRECTORY", path)
            

        if EasyDialogs:

            choice = EasyDialogs.AskFolder(defaultLocation=path, wanted=str)
            if choice is not None:
                path = choice                

        else:

            try:

                env = os.environ.copy()
                if 'RENPY_OLD_LD_LIBRARY_PATH' in env:
                    env['LD_LIBRARY_PATH'] = env['RENPY_OLD_LD_LIBRARY_PATH']
                
                zen = subprocess.Popen([ "zenity", "--title=Select Projects Directory", "--file-selection", "--directory", "--filename=" + path ],
                                       env=env, stdout=subprocess.PIPE)

                choice = zen.stdout.read()        
                zen.wait()

                if choice:
                    path = choice[:-1]
            
            except:
                error(_(u"Could not run zenity. The projects directory has been set to the directory immediately above the directory containing Ren'Py."), None)

        persistent.projects_directory = path                    
        choose_default_project()

    return
                               
