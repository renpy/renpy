.. _thequestion:

Script of The Question
======================

The script is divided over two files.

* `script.rpy`_ contains the main body of the game.

* `options.rpy`_ contains options which customize the display of parts
  of the game.

script.rpy
----------

::

    # Declare images used by this game.
    image bg lecturehall = "lecturehall.jpg"
    image bg uni = "uni.jpg"
    image bg meadow = "meadow.jpg"
    image bg club = "club.jpg"

    image sylvie normal = "sylvie_normal.png"
    image sylvie giggle = "sylvie_giggle.png"
    image sylvie smile = "sylvie_smile.png"
    image sylvie surprised = "sylvie_surprised.png"

    image sylvie2 normal = "sylvie2_normal.png"
    image sylvie2 giggle = "sylvie2_giggle.png"
    image sylvie2 smile = "sylvie2_smile.png"
    image sylvie2 surprised = "sylvie2_surprised.png"

    # Define characters used by this game.
    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")


    # The game starts here.
    label start:

        $ bl_game = False

        play music "illurock.ogg"

        scene bg lecturehall
        with fade

        "Well, professor Eileen's lecture was interesting."
        "But to be honest, I couldn't concentrate on it very much."
        "I had a lot of other thoughts on my mind."
        "And they all ended up with a question."
        "A question, I've been meaning to ask someone."

        scene bg uni
        with fade

        "When we came out of the university, I saw her."

        show sylvie normal
        with dissolve

        "She was a wonderful person."
        "I've known her ever since we were children."
        "And she's always been a good friend."
        "But..."
        "Recently..."
        "I think..."
        "... that I wanted more."
        "More just talking... more than just walking home together when our classes ended."
        "And I decided..."

        menu:

            "... to ask her right away.":

                jump rightaway

            "... to ask her later.":

                jump later


    label rightaway:

        show sylvie smile

        s "Oh, hi, do we walk home together?"
        m "Yes..."
        "I said and my voice was already shaking."

        scene bg meadow
        with fade

        "We reached the meadows just outside our hometown."
        "Autumn was so beautiful here."
        "When we were children, we often played here."
        m "Hey... ummm..."

        show sylvie smile
        with dissolve

        "She turned to me and smiled."
        "I'll ask her..."
        m "Ummm... will you..."
        m "Will you be my artist for a visual novel?"

        show sylvie surprised

        "Silence."
        "She is shocked. And then..."

        show sylvie smile

        s "Sure, but what is a \"visual novel?\""

        menu:

            "It's a story with pictures.":
                jump vn

            "It's a hentai game.":
                jump hentai

    label vn:

        m "It's a story with pictures and music."
        m "And you'll be able to make choices that influence the outcome of the story."
        s "So it's like those choose-your-adventure books?"
        m "Exactly! I plan on making a small romantic story."
        m "And I figured you could help me... since I know how you like to draw."

        show sylvie normal

        s "Well, I can try. I hope I don't disappoint you."
        m "You can't disappoint me, you know that."

        jump marry

    label hentai:

        $ bl_game = True

        m "Why it's a game with lots of sex."
        s "You mean, like a boy's love game?"
        s "I've always wanted to make one of those."
        s "I'll get right on it!"

        hide sylvie
        with dissolve

        "..."

        m "That wasn't what I meant!"

        jump marry

    label marry:

        scene black
        with dissolve

        "--- years later ---"

        scene bg club
        with dissolve

        "And so, we became a visual novel creating team."
        "We made games and had a lot of fun making them."

        if bl_game:
            "Well, apart from that Boy's Love game she insisted on making."

        "And one day..."

        show sylvie2 normal
        with dissolve

        s "Hey..."
        m "Yes?"

        show sylvie2 giggle

        s "Marry me!"
        m "What???"

        show sylvie2 surprised

        s "Well, don't you love me?"
        m "I do, actually."

        show sylvie2 smile

        s "See? We've been making romantic visual novels, spending time together, helping each other...."
        s "... and when you give love to others, love will come to you."
        m "Hmmm, that's a nice thought."

        show sylvie2 giggle

        s "I just made that up."
        m "But it's good."

        show sylvie2 normal

        s "I know. So, will you marry me?"
        m "Ummm, of course I will. I've actually been meaning to ask you, but since you brought it up..."
        s "I know, but you are so indecisive, that I thought I'd take the initiative. "
        m "I guess... It's all all about asking the right question... at the right time."

        show sylvie2 giggle

        s "It is. But now, stop being theoretical, and give me a kiss!"

        scene black
        with dissolve

        "And we got married shortly after that."
        "In fact, we made many more visual novels."
        "And together, we lived happily ever after."

        ".:. Good Ending."

        return

    label later:

        scene black
        with dissolve

        "And so I decided to ask her later."
        "But I was indecisive."
        "I couldn't ask her that day, and I couldn't ask her later."
        "I guess I will never know now."

        ".:. Bad Ending."

        return


options.rpy
-----------

::

    ## This file contains some of the options that can be changed to customize
    ## your Ren'Py game. It only contains the most common options... there
    ## is quite a bit more customization you can do.
    ##
    ## Lines beginning with two '#' marks are comments, and you shouldn't
    ## uncomment them. Lines beginning with a single '#' mark are
    ## commented-out code, and you may want to uncomment them when
    ## appropriate.

    init -1:
        python hide:

            ## Should we enable the use of developer tools? This should be
            ## set to False before the game is released, so the user can't
            ## cheat using developer tools.

            config.developer = True

            ## These control the width and height of the screen.

            config.screen_width = 800
            config.screen_height = 600

            ## This controls the title of the window, when Ren'Py is
            ## running in a window.

            config.window_title = u"The Question"

            ## We then want to call a theme function. themes.roundrect is
            ## a theme that features the use of rounded rectangles. It's
            ## the only theme we currently support.
            ##
            ## The theme function takes a number of parameters that can
            ## customize the color scheme.
            theme.roundrect(

                ## The color of an idle widget face.
                widget = "#F8AD00",

                ## The color of a focused widget face.
                widget_hover = "#E97F00",

                ## The color of the text in a widget.
                widget_text = "#581A00",

                ## The color of the text in a selected widget. (For
                ## example, the current value of a preference.)
                widget_selected = "#58A1FF",

                ## The color of a disabled widget face.
                disabled = "#404040",

                ## The color of disabled widget text.
                disabled_text = "#FFC89A",

                ## The color of informational labels.
                label = "#ffffff",

                ## The color of a frame containing widgets.
                frame = "#95850F",

                ## If this is True, in-game menus are placed in the center
                ## the screen. If False, they are placed inside a window
                ## at the bottom of the screen.
                button_menu = True,

                ## The background of the main menu. This can be a color
                ## beginning with '#', or an image filename. The latter
                ## should take up the full height and width of the screen.
                mm_root = "menu.jpg",

                ## The background of the game menu. This can be a color
                ## beginning with '#', or an image filename. The latter
                ## should take up the full height and width of the screen.
                gm_root = "menu2.jpg",

                ## And we're done with the theme. The theme will customize
                ## various styles, so if we want to change them, we should
                ## do so below.
                )


            #########################################
            ## These settings let you customize the window containing the
            ## dialogue and narration, by replacing it with an image.

            ## The background of the window. In a Frame, the two numbers
            ## are the size of the left/right and top/bottom borders,
            ## respectively.

            # style.window.background = Frame("frame.png", 12, 12)

            ## Margin is space surrounding the window, where the background
            ## is not drawn.

            # style.window.left_margin = 6
            # style.window.right_margin = 6
            # style.window.top_margin = 6
            # style.window.bottom_margin = 6

            ## Padding is space inside the window, where the background is
            ## drawn.

            # style.window.left_padding = 6
            # style.window.right_padding = 6
            # style.window.top_padding = 6
            # style.window.bottom_padding = 6

            ## This is the minimum height of the window, including the margins
            ## and padding.

            # style.window.yminimum = 250


            #########################################
            ## This lets you change the placement of the main menu.

            ## The way placement works is that we find an anchor point
            ## inside a displayable, and a position (pos) point on the
            ## screen. We then place the displayable so the two points are
            ## at the same place.

            ## An anchor/pos can be given as an integer or a floating point
            ## number. If an integer, the number is interpreted as a number
            ## of pixels from the upper-left corner. If a floating point,
            ## the number is interpreted as a fraction of the size of the
            ## displayable or screen.

            # style.mm_menu_frame.xpos = 0.5
            # style.mm_menu_frame.xanchor = 0.5
            # style.mm_menu_frame.ypos = 0.75
            # style.mm_menu_frame.yanchor = 0.5


            #########################################
            ## These let you customize the default font used for text in Ren'Py.

            ## The file containing the default font.

            # style.default.font = "DejaVuSans.ttf"

            ## The default size of text.

            # style.default.size = 22

            ## Note that these only change the size of some of the text. Other
            ## buttons have their own styles.


            #########################################
            ## These settings let you change some of the sounds that are used by
            ## Ren'Py.

            ## Set this to False if the game does not have any sound effects.

            config.has_sound = True

            ## Set this to False if the game does not have any music.

            config.has_music = True

            ## Set this to False if the game does not have voicing.

            config.has_voice = True

            ## Sounds that are used when button and imagemaps are clicked.

            # style.button.activate_sound = "click.wav"
            # style.imagemap.activate_sound = "click.wav"

            ## Sounds that are used when entering and exiting the game menu.

            # config.enter_sound = "click.wav"
            # config.exit_sound = "click.wav"

            ## A sample sound that can be played to check the sound volume.

            # config.sample_sound = "click.wav"

            ## Music that is played while the user is at the main menu.

            # config.main_menu_music = "main_menu_theme.ogg"


            #########################################
            ## Miscellaneous customizations

            ## These let you change the transitions that are used when entering
            ## and exiting the game menu.

            config.enter_transition = dissolve
            config.exit_transition = dissolve

