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
                        
                        textbutton _("Combined Windows/Mac/Linux zip") style "l_checkbox": 
                            action PlatformToggle(True, "build_all")
                        
                        textbutton _("Windows x86 zip") style "l_checkbox":
                            action PlatformToggle(True, "build_windows")
                        
                        textbutton _("Macintosh x86 application zip") style "l_checkbox":
                            action PlatformToggle(True, "build_mac")

                        textbutton _("Linux x86/x86_64 tar.bz2") style "l_checkbox":
                            action PlatformToggle(True, "build_linux")
                                                           
                    add SPACER
                    null height 6

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
    textbutton _("Build") action Jump("distribute") style "l_right_button"


# Shows the list of file patterns to the user, and allows the user to
# edit that list.
#
# title
#     The title of this file patterns section.
# patterns
#     The list of file patterns that are being exited.
# description
#     A description of what the patterns are being used for.
screen edit_file_patterns:
    
    frame:
        style_group "l"
        style "l_root"
        
        window:
    
            has vbox

            label title
            
            add HALF_SPACER

            hbox:
                
                # Left side.
                frame:
                    style "l_indent"
                    xmaximum 300
                    xfill True
                    
                    
                    viewport:
                        scrollbars "vertical"
                        
                        has vbox
                        
                        for p in patterns:
                            
                            hbox:
                                xfill True

                                text "[p!q]"

                                textbutton "×":
                                    xalign 1.0
                                    action RemovePattern(patterns, p)
                                    xpadding 6
                                    text_hover_color HOVER
                                    text_color DANGER
                            
                            
                    
                # Right side.
                frame:
                    style "l_indent"
                    xmaximum 454
                    xfill True

                    has vbox

                    text description
                    
                    add SPACER
                    add SPACER
                    
                    input style "l_default" size 24 xalign 0.5 default "" color "#d86b45"

                    add SPACER
                    add SPACER
   
                    text _("To add a new pattern, type it and press enter.") style "l_small_text"
   
                    add HALF_SPACER
                
                    text _("In these patterns, / is the directory separator, * matches any character but the directory separator, and ** matches any character.") style "l_small_text"
                    
                    add HALF_SPACER
                    
                    text _("For example, background/*.jpg matches JPG files in the background directory, while bg/**.jpg includes files in subdirectories.") style "l_small_text"


    textbutton _("Back") action Jump("build_distributions") style "l_left_button"

init python:
    
    class RemovePattern(object):
        def __init__(self, patterns, pattern):
            self.patterns = patterns
            self.pattern = pattern
            
        def __call__(self):
            if self.pattern in self.patterns:
                self.patterns.remove(self.pattern)
                
            project.current.save_data()
            renpy.restart_interaction()
    
    def edit_file_patterns(patterns, title, description):
        patterns.sort(key = lambda a : a.lower())
        
        while True:
            rv = renpy.call_screen("edit_file_patterns", patterns=patterns, title=title, description=description)
            patterns.append(rv)
            patterns.sort(key = lambda a : a.lower())
            
            project.current.save_data()
            
        
label edit_ignore_patterns:
    
    python:
        edit_file_patterns(
            project.current.data['ignore_patterns'],
            title=_("Ignore Patterns"),
            description=_("If a file is matched by an ignore pattern, it is not included in the distribution. Ignore patterns are relative to the base directory."))

label edit_archive_patterns:
    
    python:
        edit_file_patterns(
            project.current.data['archive_patterns'],
            title=_("Archive Patterns"),
            description=_("If a file is matched by an archive pattern, it is added to an archive file. This prevents casual users from seeing the file. Archive patterns are relative to the game directory."))

label edit_doc_patterns:
    
    python:
        edit_file_patterns(
            project.current.data['documentation_patterns'],
            title=_("Documentation Patterns"),
            description=_("If a file is matched by a documentation pattern, it is added to the root directory of a Macintosh zip, outside of the application. Documentation patterns are relative to the base directory."))


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
    