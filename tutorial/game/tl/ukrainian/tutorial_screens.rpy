
# game/tutorial_screens.rpy:165
translate ukrainian tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e "Екрани є найпотужнішою частиною Ren'Py. Екрани дозволяють налаштовувати інтерфейс поза грою та створювати нові компоненти інтерфейсу в грі."

# game/tutorial_screens.rpy:173
translate ukrainian screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "Що б ви хотіли знати про екрани?" nointeract

# game/tutorial_screens.rpy:201
translate ukrainian screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e "Екрани — це те, як ми створюємо інтерфейс користувача в Ren'Py. За винятком зображень і переходів, усе, що ви бачите, надходить з екрана."

# game/tutorial_screens.rpy:203
translate ukrainian screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e "Коли я розмовляю з вами, я використовую екран 'say'. Він відповідає за ведення діалогу та представлення його гравцеві."

# game/tutorial_screens.rpy:207
translate ukrainian screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "І коли оператор меню відображає вибір у грі, використовується екран 'choice'. Зрозуміло?" nointeract

# game/tutorial_screens.rpy:215
translate ukrainian screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e "Для введення тексту використовується екран 'input', режим NVL використовує екран 'nvl' і так далі."

# game/tutorial_screens.rpy:217
translate ukrainian screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e "Одночасно можна відображати більше одного екрана. Наприклад, кнопки внизу - Назад, Історія, Пропустити тощо - відображаються на екрані швидкого меню, який відображається весь час."

# game/tutorial_screens.rpy:219
translate ukrainian screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e "Існує багато спеціальних екранів, наприклад 'main_menu', 'load', 'save' і 'preferences'. Замість того, щоб перераховувати їх усі тут, я {a=https://www.renpy.org/doc/html/screen_special.html}відправлю вас до документації{/a}."

# game/tutorial_screens.rpy:221
translate ukrainian screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e "У щойно створеному проєкті всі ці екрани находяться у screens.rpy. Ви можете редагувати цей файл, щоб змінити їх."

# game/tutorial_screens.rpy:223
translate ukrainian screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e "Ви також не обмежені цими екранами. У Ren'Py ви можете створювати власні екрани та використовувати їх для інтерфейсу вашої гри."

# game/tutorial_screens.rpy:230
translate ukrainian screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e "Наприклад, у рольовій грі, як-от візуальний роман, на екрані може відображатися статистика гравця."

# game/tutorial_screens.rpy:234
translate ukrainian screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e "Це нагадує мені, мабуть, що я мав би вас вилікувати."

# game/tutorial_screens.rpy:241
translate ukrainian screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e "Складні екрани можуть бути основою всієї ігрової механіки. Такий екран зі статистикою може бути основою для знайомств і симуляторів життя."

# game/tutorial_screens.rpy:246
translate ukrainian screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e "Хоча екрани можуть бути складними, насправді вони є лише результатом багатьох простих частин, які працюють разом, щоб створити щось більше, ніж усі вони."

# game/tutorial_screens.rpy:265
translate ukrainian screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and its name is simple_screen." id screens_showing_1b51e9a4
    e "Ось приклад дуже простого екрану. Інструкція screen використовується, щоб сказати Ren'Py, що це екран, і його назва simple_screen." id screens_showing_1b51e9a4

# game/tutorial_screens.rpy:267
translate ukrainian screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e "В операторі екрана рядки вводять відображувані елементи, такі як рамка, vbox, text і textbutton; або такі властивості, як action, xalign і ypos."

# game/tutorial_screens.rpy:272
translate ukrainian screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e "Я буду працювати зсередини, щоб описати твердження. Але спочатку я покажу екран, щоб ви могли побачити його в дії."

# game/tutorial_screens.rpy:274
translate ukrainian screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e "Оператор text використовується для відображення наданого тексту."

# game/tutorial_screens.rpy:276
translate ukrainian screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e "Оператор textbutton представляє кнопку, яку можна натиснути. Після натискання кнопки запускається відповідна дія."

# game/tutorial_screens.rpy:278
translate ukrainian screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e "Обидва знаходяться всередині vbox(вертикальне поле), оператора, який розміщує текст поверх кнопки."

# game/tutorial_screens.rpy:280
translate ukrainian screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e "І це всередині рамки(frame), яка забезпечує фон і межі. Рамка має властивість at, яка приймає перетворення, що вказує його положення."

# game/tutorial_screens.rpy:286
translate ukrainian screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e "Є три оператори, які використовуються для відображення екранів."

# game/tutorial_screens.rpy:291
translate ukrainian screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e "Перший — оператор show screen, який відображає екран і дозволяє Ren'Py продовжувати роботу."

# game/tutorial_screens.rpy:293
translate ukrainian screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e "Екран залишатиметься показаним, доки його не буде приховано."

# game/tutorial_screens.rpy:297
translate ukrainian screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e "Приховування екрана виконується оператором hide screen."

# game/tutorial_screens.rpy:301
translate ukrainian screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e "Оператор call screen зупиняє Ren'Py від виконання скрипту, доки екран не поверне значення або не перекине сценарій в інше місце."

# game/tutorial_screens.rpy:303
translate ukrainian screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e "Оскільки ми не можемо відобразити діалог одночасно, вам доведеться натиснути 'Ок', щоб продовжити."

# game/tutorial_screens.rpy:310
translate ukrainian screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e "Коли оператор call screen завершується, екран автоматично приховується."

# game/tutorial_screens.rpy:312
translate ukrainian screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e "Як правило, ви використовуєте show screen, щоб показувати елементи, які постійно активні, і call screen, щоб показувати екрани, з якими гравець взаємодіє деякий час."

# game/tutorial_screens.rpy:335
translate ukrainian screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e "Ось приклад екрана, який приймає три параметри. Параметр message — це повідомлення для показу, тоді як дії okay та cancel виконуються, коли натиснуто відповідну кнопку."

# game/tutorial_screens.rpy:337
translate ukrainian screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e "Хоча параметр повідомлення має надаватися завжди, параметри okay і cancel мають значення за замовчуванням, які використовуються, якщо аргумент не надано."

# game/tutorial_screens.rpy:339
translate ukrainian screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e "Кожен параметр є змінною, яка визначається на екрані. На екрані ці змінні мають пріоритет над тими, що використовуються в решті Ren'Py."

# game/tutorial_screens.rpy:343
translate ukrainian screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e "При показу екрана, для кожного з параметрів можна надати аргументи. Аргументи можна давати за позицію або за іменем."

# game/tutorial_screens.rpy:350
translate ukrainian screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e "Параметри дозволяють нам змінювати те, що відображає екран, просто повторно показуючи його з іншими аргументами."

# game/tutorial_screens.rpy:357
translate ukrainian screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e "Оператор call screen також може приймати аргументи, подібно до show screen."

# game/tutorial_screens.rpy:369
translate ukrainian screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e "Є кілька властивостей, які можна застосувати до самого екрана."

# game/tutorial_screens.rpy:380
translate ukrainian screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e "Коли параметр modal має значення true, ви не можете взаємодіяти з речами під екраном. Вам потрібно буде натиснути 'Закрити цей екран', перш ніж ви зможете продовжити."

# game/tutorial_screens.rpy:398
translate ukrainian screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e "Коли екран має параметр tag, він розглядається як частина тегу назви зображення. Тут я показую a_tag_screen."

# game/tutorial_screens.rpy:402
translate ukrainian screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e "Коли я показую b_tag_screen, він замінює a_tag_screen."

# game/tutorial_screens.rpy:404
translate ukrainian screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e "Це корисно в грі та головному меню, де потрібно, щоб екран завантаження замінив екран налаштувань. За замовчуванням усі ці екрани мають меню тегів."

# game/tutorial_screens.rpy:408
translate ukrainian screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e "Чомусь tag приймає назву, а не вираз. І змінювати це вже пізно."

# game/tutorial_screens.rpy:432
translate ukrainian screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e "Параметр zorder контролює порядок, у якому екрани накладаються один на одного. Чим більший номер порядку, тим ближче до гравця екран."

# game/tutorial_screens.rpy:434
translate ukrainian screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e "За замовчуванням екран має номер порядку 0. Якщо два екрани мають однаковий номер порядку, екран, який відображається другим, знаходиться ближче до гравця."

# game/tutorial_screens.rpy:454
translate ukrainian screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e "Параметр variant вибирає екран на основі властивостей пристрою, на якому він працює."

# game/tutorial_screens.rpy:456
translate ukrainian screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e "У цьому прикладі перший екран використовуватиметься для невеликих пристроїв, таких як телефони, а інший екран використовуватиметься для планшетів і комп’ютерів."

# game/tutorial_screens.rpy:475
translate ukrainian screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e "І нарешті, параметр style_prefix визначає префікс, який застосовується до стилів на екрані."

# game/tutorial_screens.rpy:477
translate ukrainian screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e "Якщо вказано префікс 'red', рамка отримує стиль 'red_frame', а текст отримує стиль 'red_text'."

# game/tutorial_screens.rpy:479
translate ukrainian screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e "Це може заощадити багато тексту під час оформлення екранів із багатьма відображуваними елементами."

# game/tutorial_screens.rpy:491
translate ukrainian screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e "Екранна мова має кілька операторів, які виконують інші дії, окрім показу відображуваних елементів. Якщо ви ще не бачили розділ {a=jump:warp_screen_displayables}Screen Displayables{/a}, можливо, ви захочете його перевірити, а потім поверніться сюди."

# game/tutorial_screens.rpy:503
translate ukrainian screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e "Оператор python працює приблизно так само, як і скрипт. Один рядок Python вводиться зі знаком долара. Цей рядок запускається кожного разу, коли екран оновлюється."

# game/tutorial_screens.rpy:518
translate ukrainian screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e "Подібним чином оператор python вводить блок операторів python із відступом. Але є одна велика різниця між Python на екранах і Python у скриптах."

# game/tutorial_screens.rpy:520
translate ukrainian screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e "Python, який ви використовуєте в екранах, не має побічних ефектів. Це означає, що він не може робити такі речі, як зміна значення змінної."

# game/tutorial_screens.rpy:522
translate ukrainian screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e "Причина цього полягає в тому, що Ren'Py запускатиме екран і Python у ньому під час прогнозування екрана."

# game/tutorial_screens.rpy:536
translate ukrainian screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e "Оператор default дозволяє встановити першопочаткове значення змінної екрана під час першого запуску екрана. Це значення можна змінити за допомогою дій SetScreenVariable і ToggleScreenVariable."

# game/tutorial_screens.rpy:538
translate ukrainian screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e "Оператор default відрізняється від оператора Python тим, що він виконується лише один раз. Python запускається кожного разу, коли екран оновлюється, і, отже, змінна ніколи не змінить значення."

# game/tutorial_screens.rpy:557
translate ukrainian screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e "Оператор if працює так само, як і в скрипті, запускаючи один блок, якщо умова істинна, а інший, якщо умова хибна."

# game/tutorial_screens.rpy:572
translate ukrainian screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e "Оператор for приймає список значень і перебирає їх, запускаючи блок усередині циклу for зі змінною, прив’язаною до кожного елемента списку."

# game/tutorial_screens.rpy:588
translate ukrainian screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e "Оператор on і key, ймовірно, мають сенс лише на верхньому рівні екрана."

# game/tutorial_screens.rpy:590
translate ukrainian screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e "Оператор on змушує екран виконувати дію, коли відбувається подія. Подія 'show' відбувається, коли екран вперше відображається, а подія 'hide' — коли він прихований."

# game/tutorial_screens.rpy:592
translate ukrainian screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e "Подія rey запускає подію при натисканні клавіші."

# game/tutorial_screens.rpy:600
translate ukrainian screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e "Мова екрану використовує оператор, який дозволяє включити екран в інший. Це може бути корисним для запобігання дублюванню на екранах."

# game/tutorial_screens.rpy:616
translate ukrainian screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e "Візьмемо, наприклад, цей екран, який показує два записи статистики. Там вже багато дублювання, і якби ми мали більше статистики, їх було б більше."

# game/tutorial_screens.rpy:633
translate ukrainian screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e "Тут ми перемістили оператори, які показують текст і панель, на другий екран, а оператор use включає цей екран на перший."

# game/tutorial_screens.rpy:635
translate ukrainian screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e "Ім'я та кількість статистики передаються як аргументи на екран, так само, як це робиться в операторі call screen."

# game/tutorial_screens.rpy:637
translate ukrainian screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e "Роблячи це таким чином, ми контролюємо кількість дублікатів і можемо змінювати статистику в одному місці."

# game/tutorial_screens.rpy:653
translate ukrainian screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e "Оператор transclude йде ще далі, дозволяючи оператору use взяти блок операторів мови екрана."

# game/tutorial_screens.rpy:655
translate ukrainian screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e "Коли включений екран досягає оператора transclude, він замінюється блоком із оператора use."

# game/tutorial_screens.rpy:657
translate ukrainian screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e "Екран boilerplate включено в перший, а текст з першого екрана переміщається в екран boilerplate."

# game/tutorial_screens.rpy:659
translate ukrainian screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e "Use та transclude складні, але дуже потужні. Якщо ви подумаєте про це, 'use boilerplate' — це лише один крок від написання власної мови екрана."

translate ukrainian strings:

    # game/tutorial_screens.rpy:26
    old " Lv. [lv]"
    new "Рівень [lv]"

    # game/tutorial_screens.rpy:29
    old "HP"
    new ""

    # game/tutorial_screens.rpy:58
    old "Morning"
    new "Ранок"

    # game/tutorial_screens.rpy:58
    old "Afternoon"
    new "День"

    # game/tutorial_screens.rpy:58
    old "Evening"
    new "Вечір"

    # game/tutorial_screens.rpy:61
    old "Study"
    new "Вчитися"

    # game/tutorial_screens.rpy:61
    old "Exercise"
    new "Тренуватися"

    # game/tutorial_screens.rpy:61
    old "Eat"
    new "Ї'сти"

    # game/tutorial_screens.rpy:61
    old "Drink"
    new "Пити"

    # game/tutorial_screens.rpy:61
    old "Be Merry"
    new "Одружитися"

    # game/tutorial_screens.rpy:107
    old "Strength"
    new "Сила"

    # game/tutorial_screens.rpy:111
    old "Intelligence"
    new "Інтелект"

    # game/tutorial_screens.rpy:115
    old "Moxie"
    new "Рішучість"

    # game/tutorial_screens.rpy:119
    old "Chutzpah"
    new "Нахабство"

    # game/tutorial_screens.rpy:171
    old "What screens can do."
    new "Що можуть екрани."

    # game/tutorial_screens.rpy:171
    old "How to show screens."
    new "Як показувати екрани."

    # game/tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new "Передача параметрів на екрани."

    # game/tutorial_screens.rpy:171
    old "Screen properties."
    new "Властивості екрана."

    # game/tutorial_screens.rpy:171
    old "Special screen statements."
    new "Спеціальні оператори екрана."

    # game/tutorial_screens.rpy:171
    old "Using other screens."
    new "Використання інших екранів."

    # game/tutorial_screens.rpy:171
    old "That's it."
    new "Досить."

    # game/tutorial_screens.rpy:205
    old "I do."
    new "Звісно."

    # game/tutorial_screens.rpy:331
    old "Hello, world."
    new "Привіт, світ."

    # game/tutorial_screens.rpy:331
    old "You can't cancel this."
    new "Ви не можете це скасувати."

    # game/tutorial_screens.rpy:346
    old "Shiro was here."
    new "Широ був тут."

    # game/tutorial_screens.rpy:362
    old "Click either button to continue."
    new "Натисніть будь-яку кнопку, щоб продовжити."

    # game/tutorial_screens.rpy:377
    old "Close This Screen"
    new "Закрити цей екран"

    # game/tutorial_screens.rpy:388
    old "A Tag Screen"
    new "Екран тегів A"

    # game/tutorial_screens.rpy:395
    old "B Tag Screen"
    new "Екран тегів B"

    # game/tutorial_screens.rpy:447
    old "You're on a small device."
    new "Ви на маленькому пристрій."

    # game/tutorial_screens.rpy:452
    old "You're not on a small device."
    new "Ви не на маленькому пристрої."

    # game/tutorial_screens.rpy:466
    old "This text is red."
    new "Цей текст червоного кольору."

    # game/tutorial_screens.rpy:496
    old "Hello, World."
    new "Привіт, Світ."

    # game/tutorial_screens.rpy:510
    old "It's good to meet you."
    new "Приємно познайомитися."

    # game/tutorial_screens.rpy:534
    old "Increase"
    new "Збільшити"

    # game/tutorial_screens.rpy:563
    old "Earth"
    new "Земля"

    # game/tutorial_screens.rpy:563
    old "Moon"
    new "Місяць"

    # game/tutorial_screens.rpy:563
    old "Mars"
    new "Марс"

    # game/tutorial_screens.rpy:581
    old "Now press 'a'."
    new "Тепер натисніть 'a'."

    # game/tutorial_screens.rpy:583
    old "The screen was just shown."
    new "Щойно появився екран."

    # game/tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new "Ви натиснули клавішу 'a'."

    # game/tutorial_screens.rpy:608
    old "Health"
    new "Здоров'я"

    # game/tutorial_screens.rpy:613
    old "Magic"
    new "Магія"

    # game/tutorial_screens.rpy:644
    old "There's not much left to see."
    new "Нічого дивитись."

