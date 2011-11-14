image bg mugen = "bgs/mugen-park.jpg"

init -1 python:
    config.developer = True
    config.quit_action = Quit(confirm=False)

label start:
    scene bg mugen
    
    show screen topnav
    
    python:
        nav.show_page("projects")
        ui.interact()
    
    