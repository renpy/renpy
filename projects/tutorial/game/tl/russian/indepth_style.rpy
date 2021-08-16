
# game/indepth_style.rpy:40
translate russian new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "Когда вы создаёте новый проект, Ren'Py автоматический создаёт GUI — Графический Интерфейс Пользователя."

# game/indepth_style.rpy:42
translate russian new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "Он определяет вид всего интерфейса от диалогового окна до вида главного и игрового меню."

# game/indepth_style.rpy:44
translate russian new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "Стандартный GUI вполне достаточен для простенького проекта. С небольшими изменениями вы прямо сейчас видите его в действии."

# game/indepth_style.rpy:46
translate russian new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "Также, GUI создавался для простоты настройки средним разработчиком. Настройка GUI состоит в изменении файлов изображений в папке gui и переменных в gui.rpy."

# game/indepth_style.rpy:48
translate russian new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "В то же самое время, даже при возможности настройки, стандартный GUI может стать слишком узнаваемым для хорошей новеллы, и поэтому мы упростили полную его замену."

# game/indepth_style.rpy:50
translate russian new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "Мы сделали большой справочник по настройке GUI на сайте Ren'Py, так что если вы хотите узнать об этом побольше, почитайте {a=https://www.renpy.org/doc/html/gui.html}Гайд по изменению GUI{/a}."

# game/indepth_style.rpy:58
translate russian styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayables look like."
    e "У Ren'Py есть мощная стилевая система, контролирующая внешний вид объектов."

# game/indepth_style.rpy:60
translate russian styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "Несмотря на то, что в стандартном GUI уже есть много часто используемых стилей, если вы начинаете изменять GUI или создавать собственные экраны, вам нужно будет научиться использовать стили."

# game/indepth_style.rpy:66
translate russian styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "Что вы хотите узнать о стилях?" nointeract

# game/indepth_style.rpy:98
translate russian style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "Стили позволяют одному объекту выглядеть по-разному от игры к игре, или даже в рамках одной игры."

# game/indepth_style.rpy:103
translate russian style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "Например, эти две кнопки использут одни и те же объекты. Но так как к ним применяются разные стили, кнопки сильно отличаются друг от друга."

# game/indepth_style.rpy:108
translate russian style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "Стиль — это комбинация данных из чётырёх источников."

# game/indepth_style.rpy:121
translate russian style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "Первым таким источником Ren'Py считает информацию, взятую из экрана. Каждый объект, созданный экраном, может применять к себе определённый стиль или отдельные его настройки."

# game/indepth_style.rpy:138
translate russian style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "Когда экран содержит в себе текст, настройки стиля с префиксом text_ автоматически применяются к данному тексту."

# game/indepth_style.rpy:151
translate russian style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "Следующим источником являются параметры стиля, как часть оператора image. В данном случае стилевые настройки здесь являются аргументами создаваемого объекта."

# game/indepth_style.rpy:160
translate russian style_basics_ccc0d1ca:

    # egreen "Style properties can also be given as arguments when defining a character."
    egreen "Стилевые настройки также могут задаваться при определении персонажей."

# game/indepth_style.rpy:162
translate russian style_basics_013ab314:

    # egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."
    egreen "Аргументы, начинающиеся с who_ — настройки стиля, применяемые к имени персонажа, а начинающиеся с what_ — к тексту персонажа."

# game/indepth_style.rpy:164
translate russian style_basics_dbe80939:

    # egreen "Style properties that don't have a prefix are also applied to the character's name."
    egreen "Стилевые настройки, не имеющие префикса, применяются только к имени персонажа."

# game/indepth_style.rpy:174
translate russian style_basics_ac6a8414:

    # e "Finally, there is the the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "И наконец, существует оператор style, создающий или изменящий уже существующий стиль. Добавив к тексту аргумент style, мы говорим Ren'py использовать стиль blue_text."

# game/indepth_style.rpy:180
translate russian style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "Настройки стиля могут наследоваться от родительского стиля. Например, если какая-то настройка в стиле не задаётся, она автоматически применяется от родителя этого стиля."

# game/indepth_style.rpy:182
translate russian style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "Изначально, родитель стиля имеет то же начальное имя, плюс префиксы, вплоть до первого символа подчёркивания. Если в полном имени стиля нет подчёркиваний, то используется стиль 'default'."

# game/indepth_style.rpy:184
translate russian style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "Приведём понятный пример: blue_text является дочерним стилем от text, который, в свою очередь, происходит от default."
    e "Стиль default является базовым стилем, определяющим все настройки и параметры, так что он может быть только родителем."

# game/indepth_style.rpy:190
translate russian style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "Родителя можно легко изменить, использовав функцию 'is'. В данном случае мы установили родителем стиля text."

# game/indepth_style.rpy:194
translate russian style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "У каждого объекта есть базовое имя стиля. Стандартно, обычно это прописное имя объекта, например 'text' у текста, или 'button' у кнопок."

# game/indepth_style.rpy:196
translate russian style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "В экранах объекту можно дать параметр style_prefix, дающий определённый префикс объекту и всем его детям."

# game/indepth_style.rpy:198
translate russian style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "Например, объект text со стилевым префиксом 'help' даст нам стиль 'help_text'."

# game/indepth_style.rpy:200
translate russian style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "И наконец, когда объектом становится кнопка или объект внутри кнопки, у него тоже появляются префиксы."

# game/indepth_style.rpy:202
translate russian style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "Префиксы idle_, hover_, и insensitive_ используются, когда кнопка находится в ожидании, находится под наведением и когда на кнопку невозможно навестись."

# game/indepth_style.rpy:204
translate russian style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "Можно продолжить префиксом selected_, изменяющим вид нажатой кнопки, или когда в кнопке отображается текущее значение или экран."

# game/indepth_style.rpy:233
translate russian style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "Этот экран показывает префиксы в действии. Вы можете навестись на кнопку, кликнуть на неё, а затем вывести курсор за пределы экрана и продолжить."

# game/indepth_style.rpy:240
translate russian style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "Это основы стилей. Если одной настройки GUI вам недостаточно, стили позволят вам подстроить под себя почти всё."

# game/indepth_style.rpy:253
translate russian style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "Первой группой параметров, с которыми мы будем знакомиться — основные настройки стилей. Они работают с каждым объектом, ну или с абсолютном большинством."

# game/indepth_style.rpy:264
translate russian style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "У каждого объекта есть своя позиция на экране, и так как я о них уже говорила, мы их пропустим."

# game/indepth_style.rpy:275
translate russian style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "Параметры xmaximum и ymaximum устанавливают максимум ширины и высоты объекта. Благодаря им Ren'py будет пытаться сжимать объекты, если это возможно."

# game/indepth_style.rpy:277
translate russian style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "Иногда, сжатый размер оказывается даже меньше, чем заданный xmaximum и ymaximum."

# game/indepth_style.rpy:279
translate russian style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "Так что схожим образом работают параметры xminimum и yminimum, устанавливающие минимальную ширину и высоту. Если объект меньше, Ren'Py попытается его увеличить."

# game/indepth_style.rpy:289
translate russian style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "Параметры xsize и ysize уравнивают максимальные и минимальные размеры, делая объект строго определённого размера."

# game/indepth_style.rpy:291
translate russian style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "Это работает только с теми объектами, которых можно масштабировать. Некоторые объекты подобным образом делать больше или меньше нельзя."

# game/indepth_style.rpy:299
translate russian style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "Параметр area (область) берёт четыре параметра. Первые два определяют позицию, а вторые — размер области."

# game/indepth_style.rpy:308
translate russian style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "И наконец, параметр alt изменяет текст синтезатора речи, обычно используемого для слабослышащих. Можете попробовать, нажав на shift+v."

# game/indepth_style.rpy:335
translate russian style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "Настройки стиля для текста применяются, само собой очевидно, к объектам текста и ввода текста."

# game/indepth_style.rpy:337
translate russian style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "Текстовые объекты могут создаваться как явно, так и неявно. Например, текстовая кнопка (textbutton) создаёт объект текст (text), в котором стиль заканчивается на button_text."

# game/indepth_style.rpy:339
translate russian style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "Кстати, подобные настройки можно легко изменить в gui.rpy, добавив или изменив переменные. Например, размер текста изменяется параметром gui.button_text_size."

# game/indepth_style.rpy:347
translate russian style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "Параметр bold делает текст жирным. Жирным текст можно делать с помощью специального алгоритма, а не с использованием внедрённой в шрифт жирной версии."

# game/indepth_style.rpy:355
translate russian style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "Параметр color изменяет цвет текста. Он использует шестнадцатеричные цветовые коды, как и везде."

# game/indepth_style.rpy:363
translate russian style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "Параметр first_indent определяет размер отступа первой строчки."

# game/indepth_style.rpy:371
translate russian style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "Параметр font изменяет шрифт, используемый текстом. Ren'Py использует шрифты TrueType и OpenType, и для использования шрифта вам обязательно надо включить его в ресурсы вашей новеллы."

# game/indepth_style.rpy:379
translate russian style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "Параметр size изменяет размер текста."

# game/indepth_style.rpy:388
translate russian style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "Параметр italic делает текст итальянским… Шутка, курсивным. И опять же, лучше всего, когда курсив изначально есть в шрифте, хотя с небольшими фрагментами текста Ren'Py может справиться."

# game/indepth_style.rpy:397
translate russian style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "Параметр justify выравнивает весь текст, кроме последней строчки в абзаце."

# game/indepth_style.rpy:405
translate russian style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "Параметр kerning применяет к тексту кернинг. Когда его значение отрицательно, символы текста становятся ближе друг к другу. Когда положительное — наоборот."

# game/indepth_style.rpy:415
translate russian style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "Параметры line_leading и line_spacing повышают пробел ПЕРЕД каждой строчкой и МЕЖДУ строчками соответственно."

# game/indepth_style.rpy:424
translate russian style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "Параметр outlines определённым образом обводит текст. Он берёт целый список значений, который сперва кажется сложным."

# game/indepth_style.rpy:426
translate russian style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "Но если вы отбросите скобки, то вы увидите размер обводки, её цвет и смещения по горизонтали и вертикали."

# game/indepth_style.rpy:434
translate russian style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "Параметр rest_indent контролирует отступ уже всех оставшихся строк после первой."

# game/indepth_style.rpy:443
translate russian style_text_430c1959:

    # e "The text_align property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "Параметр text_align контролирует выравнивание текста по горизонтали по всему объекту. Например, 0.5 означает, что выравнивание у нас идёт по центру."

# game/indepth_style.rpy:445
translate russian style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the text_align and xalign to the same value."
    e "Но он не изменяет саму позицию текстового объекта. Для этого вам потребуется привести text_align вместе с xalign к одному значению."

# game/indepth_style.rpy:455
translate russian style_text_efc3c392:

    # e "When both text_align and xalign are set to 1.0, the text is properly right-justified."
    e "Когда оба параметры были установлены на 1.0, текст стал выровнен по правой стороне."

# game/indepth_style.rpy:464
translate russian style_text_43be63b9:

    # e "The underline property underlines the text."
    e "Параметр underline подчёркивает текст."

# game/indepth_style.rpy:471
translate russian style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "Это самые распространённые настройки текста, но далеко не все. Сейчас я покажу вам парочку, которая может вам потребоваться при особых обстоятельствах."

# game/indepth_style.rpy:479
translate russian style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "Изначально, весь текст в Ren'Py сглажен, чтобы у него не были видны острые края. Параметр antialias может выключить сглаживание, что сделает текст более резким."

# game/indepth_style.rpy:487
translate russian style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "Параметр adjust_spacing сперва кажется незаметным, так как он виден только тогда, когда игрок изменяет размеры окна. При включении, символы немного сдвигаются, так что они примерно сохраняют свой относительный отступ."

# game/indepth_style.rpy:496
translate russian style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "Когда он выключен, текст больше не будет изменяться. Но так он может оказаться чуточку шире или уже, в зависимости от размера экрана."

# game/indepth_style.rpy:505
translate russian style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "Параметр layout имеет несколько специальных значений, контролирующих перенос строки. При установке на 'nobreak', строка вообще не переносится, благодаря чему текст становится шире."

# game/indepth_style.rpy:516
translate russian style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "При установке на 'subtitle', алгоритм переноса изменяется так, чтобы строки были примерно одной длины, как обычно используется в субтитрах."

# game/indepth_style.rpy:524
translate russian style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "Параметр strikethrough зачёркивает текст. Выглядит довольно неприятно, так что я не рекомендую его использовать."

# game/indepth_style.rpy:534
translate russian style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "Параметр vertical изменяет направление письма. Обычно, это нужно для языков Азии, использующих специальных шрифты."

# game/indepth_style.rpy:540
translate russian style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "И вот пока что все стилевые параметры текста. Может показаться, что их слишком много, но мы хотим дать вам как можно больше возможностей для показа текста игрокам."

# game/indepth_style.rpy:580
translate russian style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "Далее у нас идут стилевые параметры для окон и кнопок. Они применяются к окнам (одно такое вы сейчас читаете) и рамкам, в которых мы показываем вам примеры."

# game/indepth_style.rpy:582
translate russian style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "Да, также их можно применять к кнопками как в игре, так и вне её. Кнопка в Ren'Py — это окно, на которое можно кликнуть."

# game/indepth_style.rpy:593
translate russian style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "Для начала, я начну со стиля, в котором наследуется буквально всё. Чтобы было попроще, он будет наследовать параметры базового стиля, а наверху вы увидите уже готовые кнопки, которые мы будем постепенно улучшать."

# game/indepth_style.rpy:595
translate russian style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "Первый параметр стиля — это параметр background. Он добавляет кнопке или окну фон. Учитывая, что это кнопка, мы добавим ему фон в ожидании и другой фон при наведении."

# game/indepth_style.rpy:597
translate russian style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "Также, мы центрировали обе кнопки, применив параметр xalign."

# game/indepth_style.rpy:601
translate russian style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "Также мы изменили стиль текста в кнопках, использовав вот такой стиль. Он центрирует текст и заставляет его менять цвет при наведении на кнопку."

# game/indepth_style.rpy:612
translate russian style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "Без небольшого открытого пространства вокруг текста, кнопка выглядит обрезанной. В Ren'Py есть параметр padding, позволяющий увеличить размер фона на краях."

# game/indepth_style.rpy:621
translate russian style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "Хотя чаще всего, используются параметры xpadding и ypadding, которые добавляют одинаковое количество пространства по горизонтали и по вертикали."

# game/indepth_style.rpy:629
translate russian style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "Параметры margin работают почти также, но они ещё и расширяют пространство вне кнопки. Полный набор margin: left_margin, right_margin, top_margin, bottom_margin, xmargin и ymargin."

# game/indepth_style.rpy:638
translate russian style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "Параметр size_group задаёт определённое условие. Таким образом Ren'Py убедится, что все окна и кнопки одной size_group будут одного размера."

# game/indepth_style.rpy:647
translate russian style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "Другой метод: параметры xfill и yfill позволят кнопке занять всё доступное пространство по горизонтали и вертикали."

# game/indepth_style.rpy:657
translate russian style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "Параметр foreground добавляет объект, который располагается надо всем содержимым кнопки или окна."

# game/indepth_style.rpy:659
translate russian style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "Одним из способов его использования может быть декорирование нажатой кнопки галочкой или чем-либо ещё. Другой вариант: использовать его с рамкой, которая будет перекрывать содержимое кнопки."

# game/indepth_style.rpy:668
translate russian style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "Также существует несколько параметров, применимых только ко кнопкам. Параметры hover_sound и activate_sound проигрывают звуковой файл при наведении или активации кнопки."

# game/indepth_style.rpy:677
translate russian style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "И последнее, параметр focus_mask применяется к частично прозрачным кнопкам. Когда параметр включается, только область кнопки, не затронутая прозрачностью, будет вызывать эффект наведения."

# game/indepth_style.rpy:759
translate russian style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "Чтобы продемонстрировать вам эти стили, позвольте сперва показать два изображения, которые мы будем использовать. Вот это изображение мы будем использовать, когда полоска будет пустой."

# game/indepth_style.rpy:763
translate russian style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "А это, когда полоска будет заполнена."

# game/indepth_style.rpy:775
translate russian style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "Параметры left_bar и right_bar и их hover варианты отвечают за левую и правую стороны полоски. Это связано с тем, что изначально значение повышается слева направо."

# game/indepth_style.rpy:777
translate russian style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "И так же изначально и левый объект и правый обрабатываются во всю ширину полоски, а затем обрезаются до подходящего размера."

# game/indepth_style.rpy:779
translate russian style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "Мы дали полоске параметр ysize, чтобы указать на то, какой высоты она должна быть. Мы так же могли бы сделать с xsize, задав ширину, но в данном случае полоска ограничена шириной рамки."

# game/indepth_style.rpy:792
translate russian style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "Когда включается параметр bar_invert, полоска начинает увеличиваться справа налево. Хотя можно просто поменять местами наши объекты."

# game/indepth_style.rpy:806
translate russian style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "Параметр bar_resizing заставляет изображения масштабироваться, вместо того чтобы обрабатываться в полном размере, а затем обрезаться."

# game/indepth_style.rpy:819
translate russian style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "Параметр thumb вставляет изображение, накладываемое на текущее значение полоски. В случае полос прокрутки, оно масштабируется, когда это возможно."

# game/indepth_style.rpy:821
translate russian style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "В данном случае мы использовали его вместе с параметром base_bar, который привёл оба изображения полоски к одному объекту."

# game/indepth_style.rpy:836
translate russian style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "Параметры left_gutter и right_gutter вставляют канавки на левую и правую стороны полоски. Канавка — это свободное пространство, обозначающее границу полоски."

# game/indepth_style.rpy:851
translate russian style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "Параметр bar_vertical отображает вертикально-ориентированную полоску. Все остальные параметры из-за этого меняют имя: left_bar становится top_bar, а right_bar — bottom_bar."

# game/indepth_style.rpy:856
translate russian style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "И наконец, есть один стиль, который мы не можем здесь показать, и это unscrollable. Он контролирует, что случится, если значение полосы прокрутки изменить нельзя."

# game/indepth_style.rpy:858
translate russian style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "По стандарту, она показывается. Но если параметр unscrollable поставить в 'insensitive', полоска становится для игрока нечувствительное. А если в 'hide', полоска скрывается, но всё ещё занимает определённое пространство."

# game/indepth_style.rpy:862
translate russian style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "На этом с полосками мы закончили. Используя их, разработчик может изменять полоски, полосы прокрутки и слайдеры."

# game/indepth_style.rpy:961
translate russian style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "Объект hbox используется, чтобы показать свои дочерние объекты горизонтально. По стандарту, между \'детьми\' нет пропусков, так что они сливаются."

# game/indepth_style.rpy:967
translate russian style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "Похожим образом действует vbox, показывая свои дочерние объекты вертикально. Оба стиля поддерживают параметры, контролирующие местоположение объектов."

# game/indepth_style.rpy:972
translate russian style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "Чтобы сделать размер коробки видимым, я подсвечу именно её, а не общую рамку."

# game/indepth_style.rpy:980
translate russian style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "Коробки поддерживают параметры xfill и yfill. Эти параметры заставляют коробку расширяться на всё возможное пространство, а не только по размеру наибольшего \'ребёнка\'."

# game/indepth_style.rpy:990
translate russian style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "Параметр spacing берёт значение в пикселях и добавляет равное им свободное пространство между каждым \'ребёнком\' коробки."

# game/indepth_style.rpy:1000
translate russian style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "Параметр first_spacing действует похожим образом, но он добавляет пространство только между первым и вторым ребёнком. Это полезно, когда первая строчка — заголовок, которому требуются другие размеры."

# game/indepth_style.rpy:1010
translate russian style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "Параметр box_reverse переворачивает порядок показа детей в коробке."

# game/indepth_style.rpy:1023
translate russian style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "Для следующего примера мы вернёмся к горизонтальной коробке."

# game/indepth_style.rpy:1033
translate russian style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "Параметр box_wrap заполняет коробку детьми, пока она не переполнится, а затем переносит оставшихся детей на следущие строки."

# game/indepth_style.rpy:1046
translate russian style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "У таблиц есть ещё два стилевых параметра. Это xspacing и yspacing, контролирующие отступы по горизонтали и вертикали."

# game/indepth_style.rpy:1053
translate russian style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "И последнее, у нас есть фиксированный слой (fixed). Фиксированный слой обычно расширяется на всё пространство и показывает своих детей друг над другом."

# game/indepth_style.rpy:1055
translate russian style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "Но само собой, у нас есть для него пара параметров."

# game/indepth_style.rpy:1064
translate russian style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "Если параметр xfit равен True, фиксация покрывает всех своих детей, а затем сжимается до их размера по ширине. Параметр yfit работает уже по высоте."

# game/indepth_style.rpy:1072
translate russian style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "Параметр order_reverse изменяет порядок показа детей. Вместо того, чтобы показывать их наружу, они начинают показываться в порядке внутрь."

# game/indepth_style.rpy:1084
translate russian style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "Иногда трудно понять, какой стиль использует тот или иной объект. Диспетчер объектов может с этим помочь."

# game/indepth_style.rpy:1086
translate russian style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "Чтобы использовать его, наведите мышь на какую-либо часть игрового интерфейса Ren'Py и нажмите shift+i."

# game/indepth_style.rpy:1088
translate russian style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "Ren'Py выдаст список объектов, на которые навелась мышка. После каждого объекта идёт имя его стиля."

# game/indepth_style.rpy:1090
translate russian style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "Вы можете кликнуть на имя стиля, чтобы увидеть его параметры или их принадлежность."

# game/indepth_style.rpy:1092
translate russian style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "По стандарту, диспетчер показывает только элементы интерфейса, не изображения. Если вы хотите увидеть в диспетчере и изображения, нажмите shift+alt+i."

# game/indepth_style.rpy:1094
translate russian style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "Можете попробовать диспетчер прямо сейчас, наведя мышку на этот текст и нажав shift+i."

translate russian strings:

    # indepth_style.rpy:20
    old "Button 1"
    new "Кнопка 1"

    # indepth_style.rpy:22
    old "Button 2"
    new "Кнопка 2"

    # indepth_style.rpy:66
    old "Style basics."
    new "Основы стилей."

    # indepth_style.rpy:66
    old "General style properties."
    new "Основные параметры стилей."

    # indepth_style.rpy:66
    old "Text style properties."
    new "Текст и его стили."

    # indepth_style.rpy:66
    old "Window and Button style properties."
    new "Параметры стилей для Окон и Кнопок."

    # indepth_style.rpy:66
    old "Bar style properties."
    new "Полоски горизонтальные и вертикальные."

    # indepth_style.rpy:66
    old "Box, Grid, and Fixed style properties."
    new "Стили для Коробок, Фиксаций и Таблиц."

    # indepth_style.rpy:66
    old "The Displayable Inspector."
    new "Диспетчер объектов."

    # indepth_style.rpy:66
    old "That's all I want to know."
    new "Этого достаточно."

    # indepth_style.rpy:112
    old "This text is colored green."
    new "Этот текст окрашен в зелёный."

    # indepth_style.rpy:126
    old "Danger"
    new "Опасность"

    # indepth_style.rpy:142
    old "This text is colored red."
    new "Этот текст окрашен в розовый."

    # indepth_style.rpy:170
    old "This text is colored blue."
    new "Этот текст окрашен в синий."

    # indepth_style.rpy:248
    old "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"
    new "Облетев Землю в корабле-спутнике, я увидел, как прекрасна наша планета.\n–Юрий Гагарин"

    # indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "\"Облетев Землю в корабле-спутнике, я увидел, как прекрасна наша планета.\" Цитата Юрия Гагарина."

    # indepth_style.rpy:326
    old "Vertical"
    new "Вертикальный текст"

    # indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "Лучше осмеливаться на могучие дела, добиваться славных триумфов, пусть и перемежающихся с неудачами, чем стоять в одном ряду со слабыми духом, которые не могут ни наслаждаться от души, ни сильно страдать, потому что живут в серых сумерках, где нет ни побед, ни поражений.\n\nТеодор Рузвельт"

    # indepth_style.rpy:561
    old "Top Choice"
    new "Верхний выбор"

    # indepth_style.rpy:566
    old "Bottom Choice"
    new "Нижний выбор"

    # indepth_style.rpy:879
    old "First Child"
    new "Первый"

    # indepth_style.rpy:880
    old "Second Child"
    new "Второй"

    # indepth_style.rpy:881
    old "Third Child"
    new "Третий"

    # indepth_style.rpy:884
    old "Fourth Child"
    new "Четвёртый"

    # indepth_style.rpy:885
    old "Fifth Child"
    new "Пятый"

    # indepth_style.rpy:886
    old "Sixth Child"
    new "Шестой"

