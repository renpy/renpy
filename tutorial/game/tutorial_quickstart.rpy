#begin characters
define l = Character(_("Lucy"), color="#ffcccc")
#end characters

#begin slowdissolve
define slowdissolve = Dissolve(1.0)
#end slowdissolve

default name = "Player"

transform rightish:
    xcenter .6
    ypos 50

transform launcher_place:
    xpos 0.05
    xanchor 0
    ypos 0.1
    yanchor 0



label tutorial_create:

    show launcher step1 at launcher_place
    with dissolve

    e "When you're ready to use Ren'Py to create your visual novel, the first step is to create a new project."

    e "You can create a new project by clicking 'Create New Project' on the front screen of the launcher."

    e "If this is your first time using Ren'Py, it'll ask you for the place you want to keep your projects. The best place is always somewhere that's frequently backed up."

    show launcher step2

    e "After that, Ren'Py will ask for a name for your project. You'll have to stick to English letters and numbers, as zip files can't handle anything more than that."

    show launcher step3

    e "The next thing Ren'Py will ask for is the resolution the visual novel will run at. This controls how large or small you'll have to make your game's artwork."

    show launcher step4

    e "Finally, Ren'Py will ask you to select a color scheme. You can change this after the game has been created, so just pick a color that's pleasing."

    show launcher step5

    e "Once that's done, Ren'Py will work for a bit and return you to the main menu with the new project selected. Now, when you click Launch, Ren'Py will start your new game."

    e "To get back here, you can choose 'Tutorial' to switch to this tutorial game."

    e "You'll also need to edit the games script to make changes. To do that, click 'script.rpy' on the front page of the launcher."

    e "If it's your first time doing so, Ren'Py will ask you to select a text editor. Atom might be a safe choice, but read the descriptions to be sure."

    e "After the text editor is downloaded, the script will open up and you can start to change what characters are saying."

    hide launcher
    with dissolve

    return





label tutorial_dialogue:

    e "Probably the most common thing a creator does with Ren'Py is to write dialogue for the player to read."

    e "But before I can show you how to write dialogue, let me show you how we present script examples."

    example large:
        "Eileen" "Examples will show up in a window like the one above. You'll need to click outside of the example window in order to advance the tutorial."

        "Eileen" "When an example is bigger than the screen, you can scroll around in it using the mouse wheel or by simply dragging the mouse."

        "Eileen" "Script might seem scary at first, but if you look you'll see it's easy to match it up to what I'm saying."

    hide example

    e "Let's see the simplest possible Ren'Py game."

    scene black
    with dissolve

    example dialogue1 hide:

        "Wow, It's really really dark in here."

        "Lucy" "Better watch out. You don't want to be eaten by a Grue."

    scene bg washington
    show eileen happy
    with dissolve

    show example start dialogue1

    e "I'll show you the script of that example."

    e "This script demonstrates two kinds of Ren'Py statements, labels and say statements."

    e "The first line is a label statement. The label statement is used to give a name to a place in the program."

    e "In this case, we're naming a place \"start\". The start label is special, as it marks the place a game begins running."

    e "The next line is a simple say statement. It consists of a string beginning with a double-quote, and ending at the next double-quote."

    e "Special characters in strings can be escaped with a backslash. To include \" in a string, we have to write \\\"."


    hide example
    scene black
    with dissolve

    "Wow, It's really really dark in here."

    scene bg washington
    show eileen happy
    with dissolve


    show example start dialogue1

    e "When Ren'Py sees a single string on a line by itself, it uses the narrator to say that string. So a single string can be used to express a character's thoughts."

    hide example
    scene black
    with dissolve

    "Lucy" "Better watch out. You don't want to be eaten by a Grue."

    scene bg washington
    show eileen happy
    with dissolve

    show example start dialogue1

    e "When we have two strings separated by a space, the first is used as the character's name, and the second is what the character is saying."

    e "This two-argument form of the say statement is used for dialogue, where a character is speaking out loud."

    e "If you'd like, you can run this game yourself by erasing everything in your project's script.rpy file, and replacing it with the code in the box above."

    e "Be sure to preserve the spacing before lines. That's known as indentation, and it's used to help Ren'Py group lines of script into blocks."

    hide example

    e "Using a string for a character's name is inconvenient, for two reasons."

    e "The first is that's it's a bit verbose. While typing \"Lucy\" isn't so bad, imagine if you had to type \"Eileen Richardson\" thousands of times."

    e "The second is that it doesn't leave any place to put styling, which can change the look of a character."

    e "To solve these problems, Ren'Py lets you define Characters."

    show example characters

    e "Here's an example Character definition. It begins with the word \"define\". That tells Ren'Py that we are defining something."

    e "Define is followed by a short name for the character, like \"l\". We'll be able to use that short name when writing dialogue."

    e "This is followed by an equals sign, and the thing that we're defining. In this case, it's a Character."

    e "On the first line, the character's name is given to be \"Lucy\", and her name will be drawn a reddish color."

    e "These short names are case-sensitive. Capital L is a different name from lower-case l, so you'll need to be careful about that."

    hide example

    e "Now that we have a character defined, we can use it to say dialogue."

    scene black
    with dissolve

    example dialogue2 hide:

        l "Why are you trying to put words into my mouth? And who are you calling \"it\"?"

        l "What's more, what are you going to do about the Grue problem? Are you just going to leave me here?"

    scene bg washington
    show eileen happy
    with dissolve

    show example characters start dialogue1 dialogue2

    e "Here's the full game, including the two new lines of dialogue, both of which use the Character we defined to say dialogue."

    e "The one-argument form of the say statement is unchanged, but in the two-argument form, instead of the first string we can use a short name."

    e "When this say statement is run, Ren'Py will look up the short name, which is really a Python variable. It will then use the associated Character to show the dialogue."

    e "The Character object controls who is speaking, the color of their name, and many other properties of the dialogue."

    hide example

    e "Since the bulk of a visual novel is dialogue, we've tried to make it as easy to write as possible."

    e "Hopefully, by allowing the use of short names for characters, we've succeeded."

    return

label tutorial_images:

    e "A visual novel isn't much without images. So let's add some images to our little game."

    e "Before we can show images, we must first choose image names, then place the image files into the images directory."

    e "An image name is something like 'bg cave' or 'lucy happy', with one or more parts separated by spaces."

    e "Each part should start with a lower-case letter, and then contain lower-case letters, numbers, and underscores."

    e "The first part of an image is called the tag. For 'bg cave' the tag is 'bg', while for 'lucy happy' the tag is 'lucy'."

    e "You can open the images directory by clicking the appropriate button in the Ren'Py launcher."

    e "The files in the images directory should have the same name as the image, followed by an extension like .jpg, .png, or .webp."

    e "Our example uses 'bg cave.jpg', 'lucy happy.png', and 'lucy mad.png'."

    hide screen example

    e "Let's see what those look like in the game."

    example images1 hide:
        scene bg cave
        show lucy happy

        l "Now that the lights are on, we don't have to worry about Grues anymore."

        show lucy mad at right

        l "But what's the deal with me being in a cave? Eileen gets to be out in the sun, and I'm stuck here!"

    scene bg washington
    show eileen happy
    with dissolve

    show example start images1 large

    e "Here's the script for that scene. Notice how it includes two new statements, the scene and show statement."

    e "The scene statement clears the screen, and then adds a background image."

    e "The show statement adds a new image on top of all the other images on the screen."

    e "If there is already an image with the same tag, the new image is used to replace the old one."

    e "Changes to the list of shown images take place instantly, so in the example, the user won't see the background by itself."

    e "The second show statement has an at clause, which gives a location on the screen. Common locations are left, right, and center, but you can define many more."

    example:
        show logo base at rightish behind eileen

    e "In this example, we show an image named logo base, and we show it at a creator-defined position, rightish."

    e "We also specify that it should be shown behind another image, in this case eileen. That's me."

    example:
        hide logo

    e "Finally, there's the hide statement, which hides the image with the given tag."

    e "Since the show statement replaces an image, and the scene statement clears the scene, it's pretty rare to hide an image."

    e "The main use is for when a character or prop leaves before the scene is over."

    hide example

    return


example slightleft:
    transform slightleft:
        xalign 0.25
        yalign 1.0

label tutorial_simple_positions:

    e "When the standard positions that come with Ren'Py aren't enough for you, you can create your own. Here, I'll show you the easy way to do it."

    example:
        show eileen happy:
            xalign 0.75
            yalign 1.0

    with move

    e "The first way to do it is to show an image followed by a colon. Then indented on the next couple of lines are the xalign and yalign transform properties."

    e "Each of the transform properties is a name followed by a value. For xalign and yalign, the values are numbers."

    e "The xalign transform property is the important one, as it controls where the image is placed horizontally on the screen."


    example:
        show eileen happy:
            xalign 0.0
            yalign 1.0

    with move

    e "An xalign of 0.0 is the left side."


    example:
        show eileen happy:
            xalign 0.5
            yalign 1.0

    with move

    e "0.5 is the center."

    example:
        show eileen happy:
            xalign 1.0
            yalign 1.0

    with move

    e "And 1.0 is the right. The decimal place is important and has to be there. Just 1 by itself won't work the same."

    example:
        show eileen happy:
            xalign 0.75
            yalign 1.0

    with move

    e "Of course, you can pick any position in between."

    e "The yalign property is the same way, with 0.0 being the top of the screen and 1.0 being the bottom. Since most sprites stick to the bottom, it's almost always 1.0."

    hide example
    show eileen happy at center
    with move

    e "While being able to write positions like this is useful, having to repeatedly do so isn't. So Ren'Py lets you define a transform once, and reuse it."

    show example slightleft

    e "Usually transforms are defined at the top of a file, right after the characters. But it doesn't matter to Ren'Py where you define them."

    e "The transform is given a name, slightleft, and then the xalign and yalign properties."

    example:
        show eileen vhappy at slightleft

    with move


    e "Once a transform has been defined, you can use it in the at clause of the show statement."

    example:
        show eileen happy

    e "Transforms are sticky. If you replace an image without using a transform, Ren'Py will keep the same transforms it had been using."

    hide example

    e "Of course, there's a lot more to transforms than this. If you want to learn more, you can read the sections on Position Properties, Transforms and Animation, and Transform Properties."

    e "But for many visual novels, xalign and yalign are the only properties that matter."

    return










label tutorial_transitions:

    e "It can be somewhat jarring for the game to jump from place to place."

    scene bg whitehouse
    pause .5
    scene bg washington
    show eileen happy

    e "To help take some of edge off a change in scene, Ren'Py supports the use of transitions. Let's try that scene change again, but this time we'll use transitions."

    example trans1 hide:
        scene bg whitehouse
        with Dissolve(.5)

        pause .5

        scene bg washington
        show eileen happy
        with Dissolve(.5)

    show example trans1 large

    e "That's much smoother. Here's some example code showing how we include transitions in our game."

    e "It uses the with statement. The with statement causes the scene to transition from the last things shown to the things currently being shown."

    e "It takes a transition as an argument. In this case, we're using the Dissolve transition. This transition takes as an argument the amount of time the dissolve should take."

    e "In this case, each transition takes half a second."

    show example slowdissolve

    e "We can define a short name for a transition, using the define statement. Here, we're defining slowdissolve to be a dissolve that takes a whole second."

    hide example

    example trans2 hide:

        scene bg whitehouse
        with slowdissolve

        scene bg washington
        show eileen happy
        with slowdissolve

    show example trans2

    e "Once a transition has been given a short name, we can use it in our game."

    hide example

    e "Ren'Py defines some transitions for you, like dissolve, fade, and move. For more complex or customized transitions, you'll have to define your own."

    e "If you're interested, check out the Transitions Gallery section of this tutorial."

    return

label tutorial_music:

    e "Another important part of a visual novel or simulation game is the soundtrack."

    e "Ren'Py breaks sound up into channels. The channel a sound is played on determines if the sound loops, and if it is saved and restored with the game."

    e "When a sound is played on the music channel, it is looped, and it is saved when the game is saved."

    e "When the channel named sound is used, the sound is played once and then stopped. It isn't saved."

    e "The sounds themselves are stored in audio files. Ren'Py supports the Opus, Ogg Vorbis, and mp3 formats."

    e "Let's check out some of the commands that can affect the music channel."

    example:
        play music "sunflower-slow-drag.ogg" fadeout 1

    e "The play music command replaces the currently playing music, and replaces it with the named filename."

    e "If you specify the currently-playing song, it will restart it."

    e "If the optional fadeout clause is given, it will fade out the currently playing music before starting the new music."

    example:
        queue music "sunflower-slow-drag.ogg"

    e "The queue statement also adds music to the named channel, but it waits until the currently-playing song is finished before playing the new music."

    example:
        stop music fadeout 1

    e "The third statement is the stop statement. It stops the music playing on a channel. It too takes the fadeout clause."

    example:
        play sound "tower_clock.ogg"

    e "Unlike the music channel, playing a sound on the sound channel causes it to play only once."

    example:
        queue sound "tower_clock.ogg"
        queue sound "tower_clock.ogg"
        queue sound "tower_clock.ogg"

    e "You can queue up multiple sounds on the sound channel, but the sounds will only play one at a time."

    play music "sunflower-slow-drag.ogg"

    hide example

    e "Ren'Py has separate mixers for sound, music, and voices, so the player can adjust them as they like."

    return

label tutorial_menus:

    e "Many visual novels require the player to make choices from in-game menus. These choices can add some challenge to the game, or adjust it to the player's preferences."

    e "Do you like to play visual novels with choices in them?"

    example menu1 hide:
        menu:

            "Yes, I do.":
                jump choice1_yes

            "No, I don't.":
                jump choice1_no

        label choice1_yes:

            $ menu_flag = True

            e "While creating a multi-path visual novel can be a bit more work, it can yield a unique experience."

            jump choice1_done

        label choice1_no:

            $ menu_flag = False

            e "Games without menus are called kinetic novels, and there are dozens of them available to play."

            jump choice1_done

        label choice1_done:

            # ... the game continues here.


    show example menu1 large

    e "Here, you can see the code for that menu. If you scroll down, you can see the code we run after the menu."

    e "Menus are introduced by the menu statement. The menu statement takes an indented block, in which there can be one line of dialogue and multiple choices."

    e "Each choice must end with a colon, as each choice has its own block of Ren'Py code, that is run when that choice is selected."

    e "Here, each block jumps to a label. While you could put small amounts of Ren'Py code inside a menu label, it's probably good practice to usually jump to a bigger block of code."

    e "Scrolling down past the menu, you can see the labels that the menu jumps to. There are three labels here, named choice1_yes, choice1_no, and choice1_done."

    e "When the first menu choice is picked, we jump to the choice1_yes, which runs two lines of script before jumping to choice1_done."

    e "Similarly, picking the second choice jumps us to choice1_no, which also runs two lines of script."

    e "The lines beginning with the dollar sign are lines of python code, which are used to set a flag based on the user's choice."

    e "The flag is named menu_flag, and it's set to True or False based on the user's choice. The if statement can be used to test a flag, so the game can remember the user's choices."

    example:
        if menu_flag:

            e "For example, I remember that you plan to use menus in your game."

        else:

            e "For example, I remember that you're planning to make a kinetic novel, without menus."

    e "Here's an example that shows how we can test a flag, and do different things if it is true or not."


example:
    menu:
        e "Finally, this shows how you can show dialogue and menus at the same time. Understand?"

        "Yes.":

            e "Great."

        "No.":

            e "If you look at the example, before the first choice, there's an indented say statement."

label menu3_done:

    hide example

    e "Although we won't demonstrate it here, Ren'Py supports making decisions based on a combinations of points, flags, and other factors."

    e "One of Ren'Py's big advantages is the flexibility using a scripting language like Python provides us. It lets us easily scale from kinetic novels to complex simulation games."

    return

example guy:
    define g = Character("[name]")

label tutorial_input:

    e "Some games might prompt the player for input."

    example input hide:
        python:
            name = renpy.input(_("What's your name?"))

            name = name.strip() or __("Guy Shy")

    python:
        if name.lower() == "shiro":
            renpy.run(OpenURL("https://shiro-heartcat.tumblr.com/"))

    show example input

    e "That's done with Python, and especially the renpy.input function. The first line of this example prompts the player for some texts, and sticks it in the name variable."

    e "Often times, you'll want to clean the name up before you use it. The last line does that, by calling the strip method to remove whitespace, and replacing the name with a default if it's missing."

    example:

        e "To interpolate a variable, write it in square brackets. Isn't that right, [name]?"

    show example guy

    e "Variable names can also be shown in character names. To do that, just include the variable in square brackets in the character's name. Got it?"

    example:
        g "I think I do."


    example:
        $ answer = 42
        $ flag = True

        e "Variable interpolation also works with other variables. Here, the answer is [answer] and the flag is [flag]."

    return
