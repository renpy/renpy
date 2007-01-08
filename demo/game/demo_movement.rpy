init:
    # Defines a big image we can pan over.
    image bg onememorial = "1memorial.jpg"

    # Defines a SnowBlossom object, which uses particle motion to show falling
    # cherry blossom petals.
    image snowblossom = SnowBlossom(anim.Filmstrip("sakura.png", (20, 20), (2, 1), .15), fast=True)

    
label demo_movement:

    
    e "I'm not stuck standing in the middle of the screen, even though I like being the center of attention."

    e "Positions, given with an at clause, specify where I'm standing, while the 'move' transition moves around images that have changed position."

    e "For example..."

    show eileen happy at offscreenleft
    with move

    e "I can move over to the offscreenleft position, just off the left side of the screen."

    show eileen happy at left
    with move

    e "The left position has my left side border the left side of the screen."

    show eileen happy at center
    with move

    e "I can also move to the center..."

    show eileen happy at right
    with move

    e "... the right ..."

    show eileen happy at offscreenright
    with move

    e "... or even to offscreenright, off the right-hand side of the screen."

    show eileen happy at right
    with move

    e "We don't limit you to these five positions either. You can always create your own Position objects."

    # This is necessary to restart the time at which we are
    # shown. 
    hide eileen happy

    show eileen happy at Move((1.0, 1.0, 1.0, 1.0),
                              (0.0, 1.0, 0.0, 1.0),
                              4.0, repeat=True, bounce=True)

    e "It's also possible to have a movement happen while showing dialogue on the screen, using the Move function."

    e "Move can repeat a movement, and even have it bounce back and forth, like I'm doing now."

    scene bg onememorial at Pan((0, 800), (0, 0), 10.0)
    with dissolve

    e "We can pan around an image larger than the screen, using the Pan function in an at clause. That's what we're doing now."

    scene bg whitehouse
    with dissolve
    scene bg whitehouse at Zoom((800, 600), (0, 0, 800, 600), (225, 150, 400, 300), 1.0)

    e "We can zoom into images..."

    scene bg whitehouse at Zoom((800, 600), (225, 150, 400, 300), (0, 0, 800, 600), 1.0)

    e "... and zoom back out of them again."

    scene bg whitehouse
    show eileen happy at FactorZoom(1.0, 0.5, 1.0, opaque=False), center

    e "We can also zoom images by a factor..."

    show eileen happy at FactorZoom(0.5, 1.0, 1.0, opaque=False), center

    e "... and zoom {i}them{/i} out again."


    scene bg washington
    show eileen happy
    show snowblossom
    with dissolve

    e "Finally, Ren'Py has a particle motion system, that can be used for things like falling cherry blossoms, falling snow, and rising bubbles."

    e "The particle motion system uses a factory to create particles over the course of an interaction."
    
    e "While the  SnowBlossom function wraps a factory that provides convenient support for things rising and falling in straight lines, it's also possible to define your own."

    e "The sky's the limit."

    e "Or the ground, in the case of these cherry blossoms."

    hide snowblossom
    with dissolve

    return
