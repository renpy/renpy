# This file demonstrates the Ren'Py User Experience... the features you get
# for free by choosing to use Ren'Py as a visual novel engine.


transform popup_place:
    xpos 0.1 xanchor 0.0 ypos 0.1 yanchor 0.0


label tutorial_playing:

    e "As someone who has played more than a few visual novels, there are many features that I expect all games to have."

    e "Features like saving, loading, changing preferences, and so on."

    e "One of the nice things about Ren'Py is that the engine provides many of these features for you. You can spend your time creating your game, and let us provide these things."

    e "While you're in the game, you can access the game menu by right clicking or hitting the escape key."

    e "You can also access the game menu through some of the quick menu buttons at the bottom of this screen."

    show eileen happy at right
    show popup save at popup_place
    with moveinleft

    e "When you first enter the game menu, you'll see the save screen. Clicking on a numbered slot will save the game."

    e "Unlike other engines, Ren'Py doesn't limit the number of save slots that you can use. You can keep hitting next until you reach the page you want."

    e "Clicking on the title of the page allows you to start typing to change the page name."

    e "The load screen looks quite similar to the save screen, and lets you load a game from a save slot."

    e "It also lets you load one of the auto-saves that Ren'Py makes for you."

    show popup prefs at popup_place
    with dissolve

    e "The game menu also has the preferences screen."

    e "This screen lets you decide how Ren'Py displays, pick what Ren'Py skips, control text speed and auto-click speed, and adjust sound, music, and voice volumes."

    e "The game menu also lets you end the game and return to the main menu, or quit Ren'Py entirely."

    show popup hrpprefs at popup_place
    with dissolve

    e "While the default game menus look a bit generic, with a little work they can be customized or even entirely replaced, allowing you to create menus as unique as your game."

    hide popup
    show eileen happy at center
    with moveoutleft

    e "While inside the game, there are a few more things you can do."

    e "When I'm liking a visual novel, I want to see all the endings. Ren'Py's skip function lets me easily do this, by skipping text that I've already seen."

    e "I can skip a few lines by holding down Control, or I can toggle skip mode by clicking the skip button at the bottom of the screen."

    e "By default, we only skip read text, so this won't do anything the first time through the game."

    e "Clicking the auto button toggles auto-forward mode, which makes the game advance without you clicking."

    e "The Q.Save and Q.Load buttons provide a single-click way to make a save, and a fast way to load that save again."

    e "Pressing the 's' key saves a screenshot to disk, so I can upload pictures of the game to websites like {a=https://www.renpy.org}renpy.org{/a}."

    e "The history button displays a history of read text - but you can also use rollback, which is usually better."

    menu:

        e "Would you like to hear about rollback?"

        "Yes.":

            jump tutorial_rollback

        "No.":

            jump tutorial_rollback_done


label tutorial_rollback:

    e "You can invoke a rollback by clicking the 'Back' button, scrolling the mouse wheel up, or by pushing the page up key. That'll bring you back to the previous screen."

    e "While at a previous screen, you can roll forward by scrolling the mouse wheel down, or pushing the page down key."

    e "Rolling forward through a menu will make the same choice you did last time. But you don't have to do that - Ren'Py's rollback system allows you to make a different choice."

    e "You can try it by rolling back through the last menu, and saying 'No'."

    e "Click back a few times, press page up, or scroll up the mouse wheel."

    show eileen concerned

    e "Well, are you going to try it?"

    e "Your loss."

    e "Moving on."

    show eileen happy

label tutorial_rollback_done:

    e "By allowing Ren'Py to take care of out-of-game issues like loading and saving, you can focus on making your game, while still giving players the experience they've come to expect when playing visual novels."

    return
