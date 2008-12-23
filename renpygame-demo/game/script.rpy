# You can place the script of your game in this file.

init:
    # Declare images below this line, using the image statement.
    image bg m64 = "m64.jpg"
    image eileen happy = "eileen_happy.png"

    # Declare characters used by this game.
    $ e = Character('Eileen', color="#c8ffc8")

    $ import aliens
    

# The game starts here.
label start:

    scene bg m64
    show eileen happy at left
    
    e "Welcome!"

    e "You're here to defend the moon from invaders from the M-64 galaxy."

    e "You can move your van back and forth with the arrow keys, and then press space to fire a missile."

    e "Good luck!"

label retry:

    $ renpy.free_memory()
    $ score = aliens.main()

    # This eats up any remaining keypresses.
    $ renpy.pause(.1)
    
    e "You shot down %(score)d aliens."

    if score > 10:

        e "Not bad!"

    menu:

        "Would you like to try again?"

        "Sure.":

            "Okay, get ready..."

            jump retry

        "No thanks.":

            pass

    e "No problem."

    e "This game was based off one of the examples that came with pygame."

    e "It shows how pygame games can be integrated with Ren'Py."

    e "Thank you for playing."

    return


        
