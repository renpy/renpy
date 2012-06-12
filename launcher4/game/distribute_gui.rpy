init python:
    def PlatformToggle(condition, item):
        if condition:
            return [ ToggleDict(project.current.data, item), project.current.save_data ]
        else:
            return None

# This represents a pattern list link.
#
# Parameters:
# patterns
#     The list of patterns in question.
# singular
#     How we refer to the patterns in the singular.
# plural
#     How we refer to the patterns in the plural.
# action
#     What we do when the patterns are clicked.
screen pattern_list_link:
    
    # Projects directory selection.
    $ count = len(patterns)

    if count == 1:
        textbutton singular action action
    else:
        textbutton plural action action

# A screen that displays a file or directory name, and 
# lets the user change it,
#
# title
#     The title of the link.
# value
#     The value of the field.
# action
#     What to do when the link is clicked.
screen name_change_link:
    
    add SEPARATOR2
         
    frame:
        style "l_indent"
        has vbox
        
        text title
        
        add HALF_SPACER
        
        textbutton "[value!q]" action action xpadding INDENT


    add SPACER


screen build_distributions:
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox

            label _("Build Distributions: [project.current.name!q]")
            
            add HALF_SPACER

            hbox:
                
                # Left side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True
                    
                    has vbox

                    use name_change_link(
                        title=_("Directory Name:"),
                        value=project.current.data["directory_name"],
                        action=Jump("change_directory_name"))
                    
                    use name_change_link(
                        title=_("Executable Name:"),
                        value=project.current.data["executable_name"],
                        action=Jump("change_executable_name"))

                    add SEPARATOR2
                         
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("File Patterns:")
                        
                        add HALF_SPACER
                        
                        frame:
                            style "l_indent"
                            
                            has vbox
                        
                            use pattern_list_link(
                                patterns=project.current.data["ignore_patterns"], 
                                singular=_("[count] ignore pattern"),
                                plural=_("[count] ignore patterns"),
                                action=Jump("edit_ignore_patterns"),
                                )

                            add HALF_SPACER

                            use pattern_list_link(
                                patterns=project.current.data["archive_patterns"], 
                                singular=_("[count] archive pattern"),
                                plural=_("[count] archive patterns"),
                                action=Jump("edit_archive_patterns"),
                                )

                            add HALF_SPACER

                            use pattern_list_link(
                                patterns=project.current.data["documentation_patterns"], 
                                singular=_("[count] documentation pattern"),
                                plural=_("[count] documentation patterns"),
                                action=Jump("edit_doc_patterns"),
                                )
                        
                    add SPACER
                        
                    
                # Right side.
                frame:
                    style "l_indent"
                    xmaximum ONEHALF
                    xfill True

                    has vbox

                    add SEPARATOR2
                         
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Build Platforms:")

                        add HALF_SPACER
                        
                        textbutton _("Combined Windows/Mac/Linux") style "l_checkbox": 
                            action PlatformToggle(True, "build_all")
                        
                        textbutton _("Windows x86") style "l_checkbox":
                            action PlatformToggle(True, "build_windows")
                        
                        textbutton _("Macintosh x86") style "l_checkbox":
                            action PlatformToggle(True, "build_mac")

                        textbutton _("Linux x86/x86_64") style "l_checkbox":
                            action PlatformToggle(True, "build_linux")
                                                           
                    add SPACER

                    add SEPARATOR2
                         
                    frame:
                        style "l_indent"
                        has vbox
                        
                        text _("Build Options:")

                        add HALF_SPACER
                        
                        textbutton _("Include update information") style "l_checkbox":
                            action PlatformToggle(True, "include_update")
                        textbutton _("Build update packages") style "l_checkbox":
                            action PlatformToggle(project.current.data["include_update"], "build_update")
                                                           
                    add SPACER


    textbutton _("Back") action Jump("front_page") style "l_left_button"

label change_directory_name:
    python:
        name = interface.input(
            _("DIRECTORY NAME"),
            _("The name that will will be uses for directories containing the project."),
            filename=True,
            cancel=Jump("build_distributions"),
            default=project.current.data["directory_name"])

        name = name.strip()
        if name:
            project.current.data["directory_name"] = name
            project.current.save_data()
        
    jump build_distributions

label change_executable_name:
    python:
        project.current.data["executable_name"] = interface.input(
            _("EXECUTABLE NAME"),
            _("The name that will will be uses for executables that the user can run to start the project."),
            filename=True,
            cancel=Jump("build_distributions"),
            default=project.current.data["executable_name"])

        name = name.strip()
        if name:
            project.current.data["executable_name"] = name
            project.current.save_data()

    jump build_distributions


label build_distributions:
    call screen build_distributions
    