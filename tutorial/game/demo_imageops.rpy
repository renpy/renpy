# This file demonstrates the use of image operators.

init:
    image logo base = "logo.png"

    image logo crop = im.Crop("logo.png", 0, 0, 100, 307)

    image logo scale = im.Scale("logo.png", 100, 150)

    image logo factorscale = im.FactorScale("logo.png", 1.5, 1.5)

    image logo composite = im.Composite((200, 407),
                                        (0, 0), "logo.png",
                                        (0, 50), "logo.png",
                                        (0, 100), "logo.png")

    image logo livecomposite = LiveComposite((200, 407),
                                             (0, 0), anim.Blink(Image("logo.png")),
                                             (0, 50), "logo.png",
                                             (0, 100), "logo.png")

    image logo green = im.Map("logo.png", rmap=im.ramp(0, 0))

    image logo green2 = im.Recolor("logo.png", 0, 255, 255, 255)

    image logo alpha = im.Alpha("logo.png", 0.5)

    image logo blackwhite = "logobw.png"

    image logo twocolor = im.Twocolor("logobw.png",
                                      (128, 255, 255, 255),
                                      (255, 0, 0, 255))


    image eileen alpha = im.Alpha("images/eileen happy.png", 0.5)

    image eileen flip = im.Flip("images/eileen happy.png", vertical=True)


    image logo halfsat = im.MatrixColor("logo.png",
                                        im.matrix.saturation(.5))

    # This could be better done with im.matrix.invert(), but I want to show
    # how to use a matrix.
    image logo invert = im.MatrixColor("logo.png",
                                       [ -1,  0,  0, 0, 1,
                                          0, -1,  0, 0, 1,
                                          0,  0, -1, 0, 1,
                                          0,  0,  0, 1, 0, ])

    image logo tintblue = im.MatrixColor("logo.png",
                                         im.matrix.saturation(.5) * im.matrix.tint(.75, .75, 1.0))

    image logo hue = im.MatrixColor("logo.png",
                                    im.matrix.hue(90))

    image logo bright = im.MatrixColor("logo.png",
                                       im.matrix.brightness(.5))

    image logo sepia = im.Sepia("logo.png")

    image logo grayscale = im.Grayscale("logo.png")


    $ logopos = Position(xpos=.5, xanchor=0, ypos=50, yanchor=0)

label demo_imageops:

    e "Image operations allow us to manipulate images as they are loaded in."

    e "They're efficient, as they are only evaluated when an image is first loaded."

    e "This way, there's no extra work that needs to be done when each frame is drawn to the screen."

    show eileen happy at left
    with move
    show logo base at logopos
    with dissolve

    e "Let me show you a test image, the Ren'Py logo."

    e "We'll be applying some image operations to it, to see how they can be used."

    show logo crop at logopos
    with dissolve

    e "The im.Crop operation can take the image, and chop it up into a smaller image."

    show logo composite at logopos
    with dissolve

    e "The im.Composite operation lets us take multiple images, and draw them into a single image."

    e "While you can do this by showing multiple images, this is often more efficient."

    show logo livecomposite at logopos
    with dissolve

    e "There's also LiveComposite, which is less efficent, but allows for animation."

    e "It isn't really an image operation, but we don't know where else to put it."

    show logo scale at logopos
    with dissolve

    e "The im.Scale operation lets us scale an image to a particular size."

    show logo factorscale at logopos
    with dissolve

    e "im.FactorScale lets us do the same thing, except to a factor of the original size."

    show logo green at logopos
    with dissolve

    e "The im.Map operation lets us mess with the red, green, blue, and alpha channels of an image."

    e "In this case, we removed all the red from the image, leaving only the blue and green channels."

    show logo base at logopos
    with dissolve
    show logo green2 at logopos
    with dissolve

    e "The im.Recolor operation can do the same thing, but is more efficient when we're linearly mapping colors."

    show logo blackwhite at logopos
    with dissolve

    e "The im.Twocolor operation lets you take a black and white image, like this one..."

    show logo twocolor at logopos
    with dissolve

    e "... and assign colors to replace black and white."

    show logo halfsat at logopos
    with dissolve

    e "The im.MatrixColor operation lets you use a matrix to alter the colors. With the right matrix, you can desaturate colors..."

    show logo tintblue at logopos
    with dissolve

    e "... tint the image blue..."

    show logo hue at logopos
    with dissolve

    e "... rotate the hue... "

    show logo invert at logopos
    with dissolve

    e "... or invert the colors, for a kinda scary look."

    show logo bright at logopos
    with dissolve

    e "It can even adjust brightness and contrast."

    e "We've made some of the most common matrices into image operators."

    show logo grayscale at logopos
    with dissolve

    e "im.Grayscale can make an image grayscale..."

    show logo sepia at logopos
    with dissolve

    e "... while im.Sepia can sepia-tone an image."

    show logo base at logopos
    with dissolve
    show logo alpha at logopos
    with dissolve

    e "The im.Alpha operation can adjust the alpha channel on an image, making things partially transparent."

    show eileen alpha at left
    with dissolve

    e "It's useful if a character just happens to be ghost."

    hide logo
    show eileen happy at left
    with dissolve

    e "But that isn't the case with me."

    show eileen happy
    with move
    show eileen flip
    with dissolve

    e "Finally, there's im.Flip, which can flip an image horizontally or vertically."

    e "I think the less I say about this, the better."

    show eileen happy
    with dissolve

    return
