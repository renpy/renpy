# TODO: Translation updated at 2019-01-15 15:31

# game/tutorial_screens.rpy:165
translate korean tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e ""

# game/tutorial_screens.rpy:171
translate korean screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "" nointeract

# game/tutorial_screens.rpy:201
translate korean screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e ""

# game/tutorial_screens.rpy:203
translate korean screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e ""

# game/tutorial_screens.rpy:205
translate korean screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "" nointeract

# game/tutorial_screens.rpy:215
translate korean screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e ""

# game/tutorial_screens.rpy:217
translate korean screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e ""

# game/tutorial_screens.rpy:219
translate korean screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e ""

# game/tutorial_screens.rpy:221
translate korean screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e ""

# game/tutorial_screens.rpy:223
translate korean screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e ""

# game/tutorial_screens.rpy:230
translate korean screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e ""

# game/tutorial_screens.rpy:234
translate korean screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e ""

# game/tutorial_screens.rpy:241
translate korean screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e ""

# game/tutorial_screens.rpy:246
translate korean screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e ""

# game/tutorial_screens.rpy:265
translate korean screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."
    e ""

# game/tutorial_screens.rpy:267
translate korean screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e ""

# game/tutorial_screens.rpy:272
translate korean screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e ""

# game/tutorial_screens.rpy:274
translate korean screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e ""

# game/tutorial_screens.rpy:276
translate korean screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e ""

# game/tutorial_screens.rpy:278
translate korean screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e ""

# game/tutorial_screens.rpy:280
translate korean screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e ""

# game/tutorial_screens.rpy:286
translate korean screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e ""

# game/tutorial_screens.rpy:291
translate korean screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e ""

# game/tutorial_screens.rpy:293
translate korean screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e ""

# game/tutorial_screens.rpy:297
translate korean screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e ""

# game/tutorial_screens.rpy:301
translate korean screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e ""

# game/tutorial_screens.rpy:303
translate korean screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e ""

# game/tutorial_screens.rpy:310
translate korean screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e ""

# game/tutorial_screens.rpy:312
translate korean screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e ""

# game/tutorial_screens.rpy:335
translate korean screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e ""

# game/tutorial_screens.rpy:337
translate korean screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e ""

# game/tutorial_screens.rpy:339
translate korean screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e ""

# game/tutorial_screens.rpy:343
translate korean screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e ""

# game/tutorial_screens.rpy:350
translate korean screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e ""

# game/tutorial_screens.rpy:357
translate korean screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e ""

# game/tutorial_screens.rpy:369
translate korean screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e ""

# game/tutorial_screens.rpy:380
translate korean screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e ""

# game/tutorial_screens.rpy:398
translate korean screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e ""

# game/tutorial_screens.rpy:402
translate korean screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e ""

# game/tutorial_screens.rpy:404
translate korean screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e ""

# game/tutorial_screens.rpy:408
translate korean screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e ""

# game/tutorial_screens.rpy:432
translate korean screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e ""

# game/tutorial_screens.rpy:434
translate korean screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e ""

# game/tutorial_screens.rpy:454
translate korean screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e ""

# game/tutorial_screens.rpy:456
translate korean screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e ""

# game/tutorial_screens.rpy:475
translate korean screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e ""

# game/tutorial_screens.rpy:477
translate korean screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e ""

# game/tutorial_screens.rpy:479
translate korean screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e ""

# game/tutorial_screens.rpy:491
translate korean screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e ""

# game/tutorial_screens.rpy:503
translate korean screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e ""

# game/tutorial_screens.rpy:518
translate korean screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e ""

# game/tutorial_screens.rpy:520
translate korean screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e ""

# game/tutorial_screens.rpy:522
translate korean screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e ""

# game/tutorial_screens.rpy:536
translate korean screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e ""

# game/tutorial_screens.rpy:538
translate korean screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e ""

# game/tutorial_screens.rpy:557
translate korean screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e ""

# game/tutorial_screens.rpy:572
translate korean screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e ""

# game/tutorial_screens.rpy:588
translate korean screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e ""

# game/tutorial_screens.rpy:590
translate korean screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e ""

# game/tutorial_screens.rpy:592
translate korean screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e ""

# game/tutorial_screens.rpy:600
translate korean screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e ""

# game/tutorial_screens.rpy:616
translate korean screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e ""

# game/tutorial_screens.rpy:633
translate korean screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e ""

# game/tutorial_screens.rpy:635
translate korean screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e ""

# game/tutorial_screens.rpy:637
translate korean screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e ""

# game/tutorial_screens.rpy:653
translate korean screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e ""

# game/tutorial_screens.rpy:655
translate korean screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e ""

# game/tutorial_screens.rpy:657
translate korean screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e ""

# game/tutorial_screens.rpy:659
translate korean screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e ""

translate korean strings:

    # tutorial_screens.rpy:26
    old " Lv. [lv]"
    new ""

    # tutorial_screens.rpy:29
    old "HP"
    new ""

    # tutorial_screens.rpy:58
    old "Morning"
    new ""

    # tutorial_screens.rpy:58
    old "Afternoon"
    new ""

    # tutorial_screens.rpy:58
    old "Evening"
    new ""

    # tutorial_screens.rpy:61
    old "Study"
    new ""

    # tutorial_screens.rpy:61
    old "Exercise"
    new ""

    # tutorial_screens.rpy:61
    old "Eat"
    new ""

    # tutorial_screens.rpy:61
    old "Drink"
    new ""

    # tutorial_screens.rpy:61
    old "Be Merry"
    new ""

    # tutorial_screens.rpy:107
    old "Strength"
    new ""

    # tutorial_screens.rpy:111
    old "Intelligence"
    new ""

    # tutorial_screens.rpy:115
    old "Moxie"
    new ""

    # tutorial_screens.rpy:119
    old "Chutzpah"
    new ""

    # tutorial_screens.rpy:171
    old "What screens can do."
    new ""

    # tutorial_screens.rpy:171
    old "How to show screens."
    new ""

    # tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new ""

    # tutorial_screens.rpy:171
    old "Screen properties."
    new ""

    # tutorial_screens.rpy:171
    old "Special screen statements."
    new ""

    # tutorial_screens.rpy:171
    old "Using other screens."
    new ""

    # tutorial_screens.rpy:171
    old "That's it."
    new ""

    # tutorial_screens.rpy:205
    old "I do."
    new ""

    # tutorial_screens.rpy:331
    old "Hello, world."
    new ""

    # tutorial_screens.rpy:331
    old "You can't cancel this."
    new ""

    # tutorial_screens.rpy:346
    old "Shiro was here."
    new ""

    # tutorial_screens.rpy:362
    old "Click either button to continue."
    new ""

    # tutorial_screens.rpy:377
    old "Close This Screen"
    new ""

    # tutorial_screens.rpy:388
    old "A Tag Screen"
    new ""

    # tutorial_screens.rpy:395
    old "B Tag Screen"
    new ""

    # tutorial_screens.rpy:447
    old "You're on a small device."
    new ""

    # tutorial_screens.rpy:452
    old "You're not on a small device."
    new ""

    # tutorial_screens.rpy:466
    old "This text is red."
    new ""

    # tutorial_screens.rpy:496
    old "Hello, World."
    new ""

    # tutorial_screens.rpy:510
    old "It's good to meet you."
    new ""

    # tutorial_screens.rpy:534
    old "Increase"
    new ""

    # tutorial_screens.rpy:563
    old "Earth"
    new ""

    # tutorial_screens.rpy:563
    old "Moon"
    new ""

    # tutorial_screens.rpy:563
    old "Mars"
    new ""

    # tutorial_screens.rpy:581
    old "Now press 'a'."
    new ""

    # tutorial_screens.rpy:583
    old "The screen was just shown."
    new ""

    # tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new ""

    # tutorial_screens.rpy:608
    old "Health"
    new ""

    # tutorial_screens.rpy:613
    old "Magic"
    new ""

    # tutorial_screens.rpy:644
    old "There's not much left to see."
    new ""

