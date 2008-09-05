# You can place the script of your game in this file.

init:
    # Declare images below this line, using the image statement.
    # eg. image eileen happy = "eileen_happy.png"

    # Declare characters used by this game.
    $ e = Character('Eileen', color="#c8ffc8")

    image eileen happy = "eileen_happy.png"
    image eileen mad = "eileen_concerned.png"
    image bg green = "#282"

    
label main_menu:
    return
    

label start:

    scene bg green
    
    python:
        k = Klondike(1)
        k.show()

        while True:
            if k.interact():
                break

    "Congratulations!"
    
