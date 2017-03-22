# Declare images used by this game.
# image bg lecturehall = "lecturehall.jpg"
# image bg uni = "uni.jpg"
# image bg meadow = "meadow.jpg"
# image bg club = "club.jpg"
#
# image sylvie normal = "sylvie_normal.png"
# image sylvie giggle = "sylvie_giggle.png"
# image sylvie smile = "sylvie_smile.png"
# image sylvie surprised = "sylvie_surprised.png"
#
# image sylvie2 normal = "sylvie2_normal.png"
# image sylvie2 giggle = "sylvie2_giggle.png"
# image sylvie2 smile = "sylvie2_smile.png"
# image sylvie2 surprised = "sylvie2_surprised.png"

# Declare characters used by this game.
define s = Character('Sylvie', color="#c8ffc8")
define m = Character('Me', color="#c8c8ff")

# The game starts here.
label start:
    $ book = False

    play music "illurock.ogg"

    scene bg lecturehall
    with fade

    "It's only when I hear the sounds of shuffling feet and supplies being put away that I realize that the lecture's over."
    "Professor Eileen's lectures are usually interesting, but today I just couldn't concentrate on it."
    "I've had a lot of other thoughts on my mind...thoughts that culminate in a question."
    "It's a question that I've been meaning to ask a certain someone."

    scene bg uni
    with fade

    "When we come out of the university, I spot her right away."

    show sylvie normal
    with dissolve

    "I've known Sylvie since we were kids. She's got a big heart and she's always been a good friend to me."
    "But recently... I've felt that I want something more."
    "More than just talking, more than just walking home together when our classes end."
    "As soon as she catches my eye, I decide..."

    menu:

        "To ask her right away.":

            jump rightaway

        "To ask her later.":

            jump later


label rightaway:

    show sylvie smile

    s "Hi there! How was class?"
    m "Good..."
    "I can't bring myself to admit that it all went in one ear and out the other."
    m "Are you going home now? Wanna walk back with me?"
    s "Sure!"

    scene bg meadow
    with fade

    "After a short while, we reach the meadows just outside the neighborhood where we both live."
    "It's a scenic view I've grown used to. Autumn is especially beautiful here."
    "When we were children, we played in these meadows a lot, so they're full of memories."
    m "Hey... Umm..."

    show sylvie smile
    with dissolve

    "She turns to me and smiles. She looks so welcoming that I feel my nervousness melt away."
    "I'll ask her...!"
    m "Ummm... Will you..."
    m "Will you be my artist for a visual novel?"

    show sylvie surprised

    "Silence."
    "She looks so shocked that I begin to fear the worst. But then..."

    show sylvie smile

    s "Sure, but what's a \"visual novel?\""

    menu:

        "It's a videogame.":
            jump game

        "It's an interactive book.":
            jump book

label game:

    m "It's a kind of videogame you can play on your computer or a console."
    m "Visual novels tell a story with pictures and music."
    m "Sometimes, you also get to make choices that affect the outcome of the story."
    s "So it's like those choose-your-adventure books?"
    m "Exactly! I've got lots of different ideas that I think would work."
    m "And I thought maybe you could help me...since I know how you like to draw."
    m "It'd be hard for me to make a visual novel alone."

    show sylvie normal

    s "Well, sure! I can try. I just hope I don't disappoint you."
    m "You know you could never disappoint me, Sylvie."

    jump marry

label book:

    $ book = True

    m "It's like an interactive book that you can read on a computer or a console."
    show sylvie surprised
    s "Interactive?"
    m "You can make choices that lead to different events and endings in the story."
    s "So where does the \"visual\" part come in?"
    m "Visual novels have pictures and even music, sound effects, and sometimes voice acting to go along with the text."
    show sylvie smile
    s "I see! That certainly sounds like fun. I actually used to make webcomics way back when, so I've got lots of story ideas."
    m "That's great! So...would you be interested in working with me as an artist?"
    s "I'd love to!"

    jump marry

label marry:

    scene black
    with dissolve

    "And so, we become a visual novel creating duo."


    scene bg club
    with dissolve

    "Over the years, we make lots of games and have a lot of fun making them."

    if book:
        "Our first game is based on one of Sylvie's ideas, but afterwards I get to come up with stories of my own, too."

    "We take turns coming up with stories and characters and support each other to make some great games!"

    "And one day..."

    show sylvie2 normal
    with dissolve

    s "Hey..."
    m "Yes?"

    show sylvie2 giggle

    s "Will you marry me?"
    m "What? Where did this come from?"

    show sylvie2 surprised

    s "Come on, how long have we been dating?"
    m "A while..."

    show sylvie2 smile

    s "These last few years we've been making visual novels together, spending time together, helping each other..."
    s "I've gotten to know you and care about you better than anyone else. And I think the same goes for you, right?"
    m "Sylvie..."

    show sylvie2 giggle

    s "But I know you're the indecisive type. If I held back, who knows when you'd propose?"

    show sylvie2 normal

    s "So will you marry me?"
    m "Of course I will! I've actually been meaning to propose, honest!"
    s "I know, I know."
    m "I guess... I was too worried about timing. I wanted to ask the right question at the right time."

    show sylvie2 giggle

    s "You worry too much. If only this were a visual novel and I could pick an option to give you more courage!"

    scene black
    with dissolve

    "We get married shortly after that."
    "Our visual novel duo lives on even after we're married...and I try my best to be more decisive."
    "Together, we live happily ever after even now."

    "{b}Good Ending{/b}."

    return

label later:

    "I can't get up the nerve to ask right now. With a gulp, I decide to ask her later."

    scene black
    with dissolve

    "But I'm an indecisive person."
    "I couldn't ask her that day and I end up never being able to ask her."
    "I guess I'll never know the answer to my question now..."

    "{b}Bad Ending{/b}."

    return
