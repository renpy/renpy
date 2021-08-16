
# game/indepth_character.rpy:11
translate russian demo_character_e7e1b1bb:

    # e "We've already seen how to define a Character in Ren'Py. But I want to go into a bit more detail as to what a Character is."
    e "Мы уже видели, как определять персонажа в Ren'Py, но я хочу немного поглубже рассказать вам, что такое Персонаж."

# game/indepth_character.rpy:17
translate russian demo_character_d7908a94:

    # e "Here are couple of additional characters."
    e "Вот пара дополнительных персонажей."

# game/indepth_character.rpy:19
translate russian demo_character_275ef8b9:

    # e "Each statement creates a Character object, and gives it a single argument, a name. If the name is None, no name is displayed."
    e "Каждая строка создаёт объект-персонаж и даёт ему имя, единственный обязательный аргумент. Если имени нет, то оно не отображается."

# game/indepth_character.rpy:21
translate russian demo_character_a63aea0c:

    # e "This can be followed by named arguments that set properties of the character. A named argument is a property name, an equals sign, and a value."
    e "Далее могут следовать аргументы, настраивающие данного персонажа. Подобные аргументы должны содержать правильное имя аргумента, знак = и значение аргумента."

# game/indepth_character.rpy:23
translate russian demo_character_636a502e:

    # e "Multiple arguments should be separated with commas, like they are here. Let's see those characters in action."
    e "Аргументы должны отделяться друг от друга запятыми, как на примере. А теперь давайте посмотрим на этих персонажей в действии."

# game/indepth_character.rpy:27
translate russian demo_character_44b54e1d:

    # e_shout "I can shout!"
    e_shout "Я умею кричать!"

# game/indepth_character.rpy:29
translate russian demo_character_a9646dd8:

    # e_whisper "And I can speak in a whisper."
    e_whisper "И шептать тоже могу."

# game/indepth_character.rpy:31
translate russian demo_character_79793208:

    # e "This example shows how the name Character is a bit of a misnomer. Here, we have multiple Characters in use, but you see it as me speaking."
    e "Этот пример показывает, каким неоднозначным может быть имя персонажа. Мы применили сразу несколько \"персонажей\", но вы видели, что говорю только я."

# game/indepth_character.rpy:33
translate russian demo_character_5d5d7482:

    # e "It's best to think of a Character as repesenting a name and style, rather than a single person."
    e "На самом деле лучше представлять персонажа как связку определённого имени и стиля, нежели как какого-то определённого человека."

# game/indepth_character.rpy:37
translate russian demo_character_66d08d98:

    # e "There are a lot of properties that can be given to Characters, most of them prefixed styles."
    e "Есть множество настроек, которые могут применять к персонажам, и большинство из них — с префиксами."

# game/indepth_character.rpy:39
translate russian demo_character_7e0d75aa:

    # e "Properties beginning with window apply to the textbox, those with what apply to the the dialogue, and those with who to the name of Character speaking."
    e "Настройки можно разделить на те, что начинаются с window и применяются к текстовому окну, на те, что применяются к диалогу и на те, что применяются к имени персонажа."

# game/indepth_character.rpy:41
translate russian demo_character_56703784:

    # e "If you leave a prefix out, the style customizes the name of the speaker."
    e "Если вы выбросите префикс, стиль будет работать только для имени персонажа."

# game/indepth_character.rpy:43
translate russian demo_character_b456f0a9:

    # e "There are quite a few different properties that can be set this way. Here are some of the most useful."
    e "Таким образом работает только несколько параметров, и сейчас я перечислю наиболее полезные."

# game/indepth_character.rpy:48
translate russian demo_character_31ace18e:

    # e1 "The window_background property sets the image that's used for the background of the textbox, which should be the same size as the default in gui/textbox.png."
    e1 "Параметр window_background устанавливает картинку фоном диалогового окна. Она должно быть того же размера, что и стандартное, по адресу gui/textbox.png."

# game/indepth_character.rpy:54
translate russian demo_character_18ba073d:

    # e1a "If it's set to None, the textbox has no background window."
    e1a "Если этот параметр установить на None, из диалогового окна пропадёт фон."

# game/indepth_character.rpy:59
translate russian demo_character_5a26445c:

    # e2 "The who_color and what_color properties set the color of the character's name and dialogue text, respectively."
    e2 "Параметры who_color и what_color устаналивают цвета имени персонажа и текста диалога соответственно."

# game/indepth_character.rpy:61
translate russian demo_character_88a18c32:

    # e2 "The colors are strings containing rgb hex codes, the same sort of colors understood by a web browser."
    e2 "Цвета — это строки, содержащие RGB-код в шестнадцатиричном формате (hex), используемом в веб-браузерах."

# game/indepth_character.rpy:67
translate russian demo_character_ed690751:

    # e3 "Similarly, the who_font and what_font properties set the font used by the different kinds of text."
    e3 "Похожим образом работают параметры who_font и what_font, устанавливающие шрифты различного текста."

# game/indepth_character.rpy:74
translate russian demo_character_8dfa6426:

    # e4 "Setting the who_bold, what_italic, and what_size properties makes the name bold, and the dialogue text italic at a size of 20 pixels."
    e4 "Применив параметры who_bold, what_italic, и what_size, мы сделаем имя жирным, а диалог курсивным и размером в 20 пикселей."

# game/indepth_character.rpy:76
translate russian demo_character_20e83c32:

    # e4 "Of course, the what_bold, who_italic and who_size properties also exist, even if they're not used here."
    e4 "Само собой, параметры what_bold, who_italic и who_size тоже существуют, даже если они здесь не используются."

# game/indepth_character.rpy:83
translate russian demo_character_e4cbb1f2:

    # e5 "The what_outlines property puts an outline around the text."
    e5 "Параметр what_outlines обводит наш текст."

# game/indepth_character.rpy:85
translate russian demo_character_71535ecf:

    # e5 "It's a little complicated since it takes a list with a tuple in it, with the tuple being four things in parenthesis, and the list the square brackets around them."
    e5 "Этот параметр немного сложнее, так как outlines берёт сразу список значений, состоящий из четырёх родительских значений и нескольких скобок."

# game/indepth_character.rpy:87
translate russian demo_character_e9ac7482:

    # e5 "The first number is the size of the outline, in pixels. That's followed by a string giving the hex-code of the color of the outline, and the x and y offsets."
    e5 "Первая цифра обозначает размер обводки в пикселях. Дальше следует hex-код цвета для обводки, и дальше смещение по x и y."

# game/indepth_character.rpy:93
translate russian demo_character_ea72d988:

    # e6 "When the outline size is 0 and the offsets are given, what_outlines can also act as a drop-shadow behind the text."
    e6 "Если размер обводки равен 0, а смещение всё же дано, what_outlines может послужить заменой тени текста."

# game/indepth_character.rpy:99
translate russian demo_character_8d35ebcd:

    # e7 "The what_xalign and what_textalign properties control the alignment of text, with 0.0 being left, 0.5 being center, and 1.0 being right."
    e7 "Параметры what_xalign и what_textalign вместе контролируют выравнивание текста: 0.0 слева, 0.5 по центру, 1.0 справа."

# game/indepth_character.rpy:101
translate russian demo_character_7c75906c:

    # e7 "The what_xalign property controls where all the text itself is placed within the textbox, while what_textalign controls where rows of text are placed relative to each other."
    e7 "Параметр what_xalign контролирует, где размещается текст по отношению к текстовой коробке, а what_textalign контролирует, как размещаются строки текста по отношению друг к другу."

# game/indepth_character.rpy:103
translate russian demo_character_e2811c1c:

    # e7 "Generally you'll want to to set them both what_xalign and what_textalign to the same value."
    e7 "В основном, вам понадобится приводить what_xalign и what_textalign к одному значению."

# game/indepth_character.rpy:105
translate russian demo_character_baa52234:

    # e7 "Setting what_layout to 'subtitle' puts Ren'Py in subtitle mode, which tries to even out the length of every line of text in a block."
    e7 "Поставив what_layout на 'subtitle', Ren'Py переходит в режим субтитров, когда длина каждой строчки пытается быть примерно одинаковой."

# game/indepth_character.rpy:110
translate russian demo_character_41190f01:

    # e8 "These properties can be combined to achieve many different effects."
    e8 "Эти параметры могут комбинироваться для достижения самых разных эффектов."

# game/indepth_character.rpy:124
translate russian demo_character_aa12d9ca:

    # e8 "This example hides the background and shows dialogue centered and outlined, as if the game is being subtitled."
    e8 "Этот пример прячет фон текстового окна и показывает центрированный и обведённый диалог, как будто в игре есть субтитры."

# game/indepth_character.rpy:133
translate russian demo_character_a7f243e5:

    # e9 "There are two interesting non-style properties, what_prefix and what_suffix. These can put text at the start and end of a line of dialogue."
    e9 "Есть два интересных нестилевых параметра: what_prefix и what_suffix. Они могут добавлять текст в начале и в конце диалога."

# game/indepth_character.rpy:139
translate russian demo_character_f9b0052f:

    # e "By using kind, you can copy properties from one character to another, changing only what you need to."
    e "Используя kind, вы можете скопировать параметры одного из персонажей, изменив только то, что вам нужно."

# game/indepth_character.rpy:148
translate russian demo_character_6dfce4b7:

    # l8 "Like this! Finally I get some more dialogue around here."
    l8 "Так-то! Наконец, мне дали что-то сказать."

# game/indepth_character.rpy:157
translate russian demo_character_68d9e46c:

    # e "The last thing you have to know is that there's a special character, narrator, that speaks narration. Got it?"
    e "Последнее, что вам надо узнать, это то что есть специальный персонаж — narrator, играющий роль рассказчика. Понятно, что он делает?"

# game/indepth_character.rpy:159
translate russian demo_character_0c8f314a:

    # "I think I do."
    "Даже не догадываюсь…"

