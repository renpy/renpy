define director.show_tags = { "eileen", "lucy" }

label director:

    e "There are a few tools you can access by pressing the right commands on the keyboard."

    e "Typing Shift+R turns on autoreload mode. When it's enabled, your game will automatically reload when you edit a script file."

    e "Shift+O brings you to the console, which lets you enter Ren'Py and Python commands to try them out."

    e "Shift+D pops up a developer menu with access to these and other functions."

    e "The most powerful tool is the interactive director that lets you add images, music, and voice lines to your game from inside Ren'Py."

    e "The idea is that you can use an editor to write the script and logic of your visual novel, and then interactively add images in the right places."

    if director_readonly:

        show eileen concerned

        e "It looks like Ren'Py is installed read-only on your system, so you won't be able to try out the interactive director now."

        e "You'll need to make your own project, and try it out there. But I can tell you how to use it."

        show eileen happy

    else:

        e "You can try the interactive director out right now, by using it to change this tutorial game."

        e "Be sure to click my dialogue at the bottom of the screen to advance the tutorial."

        e "If something goes wrong, don't worry. Quitting and restarting this tutorial will remove your changes and bring everything back to normal."


    stop music fadeout 1.0
    scene
    with dissolve

    $ director.enable = not director_readonly

    e "To get started, let's go back to a blank slate, with no images on the screen."

    e "You can show the director at any time by pressing the 'D' key on your keyboard. Ren'Py will reload, and you'll come back here. Try it now."

    e "Let's add a background. Click the '+' to pick where to add it, then the 'scene' statement and 'washington' for the image. Finally, click 'Add' to add it."

    e "Next, add a sprite. Click '+', then 'show', 'eileen', 'happy', and 'Add'. Once you've added it, dissolve it in by clicking the second '+', then 'with', 'dissolve', and 'Add'."

    show eileen happy

    e "You can edit or remove statements with the pencil icon. You can move me to the right by editing the show statement, then clicking '(transform)', 'right', and 'Change'."

    e "Finally, you can use the play, queue, stop, and voice statements to manage audio. Try adding 'play', 'music', 'sunflower-slow-drag.ogg'."

    $ director.state.show_director = False
    $ director.enable = False

    if renpy.showing("lucy"):

        l "Finally, I get some more screen time!"

    queue music "sunflower-slow-drag.ogg"

    scene bg washington
    show eileen happy
    with dissolve

    e "The changes you make with the director are permanent. They're saved to the script, and you can rollback or repeat this section to see them."

    e "However, we reset this tutorial when the game restarts, so you can try again from a clean slate. That won't happen with your own visual novel."

    e "I hope these tools make developing your visual novel that much easier."

    return


