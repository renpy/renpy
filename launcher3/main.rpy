image bg mugen = "bgs/mugen-park.jpg"

init python:
    config.developer = True

label start:
    scene bg mugen
    
    show screen topnav
    
    python:
        nav.show_page("projects")
        ui.interact()
    
    