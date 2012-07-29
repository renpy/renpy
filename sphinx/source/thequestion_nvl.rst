.. _thequestion_nvl:

NVL-mode script for The Question
================================

Take "The Question" from the Ren'Py distribution, and replace the contents
of the ``script.rpy`` file with the following code.  Also, this script
uses a background image called ``nvl_window.png``, available
`here <http://www.renpy.org/w/images/8/8f/nvl_window.png>`_.

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

    # Declare characters
    define s = Character(None, kind=nvl, what_prefix="\"", what_suffix="\"",
                         what_color="#c8ffc8")
    define m = Character(None, kind=nvl, what_prefix="\"", what_suffix="\"",
                         what_color="#ffc8c8")
    define narrator = Character(None, kind=nvl)

    # NVL configuration
    init python:
        menu = nvl_menu

        # The color of a menu choice when it isn't hovered.
        style.nvl_menu_choice.idle_color = "#ccccccff"

        # The color of a menu choice when it is hovered.
        style.nvl_menu_choice.hover_color = "#ffffffff"

        # The color of the background of a menu choice, when it isn't
        # hovered.
        style.nvl_menu_choice_button.idle_background = "#00000000"

        # The color of the background of a menu choice, when it is
        # hovered.
        style.nvl_menu_choice_button.hover_background = "#ff000044"

        # How far from the left menu choices should be indented.
        style.nvl_menu_choice_button.left_margin = 20


        style.nvl_window.background = "nvl_window.png"
        style.nvl_window.xpadding = 55
        style.nvl_window.ypadding = 55

        config.empty_window = nvl_show_core
        config.window_hide_transition = dissolve
        config.window_show_transition = dissolve


    # The game starts here.
    label start:

        $ bl_game = False

        play music "illurock.ogg"

        scene bg lecturehall
        with fade

        window show

        "Well, professor Eileen's lecture was interesting, but to be honest,
         I couldn't concentrate on it very much."

        "I had a lot of other thoughts on my mind, and they all ended up with
         a question."

        "A question I've been meaning to ask someone."

        window hide
        nvl clear

        scene bg uni
        with fade
        window show

        "When we came out of the university, I saw her."

        window hide
        show sylvie normal
        with dissolve
        window show

        "She was a wonderful person. I've known her ever since we were children,
         and she's always been a good friend."

        "But... Recently... I think..."
        "... that I wanted more."

        "More just talking... more than just walking home together when our
         classes ended."

        menu:
            "And I decided..."

            "... to ask her right away.":

                jump rightaway

            "... to ask her later.":

                jump later


    label rightaway:

        nvl clear

        show sylvie smile

        s "Oh, hi, do we walk home together?"
        m "Yes..."
        "I said and my voice was already shaking."

        nvl clear

        window hide
        scene bg meadow
        with fade
        window show

        "We reached the meadows just outside our hometown. Autumn was so
         beautiful here."
        "When we were children, we often played here."

        m "Hey... ummm..."

        window hide
        show sylvie smile
        with dissolve
        window show

        "She turned to me and smiled."
        "I'll ask her..."
        m "Ummm... will you..."
        m "Will you be my artist for a visual novel?"

        show sylvie surprised

        nvl clear

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

        nvl clear

        m "It's a story with pictures and music. And you'll be able to make
           choices that influence the outcome of the story."
        s "So it's like those choose-your-adventure books?"
        m "Exactly! I plan on making a small romantic story. I figured you
           could help me... since I know how you like to draw."

        show sylvie normal

        s "Well, I can try. I hope I don't disappoint you."
        m "You can't disappoint me, you know that."

        jump marry

    label hentai:

        nvl clear

        $ bl_game = True

        m "Why it's a game with lots of sex."
        s "You mean, like a boy's love game? I've always wanted to make one of
           those. I'll get right on it!"

        hide sylvie
        with dissolve

        "..."

        m "That wasn't what I meant!"

        jump marry

    label marry:

        window hide
        nvl clear

        scene black
        with dissolve

        "--- years later ---"

        nvl clear

        scene bg club
        with dissolve
        window show

        "And so, we became a visual novel creating team. We made games and had
         a lot of fun making them."

        if bl_game:
            "Well, apart from that Boy's Love game she insisted on making."

        window hide
        nvl clear

        show sylvie2 normal
        with dissolve
        window show

        "And one day, she asked me..."

        s "Hey..."
        m "Yes?"

        show sylvie2 giggle

        s "Marry me!"
        m "What???"

        show sylvie2 surprised

        s "Well, don't you love me?"
        m "I do, actually."

        nvl clear
        show sylvie2 smile

        s "See? We've been making romantic visual novels, spending time
           together, helping each other... and when you give love to others,
           love will come to you."
        m "Hmmm, that's a nice thought."

        show sylvie2 giggle

        s "I just made that up."
        m "But it's good."

        nvl clear
        show sylvie2 normal

        s "I know. So, will you marry me?"
        m "Ummm, of course I will. I've actually been meaning to ask you, but
           since you brought it up..."
        s "I know, but you are so indecisive, that I thought I'd take the
           initiative. "
        m "I guess... It's all about asking the right question... at the
           right time."

        show sylvie2 giggle

        s "It is. But now, stop being theoretical, and give me a kiss!"

        nvl clear
        window hide
        scene black
        with dissolve

        "And we got married shortly after that. In fact, we made many more
         visual novels. And together, we lived happily ever after."

        ".:. Good Ending."

        return

    label later:

        nvl clear
        window hide

        scene black
        with dissolve

        "And so I decided to ask her later."
        "But I was indecisive."
        "I couldn't ask her that day, and I couldn't ask her later. I guess
         I will never know now."

        ".:. Bad Ending."

        return
