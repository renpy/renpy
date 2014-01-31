# Code that demonstrates layers and advanced show.

init:

    # Declare a layer, 'demo', that lives just above the default 'master'
    # layer.
    $ config.layers.insert(1, 'demo')

    # Make it so that it only takes up part of the screen.
    $ config.layer_clipping['demo'] = (50, 50, 700, 500)


label demo_layers:

    e "Ren'Py lets you define layers, and show images on specific layers."

    hide eileen
    with dissolve

    show bg whitehouse onlayer demo
    with dissolve

    show eileen happy onlayer demo
    with dissolve

    e "The \"onlayer\" clause of the scene, show, and hide statements lets us pick which layers the commands affect."

    e "As you can see, layers do not have to take up the entire screen. When a layer doesn't, images are clipped to the layer."

    scene onlayer demo
    show eileen happy
    with dissolve

    e "The \"as\" clause lets you change the tag of an image."

    show eileen happy as eileen2
    with None

    show eileen happy at left
    show eileen happy at right as eileen2
    with move

    e "This is useful when you want to show two copies of the same image."

    e "Or if a character has a twin."

    show eileen happy at center
    show eileen happy at offscreenright as eileen2
    with move

    hide eileen2

    show expression Text(_("This is text."), size=50, yalign=0.5, xalign=0.5, drop_shadow=(2, 2)) as text
    with dissolve

    e "You can use \"show expression\" to show things that aren't just images, like text."

    hide text
    with dissolve

    show logo base at Position(xalign=0.6, yalign=0.0) behind eileen
    with dissolve

    e "The \"behind\" clause lets you place an image behind another."

    hide logo base
    show eileen happy
    with dissolve

    show layer master:
        xalign 0.5
        yalign 0.5
        linear 0.75 rotate 180.0

    pause 0.75

    e "Finally, the \"show layer\" statement allows you to apply a transform to an entire layer."

    show layer master:
        xalign 0.5
        yalign 0.5
        rotate 180.0
        linear 0.75 rotate 360.0

    pause 0.75

    # Cancels the layer transform.
    show layer master

    e "And that's it for layers and advanced show."

    return
