
# game/tutorial_screens.rpy:165
translate russian tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e "Экраны — одна из сильнейших сторон Ren'Py. Экраны позволяют изменять внеигровой интерфейс и создавать новые компоненты внутриигрового интерфейса."

# game/tutorial_screens.rpy:171
translate russian screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "Что вы хотите узнать об экранах?" nointeract

# game/tutorial_screens.rpy:201
translate russian screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e "Экраны — это наш метод создания пользовательского интерфейса в Ren'Py. За исключением изображений и переходов, всё, что вы видите, сделано благодаря экранам."

# game/tutorial_screens.rpy:203
translate russian screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e "Когда я говорю с вами, я использую экран 'say'. Он отвечает за диалог и отображение его игроку."

# game/tutorial_screens.rpy:205
translate russian screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "А когда мы используем оператор menu для отображения внутриигровых выборов, используется экран 'choice'. Понятно?" nointeract

# game/tutorial_screens.rpy:215
translate russian screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e "Ввод текста использует экран 'input', режим NVL использует экран 'nvl' и так далее."

# game/tutorial_screens.rpy:217
translate russian screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e "В игре может показываться больше одного экрана за раз. Например, кнопки внизу — Назад, История, Пропуск и т.д. — отображаются благодаря экрану quick_menu, который показывался вам всё это время."

# game/tutorial_screens.rpy:219
translate russian screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e "Есть ещё много особых экранов, таких как 'main_menu', 'load', 'save', и 'preferences'. Вместо того чтобы перечислять их всех, я {a=https://www.renpy.org/doc/html/screen_special.html}направлю вас на документацию{/a}."

# game/tutorial_screens.rpy:221
translate russian screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e "В только что созданном проекте все эти экраны находятся в файле screens.rpy. Там вы можете свободно их изменять."

# game/tutorial_screens.rpy:223
translate russian screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e "Впрочем, вы не ограничены одними только этими экранами. В Ren'Py вы можете делать собственные экраны, а затем использовать их в интерфейсе вашей игры."

# game/tutorial_screens.rpy:230
translate russian screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e "Например, для RPG-новеллы экран может показать основные параметры игрока."

# game/tutorial_screens.rpy:234
translate russian screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e "Кстати, мне нужно вас подлечить."

# game/tutorial_screens.rpy:241
translate russian screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e "Сложные экраны могут стать основой целой игровой механики. Например, такой экран может стать основой симулятора свидания или симулятора жизни."

# game/tutorial_screens.rpy:246
translate russian screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e "Несмотря на то, что экраны могут быть сложными, они всего лишь результат работы множества простых его составляющих, делающих из него нечто большее."

# game/tutorial_screens.rpy:265
translate russian screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."
    e "Вот пример очень простого экрана. Оператор screen говорит Ren'Py, что это экран, а его имя: simple_screen."

# game/tutorial_screens.rpy:267
translate russian screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e "Строки внутри экрана представляют объекты frame, vbox, text, и textbutton, или параметры типа action, xalign, и ypos."

# game/tutorial_screens.rpy:272
translate russian screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e "Я начну с составляющих частей оператора и опишу его, но прежде всего я покажу вам экран в действии."

# game/tutorial_screens.rpy:274
translate russian screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e "Оператор text используется для показа текста."

# game/tutorial_screens.rpy:276
translate russian screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e "Оператор textbutton представляет из себя текстовую кнопку, на которую можно кликнуть. Когда кнопка будет кликнута, то начнётся заявленное действие (action)."

# game/tutorial_screens.rpy:278
translate russian screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e "Оба этих оператора находятся внутри vbox (вертикальной коробки); внутри оператора, который кладёт текст на нашу кнопку."

# game/tutorial_screens.rpy:280
translate russian screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e "И всё это в рамке (frame), которая задаёт фон и границы. У рамки есть параметры at, которые трансформируют её, определяя её позицию."

# game/tutorial_screens.rpy:286
translate russian screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e "Существует три оператора отображения экрана."

# game/tutorial_screens.rpy:291
translate russian screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e "Первый — show screen, который показывает экран, а Ren'Py идёт дальше."

# game/tutorial_screens.rpy:293
translate russian screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e "Экран будет показываться, пока его не спрячут."

# game/tutorial_screens.rpy:297
translate russian screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e "Спрятать экран можно оператором hide screen."

# game/tutorial_screens.rpy:301
translate russian screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e "Оператор call screen останавливает Ren'Py при прохождении скрипта, пока экран либо не вернёт какое-либо значение, либо не прыгнет на какое-то другое место скрипта."

# game/tutorial_screens.rpy:303
translate russian screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e "Так как мы не сможем показать диалог вместе с этим оператором, вам придётся нажать 'Ок', чтобы продолжить обучение."

# game/tutorial_screens.rpy:310
translate russian screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e "Когда оператор call screen заканчивается, экран автоматически скрывается."

# game/tutorial_screens.rpy:312
translate russian screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e "В основном, вам пригодится show screen, чтобы показывать элементы, которые видны всё время, а call screen — чтобы показывать короткие интерактивные экраны."

# game/tutorial_screens.rpy:335
translate russian screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e "Вот пример экрана, берущего три параметра. Параметр message — это показываемое сообщение, а действия okay и cancel запускаются при нажатии соответствующих им кнопок."

# game/tutorial_screens.rpy:337
translate russian screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e "И хотя параметр сообщения нужно прописывать всегда, параметры okay и cancel — базовые значения, используемые, когда не задано никаких других аргументов."

# game/tutorial_screens.rpy:339
translate russian screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e "Каждый параметр — определённая переменная внутри экрана. В экране эти переменные имеют приоритет над всеми остальными переменными Ren'Py."

# game/tutorial_screens.rpy:343
translate russian screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e "При показе экрана для каждого параметра могут быть проставлены аргументы. Аргументы могут даваться по позиции или по имени параметра."

# game/tutorial_screens.rpy:350
translate russian screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e "Параметры позволяют нам изменять внешний вид экрана, попросту показав его с другими аргументами."

# game/tutorial_screens.rpy:357
translate russian screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e "При вызове экрана тоже можно применять аргументы, прямо как и при показе."

# game/tutorial_screens.rpy:369
translate russian screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e "Есть некоторые параметры, которые могут быть применены к самому экрану."

# game/tutorial_screens.rpy:380
translate russian screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e "Когда параметр modal имеет значение true, вы не можете взаимодейстовать с объектами за экраном. Поэтому сейчас вам надо нажать на 'Закрыть этот экран', чтобы мы смогли продолжить."

# game/tutorial_screens.rpy:398
translate russian screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e "Когда у экрана есть параметр tag, он рассматривается как часть имени изображения. Вот, это a_tag_screen."

# game/tutorial_screens.rpy:402
translate russian screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e "И теперь, когда я показала b_tag_screen, новый экран автоматически заменил старый tag_screen."

# game/tutorial_screens.rpy:404
translate russian screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e "Это очень полезно и в игровом, и в главном меню, когда нужно, чтобы экран загрузки сменял экран настроек, затем сменялся экраном помощи и так далее. Обычно, подобные экраны можно легко узнать по tag menu."

# game/tutorial_screens.rpy:408
translate russian screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e "По какой-то причине параметр tag берёт имя, а не выражение. И теперь слишком поздно что-то менять."

# game/tutorial_screens.rpy:432
translate russian screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e "Параметр zorder контролирует порядок наложения экранов друг на друга. Чем больше значение zorder, тем ближе экран к игроку."

# game/tutorial_screens.rpy:434
translate russian screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e "Стандартный экран имеет значение zorder 0. Когда два экрана имеют равное значение zorder, экран, показанный вторым, становится ближе к игроку."

# game/tutorial_screens.rpy:454
translate russian screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e "Параметр variant выбирает экран, основываясь на характеристиках вашего устройства."

# game/tutorial_screens.rpy:456
translate russian screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e "В этом примере первый экран будет показан, если у вас небольшое устройство (телефон), а второй при использовании планшетов, компьютеров и телевизоров."

# game/tutorial_screens.rpy:475
translate russian screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e "И наконец, параметр style_prefix определяет стиль экрана."

# game/tutorial_screens.rpy:477
translate russian screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e "Когда используется префикс 'red', рамка берёт стиль из 'red_frame', а текст, соответственно, из 'red_text'."

# game/tutorial_screens.rpy:479
translate russian screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e "Это может сохранить вам много времени, если вы собираетесь стилизовать экраны со множеством объектов."

# game/tutorial_screens.rpy:491
translate russian screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e "Язык экранов имеет несколько операторов, которые делают всё несколько иначе, чем при обычном показе объектов. Если вы ещё не видели тему {a=jump:warp_screen_displayables}Экранные Объекты{/a}, вы можете посмотреть сначала на них, а затем вернуться сюда."

# game/tutorial_screens.rpy:503
translate russian screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e "Операторы python работают здесь также, как и в обычном скрипте. Строка с Python-кодом начинается со знака доллара, плюс эта строка запускается каждый раз, как обновляется экран."

# game/tutorial_screens.rpy:518
translate russian screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e "Похожим образом оператор python начинает блок остальных операторов python. Но здесь есть одна большая разница между Python в экранах и Python в скрипте."

# game/tutorial_screens.rpy:520
translate russian screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e "В Python-экранах не разрешается иметь сторонние функции. Это значит, что в экране вы не сможете изменить значение переменной."

# game/tutorial_screens.rpy:522
translate russian screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e "Причина этому в том, что Ren'Py запускает экран, а в нём и Python, только во время алгоритма предсказания экрана."

# game/tutorial_screens.rpy:536
translate russian screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e "Оператор default позволяет вам установить первоначальное значение переменной экрана при его запуске. Это значение может быть изменено через действия SetScreenVariable и ToggleScreenVariable."

# game/tutorial_screens.rpy:538
translate russian screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e "Здешний default отличается от обычного в Python тем, что он запускается лишь единожды. Python запускается каждый раз при обновлении экрана, следовательно переменная не должна больше изменять своё значение."

# game/tutorial_screens.rpy:557
translate russian screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e "Оператор if работает как и в скрипте: запускаем один блок Если условие = Верно и второй Если условие = Неверно."

# game/tutorial_screens.rpy:572
translate russian screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e "Оператор for берёт список значений и проходит через них, запуская блок, в котором одна переменная привязывается к каждому значению в списке."

# game/tutorial_screens.rpy:588
translate russian screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e "Операторы on и key, вероятно, имеют смысл только при отображении над другими экранами."

# game/tutorial_screens.rpy:590
translate russian screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e "Оператор on создаёт экран, запускающийся при наступлении события. Событие 'show' происходит, когда экран впервые показывается, а событие 'hide' — когда он скрывается."

# game/tutorial_screens.rpy:592
translate russian screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e "Оператор key запускает событие, как только будет нажата клавиша 'a'."

# game/tutorial_screens.rpy:600
translate russian screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e "Язык экранов использует оператор, позволяющий вам включить один экран в другой (эффект экран-в-экране). Это может быть полезно, если вы хотите избавиться от разных дубликатов экранов."

# game/tutorial_screens.rpy:616
translate russian screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e "Возьмём, например, этот экран, показывающий два основных RPG параметра. В коде и так много дубликатов, а если мы возьмём ещё больше параметров, наш код будет просто чрезмерным."

# game/tutorial_screens.rpy:633
translate russian screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e "Держите, мы сместили операторы, показывающие текст и полоски, на второй экран и использовали оператор, включающий один экран в другой."

# game/tutorial_screens.rpy:635
translate russian screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e "Имена и значения параметров прописаны как аргументы второго экрана, прямо как если бы мы вызывали этот экран."

# game/tutorial_screens.rpy:637
translate russian screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e "Сделав всё таким образом, мы проконтролировали количество дубликатов и теперь можем изменять значения параметров из одного места."

# game/tutorial_screens.rpy:653
translate russian screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e "Оператор transclude заходит ещё дальше, позволяя оператору use брать целый блок операторов Языка Экранов."

# game/tutorial_screens.rpy:655
translate russian screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e "Когда экран доходит до оператора transclude, экран заменяется блоком, используемым оператором use."

# game/tutorial_screens.rpy:657
translate russian screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e "Экран boilerplate находится экран-в-экране, и текст из первого экрана переносится (трансклюкируется) на экран boilerplate."

# game/tutorial_screens.rpy:659
translate russian screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e "Операторы use и transclude — сложные, но очень мощные. Если вам вдруг интересно, 'use boilerplate' всего-лишь на один шаг отделяет вас от написания собственного оператора Языка Экранов."

translate russian strings:

    # tutorial_screens.rpy:26
    old " Lv. [lv]"
    new " Уровень [lv]"

    # tutorial_screens.rpy:29
    old "HP"
    new "ОЗ"

    # tutorial_screens.rpy:58
    old "Morning"
    new "Утро"

    # tutorial_screens.rpy:58
    old "Afternoon"
    new "Полдень"

    # tutorial_screens.rpy:58
    old "Evening"
    new "Вечер"

    # tutorial_screens.rpy:61
    old "Study"
    new "Учиться"

    # tutorial_screens.rpy:61
    old "Exercise"
    new "Тренироваться"

    # tutorial_screens.rpy:61
    old "Eat"
    new "Есть"

    # tutorial_screens.rpy:61
    old "Drink"
    new "Пить"

    # tutorial_screens.rpy:61
    old "Be Merry"
    new "Жениться"

    # tutorial_screens.rpy:107
    old "Strength"
    new "Сила"

    # tutorial_screens.rpy:111
    old "Intelligence"
    new "Интеллект"

    # tutorial_screens.rpy:115
    old "Moxie"
    new "Решимость"

    # tutorial_screens.rpy:119
    old "Chutzpah"
    new "Наглость"

    # tutorial_screens.rpy:171
    old "What screens can do."
    new "Что умеют экраны?"

    # tutorial_screens.rpy:171
    old "How to show screens."
    new "Как показать экран?"

    # tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new "Применение новых параметров к экранам."

    # tutorial_screens.rpy:171
    old "Screen properties."
    new "Настройки экранов."

    # tutorial_screens.rpy:171
    old "Special screen statements."
    new "Специальные операторы экранов."

    # tutorial_screens.rpy:171
    old "Using other screens."
    new "Использование других экранов."

    # tutorial_screens.rpy:171
    old "That's it."
    new "Достаточно."

    # tutorial_screens.rpy:205
    old "I do."
    new "Конечно."

    # tutorial_screens.rpy:331
    old "Hello, world."
    new "Привет, мир."

    # tutorial_screens.rpy:331
    old "You can't cancel this."
    new "Вы не можете это отменить."

    # tutorial_screens.rpy:346
    old "Shiro was here."
    new "Здесь были МихиРису."

    # tutorial_screens.rpy:362
    old "Click either button to continue."
    new "Нажмите на любую кнопку, чтобы продолжить."

    # tutorial_screens.rpy:377
    old "Close This Screen"
    new "Закрыть этот экран"

    # tutorial_screens.rpy:388
    old "A Tag Screen"
    new "Тег-экран A"

    # tutorial_screens.rpy:395
    old "B Tag Screen"
    new "Тег-экран B"

    # tutorial_screens.rpy:447
    old "You're on a small device."
    new "Вы на маленьком устройстве."

    # tutorial_screens.rpy:452
    old "You're not on a small device."
    new "Вы на большом устройстве."

    # tutorial_screens.rpy:466
    old "This text is red."
    new "Этот текст — красный."

    # tutorial_screens.rpy:496
    old "Hello, World."
    new "Привет, Мир."

    # tutorial_screens.rpy:510
    old "It's good to meet you."
    new "Приятно с тобой познакомиться."

    # tutorial_screens.rpy:534
    old "Increase"
    new "Увеличить"

    # tutorial_screens.rpy:563
    old "Earth"
    new "Земля"

    # tutorial_screens.rpy:563
    old "Moon"
    new "Луна"

    # tutorial_screens.rpy:563
    old "Mars"
    new "Марс"

    # tutorial_screens.rpy:581
    old "Now press 'a'."
    new "Теперь нажмите на английскую 'a'."

    # tutorial_screens.rpy:583
    old "The screen was just shown."
    new "Только что появился экран!"

    # tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new "Вы нажали на клавишу 'a'."

    # tutorial_screens.rpy:608
    old "Health"
    new "Здоровье"

    # tutorial_screens.rpy:613
    old "Magic"
    new "Магия"

    # tutorial_screens.rpy:644
    old "There's not much left to see."
    new "Не на что смотреть."

