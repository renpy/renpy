
# game/indepth_character.rpy:11
translate schinese demo_character_e7e1b1bb:

    # e "We've already seen how to define a Character in Ren'Py. But I want to go into a bit more detail as to what a Character is."
    e "我们已经看过如何在Ren'Py中定义一个角色（Character）。但我想更详细地谈谈什么是Character。"

# game/indepth_character.rpy:17
translate schinese demo_character_d7908a94:

    # e "Here are couple of additional characters."
    e "这里还有一些其他的角色。"

# game/indepth_character.rpy:19
translate schinese demo_character_275ef8b9:

    # e "Each statement creates a Character object, and gives it a single argument, a name. If the name is None, no name is displayed."
    e "每个语句创建一个Character对象，并给它一个参数，名字。如果名字为None，则不显示名称。"

# game/indepth_character.rpy:21
translate schinese demo_character_a63aea0c:

    # e "This can be followed by named arguments that set properties of the character. A named argument is a property name, an equals sign, and a value."
    e "后面可以是设置字符属性的命名参数。命名参数由属性名、等号和值组成。"

# game/indepth_character.rpy:23
translate schinese demo_character_636a502e:

    # e "Multiple arguments should be separated with commas, like they are here. Let's see those characters in action."
    e "多个参数应该用逗号分隔，就像它们在这里一样。让我们看看那些角色的动作。"

# game/indepth_character.rpy:27
translate schinese demo_character_44b54e1d:

    # e_shout "I can shout!"
    e_shout "我能大喊大叫！"

# game/indepth_character.rpy:29
translate schinese demo_character_a9646dd8:

    # e_whisper "And I can speak in a whisper."
    e_whisper "也能小声逼逼。"

# game/indepth_character.rpy:31
translate schinese demo_character_79793208:

    # e "This example shows how the name Character is a bit of a misnomer. Here, we have multiple Characters in use, but you see it as me speaking."
    e "这个例子显示Character有点用词不当。在这里，我们有多个Character在使用，但你看到只有我说话。"

# game/indepth_character.rpy:33
translate schinese demo_character_5d5d7482:

    # e "It's best to think of a Character as repesenting a name and style, rather than a single person."
    e "最好把一个Character当作展示一个名字和样式，而不是一个人。"

# game/indepth_character.rpy:37
translate schinese demo_character_66d08d98:

    # e "There are a lot of properties that can be given to Characters, most of them prefixed styles."
    e "有很多属性可以赋予Character，大多数都是前缀样式。"

# game/indepth_character.rpy:39
translate schinese demo_character_7e0d75aa:

    # e "Properties beginning with window apply to the textbox, those with what apply to the the dialogue, and those with who to the name of Character speaking."
    e "以window开头的属性应用于文本框，以what开头的属性应用于对话，以who开头的属性应用于Character的名字。"

# game/indepth_character.rpy:41
translate schinese demo_character_56703784:

    # e "If you leave a prefix out, the style customizes the name of the speaker."
    e "如果不使用前缀，则样式将定义说话者的名字。"

# game/indepth_character.rpy:43
translate schinese demo_character_b456f0a9:

    # e "There are quite a few different properties that can be set this way. Here are some of the most useful."
    e "有很多不同的属性可以这样设置。以下是一些最有用的。"

# game/indepth_character.rpy:48
translate schinese demo_character_31ace18e:

    # e1 "The window_background property sets the image that's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."
    e1 "window_background属性设置用于文本框背景的图像，其大小应与 gui/textbox.png 中的默认大小相同。"

# game/indepth_character.rpy:54
translate schinese demo_character_18ba073d:

    # e1a "If it's set to None, the textbox has no background window."
    e1a "如果设置为None，则文本框没有背景窗口。"

# game/indepth_character.rpy:59
translate schinese demo_character_5a26445c:

    # e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."
    e2 "who_color和what_color属性分别设置人物名字和对话文本的颜色。"

# game/indepth_character.rpy:61
translate schinese demo_character_88a18c32:

    # e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."
    e2 "这些颜色是包含RGB十六进制代码的字符串，与网页浏览器所理解的颜色类型相同。"

# game/indepth_character.rpy:67
translate schinese demo_character_ed690751:

    # e3 "Similarly, the who_font and what_font properties set the font used by the different kinds of text."
    e3 "类似的，who_font和what_font属性设置不同文本使用的字体。"

# game/indepth_character.rpy:74
translate schinese demo_character_8dfa6426:

    # e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."
    e4 "设置who_bold、what_italic和what_size属性可使姓名变为粗体，对话文本变为20像素大小的斜体。"

# game/indepth_character.rpy:76
translate schinese demo_character_20e83c32:

    # e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."
    e4 "当然，what_bold、who_italic和who_size属性也存在，即使它们不在这里使用。"

# game/indepth_character.rpy:83
translate schinese demo_character_e4cbb1f2:

    # e5 "The what_outlines property puts an outline around the text."
    e5 "what_outlines属性在文本周围放置轮廓。"

# game/indepth_character.rpy:85
translate schinese demo_character_71535ecf:

    # e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."
    e5 "这有点复杂，因为它需要一个列表（list），里面是一个元组（tuple），元组是括号中的四个东西，列表由方括号包围。"

# game/indepth_character.rpy:87
translate schinese demo_character_e9ac7482:

    # e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."
    e5 "第一个数字是轮廓的粗细，以像素为单位。后面是一个字符串，给出轮廓颜色的十六进制代码，以及X和Y偏移量。"

# game/indepth_character.rpy:93
translate schinese demo_character_ea72d988:

    # e6 "When the outline size is 0 and the offsets are given, what_outlines can also act as a drop-shadow behind the text."
    e6 "当轮廓大小为0且给定偏移量时，what_outlines也可以充当文本后面的阴影。"

# game/indepth_character.rpy:99
translate schinese demo_character_8d35ebcd:

    # e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."
    e7 "what_xalign和what_textalign属性控制文本的对齐，0.0为左，0.5为中，1.0为右。"

# game/indepth_character.rpy:101
translate schinese demo_character_7c75906c:

    # e7 "The what_xalign property controls where all the text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."
    e7 "what_xalign属性控制所有文本本身放置在文本框中的位置，what_textalign属性控制文本行相对放置的位置。"

# game/indepth_character.rpy:103
translate schinese demo_character_e2811c1c:

    # e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."
    e7 "通常，您需要将what_xalign和what_textalign设置为相同的值。"

# game/indepth_character.rpy:105
translate schinese demo_character_baa52234:

    # e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."
    e7 "将what_layout设置为“subtitle”将使Ren'Py进入subtitle模式，该模式尝试平衡块中每行文本的长度。"

# game/indepth_character.rpy:110
translate schinese demo_character_41190f01:

    # e8 "These properties can be combined to achieve many different effects."
    e8 "这些特性可以组合起来达到许多不同的效果。"

# game/indepth_character.rpy:124
translate schinese demo_character_aa12d9ca:

    # e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."
    e8 "这个例子隐藏了背景，显示居中并加上轮廓的对话，就好像游戏有字幕一样。"

# game/indepth_character.rpy:133
translate schinese demo_character_a7f243e5:

    # e9 "There are two interesting non-style properties, what_prefix and what_suffix. These can put text at the start and end of a line of dialogue."
    e9 "有两个有趣的非样式属性：what_prefix和what_suffix。它们可以将文本放在一行对话的开头和结尾。"

# game/indepth_character.rpy:139
translate schinese demo_character_f9b0052f:

    # e "By using kind, you can copy properties from one character to another, changing only what you need to."
    e "通过使用kind，可以将属性从一个角色复制到另一个角色，只需更改所需的内容。"

# game/indepth_character.rpy:148
translate schinese demo_character_6dfce4b7:

    # l8 "Like this! Finally I get some more dialogue around here."
    l8 "像这样！最后我在这里找到更多的对话。"

# game/indepth_character.rpy:157
translate schinese demo_character_68d9e46c:

    # e "The last thing you have to know is that there's a special character, narrator, that speaks narration. Got it?"
    e "最后你要知道的是，有一个特殊的角色，旁白，负责念旁白。懂了？"

# game/indepth_character.rpy:159
translate schinese demo_character_0c8f314a:

    # "I think I do."
    "我想我明白了。"
