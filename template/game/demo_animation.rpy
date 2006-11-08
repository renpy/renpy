# This file contains the code that demonstrates animation.

init:

    # A simple animation. We interleave the displayables we want to
    # show with the times we want to show them for.
    image eileen animated = Animation(
        "eileen_vhappy.png", 1.0,
        "eileen_happy.png", 1.0)

    # The blink animation.
    image blinking text = anim.Blink(Text("Blink", color="#ff0", size=72))
    
    # A state machine-based animation.
    image smanim = anim.SMAnimation(
        
        # The name of the starting state.
        "r",

        # The states we use, and the displayables we show during those
        # states.
        anim.State("r", "#f00"),
        anim.State("g", "#0f0"),
        anim.State("b", "#00f"),

        # The edges, given as a state, a time we remain in that state for,
        # the new state, and the time it takes to transition between the
        # two of them.
        #
        # dissolve only works with solid images. move is also useful here.        
        anim.Edge("r", .5, "g", dissolve),
        anim.Edge("r", .5, "b", dissolve),

        anim.Edge("g", .5, "r", dissolve),
        anim.Edge("g", .5, "b", dissolve),

        anim.Edge("b", .5, "r", dissolve),
        anim.Edge("b", .5, "g", dissolve),         
        )

label demo_animation:



    e "Ren'Py supports a number of ways of creating animations."

    e "These animations let you vary images, independent of the user's clicks."

    show eileen animated

    e "For example, I'm switching my expression back and forth, once a second."

    e "Even though you clicked, I'm still doing it."

    e "This is an example of the Animation function at work."

    show eileen happy

    e "The Animation function is limited to simple lists of images, with fixed delays between them."

    e "The sequence can repeat, or can stop after one go-through."

    e "If you want more control, you can use the anim.SMAnimation function."

    e "It can randomly change images, and even apply transitions to changes."

    scene smanim
    show eileen happy
    with dissolve

    e "Here, we are randomly dissolving the background between red, green, and blue images."

    e "Psychadelic."

    scene bg washington
    show eileen happy
    with dissolve

    e "It's probably best if we stop here, before somebody's brain explodes."

    show blinking text at Position(xalign=.5, yalign=.7)
        
    e "Finally, there's anim.Blink, which can be used to blink things in and out."

    e "I don't know why you'd want to do that to a character, but blinking text seems reasonable for signs and things like that." 

    hide blinking text
    with dissolve
    
    return

    
