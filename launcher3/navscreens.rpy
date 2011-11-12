screen topnav:
    zorder 100

    frame:
        style_group "topnav"

        has hbox
        
        textbutton "Welcome" action nav.TopPage("projects")
        textbutton "Navigate" action Return(None)
        textbutton "Insert" action Return(None)
        textbutton "Tools" action nav.TopPage("tool1")
        textbutton "Distribute" action Return(None)
        
    textbutton "Launch":
        style "command_button"

        text_font "DejaVuSans-ExtraLight.ttf"
        text_size 18

        xalign 1.0
        xmargin 5
        ymargin 5

        action Return(None)

screen secnav_welcome:

    frame:
        style_group "secnav"
        
        has hbox
        
        textbutton "Projects" action nav.SecPage("projects")
        textbutton "Settings" action nav.SecPage("settings")
        textbutton "Gallery" action Return(None)
                        
                        
screen secnav_tools:

    frame:
        style_group "secnav"
        
        has hbox

        textbutton "Tool1" action nav.SecPage("tool1")
        textbutton "Tool2" action nav.SecPage("tool2")

screen projects:
    frame:
        style_group "launcher"
        
        has vbox

        text "Projects"
        
        hbox:
            style_group "command"
            textbutton "Test Button" action Return(True)
        
        
screen settings:
    frame:
        style_group "launcher"
         
        text "Settings"
        
screen tool1:
    frame:
        style_group "launcher"
         
        text "Tool1"

screen tool2:
    frame:
        style_group "launcher"
         
        text "Tool2"

init python:
    nav.page("projects", "welcome")
    nav.page("settings", "welcome")
    nav.page("tool1", "tools")
    nav.page("tool2", "tools")

