
# game/tutorial_screen_displayables.rpy:3
translate schinese screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "屏幕语言中有不少显示对象。这里介绍其中最重要的几种。"

# game/tutorial_screen_displayables.rpy:9
translate schinese screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "你想了解哪一项？" nointeract

# game/tutorial_screen_displayables.rpy:49
translate schinese screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "每个屏幕语言显示对象都有一些共用属性。下面逐一演示。"

# game/tutorial_screen_displayables.rpy:57
translate schinese screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "首先，每个屏幕语言显示对象都支持位置属性。只要所在容器支持，就可以使用 align、anchor、pos 等属性。"

# game/tutorial_screen_displayables.rpy:69
translate schinese screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "at 属性会对显示对象应用变换，作用方式与 show 语句中的 at 子句相同。"

# game/tutorial_screen_displayables.rpy:106
translate schinese screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "id 属性主要用于显示对话的 say 屏幕。在其他屏幕中很少用到。"

# game/tutorial_screen_displayables.rpy:108
translate schinese screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "它会告诉 Ren'Py 哪个显示对象是背景窗口、谁在说话以及说了什么。过去它还用于应用每个角色的样式，并协助自动推进模式。"

# game/tutorial_screen_displayables.rpy:123
translate schinese screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "style 属性可指定单个显示对象所使用的样式。"

# game/tutorial_screen_displayables.rpy:144
translate schinese screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "style_prefix 属性会设置显示对象及其子对象所用样式的前缀。"

# game/tutorial_screen_displayables.rpy:146
translate schinese screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "例如，style_prefix 为“green”时，vbox 使用“green_vbox”样式，其中的文本使用“green_text”样式。"

# game/tutorial_screen_displayables.rpy:150
translate schinese screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "属性还不止这些，其余内容可以查阅文档。不过，在游戏的默认屏幕中，你通常会遇到的就是这些。"

# game/tutorial_screen_displayables.rpy:156
translate schinese add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "有时你会想把一个显示对象（例如图像）添加到屏幕上。"

# game/tutorial_screen_displayables.rpy:165
translate schinese add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "可以使用 add 语句完成，它会将图像或其他显示对象添加到屏幕。"

# game/tutorial_screen_displayables.rpy:167
translate schinese add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "引用图像有几种方式。如果图像位于 images 目录，或由 image 语句定义，只需把名称写在引号中即可。"

# game/tutorial_screen_displayables.rpy:176
translate schinese add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "也可以使用相对于游戏目录的文件名引用图像。"

# game/tutorial_screen_displayables.rpy:185
translate schinese add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "add 语句也能添加其他显示对象。这里用 Solid 显示对象显示一块纯色。"

# game/tutorial_screen_displayables.rpy:195
translate schinese add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "除了显示对象本身，add 语句还可以接受变换属性，用来放置或以其他方式变换所添加的显示对象。"

# game/tutorial_screen_displayables.rpy:207
translate schinese add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "当然，add 语句还支持 at 属性，让你可以指定更复杂的变换。"

# game/tutorial_screen_displayables.rpy:222
translate schinese text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "屏幕语言的 text 语句会向屏幕添加文本显示对象。它接受一个参数，即要显示的文本。"

# game/tutorial_screen_displayables.rpy:224
translate schinese text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "除了所有显示对象通用的属性，text 还接受文本样式属性。例如，size 用来设置文字大小。"

# game/tutorial_screen_displayables.rpy:234
translate schinese text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "text 显示对象还可以插值方括号中的值。"

# game/tutorial_screen_displayables.rpy:236
translate schinese text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "使用 text 语句在屏幕上显示文本时，屏幕内部定义的变量优先于屏幕外定义的变量。"

# game/tutorial_screen_displayables.rpy:238
translate schinese text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "这些变量可以是屏幕参数、通过 default 或 python 语句定义的变量，也可以由 SetScreenVariable 动作设置。"

# game/tutorial_screen_displayables.rpy:247
translate schinese text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "屏幕中的文本没有更多特殊之处，其工作方式与 Ren'Py 中的其他文本相同。"

# game/tutorial_screen_displayables.rpy:255
translate schinese layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "布局显示对象会接收其他显示对象，并将它们排布在屏幕上。"

# game/tutorial_screen_displayables.rpy:269
translate schinese layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "例如，hbox 显示对象会接收子对象，并将它们水平排列。"

# game/tutorial_screen_displayables.rpy:284
translate schinese layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "vbox 类似，不过会将子对象垂直排列。"

# game/tutorial_screen_displayables.rpy:286
translate schinese layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "两种 box 都接受 box 样式属性，其中最有用的是 spacing，即子对象之间要保留的间距。"

# game/tutorial_screen_displayables.rpy:301
translate schinese layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "grid 显示对象会把子对象排成大小相同的网格单元。它接受两个参数：列数和行数。"

# game/tutorial_screen_displayables.rpy:303
translate schinese layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "网格必须填满，否则 Ren'Py 会报错。注意在这个例子中，空单元格由 null 填充。"

# game/tutorial_screen_displayables.rpy:305
translate schinese layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "和 box 一样，grid 使用 spacing 属性指定单元格之间的间距。"

# game/tutorial_screen_displayables.rpy:321
translate schinese layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "grid 还接受 transpose 属性，使其先从上到下填充，再从左到右填充。"

# game/tutorial_screen_displayables.rpy:338
translate schinese layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "为了演示所有单元格大小相同，看看其中一个子对象比其他子对象更大时会发生什么。"

# game/tutorial_screen_displayables.rpy:353
translate schinese layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "fixed 显示对象使用 Ren'Py 的常规放置算法显示子对象，因此可以把显示对象放在屏幕的任意位置。"

# game/tutorial_screen_displayables.rpy:355
translate schinese layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "默认情况下，布局会扩展到填满所有可用空间。要阻止这一点，可以用 xsize 和 ysize 属性预先设置大小。"

# game/tutorial_screen_displayables.rpy:369
translate schinese layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "当非布局显示对象包含两个或更多子对象时，不必手动创建 fixed。Ren'Py 会自动添加一个 fixed，并将子对象放入其中。"

# game/tutorial_screen_displayables.rpy:384
translate schinese layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "最后介绍一种节省空间的写法。嵌套许多显示对象时，为每一层添加布局会造成很深、很难读的缩进。"

# game/tutorial_screen_displayables.rpy:386
translate schinese layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "has 语句会创建一个布局，然后把父对象后续的所有子对象添加到该布局中。这只是为了让屏幕代码更易读。"

# game/tutorial_screen_displayables.rpy:395
translate schinese window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "Ren'Py 为游戏创建的默认 GUI 中，大多数用户界面元素都需要某种背景。"

# game/tutorial_screen_displayables.rpy:405
translate schinese window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "没有背景时，文本可能难以阅读。frame 并非绝对必要，但许多屏幕会使用一个或多个 frame。"

# game/tutorial_screen_displayables.rpy:417
translate schinese window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "不过，加上背景后就容易读多了。因此，有两种显示对象专门为用户界面元素提供背景。"

# game/tutorial_screen_displayables.rpy:419
translate schinese window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "这两种显示对象是 frame 和 window。上面使用的是 frame，它可以为用户界面的任意部分提供背景。"

# game/tutorial_screen_displayables.rpy:423
translate schinese window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "window 显示对象则用途很专一，用来提供文本窗口。如果你正在读我说的话，现在看到的就是文本窗口。"

# game/tutorial_screen_displayables.rpy:425
translate schinese window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "frame 和 window 都可以接受 window 样式属性，用于修改背景以及窗口周围的外边距和内边距。"

# game/tutorial_screen_displayables.rpy:433
translate schinese button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "最灵活的显示对象之一是 button，以及它的 textbutton 和 imagebutton 变体。"

# game/tutorial_screen_displayables.rpy:443
translate schinese button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "button 是一种显示对象，选中后会执行一个动作。可以用鼠标点击、触摸、键盘或控制器选中按钮。"

# game/tutorial_screen_displayables.rpy:445
translate schinese button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "动作可以执行许多操作，例如设置变量、显示屏幕、跳转到标签或返回值。{a=https://www.renpy.org/doc/html/screen_actions.html}Ren'Py 文档{/a}列出了许多动作，你也可以自行编写动作。"

# game/tutorial_screen_displayables.rpy:458
translate schinese button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "也可以在按钮获得或失去焦点时执行动作。"

# game/tutorial_screen_displayables.rpy:473
translate schinese button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "button 会把另一个显示对象作为子对象。由于这个子对象可以是布局，按钮就能包含任意数量的子对象。"

# game/tutorial_screen_displayables.rpy:483
translate schinese button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "很多时候按钮需要显示文本。为此，可以使用 textbutton 显示对象，并把文本作为参数传入。"

# game/tutorial_screen_displayables.rpy:485
translate schinese button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "textbutton 显示对象会替你管理按钮文本的样式，因此默认 GUI 最常使用这种按钮。"

# game/tutorial_screen_displayables.rpy:498
translate schinese button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "还有 imagebutton，它接受一组显示对象，分别对应按钮可能处于的各种状态，并将它们作为按钮显示。"

# game/tutorial_screen_displayables.rpy:500
translate schinese button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "imagebutton 能让你最精确地控制按钮外观，但较难翻译，而且游戏窗口缩放后效果可能不佳。"

# game/tutorial_screen_displayables.rpy:522
translate schinese button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "button 接受 Window 样式属性，可用来指定背景、外边距和内边距。它还接受按钮专用属性，例如鼠标悬停时播放的声音。"

# game/tutorial_screen_displayables.rpy:524
translate schinese button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "与按钮一起使用时，可以给样式属性加上 idle、hover 等前缀，让属性随按钮状态变化。"

# game/tutorial_screen_displayables.rpy:526
translate schinese button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "textbutton 还接受以 text 为前缀的 Text 样式属性，这些属性会应用到它在内部创建的文本显示对象。"

# game/tutorial_screen_displayables.rpy:558
translate schinese button_displayables_b89d12aa:

    # e "Of course, it's pretty rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "当然，很少会像这样直接在屏幕中定制按钮。通常我们会创建自定义样式，然后告诉 Ren'Py 使用这些样式。"

# game/tutorial_screen_displayables.rpy:577
translate schinese bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "bar 和 vbar 是显示数值条的灵活显示对象。数值可以是静态的、随时间动画变化的，也可以由玩家调整。"

# game/tutorial_screen_displayables.rpy:579
translate schinese bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "value 属性接受一个 BarValue 对象，用来决定数值及其范围。这里用 StaticValue 将范围设为 100、数值设为 66，于是数值条填充了三分之二。"

# game/tutorial_screen_displayables.rpy:581
translate schinese bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "{a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}Ren'Py 文档{/a}列出了所有可用的 BarValue。"

# game/tutorial_screen_displayables.rpy:583
translate schinese bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "这个例子为 frame 设置了 xsize 属性。否则，数值条会扩展到填满所有可用的水平空间。"

# game/tutorial_screen_displayables.rpy:600
translate schinese bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "默认 GUI 定义了几种不同的数值条样式。样式由 style 属性选择，而默认样式则根据 value 决定。"

# game/tutorial_screen_displayables.rpy:602
translate schinese bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "最上面的样式是 bar。它用于显示玩家无法调整的数值，例如生命值条或进度条。"

# game/tutorial_screen_displayables.rpy:604
translate schinese bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "中间的样式是 slider。它用于显示玩家需要调整的数值，例如音量设置。"

# game/tutorial_screen_displayables.rpy:606
translate schinese bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "最下面的是 scrollbar，用于水平滚动条。作为滚动条使用时，中间的滑块会改变大小，以反映视口中当前可见的区域。"

# game/tutorial_screen_displayables.rpy:623
translate schinese bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "vbar 显示对象与 bar 类似，不过默认使用垂直样式 vbar、vslider 和 vscrollbar。"

# game/tutorial_screen_displayables.rpy:626
translate schinese bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "数值条接受 Bar 样式属性，可以大幅定制外观。看看 bar、slider 和 scrollbar 样式之间的差异就知道了。"

# game/tutorial_screen_displayables.rpy:635
translate schinese imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "imagemap 使用两个或更多图像来显示按钮和数值条。先来看看一个实际运行的 imagemap。"

# game/tutorial_screen_displayables.rpy:657
translate schinese swimming_405542a5:

    # e "You chose swimming."
    e "你选择了游泳。"

# game/tutorial_screen_displayables.rpy:659
translate schinese swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "游泳听起来很有趣，不过我没带泳衣。"

# game/tutorial_screen_displayables.rpy:665
translate schinese science_83e5c0cc:

    # e "You chose science."
    e "你选择了科学。"

# game/tutorial_screen_displayables.rpy:667
translate schinese science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "我听说有些学校有竞争激烈的科学队，但研究不能急于求成。"

# game/tutorial_screen_displayables.rpy:672
translate schinese art_d2a94440:

    # e "You chose art."
    e "你选择了艺术。"

# game/tutorial_screen_displayables.rpy:674
translate schinese art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "真正出色的背景美术很难制作，所以很多游戏会使用加滤镜的照片。也许你能改变这一点。"

# game/tutorial_screen_displayables.rpy:680
translate schinese home_373ea9a5:

    # e "You chose to go home."
    e "你选择了回家。"

# game/tutorial_screen_displayables.rpy:686
translate schinese imagemap_done_48eca0a4:

    # e "Anyway..."
    e "总之……"

# game/tutorial_screen_displayables.rpy:691
translate schinese imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "为了演示如何组合 imagemap，我来展示构成一个较小 imagemap 的五张图像。"

# game/tutorial_screen_displayables.rpy:697
translate schinese imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "idle 图像用于 imagemap 背景、未获得焦点或未选中的热点按钮，以及未获得焦点的数值条空白部分。"

# game/tutorial_screen_displayables.rpy:703
translate schinese imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "hover 图像用于已获得焦点但未选中的热点，以及已获得焦点的数值条空白部分。"

# game/tutorial_screen_displayables.rpy:705
translate schinese imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "注意这张图里数值条和按钮都高亮了。把它们作为屏幕的一部分显示时，只有一个会处于焦点状态。"

# game/tutorial_screen_displayables.rpy:711
translate schinese imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "selected_idle 之类的 selected 图像用于数值条的填充部分，以及已选中的按钮，例如当前屏幕和已勾选的复选框。"

# game/tutorial_screen_displayables.rpy:717
translate schinese imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "这里是 selected_hover 图像。图中的按钮永远不会显示，因为它永远不会被标记为已选中。"

# game/tutorial_screen_displayables.rpy:723
translate schinese imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "最后还可以提供 insensitive 图像，在热点无法交互时使用。"

# game/tutorial_screen_displayables.rpy:728
translate schinese imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "imagemap 不限于图像；凡是需要图像的地方，都可以使用任意显示对象。"

# game/tutorial_screen_displayables.rpy:743
translate schinese imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "这是用那五张图像构成的 imagemap。现在它已经是 imagemap 了，你可以与它互动。"

# game/tutorial_screen_displayables.rpy:755
translate schinese imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "为了让代码更简洁，可以用 auto 属性代替五张图像；它会根据需要将“%%s”替换为 idle、hover、selected_idle、selected_hover 或 insensitive。"

# game/tutorial_screen_displayables.rpy:757
translate schinese imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "如果游戏不需要 selected 或 insensitive 图像，可以省略它们。Ren'Py 会用 idle 或 hover 图像代替。"

# game/tutorial_screen_displayables.rpy:759
translate schinese imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "hotspot 和 hotbar 语句分别描述 imagemap 中应当充当按钮和数值条的区域。"

# game/tutorial_screen_displayables.rpy:761
translate schinese imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "两者都接受区域坐标，格式为 (x, y, width, height)。"

# game/tutorial_screen_displayables.rpy:763
translate schinese imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "hotspot 接受在热点激活时执行的动作。它还可以像按钮一样，接受在鼠标悬停和移开时执行的动作。"

# game/tutorial_screen_displayables.rpy:765
translate schinese imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "hotbar 接受一个 BarValue 对象，用来描述数值条的填充程度及其显示范围，与 bar 和 vbar 相同。"

# game/tutorial_screen_displayables.rpy:772
translate schinese imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "一种常见做法是定义一个带 imagemap 的屏幕，其中的热点跳转到各个标签，再用 call screen 语句调用这个屏幕。"

# game/tutorial_screen_displayables.rpy:774
translate schinese imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "之前展示的学校示例就是这样做的。这是它的脚本。脚本很长，但 imagemap 本身相当简单。"

# game/tutorial_screen_displayables.rpy:778
translate schinese imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "imagemap 有优点也有缺点。一方面，设计师很容易创建它，而且效果可能很好看；另一方面，它可能很难翻译，直接绘制在图像中的文字在窗口缩放后也可能变得模糊。"

# game/tutorial_screen_displayables.rpy:780
translate schinese imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "是否适合你的项目，由你和团队决定。"

# game/tutorial_screen_displayables.rpy:787
translate schinese viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "有时你会想显示比屏幕更大的内容，这时就可以使用 viewport 显示对象。"

# game/tutorial_screen_displayables.rpy:803
translate schinese viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "下面是一个简单 viewport 的例子，用来显示一张远大于屏幕的图像。由于 viewport 会扩展到屏幕大小，所以用 xysize 属性把它设为更小的尺寸。"

# game/tutorial_screen_displayables.rpy:805
translate schinese viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "viewport 默认不能移动，因此设置 draggable、mousewheel 和 arrowkeys 属性，就可以通过多种方式移动它。"

# game/tutorial_screen_displayables.rpy:820
translate schinese viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "设置 edgescroll 属性后，鼠标靠近 viewport 边缘时，它就会自动滚动。两个数字分别表示边缘大小，以及每秒滚动的像素数。"

# game/tutorial_screen_displayables.rpy:839
translate schinese viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "为 viewport 设置 scrollbars 属性后，周围会显示滚动条。scrollbars 属性可以取 both、horizontal 和 vertical。"

# game/tutorial_screen_displayables.rpy:841
translate schinese viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "spacing 属性控制 viewport 与滚动条之间的距离，单位是像素。"

# game/tutorial_screen_displayables.rpy:864
translate schinese viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "xinitial 和 yinitial 属性按可滚动总量的比例设置初始滚动位置。"

# game/tutorial_screen_displayables.rpy:885
translate schinese viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "最后是 child_size 属性。要说明它的作用，先看看没有这个属性时会发生什么。"

# game/tutorial_screen_displayables.rpy:887
translate schinese viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "可以看到，文本发生了换行，因为 Ren'Py 给它的空间不够大。"

# game/tutorial_screen_displayables.rpy:909
translate schinese viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "设置 child_size 后，屏幕会为子对象提供更多空间，从而可以滚动。它接受水平和垂直尺寸；如果其中一个分量为 None，就使用 viewport 的对应尺寸。"

# game/tutorial_screen_displayables.rpy:936
translate schinese viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "最后是 vpgrid 显示对象。它把 viewport 和 grid 合并为一个显示对象，而且效率更高，因为不必绘制每个子对象。"

# game/tutorial_screen_displayables.rpy:938
translate schinese viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "它接受 cols 和 rows 属性，分别指定子对象的列数和行数。如果省略其中一个，Ren'Py 会根据另一个属性和子对象数量推算出来。"

translate schinese strings:

    # game/tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "所有可视组件共享的常见属性。"

    # game/tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "添加图像和其他可视组件。"

    # game/tutorial_screen_displayables.rpy:9
    old "Text."
    new "文本。"

    # game/tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "框和其他布局。"

    # game/tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "窗口和框架。"

    # game/tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "按钮。"

    # game/tutorial_screen_displayables.rpy:9
    old "Bars."
    new "条。"

    # game/tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "视口。"

    # game/tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "图像映射。"

    # game/tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "目前就这些。"

    # game/tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "这使用位置属性。"

    # game/tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "世界颠倒了……"

    # game/tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "平衡飞行压力。"

    # game/tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "切换内部动力。"

    # game/tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "发射就位。"

    # game/tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "发射！"

    # game/tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "答案是[answer]。"

    # game/tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "文本标签在界面中{color=#c8ffc8}作用{/color}。"

    # game/tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "更大"

    # game/tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "这是一个界面。"

    # game/tutorial_screen_displayables.rpy:402
    old "Okay"
    new "确定"

    # game/tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "你点击了按钮。"

    # game/tutorial_screen_displayables.rpy:441
    old "Click me."
    new "点我。"

    # game/tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "你悬停在按钮上。"

    # game/tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "你离开了按钮。"

    # game/tutorial_screen_displayables.rpy:470
    old "Heal"
    new "治愈"

    # game/tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "这是一个文本按钮。"

    # game/tutorial_screen_displayables.rpy:539
    old "Or me."
    new "或者我。"

    # game/tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "你点击了另一个按钮。"

    # game/tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "这段文本比视口更宽。"
