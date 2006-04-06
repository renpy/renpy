# This file contains the script for American Bishoujo's first game,
# "Moonlight Walks".
#
# We've released this to give an example of a complete game. It's okay
# to get ideas from this script, but remember, it's still copyright by
# me. This script may be distributed either modified or unmodified,
# provided a modified script is not called "Moonlight Walks".
#
# While I will probably allow people to translate this game not
# non-english languages, I ask that you contact me for permission
# before doing so.

# This file works with modern versions of Ren'Py, but uses the media
# that's shipped with the moonlight walks distribution.

init:
    # Basic configuration.
    $ config.screen_width = 800
    $ config.screen_height = 600
    $ config.window_title = 'Moonlight Walks'
    $ config.window_icon = 'icon32.png'

    # Menu backgrounds.
    $ style.mm_root_window.background = Image('beach1a.jpg')
    $ style.gm_root_window.background = Image('beach3.jpg')

    # File picker entry.
    $ style.file_picker_entry.background = Frame('saveslot.png', 16, 16)
    $ style.file_picker_entry.xpadding = 2
    $ style.file_picker_entry.ypadding = 2
    
    # Main menu window.
    $ style.mm_menu_window.background = Frame('saveslot.png', 16, 16)
    $ style.mm_menu_window.xpadding = 20
    $ style.mm_menu_window.ypadding = 20
    $ style.mm_menu_window.xpos = 0.5
    $ style.mm_menu_window.xanchor = 'center'
    $ style.mm_menu_window.ypos = 0.5
    $ style.mm_menu_window.yanchor = 'top'

    # Game menu window.
    $ style.gm_nav_window.background = Frame('saveslot.png', 16, 16)
    $ style.gm_nav_window.xpadding = 20
    $ style.gm_nav_window.ypadding = 20
    $ style.gm_nav_window.xpos = 0.5
    $ style.gm_nav_window.xanchor = 'center'

    # Colors of various labels.
    $ style.yesno_label.color = (255, 255, 0, 255)
    $ style.prefs_label.color = (255, 255, 0, 255)

    # Windows
    $ style.window.xmargin = 0
    $ style.window.ymargin = 0
    $ style.window.background = Frame('background.png', 16, 16)
    $ style.window.xpadding = 10
    $ style.window.ypadding = 5

    # This indents the second line of text that has been said by a
    # character. The goal is to push it past the opening quote (added
    # when the Characters are defined), so it looks better. 
    $ style.say_dialogue.rest_indent = 9

        
    # Transitions.
    # $ fade = Fade(.5, 0, .5) # Fade to black and back.
    $ dissolve = Dissolve(0.5)
    $ slowdissolve = Dissolve(1.0)

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

    # Well, stepping into the light, anyway.
    image heaven = Image("heaven.jpg")

    # Endings Common
    image good_ending = Image("ending.jpg")
    image bad_ending = Image("badending.jpg")

    # Mary.

    # We rendered each emotion that Mary has in two color
    # schemes... dark (for nighttime) and dawn.

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
    

    # Characters.

    # We put a blank name on top of the narration, so that the text of
    # the narration lines up with the text of dialogue.
    $ narrator = Character("", who_suffix='', what_prefix='', what_suffix='', what_style='say_thought')

    # We use what_prefix and what_suffix to ensure that all the
    # dialogue the various characters say is contained in quotes.    
    $ p = Character("", who_suffix='', what_prefix='"', what_suffix='"')
    $ pm = Character("Me, Speaking as a Minister", who_suffix=': ', what_prefix='"', what_suffix='"')

    $ g = Character("Girl", who_suffix=': ', what_prefix='"', what_suffix='"', color=(255, 128, 128, 255))
    $ m = Character("Mary", who_suffix=': ', what_prefix='"', what_suffix='"', color=(255, 128, 128, 255))

    # lm is short for little Mary. 
    $ lm = Character("Granddaughter", who_suffix=': ', what_prefix='"', what_suffix='"', color=(255, 255, 128, 255))

    # Translations.

    # We use this to change the label for the Music preference.
    $ library.translations = { 'Music' : 'Music and Ambient Sound' }

# This is right from extras/fullscreen.rpy. If we haven't already done
# so once, set the game to fullscreen on startup.
init:
    python:
        if not persistent.set_fullscreen:
            persistent.set_fullscreen = True
            _preferences.fullscreen = True

# Okay, the splashscreen is to pan down a big image to the
# beach. During the pan, dissolve in "American Bishoujo presents...",
# wait a few seconds, and dissolve it out again.
#
# I actually don't like this that much, in retrospect. The problem is
# that it's more expensive to draw one pan dissolving to another than
# a single pan... so the framerate jumps back and forth too much.
#
# Hopefully, we'll improve this a bit in the future.
label splashscreen:

    # Start with a black screen.
    scene black

    # This is necessary so we transition from the black screen.
    with None

    # Start us panning down the big beach picture. We actually start
    # 300 pixels down the 1800 pixel high picture... This sped it up
    # a bit, which looked better.
    scene bigbeach1 at Pan((0, 300), (0, 1200), 9.0)

    # Dissolve from black to the pan. We use the renpy.with function,
    # so that if the user clicks, we jump to the end_splash label.
    if renpy.with(dissolve):
        jump end_splash

    # We keep track of the time we've taken so far.
    # .5 s

    # Dissolve in the "American Bishoujo presents..."
    show presents at Position(yanchor='center', ypos=0.5)

    if renpy.with(slowdissolve):
        jump end_splash

    # 1.5 s

    # Pause for 2.5 seconds. Again, if the user clicks, we jump to
    # end_splash.
    if renpy.pause(2.5):
        jump end_splash

    # 4.0 s

    # Now, dissolve it out.
    hide presents
    
    if renpy.with(slowdissolve):
        jump end_splash

    # 5.0 s

    # Wait for 4 seconds for the pan to end.

    if renpy.pause(4.0):
        jump end_splash

    # 9.0 s
    



label end_splash:

    # At the end of the splash screen, we queue up a transition. This
    # transition will occur when the main menu is actually shown.
    $ renpy.transition(slowdissolve)

    return

# The main menu... play background noise, then jump to the real main
# menu.
label main_menu:
    $ renpy.music_start('waves.ogg')

    jump _library_main_menu

label start:

    # Did she tell us her family history?    
    $ family_history = False

    # Did we decide to meet again?
    $ meet_again = False

    $ renpy.clear_game_runtime()
    $ renpy.music_start('waves.ogg')

    scene beach1 title with None    
    scene beach1 with slowdissolve


    "It was the summer before I started college. I had spent the past
     two years studying, taking tests, and applying for admissions."

    "Now, for the first time in a while, I had a little downtime. So I
     decided to take the opportunity to explore America."

    "But, since I was broke, my plans were quickly scaled
     down to spending the summer at my aunt and uncle's house, on
     a small island known as North Sand Island."

    "North Sand Island was a barrier island in the Atlantic ocean. It
     was remote enough that there wasn't even a bridge to it, just a
     ferry that ran a few times a day."

    "Being such a small island, there wasn't all that much to do. But
     the solitude was nice, and I found ways to pass the time."

    "One thing I did was to take pictures with my digital camera. On
     the night of the full moon, I decided that I wanted to capture
     the moonrise."

    "So I went out to the beach just before the moon came up, set up my
     camera on a tripod, and locked in the appropriate shutter speed
     and f-stop."

    "Every few seconds as the moon rose, I used the remote that came
     with my camera to snap another frame showing the moon and its
     reflection in the water."

    "It only took a few minutes for the moon to rise over the horizon,
     but I kept at it for a while longer."

    "Finally, I was done. I started packing up my camera
     and my tripod, to get ready to head back to my aunt and
     uncle's house."

    scene beach1 mary with dissolve

    "That's when I first saw her. In the distance, I could see someone
     else walking down the beach."

    "I could tell that it was probably a girl or a woman from the long
     white dress she wore, but from that distance it was hard to tell
     anything else about her."

    "I decided to stay a bit to see who it was. In all the times I've
     gone out stargazing, I'd never met anyone just walking
     down the beach in the middle of the night."

    "At that late hour, most people were either at home, or in a
     town with other people. You hardly ever saw people by
     themselves."

    "The only time I've seen someone else on the beach at night would
     be when they are watching the stars or the satellites go by."

    "But those people stay still and look up at the sky, while this
     girl was looking down at the ground in front of her, watching
     where she was going."

    "I ran through a number of crazy scenarios in my head. Maybe she
     had some disease that meant she couldn't be out in the sun. Maybe
     she was looking for buried treasure."

    "It only took me a few seconds to dismiss these. What was the
     chance of them actually happening?"

    "I waited for a while, as she slowly made her way down the
     beach. I didn't think such a slow walk could be for
     exercise, but I had no idea what else she could be doing out
     there."

    # Change Mary's size.

    "Finally, she was close enough that I could get a good look at
     her, using the telephoto lens on my camera."

    "She was the most beautiful girl I'd ever seen. She was around my
     age, a year or two younger or older at the most, and in perfect
     shape."

    "Her skin was flawless, if a bit pale, and her hair was very
     light, almost as white as the long dress she was wearing."

    "Together, the combination of pale skin, light hair, and a white
     dress made her seem to glow in the moonlight."

    "She was a fair ways off, and I was pretty sure that she hadn't
     seen me. I knew what it was I wanted to do."

menu menu_1:

    "I knew that I wanted to take her picture.":
        jump take_her_picture

    "I knew that I needed to talk to her.":
        jump talk_to_her


label take_her_picture:

    "I thought I would be a failure as a photographer if I let such
     a beautiful sight go without capturing it, so I readied my camera
     to take her picture."

    "I didn't let her know I was there. It's best to take pictures of
     unaware people, because if they know you're taking their picture,
     they tend to pose unnaturally."

    "I set the camera to auto, framed her in the picture, and pressed the shutter release
     button. The camera beeped softly as it captured the picture."

    "I repeated this a dozen times. I find that it helps to take
     many pictures, in the hopes that one or two of them will come out
     perfectly."

    "When I was done taking the pictures, I lowered my camera and
     waved to her."

    "After a few seconds, she finally noticed me and waved back."

    "But she was still far enough away that if I had tried talking to
     her, my voice would have been lost over the crash of the waves."

    "I put my camera back into its case, picked up the tripod, and
     started heading back to my aunt and uncle's house."

    $ renpy.music_stop()
    $ renpy.play('click.wav')

    scene transfer

    "When I got back, I hooked the camera up to my computer, and
     started downloading the pictures I took that night."

    scene moonpic

    "The series of photographs of the moon came out well, but they
     weren't really what I was interested in."

    "I quickly skipped through them, looking for the pictures I took
     of the girl."

    $ renpy.play('click.wav')
    scene transfer

    "But when I finally got to the pictures I took of her, there was
     something strange about them."

    scene nogirlpic

    "She wasn't there."

    "I'm almost certain that I had framed the pictures right, but all
     I saw in them was the sandy beach behind where she was standing."

    "There were a dozen pictures like this. Each of them had the
     background of the shot I had framed, but the subject was nowhere
     to be seen."

    "I must have spent an hour slowly cycling through the pictures I
     took of the girl, hoping in vain that she would show up in
     at least one of them."

    "But she was never there."

    "The combination of her mysterious beauty and the strangeness of
     those pictures imprinted her image on my mind."

    "Even today, years later, I can close my eyes, think back, and see
     her as I saw her through my lens that day."

    $ renpy.music_start('waves.ogg')
    scene beach1 with dissolve

    "I went stargazing at that beach several times over the summer,
     hoping that I would be able to see her again."

    "But I never did."

    # .:. Ending 1 "No Dialogue"
    $ ending = 1, "Nothing to Say"
    jump ending


label talk_to_her:

    "As the girl was walking this way, I decided the best thing to do
     was to put my camera away and wait for her to come closer."

    "I didn't want to scare her away by running towards her, or to
     have to shout over the ocean waves."

    scene beach1
    show mary dark wistful
    with dissolve

    "After I had patiently waited for what must have been twenty
     minutes, she was finally close enough that I could talk to her in
     a reasonable voice."

    p "Hello."

    "Maybe it wasn't the most eloquent of lines, but it was all I
     could think of at the time, and it got the job done."

    "She stopped, and looked at me, as if waiting for me to say
     something else."

    p "It's a nice night. It's warm, but not really all that hot."

    "She nodded at this, but didn't say anything. I finally decided to
     cut to the chase and ask her the question on my mind."

    p "So what are you doing out here?"

    g "Walking."

    p "Just... walking? In the middle of the night?"

    g "Yes."

    p "Are you going anywhere in particular?"

    g "I walk around the island, following the beaches."

    "The island wasn't that big. I could go around it in a few hours,
     maybe a little more if I stopped for a break. I'd have no
     problems keeping up with her."


    p "Mind if I walk with you?"

    g "If that's what you want."

    "I decided that I'd bring my camera with me, but I hid my tripod
     and bag in the dunes."

    "This took only a few seconds, and we quickly started walking down
     the beach."
     
    
    scene beach2 with dissolve

    "We walked in silence for a while, until we could no longer see
     where we started."

    "I looked back anyway, and saw only our footprints breaking up the
     sand of the beach."

    "Walking was great, but I needed to try talking to this
     girl. I decided to see if I could find out why she was out
     at night."

    p "So..."

    show mary dark wistful with dissolve

    "She stopped, and looked at me."

    p "Is there a reason why we're walking down the beach at night?"

    g "It's something to do."

    p "I see. Do you do this often?"

    g "It seems like I do this every day."

    p "Do you always walk alone, or do other people come with you?"

    g "Usually, I'm walking by myself. But once in a while, I meet
       someone else, and sometimes they decide to walk with me."

    g "It's only happened a few times, though, and I don't think that
       anyone has asked as many questions as you."

    "I didn't know how to take this, and we stood in silence for a
     second."

    show mary dark smiling

    "Finally, she let out a small laugh, smiled, and took the
     initiative."    
    
    g "What were you doing out there?"

    "I didn't think that she was interested in me, and so it took me a
     second to respond to her question."

    "Seeing my hesitation, she elaborated."

    g "I think we both agree that it's rare to meet someone else out
       on the beach this time of night. So what were you doing there?"

    "It took me another second to think back to what I was doing, but
     finally I answered her."

    p "I'm into astronomy... well, stargazing, really. I was out
       taking digital photos of the moon as it rose."

    show mary dark confused wistful

    "She looked at me questioningly, as if she didn't know what I was
     talking about. I found that a little odd, as I thought everyone
     knew what a digital camera was."

    menu menu_01171024:
        "I decided to show her my camera.":

            "I decided that the easiest way to explain was to show her
             some of the pictures I had taken, and so I pulled my
             camera out of its case, and turned it on."

            "I switched it to displaying pictures, and called up one
             of the last pictures I had taken, one which showed the
             full disk of the moon."

            "I held up the camera to the girl, to let her see the
             picture on its screen."

            "She took a good look at it, turned to take a look at the
             moon in the sky, and then took another long
             look at the screen."

            g "The moon is... It's so small."

            "I didn't know what exactly she was trying to get at
             here."

            p "The pictures are small here, but they look much bigger on the
               computer screen."

            "I tried explaining, but it just seemed to confuse her even more, so
             I decided to change the topic."

        "I decided to show her the moon.":

            p "I was really into astronomy when I was young. I could
               look up at the moon and name all of the seas."

            g "Really?"

            p "Well, I can't do it anymore. But I still remember where
               one of the seas is."

            hide mary

            "I point up to the moon, and she turns to take a look at
             it." 

            p "Take a look at the right side of the moon. If you look,
               you can see what looks like a boy, with a head, body,
               and two legs."

            p "Do you see it?"

            g "I see it!"

            "She seemed excited by this, as if she had never
             looked at the moon like this before. Maybe
             she hadn't."

            "People look at the moon in different ways. Some people
             see a man, others a boy and a girl, others a rabbit."

            p "Well, if you look at his body, that's the sea of
               tranquility, where Neil Armstrong and Buzz Aldrin
               walked."

            show mary dark confused smiling with dissolve

            g "Buzz? Like the sound?"

            p "Well, his real name was Edwin. But everyone called him
               Buzz. I don't know why."

            "She didn't say anything, for a few seconds, as she took
             this in."

            g "So there are people walking around on the moon?"

            p "Not anymore. We sent the last people in the seventies,
               and nobody has been back there since."

            g "So we sent them?"

            p "Yes. Every man on the moon was an American."
            
            show mary dark smiling

            "She smiled at this, as if she had just found out and
             taken great satisfaction in this fact."

            "I thought it was odd, though, that she hadn't heard of
             the moon landings. I had though everyone learned about them
             when they were young."

            "Still, it gave me a sense of satisfaction to be the
             person that told her about them."

            "I decided that I would change the topic to something I
             was sure that she could talk about."

    p "Did you grow up around here?"

    show mary dark smiling

    g "I did."

    g "When I was growing up, there weren't all these houses and
       buildings on the island."

    g "The only things on the island were farms, and the farms were
       huge."

    g "Only four families lived here, and between us we owned all the
       land on the island."

    g "My family was one of the four. We owned the southern end of
       the island, where we first met."

    g "We hadn't cleared all of our land, but we had a large enough
       farm that we could grow the food we needed and sell some at
       market."

    "I didn't know that the island's population was so small, so
     recently. I knew that tourism could grow a population... but so
     quickly?"

    p "Did you go to school on the mainland, then?"

    g "Once in a while. When we took the ferry over to sell our produce,
       we would spend a few days in the school being tested."

    g "But most of the time, we were homeschooled."

    g "Mama would teach us reading and writing, and Papa would teach
       us math and things."

    show mary dark wistful

    g "At least, before they died..."

    "With this, her smile went away. It was obvious that this was a
     hard subject for her to talk about."

menu menu_2:

    "I asked her about her parents.":
        jump asked_about_parents

    "I dropped the subject.":
        jump dropped_it

label asked_about_parents:

    $ family_history = True

    p "What can you tell me about your parents?"

    g "Papa and Mama both came across the ocean as settlers when they
       were just children."

    g "Papa fought in the war. When it was over, he married Mama, and
       they used his pension to move here from the mainland, and to
       build us a house."

    g "Together, they farmed the land, and eventually they had
       children."

    g "I had an older sister and a younger sister. I was the middle
       child."

    show mary dark sad

    "She paused for a second to collect her thoughts before
     continuing. This part was taking a strain on her."

    g "When I was ten, an epidemic hit the island."

    g "We came down with it, and so did all of the other families."

    g "My family was too sick to move, but our neighbors, the Millers,
       sent some of their boys to get help from the mainland."

    "I remember thinking that Miller was the last name of my aunt and
     uncle, and wondering if they could be related to me."

    g "I don't know what happened to them, but I never heard from them
       again."


    show mary dark crying

    g "It lasted a week, and than it was over. My sisters... my
       parents... they all..."

    g "Now I'm the only one left."

    p "I'm sorry."

    "I didn't know what else to say to a girl that had lost her
     family, and was obviously broken up about it."

    show mary dark sad

    "She nodded in response, wiped her tears, and we once again
     started walking in silence."

    jump walking_again

label dropped_it:

    "It looked like if I asked her to continue, she would break out in
     tears. So I decided to let it go, and instead just started
     walking down the beach again."


label walking_again:

    scene beach3 with dissolve

    "I don't know how much time passed until we spoke again. Maybe it
     was an hour, maybe less, maybe longer."

    "We slowly made our way around the island, with me walking a few
     feet behind her."

    "If it had been someone else, I probably would have taken my leave
     and headed back for home."

    "But there was something about this girl that made me want to stay
     with her."

    "An aura, of some sort. Of beauty? Of tragedy? Of loneliness?
     Perhaps some combination of all of them, and more."

    "And so, we kept silently walking down the moonlit beach."


    "Finally, I couldn't take it any more, and I tried once again
     to strike up a conversation."

    show mary dark wistful with dissolve

    p "So... is there anything you want to do with your life?"

    "For a few seconds, she said nothing, as if I had said something
     wrong."

    "But then, she began to speak."

    show mary dark smiling

    g "Once, I thought I knew."

    g "When I was younger, it was like my life was planned out for me
       already. I would follow in my mother's footsteps."

    g "I'd help out on the farm for a few years. Even when we were
       young, we had chores, but when we finished our schooling we
       could help out even more."

    g "Eventually, I'd meet a nice boy. I didn't know who, at the
       time... Thinking back, it probably would have been one of the
       Miller boys. They were around my age."

    g "We would get married, and start a farm of our own."

    g "We'd raise a family together. A few girls, and I always wanted
       a boy, because all I had was sisters."

    show mary dark wistful

    g "Now, however..."

    "Her smile vanished as she let the thought trail off. After a
     little while, she changed the subject back to me."

    g "What about you? What do you plan to do in the future?"

    "Her question took me a little off guard, both because I wasn't expecting
     her to ask me the same thing, and because I'd never really thought
     much about my future."

    show mary dark smiling

    "She smiled a little at my obvious confusion."

    p "Well, I'm spending this summer visiting with my family. When
       it's over, I'll be going off to school."

    g "Aren't you a little old to still be in school?"

    p "Well, state school... I'm going to be attending a university in
       the fall."
    
    p "I don't know what I'll do after that... I don't even know what
       classes I'll be taking, or exactly what my major will be."

    p "I figure that when I'm not at school, I'll be living with my
       parents for a while."

    p "Eventually, I'll get a job and move out."

    p "As to settling down and starting a family... well, I have no
       idea about when that's going to happen."

    p "I haven't really thought much about it yet. I don't think many
       people have their lives as well planned as you."

    p "I think most people are just sort of winging it."

    show mary dark laughing

    "At this, she let out a quiet laugh."

    p "Is there something wrong with that?"

    show mary dark smiling

    g "No, no, nothing at all. In fact, I think I envy you."

    p "Why?"

    g "Well, you can do anything you want with your life. You can go
       anywhere you want."

    g "Some people would think that having too many choices is some
       sort of curse, or a burden."

    g "But I think it's just freedom, and that's a good thing."

    g "I think it's nice to live a life where your future is open,
       where you can do anything you want."

    "Once again, I didn't know what to say, and for a second I thought
     we'd go back to walking in silence."

    "But instead of letting the conversation falter, she kept it
     going."

    g "What do you do for fun?"

    p "Lots of things. I like drawing, listening to music, and
       watching cartoons and football on TV."

    show mary dark confused smiling

    g "Foot...ball?"

    "She repeated the term slowly, as if she knew both words, but had
     never heard them together in that way before."

    p "Yeah, football. You know, the sport... you've heard of it,
       right?"

    "She shook her head to indicate that she hadn't."

    p "How can I begin to describe it?"

    p "There are two teams on the field at once, and one of them has
       the ball. The center hikes the ball to the quarterback."

    p "The quarterback can either throw the ball to another player,
       hand it to another guy, or try to run with it."

    "Everything I said seemed to confuse her even more. But I didn't
     know what else to do, so I just kept on going."

    p "The other team tries to stop them by tackling the player with
       the ball. If they can't move the ball 10 yards in 4 downs, then
       the other team gets it..."

    show mary dark laughing

    "It was around this part of my explanation that she broke out
     giggling. Now that I look back on it, my explanation was sort of
     absurd."

    hide mary with dissolve

    "And so, we passed the night talking about things."

    "Mostly, I talked, and she listened. Sometimes she would ask me
     questions, and I would answer them as best I could."

    "Many times, that wouldn't be good enough, and she would break out
     laughing as I fumbled through another explanation."


    "We spent the rest of the night like this, talking and laughing
     as we made our way around the island."

    $ renpy.music_start('softwaves.ogg')
    scene dawn1 with dissolve
    show mary dawn smiling with dissolve


    "By dawn, we had made it almost all the way around the island, to
     a cliff not far from where we had first met."

    "The girl started to climb back down to the beach below, but I
     stopped her."

    show mary dawn confused smiling

    p "I thought we could stay here and watch the sun come up."

    show mary dawn confused wistful

    "To my surprise, her reaction to my explanation was one of
     shock."

    g "It's sunrise already? I have to be going!"

    "This came as a surprise to me. We had been getting along well, and
     now she was about to run off."

    show mary dawn wistful

    "She must have seen the disappointment on my face, as she changed
     her tone as she elaborated."

    g "It... it's not you, I like... it's just that I... I can't."

    p "I understand."

    "I said, not really understanding anything."

    hide mary with dissolve

    "As she started walking away, I searched my mind to see if there
     was anything I could say to keep her there just a little longer."

    "Suddenly, I realized that there was something I had forgotten to
     ask her."

menu menu_3:
    '"What is your name?"':

        "I realized that throughout the entire night, I had never
         asked her what her name was. A bad habit of mine is that I
         can have whole conversations without knowing someone's name."

        "So I asked her, almost shouting the question to her."

        show mary dawn smiling with dissolve

        "She stopped walking, turned back to me, and smiled."

        g "It's Mary... Mary Harper!"


    '"When can I see you again?"':

        "I realized I didn't know when I could see her again. Without
         knowing that, I'd probably never see her again."

        show mary dawn smiling with dissolve

        "She paused for a second, thinking, and then finally told me."

        g "You can meet me again on the night of the next full moon."

        p "The next full moon? That's not for almost a month. Can't we
           meet before then?"

        show mary dawn wistful

        g "I'm sorry... that's just the next time..."

        p "I understand. I'll be there, where we first met!"

        $ meet_again = True

# Fade to bright yellow, then fade to black.
scene yellow with dissolve
scene black with slowdissolve

"At that moment, the sun cleared the horizon. Its brilliance blinded
 me, and I reflexively closed my eyes."

"I've seen the sunrise many times, before and since, but I've never seen it
 as bright as it was that time."

scene dawn2 with dissolve

"When I opened my eyes again, the girl was gone."

"I didn't know why she went, how she had left so quickly, or where she
 had gotten off to."

"The one thing I did know was that I wanted to meet her again."

if meet_again:
    jump second_day

label ending2:

    "Having found out her name, I proceeded to look her up on the
     web."

    "Of course, the name \"Mary Harper\" gave me thousands of hits."

    "But after I narrowed it down to the local area, I got
     nothing at all."

    "According to the online phonebook, no one named \"Harper\" lived
     on the island."

    $ renpy.music_start('cars.ogg')                       
    scene library with dissolve
    
    "After getting some sleep, I went to the library to try to
     find out more about her."

    "Knowing she said that she was from around here, I took out a
     book on the history of North Sand Island."

    if family_history:

        "I figured that a family being wiped out by disease would be
         worth recording."

    "The only thing I found when I looked up \"Harper\" in the book was
     the story of a Harper family that lived on the island in the
     1780s."

    "They were wiped out by an epidemic that killed almost everyone
     on the island in 1790. Only a few boys escaped to tell the tale."

    "It left the island empty, and it wasn't until after the civil war
     that people settled here again."

    if family_history:

        "It's eerie how similar their situation was to what happened
         to Mary."

        "A father, mother, and three daughters, all wiped out by
         disease."

        "Along with everyone else on the island."

        "But, of course, it had to be a coincidence, since it happened
         over two centuries ago."

        "I couldn't find anything newer than that, and eventually gave
         up."

    else:

        "I looked through the book, and through the records of people
         living on the island after it was resettled."

        "Despite hours of searching, I couldn't find anyone named
         Harper."
        

    $ renpy.music_start('waves.ogg')
    scene beach1 with dissolve

    "That night, I went out to the beach where I first saw her, hoping
     to meet her again."

    "I spent the entire night there, but she didn't show up."

    "I tried again the next night, and the night after that. Every
     night for two weeks."

    "But after that first night, I never saw her again."

    "And I never forgot her, either."


    # .:. Ending 2 - History.
    $ ending = 2, "History"
    jump ending


label second_day:

    "It takes twenty-nine days for the moon to go from full to new to
     full again, and that's how long I had to wait before I could see
     her again."

    "It would have made for a really good story if I could have said I
     spent that entire time thinking about her, but that's not the way
     life works."

    "I'm sure I did other things, that month, but looking back I can
     hardly remember them."

    "I did spend quite a bit of time thinking about her, remembering
     her smile and her laugh."

    "Kicking myself for forgetting to ask her name."

    "Constantly checking and re-checking the exact moment of the full
     moon, to be sure that I showed up on the right night."

    $ renpy.music_start('waves.ogg')
    scene beach1 with dissolve

    "And finally, it was that night, and I found myself once again
     standing out on the beach, looking up at the moon."

    g "Were you waiting long?"

    show mary dark smiling with dissolve

    "I turned, and found her standing next to me."

    g "I wasn't really expecting you to be here. It's rare that I get
       to see someone a second time."

    p "Hey, I said I was going to be here, didn't I?"

    g "You did."

    p "I'm the type of guy who keeps his word. When I say I'm going to
       be somewhere, I'll be there."

    p "Besides, a guy would have to be crazy not to come back to see
       you again."

    p "Or did you not hear what I said? You left in an awful hurry
       last time. I didn't even get a chance to ask your name."

    g "Mary."

    m "It's Mary Harper."

    p "Well, Mary Harper, it's good to see you again, after almost an
       entire month."

    show mary dark wistful

    m "It's good to see you, too, but for me it feels like we were
       together only yesterday."

    "I didn't exactly pick up what she was saying here, so I just said
     what I was thinking before."

    p "I think it was the same way for me. I spent the entire month
       thinking about you."

    show mary dark smiling

    m "I'm not sure if it's exactly the same... but that's sweet."

    "I didn't know what to say after that, and so I didn't say
     anything."

    "Instead I simply motioned down the beach, and we started
     walking together, down the shore."

    scene beach2 with dissolve

    "It wasn't long before Mary broke the silence, by asking me a
     question."

    show mary dark smiling with dissolve

    m "I told you a little about my family... but I haven't asked you
       about yours yet. What's your family like?"
       
    p  "When I'm on the island here, I live with my aunt and uncle, but back
       home, I live with my mother, father, and sister."

    m "A sister? Is she older or younger?"

    p "She's two years younger than me."

    m "Do you get along with her well?"

    "I thought about how to answer this for a second, and decided that
     honesty was the best policy."

    p "Not really. We fight like cats and dogs."

    show mary dark laughing

    "At this, she gave a gentile laugh."

    show mary dark smiling

    m "What do you fight about?"

    p "Oh, it's never about the same two things. Put the two of us in
       a room together for a few hours, and all of a sudden, there's
       something... and we're at it again."

    "I was pretty sure I didn't want to keep going on about how my
     sister and I fought all the time, so I needed to find a way to
     get out of talking about it."

    if family_history:

        p "How did you get along with your sisters?"

        show mary dark wistful

        "For a second, I regretted asking that question, remembering
         how she nearly broke down last time she spoke about her
         family."

        show mary dark smiling
        
        "But this time, she seemed happy to talk about it."

        m "My sisters and I... we were the best of friends."

        m "We almost had to be, since our house was so small."

        m "Until I was seven, we even slept in the same bed."

        m "But we did everything together. When we had to do chores,
           we would all help each other out, and we got it done in
           half the time."

        p "Did you play together often?"

        m "We did! Papa built us all a dollhouse, and Mama made us
           all dolls, and we would play with them together."

        m "We would play house. Karen would be the father, I would be
           the mother, and Alice would be our daughter."

        m "We would sing, and make each other laugh. I haven't laughed
           like that since..."

        show mary dark wistful
        
        m "Well, since we met last month."

        "I heard the wistful tone in her voice, and decided to drop
         the subject. We started off again, walking down the beach."
        
    else:

        show mary dark confused smiling

        p "Look over there!"

        hide mary
        
        "I shouted the first thing that came to mind, and took off
         running down the beach."

        "She followed, chasing after me."

        "After a little bit, I slowed down and let her catch me."


        show mary dark laughing with dissolve

        m "Got you!"
    
        "She said, laughing as she grabbed hold of my shirt."

        hide mary with dissolve

        "And we kept walking, together, down the beach."

    scene beach3 with dissolve

    "As the night went by, we talked about many things. To be honest,
     I don't really remember exactly what we said."

    "What stayed with me are the sensations."

    "The smell of the salt in the sea air."

    "The sound of the waves hitting the shore."

    "The way the moonlight made her skin glow."

    "The feel of the sand as I tripped on a rock and fell."

    "The warmth of Mary's hand as she reached out and helped me back
     up."

    show mary dark wistful with dissolve

    m "Are you alright?"

    p "I think so. The sand was soft."

    show mary dark smiling

    m "I'm glad. What did you trip on?"

    p "I think it was a rock or something."

    "I turned to look at where I fell. There were rocks there, enough
     that it would have been hard to assign any one sole blame."

    m "Be careful. I wouldn't want you to be hurt."

    "I nodded, gave the rocks one last look, and turned to start
     walking again. But just then, a golden glint hit my eye."

    "I went over to where I saw the glint, and started digging. After
     a few seconds, Mary came over to where I was."

    show mary dark confused smiling

    m "Did you find something?"

    p "I don't..."

    "I was going to say I didn't know, but I stopped myself. For I had
     found what I was looking for."

    "In my hands was a gold ring. I held it up for Mary to take a look
     at."

    p "It's a ring."

    "I examined it a little more closely. It was far too light to be
     made of real gold, and a there were scratches where the gold
     plating was worn off."

    "I held it up so Mary could have a better look at it."

    show mary dark smiling

    m "It's beautiful!"

    p "It's not real. Someone took a metal ring and plated gold onto
       it to make it look nicer."

    m "But it's so pretty."

    p "If you like it, you can have it."

    show mary dark vhappy

    m "Can I?"

    p "Sure."

    m "Can you put it on for me?"

    "I didn't need to answer this, as she held out her hand. I took
     it, and slid the ring onto her finger. It was a perfect fit."

    m "Thank you!"

    hide mary with dissolve

    "With that, she grabbed onto my arm, and together, we started
     walking down the beach."

    $ renpy.music_start('softwaves.ogg')
    scene dawn1 with dissolve
                         
    "Before we knew it, it was dawn, and we found ourselves in the
     same place where we parted a month ago."

    p "Can you stay and watch the sunrise this time?"

    show mary dawn wistful with dissolve

    m "I'm sorry... I can't."

    p "Well, then when can I see you again?"

    m "I can only see you on the night of the full moon."

    "Even though I thought she might say this, it still hurt a little
     to hear it. I didn't know how I could go a month without seeing
     her."

    p "How come? Why can't I see you before then?"

    m "Because I'm a ghost."

    "She said it as if it was the most obvious thing in the world, as
     if someone telling you that she's a ghost is something that
     happens every day."

    "Not knowing exactly what to say, I just stood there in silence."
    
    "Eventually, Mary decided to elaborate on this, to tell me her
     story."

    m "I became a ghost, after I died... I died, along with my family,
       in the epidemic that hit this island when I was ten."

    m "For some reason, I came back on the night of the full moon. I
       just found myself here on the island."

    m "I came back on the night of the next full moon, and the next,
       and as far as I know every one after that. I always come back
       on the night of the full moon."

    m "I can do whatever I want that night, but when the sun rises,
       everything goes dark, and suddenly it's the next month."

    m "It's been that way for hundreds of years."

    m "It was boring for a while, but eventually people came back to
       the island. Once in a while, someone would meet me, like you
       did."

    m "We would talk for a while. But most of them were only
       interested in talking to me because I was a ghost."

    m "They always went away after a while. I guess there's only so
       much I can say about it."

    show mary dawn confused wistful

    m "Come to think of it, you never asked me about it. Didn't you
       figure it out?"

    menu menu_4:

        '"Of course I knew."':

            "In retrospect, it was obvious. The way she disappeared
             with that first sunrise, the way she knew nothing about
             things everyone alive today knows about..."

            "But it took her saying it for me to finally put the pieces
             together, and begin to accept it."

        '"I had no idea."':

            show mary dawn smiling

            m "You didn't? Usually people figure it out on the first
               night."

            m "That's the only reason people ever came back. They
               would come and talk to the ghost, until they lost
               interest."

            show mary dawn vhappy

            "She let out a small laugh, and then seemed to realize
             something."

            m "That means... you aren't here because I'm a ghost?"

            m "You came back because you chose to be with me?"

            "Once again, I was speechless, so we stood there for a
             little while."

    show mary dawn wistful
  
    "Finally, she broke the silence."

    m "The sun's almost up, and I need to be going."

    p "Don't go."

    show mary dawn confused wistful

    m "But..."

    hide mary with dissolve

    "I grabbed her hand, and pulled her close to me."

    p "Stay with me and watch the sunrise."

    "We didn't say anything after that. We just stood there, hand in
     hand, watching the sky slowly brighten."

    "I could feel her left hand in my right, as we stood there looking
     out over the ocean."

    scene dawn2 with dissolve
    
    "And then the sun rose, and suddenly my right hand was empty."

    "I turned to look, but the girl who was standing there was gone."

    p "I guess she really is a ghost."

    "I said, to no one in particular. She had told me, and I believed
     her, but until she disappeared, there was still a little bit of
     doubt."

    "I spent the morning standing at that cliff, thinking about
     it."

    menu menu_5:

        "And finally I realized,"

        "I had to set her free.":

            jump ending3

        "It didn't really matter.":

            jump ending4

##############################################################################
# Ending 3

label ending3:

    "I realized that it wasn't natural for someone like Mary to be
     trapped for hundreds of years as a ghost, condemned to show up
     only on the night of the full moon."

    "And despite my feelings for her, I came to the conclusion that
     the best thing I could do was to help her find peace."

    $ renpy.music_start('cars.ogg')
    scene library with dissolve

    "I spent the next month doing research in the island's small
     library."

    "I poured through every book they had on the occult. Ghosts,
     magic, witchcraft... things like that."

    "I read two or three books a day."

    "When I finished the few books the island's library had, I had
     them order more from the mainland."

    "It got to the point where most of the librarians knew me by
     name, and the rest knew me by my reputation as the college guy
     obsessed with the occult."

    "The thing with those books was that while most of their content
     was made up, deep under the surface some contained a small grain
     of truth."

    "The only way I could figure it out was to read everything I could
     on the subject, and figure out what it all had in common."

    "On the night of the next full moon, I was ready to put what I had
     learned into practice."

    $ renpy.music_start('waves.ogg')
    scene beach1 with dissolve
    show mary dark smiling with dissolve

    "I returned to the spot where we met on the first two nights, and
     watched the ocean waves slowly rolling in."

    "Mary was there, waiting for me."

    m "You came back."

    p "I wasn't going to leave you alone, after all that."

    "She doesn't say anything to this."

    p "So, what are we going to do tonight?"

    m "Usually, I spend the night walking around the island, like we
       did the other nights."

    p "I see. So, may I escort you?"

    m "Of course."

    hide mary with dissolve

    "She grabbed my arm, and we started off on our customary journey
     around the island."

    scene beach2 with dissolve 

    "We didn't talk as much this time. We didn't need to. Just being
     in each others presence was enough."

    "The chill in the air contrasted with the warmth of her skin."

    "Who would have thought that a ghost could be warm?"

    "We had a few short conversations, to pass the time."

    "But mostly, we walked in silence. The events of last time weighed
     heavily on us, as if we were both waiting for the other shoe to
     drop."

    "Finally, I couldn't take it anymore and came right out and asked
     her the question I needed to."

    show mary dark smiling with dissolve

    p "Mary, is there something you regret never being able to do?"

    "The key insight, the kernel of truth that I discovered in all
     those books was that the thing that makes a ghost is regret."

    show mary dark confused smiling

    m "What do you mean?"

    p "I don't know... Is there something you wanted to do, but were
       never able to?"

    show mary dark wistful

    "She thought about this for a while."
    
    "Finally, she responded in a barely audible whisper."

    m "I wanted to be a bride."

    "I knew it."

    "I had come up with a list of things Mary could possibly regret,
     and this was on the top of the list."

    "She had said her dream was to get married... heck, her dress even
     looked like a wedding dress."

    "I knew that if I loved her, there was only one thing I could
     do. So I got down on one knee and said,"

    p "Mary Harper, will you marry me?"

    show mary dark confused wistful

    "She was stunned by this... and stood there for a few seconds,
     saying nothing. Finally, she spoke."

    m "Are you sure... are you sure you want to marry... me?"

    p "The most sure that I've ever been."

    show mary dark vhappy

    m "Then... Yes!"

    show mary dark confused smiling

    "I got up, and we embraced. But she was still a little confused."

    m "But how can we do it? I can only go out at night, and I don't
       think that any minister would marry off a ghost."

    p "Don't worry. We can have a common law marriage."

    m "Common law?"

    p "As long as we say we're married, and make vows to each other,
       it counts."

    show mary dark vhappy

    m "Really? So when can we get married?"

    p "If you're ready, we can do it right now."

    m "I am!"

    p "Then let's do this."

    "I pulled out of my back pocket a sheet containing wedding vows
     that I had prepared."

    show mary dark smiling

    "I changed my voice to sound as if I was some sort of minister,
    and began reading."

    pm "Do you take this woman to be your wedded wife, to have and to
        hold, from this day forward, for better, for
        worse, for richer, for poorer, in sickness or in health, as
        long as you both exist?"

    "In my normal voice, I responded,"

    menu menu_ido:
        ' '
        
        '"I do."':

            pass

    "I turn to Mary and repeat the vow for her."

    pm "Do you take this man to be your wedded husband, to have and to
        hold, from this day forward, for better, for
        worse, for richer, for poorer, in sickness or in health, as
        long as you both exist?"

    m "I do."

    "We stood there for a second, before I finally continued."

    p "Well, that's it. We're married. All that's left is the kiss."

    "She came close to me, and we embraced."

    scene black with dissolve

    "I closed my eyes, waiting for her lips."

    m "Thank you."

    "I heard her whisper, and I felt the warmth of her lips as
     they touched mine."

    "Then I felt nothing but the cool night air."

    scene beach2 with dissolve

    "When I opened my eyes, I was alone."

    $ renpy.music_start('frogpond.ogg')
    scene littlemary
    
    lm "Ewww!"

    "My granddaughter's interruptions stops my telling of the story."

    lm "You kissed someone who wasn't Grandma!"

    lm "You _married_ someone who wasn't Grandma!"

    p "Well, that was before I met your grandmother."

    p "In fact, that's how I first met your grandmother. She was
       working as an intern at the library."

    p "And after that, I never saw Mary again."

    "She seems unconvinced."

    lm "Was that really a true story?"

    p "You have my word."

    "She thinks about this for a few seconds, before replying."

    lm "I don't believe you. Tell me another story!"

    p "Not tonight. It's after your bedtime."

    lm "But!"

    p "No buts, now it's time to get to sleep."

    scene black with dissolve

    "I turned off the lights, so that she could finally go to bed."

    "If I didn't, then my granddaughter would stay up all night, and
     never go to sleep."

    "My granddaughter Mary, whose name I suggested to my son-in-law
     while we were waiting in the hospital."

    "My granddaughter, named for the girl I was married to for a few
     moments, on a moonlit beach, long ago."

    # .:. Ending 3.
    $ ending = 3, "Married for Moments"
    jump ending



##############################################################################
# Ending 4

label ending4:

    $ renpy.music_start('waves.ogg')
    with None
    scene beach1
    show mary dark wistful
    with dissolve

    "A month later, I returned to the beach. This time, Mary was
     waiting for me."

    p "Hey."

    m "Welcome back. I suppose you have a few questions to ask
       me. Everyone always does."

    p "Not me."

    show mary dark confused wistful

    "This stopped her in her tracks."

    m "You don't have any questions? Doesn't it matter to you what I
       am?"

    p "What you are? What do you mean?"

    m "You know... a ghost."

    p "That's not what you are to me."

    show mary dark confused smiling

    p "To me, you're the girl I want to be with. The girl that I love."

    show mary dark smiling

    p "Beyond that, I doesn't matter if you're a ghost or if I'm a
       leprechaun."

    p "All of that is unimportant."

    p "What matters is that you're you, and I'm me, and that we're
       together."

    hide mary with dissolve

    "With this I started walking down the beach. She must have been
     too stunned to move, as she stood in one place for a while."

    "Finally, I turned to her, and asked:"

    p "Are you coming?"

    show mary dark vhappy with dissolve

    m "Yes!"

    "She cried out her response, and started running after me."

    "Together, we set off for another moonlight walk down the beach."

    hide mary with dissolve

    "From that night on, we spent every full moon together."

    "I went away to college, but I would always find time to drive
     down to the island to spend our night together."

    "My first job was on the mainland, right across from the island. I
     would schedule my days off to ensure that I had enough time to
     get to the beach before Mary appeared."

    "Eventually, I saved up enough money to buy a house on the beach,
     near where we first met."

    "I started a software consulting business out of my house. It paid
     the bills and then some, but the important part was I could
     always take time off around the full moon."

    "I never missed a night. I would be there, in clear weather and in
     rain. Once it even snowed, and once I had make my way through a
     hurricane."

    "Mary once said that it was nice to live a life where you could do
     what you want. Well, I knew what I wanted, and that was to spend
     my life with her."

    "Together, we celebrated my birthday seventy times, and hers
     twice. We never missed a night together."

    "Never, that is, until tonight."

    $ renpy.music_start('heartbeat.wav')
    scene hospital1 with dissolve
    # Music heartbeat

    "I'm dying."

    "It's not as bad as it sounds. I'm eighty-eight, and I guess
     it's just my time."

    "My heart is giving out, and I've told the doctors not to do
     anything when it goes."

    "Do I have any regrets? Not really."

    "Some people might think I would regret not having gotten married
     and having children."

    "But for me, Mary was enough, even if we never actually got
     married."

    "Besides, I used the money I made in my business to put my sister's
     children and grandchildren through school, and there's enough
     left that they'll all have a nice inheritance."

    "I'll leave the rest to charity. I think that taking care of my
     family and the world is as good a contribution to posterity as
     any."

    "There is one thing I do regret, and that's that I can't see Mary
     for one last time tonight."

    "It's the night of the full moon, but I'm stuck in this hospital
     bed, too weak to move on my own."

    
    "The end is near."

    "My sense of the world outside myself grows dim, and I focus
     more and more on my body as it starts to give out."

    # Stop music
    $ renpy.music_stop()

    "I feel my heartbeat growing fainter and fainter."

    # Play 1 heartbeat.
    $ renpy.play('heartbeat.wav')        

    "Beat."

    # Play 1 heartbeat.
    $ renpy.play('heartbeat.wav')        

    "Beat."

    "..."

    "..."

    "Finally, it stops entirely, and I realize that the end is upon me."

    scene hospital3 with slowdissolve

    "I was ready to face it alone, but now I realize I don't have
     to. Mary is standing here with me."

    "I don't know why or how... but I do know that she's here."
    
    m "What matters is ... that we're together."

    scene heaven with slowdissolve

    "The world becomes white, and I feel the years leaving me."

    "Now all I can see is Mary. For some reason she begins walking
     away from me."

    "After a few seconds, she turns back to me and asks:"

    m "Are you coming?"

    "I run to her, and somehow grab her hand."

    "Together, we step into the light."

    scene white with slowdissolve

    # .:. Ending 4.
    $ ending = 4, "Together, Into the Light"
    jump ending
    
label ending:

    scene black with slowdissolve
    
    $ ending_number, ending_name = ending
    
    ".:. Ending %(ending_number)d: %(ending_name)s" 

    if ending_number in (3, 4):
        scene good_ending
    else:
        scene bad_ending
        
    
    python hide:

        renpy.music_start('end_theme.ogg', 0)
        renpy.transition(slowdissolve)

        text = '"Moonlight Walks"\n\n\n'
        text += 'Story, Art, and Programming by PyTom.\n'
        text += "Powered by Ren'Py.\n\n\n\n\n\n"
        text += 'Thanks to the posters at the Lemmasoft Forums\nfor their support and advice.\n\n'
        text += 'Thank you for playing!\n\n\n'


        minutes, seconds = divmod(int(renpy.get_game_runtime()), 60)
        text += 'It took you %d:%02d to reach ending %d.' % (minutes, seconds, ending_number)


        # text += 'Copyright 2005 American Bishoujo'

        ui.vbox(ypos=0.5, xpos=0.5, xanchor='center', yanchor='center')

        ui.text(text, xpos=0.5, xanchor='center', ypos=0.5, yanchor='center',
                textalign=0.5)

        ui.textbutton('Return to the Main Menu.', clicked=ui.returns(True))
                                                                            

        ui.text("\nCopyright 2005 PyTom/American Bishoujo.\nSome Rights Reserved.",
                xpos=0.5, xanchor='center', ypos=0.5, yanchor='center',
                textalign=0.5)
        

        ui.close()
                                                                            
        ui.interact()
                   
    
        renpy.full_restart()
