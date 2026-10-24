
# game/tutorial_screens.rpy:165
translate schinese tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e "屏幕是 Ren'Py 最强大的部分。屏幕可以定制游戏外界面，也可以创建新的游戏内界面组件。"

# game/tutorial_screens.rpy:171
translate schinese screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "你想了解屏幕的哪一方面？" nointeract

# game/tutorial_screens.rpy:201
translate schinese screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e "屏幕是 Ren'Py 用来创建用户界面的方式。除了图像和转场，你看到的一切都来自屏幕。"

# game/tutorial_screens.rpy:203
translate schinese screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e "我和你说话时使用的是 say 屏幕。它负责接收对话并呈现给玩家。"

# game/tutorial_screens.rpy:205
translate schinese screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "menu 语句显示游戏内选项时，则使用 choice 屏幕。明白了吗？" nointeract

# game/tutorial_screens.rpy:215
translate schinese screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e "文本输入使用 input 屏幕，NVL 模式使用 nvl 屏幕，等等。"

# game/tutorial_screens.rpy:217
translate schinese screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e "可以同时显示多个屏幕。例如，底部的“后退”“历史记录”“跳过”等按钮，都由一直显示的 quick_menu 屏幕负责显示。"

# game/tutorial_screens.rpy:219
translate schinese screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e "还有许多特殊屏幕，例如 main_menu、load、save 和 preferences。这里不一一列出，{a=https://www.renpy.org/doc/html/screen_special.html}请查阅文档{/a}。"

# game/tutorial_screens.rpy:221
translate schinese screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e "新建项目时，所有这些屏幕都位于 screens.rpy 中。编辑这个文件即可修改它们。"

# game/tutorial_screens.rpy:223
translate schinese screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e "你也不必局限于这些屏幕。在 Ren'Py 中，可以创建自己的屏幕，并将其用于游戏界面。"

# game/tutorial_screens.rpy:230
translate schinese screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e "例如，在 RPG 风格的视觉小说中，屏幕可以显示玩家的属性。"

# game/tutorial_screens.rpy:234
translate schinese screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e "说到这里，我应该先给你治疗一下。"

# game/tutorial_screens.rpy:241
translate schinese screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e "复杂的屏幕可以成为完整游戏机制的基础。像这样的属性屏幕，就可以作为恋爱或生活模拟游戏的基础。"

# game/tutorial_screens.rpy:246
translate schinese screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e "屏幕看起来可能很复杂，但其实只是许多简单部分协同工作，组合成更大整体的结果。"

# game/tutorial_screens.rpy:265
translate schinese screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."
    e "这是一个非常简单的屏幕示例。screen 语句告诉 Ren'Py 这里定义的是屏幕，屏幕名称为 simple_screen。"

# game/tutorial_screens.rpy:267
translate schinese screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e "在 screen 语句内部，各行可以引入 frame、vbox、text 和 textbutton 等显示对象，也可以设置 action、xalign 和 ypos 等属性。"

# game/tutorial_screens.rpy:272
translate schinese screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e "我会从内到外介绍这些语句。不过先显示这个屏幕，让你看看它实际运行的样子。"

# game/tutorial_screens.rpy:274
translate schinese screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e "text 语句用于显示给定的文本。"

# game/tutorial_screens.rpy:276
translate schinese screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e "textbutton 语句定义一个可以点击的按钮。点击按钮时，就会执行给定的动作。"

# game/tutorial_screens.rpy:278
translate schinese screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e "两者都位于 vbox（垂直框）中，因此文本会排列在按钮上方。"

# game/tutorial_screens.rpy:280
translate schinese screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e "vbox 又位于提供背景和边框的 frame 中。frame 的 at 属性接收一个变换，用来指定它的位置。"

# game/tutorial_screens.rpy:286
translate schinese screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e "有三个语句用于显示屏幕。"

# game/tutorial_screens.rpy:291
translate schinese screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e "第一个是 show screen 语句，它显示屏幕，并让 Ren'Py 继续执行。"

# game/tutorial_screens.rpy:293
translate schinese screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e "屏幕会一直显示，直到被隐藏。"

# game/tutorial_screens.rpy:297
translate schinese screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e "使用 hide screen 语句可以隐藏屏幕。"

# game/tutorial_screens.rpy:301
translate schinese screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e "call screen 语句会暂停 Ren'Py 的脚本执行，直到屏幕返回值，或将脚本跳转到其他位置。"

# game/tutorial_screens.rpy:303
translate schinese screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e "由于此时无法同时显示对话，你需要点击“确定”才能继续。"

# game/tutorial_screens.rpy:310
translate schinese screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e "call screen 语句结束时，屏幕会自动隐藏。"

# game/tutorial_screens.rpy:312
translate schinese screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e "通常，使用 show screen 显示始终存在的叠加层，使用 call screen 显示玩家只需暂时交互的屏幕。"

# game/tutorial_screens.rpy:335
translate schinese screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e "这是一个接收三个参数的屏幕示例。message 参数是要显示的消息，选择相应按钮时会执行 okay 或 cancel 动作。"

# game/tutorial_screens.rpy:337
translate schinese screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e "message 参数始终必须提供，而 okay 和 cancel 参数有默认值；未提供参数时会使用默认值。"

# game/tutorial_screens.rpy:339
translate schinese screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e "每个参数都是在屏幕内部定义的变量。在屏幕中，这些变量的优先级高于 Ren'Py 其他部分使用的同名变量。"

# game/tutorial_screens.rpy:343
translate schinese screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e "显示屏幕时，可以为每个参数提供实参。实参可以按位置或按名称提供。"

# game/tutorial_screens.rpy:350
translate schinese screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e "只要使用不同的参数重新显示屏幕，就可以改变屏幕显示的内容。"

# game/tutorial_screens.rpy:357
translate schinese screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e "和 show screen 一样，call screen 语句也可以接收参数。"

# game/tutorial_screens.rpy:369
translate schinese screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e "有几个属性可以直接应用于屏幕本身。"

# game/tutorial_screens.rpy:380
translate schinese screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e "modal 属性为 true 时，无法与屏幕下方的内容交互。必须点击“关闭此屏幕”才能继续。"

# game/tutorial_screens.rpy:398
translate schinese screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e "屏幕拥有 tag 属性时，会像图像名称中的标签部分一样处理。这里显示的是 a_tag_screen。"

# game/tutorial_screens.rpy:402
translate schinese screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e "显示 b_tag_screen 时，它会替换 a_tag_screen。"

# game/tutorial_screens.rpy:404
translate schinese screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e "这在游戏菜单和主菜单中很有用，例如让 load 屏幕替换 preferences 屏幕。默认情况下，这些屏幕的 tag 都是 menu。"

# game/tutorial_screens.rpy:408
translate schinese screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e "出于某种原因，tag 接收的是名称而不是表达式。现在已经来不及改了。"

# game/tutorial_screens.rpy:432
translate schinese screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e "zorder 属性控制屏幕相互叠加的顺序。zorder 数值越大，屏幕就越靠近玩家。"

# game/tutorial_screens.rpy:434
translate schinese screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e "屏幕的 zorder 默认是 0。当两个屏幕的 zorder 相同，后显示的屏幕会更靠近玩家。"

# game/tutorial_screens.rpy:454
translate schinese screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e "variant 属性会根据运行设备的特征选择屏幕。"

# game/tutorial_screens.rpy:456
translate schinese screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e "在这个例子中，第一个屏幕用于手机等小型设备，另一个屏幕用于平板电脑和计算机。"

# game/tutorial_screens.rpy:475
translate schinese screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e "最后，style_prefix 属性指定应用于屏幕内样式的前缀。"

# game/tutorial_screens.rpy:477
translate schinese screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e "指定 red 前缀时，frame 会使用 red_frame 样式，文本会使用 red_text 样式。"

# game/tutorial_screens.rpy:479
translate schinese screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e "为包含许多显示对象的屏幕设置样式时，这可以省下大量输入。"

# game/tutorial_screens.rpy:491
translate schinese screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e "屏幕语言还有一些用于执行其他操作的语句。如果还没看过{a=jump:warp_screen_displayables}屏幕显示对象{/a}一节，可以先去看看，再回到这里。"

# game/tutorial_screens.rpy:503
translate schinese screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e "python 语句的工作方式与脚本中的基本相同。用美元符号引入一行 Python，这一行会在屏幕每次更新时执行。"

# game/tutorial_screens.rpy:518
translate schinese screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e "同样，python 语句也可以引入缩进的 Python 语句块。不过，屏幕中的 Python 与脚本中的 Python 有一个重要区别。"

# game/tutorial_screens.rpy:520
translate schinese screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e "屏幕中使用的 Python 不允许产生副作用。这意味着它不能执行修改变量值之类的操作。"

# game/tutorial_screens.rpy:522
translate schinese screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e "这是因为 Ren'Py 在屏幕预测期间会运行屏幕及其中的 Python。"

# game/tutorial_screens.rpy:536
translate schinese screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e "default 语句可以在屏幕第一次运行时设置屏幕变量的值。之后可以使用 SetScreenVariable 和 ToggleScreenVariable 动作修改该值。"

# game/tutorial_screens.rpy:538
translate schinese screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e "default 语句与 Python 语句不同，它只运行一次。Python 会在屏幕每次更新时运行，因此用 Python 设置的变量不会保留变化。"

# game/tutorial_screens.rpy:557
translate schinese screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e "if 语句的工作方式与脚本中相同：条件为 true 时运行一个代码块，为 false 时运行另一个代码块。"

# game/tutorial_screens.rpy:572
translate schinese screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e "for 语句接收一个值列表并遍历它们；每次循环时，循环变量都会绑定到当前列表项，并执行循环体。"

# game/tutorial_screens.rpy:588
translate schinese screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e "on 和 key 语句通常只在屏幕的顶层使用才有意义。"

# game/tutorial_screens.rpy:590
translate schinese screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e "on 语句让屏幕在事件发生时执行动作。屏幕第一次显示时发生 show 事件，被隐藏时发生 hide 事件。"

# game/tutorial_screens.rpy:592
translate schinese screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e "key 事件会在按下按键时触发事件。"

# game/tutorial_screens.rpy:600
translate schinese screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e "屏幕语言的 use 语句可以把一个屏幕包含在另一个屏幕中，有助于避免屏幕代码重复。"

# game/tutorial_screens.rpy:616
translate schinese screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e "以这个显示两条属性的屏幕为例。这里已经有不少重复内容；如果属性更多，重复也会更多。"

# game/tutorial_screens.rpy:633
translate schinese screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e "这里把显示文本和数值条的语句移到了第二个屏幕，再用 use 语句把第二个屏幕包含到第一个屏幕中。"

# game/tutorial_screens.rpy:635
translate schinese screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e "属性名称和数值会作为参数传给屏幕，方式与 call screen 语句相同。"

# game/tutorial_screens.rpy:637
translate schinese screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e "这样既能控制重复内容的数量，也只需在一个地方修改属性。"

# game/tutorial_screens.rpy:653
translate schinese screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e "transclude 语句更进一步，让 use 语句可以接收一整个屏幕语言语句块。"

# game/tutorial_screens.rpy:655
translate schinese screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e "被包含的屏幕执行到 transclude 语句时，该语句会被 use 语句提供的代码块替换。"

# game/tutorial_screens.rpy:657
translate schinese screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e "第一个屏幕包含 boilerplate 屏幕，而第一个屏幕中的文本则通过 transclude 插入 boilerplate 屏幕。"

# game/tutorial_screens.rpy:659
translate schinese screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e "use 和 transclude 虽然复杂，却非常强大。仔细想想，使用“use boilerplate”距离编写自己的屏幕语言语句只差一步。"

translate schinese strings:

    # game/tutorial_screens.rpy:26
    old " Lv. [lv]"
    new " Lv. [lv]"

    # game/tutorial_screens.rpy:29
    old "HP"
    new "HP"

    # game/tutorial_screens.rpy:58
    old "Morning"
    new "早晨"

    # game/tutorial_screens.rpy:58
    old "Afternoon"
    new "下午"

    # game/tutorial_screens.rpy:58
    old "Evening"
    new "傍晚"

    # game/tutorial_screens.rpy:61
    old "Study"
    new "学习"

    # game/tutorial_screens.rpy:61
    old "Exercise"
    new "锻炼"

    # game/tutorial_screens.rpy:61
    old "Eat"
    new "吃"

    # game/tutorial_screens.rpy:61
    old "Drink"
    new "喝"

    # game/tutorial_screens.rpy:61
    old "Be Merry"
    new "开心"

    # game/tutorial_screens.rpy:107
    old "Strength"
    new "力量"

    # game/tutorial_screens.rpy:111
    old "Intelligence"
    new "智力"

    # game/tutorial_screens.rpy:115
    old "Moxie"
    new "勇气"

    # game/tutorial_screens.rpy:119
    old "Chutzpah"
    new "狂妄"

    # game/tutorial_screens.rpy:171
    old "What screens can do."
    new "界面能做什么。"

    # game/tutorial_screens.rpy:171
    old "How to show screens."
    new "如何显示界面。"

    # game/tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new "传递参数给界面。"

    # game/tutorial_screens.rpy:171
    old "Screen properties."
    new "界面属性。"

    # game/tutorial_screens.rpy:171
    old "Special screen statements."
    new "特殊界面语句。"

    # game/tutorial_screens.rpy:171
    old "Using other screens."
    new "使用其他界面。"

    # game/tutorial_screens.rpy:171
    old "That's it."
    new "就这些。"

    # game/tutorial_screens.rpy:205
    old "I do."
    new "我懂。"

    # game/tutorial_screens.rpy:331
    old "Hello, world."
    new "Hello, world."

    # game/tutorial_screens.rpy:331
    old "You can't cancel this."
    new "你不能取消这个。"

    # game/tutorial_screens.rpy:346
    old "Shiro was here."
    new "西罗刚才在这里。"

    # game/tutorial_screens.rpy:362
    old "Click either button to continue."
    new "单击任一按钮继续。"

    # game/tutorial_screens.rpy:377
    old "Close This Screen"
    new "关闭此界面"

    # game/tutorial_screens.rpy:388
    old "A Tag Screen"
    new "A标签界面"

    # game/tutorial_screens.rpy:395
    old "B Tag Screen"
    new "B标签界面"

    # game/tutorial_screens.rpy:447
    old "You're on a small device."
    new "你在使用小型设备。"

    # game/tutorial_screens.rpy:452
    old "You're not on a small device."
    new "你不在使用小型设备。"

    # game/tutorial_screens.rpy:466
    old "This text is red."
    new "这段文字是红色。"

    # game/tutorial_screens.rpy:496
    old "Hello, World."
    new "Hello, World."

    # game/tutorial_screens.rpy:510
    old "It's good to meet you."
    new "很高兴认识你。"

    # game/tutorial_screens.rpy:534
    old "Increase"
    new "增加"

    # game/tutorial_screens.rpy:563
    old "Earth"
    new "地球"

    # game/tutorial_screens.rpy:563
    old "Moon"
    new "月球"

    # game/tutorial_screens.rpy:563
    old "Mars"
    new "火星"

    # game/tutorial_screens.rpy:581
    old "Now press 'a'."
    new "现在按下“A”。"

    # game/tutorial_screens.rpy:583
    old "The screen was just shown."
    new "界面刚才显示了。"

    # game/tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new "你按了“A”键。"

    # game/tutorial_screens.rpy:608
    old "Health"
    new "体力"

    # game/tutorial_screens.rpy:613
    old "Magic"
    new "魔力"

    # game/tutorial_screens.rpy:644
    old "There's not much left to see."
    new "没什么可看的了。"
