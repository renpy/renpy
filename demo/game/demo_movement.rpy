init:
    # Defines a big image we can pan over.
    image bg onememorial = "1memorial.jpg"

    # Defines a SnowBlossom object, which uses particle motion to show falling
    # cherry blossom petals.
    image snowblossom = SnowBlossom(anim.Filmstrip("sakura.png", (20, 20), (2, 1), .15), fast=True)

    # Defines the magic circle image.
    image magic_circle = "magic.png"

    # Defines an image that zooms between various sizes.
    image logo sizezoom = Animation(
        At("logo.png", SizeZoom((100, 300), (300, 100), 1, opaque=False)), 1,
        At("logo.png", SizeZoom((300, 100), (100, 300), 1, opaque=False)), 1,
        )

# Defines a spline motion.
init python:
    spline = SplineMotion([
        ((-0.042, 0.523,),),
        ((0.768, 0.296,), (0.082, 0.507,), (0.772, 0.573,),),
        ((0.292, 0.304,), (0.766, 0.112,), (0.296, 0.123,),),
        ((1.152, 0.509,), (0.288, 0.555,), (1.076, 0.499,),),
        ], 3.0, anchors=(0.5, 0.5))
 
label demo_movement:

    
    e "I'm not stuck standing in the middle of the screen, even though I like being the center of attention."

    e "Positions, given with an at clause, specify where I'm standing, while the 'move' transition moves around images that have changed position."

    e "For example..."

    show eileen happy at left
    with move

    e "The left position has my left side border the left side of the screen."

    show eileen happy at center
    with move

    e "I can also move to the center..."

    show eileen happy at right
    with move

    e "and the right."

    e "We don't limit you to these positions either. You can always create your own Position objects."

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

    # spline is defined near the top of this file.
    show logo base at spline

    e "SplineMotion allows for more complex movements to be defined."

    hide logo base
    
    scene bg whitehouse at Zoom((800, 600), (0, 0, 800, 600), (225, 150, 400, 300), 1.0)

    e "We can zoom into images..."

    scene bg whitehouse at Zoom((800, 600), (225, 150, 400, 300), (0, 0, 800, 600), 1.0)

    e "... and zoom back out of them again."

    scene bg whitehouse
    show eileen happy at FactorZoom(1.0, 0.5, 1.0, opaque=False), center

    e "We can also zoom images by a factor..."

    show eileen happy at FactorZoom(0.5, 1.0, 1.0, opaque=False), center

    e "... and zoom {i}them{/i} out again."

    show eileen happy at left
    # logo sizezoom is defined at the top of this file.
    show logo sizezoom at Position(xalign=.75, yalign=.4) 
    with moveinright

    e "We can scale images to arbitrary sizes."

    show eileen happy at center
    hide logo sizezoom
    with moveoutright

    with Pause(.5)
    
    $ renpy.layer_at_list([ Zoom((800, 600), (0, 0, 800, 600), (200, 0, 400, 300), 1)])
    with Pause(1)
    $ renpy.layer_at_list([ Zoom((800, 600), (200, 0, 400, 300), (0, 0, 800, 600), 1)])
    with Pause(1)
    $ renpy.layer_at_list([ ])

    e "We can apply motions to a layer as a whole."
    
    show eileen happy
    show magic_circle at RotoZoom(0, 360, 5, 0, 1, 1, rot_repeat=True, rot_anim_timebase=True, opaque=False, xalign=0.5, yalign=0.5)

    with Pause(1)
    
    e "We can rotate and zoom images in a single operation."

    e "And when we're no longer feeling so occult, we can zoom them back out again."

    show magic_circle at RotoZoom(0, 360, 5, 1, 0, 1, rot_repeat=True, rot_anim_timebase=True, opaque=False, xalign=0.5, yalign=0.5)

    with Pause(1)

    hide magic_circle
    
    show eileen happy    
    show logo base at Position(xpos=250, ypos=300, xanchor=0.5, yanchor=0.5), Revolve(0, 360, 4, repeat=True) behind eileen
    with dissolve
    
    "We can also revolve an image around in a circle."

    show bg washington
    hide logo base
    show snowblossom
    with dissolve

    e "Finally, Ren'Py has a particle motion system, that can be used for things like falling cherry blossoms, falling snow, and rising bubbles."
    
    e "The particle motion system uses a factory to create particles over the course of an interaction."
    
    e "While the SnowBlossom function wraps a factory that provides convenient support for things rising and falling in straight lines, it's also possible to define your own."

    e "The sky's the limit."

    e "Or the ground, in the case of these cherry blossoms."

    hide snowblossom
    with dissolve

    return
