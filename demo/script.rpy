init:
    # Set up the size of the screen.
    $ config.screen_width = 800
    $ config.screen_height = 600

    # Positions of things on the screen.
    $ left = Position(xpos=0.0, xanchor='left')
    $ right = Position(xpos=1.0, xanchor='right')
    $ center = Position()

    # Backgrounds.
    image whitehouse = Image("whitehouse.jpg")

    # Character pictures.
    image eileen happy = Image("9a_happy.png")
    image eileen vhappy = Image("9a_vhappy.png")
    image eileen concerned = Image("9a_concerned.png")

    # Character objects.
    $ e = Character('Eileen', color=(200, 255, 200, 255))


# The actual game starts here.
label start:
    
    scene whitehouse
    show eileen vhappy

    "Girl" "Welcome to Ren'Py 4 Preview Release 1."

    show eileen happy

    "Girl" "And welcome to American Bishoujo's southern base, just
            outside of Washington, D.C."

    show eileen happy at left

    "Girl" "This isn't the view from our home base, but it'll do for
            this demo."

    show eileen happy

    "Girl" "My name is Eileen, and while I plan to star in my own game
            one day, for now I'm helping to introduce you to Ren'Py."

    e "Ren'Py is an engine that makes it easy to write visual novel
       games, by taking care of much of the hard work of writing a
       game."

    e "For example, displaying a line of dialogue is a single
       statement. So is displaying a thought or narration."

    "I understand."

    e "Dialogue is easy to write. Just put a string on a line by
       itself, or to the right of an object name or label string."

    e "Since dialogue makes up the bulk of these games, we thought it
       should be easy to write."

    e "Ren'Py can also display menus that let you alter the flow of
       the story."

    menu:
        "Why don't you try a menu out by picking a number?"

        "1":
            show eileen concerned
            e "You picked one. I don't like odd numbers."

        "2":
            show eileen vhappy
            e "You picked two. Even numbers are lucky!"

    show eileen happy

    e "There are a number of statements that control what's displayed
       on the screen. The image statement is used to introduce
       images with names."

    scene

    e "The scene statement can clear the screen..."

    scene whitehouse

    e "... or it can clear the screen and then show a background."

    show eileen happy

    e "The show statement is used to show pictures."

    e "When the show statement is used on an image with the same first
       name (called a tag) as one already shown, it replaces that picture."

    show eileen vhappy

    e "This makes it easy for characters to change emotions."

    hide eileen

    e "The hide statement hides an image."

    show eileen happy at center

    e "A new feature in Ren'Py 4 is the at clause on images, which
       lets you say where you want to show the image at. I can go
       from the center of the screen..."

    show eileen happy at left

    e "... to the left of the screen ..."

    show eileen happy at right

    e "... to the right of the screen ..."

    show eileen happy

    e "... and back to the center."
    
    e "Ren'Py supports a variety of control statements, such as jump,
       call, return, if, and while statements."

    e "Rather than bore you with the details, i'll just tell you to
       check grab the Ren'Py tutorial from http://www.bishoujo.us/renpy/."

    e "That's just about it for writing scripts. Let me show you some
       of the new engine features."

    e "The first feature I can show off is the ability to go
       full-screen. Hit the 'f' key to try it out, and hit 'f'
       again to go back to a window."

    show eileen vhappy

    e "The next feature, rollback, is really neat."

    show eileen happy

    menu:
        "Would you like to see it?"

        "Yes.":
            pass

        "No.":
            jump after_rollback

    e "Rollback lets you play the game backwards."

    e "It lets you go back and reread a line of dialogue you missed,
       or even to go back to a menu and make a different choice if you
       made a mistake."

    e "We do limit the number of steps someone can rollback."

    e "Try it out now, by hitting page up until you get back to the
       menu, and then choose 'No' instead of 'Yes'."

    show eileen concerned

    e "Well, try it."

    e "You want to hit page up."

    e "Well, whatever, your loss. Moving on."
    

label after_rollback:

    show eileen happy

    e "Another new feature works only on Windows. If a game crashes,
       a notepad is brought up showing the crash message, to help
       you debug what went wrong."

    e "The biggest new feature, though, is reasonable
       documentation, which you can read at http://www.bishoujo.us/renpy/."

    show eileen concerned

    e "Since this is just a preview release, there are still a few
       things missing."

    e "For example, there's no support for loading or saving."

    e "We also left out music and animations."

    show eileen happy

    e "Don't worry, though. Those will be coming in the final release,
       which is due out in a few weeks."

    e "You can begin making your own game by editing game/script.rpy. That's
       the script for the game you're playing now."

    e "After you make a change, you have to re-run the game to see
       the change take effect."

    show eileen vhappy

    e "Good luck making your own games!"

    return
