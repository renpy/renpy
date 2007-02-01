label new:

    python hide:

        import os
        import os.path


        # Select a template.
        
        choices = [ (p.name, p.info["description"], p, None) for p in projects if p.info.get("template", None)]

        template = paged_menu("Select a Template", choices, "Please select a project to use as a template for your project.")

        # Choose project name.
        
        name = prompt("Project Name", "Type the name of your new project, and press enter.\n", "main")
        name = name.strip()

        error = None

        if not name:
            error = "Please enter a non-empty project name."
        elif os.path.exists(name):
            error = "A file or directory named '%s' already exists." % name
        else:
            try:
                name = name.encode("ascii")
            except:
                error = "Project names must be ASCII. This is because archive file formats do not support non-ASCII characters in a uniform way."
                
        if error:
            store.error("Error", error, "main")

        # Tell the user we're creating the project.
        title("Creating Project")
        store.message = "Please wait while we create the project."
        ui.pausebehavior(0)
        interact()
                    
        # Here is where we actually create the project.

        import shutil

        shutil.copytree(template.path, name)

        unlink = template.info.get("unlink", [ ])
        unlink += [ 'launcherinfo.py' ]

        for i in unlink:
            if os.path.exists(name + "/" + i):
                os.unlink(name + "/" + i)

        persistent.project = name

    call find_project from _call_find_project_2

label choose_theme:

    python hide:
        
        # Select a color scheme.
        
        themes = theme_data.keys()
        themes.sort()
        
        choices = [ ]
        for i in themes:

            def hovered(i=i):
                td = theme_data[i].copy()
                engine = td["theme"]
                del td["theme"]

                if engine == "roundrect":
                    renpy.style.restore(style_backup)
                    theme.roundrect(launcher=True, **td)
                    renpy.style.rebuild()
                    return ("repeat", 0)

            choices.append((i, None, i, hovered))

        color_theme = paged_menu("Select a Theme", choices, "Please select a color theme for your project. You can always change the colors later.", cancel='color_theme_cancel')

        # Restore default theme.
        renpy.style.restore(style_backup)
        theme.roundrect(launcher=True)
        renpy.style.rebuild()

        ofn = project.path + "/game/options.rpy"

        import os
        import re

        if not os.path.exists(ofn):
            error("Changing Theme", "The options file does not seem to exist.", "main")
        
        inf = file(ofn, "rU")
        outf = file(ofn + ".new", "wU")

        td = theme_data[color_theme]

        # TODO: Make this less specific to roundrect. Need to figure out
        # how to switch themes, rather than just recolor them.

        changing = False
        changed = False
        
        for l in inf:

            if re.match(r'\s*theme.roundrect\(', l):
                changing = True
                changed = True
            elif re.match(r'\s*\)', l):
                changing = False
            elif changing:

                def repl(m, td=td):
                    return m.group(1) + m.group(2) + " = \"" + td.get(m.group(2), m.group(3)) + "\","

                l = re.sub(r'^(\s*)(\w+) = "([\da-fA-F#]+)",', repl, l)
                
            outf.write(l)

        outf.close()
        inf.close()

        os.rename(ofn + ".new", ofn)
        
        if not changed:
            error("Changing Theme", "Could not modify options.rpy, perhaps it was edited too much.", "main")
        
    jump main
        


label color_theme_cancel:

    python hide:

        # Restore default theme.
        renpy.style.restore(style_backup)
        theme.roundrect(launcher=True)
        renpy.style.rebuild()

    jump main
