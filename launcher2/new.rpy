init python:

    import os
    import os.path
    import shutil
    
label new_project:

    if persistent.projects_directory is None:
        call choose_projects_directory

    python hide:

        name = input(
            _(u"New Project"),
            _(u"Please type the name of your new project."),
            "", cancel='top')

        name = name.strip()

        path = os.path.join(persistent.projects_directory, name)

        set_tooltip("")
        
        if os.path.exists(path):
            error(_(u"Something with that name already exists in the projects directory."))
            
        info(_(u"Creating Project"),
             _(u"Please wait while we create the project."))

        template = os.path.join(config.renpy_base, "template")

        try:
            shutil.copytree(template, path)
        except OSError, e:
            error(_(u"Could not create the project directory. The error was: %s") % unicode(e))
            
        launcherinfo = os.path.join(path, "launcherinfo.py")
        if os.path.exists(launcherinfo):
            os.unlink(launcherinfo)

        # Change the save directory.
        options = file(path + "/game/options.rpy").read()
        save_dir = "%s-%d" % (name, time.time())
        options = options.replace("template-1220804310", save_dir)
        file(path + "/game/options.rpy", "w").write(options)

        p = Project(path)
        p.select()

    jump choose_theme

