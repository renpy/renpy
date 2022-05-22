# This file demonstrates the built-in transitions which are defined in
# common/definitions.rpy, and also the new transitions given above.

example slow_dissolve:
    define slow_dissolve = Dissolve(1.0)

example flashbulb:
    define flashbulb = Fade(0.2, 0.0, 0.8, color='#fff')

# Imagedissolve Transitions.

example circleirisout:
    define circleirisout = ImageDissolve("imagedissolve circleiris.png", 1.0, 8)

example circleirisin:
    define circleirisin = ImageDissolve("imagedissolve circleiris.png", 1.0, 8 , reverse=True)

example circlewipe:
    define circlewipe = ImageDissolve("imagedissolve circlewipe.png", 1.0, 8)

example dream:
    define dream = ImageDissolve("imagedissolve dream.png", 2.0, 64)

example teleport:
    define teleport = ImageDissolve("imagedissolve teleport.png", 1.0, 0)

image bg circleiris = "imagedissolve circleiris"
image bg teleport = "imagedissolve teleport"

example alphadissolve:

    image alpha_control:
        "spotlight.png"

        anchor (.5, .5)

        parallel:
            zoom 0
            linear .5 zoom .75
            pause 2
            linear 1.0 zoom 4.0

        parallel:
            xpos 0.0 ypos .6
            linear 1.5 xpos 1.0
            linear 1.0 xpos .5 ypos .2

        pause .5
        repeat

    define alpha_example = AlphaDissolve("alpha_control", delay=3.5)


label demo_transitions:

    e "Ren'Py ships with a large number of built-in transitions, and also includes classes that let you define your own."

    menu demo_transitions_menu:

        e "What kind of transitions would you like demonstrated?"

        "Simple Transitions":

            call demo_simple_transitions from _call_demo_simple_transitions_1

        "ImageDissolve Transitions":

            call demo_imagedissolve_transitions from _call_demo_imagedissolve_transitions_1

        "MoveTransition Transitions":

            call demo_movetransition from _call_demo_movetransition_1

        "CropMove Transitions":

            call demo_cropmove_transitions from _call_demo_cropmove_transitions_1

        "PushMove Transitions":

            call demo_pushmove_transitions from _call_demo_pushmove_transitions_1

        "AlphaDissolve Transitions":

            call demo_alphadissolve from _call_demo_alphadissolve

        "How about something else?":

            return

    jump demo_transitions_menu


label demo_simple_transitions:

    e "Okay, I can tell you about simple transitions. We call them simple because they don't take much in the way of configuration."

    e "But don't let that get you down, since they're the transitions you'll probably use the most in a game."

    example:
        show bg whitehouse
        with dissolve

    e "The 'dissolve' transition is probably the most useful, blending one scene into another."

    example slow_dissolve small:
        show bg washington
        with slow_dissolve

    e "The 'Dissolve' function lets you create your own dissolves, taking a different amount of time."


    example:
        show bg whitehouse
        with fade

    e "The 'fade' transition fades to black, and then fades back in to the new scene."

    e "If you're going to stay at a black screen, you'll probably want to use 'dissolve' rather than 'fade'."

    example flashbulb small:
        with flashbulb

    e "You can use 'Fade' to define your own fades. By changing the timing and the color faded to, you can use this for special effects, like flashbulbs."

    example:
        show bg washington
        with pixellate

    e "The 'pixellate' transition pixellates out the old scene, switches to the new scene, and then unpixellates that."

    e "It's probably not appropriate for most games, but we
       think it's kind of neat."

    e "You can use 'Pixellate' to change the details of the pixellation."

    e "Motions can also be used as transitions."

    "..."

    "......"

    example:
        play audio "punch.opus"
        with vpunch

    e "Hey! Pay attention."

    e "I was about to demonstrate 'vpunch'... well, I guess I just did."

    example:
        play audio "punch.opus"
        with hpunch

    e "We can also shake the screen horizontally, with 'hpunch'. These were defined using the 'Move' function."

    e "There's also the 'move' transition, which is confusingly enough defined using the 'MoveTransition' function."

    example:
        show eileen happy at right
        with move
        show eileen happy at center
        with move

    e "The 'move' transition finds images that have changed placement, and slides them to their new place. It's an easy way to get motion in your game."

    hide example

    e "That's it for the simple transitions."

    return


label demo_imagedissolve_transitions:

    e "Perhaps the most flexible kind of transition is the ImageDissolve, which lets you use an image to control a dissolve."

    e "This lets us specify very complex transitions, fairly simply. Let's try some, and then I'll show you how they work."

    e "There are two ImageDissolve transitions built into Ren'Py."


    example:
        scene black
        with blinds

        scene bg washington
        show eileen happy
        with blinds


    e "The 'blinds' transition opens and closes what looks like vertical blinds."

    example:
        scene black
        with squares

        scene bg washington
        show eileen happy
        with squares

    e "The 'squares' transition uses these squares to show things."

    e "I'm not sure why anyone would want to use it, but it was used in some translated games, so we added it."

    hide example

    e "The most interesting transitions aren't in the standard library."

    e "These ones require an image the size of the screen, and so we couldn't include them as the size of the screen can change from game to game."

    example circleirisin small:
        scene black
        with circleirisin

    e "We can hide things with a 'circleirisin'..."

    example circleirisout small:
        scene bg washington
        with circleirisout

    e "... and show them again with a 'circleirisout'."

    example circlewipe small:
        show bg whitehouse
        with circlewipe

    e "The 'circlewipe' transitions changes screens using a circular wipe effect."

    example dream small:
        scene bg washington
        with dream

    e "The 'dream' transition does this weird wavy dissolve, and does it relatively slowly."

    example teleport small:
        show eileen happy
        with teleport

    e "The 'teleport' transition reveals the new scene one line at a time."

    show example circleirisout small

    scene bg circleiris
    with dissolve

    e "This is the background picture used with the circleirisout transition."

    e "When we use an ImageDissolve, the white will dissolve in first, followed by progressively darker colors. Let's try it."

    show bg washington
    with circleirisout

    show example circleirisout small

    e "If we give ImageDissolve the 'reverse' parameter, black areas will dissolve in first."

    show bg circleiris
    with circleirisin

    e "This lets circleirisin and circleirisout use the same image."

    show example teleport small

    show bg teleport
    with dissolve

    e "The teleport transition uses a different image, one that dissolves things in one line at a time."

    show bg washington
    with teleport

    e "A dissolve only seems to affect parts of the scene that have changed..."

    show eileen happy
    with teleport

    e "... which is how we apply the teleport effect to a single character."

    hide example

    return

label demo_cropmove_transitions:

    e "The CropMove transition class provides a wide range of transition effects. It's not used very much in practice, though."

    show eileen happy at offscreenleft
    with move

    e "I'll stand offscreen, so you can see some of its modes. I'll read out the mode name after each transition."

    example:
        scene bg whitehouse
        with wiperight

    e "We first have wiperight..."

    example:
        scene bg washington
        with wipeleft

    e "...followed by wipeleft... "

    example:
        scene bg whitehouse
        with wipeup

    e "...wipeup..."

    example:
        scene bg washington
        with wipedown

    e "...and wipedown."

    e "Next, the slides."

    example:
        scene bg whitehouse
        with slideright

    e "Slideright..."

    example:
        scene bg washington
        with slideleft

    e "...slideleft..."

    example:
        scene bg whitehouse
        with slideup

    e "...slideup..."

    example:
        scene bg washington
        with slidedown

    e "and slidedown."

    e "While the slide transitions slide in the new scene, the
       slideaways slide out the old scene."

    example:
        scene bg whitehouse
        with slideawayright

    e "Slideawayright..."

    example:
        scene bg washington
        with slideawayleft

    e "...slideawayleft..."

    example:
        scene bg whitehouse
        with slideawayup

    e "...slideawayup..."

    example:
        scene bg washington
        with slideawaydown

    e "and slideawaydown."

    e "We also have a couple of transitions that use a
       rectangular iris."

    example:
        scene bg whitehouse
        with irisout

    e "There's irisout..."

    example:
        scene bg washington
        show eileen happy
        with irisin

    e "... and irisin."

    hide example

    e "It's enough to make you feel a bit dizzy."

    return

label demo_pushmove_transitions:

    e "The PushMove transitions use the new scene to push the old one out. Let's take a look."

    example:

        show bg whitehouse
        hide eileen
        with pushright

    "There's pushright..."

    example:

        show bg washington
        with pushleft

    "...pushleft..."


    example:

        show bg whitehouse
        with pushdown

    "...pushdown..."

    example:

        show bg washington
        show eileen happy
        with pushup

    "... and pushup. And that's it the for the PushMove-based transitions."

    hide example
    pause .5

    return

label demo_movetransition:


    e "The most common MoveTransition is move, which slides around images that have changed position on the screen."

    example move:

        show eileen happy at left
        with move


    e "Just like that."

    show example moveinout

    e "There are also the moveout and movein transitions."

    e "The moveout transitions (moveoutleft, moveoutright, moveouttop, and moveoutbottom) slide hidden images off the appropriate side of the screen."

    e "The movein transitions (moveinleft, moveinright, moveintop, and moveinbottom) slide in new images."

    e "Let's see them all in action."

    hide example
    pause .5

    example moveinout hide:
        hide eileen happy
        with moveoutleft

        show eileen happy
        with moveinbottom

        hide eileen happy
        with moveoutbottom

        show eileen happy
        with moveinright

        hide eileen happy
        with moveoutright

        show eileen happy:
            yzoom -1
            xalign 0.5
            yalign 0.0


        with moveintop

        hide eileen happy
        with moveouttop

        show eileen happy
        with moveinleft

    e "That's it for the moveins and moveouts."

    e "Finally, there are the zoomin and zoomout transitions, which show and hide things using a zoom."

    example:

        hide eileen happy
        with zoomout

        show eileen happy
        with zoomin

    e "And that's all there is."

    hide example
    pause .5

    return

label demo_alphadissolve:

    e "The AlphaDissolve transition lets you use one displayable to combine two others. Click, and I'll show you an example."

    scene black
    with dissolve

    example alphadissolve large:
        scene bg washington
        show eileen happy at center
        with alpha_example

    e "The AlphaDissolve displayable takes a control displayable, usually an ATL transform."

    scene
    show alpha_control

    e "To be useful, the control displayable should be partially transparent."

    e "During an AlphaDissolve, the old screen is used to fill the transparent areas of the image, while the new screen fills the opaque areas."

    scene black

    e "For our spotlight example, the old screen is this all-black image."

    scene bg washington
    show eileen happy at center

    e "The new screen is me just standing here."

    scene black
    with dissolve
    scene bg washington
    show eileen happy at center
    with alpha_example

    e "By combining them using AlphaDissolve, we can build a complicated effect out of simpler parts."

    hide example
    pause .5

    return
