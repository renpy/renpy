image bg band = Transform("concert1", zoom=.75)
image logo small = Transform("logo base", zoom=.66)

image concert:
    subpixel True
    size (1280, 720)
    xalign .5
    yalign .5

    parallel:
        "concert2"
        pause 1.0

        block:
            "concert1" with Dissolve(.1)
            pause .4
            "concert2" with Dissolve(.1)
            pause .4
            "concert3" with Dissolve(.1)
            pause .4
            "concert2" with Dissolve(.1)
            pause .4
            repeat

        time 43.0

    parallel:


        # Lucy Strums.
        crop (213, 778, 590, 332)
        pause 1.0
        easeout .6 crop (286, 818, 469, 264)

        crop (87, 370, 590, 332)
        easein .8 crop (14, 306, 791, 445)

        # Mary cymbals.
        time 2.9
        crop (1035, 656, 417, 235)
        time 3.4
        crop (564, 545, 552, 311)
        time 3.9
        crop (1035, 656, 417, 235)
        time 4.4
        crop (564, 545, 552, 311)

        # Zoom out.
        time 5.0
        linear 4.0 crop (0, 482, 1738, 978)
        easein 4.0 crop (267, 91, 2133, 1200)
        easeout 4.0 crop (0, 91, 2133, 1200)


        # Pan up Eileen
        time 17.0
        crop (1047, 849, 1132, 637)

        linear 4.0 crop (868, 58, 1532, 862)

        time 22.25

        # Mary's random crops.
        block:
            choice:
                crop (741, 517, 725, 408)
            choice:
                crop (409, 594, 1157, 651)
            choice:
                crop (719, 526, 753, 424)
            choice:
                crop (692, 521, 449, 253)
            choice:
                crop (468, 903, 1038, 584)

            pass

            choice:
                zoom 1.0
            choice:
                zoom 1.3
            choice:
                zoom 1.5

            pause .43

            repeat

        # Lucy and Mary
        time 26.97
        zoom 1
        crop (0, 482, 1738, 978)
        pause 1.0

        # Mary
        crop (0, 775, 984, 554)
        easein 5.5 crop (0, 279, 984, 554)

        # Final shot.
        easeout 4.0 crop (0, 91, 2133, 1200)
        easein 4.0 crop (267, 91, 2133, 1200)




image pos:
    "target1.png"
    block:
        rotate 0
        linear 2.0 rotate 360.0
        repeat

image anchor:
    "target2.png"
    block:
        rotate 360.0
        linear 2.0 rotate 0.0
        repeat

example atl_right:
    transform right:
        xalign 1.0
        yalign 1.0

example atl_image:
    image eileen animated:
        "eileen vhappy"
        pause .5
        "eileen happy"
        pause .5
        repeat

example atl_image1:
    image eileen animated twice:
        "eileen vhappy"
        pause .5
        "eileen happy"
        pause .5
        repeat 2

example atl_image2:
    image eileen animated once:
        "eileen vhappy"
        pause .5
        "eileen happy"

example atl_with:
    image bg atl transitions:
        "bg washington"
        "bg whitehouse" with dissolve
        pause 1.0
        "bg washington" with dissolve
        pause 1.0
        repeat


example atl_transform:
    transform topright:
        xalign 1.0 yalign 0.0


example atl_transform1:
    transform move_jump:
        xalign 1.0 yalign 0.0
        pause 1.0
        xalign 0.0
        pause 1.0
        repeat

example atl_transform2:
    transform move_slide:
        xalign 1.0 yalign 0.0
        linear 3.0 xalign 0.0
        pause 1.0
        repeat

transform reset:
    xpos 0.5
    xanchor 0.5
    ypos 0.3
    yanchor 0.5

    zoom 1.0
    xzoom 1.0
    yzoom 1.0

    crop None

    xsize None
    ysize None
    fit None

    alpha 1.0

    rotate None
    rotate_pad True
    nearest False
    additive 0.0

    xtile 1
    ytile 1

    xpan None
    ypan None

label tutorial_positions:

    e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."

    e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."

    e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."

    e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."

    e "When we're positioning something, the area is usually the entire screen."

    e "Let me get out of the way, and I'll show you where some positions are."

    hide eileen
    with moveoutright

    show pos:
       xanchor 0.5 yanchor 0.5 xpos 0.5 ypos 0.5
       subpixel True

    with dissolve

    show pos:
        linear .5 xpos 0.0 ypos 0.0

    e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."

    show pos:
        ypos 0.0
        linear .5 xpos 0.5

    e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."

    show pos:
        linear .5 xpos 1.0

    e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."

    show pos:
        xpos 1280
        linear .5 xpos 640

    e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."

    e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."

    show pos:
        xpos 640
        linear .5 ypos .5

    e "Here's a ypos of 0.5."

    show pos:
        linear .5 ypos 1.0

    e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."

    e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."

    show pos:
        linear .5 xpos .75 ypos .25


    menu:

        e "Can you guess where this position is, relative to the screen?"

        "xpos 1.0 ypos .5":

            e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."

            e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."

        "xpos .75 ypos .25":

            e "Good job! You got that position right."

        "xpos .25 ypos .33":

            e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."

            e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."

    hide pos

    show logo solid:
        xpos 523 ypos 100

    show anchor:
        xanchor 0.5 yanchor 0.5
        xpos 523 ypos 100

    with dissolve


    e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."

    e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."

    show anchor:
        linear .5 xpos 757

    e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."

    show anchor:
        linear .5 ypos 460

    e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."

    show pos:
        xanchor .5 yanchor .5
        xpos 957 ypos 460


    e "To place an image on the screen, we need both the position and the anchor."

    show logo solid:
        linear .5 xpos 723 ypos 100

    show anchor:
        linear .5 xpos 957 ypos 460

    e "We then line them up, so that both the position and anchor are at the same point on the screen."


    show anchor:
        linear .5 xpos 0 ypos 0
    show pos:
        linear .5 xpos 0 ypos 0
    show logo solid:
        linear .5 xpos 0 ypos 0

    e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."

    show anchor:
        linear .5 xpos 0.5 ypos 0.5
    show pos:
        linear .5 xpos 0.5 ypos 0.5
    show logo solid:
        linear .5 xalign 0.5 yalign 0.5

    e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."

    show logo solid:
        linear .5 yalign .3

    with None

    hide anchor
    hide pos

    with dissolve

    e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."

    show logo solid:
        linear .5 xalign 0.0

    e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."

    show logo solid:
        linear .5 xalign 1.0

    e "When we set it to 1.0, then we're aligned to the right side of the screen."

    show logo solid:
        linear .5 xalign .5

    e "And when we set it to 0.5, we're back to the center of the screen."

    e "Setting yalign is similar, except along the y-axis."

    e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."

    show logo solid:
        linear .5 xcenter .75

    e "The xcenter and ycenter properties position the center of the image.  Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."

    show logo solid:
        linear 1.0 xcenter 1.0

    e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."

    show logo solid:
        linear .5 xalign 0.5 yalign 0.5
        linear .5 xoffset 50 yoffset 20

    pause .5

    e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."

    show logo solid:
        linear .5 xoffset -50 yoffset -20

    e "Of course, you can use negative numbers to offset things to the left and top."

    show logo solid:
        linear .5 align (0.5, 0.5) offset (0, 0)

    e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."

    hide logo
    with dissolve
    show eileen happy
    with moveinright

    e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."

    return


label tutorial_atl:

    e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"

    example simple_transform:
        show eileen happy at right

    with move

    e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."

    hide example

    e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"

    stop music fadeout 1.0
    scene concert
    with fade

    play music "renpyallstars.ogg" noloop

    e "But first, let's have... a Gratuitous Rock Concert!"

    play music "sunflower-slow-drag.ogg" fadeout 1.0

    scene bg washington
    show eileen happy
    with dissolve

    e "That was a lot of work, but it was built out of small parts."

    e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."

    e "There are currently three places where ATL can be used in Ren'Py."

    show example atl_image
    show eileen animated

    e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."

    e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."

    show example atl_transform
    show eileen happy at right

    e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."

    example:

        show logo base:
            xalign .3 yalign .7
            linear 1.0 xalign .7 yalign .3
            linear 1.0 xalign .3 yalign .7
            repeat

    with dissolve

    e "Finally, an ATL block can be used as part of a show statement, instead of the at clause." id tutorial_atl_da7a7759


    example:
        show logo base:
            yoffset 10

    e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though your click stopped the motion, the image remains in the same place." id tutorial_atl_1dd345c6

    hide logo
    show eileen happy at center
    with moveoutleft

    hide screen example

    e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."

    e "Before I explain how ATL works, let me explain what animation and transformation are."

    show eileen animated:
        center

    e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."

    show eileen happy

    show magic:
        yalign .5 subpixel True

        parallel:
            xalign .5
            linear 3.0 xalign .75
            linear 6.0 xalign .25
            linear 3.0 xalign .5
            repeat

        parallel:
            alpha 1.0 zoom 1.0
            linear .75 alpha .5 zoom .9
            linear .75 alpha 1.0 zoom 1.0
            repeat

        parallel:
            rotate 0
            linear 5 rotate 360
            repeat

    with dissolve

    e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."

    hide magic
    with dissolve

    show example atl_image
    show eileen animated

    e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."

    e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."

    e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."

    e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."

    e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."

    show example atl_image1
    show eileen animated twice

    e "If we were to write repeat 2 instead, the animation would loop twice, then stop."

    show example atl_image1
    show eileen animated once

    e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."


    show example atl_with
    show bg atl transitions

    e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."

    show bg washington
    with dissolve

    hide screen example

    e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."

    show logo base behind eileen

    show logo base at topright
    with dissolve

    show example atl_transform

    e "The simplest thing we can do is to statically position an image. This is done by giving the names of the position properties, followed by the property values." id tutorial_atl_ddc55039

    show example atl_transform1
    show logo base at move_jump

    e "With a few more statements, we can move things around on the screen."

    e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."

    e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."

    show example atl_transform2
    show logo base at move_slide

    e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."

    e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."

    e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."

    e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."

    e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."

    hide example

    show eileen happy at right
    with move

    show logo base:
        alignaround (.5, .3)
        linear 2.0 xalign .5 yalign .3 clockwise circles 3

    e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."

    hide logo with dissolve

    e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."

    example large:
        show eileen happy:
            right
            pause 1.25
            left
            pause 1.25
            repeat

    with dissolve

    e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."

    show eileen happy at center
    show logo base behind eileen
    with dissolve

    example:
        show logo base:
            xalign 0.0 yalign 0.0
            block:
                linear 1.0 xalign 1.0
                linear 1.0 xalign 0.0
                repeat
            time 11.5
            linear .5 xalign 1.0

    e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."

    e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."

    e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."


    example:
        show logo base:
            parallel:
                linear 1.0 xalign 0.0
                linear 1.0 xalign 1.0
                repeat
            parallel:
                linear 1.3 yalign 1.0
                linear 1.3 yalign 0.0
                repeat

    e "The parallel statement lets us run two blocks of ATL code at the same time."

    e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."

    show logo base:
        yalign 0.0
        xalign 0.0

    example:
        show logo base:
            choice:
                linear 1.0 xalign 0.0
            choice:
                linear 1.0 xalign 1.0
            repeat

    e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."

    hide logo base
    with dissolve
    hide example

    e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."


    return



label transform_properties:

    e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "Here, we'll show them off so you can see them in action and get used to what each does."


    show eileen happy at right
    with move


    example:
        show logo base:
            xpos 0.5
            xanchor 0.5
            ypos 0.3
            yanchor 0.5

    with dissolve

    e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."


    hide eileen
    hide logo base

    show bg band:
        xanchor 0 yanchor 0
        xpos 0 ypos -428

    with dissolve

    example:
        show bg band:
            xanchor 0 yanchor 0
            xpos 0 ypos -428
            linear 3.0 xpos -220 ypos -60

    e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."

    # Let's not demo this until it's not terrible.
    if False:

        example:
            show bg band:
                subpixel False
                linear 60.0 xpos 0

        "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."

        example:
            show bg band:
                subpixel True
                linear 60.0 xpos 0

        "When it's set to True, movement is smoother at the cost of blurring images a little."


    hide bg
    show bg washington

    show eileen happy at right

    hide logo

    example:
        show logo small:
            anchor (0.5, 0.5)
            around (640, 216)
            angle 270
            radius 200

    with dissolve

    e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."

    example:
        show logo small:
            linear 1.0 angle 315
            linear 1.0 angle 270
            repeat

    e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."


    example:
        show logo small:
            linear 1.0 radius 100
            linear 1.0 radius 200
            repeat

    e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."


    hide logo small
    show logo base at reset
    with dissolve

    example:
        show logo base:
            zoom 1.0
            linear 1.0 zoom 1.5
            linear 1.0 zoom 1.0
            repeat

    e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."

    show logo base at reset

    example:
        show logo base:
            xzoom .75 yzoom 1.25
            linear 1.0 xzoom 1.25 yzoom .75
            linear 1.0 xzoom .75 yzoom 1.25
            repeat

    with dissolve

    e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."

    show logo base at reset

    example:
        show logo base:
            linear 1.0 xzoom -1.0 yzoom 1.0

    with dissolve

    e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."

    show logo base at reset

    example:
        show logo base:
            size (350, 540)

    with dissolve

    e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."

    show logo base at reset

    example:
        show logo base:
            alpha 1.0
            linear 1.0 alpha 0.0
            pause .5
            linear 1.0 alpha 1.0
            pause .5
            repeat

    with dissolve

    e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."

    show logo base at reset

    example:
        show logo base:
            xanchor 0.5 yanchor 0.5
            rotate 0
            linear 4.0 rotate 360
            repeat

    with dissolve

    e "The rotate property rotates a displayable."

    example:
        show logo base:
            xalign 0.0 yalign 0.0
            rotate 0
            linear 4.0 rotate 360
            repeat

    with dissolve

    e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."

    example:
        show logo base:
            rotate_pad False
            xalign 0.0 yalign 0.0
            rotate 0
            linear 4.0 rotate 360
            repeat

    with dissolve

    e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."

    show logo base at reset

    example:
        show logo base:
            xtile 3
            ytile 2

    with dissolve

    e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."

    show logo base at reset

    example:
        show logo base:
            crop (0, 0, 117, 360)

    with dissolve

    e "The crop property crops a rectangle out of a displayable, showing only part of it."

    hide logo base
    with dissolve

    example:
        show bg washington:
            crop (0, 0, 800, 600)
            size (1280, 720)

            linear 4.0 crop (451, 437, 409, 230)

    with dissolve

    e "When used together, crop and size can be used to focus in on specific parts of an image."

    hide bg

    example:
        show bg panorama:
            xpan 0
            linear 10.0 xpan 360
            repeat

    with dissolve

    e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."

    hide example
    scene bg washington
    show eileen happy
    with dissolve

    e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."

    show eileen happy

    return
