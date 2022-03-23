
# game/tutorial_atl.rpy:205
translate russian tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "В этой части обучения, я расскажу вам, как Ren'Py позиционирует объекты на экране. Но до этого давайте немного узнаем об обработке чисел в Python."

# game/tutorial_atl.rpy:207
translate russian tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Python поддерживает два вида чисел — целые и дробные. Целое число состоит полностью из цифр, а дробные числа содержат точку."

# game/tutorial_atl.rpy:209
translate russian tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "Например, 100 — целое число, а 0.5 — дробное. При такой системе есть целых два нуля — целый 0, и дробный 0.0."

# game/tutorial_atl.rpy:211
translate russian tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Py использует целые числа для абсолютных координат, а дробные — для долей области с известными размерами."

# game/tutorial_atl.rpy:213
translate russian tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "Когда мы размещаем нечто на экране, областью обычно становится весь экран."

# game/tutorial_atl.rpy:215
translate russian tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "Позвольте мне уйти и я покажу вам, где распологаются некоторые позиции."

# game/tutorial_atl.rpy:229
translate russian tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "Верхний левый угол является основным. Это место, где xpos (положение по горизонтали) и ypos (положение по вертикали) равны нулю."

# game/tutorial_atl.rpy:235
translate russian tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "Когда мы увеличиваем xpos, мы движемся вправо. Значит, если xpos равен 0.5, мы находимся в середине экрана по горизонтали."

# game/tutorial_atl.rpy:240
translate russian tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "Увеличивая xpos до 1.0, мы переместимся к правому краю экрана."

# game/tutorial_atl.rpy:246
translate russian tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "Также мы можем использовать абсолютные значения xpos в пикселях, считая с левой стороны экрана. Например, если окно игры по ширине в 1280 пикселей, установив xpos на 640, мы вернём позицию на центр вершины экрана."

# game/tutorial_atl.rpy:248
translate russian tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "Вертикальная позиция (ypos) работает также. Сейчас у нас ypos 0.0."

# game/tutorial_atl.rpy:254
translate russian tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "Вот ypos 0.5."

# game/tutorial_atl.rpy:259
translate russian tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "И ypos равный 1.0 показывает самый низ экрана. Если вы посмотрите внимательно, вы увидите индикатор позиции под текстовым окном."

# game/tutorial_atl.rpy:261
translate russian tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "Как и xpos, ypos тоже может быть целым значением. В таком случае он представляет из себя число пикселей от верха экрана."

# game/tutorial_atl.rpy:267
translate russian tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "Сможете угадать, где находится эта позиция относительно экрана?" nointeract

# game/tutorial_atl.rpy:273
translate russian tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Простите, но это неверно. Здесь xpos = 0.75, ypos = 0.25."

# game/tutorial_atl.rpy:275
translate russian tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "Другими словами, 75%% пути слева и 25%% пути сверху."

# game/tutorial_atl.rpy:279
translate russian tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "Хорошая работа! Вы угадали позицию."

# game/tutorial_atl.rpy:283
translate russian tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "Простите, но это неверно. Здесь xpos = 0.75, ypos = 0.25."

# game/tutorial_atl.rpy:285
translate russian tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "Другими словами, 75%% пути слева и 25%% пути сверху."

# game/tutorial_atl.rpy:299
translate russian tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "Вторая позиция — якорь. Якорь — точка позиционирования нашего объекта."

# game/tutorial_atl.rpy:301
translate russian tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "Например, с xanchor = 0.0 и yanchor = 0.0 якорем будет служить верхний левый угол изображения."

# game/tutorial_atl.rpy:306
translate russian tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "Если мы увеличим xanchor до 1.0, якорем станет правый угол изображения."

# game/tutorial_atl.rpy:311
translate russian tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "Аналогичным образом, когда xanchor и yanchor равны 1.0, якорем становится нижний правый угол."

# game/tutorial_atl.rpy:318
translate russian tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "Для размещения изображения на экране, нам нужна как позиция, так и якорь."

# game/tutorial_atl.rpy:326
translate russian tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "Потом мы совмещаем их так, чтобы как позиция, так и якорь были на одной точке на экране."

# game/tutorial_atl.rpy:336
translate russian tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "Если мы разместим оба из них в левом верхнем углу, изображение переместится к левому верхнему углу экрана."

# game/tutorial_atl.rpy:345
translate russian tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "С правильной комбинацией позиции и якоря можно указать любое место на экране даже не зная размеров изображения."

# game/tutorial_atl.rpy:357
translate russian tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "Полезно бывает привести xpos и xanchor к одному значение. Мы называем это xalign, и он задаёт долевую позицию на экране."

# game/tutorial_atl.rpy:362
translate russian tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "Например, установив xalign в 0.0, мы можем выровнять объекты по левой стороне экрана."

# game/tutorial_atl.rpy:367
translate russian tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "В 1.0 — по правой."

# game/tutorial_atl.rpy:372
translate russian tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "А установив его на 0.5, мы вернёмся к центру экрана."

# game/tutorial_atl.rpy:374
translate russian tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "Параметр yalign работает похожим образом для вертикальной оси."

# game/tutorial_atl.rpy:376
translate russian tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "Помните, что используя xalign вы устанавливаете одинаковые значения xpos и xanchor, а с yalign — ypos и yanchor."

# game/tutorial_atl.rpy:381
translate russian tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "Параметры xcenter и ycenter позиционируют центр изображения. Сейчас мы поставили xcenter на .75, так что центр изображения находится в четверти от правой стороны экрана."

# game/tutorial_atl.rpy:386
translate russian tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "Разница между xalign и xcenter более очевидна, когда последнее становится равным 1.0, и половина изображения начинает выглядывать из края экрана."

# game/tutorial_atl.rpy:394
translate russian tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "Есть ещё параметры xoffset и yoffset, которые применяются после всех остальных и смещают объект вправо или вниз, соответственно."

# game/tutorial_atl.rpy:399
translate russian tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "Разумеется, вы можете использовать и отрицательные значения, так что смещение произойдёт влево и вверх."

# game/tutorial_atl.rpy:404
translate russian tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "И последним я упомяну о комбинированных параметрах, таких как align, pos, anchor и center. Align берёд две цифры и устанавливает сначала xalign, а затем yalign. Остальные параметры действуют похожим образом."

# game/tutorial_atl.rpy:411
translate russian tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "Как только вы разберётесь с позициями, вы сможете воспользоваться трансформациями для перемещения объектов на экранэ."

# game/tutorial_atl.rpy:418
translate russian tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "Ren'Py использует трансформации для анимирования, манипулирования и отображения изображений. Мы уже видели одну из простейших трансформаций, я сейчас снова вам её покажу…"

# game/tutorial_atl.rpy:425
translate russian tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "Трансформации могут быть очень простыми инструментами отображения изображений где-либо на экране. Такой трансформацией и является at right."

# game/tutorial_atl.rpy:429
translate russian tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "Но трансформации могут быть очень сложными и комплексными, представляющими и анимацию, и эффекты одновременно. Чтобы это продемонстрировать, устроим бесплатный рок-концерт!"

# game/tutorial_atl.rpy:437
translate russian tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "Сперва устроим... бесплатный рок-концерт!"

# game/tutorial_atl.rpy:445
translate russian tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "Мы приложили к этому концерту много усилий, но всё здесь состоит из небольших частей."

# game/tutorial_atl.rpy:447
translate russian tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "Большинство трансформаций в Ren'Py построено на Языке Анимаций и Трансформаций, сокращённо — ATL."

# game/tutorial_atl.rpy:449
translate russian tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "ATL может использоваться в Ren'py в трёх местах."

# game/tutorial_atl.rpy:454
translate russian tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "Первое место, где можно использовать ATL — частью оператора image. Вместо отображаемого объекта, изображение можно определить как блок кода ATL."

# game/tutorial_atl.rpy:456
translate russian tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "Если мы используем ATL таким образом, нам нужно включить в него отображаемые объекты."

# game/tutorial_atl.rpy:461
translate russian tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "Второй способ — использование оператора трансформации. Он присвоит блок ATL переменной Python, что позволит использовать его в условиях at и внутри других трансформации."

# game/tutorial_atl.rpy:473
translate russian tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "Наконец, блок ATL можно использовать как часть оператора show, вместо условия at."

# game/tutorial_atl.rpy:480
translate russian tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though your click stopped the motion, the image remains in the same place."
    e "Когда ATL используется как часть оператора show, значения параметров сохраняются даже при изменении трансформации. Так что даже после остановки анимации картинка всего-лишь чуть-чуть сместилась вниз со своей последней позиции."

# game/tutorial_atl.rpy:488
translate russian tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "Ключом к ATL является то, что он создаётся из относительно простых команд, но их можно сочетать для создания сложных трансформаций."

# game/tutorial_atl.rpy:490
translate russian tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "До того, как я начну объяснять вам как работает ATL, позвольте объяснить, что такое анимации и трансформации."

# game/tutorial_atl.rpy:495
translate russian tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "Анимация — изменение показываемого объекта. Например, прямо сейчас я изменяю своё выражение лица."

# game/tutorial_atl.rpy:522
translate russian tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "Трансформация — передвижение или изменение изображения. Например, размещение его на экране, масштабирование, вращение, изменение прозрачности…"

# game/tutorial_atl.rpy:530
translate russian tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "Для введения в ATL, начнём с простой анимации. Вот анимация, состоящая из пяти строк кода ATL, содержащаяся внутри оператора image."

# game/tutorial_atl.rpy:532
translate russian tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "Изменение отображаемого объекта осуществляется упоминанием его на строке ATL-кода. Здесь мы меняем два изображения туда-обратно."

# game/tutorial_atl.rpy:534
translate russian tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "Так как мы определяем новое изображение, первая строчка ATL должна использоваться для создания объекта. В противном случае, нечего было бы показывать."

# game/tutorial_atl.rpy:536
translate russian tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "Вторая и четвёртая строка в блоке — операторы паузы, заставляющие ATL подождать половину секунды, прежде чем продолжить цикл. Так мы задаём задержку между изображениями."

# game/tutorial_atl.rpy:538
translate russian tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "Последняя строка — оператор repeat. Он перезапускает текущий блок ATL. В одном блоке ATL может быть лишь один оператор repeat."

# game/tutorial_atl.rpy:543
translate russian tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "Мы также могли бы написать, например, repeat 2. Тогда анимация бы повторилась дважды и остановилась."

# game/tutorial_atl.rpy:548
translate russian tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "Если оператор repeat не добавлять, анимация прекратится по достижении конца блока ATL."

# game/tutorial_atl.rpy:554
translate russian tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "По умолчанию, отображаемые объекты заменяются сразу же. Мы также можем использовать условие with для создания перехода между объектами."

# game/tutorial_atl.rpy:561
translate russian tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "После конца анимации мы посмотрим, как ATL может трансформировать изображения, и начнём мы с того, что поместим одно из них на экран."

# game/tutorial_atl.rpy:570
translate russian tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "Простейшее из того, что мы можем сделать — статично разместить изображение. Это делается при помощи вызова позиционных параметров вместе со значениями."

# game/tutorial_atl.rpy:575
translate russian tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "С некоторыми другими операторами мы можем перемещать объекты по экрану."

# game/tutorial_atl.rpy:577
translate russian tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "Этот пример размещает изображение в правом верхнем углу и ждёт секунду. Затём изображение передвигается в левый угол, ждёт ещё одну секунду и повторяет цикл."

# game/tutorial_atl.rpy:579
translate russian tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "Операции pause и repeat — те же, что мы использовали в анимации. Они работают в любом коде ATL."

# game/tutorial_atl.rpy:584
translate russian tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "Однако изображение, прыгающее по экрану, не очень полезно. Поэтому ATL поддерживает интерполяцию."

# game/tutorial_atl.rpy:586
translate russian tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "Интерполяция позволяет плавно изменять значение трансформации от старого к новому."

# game/tutorial_atl.rpy:588
translate russian tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "В данном примере оператор интерполяции у нас на второй строке кода ATL. Он начинается с имени функции времени (linear)."

# game/tutorial_atl.rpy:590
translate russian tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "После этого следует количество времени, в нашем случае — три секунды. Он заканчивается списком свойств, и их новых значений."

# game/tutorial_atl.rpy:592
translate russian tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "Значение каждого параметра интерполируется исходя из их начального значения и вплоть до значений конечного оператора. Интерполяция происходит раз в кадр, позволяя нам делать плавную анимацию."

# game/tutorial_atl.rpy:603
translate russian tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL поддерживает более сложные виды движений, например, круговое. Но я их вам не покажу."

# game/tutorial_atl.rpy:607
translate russian tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "Кроме объектов, пауз, интерполяций и повторов, мы можем использовать в ATL ещё несколько операторов."

# game/tutorial_atl.rpy:619
translate russian tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "Трансформации ATL, созданные операторами, сами по себе являются операторами ATL. Учитывая, что базовые позиции — это тоже трансформации, мы можем использовать left, right и center внутри блока ATL."

# game/tutorial_atl.rpy:635
translate russian tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "Здесь мы имеем два новых оператора. Оператор block позволяет вам создавать новый блок внутри кода ATL. Учитывая, что оператор repeat применяется именно к блоками, это позволяет вам повторить только часть трансформации."

# game/tutorial_atl.rpy:637
translate russian tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "Также у нас есть оператор time, который запускается после заданного времени с начала блока. Он запустится, даже при запуске другого оператора, таким образом останавив его действие."

# game/tutorial_atl.rpy:639
translate russian tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "Таким образом этот пример перемещается туда-сюда в течение 11.5 секунд, а затем передвигается в правый угол экрана."

# game/tutorial_atl.rpy:653
translate russian tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "Оператор parallel позволяет нам запускать два блока ATL одновременно."

# game/tutorial_atl.rpy:655
translate russian tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "В нашем случае, верхний блок передвигает объект по горизонтали, а нижний по вертикали. Учитывая, что движутся они с разными скоростями, всё выглядит так, будто картинка отскакивает от стенок экрана."

# game/tutorial_atl.rpy:669
translate russian tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "И наконец, оператор choice позволяет Ren'Py выбрать, использовать ли блок ATL. Это позволяет вам добавить несколько вариантов того, что может быть показано игрокy."

# game/tutorial_atl.rpy:675
translate russian tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "Эта обучающая игра учит только самым основам ATL. Например, мы даже ещё не притронулись к операторам on и event. Чтобы узнать об ATL побольше, вы можете почитать {a=https://renpy.org/doc/html/atl.html}в документации главу про ATL{/a}."

# game/tutorial_atl.rpy:684
translate russian transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "У Ren'Py есть несколько параметров трансформаций, которые могут использоваться с ATL, объектом Transform и даже добавлять операторов Языка Экранов."

# game/tutorial_atl.rpy:685
translate russian transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "В данной секции мы покажем их, так что вы увидите их и поймёте, что они из себя представляют."

# game/tutorial_atl.rpy:701
translate russian transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "Начну сначала: все параметры позиций — это те же параметры трансформаций. Они включают параметры pos, anchor, align, center и offset."

# game/tutorial_atl.rpy:719
translate russian transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "Параметры позиций также можно использовать для панорамирования объектов, которые больше экрана, задавая им отрицательные значения xpos и ypos."

# game/tutorial_atl.rpy:729
translate russian transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "Параметр subpixel контролирует метод обработки масштабирования на экране. При False изображения будут писксель-идеальными, то есть не будут сглаживаться." ### неточно

# game/tutorial_atl.rpy:736
translate russian transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "При True объект становится сглаженней, но ценой небольшого размытия изображения."

# game/tutorial_atl.rpy:755
translate russian transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "Трансформации также поддерживают полярную систему координат. Параметр around устанавливает центр координатной системы на абсолютную позицию."

# game/tutorial_atl.rpy:763
translate russian transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "Параметр angle устанавливает значение угла в градусах. Угол поворачивается по часовой стрелке, где значением 0 является верх экрана."

# game/tutorial_atl.rpy:772
translate russian transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "Параметр radius определяет дистанцию от заданной позиции объекта до центра координат."

# game/tutorial_atl.rpy:786
translate russian transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "Есть несколько методов масштабирования объектов. Параметр zoom позволяет нам масштабировать объект по дробному числу, делая его больше или меньше."

# game/tutorial_atl.rpy:799
translate russian transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "Параметры xzoom и yzoom позволяют масштабировать объект уже отдельно по горизонтали и вертикали."

# game/tutorial_atl.rpy:809
translate russian transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "Приводя xzoom или yzoom к отрицательным значениям, мы можем отразить объект по горизонтали или вертикали."

# game/tutorial_atl.rpy:819
translate russian transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "Вместо того, чтобы зумить изображение по дробному числу, параметр size может промасштабировать объект до определённого размера."

# game/tutorial_atl.rpy:834
translate russian transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "Параметр alpha используется для изменения прозрачности объекта. Благодаря ему изображение можно выявить и испарить."

# game/tutorial_atl.rpy:847
translate russian transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "Параметр rotate вращает объект."

# game/tutorial_atl.rpy:858
translate russian transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "По стандарту, если объект вращается, Ren'Py добавляет ему дополнительное пространство, так что размер объекта не изменяется."
    e "Здесь вы видите, что несмотря на то, что объект мы поместили в угол, у него осталось свободное пространство."

# game/tutorial_atl.rpy:870
translate russian transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "Установив rotate_pad на False, мы можем избавиться от свободных пространств, но общий размер объекта будет постоянно изменяться."

# game/tutorial_atl.rpy:881
translate russian transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "Параметры tile — xtile и ytile — клонируют объект несколько раз."

# game/tutorial_atl.rpy:891
translate russian transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "Параметр crop обрезает объект, показывая только его часть."

# game/tutorial_atl.rpy:905
translate russian transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "Используясь вместе, crop и size могут сфокусироваться на определённой части изображения."

# game/tutorial_atl.rpy:917
translate russian transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "Параметры xpan и ypan могут использоваться для панорамирования объекта, давая ему определённый угол в градусах, где угол 0 будет центром изображения."

# game/tutorial_atl.rpy:924
translate russian transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "Это были все трансформации, с которыми мы работаем. Комбинируя их вместе и в правильном порядке, вы сможете создать очень сложные вещи."

translate russian strings:

    # tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"

