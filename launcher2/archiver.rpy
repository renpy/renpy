init python:
    import renpy.tools.archiver as archiver
    import os
    import os.path
    import fnmatch
    
label archiver:

    python hide:

        # Get the options
        name = project.info.get('archive_name', "data")
        include = project.info.get('archive_include', "*.png *.gif *.jpg")
        exclude = project.info.get('archive_exclude', "presplash.png")

        # Allow the user to set the options.
        while True:

            set_tooltip("")

            screen()
            ui.vbox()
            
            title(_(u"Archiver"))

            text(_(u"The archiver allows you to obfuscate your game by including files in an archive file."))

            ui.null(height=15)
            
            text_variable(_(u"Archive Name:"), name, "name",
                          _(u"The name of the archive to create."))

            text_variable(_(u"Include Patterns:"), include, "include",
                          _(u"Files matching these patterns are included in the archive."))

            text_variable(_(u"Exclude Patterns:"), exclude, "exclude",
                          _(u"Files matching these patterns are excluded from the archive."))

            ui.null(height=15)

            button(_(u"Archive"), ui.returns("archive"), _(u"Build the archive."))
            button(_(u"Cancel"), ui.jumps("top"), "")

            ui.close()

            act = interact()

            if act == "name":
                name = input(
                    _(u"Archive Name"),
                    _(u"The name of the archive file to create, without the .rpa extension.\n\nThe \"data\" archive is loaded automatically. Other archives must be added to config.archives."),
                    name)
                       
            elif act == "include":
                include = input(
                    _(u"Include Patterns"),
                    _(u"This is a space-separated list of file patterns. Files matching these patterns are added to the archive.\n\nAsterisks (*) can be used as a wildcard."),
                    include)

            elif act == "exclude":
                exclude = input(
                    _(u"Include Patterns"),
                    _(u"This is a space-separated list of file patterns. Files matching these patterns are excluded from the archive. If a file is matched by both an exclude and include pattern, the exclude takes precedence.\n\nAsterisks (*) can be used as a wildcard."),
                    exclude)

            elif act == "archive":
                break

        # Store the options.
            
        project.info["archive_name"] = name
        project.info["archive_include"] = include
        project.info["archive_exclude"] = exclude

        project.save()


        # Break up the extension lists.

        include = [ i.strip() for i in include.split() ]
        exclude = [ i.strip() for i in exclude.split() ]

        # Get the gamedir and the archived dir.
        gamedir = os.path.join(project.path, "game")
        archived = os.path.join(project.path, "archived")

        # The prefix of the archive file.
        prefix = os.path.join(gamedir, name)

        archived_files = set()
        files = [ ]
        
        # Choose files to archive.

        set_tooltip("")
        
        info(
            _(u"Scanning Files..."),
            "")
        
        for bdir in (gamedir, archived):
            
            for dirname, dirs, filenames in os.walk(bdir):
                
                dirs[:] = [ i for i in dirs if not i[0] == '.' ]

                for fn in filenames:

                    fullfn = dirname + "/" + fn
                    shortfn = fullfn[len(bdir)+1:]

                    if fn[0] == ".":
                        continue
                    
                    if shortfn in archived_files:
                        continue

                    should_archive = False

                    for i in include:
                        if fnmatch.fnmatch(fn, i):
                            should_archive = True

                    for i in exclude:
                        if fnmatch.fnmatch(fn, i):
                            should_archive = False

                    if not should_archive:
                        continue

                    files.append((fullfn, shortfn))
                    archived_files.add(shortfn)

        if not files:
            error(_(u"The patterns did not match any files, so no archive was created."))
                    
        # Actually archiving files.
        info(_(u"Archiving Files..."), "")
                    
        archiver.archive(prefix, files)

        # Move files out of the way.
        for fullfn, shortfn in files:
            afn = archived + "/" + shortfn

            if fullfn == afn:
                continue

            try:
                os.makedirs(os.path.dirname(afn))
            except:
                pass

            try:
                os.rename(fullfn, afn)
            except:
                os.rename(afn, afn + ".old")
                os.rename(fullfn, afn)
                os.unlink(afn + ".old")

        # Report success.
        screen()
        ui.vbox()
        
        title(_(u"Success"))
        text(_(u"The files have been added to the archive, and moved into the \"archived\" directory. Future runs of the archiver will archive files in both the \"game\" and \"archived\" directories."))

        ui.null(height=20)

        button(_(u"Return"), ui.jumps("top"), None)
        
        ui.close()
        interact()

            
        
        
