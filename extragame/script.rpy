init -10:

    $ config.searchpath.append('moonlight')

    # Set up the size of the screen, and the window title.
    $ config.screen_width = 800
    $ config.screen_height = 600
    $ config.window_title = "A Ren'Py Extras Game"

    # These are positions that can be used inside at clauses. We set
    # them up here so that they can be used throughout the program.
    $ left = Position(xpos=0.0, xanchor='left')
    $ right = Position(xpos=1.0, xanchor='right')
    $ center = Position()

    # Likewise, we set up some transitions that we can use in with
    # clauses and statements.
    $ fade = Fade(.5, 0, .5) # Fade to black and back.
    $ dissolve = Dissolve(0.5)
    
    $ wiperight = CropMove(1.0, "wiperight")
    $ wipeleft = CropMove(1.0, "wipeleft")
    $ wipeup = CropMove(1.0, "wipeup")
    $ wipedown = CropMove(1.0, "wipedown")

    $ slideright = CropMove(1.0, "slideright")
    $ slideleft = CropMove(1.0, "slideleft")
    $ slideup = CropMove(1.0, "slideup")
    $ slidedown = CropMove(1.0, "slidedown")

    $ slideawayright = CropMove(1.0, "slideawayright")
    $ slideawayleft = CropMove(1.0, "slideawayleft")
    $ slideawayup = CropMove(1.0, "slideawayup")
    $ slideawaydown = CropMove(1.0, "slideawaydown")

    $ irisout = CropMove(1.0, "irisout")
    $ irisin = CropMove(1.0, "irisin")

    # Now, we declare the images that are used in the program.

    # Images.
    image black = Solid((0, 0, 0, 255))
    image white = Solid((255, 255, 255, 255))
    image yellow = Solid((255, 255, 200, 255))

    # Opening Sequence.
    image bigbeach1 = Image("bigbeach1.jpg")
    image presents = Image("presents.png")

    # Backgrounds.
    image beach1 = Image("beach1b.jpg")
    image beach1 mary = Image("beach1c.jpg")
    image beach1 title = Image("beach1a.jpg")

    image beach2 = Image("beach2.jpg")
    image beach3 = Image("beach3.jpg")

    image dawn1 = Image("dawn1.jpg")
    image dawn2 = Image("dawn2.jpg")

    image library = Image("library.jpg")

    # Ending 1.
    image transfer = Image("transfer.png")
    image moonpic = Image("moonpic.jpg")
    image nogirlpic = Image("nogirlpic.jpg")


    # Ending 3.
    image littlemary = Image("littlemary.jpg")

    # Ending 4.
    image hospital1 = Image("hospital1.jpg")
    image hospital2 = Image("hospital2.jpg")
    image hospital3 = Image("hospital3.jpg")
    image heaven = Image("heaven.jpg")

    # Endings Common
    image good_ending = Image("ending.jpg")
    image bad_ending = Image("badending.jpg")

    # Mary.
    image mary dark confused smiling = Image("mary_dark_confused_smiling.png")
    image mary dark confused wistful = Image("mary_dark_confused_wistful.png")
    image mary dark crying = Image("mary_dark_crying.png")
    image mary dark laughing = Image("mary_dark_laughing.png")
    image mary dark sad = Image("mary_dark_sad.png")
    image mary dark smiling = Image("mary_dark_smiling.png")
    image mary dark vhappy = Image("mary_dark_vhappy.png")
    image mary dark wistful = Image("mary_dark_wistful.png")

    image mary dawn confused smiling = Image("mary_dawn_confused_smiling.png")
    image mary dawn confused wistful = Image("mary_dawn_confused_wistful.png")
    image mary dawn crying = Image("mary_dawn_crying.png")
    image mary dawn laughing = Image("mary_dawn_laughing.png")
    image mary dawn sad = Image("mary_dawn_sad.png")
    image mary dawn smiling = Image("mary_dawn_smiling.png")
    image mary dawn vhappy = Image("mary_dawn_vhappy.png")
    image mary dawn wistful = Image("mary_dawn_wistful.png")


label start:
    jump example
