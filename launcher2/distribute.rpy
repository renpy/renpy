# This file contains the code needed to build a Ren'Py distribution.

init python:
    import os
    import os.path
    
    def dist_exists(fn):
        """
         Returns true if the given file exists in the renpy directory.
         """
        
        return os.path.exists(os.path.join(config.renpy_base, fn))

    

label distribute:

    # call lint

    # if not yesno("Building Distributions", 
    #              "I've just performed a lint on your project. If it contains errors, you should say no and fix them.\nPlease also check {a=http://www.renpy.org/wiki/renpy/Download_Ren'Py}www.renpy.org{/a} to see if updates or fixes are available.\n\nDo you want to continue?"):

    #     jump top

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
        build_macapp = has_mac and project.info.get("build_mac", False)
        build_all = has_all and project.info.get("build_all", False)

        # The base name of the distribution.
        base_name = project.info.get("distribution_base", project.name)

        # The executable name.
        executable_name = project.info.get("executable_name", project.name)

        # Extensions to exclude.
        ignore_extensions = project.info.get("ignore_extensions", "~ .bak")


        # Prompt the user for all of the above.

        while True:
        
            set_tooltip("")
            screen()
            
            ui.vbox()

            title("Building Distributions")

            text_variable(_("Base Name:"), base_name, "base_name",
                          _("Used to generate the names of directories and archive files."))

            text_variable(_("Executable Name:"), executable_name, "executable_name",
                          _("Used to generate the names of executables and runnable programs."))

            text_variable(_("Ignore Extensions:"), ignore_extensions, "ignore_extensions",
                          _("Files with these extensions will not be included in the distributions."))


            text(_("Distributions to Build:"))

            if has_windows:
                toggle_button(_("Windows x86"), build_windows, ui.returns("build_windows"),
                              _("Zip distribution for the 32-bit Windows platform."))

            if has_linux:
                toggle_button(_("Linux x86"), build_linux, ui.returns("build_linux"),
                              _("Tar.Bz2 distribution for the Linux x86 platform."))

            if has_mac:
                toggle_button(_("Macintosh Universal"), build_mac, ui.returns("build_mac"),
                              _("Zip distribution for the Macintosh x86 and ppc platforms."))

                toggle_button(_("Macintosh Universal Application"), build_macapp, ui.returns("build_macapp"),
                              _("Single application distribution for the Macintosh x86 and ppc platforms."))

            if has_all:
                toggle_button(_("Windows/Linux/Mac Combined"), build_all, ui.returns("build_all"),
                              _("Zip distribution for the Windows x86, Linux x86, Macintosh x86 and Macintosh ppc platforms."))
                

            ui.null(height=15)
            
            button(_("Build"), ui.returns("build"), _("Start building the distributions."))
            button(_("Cancel"), ui.jumps("top", ""), "")

            ui.close()

            act = interact()

            if act == "build_windows":
                build_windows = not build_windows
            elif act == "build_linux":
                build_linux = not build_linux
            elif act == "build_mac":
                build_mac = not build_mac
            elif act == "build_macapp":
                build_macapp = not build_macapp
            elif act == "build_all":
                build_all = not build_all
            elif act == "base_name":

                base_name = input(
                    _("Base Name"),
                    _("Please enter in the base name for your distribution. This name is used to generate the names of directories and archive files. Usually, this is the name of your game, plus a version number, like \"moonlight-1.0\"."),
                    base_name)

            elif act == "executable_name":
                
                executable_name = input(
                    _("Executable Name"),
                    _("Please enter a name for the executables in your distribution. This should not include an extension, as that will be added automatically."),
                    executable_name)
            
            elif act == "ignore_extensions":

                ignore_extensions = input(
                    _("Ignore Extensions"),
                    _("Please enter a space-separated list of file extensions. Files with these extensions will not be included in the built distributions."),
                    ignore_extensions)
                
