# TODO: Translation updated at 2017-09-06 22:45

# game/tutorial_screen_displayables.rpy:3
translate indonesian screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e ""

# game/tutorial_screen_displayables.rpy:9
translate indonesian screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "" nointeract

# game/tutorial_screen_displayables.rpy:49
translate indonesian screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e ""

# game/tutorial_screen_displayables.rpy:57
translate indonesian screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e ""

# game/tutorial_screen_displayables.rpy:69
translate indonesian screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e ""

# game/tutorial_screen_displayables.rpy:106
translate indonesian screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e ""

# game/tutorial_screen_displayables.rpy:108
translate indonesian screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e ""

# game/tutorial_screen_displayables.rpy:123
translate indonesian screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e ""

# game/tutorial_screen_displayables.rpy:144
translate indonesian screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e ""

# game/tutorial_screen_displayables.rpy:146
translate indonesian screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e ""

# game/tutorial_screen_displayables.rpy:150
translate indonesian screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e ""

# game/tutorial_screen_displayables.rpy:156
translate indonesian add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e ""

# game/tutorial_screen_displayables.rpy:165
translate indonesian add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e ""

# game/tutorial_screen_displayables.rpy:167
translate indonesian add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e ""

# game/tutorial_screen_displayables.rpy:176
translate indonesian add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e ""

# game/tutorial_screen_displayables.rpy:185
translate indonesian add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e ""

# game/tutorial_screen_displayables.rpy:195
translate indonesian add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e ""

# game/tutorial_screen_displayables.rpy:207
translate indonesian add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e ""

# game/tutorial_screen_displayables.rpy:222
translate indonesian text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e ""

# game/tutorial_screen_displayables.rpy:224
translate indonesian text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e ""

# game/tutorial_screen_displayables.rpy:234
translate indonesian text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e ""

# game/tutorial_screen_displayables.rpy:236
translate indonesian text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e ""

# game/tutorial_screen_displayables.rpy:238
translate indonesian text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e ""

# game/tutorial_screen_displayables.rpy:247
translate indonesian text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e ""

# game/tutorial_screen_displayables.rpy:255
translate indonesian layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e ""

# game/tutorial_screen_displayables.rpy:269
translate indonesian layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e ""

# game/tutorial_screen_displayables.rpy:284
translate indonesian layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e ""

# game/tutorial_screen_displayables.rpy:286
translate indonesian layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e ""

# game/tutorial_screen_displayables.rpy:301
translate indonesian layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e ""

# game/tutorial_screen_displayables.rpy:303
translate indonesian layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e ""

# game/tutorial_screen_displayables.rpy:305
translate indonesian layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e ""

# game/tutorial_screen_displayables.rpy:321
translate indonesian layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e ""

# game/tutorial_screen_displayables.rpy:338
translate indonesian layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e ""

# game/tutorial_screen_displayables.rpy:353
translate indonesian layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e ""

# game/tutorial_screen_displayables.rpy:355
translate indonesian layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e ""

# game/tutorial_screen_displayables.rpy:369
translate indonesian layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e ""

# game/tutorial_screen_displayables.rpy:384
translate indonesian layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e ""

# game/tutorial_screen_displayables.rpy:386
translate indonesian layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e ""

# game/tutorial_screen_displayables.rpy:395
translate indonesian window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e ""

# game/tutorial_screen_displayables.rpy:405
translate indonesian window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e ""

# game/tutorial_screen_displayables.rpy:417
translate indonesian window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e ""

# game/tutorial_screen_displayables.rpy:419
translate indonesian window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e ""

# game/tutorial_screen_displayables.rpy:423
translate indonesian window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e ""

# game/tutorial_screen_displayables.rpy:425
translate indonesian window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e ""

# game/tutorial_screen_displayables.rpy:433
translate indonesian button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e ""

# game/tutorial_screen_displayables.rpy:443
translate indonesian button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e ""

# game/tutorial_screen_displayables.rpy:445
translate indonesian button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e ""

# game/tutorial_screen_displayables.rpy:458
translate indonesian button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e ""

# game/tutorial_screen_displayables.rpy:473
translate indonesian button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e ""

# game/tutorial_screen_displayables.rpy:483
translate indonesian button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e ""

# game/tutorial_screen_displayables.rpy:485
translate indonesian button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e ""

# game/tutorial_screen_displayables.rpy:498
translate indonesian button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e ""

# game/tutorial_screen_displayables.rpy:500
translate indonesian button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e ""

# game/tutorial_screen_displayables.rpy:522
translate indonesian button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e ""

# game/tutorial_screen_displayables.rpy:524
translate indonesian button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e ""

# game/tutorial_screen_displayables.rpy:526
translate indonesian button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e ""

# game/tutorial_screen_displayables.rpy:558
translate indonesian button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e ""

# game/tutorial_screen_displayables.rpy:577
translate indonesian bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e ""

# game/tutorial_screen_displayables.rpy:579
translate indonesian bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e ""

# game/tutorial_screen_displayables.rpy:581
translate indonesian bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e ""

# game/tutorial_screen_displayables.rpy:583
translate indonesian bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e ""

# game/tutorial_screen_displayables.rpy:600
translate indonesian bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e ""

# game/tutorial_screen_displayables.rpy:602
translate indonesian bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e ""

# game/tutorial_screen_displayables.rpy:604
translate indonesian bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e ""

# game/tutorial_screen_displayables.rpy:606
translate indonesian bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e ""

# game/tutorial_screen_displayables.rpy:623
translate indonesian bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e ""

# game/tutorial_screen_displayables.rpy:626
translate indonesian bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e ""

# game/tutorial_screen_displayables.rpy:635
translate indonesian imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e ""

# game/tutorial_screen_displayables.rpy:657
translate indonesian swimming_405542a5:

    # e "You chose swimming."
    e ""

# game/tutorial_screen_displayables.rpy:659
translate indonesian swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e ""

# game/tutorial_screen_displayables.rpy:665
translate indonesian science_83e5c0cc:

    # e "You chose science."
    e ""

# game/tutorial_screen_displayables.rpy:667
translate indonesian science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e ""

# game/tutorial_screen_displayables.rpy:672
translate indonesian art_d2a94440:

    # e "You chose art."
    e ""

# game/tutorial_screen_displayables.rpy:674
translate indonesian art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e ""

# game/tutorial_screen_displayables.rpy:680
translate indonesian home_373ea9a5:

    # e "You chose to go home."
    e ""

# game/tutorial_screen_displayables.rpy:686
translate indonesian imagemap_done_48eca0a4:

    # e "Anyway..."
    e ""

# game/tutorial_screen_displayables.rpy:691
translate indonesian imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e ""

# game/tutorial_screen_displayables.rpy:697
translate indonesian imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e ""

# game/tutorial_screen_displayables.rpy:703
translate indonesian imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e ""

# game/tutorial_screen_displayables.rpy:705
translate indonesian imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e ""

# game/tutorial_screen_displayables.rpy:711
translate indonesian imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e ""

# game/tutorial_screen_displayables.rpy:717
translate indonesian imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e ""

# game/tutorial_screen_displayables.rpy:723
translate indonesian imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e ""

# game/tutorial_screen_displayables.rpy:728
translate indonesian imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e ""

# game/tutorial_screen_displayables.rpy:743
translate indonesian imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e ""

# game/tutorial_screen_displayables.rpy:755
translate indonesian imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e ""

# game/tutorial_screen_displayables.rpy:757
translate indonesian imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e ""

# game/tutorial_screen_displayables.rpy:759
translate indonesian imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e ""

# game/tutorial_screen_displayables.rpy:761
translate indonesian imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e ""

# game/tutorial_screen_displayables.rpy:763
translate indonesian imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e ""

# game/tutorial_screen_displayables.rpy:765
translate indonesian imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e ""

# game/tutorial_screen_displayables.rpy:772
translate indonesian imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e ""

# game/tutorial_screen_displayables.rpy:774
translate indonesian imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e ""

# game/tutorial_screen_displayables.rpy:778
translate indonesian imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e ""

# game/tutorial_screen_displayables.rpy:780
translate indonesian imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e ""

# game/tutorial_screen_displayables.rpy:787
translate indonesian viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e ""

# game/tutorial_screen_displayables.rpy:803
translate indonesian viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e ""

# game/tutorial_screen_displayables.rpy:805
translate indonesian viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e ""

# game/tutorial_screen_displayables.rpy:820
translate indonesian viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e ""

# game/tutorial_screen_displayables.rpy:839
translate indonesian viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e ""

# game/tutorial_screen_displayables.rpy:841
translate indonesian viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e ""

# game/tutorial_screen_displayables.rpy:864
translate indonesian viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e ""

# game/tutorial_screen_displayables.rpy:885
translate indonesian viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e ""

# game/tutorial_screen_displayables.rpy:887
translate indonesian viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e ""

# game/tutorial_screen_displayables.rpy:909
translate indonesian viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e ""

# game/tutorial_screen_displayables.rpy:936
translate indonesian viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e ""

# game/tutorial_screen_displayables.rpy:938
translate indonesian viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e ""

translate indonesian strings:

    # tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Text."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Buttons."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Bars."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Viewports."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new ""

    # tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new ""

    # tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new ""

    # tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new ""

    # tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new ""

    # tutorial_screen_displayables.rpy:116
    old "On internal power."
    new ""

    # tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new ""

    # tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new ""

    # tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new ""

    # tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new ""

    # tutorial_screen_displayables.rpy:336
    old "Bigger"
    new ""

    # tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new ""

    # tutorial_screen_displayables.rpy:402
    old "Okay"
    new ""

    # tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new ""

    # tutorial_screen_displayables.rpy:441
    old "Click me."
    new ""

    # tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new ""

    # tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new ""

    # tutorial_screen_displayables.rpy:470
    old "Heal"
    new ""

    # tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new ""

    # tutorial_screen_displayables.rpy:539
    old "Or me."
    new ""

    # tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new ""

    # tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new ""

