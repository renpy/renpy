
# game/indepth_style.rpy:40
translate schinese new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "创建新项目时，Ren'Py 会自动为项目创建 GUI（图形用户界面）。"

# game/indepth_style.rpy:42
translate schinese new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "它定义游戏内界面（例如这个文本框）以及游戏外界面（例如主菜单和游戏菜单）的外观。"

# game/indepth_style.rpy:44
translate schinese new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "默认 GUI 对简单项目来说已经足够美观。稍作修改，就能得到你在这个游戏中看到的效果。"

# game/indepth_style.rpy:46
translate schinese new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "默认 GUI 也方便有一定经验的创作者定制。定制 GUI 包括修改 gui 目录中的图像文件，以及修改 gui.rpy 中的变量。"

# game/indepth_style.rpy:48
translate schinese new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "不过，即使经过定制，默认 GUI 对于追求高度打磨的游戏来说仍可能过于容易辨认。因此，我们让它可以被完全替换。"

# game/indepth_style.rpy:50
translate schinese new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "我们在 Ren'Py 网站上提供了详尽的 GUI 定制指南。想进一步了解，请参阅{a=https://www.renpy.org/doc/html/gui.html}GUI 定制指南{/a}。"

# game/indepth_style.rpy:58
translate schinese styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayables look like."
    e "Ren'Py 拥有强大的样式系统，用来控制显示对象的外观。"

# game/indepth_style.rpy:60
translate schinese styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "默认 GUI 使用变量为样式提供合理的默认值；如果要替换 GUI 或创建自己的屏幕，就需要自己了解样式。"

# game/indepth_style.rpy:66
translate schinese styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "你想了解样式的哪一方面？" nointeract

# game/indepth_style.rpy:98
translate schinese style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "样式可以让显示对象在不同游戏中，甚至在同一个游戏的不同位置呈现不同外观。"

# game/indepth_style.rpy:103
translate schinese style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "这两个按钮使用相同的显示对象，但应用了不同样式，所以外观各不相同。"

# game/indepth_style.rpy:108
translate schinese style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "样式由来自四个不同地方的信息组合而成。"

# game/indepth_style.rpy:121
translate schinese style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "Ren'Py 获取样式信息的第一个地方是屏幕的一部分。屏幕创建的每个显示对象都可以指定样式名称和样式属性。"

# game/indepth_style.rpy:138
translate schinese style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "屏幕显示对象包含文本时，以 text_ 开头的样式属性会应用于该文本。"

# game/indepth_style.rpy:151
translate schinese style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "第二个地方是 image 语句中创建的显示对象。样式属性就是传给显示对象的参数。"

# game/indepth_style.rpy:160
translate schinese style_basics_ccc0d1ca:

    # egreen "Style properties can also be given as arguments when defining a character."
    egreen "定义人物时，样式属性也可以作为参数。"

# game/indepth_style.rpy:162
translate schinese style_basics_013ab314:

    # egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."
    egreen "以who_开头的参数是应用于人物名的样式属性，而以what_开头的参数则应用于人物的对话。"

# game/indepth_style.rpy:164
translate schinese style_basics_dbe80939:

    # egreen "Style properties that don't have a prefix are also applied to the character's name."
    egreen "没有前缀的样式特性也应用于人物的名字。"

# game/indepth_style.rpy:174
translate schinese style_basics_ac6a8414:

    # e "Finally, there is the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "最后是 style 语句，它会创建或修改命名样式。给 Text 指定 style 参数，就会让它使用 blue_text 样式。"

# game/indepth_style.rpy:180
translate schinese style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "样式属性可以继承自父样式。如果某个样式没有指定属性，就会从它的父样式继承。"

# game/indepth_style.rpy:182
translate schinese style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "默认情况下，父样式名称与当前样式相同，但会去掉第一个下划线之前的前缀。如果样式名中没有下划线，就使用 default。"

# game/indepth_style.rpy:184
translate schinese style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "例如，blue_text 继承自 text，而 text 又继承自 default。default 样式定义了所有属性，因此不继承任何样式。"

# game/indepth_style.rpy:190
translate schinese style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "给 style 语句添加 is 子句可以显式更改父样式。这里，我们明确把样式的父样式设为 text 的父样式。"

# game/indepth_style.rpy:194
translate schinese style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "每个显示对象都有默认样式名。通常是显示对象名称的小写形式，例如 Text 使用 text，按钮使用 button。"

# game/indepth_style.rpy:196
translate schinese style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "在屏幕中，可以给显示对象设置 style_prefix 属性，为该显示对象及其子对象提供样式前缀。"

# game/indepth_style.rpy:198
translate schinese style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "例如，style_prefix 为 help 的文本显示对象会使用 help_text 样式。"

# game/indepth_style.rpy:200
translate schinese style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "最后，如果显示对象本身是按钮或位于按钮内部，它还可以使用样式前缀。"

# game/indepth_style.rpy:202
translate schinese style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "按钮未获得焦点、获得焦点和不可用时，分别使用 idle_、hover_ 和 insensitive_ 前缀。"

# game/indepth_style.rpy:204
translate schinese style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "这些前缀前面还可以加 selected_，改变按钮表示选定值或屏幕时的外观。"

# game/indepth_style.rpy:233
translate schinese style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "这个屏幕展示了样式前缀的实际效果。点击按钮可以选中它，点击外部则继续。"

# game/indepth_style.rpy:240
translate schinese style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "这就是样式的基础。如果 GUI 定制仍然不够，样式几乎可以定制 Ren'Py 中的一切。"

# game/indepth_style.rpy:253
translate schinese style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "接下来介绍第一组样式属性：通用样式属性。它们适用于每个显示对象，至少适用于许多显示对象。"

# game/indepth_style.rpy:264
translate schinese style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "每个显示对象都接受位置属性，用来控制它在屏幕上的位置。前面已经介绍过，这里不再重复。"

# game/indepth_style.rpy:275
translate schinese style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "xmaximum 和 ymaximum 属性分别设置显示对象的最大宽度和最大高度；如果可能，Ren'Py 会据此缩小内容。"

# game/indepth_style.rpy:277
translate schinese style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "有时，缩小后的尺寸会小于 xmaximum 和 ymaximum 指定的尺寸。"

# game/indepth_style.rpy:279
translate schinese style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "同样，xminimum 和 yminimum 属性设置最小宽度和最小高度。如果显示对象太小，Ren'Py 会尝试将它放大。"

# game/indepth_style.rpy:289
translate schinese style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "xsize 和 ysize 属性把最小尺寸和最大尺寸设为同一个值，从而固定尺寸。"

# game/indepth_style.rpy:291
translate schinese style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "这些属性只对可以调整大小的显示对象有效。有些显示对象（例如图像）无法放大或缩小。"

# game/indepth_style.rpy:299
translate schinese style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "area 属性接收一个元组，也就是用圆括号括起来的四项列表。前两项表示位置，后两项表示尺寸。"

# game/indepth_style.rpy:308
translate schinese style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "最后，alt 属性会改变自动朗读为听障用户使用的文本。"

# game/indepth_style.rpy:335
translate schinese style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "文本样式属性适用于 text 和 input 显示对象。"

# game/indepth_style.rpy:337
translate schinese style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "文本显示对象可以隐式或显式创建。例如，textbutton 会创建一个样式名以 button_text 结尾的文本显示对象。"

# game/indepth_style.rpy:339
translate schinese style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "也可以在 gui.rpy 中修改或定义名称类似 gui.button_text_size 的变量来设置这些属性。"

# game/indepth_style.rpy:347
translate schinese style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "bold 样式属性会让文本变粗。它可以通过算法实现，不一定需要另一套字体。"

# game/indepth_style.rpy:355
translate schinese style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "color 属性改变文本颜色。它接收十六进制颜色代码，与 Ren'Py 的其他部分相同。"

# game/indepth_style.rpy:363
translate schinese style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "first_indent 样式属性决定第一行缩进多少。"

# game/indepth_style.rpy:371
translate schinese style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "font 样式属性改变文本使用的字体。Ren'Py 支持 TrueType 和 OpenType 字体，你需要把字体文件作为视觉小说的一部分提供。"

# game/indepth_style.rpy:379
translate schinese style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "size 属性改变文本大小。"

# game/indepth_style.rpy:388
translate schinese style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "italic 属性让文本变成斜体。同样，使用字体通常效果更好，但短文本可以交给 Ren'Py 处理。"

# game/indepth_style.rpy:397
translate schinese style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "justify 属性让文本两端对齐，使除最后一行以外的各行同时贴齐左右边缘。"

# game/indepth_style.rpy:405
translate schinese style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "kerning 属性调整字距。值为负时字符更靠近，值为正时字符间距更大。"

# game/indepth_style.rpy:415
translate schinese style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "line_leading 和 line_spacing 属性分别设置每行之前以及各行之间的间距。"

# game/indepth_style.rpy:424
translate schinese style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "outlines 属性在文本周围绘制轮廓。它接收元组列表，写法稍微复杂一些。"

# game/indepth_style.rpy:426
translate schinese style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "忽略方括号和圆括号后，可以看到其中依次是轮廓宽度、颜色，以及水平和垂直偏移量。"

# game/indepth_style.rpy:434
translate schinese style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "rest_indent 属性控制第一行之后各行的缩进。"

# game/indepth_style.rpy:443
translate schinese style_text_430c1959:

    # e "The textalign property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "textalign 属性控制文本显示对象内部多行文本的位置。例如，0.5 表示居中。"

# game/indepth_style.rpy:445
translate schinese style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the textalign and xalign to the same value."
    e "它不会改变文本显示对象本身的位置。要改变对象位置，通常需要把 textalign 和 xalign 设为相同值。"

# game/indepth_style.rpy:455
translate schinese style_text_efc3c392:

    # e "When both textalign and xalign are set to 1.0, the text is properly right-justified."
    e "当 textalign 和 xalign 都设为 1.0 时，文本就会正确地右对齐。"

# game/indepth_style.rpy:464
translate schinese style_text_43be63b9:

    # e "The underline property underlines the text."
    e "underline 属性为文本添加下划线。"

# game/indepth_style.rpy:471
translate schinese style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "这些是最常见的文本样式属性，但并不是全部。下面再介绍一些特殊情况下可能需要的属性。"

# game/indepth_style.rpy:479
translate schinese style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "默认情况下，Ren'Py 中的文本会启用抗锯齿，让边缘更平滑。antialias 属性可以关闭抗锯齿，让文字边缘更生硬。"

# game/indepth_style.rpy:487
translate schinese style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "adjust_spacing 属性很细微，只有玩家调整窗口大小时才会产生影响。设为 True 时，字符会略微移动，使 Text 保持相同的相对间距。"

# game/indepth_style.rpy:496
translate schinese style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "设为 False 时，文本不会跳动得那么明显，但宽度可能会随屏幕尺寸略有变化。"

# game/indepth_style.rpy:505
translate schinese style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "layout 属性有几个特殊值，用于控制换行位置。nobreak 会完全禁用换行，使文本变得更宽。"

# game/indepth_style.rpy:516
translate schinese style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "layout 设为 subtitle 时，会改变换行算法，尽量让每行长度接近字幕的通常效果。"

# game/indepth_style.rpy:524
translate schinese style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "strikethrough 属性在文本中间画线。一般不太会需要使用它。"

# game/indepth_style.rpy:534
translate schinese style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "vertical 样式属性会以竖排方式放置文本，主要用于使用特殊字体的亚洲语言。"

# game/indepth_style.rpy:540
translate schinese style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "这些就是文本样式属性。属性可能很多，但我们希望让你能够充分控制向玩家呈现文本的方式。"

# game/indepth_style.rpy:580
translate schinese style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "接下来是 window 和 button 样式属性。它们适用于屏幕底部的文本窗口，以及示例中使用的 frame 等窗口。"

# game/indepth_style.rpy:582
translate schinese style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "这些属性也适用于游戏内外的按钮。对 Ren'Py 来说，按钮就是一个可以点击的窗口。"

# game/indepth_style.rpy:593
translate schinese style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "先从这个样式开始，其他内容都会继承它。为了简化设置，它继承 default 样式，而不是这个游戏 GUI 中用于定制按钮的样式。"

# game/indepth_style.rpy:595
translate schinese style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "第一个样式属性是 background。它为按钮或窗口添加背景。这里是按钮，因此 idle 和 hover 变体会在获得焦点时选择不同背景。"

# game/indepth_style.rpy:597
translate schinese style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "我们还使用 xalign 位置属性让两个按钮居中。"

# game/indepth_style.rpy:601
translate schinese style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "我们也用这个样式定制按钮文本的样式，让文本居中，并在悬停时改变颜色。"

# game/indepth_style.rpy:612
translate schinese style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "文本周围没有内边距时，按钮看起来会很奇怪。Ren'Py 提供 padding 属性，为按钮背景内部增加空间。"

# game/indepth_style.rpy:621
translate schinese style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "更常用的是 xpadding 和 ypadding 样式属性，它们分别在左右两侧，或上下两侧添加相同的内边距。"

# game/indepth_style.rpy:629
translate schinese style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "margin 样式属性的工作方式类似，但它们在背景外部添加空间。完整的属性包括 left_margin、right_margin、top_margin、bottom_margin、xmargin 和 ymargin。"

# game/indepth_style.rpy:638
translate schinese style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "size_group 样式属性接收一个字符串。Ren'Py 会让所有使用相同 size_group 字符串的窗口或按钮保持相同大小。"

# game/indepth_style.rpy:647
translate schinese style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "另一种方式是使用 xfill 和 yfill 样式属性，让按钮在水平方向或垂直方向占满所有可用空间。"

# game/indepth_style.rpy:657
translate schinese style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "foreground 属性提供一个显示对象，将它放在窗口或按钮的内容和背景之上。"

# game/indepth_style.rpy:659
translate schinese style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "一种用法是给作为复选框的按钮添加额外装饰。另一种用法是配合 Frame，覆盖按钮内容并提供光泽效果。"

# game/indepth_style.rpy:668
translate schinese style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "还有一些只适用于按钮的样式属性。按钮获得焦点和激活时，hover_sound 和 activate_sound 属性分别播放声音文件。"

# game/indepth_style.rpy:677
translate schinese style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "最后，focus_mask 属性适用于部分透明的按钮。设为 True 时，只有按钮中不透明的区域会让按钮获得焦点。"

# game/indepth_style.rpy:757
translate schinese style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "为了演示样式，先看看要使用的两张图像。这是用作数值条空白部分的图像。"

# game/indepth_style.rpy:761
translate schinese style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "这是用作数值条填充部分的图像。"

# game/indepth_style.rpy:773
translate schinese style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "left_bar 和 right_bar 样式属性及其 hover 变体，分别提供数值条左侧和右侧的显示对象。默认情况下，数值显示在左侧。"

# game/indepth_style.rpy:775
translate schinese style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "同样默认情况下，左右显示对象都会以数值条的完整宽度渲染，然后裁剪到合适的尺寸。"

# game/indepth_style.rpy:777
translate schinese style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "我们给数值条设置 ysize 属性来指定高度。也可以设置 xsize 指定宽度，但这里的宽度受所在 frame 的宽度限制。"

# game/indepth_style.rpy:790
translate schinese style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "bar_invert 样式属性为 True 时，数值会显示在数值条右侧。此时可能还需要交换 left_bar 和 right_bar 显示对象。"

# game/indepth_style.rpy:804
translate schinese style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "bar_resizing 样式属性会调整数值条图像的大小来表示数值，而不是按完整尺寸渲染后再裁剪。"

# game/indepth_style.rpy:817
translate schinese style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "thumb 样式属性提供一个滑块图像，其位置由数值条的值决定。用于滚动条时，如果可能还会调整滑块大小。"

# game/indepth_style.rpy:819
translate schinese style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "这里将它与 base_bar 样式属性一起使用，base_bar 会让两张数值条图像使用同一个显示对象。"

# game/indepth_style.rpy:834
translate schinese style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "left_gutter 和 right_gutter 属性分别在数值条左侧或右侧设置不可拖动的边距。这个边距可以用来放置边框。"

# game/indepth_style.rpy:849
translate schinese style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "bar_vertical 样式属性显示垂直方向的数值条。其他属性也会改名：left_bar 变为 top_bar，right_bar 变为 bottom_bar。"

# game/indepth_style.rpy:854
translate schinese style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "最后还有一个这里无法演示的样式：unscrollable。它控制滚动条完全无法移动时的行为。"

# game/indepth_style.rpy:856
translate schinese style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "默认情况下会显示滚动条。但 unscrollable 设为 insensitive 时，数值条会变为不可用；设为 hide 时，数值条会隐藏，但仍占用空间。"

# game/indepth_style.rpy:860
translate schinese style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "数值条属性就介绍到这里。利用这些属性，创作者可以定制数值条、滚动条和滑块。"

# game/indepth_style.rpy:959
translate schinese style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "hbox 显示对象用于水平排列子对象。默认情况下，子对象之间没有间距，因此会连在一起。"

# game/indepth_style.rpy:965
translate schinese style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "类似地，vbox 显示对象用于垂直排列子对象。两者都支持控制位置的样式属性。"

# game/indepth_style.rpy:970
translate schinese style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "为了清楚展示 box 显示对象的大小，我会给 box 本身添加高亮，而不是给包含它的 frame 添加高亮。"

# game/indepth_style.rpy:978
translate schinese style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "box 支持 xfill 和 yfill 样式属性。这些属性会让 box 扩展到填满可用空间，而不是只占用最大子对象的大小。"

# game/indepth_style.rpy:988
translate schinese style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "spacing 样式属性接收像素值，在 box 的每个子对象之间加入相应的间距。"

# game/indepth_style.rpy:998
translate schinese style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "first_spacing 样式属性类似，但只在第一个和第二个子对象之间添加间距。当第一个子对象是需要特殊间距的标题时，这很有用。"

# game/indepth_style.rpy:1008
translate schinese style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "box_reverse 样式属性会反转 box 中条目的顺序。"

# game/indepth_style.rpy:1021
translate schinese style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "下一个例子我们会切换回水平 box。"

# game/indepth_style.rpy:1031
translate schinese style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "box_wrap 样式属性会不断向 box 中填充子对象，填满后就在下一行继续。"

# game/indepth_style.rpy:1044
translate schinese style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "grid 还带有两个样式属性。xspacing 和 yspacing 分别控制水平方向和垂直方向的间距。"

# game/indepth_style.rpy:1051
translate schinese style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "最后是 fixed 布局。fixed 通常会扩展到填满所有空间，并按从后到前的顺序显示子对象。"

# game/indepth_style.rpy:1053
translate schinese style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "当然，也有一些样式属性可以改变这种行为。"

# game/indepth_style.rpy:1062
translate schinese style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "xfit 样式属性为 True 时，fixed 会按完整尺寸排布所有子对象，然后缩小宽度以适应它们。yfit 的工作方式相同，但作用于高度。"

# game/indepth_style.rpy:1070
translate schinese style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "order_reverse 样式属性会改变显示子对象的顺序。它们不再从后到前显示，而是从前到后显示。"

# game/indepth_style.rpy:1082
translate schinese style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "有时很难判断某个显示对象使用了什么样式。显示对象检查器可以提供帮助。"

# game/indepth_style.rpy:1084
translate schinese style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "要使用检查器，把鼠标移到 Ren'Py 用户界面的一部分上，然后按 Shift+I。这里的 I 指 inspector（检查器）。"

# game/indepth_style.rpy:1086
translate schinese style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "Ren'Py 会弹出鼠标所在位置的显示对象列表。每个显示对象旁边都会显示它使用的样式名称。"

# game/indepth_style.rpy:1088
translate schinese style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "点击样式名称，可以查看它从哪里继承属性。"

# game/indepth_style.rpy:1090
translate schinese style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "默认情况下，检查器只显示屏幕等界面元素，不显示图像。想同时查看图像，请按 Shift+Alt+I。"

# game/indepth_style.rpy:1092
translate schinese style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "现在就可以把鼠标移到这段文字上并按 Shift+I，试试检查器。"

translate schinese strings:

    # game/indepth_style.rpy:20
    old "Button 1"
    new "Button 1"

    # game/indepth_style.rpy:22
    old "Button 2"
    new "Button 2"

    # game/indepth_style.rpy:66
    old "Style basics."
    new "样式基础。"

    # game/indepth_style.rpy:66
    old "General style properties."
    new "常规样式属性。"

    # game/indepth_style.rpy:66
    old "Text style properties."
    new "Text样式属性。"

    # game/indepth_style.rpy:66
    old "Window and Button style properties."
    new "window和button样式属性。"

    # game/indepth_style.rpy:66
    old "Bar style properties."
    new "bar样式属性。"

    # game/indepth_style.rpy:66
    old "Box, Grid, and Fixed style properties."
    new "box、grid和fixed样式属性。"

    # game/indepth_style.rpy:66
    old "The Displayable Inspector."
    new "可视组件检查器。"

    # game/indepth_style.rpy:66
    old "That's all I want to know."
    new "我只想知道这些。"

    # game/indepth_style.rpy:112
    old "This text is colored green."
    new "这段文字是绿色的。"

    # game/indepth_style.rpy:126
    old "Danger"
    new "危险"

    # game/indepth_style.rpy:142
    old "This text is colored red."
    new "这段文字是红色的。"

    # game/indepth_style.rpy:170
    old "This text is colored blue."
    new "这段文字是蓝色的。"

    # game/indepth_style.rpy:248
    old "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"
    new "在飞船中环绕地球时，我看到了我们星球的美丽。\n——尤里·加加林"

    # game/indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "\"在飞船中环绕地球时，我看到了我们星球的美丽。\"——尤里·加加林"

    # game/indepth_style.rpy:326
    old "Vertical"
    new "垂直"

    # game/indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "敢于做伟大的事情，赢得光荣的胜利，尽管会遭受挫败，也比那些精神贫乏的人强得多，他们既不会享受生活，也不会吃太多苦头，因为他们生活在不知胜利和失败的混沌时节。\n\n——西奥多·罗斯福"

    # game/indepth_style.rpy:561
    old "Top Choice"
    new "顶部选择"

    # game/indepth_style.rpy:566
    old "Bottom Choice"
    new "底部选择"

    # game/indepth_style.rpy:877
    old "First Child"
    new "第一个子组件"

    # game/indepth_style.rpy:878
    old "Second Child"
    new "第二个子组件"

    # game/indepth_style.rpy:879
    old "Third Child"
    new "第三个子组件"

    # game/indepth_style.rpy:882
    old "Fourth Child"
    new "第四个子组件"

    # game/indepth_style.rpy:883
    old "Fifth Child"
    new "第五个子组件"

    # game/indepth_style.rpy:884
    old "Sixth Child"
    new "第六个子组件"
