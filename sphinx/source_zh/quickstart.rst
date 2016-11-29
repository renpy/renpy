快速开始
==========

欢迎来到Ren'Py的快速开始手册。 这份手册是为了让你只需要几个简单步骤的拼凑就能创作出Ren'Py游戏。我们会展示怎样用拼凑的方法创作出 *The
Question*这样一款简单的游戏。这份手册包含着多个示例，同时也是示例游戏中的一部分。

翻译者：`Haitao(Kaitou)<https://github.com/HaitaoBio>`_

Ren'Py 启动器
-------------------


在你开始创作游戏之前，应该首先花点时间了解一下Ren'Py启动器是怎样运作的。启动器让你可以新建，管理，修改和运行Ren'Py游戏项目。

**开始入门** 你应该通过
`下载 Ren'Py<https://www.renpy.org/latest.html>`_
来开始入门.

当下载Ren'Py完毕，你可能会想解压缩它。对压缩包文件右键点击，选择"解压"选项或者"打开"选项就能够实现解压了。按照提示去做，就能得到 Ren'Py 的工作目录。

.. 注意::

    请确保你已经把解压缩至硬盘上所在的文件夹中(或目录中)。如果你尝试着在ZIP文件内运行它，可能会出现不能正常工作的问题。

当你把Ren'Py解压完毕后，你将要运行一下的程序。

* 在Windows系统上，运行``renpy``或者``renpy.exe``程序。
* 在Mac OS X系统上，运行``renpy``应用。
* 在Linux系统上，运行``renpy.sh``脚本。


运行之后，Ren'Py启动器应该就会运行。

Ren'Py启动器已经被多种语言翻译。要想改变界面语言，选择"preferences"并选择对应的语言。

.. image:: launcher.png
   :align: right

**选择并启动项目** 你最好先看一下完整的示例游戏
*The Question*是怎样的。通过启动Ren'Py
启动器，并在开始屏幕中选择"The Question"，选择
启动项目"来启动*The Question*游戏。

你可以用同样的方式回到Ren'Py demo，但要选择"Tutorial"而不是"The Question"。

**创建一个新项目**
从启动器中选择"Create New Project"来创建一个新项目。启动器会询问你为项目起的名称。因为
"The Question"这个名称已经被占用了，你应该输入其他不同的名称诸如
"My Question"这样的。接下来，启动器会询问你为项目选择一个颜色主题。在这一点上，你选择什么颜色主题是没有多大问题的，只要从显示出来的主题中选择即可。然后你就会返回到启动器的最初菜单，此时已经生成了你刚刚新建的游戏了。

一个简单的游戏示例
-------------

::

    label start:
        "I'll ask her..."

        "Me" "Um... will you..."
        "Me" "Will you be my artist for a visual novel?"

        "Silence."
        "She is shocked, and then..."

        "Sylvie" "Sure, but what is a \"visual novel?\""

这可能时最简单的Ren'Py游戏之一了。虽然这不包含任何的图片或者其他元素，但它展示了两个角色之间的对话了

你可以动手实践一遍，打开启动器，选择"My Question
Project"，并在 Edit File 一栏选择"script.rpy"这个脚本文件。Ren'Py会让你选择一个文本编辑器，然后会下载你所选择的文本编辑器。当下载完成后，script.rpy会在编辑器中打开。清除 script.rpy 中的所有内容,因为要从拼凑开始,不需要现成的这些东西。把上面的代码复制到 script.rpy 中，并保存。

到现在你已经可以准备运行这个示例项目了。回到启动器，并选择"Launch Project"。Ren'Py将会启动，注意,即使没有额外的工作，Ren'Py仍会给予你菜单以便于加载和保存游戏，并改变不同的偏好设置。准备好的话，点击"Launch Project"，就可以游玩这个示例游戏了。

这个示例游戏展示了一些常用的Ren'Py语句。

第一行是一个 label 语句。label语句用于给程序中的一段建立一个名称。在这个例子中，我们新建了 label 名称``start``. 这个 start label 比较特殊,用户在游戏主菜单中点击了"Start Game"后，这个Ren'Py脚本从这里开始运行。

另外一行是 say 语句，它具有两种形式。第一种是它自己本身是一行字符串 (由双引号开始，包含一连串的字符，并以双引号结束)，用于旁白和主角的内心想法。第二种时包含两组字符串。它用于对话，第一个字符串时角色的名字，第二个是角色说话的内容。

请留意所有的 say 语句都被缩进了四个空格的位置。这是因为它们都从属于 label 语句。在 Ren'Py 之中，
代码区块必须相对于优先语句进行缩进，而且，代码区快中的所有语句都必须以相同的宽度进行缩进。

如果字符串里面包含双引号这个字符，这个字符必须在前面添加一个反斜杠字符。示例中的最后一行就是这样做。

虽然这个简单的示例游戏看上去有些空洞，但这说明了在Ren'Py中做出什么东西来是多么简单。我们将会为其添加一点图片，但首先，让我们来了解一下如何声明角色。

Init
----

init 语句用于在脚本运行前执行一些 Ren'Py 语句的代码块。Init 区块被用于定义图像和角色，设置一些恒定的游戏数据结构，和定制 Ren'Py 。init
区块中的代码不应该与用户进行交互或者改变不同的层， 所以不应该包含 say, menu, scene, show, 或者 hide 语句, 和调用能实现类似功能的函数。

一个 init 语句由关键词 init 开始, 后面接着一个可选的表示优先度的数字，和一个必须写上的冒号. 如果优先度没有给定，会默认设置为0。优先度数字应该在-999到999之间的范围内。超过这个范围的数字会被反转。

优先度数字被用于确定在 init 区块中代码的执行时间。Init 区块会以优先度从低到高的顺序执行。在一个文件当中，具有相同优先度的 init 区块会以文件的顶部到底部的顺序执行。而文件间，拥有相同优先度的优先度区块的赋值顺序则是不确定的。

在特殊的 init 时期，所有 init 区块都只运行一次。 控制器运行到在普通执行中的 init 区块的结尾时，该区块的执行就结束了。如果 init 语句是在普通执行时遇到，init 区块就不能运行。取而代之的是，控制器跳过了下一个语句。

角色
----------

第一个示例中存在着一个问题，就是需要你不断重复地在每次角色说话前输入他们的名称。在一个大量对话的游戏里，就需要多次重复的输入。然而，所有角色名称子啊表现出来是都是一样的，所以输入这些重复文字真是无趣乏味。为了安排这些名称，Ren'Py 能让你以更佳的方式区定义角色。这就是用简称与名称相关联，并改变角色名称对应的显示颜色。

::

    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")

    label start:
        "I'll ask her..."

        m "Um... will you..."
        m "Will you be my artist for a visual novel?"

        "Silence."
        "She is shocked, and then..."

        s "Sure, but what is a \"visual novel?\""


第一行和第二行定义了角色。第一行定义了全名为"Sylvie"，缩略名为"s"的角色，并以偏绿色的颜色来显示(颜色是使用RGB十六位颜色编号，和网页用颜色编号是一样。)

第二行新建了一个全名为"Me"，缩略名为"m"的角色，并以偏红色的颜色来显示。更多其他角色可以通过复制这其中的一个角色定义的代码行，修改其缩略名，全名和颜色来进行定义。

我们也可以通过使用角色对象代替角色名称字符串来改变 say 语句。这命令 Ren'Py 去使用定义在 init 区块中已经定义好的角色。

图像
------

现在这个视觉小说还缺乏图像，显得比较单调。为我们的游戏加点图片吧。

::

    image bg meadow = "meadow.jpg"
    image bg uni = "uni.jpg"

    image sylvie smile = "sylvie_smile.png"
    image sylvie surprised = "sylvie_surprised.png"

    define s = Character('Sylvie', color="#c8ffc8")
    define m = Character('Me', color="#c8c8ff")

    label start:
        scene bg meadow
        show sylvie smile

        "I'll ask her..."

        m "Um... will you..."
        m "Will you be my artist for a visual novel?"

        show sylvie surprised

        "Silence."
        "She is shocked, and then..."

        show sylvie smile

        s "Sure, but what is a \"visual novel?\""


第一个新要点是定义图像，就像 init 区块中第2，3，5，6行中使用的 image 语句。这些 image 语句给定了图像名称和图片所在的文件名。

例如，第5行定义了一副图像，名称为 "sylvie smile"，能够根据为"sylvie_smile.png"的文件名来查找到该图像，并赋予名称为"sylvie"的标签。

在第12行，我们使用了 scene 语句. 这个语句会清除屏幕，并呈现 "bg meadow" 图像。下一行为 show 语句，它在屏幕上显示出"sylvie smile"图像。

image 名称的第一个部分是图像标签名。当屏幕上同时存在具有相同标签的多幅图像时，如果一张特定的图像被显现出来，这一幅图像会替换掉它们。第19行，也就是第二个 show 语句，就是这样的一个情况。在第19行运行之前，"sylvie smile"图像存在在屏幕上。当第19行运行后，图像就被替换成"sylvie surprised"的图像了，因为它们共享了便签"sylvie"。

为了能让 Ren'Py 能够查找到图像文件，图像文件需要被存放在当前项目的当前游戏目录中。游戏目录可以是"`Project-Name`/game/"，或者在启动器中点击"Game Directory"的按钮。 你可能会想复制"the_question/game/" 目录到"my_question/game/" 目录下，然后你就能运行这个示例了。

Ren'Py 不会区分人物立绘和背景，因为它们都被看做是图像。一般情况下，人物立绘会要求有透明部分，意味着需要以 PNG,WEBP 这些格式来储存。而背景就能以 JPEG, PNG, 或者 WEBP 文件格式储存。按照惯例，背景图像一般具有以"bg"开头的标签。

**Hide 语句。**
Ren'Py 同时也支持 hide 语句，用于隐藏给定的图像。

::

    label leaving:

        s "I'll get right on it!"

        hide sylvie

        "..."

        m "That wasn't what I meant!"

你需要用上 hide 语句的场合其实是很少。Show 语句能够在角色转换表情时用上，而 scene 语句用于所有人物立绘离开时。你只需要在保持当前背景但人物离开时使用 hide 语句即可。

过渡效果
-----------

简单地是图片弹出或者弹入其实是很枯燥突兀的，所以Ren'Py 实现了能让屏幕效果变得更加有趣的过渡效果。过渡改变了当前最后一次的交互(对话，菜单，或者过渡本身)的外观，变成执行 scene，show，hide语句后的外观效果。

::

    label start:
        scene bg uni
        show sylvie smile

        s "Oh, hi, do we walk home together?"
        m "Yes..."
        "I said and my voice was already shaking."

        scene bg meadow
        with fade

        "We reached the meadows just outside our hometown."
        "Autumn was so beautiful here."
        "When we were children, we often played here."
        m "Hey... ummm..."

        show sylvie smile
        with dissolve

        "She turned to me and smiled."
        "I'll ask her..."
        m "Ummm... will you..."
        m "Will you be my artist for a visual novel?"

with 语句调用了要使用的过渡的名称。最常见的是 ``dissolve`` 过渡效果，用于以溶解效果来切换到下一个场景。另一个很实用的过渡效果是 ``fade`` ，它能使屏幕图像渐变成黑色，再渐变为新的屏幕图像。

当把过渡放置在多个 scene，show 或者 hide
语句后时,会一次性地应用在多个语句上。当你这样写的话::

    ###
        scene bg meadow
        show sylvie smile
        with dissolve

"bg meadow"和"sylvie smiles"都会在同一时间出现溶解过渡效果。如果想让它们各自出现溶解效果，你需要两次写上这个语句::

    ###
        scene bg meadow
        with dissolve
        show sylvie smile
        with dissolve

第一个溶解效果出现在 meadow 中，然后第二个溶解效果出现在 sylvie 中。如果你想立即显现 meadow，然后再显现 sylvie，你可以这样写::

    ###
        scene bg meadow
        with None
        show sylvie smile
        with dissolve

在这里，None 关键词属于一种特殊的过渡效果，它告诉
Ren'Py前面的场景是什么，并且不向用户显示任何效果。

位置
---------

默认情况下，图片回忆水平居中显示，而且图片的底部会接触到屏幕的底部。这对于背景图片和单个角色是可以的，但场景里同时存在一个以上的角色时，就要考虑把他们放置在另一个位置了。为了故事剧情的需要，角色位置的变动是合情合理的。

::

   ###
        show sylvie smile at right

给 show 语句添加一个 at 从句就能做到位置的重排。at 从句调用位置参数，并且令图像显示在该位置上。Ren'Py 内置了多个预定义位置参数：``left`` 代表了屏幕左侧，``right`` 是右侧，``center`` 是水平居中(默认的)和 ``truecenter`` 代表着同时水平方向和垂直方向上的居中。

用户可以自定义位置参数，和基于事件的复杂移动，但这些超越了本快速入门的讨论范畴了。

音乐和声效
---------------

大多数游戏都会播放背景音乐。可以通过 play music
语句来控制音乐播放。你既可以给定一个表示文件名的字符串，也可以是一个包含多个文件名的列表。当给定的是列表时，将会按顺序地播放列表中的音乐。 ::

    ###
        play music "illurock.ogg"
        play music ["1.ogg", "2.ogg"]


你可以使用 fadeout 和 fadein 从句来控制音乐之间的切换。这样你就可以令到以隐出的方式结束旧的音乐，并以隐入的方式来进入新的音乐。 ::

    ###
        play music "illurock.ogg" fadeout 1.0 fadein 1.0

而且，当你使用了 loop 从句时，它就会循环播放。当你使用了 noloop 从句，它就不会循环播放。在 Ren'Py 中，音乐文件会自动地被不断循环播放，直到用户手动去暂停它。 ::

    ###
        play music "illurock.ogg" loop
        play music "illurock.ogg" noloop

可以使用 stop music 从句来停止音乐播放，也可以加上可选的的 fadeout 从句。 ::

    ###
        stop music

使用 play sound 语句可以播放声效。默认情况下这不会循环播放的。 ::

    ###
        play sound "effect.ogg"

play sound 语句和 play music 语句具有一些相同的从句可以搭配。

Ren'Py 支持多种声效和音乐文件格式，但其中，OGG 格式是最好的。就像图像文件，声效和音乐文件必须放置在游戏目录之中。

Pause 语句
---------------

pause 语句能够令 Ren'Py 暂停，直到点击鼠标后解除。 如果给定可选的表达式的话，而且是为数值的赋值的话，将会自动地在指定秒数后结束游戏暂停

结束游戏
---------------

你可以使用 return 语句来结束整个游戏，而且不需要调用任何东西。在结束之前，最好给游戏添加一些内容，来指示游戏将要结束，一般可能是一个表示结束用的数字或者结束用的名称。 ::

    ###
        ".:. Good Ending."

        return

以上就是制作一个动态小说所必不可少的东西。现在，让我们来了解一下游戏中展现菜单需要做什么。

菜单, 标签, 和跳转
-------------------------

menu 语句能够让你向玩家展示一组选项::

    ###
        s "Sure, but what's a \"visual novel?\""

    menu:
        "It's a story with pictures.":
             jump vn

        "It's a hentai game.":
             jump hentai

    label vn:
        m "It's a story with pictures and music."
        jump marry

    label hentai:
        m "Why it's a game with lots of sex."
        jump marry

    label marry:
        scene black
        with dissolve

        "--- years later ---"

这个示例展示了如何在 Ren'Py 中使用菜单功能。menu 语句开启了游戏内置菜单。而且 menu 语句占用了多个行组成的一个区块，每一行都以一个字符串和结尾的冒号组成。他们是向玩家展示的菜单选项。每一个菜单选项必须在后面带有一个或多个 Ren'Py 语句。当一个选项被选择时，跟随在其后面的语句就会被执行。

在这个例子中，每一个菜单选项都会执行 jump 语句。jump 语句会转移游戏控制器到对应的标签中，而这个标签时用 label 语句定义好的。然后，这个标签内的代码就会运行。

在上面的例子中，当 Sylvie 询问她问题之后，玩家面前出现了带有两个选项的菜单。如果玩家选择了"It's
a story with pictures.", 那第一个跳转就会被执行，控制器就会被跳转到 ``vn`` 标签。就会让主角说 "It's a story with pictures and music."，然后控制器转移到 ``marry`` 标签。

你可以在游戏目录下的多个文件里定义标签，然后以 .rpy 作为文件的拓展名。在 Ren'Py里，文件名不是很大问题, 只有在一个文件内存在多个标签时，要注意一个标签只能在一个文件里出现一次。

Python 和 If 语句
------------------------

当一个简单的 (又或者甚至时复杂的) 游戏能只用菜单和 jump 语句就能组成。有一点就变得很重要了，就是储存用户的选择在变量里，并可以在之后访问它们。这就是由  Ren'Py 的 python 语句所支持。

有两种方法去使用 Python。其一是，一行以美元符号来开头，这是单行 python 语句，其二是用"python:" 来引出一个 python 语句区块。

Python 语言使储存玩家输入变得简单。只要在游戏开始时初始化一下储存量::

    label start:
        $ bl_game = False

你可以在代码中实现菜单选择能够改变储存量的功能::

    label hentai:

        $ bl_game = True

        m "Why it's a game with lots of sex."
        s "You mean, like a boy's love game?"
        s "I've always wanted to make one of those."
        s "I'll get right on it!"

        jump marry

然后检查一下储存量::

        "And so, we became a visual novel creating team."
        "We made games and had a lot of fun making them."

        if bl_game:
            "Well, apart from that boy's love game she insisted on making."

        "And one day..."

当然，python 变量不一定是这么简单的真/假值。它可以使任意的 python 变量值。可以是储存玩家的名称，游戏分数，或者用于更多的用途。因为 Ren'Py 包含了 Python程序语言的所有功能，一切皆有可能。

发布你的游戏
-------------------

当你完成了一部游戏后，有一系列的事情需要你去做，以便于发布游戏:

**检查 Ren'Py 的新版本**
   新版本的 Ren'Py 是基于通常的基础版本，修复了bug和增加了新功能。在发布游戏之前，请使用启动器来把 Ren'Py 升级到最新版本。你也可以下载新版本并查看更新记录，在以下网站
   `http://www.renpy.org/latest.html <http://www.renpy.org/latest.html>`_.

**检查代码。**
   在启动器的首页中，选择 "Check Script
   (Lint)"。这会检查游戏中影响玩家的错误。这些错误可能会影响 Mac 和 Linux 平台上的玩家。所以这很重要，即使没有在你电脑上看到错误的报告。

**创建发行版**
   在启动器的首页中，选择 "Build Distributions". 基于 options.rpy 中包含的信息，启动器会创建一个或者多个包含你游戏本体的压缩包。

**测试。**
   Lint 不是全面测试的替代品。在发布之前检查游戏中的bug是你的责任。让你朋友去帮你玩游戏找bug，能找到你所不能找到的bug。

**发布。**
   你可以上传完成后的文件(基于 Windows, Mac, 和 Linux) 到网络上，然后告诉朋友哪里可以下载它。恭喜，你已经发布了你的游戏了！

   请你同时为 `games database <http://games.renpy.org>`_ 添加你已经发布的游戏，以便于我们能够追踪  Ren'Py 游戏。

The Question 的源代码
-----------------------

你可以查看 ''The Question'' 的完整代码 :ref:`here <thequestion>`.

接下来我们应该怎么做？
-------------------------

这篇快速开始仅仅就是介绍了 Ren'Py 的基础功能。因为要令教程尽量简单易懂，我们已经省略了很多 Ren'Py 提供的功能。要想了解 Ren'Py 的更多功能，我们强烈建议去玩一下 Tutorial，让 Eileen 告诉你更多功能。

你也可以阅读手册剩下的章节，那是 Ren'Py 的权威指南。

Ren'Py 网站里的 `FAQ <http://www.renpy.org/wiki/renpy/doc/FAQ>`_ 对于常见问题给出了答案，还有 `Cookbook <http://www.renpy.org/wiki/renpy/doc/cookbook/Cookbook>`_ 给出了一些有用的代码片段。如果你还有疑问，我们建议你在 `Lemma Soft Forums <http://lemmasoft.renai.us/forums/>`_提问，这是 Ren'Py 的官方论坛。也是 Ren'Py 社区的中心。我们欢迎新用户并乐意倾听他们的疑问。

最后衷心感谢你选择了 Ren'Py 视觉小说引擎。我们期待它能够帮助你创造出游戏作品！
