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

# Declare characters used by this game.
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
    m "I guess... It's all about asking the right question... at the right time."

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
