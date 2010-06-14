# This file contains the code needed to build a Ren'Py distribution.

init 12 python:

    import distribute

    distribute.progress = progress
    distribute.info = info
    distribute._ = _

    def dist_exists(fn):
        """
         Returns true if the given file exists in the renpy directory.
         """

        return os.path.exists(os.path.join(config.renpy_base, fn))

  
label distribute:

    call lint

    if not yesno(_(u"Building Distributions"), 
                 _(u"I've just performed a lint on your project. If it contains errors, you should say no and fix them.\nPlease also check {a=http://www.renpy.org/wiki/renpy/Download_Ren'Py}www.renpy.org{/a} to see if updates or fixes are available.\n\nDo you want to continue?")):

        jump top

    python hide:

        # Do we have the files?
        has_windows = dist_exists("renpy.exe")
        has_linux = dist_exists("lib/linux-x86")
        has_mac = dist_exists("renpy.app")
        has_all = has_windows and has_mac and has_linux

        # Should we build these distributions?
        build_windows = has_windows and project.info.get("build_windows", has_windows)
        build_linux = has_linux and project.info.get("build_linux", has_linux)
        build_mac = has_mac and project.info.get("build_mac", has_mac)
        build_all = has_all and project.info.get("build_all", False)

        # The base name of the distribution.
        base_name = project.info.get("distribution_base", project.name)

        # The executable name.
        executable_name = project.info.get("executable_name", project.name)

        # Extensions to exclude.
        ignore_extensions = project.info.get("ignore_extensions", "~ .bak")

        # Documentation extensions.
        documentation_extensions = project.info.get("documentation_extensions", "txt html")
                
        # Prompt the user for all of the above.

        while True:
        
            set_tooltip("")
            screen()
            
            ui.vbox()

            title(_(u"Building Distributions"))

            text_variable(_(u"Base Name:"), base_name, "base_name",
                          _(u"Used to generate the names of directories and archive files."))

            text_variable(_(u"Executable Name:"), executable_name, "executable_name",
                          _(u"Used to generate the names of executables and runnable programs."))

            text_variable(_(u"Ignore Extensions:"), ignore_extensions, "ignore_extensions",
                          _(u"Files with these extensions will not be included in the distributions."))

            text_variable(_(u"Documentation Extensions:"), documentation_extensions, "documentation_extensions",
                          _(u"Files with these extensions will be treated as documentation, when building the Macintosh application."))

            text(_(u"Distributions to Build:"))

            if has_windows:
                toggle_button(_(u"Windows x86"), build_windows, ui.returns("build_windows"),
                              _(u"Zip distribution for the 32-bit Windows platform."))

            if has_linux:
                toggle_button(_(u"Linux x86"), build_linux, ui.returns("build_linux"),
                              _(u"Tar.Bz2 distribution for the Linux x86 platform."))

            if has_mac:
                toggle_button(_(u"Macintosh Universal"), build_mac, ui.returns("build_mac"),
                              _(u"Single application distribution for the Macintosh x86 and ppc platforms."))

            if has_all:
                toggle_button(_(u"Windows/Linux/Mac Combined"), build_all, ui.returns("build_all"),
                              _(u"Zip distribution for the Windows x86, Linux x86, Macintosh x86 and Macintosh ppc platforms."))
                

            ui.null(height=15)
            
            button(_(u"Build"), ui.returns("build"), _(u"Start building the distributions."))
            button(_(u"Cancel"), ui.jumps("top"), "")

            ui.close()

            act = interact()

            if act == "build_windows":
                build_windows = not build_windows
            elif act == "build_linux":
                build_linux = not build_linux
            elif act == "build_mac":
                build_mac = not build_mac
            elif act == "build_all":
                build_all = not build_all
            elif act == "base_name":

                base_name = input(
                    _(u"Base Name"),
                    _(u"Please enter in the base name for your distribution. This name is used to generate the names of directories and archive files. Usually, this is the name of your game, plus a version number, like \"moonlight-1.0\"."),
                    base_name)

            elif act == "executable_name":
                
                executable_name = input(
                    _(u"Executable Name"),
                    _(u"Please enter a name for the executables in your distribution. This should not include an extension, as that will be added automatically."),
                    executable_name)
            
            elif act == "ignore_extensions":

                ignore_extensions = input(
                    _(u"Ignore Extensions"),
                    _(u"Please enter a space-separated list of file extensions. Files with these extensions will not be included in the built distributions."),
                    ignore_extensions)

            elif act == "documentation_extensions":

                documentation_extensions = input(
                    _(u"Documentation Extensions"),
                    _(u"Please enter a space separated list of documentation extensions. Files in the base directory with these extensions will have a second copy stored outside of the Macintosh application."),
                    documentation_extensions)
                
            elif act == "build":
                break

        # Store the user-selected options in info, and save info.

        project.info["distribution_base"] = base_name
        project.info["executable_name"] = executable_name
        project.info["ignore_extensions"] = ignore_extensions
        project.info["documentation_extensions"] = documentation_extensions

        project.info["build_windows"] = build_windows
        project.info["build_linux"] = build_linux
        project.info["build_mac"] = build_mac
        project.info["build_all"] = build_all

        project.save()

        distribute.distribute(
            project.path,
            config.renpy_base,
            base_name=base_name,
            executable_name=executable_name,
            ignore_extensions=ignore_extensions,
            documentation_extensions=documentation_extensions,
            build_windows=build_windows,
            build_mac=build_mac,
            build_linux=build_linux,
            build_all=build_all)
            
        # Report success to the user.
        set_tooltip(_(u"Thank you for choosing Ren'Py."))

        screen()
        ui.vbox()
        
        title(_(u"Success"))
        text(_(u"The distributions have been built. Be sure to test them before release.\n\nNote that unpacking and repacking the Macintosh, Linux, or Combined distributions on Windows is not supported.\n\nPlease announce your release at the {a=http://lemmasoft.renai.us/forums/}Lemma Soft Forums{/a}, and add it to {a=http://games.renpy.org}games.renpy.org{/a}."))

        ui.null(height=20)

        button(_(u"Return"), ui.jumps("top"), None)
        
        ui.close()
        interact()

