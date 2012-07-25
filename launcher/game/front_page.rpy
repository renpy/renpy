# Copyright 2004-2012 Tom Rothamel <pytom@bishoujo.us>
# See LICENSE.txt for license details.

define PROJECT_ADJUSTMENT = ui.adjustment()
    
init python:
        
    import os
    import subprocess

    class OpenDirectory(Action):
        """
        Opens `directory` in a file browser. `directory` is relative to
        the project root.
        """
        
        def __init__(self, directory, absolute=False):
            if absolute:
                self.directory = directory
            else:
                self.directory = os.path.join(project.current.path, directory)
            
        def get_sensitive(self):
            return os.path.exists(self.directory)
            
        def __call__(self):

            directory = renpy.fsencode(self.directory)
            
            if renpy.windows:
                os.startfile(directory)
            elif renpy.macintosh:
                subprocess.Popen([ "open", directory ])
            else:
                subprocess.Popen([ "xdg-open", directory ])
            
    # Used for testing.
    def Relaunch():
        renpy.quit(relaunch=True)
    
screen front_page:
    frame:
        style_group "l"
        style "l_root"
        
        has hbox
        
        # Projects list section - on left.
        
        frame:
            style "l_default"
            xmaximum 300
            right_margin 2
            
            top_margin 20
            bottom_margin 26
        
            side "t c b":

                window style "l_label":
                    text "PROJECTS:" style "l_label_text" size 36 yoffset 10 
            
                side "c r":
                    
                    viewport:
                        yadjustment PROJECT_ADJUSTMENT
                        mousewheel True
                        use front_page_project_list
                
                    vbar:
                        style "l_vscrollbar"
                        adjustment PROJECT_ADJUSTMENT
                        
                vbox:
                    add HALF_SPACER
                    add SEPARATOR
                    add HALF_SPACER
                    
                    textbutton _("+ Create New Project"):
                        left_margin (HALF_INDENT)
                        action Jump("new_project")
                    
                
        # Project section - on right.

        if project.current is not None:
            use front_page_project
    
    if project.current is not None:
        textbutton _("Launch Project") action project.Launch() style "l_right_button"
                                                                    
        
                
# This is used by front_page to display the list of known projects on the screen.
screen front_page_project_list:
    
    $ projects = project.manager.projects
    
    vbox:
        
        if projects:
        
            for p in projects:

                textbutton "[p.name!q]":
                    action project.Select(p)
                    style "l_list"
            
            null height 12
            
        textbutton _("Tutorial") action project.Select("tutorial") style "l_list"
        textbutton _("The Question") action project.Select("the_question") style "l_list"

        
# This is used for the right side of the screen, which is where the project-specific 
# buttons are.
screen front_page_project:
    
    $ p = project.current
        
    window:
        
        has vbox

        frame style "l_label":
            has hbox xfill True
            text "[p.name!q]" style "l_label_text"
            label "Active Project" style "l_alternate"

        grid 2 1:
            xfill True
            spacing HALF_INDENT
            
            vbox:
            
                label _("Open Directory") style "l_label_small" 

                frame style "l_indent":
                    has vbox

                    textbutton _("game") action OpenDirectory("game")
                    textbutton _("base") action OpenDirectory(".")
                    # textbutton _("images") action OpenDirectory("game/images") style "l_list"
                    # textbutton _("save") action None style "l_list"
                
            vbox:
            
                label _("Edit File") style "l_label_small"

                frame style "l_indent":
                    has vbox
                
                    textbutton _("script.rpy") action editor.Edit("game/script.rpy", check=True)
                    textbutton _("options.rpy") action editor.Edit("game/options.rpy", check=True)
                    textbutton _("screens.rpy") action editor.Edit("game/screens.rpy", check=True)
                    textbutton _("All script files") action editor.EditAll()
                
        add SPACER
        add SEPARATOR
        add SPACER
        
        frame style "l_indent":
            has vbox
            
            textbutton _("Navigate Script") text_size 30 action Jump("navigation")
        
        add SPACER
        
        grid 2 1:
            xfill True
            spacing HALF_INDENT

            frame style "l_indent":
                has vbox

                textbutton _("Check Script (Lint)") action Jump("lint")
                textbutton _("Change Theme") action Jump("choose_theme")
                textbutton _("Delete Persistent") action Jump("rmpersistent")
                
                # textbutton "Relaunch" action Relaunch

            frame style "l_indent":
                has vbox

                if ability.can_distribute:
                    textbutton _("Build Distributions") action Jump("build_distributions")
                    
        
label main_menu:
    return
    
label start:
    show screen bottom_info
    
label front_page:
    call screen front_page 
    jump front_page
    
    
label lint:
    python hide:

        interface.processing(_("Checking script for potential problems..."))
        lint_fn = project.current.temp_filename("lint.txt")
        
        project.current.launch([ 'lint', lint_fn ], wait=True)
        
        e = renpy.editor.editor
        e.begin(True)
        e.open(lint_fn)
        e.end()

    jump front_page

label rmpersistent:
    
    python hide:
        interface.processing(_("Deleting persistent data..."))
        project.current.launch([ 'rmpersistent' ], wait=True)
        
    jump front_page
    
