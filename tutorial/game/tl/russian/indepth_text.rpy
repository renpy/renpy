
# game/indepth_text.rpy:22
translate russian text_578c4060:

    # e "Sometimes, when showing text, we'll want to change the way some of the text is displayed."
    e "Иногда, при показе текста, мы хотим изменить то, как он отображается."

# game/indepth_text.rpy:25
translate russian text_60750345:

    # e "For example, we might want to have text that is {b}bold{/b}, {i}italic{/i}, {s}struckthrough{/s}, or {u}underlined{/u}." ### english example
    e "Например, мы хотим сделать его {b}жирным{/b}, {i}курсивным{/i}, {s}зачёркнутым{/s}, {u}подчёркнутым{/u}…"

# game/indepth_text.rpy:27
translate russian text_5e1a6ee8:

    # e "That's what text tags are for."
    e "Для этого и существуют текстовые теги."

# game/indepth_text.rpy:31
translate russian text_38c63ec8:

    # e "Text tags are contained in braces, like the {{b} tag above. When a text tag takes a closing tag, the closing tag begins with a slash, like {{/b} does."
    e "Теги содержатся в фигурных скобках, как в теге {{b} выше. Когда тег нужно закрыть, мы закрываем его косой чертой вот {{/b} так."

# game/indepth_text.rpy:33
translate russian text_1760f9c8:

    # e "We've already seen the b, i, s, and u tags, but there are lot more than those. I'll show you the rest of them."
    e "Мы уже увидели теги b, i, s, и u, но их гораздо больше. Я покажу вам их."

# game/indepth_text.rpy:37
translate russian text_63f23b2f:

    # e "The a text tag {a=https://www.renpy.org}links to a website{/a}." ### english example
    e "Тег, {a=https://www.renpy.org}делающий ссылку на сайт{/a}."

# game/indepth_text.rpy:41
translate russian text_d22d5f4a:

    # e "The alpha text tag makes text {alpha=.5}translucent{/alpha}." ### english example
    e "Тег альфа делает текст {alpha=.5}полупрозрачным{/alpha}."

# game/indepth_text.rpy:45
translate russian text_7c2c3cd2:

    # e "The color text tag changes the {color=#0080c0}color{/color} of the text." ### english example
    e "Тег цвета изменяет {color=#0080c0}цвет{/color} текста."

# game/indepth_text.rpy:49
translate russian text_3f81fe7b:

    # e "The cps text tag {cps=25}makes text type itself out slowly{/cps}, even if slow text is off." ### english example
    e "Тег cps {cps=25}заставляет текст печататься в определённом темпе{/cps}, даже если текст у нас появляется моментально."

# game/indepth_text.rpy:51
translate russian text_b102941f:

    # e "The cps tag can also be relative to the default speed, {cps=*2}doubling{/cps} or {cps=*0.5}halving{/cps} it." ### english example
    e "Тег cps также может относительно изменять скорость текста, {cps=*2}удваивая{/cps} и {cps=*0.5}уполовинивая{/cps} его."

# game/indepth_text.rpy:56
translate russian text_22c4339a:

    # e "The font tag changes the font, for example to {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}." ### english example
    e "Тег font изменяет шрифт, например на {font=DejaVuSans-Bold.ttf}DejaVuSans-Bold.ttf{/font}."

# game/indepth_text.rpy:58
translate russian text_d43417d7:

    # e "Sometimes, changing to a bold font looks better than using the {{b} tag." ### english example
    e "Иногда лучше использовать жирный шрифт, чем тег {{b}."

# game/indepth_text.rpy:63
translate russian text_f24052f9:

    # e "The k tag changes kerning. It can space the letters of a word {k=-.5}closer together{/k} or {k=.5}farther apart{/k}." ### english example
    e "Тег k меняет кернинг текста. Он может {k=-.5}приблизить{/k} или {k=.5}отдалить{/k} символы друг от друга."

# game/indepth_text.rpy:68
translate russian text_2310b922:

    # e "The size tag changes the size of text. It can make text {size=+10}bigger{/size} or {size=-10}smaller{/size}, or set it to a {size=30}fixed size{/size}." ### english example
    e "Тег size изменяет размер текста. Например, сделав его {size=+10}больше{/size} или {size=-10}меньше{/size}, или установив ему {size=30}определённый размер{/size}."

# game/indepth_text.rpy:73
translate russian text_f566abf2:

    # e "The space tag {space=30} adds horizontal space in text.{vspace=30}The vspace tag adds vertical space between lines." ### english example
    e "Тег space {space=30} добавляет горизонтальный пропуск в тексте.{vspace=30}Тег vspace уже в вертикали, между строками."

# game/indepth_text.rpy:77
translate russian text_054b9ffa:

    # e "There are a few text tags that only makes sense in dialogue."
    e "Есть несколько текстовых тегов, имеющих смысл только в диалоге."

# game/indepth_text.rpy:81
translate russian text_86efc45b:

    # e "The p tag breaks a paragraph,{p}and waits for the player to click." ### english example
    e "Тег p переносит строку,{p}и ожидает клика игрока."

# game/indepth_text.rpy:83
translate russian text_3ece2387:

    # e "If it is given a number as an argument,{p=1.5}it waits that many seconds." ### english example
    e "Если его аргументом задаётся число,{p=1.5}он ждёт ровно такое число секунд."

# game/indepth_text.rpy:87
translate russian text_3881f72d:

    # e "The w tag also waits for a click,{w} except it doesn't break lines,{w=.5} the way p does." ### english example
    e "Тег w тоже ждёт клика,{w} впрочем, строку он не переносит,{w=.5} в отличие от p."

# game/indepth_text.rpy:92
translate russian text_e5321e79:

    # eslow "The nw tag causes Ren'Py to continue past slow text,{nw}" ### english example. next string is russian, lol
    eslow "Тег nw заставляет медленный текст{nw}"

# game/indepth_text.rpy:94
translate russian text_1f2697ba:

    # extend " to the next statement."
    extend " немедленно перейти к следующей строке кода."

# game/indepth_text.rpy:98
translate russian text_805fddbb:

    # e "To break a line without pausing,\none can write \\n, \\' and \\\" include quotes in the text."
    e "Чтобы перенести строку без пауз,\n вы можете написать \\n, \\' и \\\", включая скобки в тексте." ### доперевод

# game/indepth_text.rpy:103
translate russian text_ffdf7e76:

    # e "The interpolation feature takes a variable name in square brackets, and inserts it into text."
    e "Функция интерполяции берёт значение переменной в квадратных скобках и вставляет его в текст."

# game/indepth_text.rpy:109
translate russian text_fc99fcbf:

    # e "For example, this displays the [variable!t]." ### english example
    e "Например, так мы отобразим [variable!t]."

# game/indepth_text.rpy:113
translate russian text_15bfae8e:

    # e "When the variable name is followed by !q, special characters are quoted. This displays the raw [variable!q], including the italics tags." ### english example ### btw, set it to [variable!q!t] in original for translation measures
    e "Когда переменная дополняется !q, специальные символы не исключаются. Это позволяет показать чистое [variable!q!t] вместе с курсивными тегами."

# game/indepth_text.rpy:118
translate russian text_c90f24a8:

    # e "When the variable name is followed by !t, it is translated to [variable!t]. It could be something else in a different language." ### здесь должно быть translatable!t ### english example
    e "Когда переменная дополняется !t, она переводится в [translatable!t], то есть становится доступна для перевода через Ren'Py. Для других языков эта фраза может выглядеть иначе."

# game/indepth_text.rpy:121
translate russian text_fb106a95:

    # e "Finally, certain characters are special. [[, {{, and \\ need to be doubled if included in text. The %% character should be doubled if used in dialogue." ### english example
    e "И наконец, некоторые символы — специальные. [[, {{, и \\ должны дублироваться в коде. Символ %% — не исключение, но только если он используется в диалоге."

translate russian strings:

    # indepth_text.rpy:107
    old "{i}variable value{/i}"
    new "{i}значение переменной{/i}"

    # indepth_text.rpy:116
    old "translatable text"
    new "переводимый текст"

