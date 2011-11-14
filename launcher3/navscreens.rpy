screen topnav:
    zorder 100

    frame:
        style_group "topnav"

        has hbox
        
        textbutton "Welcome" action nav.TopPage("projects")
        
    textbutton "Launch":
        style_group ""
        style "_button"
        text_font "DejaVuSans-ExtraLight.ttf"
        text_size 25
        text_kerning -1.5

        xalign 1.0
        top_margin 2

        action project.Launch()

init python:
    nav.page("projects", "welcome")

