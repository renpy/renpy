
# game/tutorial_screen_displayables.rpy:3
translate ukrainian screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "Існує досить багато екранів, що відображаються. Тут я розповім вам про деякі з найважливіших."

# game/tutorial_screen_displayables.rpy:11
translate ukrainian screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "Про що б ви хотіли дізнатися?" nointeract

# game/tutorial_screen_displayables.rpy:49
translate ukrainian screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "Є кілька властивостей, які мають спільні для кожної мови екрана. Ось я вам їх продемонструю."

# game/tutorial_screen_displayables.rpy:57
translate ukrainian screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "По-перше, кожна доступна мова екрана підтримує властивості позиції. Якщо контейнер, у якому знаходиться відображуваний, підтримує це, ви можете використовувати такі властивості, як align, anchor, pos тощо."

# game/tutorial_screen_displayables.rpy:69
translate ukrainian screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "Властивість at застосовує трансформацію до відображуваного так само, як це робить пропозиція at в операторі show."

# game/tutorial_screen_displayables.rpy:106
translate ukrainian screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "Властивість id здебільшого використовується з say screen, який використовується для показу діалогу. За межами скажімо екрану, він не використовується багато."

# game/tutorial_screen_displayables.rpy:108
translate ukrainian screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "Він повідомляє Ren'Py, які елементи відображення є фоновим вікном, 'who' говорить і 'what' говориться. Це використовувалося для застосування стилів для кожного символу та допомоги в режимі автоматичного пересилання."

# game/tutorial_screen_displayables.rpy:123
translate ukrainian screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "Властивість style дозволяє вказати стиль окремого відображуваного об'єкта."

# game/tutorial_screen_displayables.rpy:144
translate ukrainian screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "Властивість style_prefix встановлює префікс стилю, який використовується для відображуваного об'єкта та його дочірніх елементів."

# game/tutorial_screen_displayables.rpy:146
translate ukrainian screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "Наприклад, коли властивість style_prefix має значення 'green', vbox має стиль 'green_vbox', а текст у ньому — стиль 'green_text'."

# game/tutorial_screen_displayables.rpy:150
translate ukrainian screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "Існує ще кілька властивостей, а решту можна знайти в документації. Але це ті, які ви можете очікувати побачити у своїй грі, на екранах за замовчуванням."

# game/tutorial_screen_displayables.rpy:156
translate ukrainian add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "Іноді у вас буде відображуваний елемент, наприклад зображення, яке ви хочете додати на екран."

# game/tutorial_screen_displayables.rpy:165
translate ukrainian add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "Це можна зробити за допомогою оператора add, який додає зображення або інший відображуваний елемент на екран."

# game/tutorial_screen_displayables.rpy:167
translate ukrainian add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "Є кілька способів посилання на зображення. Якщо воно знаходиться в каталозі image або визначено оператором image, ви можете просто помістити його ім’я в лапки."

# game/tutorial_screen_displayables.rpy:176
translate ukrainian add_displayable_8ba81c26:

    # e "An image can also be referred to by its filename, relative to the game directory." id add_displayable_8ba81c26
    e "Зображення також можна посилатися за назвою файлу відносно каталогу гри." id add_displayable_8ba81c26

# game/tutorial_screen_displayables.rpy:185
translate ukrainian add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "Інші відображені елементи також можна додати за допомогою оператора add. Тут ми додаємо суцільний відображуваний елемент, що показує суцільний блок кольору."

# game/tutorial_screen_displayables.rpy:195
translate ukrainian add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "Окрім відображуваних, оператору add можна надати властивості трансформації. Вони можуть розміщувати або іншим чином трансформувати відображуваний, який додається."

# game/tutorial_screen_displayables.rpy:207
translate ukrainian add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "Звичайно, оператор add також може приймати властивість at, дозволяючи вам надати йому більш складне перетворення.."

# game/tutorial_screen_displayables.rpy:222
translate ukrainian text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "Оператор screen language text додає текст, який можна відобразити на екрані. Потрібен один аргумент, текст, який буде показано."

# game/tutorial_screen_displayables.rpy:224
translate ukrainian text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "На додаток до загальних властивостей, які мають усі відображувані елементи, текст має властивості стилю тексту. Наприклад, size встановлює розмір тексту."

# game/tutorial_screen_displayables.rpy:234
translate ukrainian text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "Відображуваний текст також може інтерполювати значення, вкладені в квадратні дужки."

# game/tutorial_screen_displayables.rpy:236
translate ukrainian text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement, variables defined in the screen take precedence over those defined outside it." id text_displayable_32d76ccb
    e "Коли текст відображається на екрані за допомогою оператора text, змінні, визначені на екрані, мають пріоритет над змінними, визначеними поза ним." id text_displayable_32d76ccb

# game/tutorial_screen_displayables.rpy:238
translate ukrainian text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "Ці змінні можуть бути параметрами, наданими екрану, визначеними операторами default або python, або встановленими за допомогою дії SetScreenVariable."

# game/tutorial_screen_displayables.rpy:247
translate ukrainian text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "Немає нічого, що можна більше сказати про текст на екранах, оскільки він працює так само, як і весь інший текст у Ren'Py."

# game/tutorial_screen_displayables.rpy:255
translate ukrainian layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "Відображувані елементи макета беруть інші відображувані елементи та розміщують їх на екрані."

# game/tutorial_screen_displayables.rpy:269
translate ukrainian layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "Наприклад, hbox displayable бере своїх дочірних і розміщує їх горизонтально."

# game/tutorial_screen_displayables.rpy:284
translate ukrainian layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "Vbox displayable схожий, за винятком того, що він бере своїх дочірніх елементів і розташовує їх вертикально."

# game/tutorial_screen_displayables.rpy:286
translate ukrainian layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "Обидва блоки приймають властивості стилю блоку, найкориснішим з яких є інтервал, кількість простору, який потрібно залишити між дочірніми елементами."

# game/tutorial_screen_displayables.rpy:301
translate ukrainian layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "Grid displayable відображає своїх дочірніх елементів у сітці клітинок однакового розміру. Він приймає два аргументи: кількість стовпців і кількість рядків."

# game/tutorial_screen_displayables.rpy:303
translate ukrainian layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "Сітка має бути заповнена, інакше Ren'Py видасть помилку. Зверніть увагу, як у цьому прикладі порожня клітинка заповнюється нулем."

# game/tutorial_screen_displayables.rpy:305
translate ukrainian layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "Подібно до прямокутників, сітка використовує властивість інтервалу, щоб визначити відстань між клітинками."

# game/tutorial_screen_displayables.rpy:321
translate ukrainian layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "Сітка також використовує властивість транспонування, щоб вона заповнювалася зверху вниз, перш ніж заповнюватися зліва направо."

# game/tutorial_screen_displayables.rpy:338
translate ukrainian layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "І щоб продемонструвати, що всі клітини однакові за розміром, ось що відбувається, коли один елемент більший за інших."

# game/tutorial_screen_displayables.rpy:353
translate ukrainian layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "Fixed displayable відображає дочірних за допомогою звичайного алгоритму розміщення Ren'Py. Це дає змогу розміщувати displayables де завгодно на екрані."

# game/tutorial_screen_displayables.rpy:355
translate ukrainian layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "За замовчуванням макет розгортається, щоб заповнити весь доступний для нього простір. Щоб запобігти цьому, ми використовуємо властивості xsize та ysize, щоб заздалегідь встановити його розмір."

# game/tutorial_screen_displayables.rpy:369
translate ukrainian layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "Коли displayable немакету надається два або більше дочірніх елементів, немає необхідності створювати fixed. Fixed додається автоматично, і до нього додаються дочірні елементи."

# game/tutorial_screen_displayables.rpy:384
translate ukrainian layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "І нарешті, є одна зручність для економії місця. Коли вкладено багато відображуваних елементів, додавання макета до кожного може спричинити божевільні рівні відступів."

# game/tutorial_screen_displayables.rpy:386
translate ukrainian layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "Оператор has створює макет, а потім додає до цього макета всіх подальших дочірніх елементів свого батька. Це просто зручність, щоб зробити екрани більш читабельними."

# game/tutorial_screen_displayables.rpy:395
translate ukrainian window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "У стандартному графічному інтерфейсі, який Ren'Py створює для гри, більшість елементів інтерфейсу користувача очікують певного фону."

# game/tutorial_screen_displayables.rpy:405
translate ukrainian window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "Без фону текст важко читати. Хоча рамка не обов’язкова, багато екранів мають одну або декілька з них."

# game/tutorial_screen_displayables.rpy:417
translate ukrainian window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "Але коли я додаю фон, це набагато простіше. Ось чому існує два відображувані елементи, призначені для надання фону елементам інтерфейсу користувача."

# game/tutorial_screen_displayables.rpy:419
translate ukrainian window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "Двома відображеннями є frame та window. Frame - це та, яку ми використовуємо вище, і вона розроблена, щоб забезпечити фон для довільних частин інтерфейсу користувача."

# game/tutorial_screen_displayables.rpy:423
translate ukrainian window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "З іншого боку, window displayable дуже специфічне. Він використовується для створення text window. Якщо ви читаєте те, що я кажу, ви зараз дивитеся на текстове вікно."

# game/tutorial_screen_displayables.rpy:425
translate ukrainian window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "Як рамкам, так і вікнам можна надати властивості window style, що дозволяє змінювати такі речі, як фон, поля та відступ навколо вікна."

# game/tutorial_screen_displayables.rpy:433
translate ukrainian button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "Одним із найбільш гнучких відображуваних елементів є button displayable, та її варіанти textbutton та imagebutton."

# game/tutorial_screen_displayables.rpy:443
translate ukrainian button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "Кнопка — це відображуваний об’єкт, який після вибору виконує дію. Кнопки можна вибирати клацанням миші, дотиком або за допомогою клавіатури та контролера."

# game/tutorial_screen_displayables.rpy:445
translate ukrainian button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "Дії можуть виконувати багато речей, наприклад встановлювати змінні, показувати екрани, переходити до мітки або повертати значення. У документації Ren'Py є багато {a=https://www.renpy.org/doc/html/screen_actions.html}дій{/a}, ви також можете написати власні."

# game/tutorial_screen_displayables.rpy:458
translate ukrainian button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "Також можна запускати дії, коли кнопка отримує або втрачає фокус."

# game/tutorial_screen_displayables.rpy:473
translate ukrainian button_displayables_47af4bb9:

    # e "A button takes another displayable as a child. Since that child can be a layout, it can take as many children as you want." id button_displayables_47af4bb9
    e "Кнопка приймає інший відображуваний елемент як дочірній. Оскільки цей дочірній елемент може бути макетом, він може прийняти скільки завгодно дочірніх елементів." id button_displayables_47af4bb9

# game/tutorial_screen_displayables.rpy:483
translate ukrainian button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "У багатьох випадках кнопкам буде надано текст. Щоб зробити це простіше, є textbutton, який приймає текст як аргумент."

# game/tutorial_screen_displayables.rpy:485
translate ukrainian button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "Оскільки textbutton displayable керує стилем тексту кнопки замість вас, саме така кнопка найчастіше використовується в графічному інтерфейсі за замовчуванням."

# game/tutorial_screen_displayables.rpy:498
translate ukrainian button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "Існує також кнопка imagebutton, яка приймає відображувані елементи, по одному для кожного стану, в якому може бути кнопка, і відображає їх як кнопку."

# game/tutorial_screen_displayables.rpy:500
translate ukrainian button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "Imagebutton дає вам найбільший контроль над тим, як виглядає кнопка, але її важче перекласти, і вона не виглядатиме так добре, якщо змінити розмір вікна гри."

# game/tutorial_screen_displayables.rpy:522
translate ukrainian button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "Кнопки мають властивості стилю вікна, які використовуються для визначення background, margins і padding. Вони також мають властивості кнопки, наприклад звук, який відтворюється при наведенні."

# game/tutorial_screen_displayables.rpy:524
translate ukrainian button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "При використанні з кнопкою, властивостям стилю можна надати префікси, як-от режим idle та hover, щоб змінити властивість разом із станом кнопки."

# game/tutorial_screen_displayables.rpy:526
translate ukrainian button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "Текстова кнопка також приймає властивості стилю тексту з префіксом тексту. Вони застосовуються до тексту, який відображається всередині."

# game/tutorial_screen_displayables.rpy:558
translate ukrainian button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "Звичайно, ми дуже рідко коли-небудь налаштовуємо кнопку на екрані так. Замість цього ми створили власні стилі та сказали Ren'Py використовувати їх."

# game/tutorial_screen_displayables.rpy:577
translate ukrainian bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "Відображувані панелі та vbar є гнучкими відображуваними елементами, які показують смужки, що представляють значення. Значення може бути статичним, анімованим або регулюватися гравцем."

# game/tutorial_screen_displayables.rpy:579
translate ukrainian bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "Властивість value дає BarValue, який є об’єктом, який визначає значення та діапазон стовпчика. Тут StaticValue встановлює діапазон до 100 і значення до 66, роблячи смужку заповненою на дві третини."

# game/tutorial_screen_displayables.rpy:581
translate ukrainian bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "Список усіх BarValues, які можна використовувати, можна знайти у {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}документації Ren'Py{/a}."

# game/tutorial_screen_displayables.rpy:583
translate ukrainian bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "У цьому прикладі ми надаємо frame властивість xsize. Якби ми цього не зробили, панель розширилася б, щоб заповнити весь доступний горизонтальний простір."

# game/tutorial_screen_displayables.rpy:600
translate ukrainian bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "Існує кілька різних стилів панелі, які визначені в графічному інтерфейсі за замовчуванням. Стилі вибираються властивістю style, а за замовчуванням вибирається значенням."

# game/tutorial_screen_displayables.rpy:602
translate ukrainian bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "Верхній стиль — стиль 'bar'. Він використовується для відображення значень, які гравець не може налаштувати, як-от індикатор життя чи прогресу."

# game/tutorial_screen_displayables.rpy:604
translate ukrainian bar_displayables_c2aa4725:

    # e "The middle style is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference." id bar_displayables_c2aa4725
    e "Середній стиль — це значення 'slider'. Він використовується для значень, які гравець, як очікується, налаштує, наприклад налаштування гучності." id bar_displayables_c2aa4725

# game/tutorial_screen_displayables.rpy:606
translate ukrainian bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "І нарешті, нижній стиль — це стиль 'scrollbar', який використовується для горизонтальних смуг прокручування. При використанні як смуги прокрутки великий палець у центрі змінює розмір, щоб відобразити видиму область вікна перегляду."

# game/tutorial_screen_displayables.rpy:623
translate ukrainian bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "Vbar displayable подібний до панелі displayable, за винятком того, що він використовує вертикальні стилі - 'vbar', 'vslider' і 'vscrollbar' - за замовчуванням."

# game/tutorial_screen_displayables.rpy:626
translate ukrainian bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "Смуги приймають властивості стилю смуги, які можуть значно налаштувати зовнішній вигляд і відчуття. Просто подивіться на різницю між стилями панелі, повзунка та смуги прокрутки."

# game/tutorial_screen_displayables.rpy:635
translate ukrainian imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "Карти зображень використовують два або більше зображень для відображення кнопок і смуг. Дозвольте почати з того, що покажу вам приклад карти зображень у дії."

# game/tutorial_screen_displayables.rpy:657
translate ukrainian swimming_405542a5:

    # e "You chose swimming."
    e "Ви вибрали плавання."

# game/tutorial_screen_displayables.rpy:659
translate ukrainian swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "Плавання здається дуже веселим, але я не взяла із собою купальник."

# game/tutorial_screen_displayables.rpy:665
translate ukrainian science_83e5c0cc:

    # e "You chose science."
    e "Ви вибрали науку."

# game/tutorial_screen_displayables.rpy:667
translate ukrainian science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "Я чула, що в деяких школах є конкурентоспроможна наукова команда, але для мене дослідження — це те, що не можна поспішати."

# game/tutorial_screen_displayables.rpy:672
translate ukrainian art_d2a94440:

    # e "You chose art."
    e "Ви вибрали мистецтво."

# game/tutorial_screen_displayables.rpy:674
translate ukrainian art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "По-справжньому якісне фонове зображення важко створити, тому в багатьох іграх використовуються відфільтровані фотографії. Можливо, ви зможете це змінити."

# game/tutorial_screen_displayables.rpy:680
translate ukrainian home_373ea9a5:

    # e "You chose to go home."
    e "Ви вирішили повернутися назад."

# game/tutorial_screen_displayables.rpy:686
translate ukrainian imagemap_done_48eca0a4:

    # e "Anyway..."
    e "Все одно..."

# game/tutorial_screen_displayables.rpy:691
translate ukrainian imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "Щоб продемонструвати, як складаються мапи зображень, я покажу вам п’ять зображень, які складають меншу карту зображень."

# game/tutorial_screen_displayables.rpy:697
translate ukrainian imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "Неактивне зображення використовується для фону карти зображення, для кнопок hotspot, які не виділені або не виділені, а також для порожньої частини несфокусованої панелі."

# game/tutorial_screen_displayables.rpy:703
translate ukrainian imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "Зображення при наведенні курсора використовується для hotspots, які виділені, але не виділені, а також для порожньої частини смуги фокусування."

# game/tutorial_screen_displayables.rpy:705
translate ukrainian imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "Зверніть увагу, як смуга і кнопка виділені на цьому зображенні. Коли ми відображаємо їх як частину екрана, лише один із них відображатиметься як виділений."

# game/tutorial_screen_displayables.rpy:711
translate ukrainian imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "Вибрані зображення, такі як це selected_idle image, використовуються для заповнених частин панелі та для вибраних кнопок, як-от поточний екран і позначений прапорець."

# game/tutorial_screen_displayables.rpy:717
translate ukrainian imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "Ось зображення selected_hover. Ця кнопка ніколи не буде показана, оскільки вона ніколи не буде позначена як вибрана."

# game/tutorial_screen_displayables.rpy:723
translate ukrainian imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "І нарешті, можна надати нечутливе зображення, яке використовується, коли з hotspot неможливо взаємодіяти."

# game/tutorial_screen_displayables.rpy:728
translate ukrainian imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "Мапи зображень не обмежуються лише зображеннями. Там, де очікується зображення, можна використовувати будь-який відображуваний."

# game/tutorial_screen_displayables.rpy:743
translate ukrainian imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "Ось мапа зображень, створена з використанням цих п’яти зображень. Тепер, коли це мапа зображення, ви можете взаємодіяти з нею, якщо хочете."

# game/tutorial_screen_displayables.rpy:755
translate ukrainian imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "Щоб зробити це трохи лаконічнішим, ми можемо замінити п’ять зображень на властивість auto, яка замінює '%%s' на 'idle', 'hover', 'selected_idle', 'selected_hover', або 'insensitive' відповідно."

# game/tutorial_screen_displayables.rpy:757
translate ukrainian imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "Не соромтеся пропускати вибрані та нечутливі зображення, якщо вони не потрібні вашій грі. Ren'Py використовуватиме неактивні або наведені зображення, щоб замінити їх."

# game/tutorial_screen_displayables.rpy:759
translate ukrainian imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "Оператори hotspot і hotbar описують області мапи зображення, які повинні працювати як кнопки або смуги відповідно."

# game/tutorial_screen_displayables.rpy:761
translate ukrainian imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "Обидва беруть координати області у форматі (x, y, ширина, висота)."

# game/tutorial_screen_displayables.rpy:763
translate ukrainian imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "Hotspot виконує дію, яка виконується, коли hotspot активовано. Він також може виконувати дії, які запускаються, коли на нього наводять і не наводять курсор, як і кнопка."

# game/tutorial_screen_displayables.rpy:765
translate ukrainian imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "Hotbar приймає об’єкт BarValue, який описує, наскільки заповнена смуга, і діапазон значень, які має відображати смужка, так само, як це роблять смуга та vbar."

# game/tutorial_screen_displayables.rpy:772
translate ukrainian imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "Корисним шаблоном є визначення екрана з мапою зображення, яка має hotspots, які переходять до міток, і виклик цього за допомогою оператора call screen."

# game/tutorial_screen_displayables.rpy:774
translate ukrainian imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "Це те, що ми зробили в шкільному прикладі, який я показала раніше. Ось скрипт для цього. Це довго, але сама мапа зображення досить проста."

# game/tutorial_screen_displayables.rpy:778
translate ukrainian imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "Мапи зображень мають плюси та мінуси. З одного боку, їх легко створити дизайнеру, і вони можуть виглядати дуже добре. У той же час їх може бути важко перекласти, а текст, вписаний у зображення, може бути розмитим під час масштабування вікна."

# game/tutorial_screen_displayables.rpy:780
translate ukrainian imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "Ви та ваша команда вирішуєте, чи підходять мапи зображень для вашого проєкту."

# game/tutorial_screen_displayables.rpy:787
translate ukrainian viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "Іноді вам захочеться показати щось більше, ніж екран. Ось для чого призначене viewport(вікно перегляду)."

# game/tutorial_screen_displayables.rpy:803
translate ukrainian viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "Ось приклад простого вікна перегляду, яке використовується для відображення одного зображення, яке значно перевищує розмір екрана. Оскільки вікно перегляду розширюється до розміру екрана, ми використовуємо властивість xysize, щоб зменшити його."

# game/tutorial_screen_displayables.rpy:805
translate ukrainian viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "За замовчуванням вікно перегляду не можна переміщувати, тому ми надаємо властивості перетягування(draggable), коліщатка миші та клавіш зі стрілками, щоб дозволити його переміщувати різними способами."

# game/tutorial_screen_displayables.rpy:820
translate ukrainian viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "Коли я надаю вікну перегляду(viewport) властивість edgescroll, вікно перегляду автоматично прокручується, коли миша знаходиться біля його країв. Два числа — це розмір країв і швидкість у пікселях за секунду."

# game/tutorial_screen_displayables.rpy:839
translate ukrainian viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "Надаючи вікну перегляду властивість scrollbars, воно оточується смугами прокручування. Властивість scrollbars може приймати значення 'both', 'horizontal' і 'vertical'."

# game/tutorial_screen_displayables.rpy:841
translate ukrainian viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "Властивість spacing контролює простір між вікном перегляду та його смугами прокрутки в пікселях."

# game/tutorial_screen_displayables.rpy:864
translate ukrainian viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "Властивості xinitial і yinitial встановлюють початкову величину прокручування як частку від величини, яку можна прокручувати."

# game/tutorial_screen_displayables.rpy:890
translate ukrainian viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "І нарешті, доступна для відображення vpgrid. Він поєднує вікно перегляду та сітку в єдиний відображуваний елемент, за винятком того, що він ефективніший, ніж обидва, оскільки йому не потрібно малювати кожного дочірнього елемента."

# game/tutorial_screen_displayables.rpy:892
translate ukrainian viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "Він приймає властивості cols і rows, які дають кількість рядків і стовпців дочірніх елементів. Якщо один пропущений, Ren'Py визначає його на основі іншого та кількості дочірніх."

translate ukrainian strings:

    # game/tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "Загальні властивості, які мають усі відображувані елементи."

    # game/tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "Додавання зображень та інших відображуваних матеріалів."

    # game/tutorial_screen_displayables.rpy:9
    old "Text."
    new "Текст."

    # game/tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "Коробки та інші макети."

    # game/tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "Вікна та рамки."

    # game/tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "Кнопки."

    # game/tutorial_screen_displayables.rpy:9
    old "Bars."
    new "Смуги."

    # game/tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "Вікна перегляду."

    # game/tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "Карти зображень."

    # game/tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "Це все, на даний момент."

    # game/tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "Це використовує властивості позиції."

    # game/tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "І світ перевернувся..."

    # game/tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "Тиск польоту в баках."

    # game/tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "На внутрішньому живленні."

    # game/tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "Запуск увімкнено."

    # game/tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "Зніміть!"

    # game/tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "Відповідь [answer]."

    # game/tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "Текстові теги {color=#c8ffc8}працюють{/color} на екранах."

    # game/tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "Більше"

    # game/tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "Це екран."

    # game/tutorial_screen_displayables.rpy:402
    old "Okay"
    new "Гаразд"

    # game/tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "Ви натиснули кнопку."

    # game/tutorial_screen_displayables.rpy:441
    old "Click me."
    new "Натисни на мене."

    # game/tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "Ви затримали кнопку."

    # game/tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "Ви відпустили кнопку."

    # game/tutorial_screen_displayables.rpy:470
    old "Heal"
    new "Вилікувати"

    # game/tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "Це textbutton."

    # game/tutorial_screen_displayables.rpy:539
    old "Or me."
    new "Або мене."

    # game/tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "Ви натиснули іншу кнопку."

