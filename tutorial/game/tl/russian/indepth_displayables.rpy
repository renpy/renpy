
# game/indepth_displayables.rpy:15
translate russian simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "В Ren'Py существует концепт \"Объекта\", который, как и изображение, можно показывать и скрывать."

# game/indepth_displayables.rpy:22
translate russian simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "Оператор image используется, чтобы объявлять имя объекта. Самый простой способ это сделать — дать объекту имя изображения."

# game/indepth_displayables.rpy:29
translate russian simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "Но это далеко не единственное, на что может ссылаться image. Когда в строке отсутствует точка, Ren'Py автоматически интерпретирует это, как ссылку на второе изображение."

# game/indepth_displayables.rpy:41
translate russian simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "Строка также может содержать цветовой код, использующий шестнадцатеричную систему счисления, прямо как цвета, используемые современными веб-браузерами."

# game/indepth_displayables.rpy:43
translate russian simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "Шесть цифр содержат по два числа значений оттенков красного, зелёного и синего, а при добавлении ещё двух — альфа-канала, то есть прозрачности."
    e "Также есть возможность сократить всё до трёх цифр, тогда, соответственно, только одна цифра будет кодировать каждый цвет, а четвёртая — прозрачность."

# game/indepth_displayables.rpy:53
translate russian simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "Объект Трансформация (Transform) берёт определённый объект и применяет к нему свои настройки."

# game/indepth_displayables.rpy:55
translate russian simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "Заметьте, раз трансформации нужен объект, она также может взять и изображение. Впрочем, трансформация может изменить любой объявленный здесь объект."

# game/indepth_displayables.rpy:63
translate russian simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "Существует более сложная форма функции Solid, которая будет брать параметры стиля. Эта форма позволяет нам изменить размер функции, так как иначе уже весь экран был бы синим."

# game/indepth_displayables.rpy:72
translate russian simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "Объект Текст (Text) позволяет Ren'Py показывать текст, как изображение."

# game/indepth_displayables.rpy:80
translate russian simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "Это означает, что мы можем применять к нему и другие объекты, так же как и к изображениям, например, трансформацию."

# game/indepth_displayables.rpy:91
translate russian simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "Объект Composite позволяет нам группировать разные объекты в один снизу вверх."

# game/indepth_displayables.rpy:101
translate russian simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "Некоторые объекты часто используются для настройки интерфейса Ren'Py, как это и происходит с объектом Frame. Этот объект Рамки берёт другой объект, а затем размеры своих границ слева, сверху, справа и снизу."

# game/indepth_displayables.rpy:111
translate russian simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "Объект Рамка расширяется или сжимается, чтобы влезть в собственные границы. Он делает это, масштабируя центр по граням и стороны по вертикали/горизонтали, в то время как его углы остаются неизменны."

# game/indepth_displayables.rpy:118
translate russian simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "Рамка также может чередовать себя своим содержимым, а не масштабироваться."

# game/indepth_displayables.rpy:126
translate russian simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "Хотя в абстрактном виде это и выглядит немного странно… зато когда у рамки появилась текстура, вы можете видеть, как мы масштабируем объекты."

# game/indepth_displayables.rpy:132
translate russian simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "Это всего лишь простейшие из объектов, которые очень часто используются напрямую."

# game/indepth_displayables.rpy:134
translate russian simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "Если вы разбираетесь в Python, то можете даже написать собственные объекты для мини-игр. Впрочем, для большинства визуальных новелл вышесказанного будет достаточно."

translate russian strings:

    # indepth_displayables.rpy:67
    old "This is a text displayable."
    new "Это текстовый объект."
