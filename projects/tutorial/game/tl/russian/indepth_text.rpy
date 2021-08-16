
# game/indepth_text.rpy:22
translate russian a_label_8d79d234:

    # e "You just clicked to jump to a label."
    e "Вы только что прыгнули на другую метку."

# game/indepth_text.rpy:28
translate russian text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e "Иногда, при показе текста, мы хотим изменить то, как он отображается."

# game/indepth_text.rpy:31
translate russian text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}."
    e "Например, мы хотим сделать его {b}жирным{/b}, {i}курсивным{/i}, {s}зачёркнутым{/s}, {u}подчёркнутым{/u}…"

# game/indepth_text.rpy:33
translate russian text_5e1a6ee8:

    # e "That's what text tags are for."
    e "Для этого и существуют текстовые теги."

# game/indepth_text.rpy:37
translate russian text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e "Теги содержатся в фигурных скобках, как в теге {{b} выше. Когда тег нужно закрыть, мы закрываем его косой чертой вот {{/b} так."

# game/indepth_text.rpy:39
translate russian text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e "Мы уже увидели теги b, i, s, и u, но их гораздо больше. Я покажу вам их."

# game/indepth_text.rpy:43
translate russian text_a620251f:

    # e "The a text tag can {a=https://www.renpy.org}link to a website{/a} or {a=jump:a_label}jump to a label{/a}."
    e "Тег a может {a=https://www.renpy.org}делать ссылку на сайт{/a} или {a=jump:a_label}прыгать на метки{/a}."

# game/indepth_text.rpy:49
translate russian after_a_label_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}."
    e "Тег альфа делает текст {alpha=.5}полупрозрачным{/alpha}."

# game/indepth_text.rpy:53
translate russian after_a_label_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text."
    e "Тег цвета изменяет {color=#0080c0}цвет{/color} текста."

# game/indepth_text.rpy:57
translate russian after_a_label_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off."
    e "Тег cps {cps=25}заставляет текст печататься в определённом темпе{/cps}, даже если текст у нас появляется моментально."

# game/indepth_text.rpy:59
translate russian after_a_label_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it."
    e "Тег cps также может относительно изменять скорость текста, {cps=*2}удваивая{/cps} и {cps=*0.5}уполовинивая{/cps} его."

# game/indepth_text.rpy:64
translate russian after_a_label_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."
    e "Тег font изменяет шрифт, например на {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."

# game/indepth_text.rpy:66
translate russian after_a_label_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag."
    e "Иногда лучше использовать жирный шрифт, чем тег {{b}."

# game/indepth_text.rpy:71
translate russian after_a_label_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}."
    e "Тег k меняет кернинг текста. Он может {k=-.5}приблизить{/k} или {k=.5}отдалить{/k} символы друг от друга."

# game/indepth_text.rpy:76
translate russian after_a_label_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}."
    e "Тег size изменяет размер текста. Например, делая его {size=+10}больше{/size} или {size=-10}меньше{/size}, или устанавливая ему {size=30}определённый размер{/size}."

# game/indepth_text.rpy:81
translate russian after_a_label_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines."
    e "Тег space {space=30} добавляет горизонтальный пропуск в тексте.{vspace=30}Тег vspace уже в вертикали, между строками."

# game/indepth_text.rpy:85
translate russian after_a_label_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e "Есть несколько текстовых тегов, имеющих смысл только в диалоге."

# game/indepth_text.rpy:89
translate russian after_a_label_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click."
    e "Тег p переносит строку,{p}и ожидает клика игрока."

# game/indepth_text.rpy:91
translate russian after_a_label_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds."
    e "Если его аргументом задаётся число,{p=1.5}он ждёт ровно такое число секунд."

# game/indepth_text.rpy:95
translate russian after_a_label_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does."
    e "Тег w тоже ждёт клика,{w} впрочем, строку он не переносит,{w=.5} в отличие от p."

# game/indepth_text.rpy:100
translate russian after_a_label_e5321e79:

    # eslow "The nw tag causes Ren'Py to continue past slow text,{nw}"
    eslow "Тег nw заставляет медленный текст{nw}"

# game/indepth_text.rpy:102
translate russian after_a_label_1f2697ba:

    # extend " to the next statement."
    extend " немедленно перейти к следующей строке кода."

# game/indepth_text.rpy:106
translate russian after_a_label_dbfca166:

    # e "To break a line without pausing,\none can write \\n. \\' and \\\" include quotes in the text."
    e "Чтобы перенести строку без пауз,\n вы можете написать \\n. \\' и \\\" позволяют писать кавычки в тексте."

# game/indepth_text.rpy:111
translate russian after_a_label_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e "Функция интерполяции берёт значение переменной в квадратных скобках и вставляет его в текст."

# game/indepth_text.rpy:117
translate russian after_a_label_fc99fcbf:

    # e "For example, this displays the [variable!t]."
    e "Например, так мы отобразим [variable!t]."

# game/indepth_text.rpy:121
translate russian after_a_label_c84d9087:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q!t], including the italics tags."
    e "Когда переменная дополняется !q, специальные символы не исключаются. Это позволяет показать чистое [variable!q!t] вместе с курсивными тегами."

# game/indepth_text.rpy:126
translate russian after_a_label_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language."
    e "Когда переменная дополняется !t, она переводится в [translatable!t], то есть становится доступна для перевода через Ren'Py. Для других языков эта фраза может выглядеть иначе."

# game/indepth_text.rpy:129
translate russian after_a_label_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue."
    e "И наконец, некоторые символы — специальные. [[, {{, и \\ должны дублироваться в коде. Символ %% — не исключение, но только если он используется в диалоге."

translate russian strings:

    # indepth_text.rpy:115
    old "{i}variable value{/i}"
    new "{i}значение переменной{/i}"

    # indepth_text.rpy:124
    old "translatable text"
    new "переводимый текст"

