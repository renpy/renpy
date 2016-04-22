# You can place the script of your game in this file.

# Declare images below this line, using the image statement.
# eg. image eileen happy = "eileen_happy.png"

# Declare characters used by this game.
define e = Character('Eileen', color="#c8ffc8")
define n = NVLCharacter("Eileen", color="#c8ffc8")

# label main_menu:
#     return

label replay:

    "Test"

    $ renpy.end_replay()

define nn = NVLCharacter(None)
define narrator = nn

# init python:
#     menu = nvl_menu
#     config.narrator_menu = False

define config.sample_sound = "foo.opus"

# The game starts here.
label start:
    scene bg mugen

    e "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes, or just because it is perfectly fine."

    n "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes."

    menu:
        "This is an nvl menu"
        "A relatively long menu choice name thing is sort of bi":
            pass
        "Choice 2":
            pass

    n "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes."
    n "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes."
    n "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes."
    n "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes."
    n "This is a relatively long block of text. Long enough that, if it naturally wraps, it's going to fill the whole text box. That is, if we make it long enough. Which takes a lot of typing, but might be worth it for testing purposes."


    n "This is the first text block."

    nn "This is the second text block."

    n "And this is the third text block, for what it is worth. And I think it's worth a lot, especially if we wrap the lines."



    e "Hi, everybody!"

    "This is the new history screen that's being added to Ren'Py during NaNoRenO 2016. Some people would call this a readback or log screen."

    "I can't help but think this is long overdue."

    e "It took a while, but better late than never, right?"


#     show screen skip_indicator_test
#
#     "It was just an ordinary, everyday village, stuck between two opposing kingdoms."
#     "And for the Kodokushi, that was reason enough."
#     "After joining the Kodokushi, I quickly realized that our work was neither noble, nor righteous."
#     n "We were not saviors of the people. We were not almighty defenders, protecting innocent civilians from harm."
#     "We were a death squad."
#     "Every day we would venture forth, treading just a little bit further away from home, searching for \"the enemy\"."
#     "It was just an ordinary, everyday village, stuck between two opposing kingdoms."
#     n "And for the Kodokushi, that was reason enough."
#     n "After joining the Kodokushi, I quickly realized that our work was neither noble, nor righteous."
#     "We were not saviors of the people. We were not almighty defenders, protecting innocent civilians from harm."
#     "We were a death squad."
#     "Every day we would venture forth, treading just a little bit further away from home, searching for \"the enemy\"."
#     "An honorable task, to be sure. We would drive away any threats before they could further encroach upon our land, taking the fight away from innocent passersby."

    $ save_name = "Chapter 1: The chaptering, brought to you by the chapter."


    $ renpy.notify("How is this?")

label loop2:

    e "Hello, world. This is the new default ADV-mode screen and the new skip indicator."

    e "Let me ask you a question."

    jump loop2

    $ renpy.run(Replay("replay", locked=False))

    $ renpy.input("Are you a turtle?", default="You bet your sweet ass I am.")

    menu:
        "This is a choice."

        "This is the first choice.":
            pass

        "This is the second choice. It's much longer, probably long enough to be split to multiple lines.":
            pass

    e "Is this particularly hard to read? No, I don't think so. Do you? But what happens when I add a lot more text to it - to the point where it wraps not once, not twice, but three times - leading to four lines in all. With more text like this."

    scene bg lwa desk

    "LWA!"

    scene expression "#ccc"

    "..."

    $ renpy.input("Hello, how are you?")

label loop:
    "A"
    "B"
    "C"
    "D"
    jump loop

    menu:
        e "I made it back to what I can only assume is my dorm room. What should I be doing for the rest of the night?"

        "Cleaning my desk.":
            pass

        "Reading the Lemma Soft Forums.":
            pass

        "Figuring out why I'm trapped in a fantasy anime.":
            pass

    show expression Transform("dialogue.png", size=(1280, 720))

    menu:
        "This is choice 2.1":
            pass

        "This is choice 2.2":
            pass

        "This is choice 2.3":
            pass



    e "Hello, world.\nHello, world."

    e "At that time it was quite clear in my own mind that the Thing had come from the planet Mars, but I judged it improbable that it contained any living creature. I thought the unscrewing might be automatic."

    show expression Transform("dialogue.png", size=(1280, 720))

    e "At that time it was quite clear in my own mind that the Thing had come from the planet Mars, but I judged it improbable that it contained any living creature. I thought the unscrewing might be automatic."

