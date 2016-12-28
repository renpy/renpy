.. _atl:

=====================================
动画变换语言(Animation and Transformation Language)
=====================================

动画变换语言(Animation and Transformation LanguageATL)提供了一套应用于可显示对象的高级变换方法，包括显示，放置在视屏上和应用诸如旋转，缩放，透明度设置等变形效果。这些具体的变换可以随时间改变，也可以响应事件。

ATL transform对象在 Python 中是等价于函数 :func:`Transform` 返回的可显示对象。您无法使用其他的代码来创建ATLTransform对象。

Ren'Py 脚本语句
========================

ATL代码可以在三种 Ren'Py 脚本语句中使用。

.. _transform-statement:

transform 语句
-------------------

transform 语句用于定义一个 transform 对象，可以在at从句中使用。该命令的语法如下：

.. productionlist:: script
    atl_transform : "transform" `name` "(" `parameters` ")" ":"
                  :    `atl_block`

transform 命令必须在初始化时运行。如果它在 init 区块之外，会以优先度为0的情况下在程序初始化时运行。transform 对象可以带有一系列的参数，当调用它时提供相应的参数。

`Name` must be a python identifier. The transform created by the ATL block is
bound to this name.::

   transform left_to_right:
       xalign 0.0
       linear 2.0 yalign 1.0
       repeat

.. _atl-image-statement:

带 ATL 区块的 image 语句
------------------------------

ATL 的第二种用途就是被包含在 image 语句。您可以将一个 transform 对象绑定到一个图像名称上。因为无法向该命令提供参数，所以只有当这个 transform 对象定义为动画时，这么做才有意义。相关语法如下：

.. productionlist:: script
    atl_image : "image" `image_name` ":"
              :    `atl_block`

::

    image eileen animated:
        "eileen_happy.png"
        pause 1.0
        "eileen_vhappy.png"
        pause 1.0
        repeat


带 ATL 区块的 scene 和 show 语句
----------------------------------------

ATL 的最后一个用途是被包含在 scene 和 show 语句。这将把一张图像作为 ATL 变换的一部分使用。

.. productionlist:: script
    atl_scene : `stmt_scene` ":"
              :     `atl_block`
    atl_show  : `stmt_show` ":"
              :     `atl_block`


::

    scene bg washington:
        zoom 2.0

    show eileen happy:
        xalign 1.0


ATL 的语法与语义
========================

一个 ATL 区块由一行或几行的逻辑语句构成，前排缩进必须对齐，并且相对前一个语句缩进。每一个在 ATL 区块里的逻辑语句必须包含一句或更多的 ATL 语句。

ATL 语句分为简单的和复杂的两种：简单的 ATL 语句不带有一个 ATL 区块，包括一句或几句 ATL 语句，用逗号隔开；复杂的 ATL 语句包含一个 ATL 区块，必须和它自己同一行。复杂的 ATL 语句的第一行总以冒号结束(":")。

默认情况下，ATL区块中的命令将会被按从上到下的顺序执行，直到区块结束为止。但是time命令将会改变这个顺序，后面会给出说明。

一个区块的执行在它里面所有的命令执行完毕后才会结束。

如果一个ATL命令需要对表达式进行求值，这个求值行为会在这个 transform 对象第一次加入到场景列表中时进行。（例如使用了 show 语句或者 ui 函数。）

 ATL 语句
==============

下面介绍的是所有的 ATL 语句。

补间动画语句
-----------------------

补间动画语句(interpolation statement)是 ATL 控制变换效果的主要方法。

.. productionlist:: atl
    atl_interp : ( `warper` `simple_expression` | "warp" `simple_expression` `simple_expression` )?
               : ( `property` `simple_expression` ( "knot" `simple_expression` )*
               : | "clockwise"
               : | "counterclockwise"
               : | "circles" simple_expression
               : | simple_expression )*

补间动画语句的第一部分是选择该补间动画使用的时间轴函数（也就是一个能把线性运动变成非线性运动的函数）。您可以使用 ATL 内置的时间轴函数，也可以使用关键字"warp"，并在后面给出您自己的时间轴函数。不管您选择的是默认的时间轴函数或是自定义的，您都需要在后面添加一个数字，用来告诉 Ren'Py 这个补间动画将会持续几秒。

若不提供时间轴函数，该补间动画将会是一个0秒的 pause 函数（也就是被无视）。

warper 和 duration 被用来计算完整片段(completion fraction)。通过补间动画的占用时间除以补间动画的持续时间来得到计算结果。而这会被 duration 把持住，并传值到 warper。之后 warper 返回的结构就是完成片段。

补间动画命令可以包含一些从句。当属性和对应值给定时，该值会在此补间动画结束时被获取。这个参数值可以通过以下方式给出：

* 如果该参数值后面跟着1到2个节点（knots）的话，系统会使用动作插值（spline motion）。该属性值的起始值为补间动画开始时的值，结束值为该参数值，而节点是用来调整这个动画的具体细节的。具体效果可以自行尝试一下。

* 如果该补间动画包含"clockwise"或者 "counterclockwise"从句，那么这个动画将被处理为圆周运动(circular motion)，会在稍后的部分里详细介绍。

* 否则，如果值是设定为开始和结束位置之间是线性补间动画(linearly interpolate)，就会使用完整的动画片段。

* 如果使用的是一个简单表达式，它应该是一个只含有位置信息的 transform 对象，不应该包含 warper ，spline 或者圆周运动，骨骼。这个对象的所有属性会作为这个补间动画结束时的各个属性值。

If a simple expression is present, it should evaluate to a transform with only
a single interpolation statement, without a warper, splines, or circular
motion. The properties from the transform are processed as if they were
included in this statement.

下面是一些补间动画的例子::

    show logo base:
         # Show the logo at the upper right side of the screen.
         xalign 1.0 yalign 0.0

         # Take 1.0 seconds to move things back to the left.
         linear 1.0 xalign 0.0

         # Take 1.0 seconds to move things to the location specified in the
         # truecenter transform. Use the ease warper to do this.
         ease 1.0 truecenter

         # Just pause for a second.
         pause 1.0

         # Set the location to circle around.
         alignaround (.5, .5)

         # Use circular motion to bring us to spiral out to the top of
         # the screen. Take 2 seconds to do so.
         linear 2.0 yalign 0.0 clockwise circles 3

         # Use a spline motion to move us around the screen.
         linear 2.0 align (0.5, 1.0) knot (0.0, .33) knot (1.0, .66)

使用pause命令可以使该变换暂停一定的时间。

有些属性可以带许多种不同类型的参数值。比如说，xpos可以是个整数，浮点数或者绝对值。当补间动画的初始值和目标值的类型不同时，该动画的行为是未定义的。

time 语句
--------------

time 命令是一个简单的控制命令。它接受一个简单表达式作为参数，值为一个时间长度。当该ATL区块开始运行时，计时器开始计时。

.. productionlist:: atl
    atl_time : "time" `simple_expression`

当该长度的时间过去之后，系统会开始执行 timer 命令之后的命令，就算之前的命令还没有结束。time命令会导致任何正在执行的命令强制立刻停止。

在处理 time 命令时，系统会隐式地在前面执行一个无限等待的 pause 命令。也就是说，如果脚本运行到了没有被触发的time命令的话，它会一直等待到该time命令被触发为止。

当一个区块里有很多 time 命令的时候，它们所带的参数必须从小到大严格递增。

::

    image backgrounds:
        "bg band"
        time 2.0
        "bg whitehouse"
        time 4.0
        "bg washington"


表达式语句
--------------------

表达式命令就是一条简单表达式。它可以带一个从句，该从句之后是第二条简单表达式。

.. productionlist:: atl
    atl_expression :  `simple_expression` ("with" `simple_expression`)?

该简单表达式的求值结果可以是以下三者之一：

* 如果是个 transform 对象，该变换将被执行。若提供的是 transform 对象，with从句的内容将被无视。

* 如果是个 transform 对象，该变换将被执行。若提供的是 transform 对象，with从句的内容将被无视。

* 否则，该表达式将被认为是一个可显示对象。该可显示对象将作为此变换的子对象，因此您就可以在动画过程中显示新的图像。若使用 with 从句，第二个简单表达式将被解释为一个转场效果，并在显示该可显示对象时使用。

::

    image atl example:
         # Display logo_base.png
         "logo_base.png"

         # Pause for 1.0 seconds.
         1.0

         # Show logo_bw.png, with a dissolve.
         "logo_bw.png" with Dissolve(0.5, alpha=True)

         # Run the move_right tranform.
         move_right

Pass 语句
--------------

.. productionlist:: atl
    atl_pass : "pass"

pass命令是一条什么都不会发生的简单命令。通常用于分隔多条不能放在一起的命令或是充当占位符。就像两套 choic 语句，否则就要以背靠背的形式存在。

Repeat 语句
----------------


repeat命令会导致含有这条命令的ATL区块不断地重复。若提供一个表达式，该表达式的求值结果表示该区块重复的次数。（所以一个含有repeat 2的区块最多会重复2次）

.. productionlist:: atl
    atl_repeat : "repeat" (`simple_expression`)?

The repeat statement must be the last statement in a block.::

    show logo base:
        xalign 0.0
        linear 1.0 xalign 1.0
        linear 1.0 xalign 0.0
        repeat


Block 语句
---------------

block命令是带一个ATL区块的复杂命令。可以用来限定重复的一段命令。

.. productionlist:: atl
    atl_block_stmt : "block" ":"
                   :      `atl_block`

::

    label logo base:
        alpha 0.0 xalign 0.0 yalign 0.0
        linear 1.0 alpha 1.0

        block:
            linear 1.0 xalign 1.0
            linear 1.0 xalign 0.0
            repeat

Choice 语句
----------------

choise 语句是带一个ATL区块的复杂命令。Ren'Py会从一系列连续的 choice 语句中随机挑出一个执行，然后从最后一个 choice 语句之后的一条命令开始继续执行下去。

.. productionlist:: atl
   atl_choice : "choice" (`simple_expression`)? ":"
              :     `atl_block`

Ren'Py会读取尽可能多的连续的choice命令。如果choice后面有个简单表达式，它的值应该是一个浮点数，表示该选项的权重。默认情况下，权重为1.0。

::

    image eileen random:
        choice:
            "eileen happy"
        choice:
            "eileen vhappy"
        choice:
            "eileen concerned"

        pause 1.0
        repeat

Parallel 语句
------------------

parallel命令允许多个ATL区块并行（同步执行）。

.. productionlist:: atl
    atl_parallel : "parallel" ":"
                 :    `atl_block`

Ren'Py会读取尽可能多的连续的parallel命令。这些parallel命令带的区块会同步执行，当这些区块全部执行完毕时，该parallel命令组结束。

这些区块的内容应该是相互独立的。如果两个区块试图同时改变一个属性，结果将会是未定义的。

::

    show logo base:
        parallel:
            xalign 0.0
            linear 1.3 xalign 1.0
            linear 1.3 xalign 0.0
            repeat
        parallel:
            yalign 0.0
            linear 1.6 yalign 1.0
            linear 1.6 yalign 0.0
            repeat

Event 语句
---------------

event 命令会触发相应的事件。

.. productionlist:: atl
    atl_event : "event" `name`

当在区块内有事件被触发时，该区块会检查相应的事件处理器是否存在。若存在，则会将控制权交给相应的处理器，否则该事件会交给其他任何存在的事件处理器处理。

On 语句
------------

On 语句是一个用于定义事件处理器的命令。连续的on命令会尽可能地被合并成一个命令。On 语句能够控制单独一个事件名称，或者以逗号分隔开的事件名称列表。

.. productionlist:: atl
   atl_on : "on" `name` [ "," `name` ] * ":"
          :      `atl_block`

on 语句用于接收事件。当事件被接收到之后，之前接收到的事件会被覆盖，系统会立即开始处理新接收到的事件。当一个事件处理完毕而没有新事件被触发时，会触发 default 事件（除非处理完毕的事件就是default 事件）。

on命令一般不会停止执行，但是可以使用time命令或者一个手动停止的事件处理器来结束它。

::

    show logo base:
        on show:
            alpha 0.0
            linear .5 alpha 1.0
        on hide:
            linear .5 alpha 0.0

    transform pulse_button:
        on hover, idle:
            linear .25 zoom 1.25
            linear .25 zoom 1.0

Contains 语句
------------------

contains 命令用于向该变换添加可显示对象（也就是它的子对象）。它有两个版本：

contains 简单表达式可以将一个简单表达式的值作为该变换的子对象。当您希望向一个变换添加子对象而不是包含另一个 ATL 变换。

.. productionlist:: atl
    atl_contains : "contains" `expression`

::

    transform an_animation:
        "1.png"
        pause 2
        "2.png"
        pause 2
        repeat

    image move_an_animation:
        contains an_animation

        # If we didn't use contains, we'd still be looping and
        # would never reach here.
        xalign 0.0
        linear 1.0 yalign 1.0


“contians 区块”则允许您直接定义一个ATL区块并添加到当前的ATL变换。一个或多个contains 区块会被一起处理，并放在一个 :func:`Fixed` 对象中，作为该变换的子对象之一。

.. productionlist:: atl
    atl_counts : "contains" ":"
         `atl_block`

每一个区块应该定义一个可显示对象，否则将会引起错误。这些 contains 语句会立即执行，不会等待子对象的动画结束。contains 语句主要是个语法糖，因为这样您可以很方便地向子对象传递参数。

::

    image test double:
        contains:
            "logo.png"
            xalign 0.0
            linear 1.0 xalign 1.0
            repeat

        contains:
            "logo.png"
            xalign 1.0
            linear 1.0 xalign 0.0
            repeat

Function 语句
------------------

function 语句允许 ATL 使用 Python 函数来控制 ATL 属性。

.. productionlist:: atl
    atl_function : "function" `expression`

这些函数带的参数与 :func:`Transform` 相同：

* 第一个参数是 transform 对象。该 transform 对象的属性将被调整。

* 第二个参数是执行时间。从函数开始运行时开始计算。

* 第三个参数是动画时间。从相同标签的对象在屏幕上显示时开始计算。

* 若函数返回一个数字x，该函数将在x秒后被再次调用（0表示尽可能快地再次调用该函数）。若返回None，脚本将继续向下运行。

::

    init python:
        def slide_function(trans, st, at):
            if st > 1.0:
                trans.xalign = 1.0
                return None
            else:
                trans.xalign = st
                return 0

    label start:
        show logo base:
            function slide_function
            pause 1.0
            repeat


.. _warpers:

时间轴函数
=======

时间轴函数是一种可以扭曲动画时间轴的函数。以下为预定义的时间轴函数。它们接受一个0到1之间的参数t并返回一个0到1之间的值t'。t表示已经经过的时间占总时间的比例，而t'表示使用了这个时间轴函数的动画认为已经经过的时间占总时间的比例。(如果该语句是设定经过时间为0时，当 Ren`py 运行时，t就会设置成1.0.)t'应该在0.0到1.0之间的范围，但也可以大一点或者小一点。

``pause``
    暂停，然后直接跃迁到新值。若t==1.0，t'=1.0，否则t'=0。
linear

``linear``
    线性补间，t'=t。

``ease``
    开始比较慢，加速，再减速。t' = .5 - math.cos(math.pi * t) / 2.0

``easein``
    开始比较快，然后减速。t' = math.cos((1.0 - t) * math.pi / 2.0

``easeout``
    开始比较慢，然后加速。t' = 1.0 - math.cos(t * math.pi / 2.0)

另外，Ren`py 是支持大多数的 Robert Penner 的简化函数的。为了令其名称与上文的相符，函数已经被稍微重新命名了。标准函数的图表可以在 http://www.easings.net/ 找到。

.. include:: inc/easings

在python early里使用renpy.atl_warper修饰符可以定义新的时间轴函数。它应该在任何使用该时间轴函数的ATL区块之前被定义好。代码类似于：

::

    python early hide:

        @renpy.atl_warper
        def linear(t):
            return t

.. _transform-properties:

变换属性列表
============================

Ren'Py中有以下的变换属性。

当属性的类型是关于位置的时候，它可以是整型，renpy.absolute或者浮点型。如果是浮点型，则表示相对于包含区域（对于pos属性来说）或者是相对于可显示对象（对于anchor属性来说）的比例，否则就是像素的个数。

请您注意，这些属性不是完全独立的。比如说 xalign 和 xpos 都会影响到某些内部数据。在 parallel 命令中，多个区块不应该改变同一个属性。angle 和 radius 属性会同时影响到水平和垂直位置。

.. transform-property:: pos

    :类型: (position, position)
    :默认值: (0, 0)

    相对于包含区域左上角的位置。

.. transform-property:: xpos

    :类型: position
    :默认值: 0

    相对于包含区域左侧的水平位置。

.. transform-property:: ypos

    :类型: position
    :默认值: 0

    相对于包含区域顶部的垂直位置。

.. transform-property:: anchor

    :类型: (position, position)
    :默认值: (0, 0)

    锚点位置，相对于可显示对象的左上角。

.. transform-property:: xanchor

    :类型: position
    :默认值: 0

    水平锚点位置，相对于可显示对象的左侧。

.. transform-property:: yanchor

    :类型: position
    :默认值: 0

    垂直锚点位置，相对于可显示对象的顶部。

.. transform-property:: align

    :类型: (float, float)
    :默认值: (0.0, 0.0)

    等价于将 pos 和 anchor 设定为同一个值。

.. transform-property:: xalign

    :类型: float
    :默认值: 0.0

    等价于将 xpos 和 xanchor 设定为同一个值。

.. transform-property:: yalign

    :类型: float
    :默认值: 0.0

    等价于将 ypos 和 yanchor 设定为同一个值。

.. transform-property:: xoffset

    :类型: float
    :默认值: 0.0

    水平方向可显示对象的偏移量（单位为像素）。正值表示向右偏移。

.. transform-property:: yoffset

    :类型: float
    :默认值: 0.0

    垂直方向可显示对象的偏移量（单位为像素）。正值表示向下偏移。



.. transform-property:: xcenter

    :类型: float
    :默认值: 0.0

    等价于将 xpos 设为这个值，同时将xanchor设为0.5。

.. transform-property:: ycenter

    :类型: float
    :默认值: 0.0

    等价于将 ypos 设为这个值，同时将yanchor设为0.5。

.. transform-property:: rotate

    :类型: float 或 None
    :默认值: None

    若为 None，则无旋转，否则图像将被旋转特定角度。旋转某个可显示对象会导致它被缩放，缩放的比例基于下文要介绍的 rotate_pad 。若 anchor 不是（0.5，0.5），图片的位置将发生变化。

.. transform-property:: rotate_pad

    :类型: boolean
    :默认值: True

    若为 True，被旋转的可显示对象所在的变换的属性值不会被改变。若为 False，相应变换的大小将被调整为能够包含旋转后的可显示对象的最小尺寸。

.. transform-property:: transform_anchor

   :类型: boolean
   :默认值: False

   若为True，锚点会随着缩放以及旋转一起变化位置。这意味着该对象将以锚点作为固定点缩放或是旋转。

.. transform-property:: zoom

    :类型: float
    :默认值: 1.0

    以接受的因数为比例缩放可显示对象。

.. transform-property:: xzoom

    :类型: float
    :默认值: 1.0

    水平方向缩放可显示对象。若为负值，则会导致图像左右翻转。

.. transform-property:: yzoom

   :类型: float
   :默认值: 1.0

   垂直方向缩放可显示对象。若为负值，则会导致图像上下翻转。

.. transform-property:: nearest

    :类型: boolean
    :默认值: None

    如果为 True 的话，可显示对象和它的子对象将会使用最近邻域过滤(nearest-neighbor filtering)来描绘。如果为 False 的话，可显示对象和它的子对象将会以双线性过滤(bilinear filtering)来描绘。如果为 None 的话，它就会继承父类的方法，或者 :var:`config.nearest_neighbor` 里定义的样式，它是值为 False 的默认处理方法。

.. transform-property:: alpha

    :类型: float
    :默认值: 1.0

    该属性控制可显示对象的透明度。

    该属性会独立地作用于可显示对象的每一个子对象。如果子对象有重叠部分，可能会产生不正确的结果。在这种情况下，您可以使用 :func:`Flatten` 来解决这个问题。

.. transform-property:: additive

    :类型: float
    :默认值: 0.0

    该属性控制Ren'Py使用增量混合的程度。若为1.0，Ren'Py使用 ADD 操作符来描绘新图像，若为0.0，Ren'Py使用 OVER 操作符来描绘新图像。

    增量混合也是独立地作用于可显示对象的每一个子对象的。

    完全使用增量混合不会改变目标图像的透明通道。若增量混合绘制的图片不是直接画在一个不透明的对象上的话，它们可能会是不可见的。（复杂的图像操作，如视端，:func:`Flatten` , :func:`Frame` ,以及某些转场效果可能在使用增量混合时出现问题）。

    .. 警告::

        只有硬件解码器支持增量混合，例如OpenGl和DirectX/ANGLE解码器。软件解码器会不正确地绘制增量图像。

        当图像系统启动后，若当期解码器支持增量混合， ``renpy.get_renderer_info()["additive"]``
        会返回True。


.. transform-property:: around

    :类型: (position, position)
    :默认值: (0.0, 0.0)

    若不为None，则用于指定极坐标系的原点，相对于包含区域的左上角。使用该属性后就可以创建圆周动画了。

.. transform-property:: alignaround

    :类型: (float, float)
    :默认值: (0.0, 0.0)

    若不为 None，则用于指定极坐标系的原点，相对于包含区域的左上角。使用该属性后就可以创建圆周动画了。（与上个不同的是这个属性同时设置了 align 的值）

.. transform-property:: angle

    :类型: float

    设置当前角度值。若没有定义极坐标原点则无效。

.. transform-property:: radius

    :类型: position

    设置当前半径。若没有定义极坐标原点则无效。

.. transform-property:: crop

    :类型: None or (int, int, int, int) or (float, float, float, float)
    :默认值: None

    若不为None，导致可显示对象变成被某个矩形裁切后的新的可显示对象。矩形由（x,y,宽，高）的四元组指定。如果浮点数是给定的，而且 crop_relative 的值是 true 时，组件是作为原图像的宽度和高度的片段被提取。否则，组件被视为一个像素的绝对数值。

.. transform-property:: crop_relative

    :类型: boolean
    :默认值: False

    如果为 True 的话，要剪裁的浮动组件将会以原图像的宽度和高度的片段提取出来。

.. transform-property:: corner1

    :类型: None or (int, int)
    :默认值: None

    若不为 None，指定裁切框的左上角位置。该属性的优先级比crop高。

.. transform-property:: corner2

    :类型: None or (int, int)
    :默认值: None

    若不为 None，指定裁切框的右下角位置。该属性的优先级比crop高。

.. transform-property:: size

    :类型: None or (int, int)
    :默认值: None

    若不为 None，将该可显示对象伸缩至指定尺寸（不一定保持原有长宽比）。

.. transform-property:: subpixel

    :类型: boolean
    :默认值: False

    若为 True，使用亚像素位置来描绘图像。

.. transform-property:: delay

    :类型: float
    :默认值: 0.0

    若该变化被作为一个转场效果使用，那么该属性指定了这个转场效果的持续时间。

.. transform-property:: events

    :类型: boolean
    :默认值: True

    如果为 True 的话，events 会被传递到这个变换的子对象里。如果为 False 的话，events 会被禁止。(能够在 ATL 变换里面被应用于阻止 events 收到 old_widget。)

.. transform-property:: xpan

    :类型: None or float
    :默认值: None

    If not None, this interpreted as an angle that is used to pan horizontally
    across a 360 degree panoramic image. The center of the image is used as the
    zero angle, while the left and right edges are -180 and 180 degrees,
    respectively.

.. transform-property:: ypan

    :类型: None or float
    :默认值: None

    If not None, this interpreted as an angle that is used to pan vertically
    across a 360 degree panoramic image. The center of the image is used as the
    zero angle, while the top and bottom edges are -180 and 180 degrees,
    respectively.

.. transform-property:: xtile

    :类型: int
    :默认值: 1

    The number of times to tile the image horizontally. (This is ignored when
    xpan is given.)

.. transform-property:: ytile

    :类型: int
    :默认值: 1

    The number of times to tile the image vertically. (This is ignored when
    ypan is given.)

这些属性以以下顺序生效：

#. tile
#. crop, corner1, corner2
#. size
#. zoom, xzoom, yzoom
#. pan
#. rotate
#. position properties


圆周运动
===============

当补间动画命令包含 ``clockwise`` 或者 ``counterclockwise`` 关键字时，该补间动画是一个圆周运动。Ren'Py 会以初始和结束位置计算旋转的中心，角度。如果提供了 circle 从句，Ren'Py 会保证旋转相应的圈数。

Ren'Py会按照相应的角度和半径属性来调整其他属性实现该圆周运动变化。若使用的是alignaround模式，调整的会是对象的align属性，否则是对象的pos属性。

外部事件
===============

以下事件可以被自动触发：

``start``
    伪事件，在运行到on命令时出发，如果没有其他优先级更高的事件的话。

``show``
    当该变换在show或者scene命令中使用时且没有相同标签的对象存在时触发该事件。

``replace``
    当该变换在show或者scene命令中使用时且已有相同标签的对象存在时触发该事件。

``hide``
    在使用 hide 或者等价于 python 的语句来隐藏该变化时触发。

    注意该事件并不会在使用scene命令清屏或者退出其所在环境（如退出游戏菜单）时触发。

``replaced``
    当该变换被其他变换所替换时触发。该图像在ATL区块结束前并不会真正地从屏幕上消失。

``update``
    Triggered when a screen is updated without being shown or replacing
    another screen. This happens in rare but possible cases, such as when
    the game is loaded and when styles or translations change.

``hover``, ``idle``, ``selected_hover``, ``selected_idle``
   当button对象包含这个变换时，或者这个变换包含button对象时，该button对象进入这些状态时触发相应事件。
