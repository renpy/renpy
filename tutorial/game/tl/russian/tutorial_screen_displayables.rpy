
# game/tutorial_screen_displayables.rpy:3
translate russian screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "На экранах существует несколько разновидностей объектов. В этом разделе я расскажу о самых важных из них."

# game/tutorial_screen_displayables.rpy:9
translate russian screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "О чём бы вы хотели узнать?" nointeract

# game/tutorial_screen_displayables.rpy:49
translate russian screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "Есть несколько параметров, которые присутствуют в языке каждого экранного объекта. Сейчас я их продемонстрирую."

# game/tutorial_screen_displayables.rpy:57
translate russian screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "Во-первых, каждый объект поддерживает позиционные параметры. Когда объект находится в каком-либо контейнере (здесь это рамка), вы можете использовать параметры align, anchor, pos и так далее, и тому подобное."

# game/tutorial_screen_displayables.rpy:69
translate russian screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "Параметр at применяет к объекту трансформацию, так же как и функция at при операторе show."

# game/tutorial_screen_displayables.rpy:106
translate russian screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "Параметр id часто используется на экране say, на котором показывается диалог. Вне этого экрана он обычно не встречается."

# game/tutorial_screen_displayables.rpy:108
translate russian screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "Он говорит Ren'Py, какие объекты отвечают за фон, кто (\"who\") говорит, и что (\"what\") было сказано. Он используется для применения стилей к каждому персонажу и помогает при использовании режима авточтения."

# game/tutorial_screen_displayables.rpy:123
translate russian screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "Параметр style позволяет вам применить стиль к какому-либо одному объекту."

# game/tutorial_screen_displayables.rpy:144
translate russian screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "Параметр style_prefix устанавливает стилевой префикс, используемый затем объектом и всеми его 'детьми'."

# game/tutorial_screen_displayables.rpy:146
translate russian screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "Например, когда параметр style_prefix установлен на 'green', на всю вертикальную коробку (vbox) применяется стиль 'green_vbox', а к тексту стиль 'green_text'."

# game/tutorial_screen_displayables.rpy:150
translate russian screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "Есть ещё несколько параметров помимо этих, и вы сможете найти их в документации. Но именно о внедрении в вашу игру показанных вам параметров вы могли бы подумать."

# game/tutorial_screen_displayables.rpy:156
translate russian add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "Иногда бывает ситуация, когда у вас есть объект, и вы хотите добавить его на экран."

# game/tutorial_screen_displayables.rpy:165
translate russian add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "Это можно сделать через оператор add."

# game/tutorial_screen_displayables.rpy:167
translate russian add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "Существует несколько способов того, как нам сослаться на нужное изображение. Если оно находится в папке images и не заявлено оператором image, вы можете просто написать его имя в скобках."

# game/tutorial_screen_displayables.rpy:176
translate russian add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "На изображение также можно сослаться при помощи полного пути к файлу относительно папки game."

# game/tutorial_screen_displayables.rpy:185
translate russian add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "С помощью оператора add мы можем добавлять и другие объекты. Здесь, например, мы добавили объект Solid, закрасив целый блок одним цветом."

# game/tutorial_screen_displayables.rpy:195
translate russian add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "В дополнение к объектам, к оператору add можно добавить трансформационные параметры. Они могут тем или иным образом трансформировать добавленный объект."

# game/tutorial_screen_displayables.rpy:207
translate russian add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "Разумеется, оператор add также может взять и параметр at, позволяющий делать более сложные трансформации."

# game/tutorial_screen_displayables.rpy:222
translate russian text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "Оператор text в языке экранов добавляет текстовый объект на экран. Он требует один аргумент — сам текст."

# game/tutorial_screen_displayables.rpy:224
translate russian text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "В дополнение к общим для всех объектов параметрам, тексту доступны стилевые параметры. Например, size устанавливает размер текста."

# game/tutorial_screen_displayables.rpy:234
translate russian text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "Текстовый объект также способен воспринимать выражения, заключённые в квадратные скобки."

# game/tutorial_screen_displayables.rpy:236
translate russian text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "Когда текст показывается на экране при помощи оператора text, переменные, определённые в рамках экрана, имеют приоритет над определёнными вне его."

# game/tutorial_screen_displayables.rpy:238
translate russian text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "Такие переменные могут быть параметрами экрана, определёнными операторами default и python, или же при помощи действия SetScreenVariable."

# game/tutorial_screen_displayables.rpy:247
translate russian text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "В общем-то не о чем больше говорить о тексте, так как он работает так же, как и любой другой текст в Ren'Py."

# game/tutorial_screen_displayables.rpy:255
translate russian layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "Слоевые объекты принимают в себя другие объекты и показывают их на экране."

# game/tutorial_screen_displayables.rpy:269
translate russian layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "Например, объект hbox берёт объекты и складывает их горизонтально."

# game/tutorial_screen_displayables.rpy:284
translate russian layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "Параметр vbox действует уже вертикально."

# game/tutorial_screen_displayables.rpy:286
translate russian layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "К обеим параметрам могут применяться параметры коробок, и самый полезный из них — spacing, обозначающий свободное пространство между объектами."

# game/tutorial_screen_displayables.rpy:301
translate russian layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "Объект grid показывает дочерние объекты в таблице с одинаковыми размерами. Он берёт два аргумента: количество колонок и количество строк."

# game/tutorial_screen_displayables.rpy:303
translate russian layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "Таблика обязательно должна быть полной, иначе Ren'py сообщит об ошибке. Заметьте, как в противном случае поступают в примере — пустая ячейка заполнена null."

# game/tutorial_screen_displayables.rpy:305
translate russian layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "Как и в коробках, таблицы используют параметр spacing для определения пространства между ячейками."

# game/tutorial_screen_displayables.rpy:321
translate russian layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "Таблицы также имеют параметр transpose для изменения направления заполнения из слева-вправо на сверху-вниз."

# game/tutorial_screen_displayables.rpy:338
translate russian layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "И для того, чтобы продемонстрировать, что все ячейки одинакового размера, я сделаю текст в одной из них больше, чем в других."

# game/tutorial_screen_displayables.rpy:353
translate russian layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "Объект fixed показывает дочерние объекты с использованием обычного алгоритма расположения. Он позволяет разместить объекты в любом месте экрана."

# game/tutorial_screen_displayables.rpy:355
translate russian layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "По стандарту, слой расширяется на всё доступное пространство. Чтобы это предотвратить, мы использовали параметры xsize и ysize, принудительно заставив принять необходимые нам размеры."

# game/tutorial_screen_displayables.rpy:369
translate russian layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "Когда в неслоевой объект добавляется два или больше дочерних объектов, то необязательно создавать fixed, так как он добавится автоматически, и все дочерние объекты будут к нему приписаны."

# game/tutorial_screen_displayables.rpy:384
translate russian layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "И наконец, есть одно удобное средство для экономии места. Когда создаётся много дочерних объектов, если начать добавлять к каждому из них слой, то всё может закончиться ну просто безумными отступами."

# game/tutorial_screen_displayables.rpy:386
translate russian layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "Оператор has создаёт слой, а затем добавляет все последующие дочерние объекты к этому слою. Это позволяет сделать экран более читабельным."

# game/tutorial_screen_displayables.rpy:395
translate russian window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "В стандартном GUI большинство элементов пользовательского интерфейса требуют какой-либо фон."

# game/tutorial_screen_displayables.rpy:405
translate russian window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "Без фона текст бывает трудно читать. И хотя рамка не строго обязательна, у большинства экранов есть хотя бы одна такая, если не больше."

# game/tutorial_screen_displayables.rpy:417
translate russian window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "Но когда я добавляю фон, всё становится гораздо проще. Именно поэтому мы используем два объекта для отображения фона игрового интерфейса."

# game/tutorial_screen_displayables.rpy:419
translate russian window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "Эти два объекта — frame и window. Первую, рамку, вы видите выше. Она предназначается для создания фона разным частям пользовательского интерфейса."

# game/tutorial_screen_displayables.rpy:423
translate russian window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "С другой стороны, объект window очень специфичен. Он используется для отображения текстового окна. Если вы сейчас это читаете, то поздравляю, вы смотрите на текстовое окно."

# game/tutorial_screen_displayables.rpy:425
translate russian window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "К рамкам и окнам могут применяться стилевые параметры для окон, позволяя вам изменять фон, поля, пространство вокруг окна и так далее."

# game/tutorial_screen_displayables.rpy:433
translate russian button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "Один из самых гибких объектов в Ren'Py — это кнопка, а также её варианты 'текстовая кнопка' и 'кнопка-изображение'."

# game/tutorial_screen_displayables.rpy:443
translate russian button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "Кнопка — это объект, который при нажатии активирует действие. На кнопку можно нажать, кликнув на неё мышью, коснувшись её или выбрав её при помощи клавиатуры или контроллёра."

# game/tutorial_screen_displayables.rpy:445
translate russian button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "Действия могут многое. Например, они отвечают за установку переменных, показ экранов, прыжки на метки, возврат значения… Множество действий {a=https://www.renpy.org/doc/html/screen_actions.html}описано в документации Ren'Py{/a}, и вы также можете написать свои собственные."

# game/tutorial_screen_displayables.rpy:458
translate russian button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "Также возможно запускать действия, когда кнопка приобретает или теряет фокус."

# game/tutorial_screen_displayables.rpy:473
translate russian button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "Кнопка может вбирать в себя другие объекты. Учитывая, что таким объектом может быть слой, внутри кнопок может содержаться столько дочерних объектов, сколько вы захотите."

# game/tutorial_screen_displayables.rpy:483
translate russian button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "Во многих случаях кнопки будут состоять из текста. Чтобы облегчить вам задачу, вот текстовая кнопка, принимающая текст как аргумент."

# game/tutorial_screen_displayables.rpy:485
translate russian button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "Учитывая, что объект текстовой кнопки управляет стилем текста в ней, данная разновидность чаще всего используется в стандартном GUI."

# game/tutorial_screen_displayables.rpy:498
translate russian button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "Также существуют кнопки-изображения, состоящие из изображений, одно на каждое возможное состояние кнопки, и показывающие их в качестве кнопки."

# game/tutorial_screen_displayables.rpy:500
translate russian button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "Кнопка-изображение даёт вам наибольший контроль над видом кнопки, но её в разы труднее переводить, и она может потерять свой вид при изменении размеров экрана."

# game/tutorial_screen_displayables.rpy:522
translate russian button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "Кнопки следуют стилевым параметрам окон, контролирующим фон, поля и окружающее их пространство. Есть также специфичные параметры для кнопок, например, которые проигрывают звук при наведении."

# game/tutorial_screen_displayables.rpy:524
translate russian button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "При использовании с кнопкой, стилевым параметрам могут даваться префиксы idle и hover, позволяющие изменить определённое состояние кнопки."

# game/tutorial_screen_displayables.rpy:526
translate russian button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "Текстовая кнопка таким же образом следует текстовым стилевым параметрам с префиксом text. Они применяются к текстовому объекту, создающемуся внутри кнопки."

# game/tutorial_screen_displayables.rpy:558
translate russian button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "И конечно, мы очень редко настраиваем каждую кнопку на подобных экранах. Вместо этого мы создаём отдельный стиль и говорим Ren'Py его использовать."

# game/tutorial_screen_displayables.rpy:577
translate russian bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "Объекты bar и vbar — это гибкие объекты-полоски, отображающие какое-то значение. Значение может быть статичным, анимированным или настраиваемым со стороны игрока."

# game/tutorial_screen_displayables.rpy:579
translate russian bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "Параметр value устанавливает BarValue — объект, определяющий значение полоски и её диапазон. Выше располагается StaticValue с диапазоном 100 и значением 66, при котором полоска заполнилась на две трети."

# game/tutorial_screen_displayables.rpy:581
translate russian bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "Список всех применимых BarValues находится {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}в документации к Ren'Py{/a}."

# game/tutorial_screen_displayables.rpy:583
translate russian bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "В этом примере мы определяем рамку и параметр xsize. Если мы этого не сделаем, полоска займёт всё доступное по горизонтали пространство."

# game/tutorial_screen_displayables.rpy:600
translate russian bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "В стандартном GUI существует несколько разных стилей полосок. Стили выбираются параметром style, а в нашем случае default определяет базовое их значение."

# game/tutorial_screen_displayables.rpy:602
translate russian bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "Верхний стиль — это 'bar'. Он используется для отображения значений, которые не могут изменяться игроком, как значения здоровья или прогресса."

# game/tutorial_screen_displayables.rpy:604
translate russian bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "Средний стиль — 'slider'. Он используется для значений, которые игрок может изменить. Например, громкость звука."

# game/tutorial_screen_displayables.rpy:606
translate russian bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "И наконец, нижний стиль — 'scrollbar', используемый для горинтальных полос прокрутки. При использовании полос прокрутки, тумблер в центре воздействует на порт просмотра, позволяя его перемещать."

# game/tutorial_screen_displayables.rpy:623
translate russian bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "Объект vbar подобен объекту bar, исключая то, что по стандарту он используется вертикальные стили — 'vbar', 'vslider' и 'vscrollbar'."

# game/tutorial_screen_displayables.rpy:626
translate russian bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "Полосы используют стилевые параметры для полос, которые могут значительно улучшить их внешний вид. Просто посмотрите на разницу между полоской, слайдером и полосой прокрутки."

# game/tutorial_screen_displayables.rpy:635
translate russian imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "Карты изображений используют два и более изображений для показа кнопок и полосок. Давайте я начну с примера карты-изображения в действии."

# game/tutorial_screen_displayables.rpy:657
translate russian swimming_405542a5:

    # e "You chose swimming."
    e "Вы выбрали плавание."

# game/tutorial_screen_displayables.rpy:659
translate russian swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "Плавать весело, но я не принесла купальник."

# game/tutorial_screen_displayables.rpy:665
translate russian science_83e5c0cc:

    # e "You chose science."
    e "Вы выбрали науку."

# game/tutorial_screen_displayables.rpy:667
translate russian science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "Я слышала, что в некоторых школах есть научные команды, но я считаю, что с исследованиями нельзя спешить."

# game/tutorial_screen_displayables.rpy:672
translate russian art_d2a94440:

    # e "You chose art."
    e "Вы выбрали искусство."

# game/tutorial_screen_displayables.rpy:674
translate russian art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "Хорошие фоны тяжело рисовать, поэтому во многих играх используются фото с фильтрами. Возможно, вам удастся это изменить."

# game/tutorial_screen_displayables.rpy:680
translate russian home_373ea9a5:

    # e "You chose to go home."
    e "Вы решили пойти домой."

# game/tutorial_screen_displayables.rpy:686
translate russian imagemap_done_48eca0a4:

    # e "Anyway..."
    e "Так вот..."

# game/tutorial_screen_displayables.rpy:691
translate russian imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "Чтобы продемонстрировать вам, как работает карта изображений, я покажу вам пять изображений, из которых формируется маленький imagemap."

# game/tutorial_screen_displayables.rpy:697
translate russian imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "Изображение idle используется для фона карты-изображения, для ненаведённых или невыбранных кнопок с горячими точками и для пустой части ненаведённой полоски."

# game/tutorial_screen_displayables.rpy:703
translate russian imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "Изображений hover используется наведёнными горячими точками, но не выбранными и пустой частью наведённой полоски."

# game/tutorial_screen_displayables.rpy:705
translate russian imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "Заметьте, как подсвечены полоска и кнопка на этом изображении. Когда мы покажем их частью экрана, только один из них может быть показан на экране."

# game/tutorial_screen_displayables.rpy:711
translate russian imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "Выбранные изображения типа selected_idle используются заполненными частями полоски и выбранными кнопками, как на данном экране, а также выбранными кнопками."

# game/tutorial_screen_displayables.rpy:717
translate russian imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "А вот картинка с selected_hover. Здешняя кнопка никогда не будет показываться, так как её невозможно посчитать выбранной."

# game/tutorial_screen_displayables.rpy:723
translate russian imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "И наконец, изображение insensitive может быть дано, когда с горячей точкой невозможно взаимодействовать."

# game/tutorial_screen_displayables.rpy:728
translate russian imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "Карты-изображения не ограничиваются одними лишь изображениями. Любой объект может использовать там, где ожидается изображение."

# game/tutorial_screen_displayables.rpy:743
translate russian imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "Вот imagemap, построенный при помощи тех пяти картинок. Так как теперь это imagemap, вы можете с ним взаимодействоватьo."

# game/tutorial_screen_displayables.rpy:755
translate russian imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "Чтобы сделать код покороче, мы можем заменить пять изображений параметром auto, который автоматически заменяет '%%s' на 'idle', 'hover', 'selected_idle', 'selected_hover' или 'insensitive' соответственно."

# game/tutorial_screen_displayables.rpy:757
translate russian imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "Не стесняйтесь опускать выбранные (selected) и нечувствительные (insensitive) изображения, если в вашей игре они не нужны. Ren'Py воспользуется изображениями idle или hover для их замены."

# game/tutorial_screen_displayables.rpy:759
translate russian imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "Операторы hotspot и hotbar описывают область карты-изображения, которая должна будет рассматриваться как кнопка или полоса."

# game/tutorial_screen_displayables.rpy:761
translate russian imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "Оба оператора берут координаты области в формате (x, y, ширина, высота)."

# game/tutorial_screen_displayables.rpy:763
translate russian imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "Горячая точка (hotspot) применяет действие, когда её активируют. Также действия могут применяться, когда вы наводитесь на точку или отводитесь, прямо как в кнопке."

# game/tutorial_screen_displayables.rpy:765
translate russian imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "Горячая полоса (hotbar) берёт объект BarValue, описывающий, насколько полна полоса, и диапазон значений, показываемый полосой, прямо как в простой полосе (bar) и вертикальной полосе (vbar)."

# game/tutorial_screen_displayables.rpy:772
translate russian imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "Полезный для разработчика шаблон: определяем экран с картой-изображением, содержащей горячие точки, вместе с действием прыжка на метки, а затем вызываем этот экран при помощи оператора call screen."

# game/tutorial_screen_displayables.rpy:774
translate russian imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "Именно для этого мы и сделали тот пример со школой. Вот его код. Он длинный, но карта-изображение сама по себе очень простая."

# game/tutorial_screen_displayables.rpy:778
translate russian imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "У карт-изображений есть плюсы и минусы. С одной стороны, они просты для дизайнера и смотрятся очень неплохо, а с другой стороны, их бывает очень трудно переводить, и текст на изображениях может замыливаться при смене разрешения."

# game/tutorial_screen_displayables.rpy:780
translate russian imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "Всё зависит от вас и вашей команды: захотите ли вы использовать карты изображений в вашем проекте — решать вам."

# game/tutorial_screen_displayables.rpy:787
translate russian viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "Иногда вы хотите показать что-то большее по размеру, чем экран. Для этого и существует порт просмотра."

# game/tutorial_screen_displayables.rpy:803
translate russian viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "Вот пример простого порта просмотра, используемого для показа одного изображения, которое в разы больше экрана."
    e "Учитывая, что порт просмотра будет расширять размер экрана, мы воспользовались параметром xysize, чтобы сделать его меньше."

# game/tutorial_screen_displayables.rpy:805
translate russian viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "Без дополнительных настроек порт просмотра сдвигать нельзя, так что мы дали ему параметры draggable, mousewheel и arrowkeys, позволяя ему перемещаться самыми разными методами."

# game/tutorial_screen_displayables.rpy:820
translate russian viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "Когда я дала порту параметр edgescroll, порт автоматически прокручивается в определённом направлении, когда мышка достигает его краёв. Две цифры — это размер края и скорость перемещения в пикселях в секунду."

# game/tutorial_screen_displayables.rpy:839
translate russian viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "Дав порту просмотра параметр scrollbars, мы окружим его полосами прокрутки. Параметр scrollbars может принимать значения 'both', 'horizontal' и 'vertical'."

# game/tutorial_screen_displayables.rpy:841
translate russian viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "Параметр spacing контролирует пространство между портом и его полосами прокрутки в пикселях."

# game/tutorial_screen_displayables.rpy:864
translate russian viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "Параметры xinitial и yinitial устанавливают начальную зону изображения, от которой можно потом прокручиваться."

# game/tutorial_screen_displayables.rpy:885
translate russian viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "И наконец, есть параметр child_size. Чтобы объяснить, что он делает, сначала мне нужно показать, что случится, если его нет."

# game/tutorial_screen_displayables.rpy:887
translate russian viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "Как вы видите, текст вверху переносится. Это потому что Ren'Py предлагает тексту недостаточное для него пространство."

# game/tutorial_screen_displayables.rpy:909
translate russian viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "Когда мы даём экрану параметр child_size, он предлагает больше места всем своим дочерним объектам, разрешая прокручивание."
    e "Его аргументами выступают горизонтальный и вертикальный размеры. Если один из компонентов равняется None, то параметр берёт размер порта просмотра."

# game/tutorial_screen_displayables.rpy:936
translate russian viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "И последнее, существует объект vpgrid. Он комбинирует порт просмотра и таблицу в один объект, который оказывается эффективнее каждого из своих составляющих, так как таблица не позволяет прорисовывать каждый свой объект."

# game/tutorial_screen_displayables.rpy:938
translate russian viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "Объект берёт параметры cols и rows, отвечающие за колонки и строки. Если один из этих параметров пропущен, то Ren'Py определяет его значение из другого, плюс количества дочерних объектов."

translate russian strings:

    # tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "Общие параметры всех объектов."

    # tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "Добавление изображений и других объектов."

    # tutorial_screen_displayables.rpy:9
    old "Text."
    new "Текст."

    # tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "Коробки и другие поверхности."

    # tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "Окна и Рамки."

    # tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "Кнопки."

    # tutorial_screen_displayables.rpy:9
    old "Bars."
    new "Полоски."

    # tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "Порты просмотра."

    # tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "Карты-изображения."

    # tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "Достаточно на этом."

    # tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "Текст использует позиционные параметры."

    # tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "И мир перевернулся вверх дном..."

    # tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "Закрытие дренажных клапанов."

    # tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "Наддув."

    # tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "Зажигание."

    # tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "Есть контакт!"

    # tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "Ответ: [answer]."

    # tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "Текстовые теги в экранах {color=#c8ffc8}работают{/color}."

    # tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "Больше"

    # tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "Это экран."

    # tutorial_screen_displayables.rpy:402
    old "Okay"
    new "Ок"

    # tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "Вы кликнули на кнопку."

    # tutorial_screen_displayables.rpy:441
    old "Click me."
    new "Кликните на меня."

    # tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "Вы навелись на кнопку."

    # tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "Вы отвелись от кнопки."

    # tutorial_screen_displayables.rpy:470
    old "Heal"
    new "Лечиться"

    # tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "Это текстовая кнопка."

    # tutorial_screen_displayables.rpy:539
    old "Or me."
    new "Или на меня."

    # tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "Вы кликнули на другую кнопку."

    # tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "Этот текст больше, чем порт просмотра."

