label add_file:

    python hide:
        import os
        import codecs
    
        filename = interface.input(_("FILENAME"), _("Enter the name of the script file to create."), filename="withslash", cancel=Jump("navigation"))
       
        if "." in filename and not filename.endswith(".rpy"):
            interface.error(_("The filename must have the .rpy extension."), label="navigation")
        elif "." not in filename:
            filename += ".rpy"
        
        path = os.path.join(project.current.gamedir, filename)
        dir = os.path.dirname(path)
        
        if os.path.exists(path):
            interface.error(_("The file already exists."), label="navigation")
            
        contents = u"\uFEFF"
        contents += _("# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n")
        contents += "\n"
        
        try:
            os.makedirs(dir)
        except:
            pass
            
        contents = u"\uFEFF"
        contents += _("# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n")

        with open(path, "wb") as f:
            f.write(contents.encode("utf-8"))
            
    jump navigation_refresh
    