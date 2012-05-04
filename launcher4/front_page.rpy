define PROJECT_ADJUSTMENT = ui.adjustment()
    
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
            ymargin 26
        
            side "t c b":

                window style "l_label":
                    text "PROJECTS:" style "l_label_text" size 32
            
                side "c l":
                    
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
                        left_margin (SCROLLBAR_SIZE + HALF_INDENT)
                        action Return()
                    
                
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

        frame style "l_indent":

            has grid 2 1 xfill True
            
            vbox:
                text _("Open Directory:")
                textbutton _("game") action Return() style "l_list" 
                textbutton _("base") action Return() style "l_list"
                textbutton _("image") action Return() style "l_list"
                textbutton _("save") action Return() style "l_list"
                
            vbox:
                text _("Edit File:")
                textbutton _("script.rpy") action Return() style "l_list"
                textbutton _("options.rpy") action Return() style "l_list"
                textbutton _("screens.rpy") action Return() style "l_list"
                textbutton _("All script files") action Return() style "l_list"
                
        add SPACER
        add SEPARATOR
        add SPACER
        
        frame style "l_indent":
            has vbox
            
            textbutton _("Script Navigation") text_size 30
        
            add SPACER
        
            grid 2 1:
                xfill True
                
                vbox:
                    textbutton _("Check Script (Lint)")
                    textbutton _("Delete Persistent")
                    
                vbox:
                    textbutton _("Build Distributions")
                    
            
        
        
label main_menu:
    return
    
label start:
    show screen bottom_info
    
label front_page:
        
    call screen front_page 
    