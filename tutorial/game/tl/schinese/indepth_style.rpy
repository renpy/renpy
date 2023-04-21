
# game/indepth_style.rpy:40
translate schinese new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "创建新项目时，Ren'Py会自动为它创建一个图形用户界面（GUI）。"

# game/indepth_style.rpy:42
translate schinese new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "它定义了游戏内界面（像是这个文本框）和游戏外界面（如主菜单和游戏菜单）的外观。"

# game/indepth_style.rpy:44
translate schinese new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "默认的GUI对于一个简单的项目来说已经足够好了。加上一些小的改变，就是你在这个游戏中看到的。"

# game/indepth_style.rpy:46
translate schinese new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "GUI对中间创建者来说很容易定制。自定义GUI包括更改GUI目录中的图像文件，以及更改 gui.rpy 中的变量。"

# game/indepth_style.rpy:48
translate schinese new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "同时，即使是定制的，默认的GUI对于一个追求极致的游戏来说也太容易识别了。这就是为什么我们让它易于替换。"

# game/indepth_style.rpy:50
translate schinese new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "我们在Ren'Py网站上提供了一个关于定制GUI的拓展指南。因此，如果您想了解更多信息，请访问{a=https://www.renpy.org/doc/html/gui.html}GUI定制指南{/a}。（{a=https://renpy.cn/doc/gui.html}中文文档{/a}）"

# game/indepth_style.rpy:58
translate schinese styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayables look like."
    e "Ren'Py有一个强大的样式系统，可以控制可视组件的外观。"

# game/indepth_style.rpy:60
translate schinese styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "虽然默认的GUI使用变量为样式提供合理的默认值，但如果要替换GUI或创建自己的界面，则需要自己学习样式。"

# game/indepth_style.rpy:66
translate schinese styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "关于样式，你想了解什么？" nointeract

# game/indepth_style.rpy:98
translate schinese style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "样式让可视组件在不同的游戏、甚至同一个游戏内看起来不同。"

# game/indepth_style.rpy:103
translate schinese style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "这两个按钮使用相同的可视组件。但由于应用了不同的样式，按钮看起来彼此不同。"

# game/indepth_style.rpy:108
translate schinese style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "样式是来自四个不同地方的信息的组合。"

# game/indepth_style.rpy:121
translate schinese style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "Ren'Py首先可以从界面的一部分得到样式信息。由界面创建的每个可视组件都可以采用样式名和样式属性。"

# game/indepth_style.rpy:138
translate schinese style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "当界面可视组件包含文本时，以text_为前缀的样式属性可用于该文本。"

# game/indepth_style.rpy:151
translate schinese style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "下一个是作为在image语句中创建的可视组件的一部分。样式属性只是可视组件的参数。"

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

    # e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "最后是样式语句，它创建或更改命名样式。通过给Text指定样式参数，我们告诉它使用blue_text样式。"

# game/indepth_style.rpy:180
translate schinese style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "样式属性可以继承自父样式。如果样式属性没有在样式中指定，它就来自父样式。"

# game/indepth_style.rpy:182
translate schinese style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "默认情况下，父样式具有相同的名称，只是删除了第一个下划线之前的前缀。如果样式名中没有下划线，则使用“default”。"

# game/indepth_style.rpy:184
translate schinese style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "例如，blue_text继承自text，而text又继承自default。default样式定义了所有属性，因此它不继承任何内容。"

# game/indepth_style.rpy:190
translate schinese style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "通过给样式语句一个“is”从句，可以显式地更改父样式。在本例中，我们明确地将样式设置为text的父类。"

# game/indepth_style.rpy:194
translate schinese style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "每个可视组件都有一个默认样式名。默认情况下，它通常是小写的可视组件名，如Text的“text”，或按钮的“button”。"

# game/indepth_style.rpy:196
translate schinese style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "在界面中，可视组件的样式前缀（style_prefix）属性，赋予该可视组件及其子组件一个前缀。"

# game/indepth_style.rpy:198
translate schinese style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "例如，文本可视组件有着“help”的style_prefix，会被赋予样式“help_text”。"

# game/indepth_style.rpy:200
translate schinese style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "最后，当可视组件是按钮，或者在按钮内部时，它可以使用样式前缀。"

# game/indepth_style.rpy:202
translate schinese style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "当按钮未聚焦、聚焦和不可聚焦时，将使用前缀idle_、hover_和insensitive_。"

# game/indepth_style.rpy:204
translate schinese style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "前面可以加上selected_，以更改按钮外观，当展示选定的值或界面时。"

# game/indepth_style.rpy:233
translate schinese style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "此界面显示正在运行的样式前缀。您可以单击一个按钮来选择它，或者单击其他部分来前进。"

# game/indepth_style.rpy:240
translate schinese style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "这些是样式的基础。如果GUI定制还不够，样式可以让您定制Ren'Py中的几乎所有内容。"

# game/indepth_style.rpy:253
translate schinese style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "我们将讨论的第一组样式属性是常规样式属性。它们适用于许多不同的可视组件。"

# game/indepth_style.rpy:264
translate schinese style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "每个可视组件都有位置属性，这些属性控制它在界面上的位置。前面已经提到，我就不在这里重复了。"

# game/indepth_style.rpy:275
translate schinese style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "xmaximum和ymaximum属性分别设置可视组件的最大宽度和高度。可能，这会使Ren'Py缩小内容。"

# game/indepth_style.rpy:277
translate schinese style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "有时，缩小后大小将小于xmaximum和ymaximum给定的大小。"

# game/indepth_style.rpy:279
translate schinese style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "类似地，xminimum和yminimum属性设置最小宽度和高度。如果可视组件更小，Ren'Py会尝试放大。"

# game/indepth_style.rpy:289
translate schinese style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "xsize和ysize属性将最小和最大设置为相同的值，从而固定大小。"

# game/indepth_style.rpy:291
translate schinese style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "这些只适用于能调整大小可视组件。有些可视组件，比如图像，不能放大或缩小。"

# game/indepth_style.rpy:299
translate schinese style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "area属性接受一个元组——以圆括号为界的四项列表。前两个给出位置，后两个给出大小。"

# game/indepth_style.rpy:308
translate schinese style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "最后，alt属性改变给听障者的自动语音文本。"

# game/indepth_style.rpy:335
translate schinese style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "文本样式属性应用于文本和输入可视组件。"

# game/indepth_style.rpy:337
translate schinese style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "Text可视组件可以隐式或显式创建。例如，textbutton创建的文本可视组件，其样式以button_text结尾。"

# game/indepth_style.rpy:339
translate schinese style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "也可以在 gui.rpy 中通过更改或定义变量，如gui.button_text_size，来设置这些值。"

# game/indepth_style.rpy:347
translate schinese style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "bold样式属性使文本变粗体。这可以使用算法来完成，而不是使用不同版本的字体。"

# game/indepth_style.rpy:355
translate schinese style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "color属性更改文本的颜色。它需要十六进制的颜色代码，就像Ren'Py的其他东西一样。"

# game/indepth_style.rpy:363
translate schinese style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "first_indent样式属性确定第一行缩进的距离。"

# game/indepth_style.rpy:371
translate schinese style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "font样式属性更改文本使用的字体。Ren'Py采用TrueType和OpenType字体，您必须将字体文件放进视觉小说。"

# game/indepth_style.rpy:379
translate schinese style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "size属性更改文本的大小。"

# game/indepth_style.rpy:388
translate schinese style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "italic属性使文本变为斜体。同样，用字体做这个更好，但是对于短文本，Ren'Py也可以。"

# game/indepth_style.rpy:397
translate schinese style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "justify属性使文本对齐，将除最后一行外的所有行在左侧和右侧对齐。"

# game/indepth_style.rpy:405
translate schinese style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "kerning属性调整文本间距。当它是负数时，字符之间的距离更近。当为正时，字符之间的距离更大。"

# game/indepth_style.rpy:415
translate schinese style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "line_leading和line_spacing属性分别每行缩进和行距。"

# game/indepth_style.rpy:424
translate schinese style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "outlines属性在文本周围放置轮廓。这需要一个元组列表，这有点复杂。"

# game/indepth_style.rpy:426
translate schinese style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "但如果忽略所有括号，就是轮廓的宽度、颜色，以及水平和垂直偏移。"

# game/indepth_style.rpy:434
translate schinese style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "rest_indent属性控制首行之外的缩进。"

# game/indepth_style.rpy:443
translate schinese style_text_430c1959:

    # e "The textalign property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "textalign属性控制文本可视组件中多行文本的位置。例如，0.5表示居中。"

# game/indepth_style.rpy:445
translate schinese style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the textalign and xalign to the same value."
    e "它不会改变文本可视组件本身的位置。为此，通常需要将textalign和xalign设置为相同的值。"

# game/indepth_style.rpy:455
translate schinese style_text_efc3c392:

    # e "When both textalign and xalign are set to 1.0, the text is properly right-justified."
    e "当textalign和xalign都设置为1.0时，文本将正确右对齐。"

# game/indepth_style.rpy:464
translate schinese style_text_43be63b9:

    # e "The underline property underlines the text."
    e "underline属性为文本加下划线。"

# game/indepth_style.rpy:471
translate schinese style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "这些是最常见的文本样式属性，但不是全部。这里还有一些在特殊情况下你可能需要的。"

# game/indepth_style.rpy:479
translate schinese style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "默认情况下，Ren'Py中的文本是抗锯齿的，以平滑边缘。antialias属性可以将其关闭，并使文本稍微锯齿化。"

# game/indepth_style.rpy:487
translate schinese style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "adjust_spacing属性非常微妙，它只在玩家调整窗口大小时才起作用。如果为True，字符将移动一点，使文本具有相同的相对间距。"

# game/indepth_style.rpy:496
translate schinese style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "如果为False，则文本不会跳来跳去。但根据界面大小，它可以更宽或更窄一些。"

# game/indepth_style.rpy:505
translate schinese style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "layout属性有一些特殊值，用于控制换行的位置。“nobreak”值完全禁用换行符，使文本变宽。"

# game/indepth_style.rpy:516
translate schinese style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "当layout属性设置为“subtitle”时，断行算法将被更改，以尝试使所有行的长度均匀，因为字幕通常是这样的。"

# game/indepth_style.rpy:524
translate schinese style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "删除线属性在文本中绘制一条线。你似乎不太可能用这个。"

# game/indepth_style.rpy:534
translate schinese style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "vertical属性将文本放置在垂直布局中。用于亚洲语言的特殊字体。"

# game/indepth_style.rpy:540
translate schinese style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "这些都是文本样式属性。可能有点多，但我们想让你自由地将文本呈现给玩家。"

# game/indepth_style.rpy:580
translate schinese style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "接下来是窗口和按钮样式的属性。这些应用于窗口像是当前界面底部的文本框，以及框架像是示例中那样。"

# game/indepth_style.rpy:582
translate schinese style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "这些属性也适用于游戏内和游戏外的按钮。对Ren'Py来说，按钮是一个可以点击的窗口。"

# game/indepth_style.rpy:593
translate schinese style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "我将从这种样式开始，一切继承于此。为了让我们更轻松，它继承了默认样式，而不是这个游戏的GUI中的自定义按钮。"

# game/indepth_style.rpy:595
translate schinese style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "第一个样式属性是background。它为按钮或窗口添加背景。由于这是一个按钮，指针空闲和悬停时选择不同的背景。"

# game/indepth_style.rpy:597
translate schinese style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "我们还使用xalign位置属性将两个按钮居中。"

# game/indepth_style.rpy:601
translate schinese style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "我们还使用这种样式定制了按钮文本的样式。它使文本居中，并在指针指向时改变颜色。"

# game/indepth_style.rpy:612
translate schinese style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "文本周围没有任何填充，按钮看起来很奇怪。Ren'Py有内边距属性，可以在按钮的背景内部添加间距。"

# game/indepth_style.rpy:621
translate schinese style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "更常用的是xpadding和ypadding样式属性，它们分别在左侧和右侧、顶部和底部添加相同的填充。"

# game/indepth_style.rpy:629
translate schinese style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "外边距样式属性的工作方式相同，除了在背景之外增加间距。全套包括：left_margin、right_margin、top_margin、bottom_margin、xmargin和ymargin。"

# game/indepth_style.rpy:638
translate schinese style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "size_group样式属性采用字符串。Ren'Py将确保具有相同size_group的所有窗口或按钮的大小相同。"

# game/indepth_style.rpy:647
translate schinese style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "或者，xfill和yfill样式属性使按钮占据水平或垂直方向上的所有可用空间。"

# game/indepth_style.rpy:657
translate schinese style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "foreground属性使可视组件位于窗口或按钮的内容和背景之上。"

# game/indepth_style.rpy:659
translate schinese style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "使用它的一种方法是为复选框按钮提供额外的装饰。另一种方法是将其与Frame一起使用，以提供覆盖按钮内容的光泽。"

# game/indepth_style.rpy:668
translate schinese style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "还有一些样式特性仅适用于按钮。hover_sound和activate_sound属性分别在按钮聚焦和激活时播放声音文件。"

# game/indepth_style.rpy:677
translate schinese style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "最后，focus_mask属性应用于部分透明的按钮。当设置为True时，只有按钮上不透明的区域才会使按钮聚焦。"

# game/indepth_style.rpy:757
translate schinese style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "为了演示样式，让我首先展示两个我们将使用的图像。这是我们在bar空着的地方使用的图像。"

# game/indepth_style.rpy:761
translate schinese style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "这是我们用在bar满的部分的。"

# game/indepth_style.rpy:773
translate schinese style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "left_bar和riht_bar样式属性，以及鼠标指向时使用的变体，给bar的左侧和右侧提供可视组件。默认该值显示在左侧。"

# game/indepth_style.rpy:775
translate schinese style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "此外，默认情况下，左右可视组件在bar的全宽上渲染，然后剪切为适当的大小。"

# game/indepth_style.rpy:777
translate schinese style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "我们给bar设置ysize属性来设置它的高度。我们也可以给它xsize来选择宽度，但这里它受所在框的宽度限制。"

# game/indepth_style.rpy:790
translate schinese style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "当bar_invert属性为True时，bar的值将显示在右侧。left_bar和right_bar可视组件也可能需要交换。"

# game/indepth_style.rpy:804
translate schinese style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "bar_resizing样式属性使bar图像的大小调整为对应的值，而不是全尺寸渲染后裁剪。"

# game/indepth_style.rpy:817
translate schinese style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "thumb样式属性提供一个缩略图，基于bar值。对于进度条，如果可能，大小会调整。"

# game/indepth_style.rpy:819
translate schinese style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "在这里，我们将其与base_bar样式属性一起使用，从而将两个bar图像设置为相同的可视组件。"

# game/indepth_style.rpy:834
translate schinese style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "left_gutter和right_gutter属性在bar的左侧或右侧大小上设置一个gutter。gutter是bar不能拖进去的空间，可以用于边界。"

# game/indepth_style.rpy:849
translate schinese style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "bar_vertical样式属性显示垂直方向的bar。所有其他属性都会更改名称——left_bar变为top_bar，right_bar变为bottom_bar。"

# game/indepth_style.rpy:854
translate schinese style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "最后，有一种样式我们无法在这里展示，它是unscrollable。它控制当进度条完全不能移动时发生的事情。"

# game/indepth_style.rpy:856
translate schinese style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "默认显示。但如果unscrollable是“insensitive”的，那么bar就会变得不敏感。如果是“hide”，则bar是隐藏的，但仍占用空间。"

# game/indepth_style.rpy:860
translate schinese style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "这是bar的属性。通过使用它们，创作者可以定制条、滚动条和滑块。"

# game/indepth_style.rpy:959
translate schinese style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "hbox可视组件用于水平放置其子组件。默认子组件之间没有间隔，因此它们一起运行。"

# game/indepth_style.rpy:965
translate schinese style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "类似地，vbox可视组件用于垂直布局其子组件。两者都支持控制放置的样式特性。"

# game/indepth_style.rpy:970
translate schinese style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "为了使box可视组件的大小显示，我将高亮box本身，而不是包含它的框架。"

# game/indepth_style.rpy:978
translate schinese style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "box支持xfill和yfill样式属性。这些属性使box拉伸以填充可用空间，而不是最大子组件的空间。"

# game/indepth_style.rpy:988
translate schinese style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "spacing样式属性以像素为单位获取值，并在box的每个子组件之间添加这么大的间距。"

# game/indepth_style.rpy:998
translate schinese style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "first_spacing样式属性类似，但它只在第一个子组件和第二个之间添加间距。当第一个子组件是标题，需要不同的间距时，这很有用。"

# game/indepth_style.rpy:1008
translate schinese style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "box_reverse样式属性反转框中条目的顺序。"

# game/indepth_style.rpy:1021
translate schinese style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "我们将在下一个示例中换回水平box。"

# game/indepth_style.rpy:1031
translate schinese style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "box_wrap样式属性用子组件填充box，直到填满，然后在下一行重新开始。"

# game/indepth_style.rpy:1044
translate schinese style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "Grid还带来两个样式特性。xspacing和yspacing属性分别控制水平和垂直方向的间距。"

# game/indepth_style.rpy:1051
translate schinese style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "最后，我们有固定的布局。固定布局通常扩展以填满所有空间，并从后到前显示其子组件。"

# game/indepth_style.rpy:1053
translate schinese style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "当然，我们有一些样式属性可以改变这种情况。"

# game/indepth_style.rpy:1062
translate schinese style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "当xfit样式属性为True时，fixed会所有子组件以全尺寸平铺，然后缩小宽度以适合它们。yfit样式以同样的方式作用在高度上。"

# game/indepth_style.rpy:1070
translate schinese style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "order_reverse样式属性更改子组件的显示顺序。不再是从后向前，而是从前到后。"

# game/indepth_style.rpy:1082
translate schinese style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "有时很难弄清楚某个特定的可视组件使用了什么样式。可视组件检查器可以帮助实现这一点。"

# game/indepth_style.rpy:1084
translate schinese style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "要使用它，请将鼠标放在Ren'Py用户界面的一部分上，然后按 shift+I 。检查器中按 I 。"

# game/indepth_style.rpy:1086
translate schinese style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "Ren'Py会在鼠标指向的位置弹出可视组件列表，每一项可视组件使用的样式的名称。"

# game/indepth_style.rpy:1088
translate schinese style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "您可以单击样式名以查看其属性的来源。"

# game/indepth_style.rpy:1090
translate schinese style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "默认情况下，检查器只显示界面元素（如界面），而不显示图像。如果您还想查看图像，请按下 shift+alt+I 。"

# game/indepth_style.rpy:1092
translate schinese style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "你现在就可以尝试检查器，将鼠标悬停在这段文字上并按下 shift+I 。"

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
    new "当我乘坐飞船在地球轨道上运行时,我为地球的美丽而惊奇。\n——尤里·加加林"

    # game/indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "“当我乘坐飞船在地球轨道上运行时,我为地球的美丽而惊奇。”尤里·加加林说。"

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
