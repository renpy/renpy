
# game/tutorial_screen_displayables.rpy:3
translate schinese screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "有相当多的界面可视组件（displayable）。这里，我将告诉你一些最重要的。"

# game/tutorial_screen_displayables.rpy:9
translate schinese screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "你想知道什么？" nointeract

# game/tutorial_screen_displayables.rpy:49
translate schinese screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "有一些属性是每个界面语言可视组件共享的。这里，我给你演示一下。"

# game/tutorial_screen_displayables.rpy:57
translate schinese screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "首先，每个界面语言可视组件都支持位置属性。当可视组件所在的容器支持时，可以使用align、anchor、pos等属性。"

# game/tutorial_screen_displayables.rpy:69
translate schinese screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "at属性对可视组件应用变换，用法与show语句中at从句相同。"

# game/tutorial_screen_displayables.rpy:106
translate schinese screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "id属性主要用于say界面，say界面用于显示对话。在say界面之外，它不常用。"

# game/tutorial_screen_displayables.rpy:108
translate schinese screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "它告诉Ren'Py哪个可视组件是背景窗口，“who”在说话，“what”被说出来。这应用于每个Character样式，并帮助自动前进模式。"

# game/tutorial_screen_displayables.rpy:123
translate schinese screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "style属性允许您指定单个可视组件的样式。"

# game/tutorial_screen_displayables.rpy:144
translate schinese screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "style_prefix属性设置可视组件及其子组件使用的样式的前缀。"

# game/tutorial_screen_displayables.rpy:146
translate schinese screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "例如，当style_prefix属性为“green”时，vbox具有“green_vbox”样式，其中的文本具有“green_text”样式。"

# game/tutorial_screen_displayables.rpy:150
translate schinese screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "此外还有一些属性，你可以在文档中找到。但是这些是你在游戏中可以看到的，在默认界面上。"

# game/tutorial_screen_displayables.rpy:156
translate schinese add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "有时你会有一个可视组件，像一个图像，想添加到界面上。"

# game/tutorial_screen_displayables.rpy:165
translate schinese add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "这可以使用add语句，向界面添加图像或其他可视组件。"

# game/tutorial_screen_displayables.rpy:167
translate schinese add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "有几种方法可以引用图像。如果它在images目录中或是用image语句定义的，那么只需将名称放入带引号的字符串中。"

# game/tutorial_screen_displayables.rpy:176
translate schinese add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "图像也可以通过文件名引用，相对于game目录。"

# game/tutorial_screen_displayables.rpy:185
translate schinese add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "其他可视组件也可以使用add语句添加。这里，我们添加了Solid可视组件，显示一个实体块的颜色。"

# game/tutorial_screen_displayables.rpy:195
translate schinese add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "除了可视组件之外，add语句还可以用于变换属性。这些可以放置或变换加入的可视组件。"

# game/tutorial_screen_displayables.rpy:207
translate schinese add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "当然，add语句也可以使用at属性，进行更复杂的变换。"

# game/tutorial_screen_displayables.rpy:222
translate schinese text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "界面语言text语句向界面添加文本可视组件。它需要一个参数，即要显示的文本。"

# game/tutorial_screen_displayables.rpy:224
translate schinese text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "除了所有可视组件都有的常见属性外，文本还有文本样式属性。例如，size设置文本的大小。"

# game/tutorial_screen_displayables.rpy:234
translate schinese text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "文本可视组件还可以插入方括号中的值。"

# game/tutorial_screen_displayables.rpy:236
translate schinese text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "当使用text语句在界面中显示文本时，在界面中定义的变量优先于外部定义的变量。"

# game/tutorial_screen_displayables.rpy:238
translate schinese text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "那些变量也许是界面的参数，用默认或python语句定义，或者用SetScreenVariable动作设置。"

# game/tutorial_screen_displayables.rpy:247
translate schinese text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "关于界面中的文本没有更多要说的，它与Ren'Py中所有其他文本的作用方式相同。"

# game/tutorial_screen_displayables.rpy:255
translate schinese layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "布局可视组件获取其他可视组件并将其铺设在界面上。"

# game/tutorial_screen_displayables.rpy:269
translate schinese layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "例如，hbox可视组件会将其子组件水平排列。"

# game/tutorial_screen_displayables.rpy:284
translate schinese layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "vbox可视组件与之类似，只不过它将子组件竖直排列。"

# game/tutorial_screen_displayables.rpy:286
translate schinese layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "这两个框（box）都采用了框样式属性，其中最有用的是间距（spacing），即子组件之间留出的空间量。"

# game/tutorial_screen_displayables.rpy:301
translate schinese layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "网格（grid）可视组件在大小相等的单元格网格中显示其子组件。它需要两个参数，列数和行数。"

# game/tutorial_screen_displayables.rpy:303
translate schinese layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "网格必须填满，否则Ren'Py将产生错误。注意在这个例子中，空单元格是如何用null填充的。"

# game/tutorial_screen_displayables.rpy:305
translate schinese layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "与框一样，grid使用spacing属性指定单元格之间的距离。"

# game/tutorial_screen_displayables.rpy:321
translate schinese layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "grid还接受transpose属性，使其先从上到下、再从左到右填充。"

# game/tutorial_screen_displayables.rpy:338
translate schinese layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "为了展示所有单元格的大小是相等的，这里是当一个子组件比其他子组件大时发生的事情。"

# game/tutorial_screen_displayables.rpy:353
translate schinese layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "fixed可视组件使用Ren'Py正常的放置算法显示子组件。你可以将可视组件放在界面的任意位置。"

# game/tutorial_screen_displayables.rpy:355
translate schinese layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "默认情况下，布局会扩展以填充所有可用空间。为了避免这种情况，我们使用xsize和ysize属性预先设置其大小。"

# game/tutorial_screen_displayables.rpy:369
translate schinese layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "当一个无布局的可视组件被赋予两个以上子组件时，不需要创建fixed。fixed将自动创建，并将子对象添加到其中。"

# game/tutorial_screen_displayables.rpy:384
translate schinese layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "最后，还有节省空间的便利。当许多可视组件嵌套时，为每一项添加布局可能会导致令人抓狂的缩进级别。"

# game/tutorial_screen_displayables.rpy:386
translate schinese layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "has语句创建一个布局，然后将其父组件的所有子组件添加到其中。这只是为了让界面便于阅读。"

# game/tutorial_screen_displayables.rpy:395
translate schinese window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "在Ren'Py为游戏创建的默认GUI中，大多数用户界面元素都需要某种背景。"

# game/tutorial_screen_displayables.rpy:405
translate schinese window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "没有背景，文本可能很难阅读。虽然frame不是严格需要的，但许多界面都有一个以上。"

# game/tutorial_screen_displayables.rpy:417
translate schinese window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "但当我加上背景的时候，就容易多了。这就是为什么有两个可视组件是用来给用户界面元素提供背景的。"

# game/tutorial_screen_displayables.rpy:419
translate schinese window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "两个可视组件是框架（frame）和窗口（window）。frame是我们在上面使用的，它被设计来为用户界面的任意部分提供背景。"

# game/tutorial_screen_displayables.rpy:423
translate schinese window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "另一方面，window可视组件非常具体。它用于提供文本窗口。如果你正在读我说的话，你就在看文本窗口。"

# game/tutorial_screen_displayables.rpy:425
translate schinese window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "frame和window都可以指定窗口样式属性，允许您更改背景（background）、窗口周围的外边距（margin）和内边距（padding）。"

# game/tutorial_screen_displayables.rpy:433
translate schinese button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "最灵活的可视组件之一是按钮（button）可视组件，以及文本按钮（textbutton）和图像按钮（imagebutton）变体。"

# game/tutorial_screen_displayables.rpy:443
translate schinese button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "按钮是被选中时运行动作（action）的可视组件。按钮可以用鼠标单击、触摸或键盘和控制器来选择。"

# game/tutorial_screen_displayables.rpy:445
translate schinese button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "动作可以做很多事情，比如设置变量、显示界面、跳转到标签或返回值。有很多{a=https://www.renpy.org/doc/html/screen_actions.html}Ren'Py文档中的动作{/a}，您也可以自己编写。（{a=https://renpy.cn/doc/screen_actions.html}中文文档{/a}）"

# game/tutorial_screen_displayables.rpy:458
translate schinese button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "当按钮获得或失去焦点时，也可以运行动作。"

# game/tutorial_screen_displayables.rpy:473
translate schinese button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "按钮将另一个可视组件作为子组件。因为子组件可以是布局，所以按钮可以包含任意数量的子组件。"

# game/tutorial_screen_displayables.rpy:483
translate schinese button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "许多情况下，按钮会被赋予文本。更简单的，这里有使用文本作为参数的textbutton可视组件。"

# game/tutorial_screen_displayables.rpy:485
translate schinese button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "由于textbutton可视组件为您管理按钮文本的样式，因此它是默认GUI中最常用的一种按钮。"

# game/tutorial_screen_displayables.rpy:498
translate schinese button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "还有imagebutton，它需要一系列可视组件，每个对应一个按钮状态，并作为按钮显示。"

# game/tutorial_screen_displayables.rpy:500
translate schinese button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "imagebutton可以让你最大程度地控制按钮的外观，但是很难翻译，而且如果游戏窗口大小改变了，效果也不太好。"

# game/tutorial_screen_displayables.rpy:522
translate schinese button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "按钮使用窗口样式属性，用于指定背景、外边距和内边距。它们还使用特定的按钮属性，例如悬停时播放的音效。"

# game/tutorial_screen_displayables.rpy:524
translate schinese button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "与按钮一起使用时，样式属性可以加上像idle和hover之类的前缀，使属性随按钮状态而改变。"

# game/tutorial_screen_displayables.rpy:526
translate schinese button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "文本按钮也使用文本样式属性，只要加上text前缀。这些应用于它在内部创建的文本可视组件。"

# game/tutorial_screen_displayables.rpy:558
translate schinese button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "当然，我们很少在界面里定制按钮。相反，我们会创建自定义样式并让Ren'Py使用。"

# game/tutorial_screen_displayables.rpy:577
translate schinese bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "bar和vbar可视组件灵活地显示代表值的条。该值可以是静态的、动画的或由玩家调整的。"

# game/tutorial_screen_displayables.rpy:579
translate schinese bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "value属性提供BarValue，它是确定条的值和范围的对象。这里，StaticValue将范围设置为100、值为66，从而使条三分之二满。"

# game/tutorial_screen_displayables.rpy:581
translate schinese bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "所有可用Barvalue的列表见{a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}Ren'Py文档{/a}。（{a=https://renpy.cn/doc/screen_actions.html#bar}中文文档{/a}）"

# game/tutorial_screen_displayables.rpy:583
translate schinese bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "在本例中，我们给frame设定了xsize属性。如果我们不这样做，这个条会扩展以填充所有可用的水平空间。"

# game/tutorial_screen_displayables.rpy:600
translate schinese bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "默认GUI定义了几种不同的条样式。样式由样式特性选择，默认根据值选择。"

# game/tutorial_screen_displayables.rpy:602
translate schinese bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "顶部样式是“条（bar）”样式。它用来显示玩家无法调整的值，比如生命或进度条。"

# game/tutorial_screen_displayables.rpy:604
translate schinese bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "中间的样式是“滑块（slider）”值。它用于玩家想调整的值，例如音量首选项。"

# game/tutorial_screen_displayables.rpy:606
translate schinese bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "最后，底部样式是“滚动条（scrollbar）”样式，用于水平滚动条。当用作滚动条时，中间的小方块改变大小以反映视口的可见区域。"

# game/tutorial_screen_displayables.rpy:623
translate schinese bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "vbar可视组件与bar可视组件类似，不过它默认使用垂直样式如“vbar”、“vslider”和“vscrollbar”。"

# game/tutorial_screen_displayables.rpy:626
translate schinese bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "条使用条样式属性，可以对外观进行很大的定制。看看条、滑块和滚动条样式之间的区别就知道了。"

# game/tutorial_screen_displayables.rpy:635
translate schinese imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "图像映射（imagemap）使用两个或多个图像来显示按钮和栏。首先让我向您展示一个imagemap的实际应用示例。"

# game/tutorial_screen_displayables.rpy:657
translate schinese swimming_405542a5:

    # e "You chose swimming."
    e "你选了游泳。"

# game/tutorial_screen_displayables.rpy:659
translate schinese swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "游泳看起来很有趣，但我没有带泳衣。"

# game/tutorial_screen_displayables.rpy:665
translate schinese science_83e5c0cc:

    # e "You chose science."
    e "你选了科学。"

# game/tutorial_screen_displayables.rpy:667
translate schinese science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "我听说有些学校有一支很有竞争力的科学团队，但对我来说，研究是一件不能急于求成的事情。"

# game/tutorial_screen_displayables.rpy:672
translate schinese art_d2a94440:

    # e "You chose art."
    e "你选了艺术。"

# game/tutorial_screen_displayables.rpy:674
translate schinese art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "真正好的背景图很难创作，这就是为什么这么多游戏使用带滤镜的照片。也许你可以改变。"

# game/tutorial_screen_displayables.rpy:680
translate schinese home_373ea9a5:

    # e "You chose to go home."
    e "你选择回家。"

# game/tutorial_screen_displayables.rpy:686
translate schinese imagemap_done_48eca0a4:

    # e "Anyway..."
    e "好吧……"

# game/tutorial_screen_displayables.rpy:691
translate schinese imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "为了演示imagemap是如何组合在一起的，我将向您展示组成较小imagemap的五个图像。"

# game/tutorial_screen_displayables.rpy:697
translate schinese imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "idle图像用于imagemap的背景、未聚焦或未选中的热点按钮以及未聚焦条的空白部分。"

# game/tutorial_screen_displayables.rpy:703
translate schinese imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "hover图像用于聚集但未选中的热点以及聚焦条的空白部分。"

# game/tutorial_screen_displayables.rpy:705
translate schinese imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "注意此图中的条和按钮是如何高亮的。当我们将它们作为界面的一部分显示时，只有其中一个会显示为已聚焦。"

# game/tutorial_screen_displayables.rpy:711
translate schinese imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "selected图像，像这个selected_idle图像，用于条的填充部分，以及选中按钮如当前界面和勾选的选择框。"

# game/tutorial_screen_displayables.rpy:717
translate schinese imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "这有selected_hover图像。这里的按钮永远不会显示，因为它永远不会被标记为选中。"

# game/tutorial_screen_displayables.rpy:723
translate schinese imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "最后，可以给出一个insensitive图像，当热点不能交互时使用。"

# game/tutorial_screen_displayables.rpy:728
translate schinese imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "imagemap不限于图像。任何可视组件都可以在需要图像的地方使用。"

# game/tutorial_screen_displayables.rpy:743
translate schinese imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "这有用这五个图像构建的imagemap。现在它是imagemap，你可以与它交互。"

# game/tutorial_screen_displayables.rpy:755
translate schinese imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "为了更简洁一点，我们可以用auto属性替换这五个图像，它将视情况替换“%%s”为“idle”、“hover”、“selected_idle”、“selected_hover”或“insensitive”。"

# game/tutorial_screen_displayables.rpy:757
translate schinese imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "如果你的游戏不需要的话，你可以随意省略selected和insensitive图像。Ren'Py将使用idle或hover图像来替换它们。"

# game/tutorial_screen_displayables.rpy:759
translate schinese imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "hotspot和hotbar语句分别描述imagemap中应该充当按钮或条的区域。"

# game/tutorial_screen_displayables.rpy:761
translate schinese imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "两者都采用 (横坐标, 纵坐标, 宽度, 高度) 格式的区域坐标。"

# game/tutorial_screen_displayables.rpy:763
translate schinese imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "hotspot需要当热点激活时运行的动作。它也可以接受悬停和未发现时运行的动作，就像按钮一样。"

# game/tutorial_screen_displayables.rpy:765
translate schinese imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "hotbar接受一个BarValue对象，描述条的填充程度、应该显示的值的范围，就像bar和vbar一样。"

# game/tutorial_screen_displayables.rpy:772
translate schinese imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "一个有用的模式是用imagemap定义一个具有跳转到标签的热点的界面，并使用call screen语句调用它。"

# game/tutorial_screen_displayables.rpy:774
translate schinese imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "在我之前展示的学校例子中，我们就是这样做的。这是脚本。它很长，但imagemap本身相当简单。"

# game/tutorial_screen_displayables.rpy:778
translate schinese imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "imagemap有优点和缺点。一方面，它们对于设计师来说很容易创作，而且看起来非常好。同时，它们可能很难翻译，而且图像中的文本可能因缩放而变得模糊。"

# game/tutorial_screen_displayables.rpy:780
translate schinese imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "由您和您的团队来决定imagemap是否适合您的项目。"

# game/tutorial_screen_displayables.rpy:787
translate schinese viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "有时候，你会想显示比界面更大的东西。这就是视口（viewport）可视组件的用途。"

# game/tutorial_screen_displayables.rpy:803
translate schinese viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "下面是一个简单视口的示例，用于显示远大于界面的单个图像。由于视口会扩展到界面大小，因此我们使用xysize属性缩小它。"

# game/tutorial_screen_displayables.rpy:805
translate schinese viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "默认情况下，视口不能移动，因此我们提供了draggable、mouseweel和arrowkeys属性，从而允许以多种方式移动。"

# game/tutorial_screen_displayables.rpy:820
translate schinese viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "如果我给视口edgescroll属性，当鼠标靠近边缘时，视口会自动滚动。这两个数字是边缘的大小和滚动速度（像素/秒）。"

# game/tutorial_screen_displayables.rpy:839
translate schinese viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "给视口scrollbars属性，则视口被scrollbars包围。scrollbars属性可以将“both”、“horizontal”和“vertical”作为值。"

# game/tutorial_screen_displayables.rpy:841
translate schinese viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "spacing属性控制视口与滚动条之间的距离（单位：像素）。"

# game/tutorial_screen_displayables.rpy:864
translate schinese viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "xinitial和yinitial属性设置滚动的初始量，作为可滚动量的一小部分。"

# game/tutorial_screen_displayables.rpy:885
translate schinese viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "最后，还有child_size属性。为了解释它的作用，我首先要告诉你，没有它时会发生什么。"

# game/tutorial_screen_displayables.rpy:887
translate schinese viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "如您所见，文本换行。这是因为Ren'Py提供的空间不够大。"

# game/tutorial_screen_displayables.rpy:909
translate schinese viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "如果我们给界面一个child_size时，它就给子组件提供了更多的空间，允许滚动。它需要水平和垂直大小。如果一个组分为None，则使用视区的大小。"

# game/tutorial_screen_displayables.rpy:936
translate schinese viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "最后，还有vpgrid可视组件。它将一个视口和一个网格组合成一个可视组件，不过它比任一都更有效，因为它不必绘制每个子组件。"

# game/tutorial_screen_displayables.rpy:938
translate schinese viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "它接受cols和rows属性，分别给出提供子组件的列数和行数。如果其中一个省略了，Ren'Py会根据另一个以及子组件的数量计算出来。"

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
