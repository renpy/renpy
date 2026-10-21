
# game/tutorial_atl.rpy:205
translate schinese tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "本教程将介绍 Ren'Py 如何在屏幕上定位物体。在此之前，先了解 Python 如何处理数字。"

# game/tutorial_atl.rpy:207
translate schinese tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Python 中主要有两类数字：整数和浮点数。整数只包含数字，浮点数则包含小数点。"

# game/tutorial_atl.rpy:209
translate schinese tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "例如，100 是整数，0.5 是浮点数，简称 float。在这个体系中，零也有两种：0 是整数，0.0 是浮点数。"

# game/tutorial_atl.rpy:211
translate schinese tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Py 使用整数表示绝对坐标，使用浮点数表示已知大小区域中的比例。"

# game/tutorial_atl.rpy:213
translate schinese tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "定位物体时，这个区域通常就是整个屏幕。"

# game/tutorial_atl.rpy:215
translate schinese tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "我先让开，给你看看一些位置。"

# game/tutorial_atl.rpy:229
translate schinese tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "原点是屏幕左上角，x 坐标（xpos）和 y 坐标（ypos）在那里都为零。"

# game/tutorial_atl.rpy:235
translate schinese tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "增大 xpos，物体就会向右移动。这里 xpos 为 0.5，表示屏幕宽度的一半。"

# game/tutorial_atl.rpy:240
translate schinese tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "把 xpos 增大到 1.0，物体就会移动到屏幕右边界。"

# game/tutorial_atl.rpy:246
translate schinese tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "也可以使用绝对 xpos，以距屏幕左侧的像素数表示。例如，这个窗口宽 1280 像素，因此 xpos 为 640 会把目标放在顶行的中央。"

# game/tutorial_atl.rpy:248
translate schinese tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "y 轴位置 ypos 的工作方式相同。现在 ypos 为 0.0。"

# game/tutorial_atl.rpy:254
translate schinese tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "这里 ypos 为 0.5。"

# game/tutorial_atl.rpy:259
translate schinese tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "ypos 为 1.0 表示屏幕底部的位置。仔细看，你会看到位置指示器在文本窗口下方旋转。"

# game/tutorial_atl.rpy:261
translate schinese tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "和 xpos 一样，ypos 也可以是整数。这时，ypos 表示距屏幕顶部的像素总数。"

# game/tutorial_atl.rpy:267
translate schinese tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "你能猜到这个位置相对于屏幕在哪里吗？" nointeract

# game/tutorial_atl.rpy:273
translate schinese tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "很遗憾，答错了。xpos 是 0.75，ypos 是 0.25。"

# game/tutorial_atl.rpy:275
translate schinese tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "换句话说，它距左侧 75%%，距顶部 25%%。"

# game/tutorial_atl.rpy:279
translate schinese tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "答得好！你找对位置了。"

# game/tutorial_atl.rpy:283
translate schinese tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "很遗憾，答错了。xpos 是 0.75，ypos 是 0.25。"

# game/tutorial_atl.rpy:285
translate schinese tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "换句话说，它距左侧 75%%，距顶部 25%%。"

# game/tutorial_atl.rpy:299
translate schinese tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "第二个要了解的位置是锚点。锚点是被定位物体上的一个点。"

# game/tutorial_atl.rpy:301
translate schinese tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "例如，这里的 xanchor 和 yanchor 都是 0.0，锚点位于 logo 图像的左上角。"

# game/tutorial_atl.rpy:306
translate schinese tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "把 xanchor 增大到 1.0，锚点就会移动到图像右上角。"

# game/tutorial_atl.rpy:311
translate schinese tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "同样，当 xanchor 和 yanchor 都为 1.0 时，锚点位于右下角。"

# game/tutorial_atl.rpy:318
translate schinese tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "要把图像放到屏幕上，需要同时指定位置和锚点。"

# game/tutorial_atl.rpy:326
translate schinese tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "然后把它们对齐，让位置和锚点位于屏幕上的同一点。"

# game/tutorial_atl.rpy:336
translate schinese tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "当两者都放在左上角时，图像就会移动到屏幕左上角。"

# game/tutorial_atl.rpy:345
translate schinese tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "通过正确组合位置和锚点，可以指定屏幕上的任意位置，甚至不必知道图像大小。"

# game/tutorial_atl.rpy:357
translate schinese tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "通常把 xpos 和 xanchor 设为相同值很有用。我们把这个组合称为 xalign，它表示屏幕上的比例位置。"

# game/tutorial_atl.rpy:362
translate schinese tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "例如，将 xalign 设为 0.0 时，物体会与屏幕左侧对齐。"

# game/tutorial_atl.rpy:367
translate schinese tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "设为 1.0 时，物体会与屏幕右侧对齐。"

# game/tutorial_atl.rpy:372
translate schinese tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "设为 0.5 时，物体就回到屏幕中央。"

# game/tutorial_atl.rpy:374
translate schinese tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "设置 yalign 的方式类似，只是作用于 y 轴。"

# game/tutorial_atl.rpy:376
translate schinese tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "记住，xalign 就是把 xpos 和 xanchor 设为相同值，yalign 就是把 ypos 和 yanchor 设为相同值。"

# game/tutorial_atl.rpy:381
translate schinese tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "xcenter 和 ycenter 属性用于定位图像中心。这里 xcenter 为 0.75，图像中心距屏幕右侧四分之三的位置。"

# game/tutorial_atl.rpy:386
translate schinese tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "当 xcenter 为 1.0、图像有一半移出屏幕右侧时，xalign 和 xcenter 的差异会更加明显。"

# game/tutorial_atl.rpy:394
translate schinese tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "xoffset 和 yoffset 属性会在其他设置完成后应用，分别让物体向右或向下偏移。"

# game/tutorial_atl.rpy:399
translate schinese tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "当然，也可以使用负数，让物体向左或向上偏移。"

# game/tutorial_atl.rpy:404
translate schinese tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "最后介绍 align、pos、anchor 和 center 之类的组合属性。align 接收一对数字，分别设置 xalign 和 yalign；其他属性的方式也类似。"

# game/tutorial_atl.rpy:411
translate schinese tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "理解位置后，就可以使用变换在 Ren'Py 屏幕上移动物体。"

# game/tutorial_atl.rpy:418
translate schinese tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "Ren'Py 使用变换为图像制作动画、进行处理和定位。我们已经见过最简单的变换："

# game/tutorial_atl.rpy:425
translate schinese tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "变换可以很简单，只负责把图像放到屏幕上的某个位置，例如 right 变换。"

# game/tutorial_atl.rpy:429
translate schinese tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "不过，变换也可以复杂得多，把动画和特效结合起来。为了演示，就来一场毫无必要的摇滚演唱会吧！"

# game/tutorial_atl.rpy:437
translate schinese tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "不过首先，让我们来一场……毫无必要的摇滚演唱会！"

# game/tutorial_atl.rpy:445
translate schinese tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "工作量确实不小，但它是由许多小部分组合而成的。"

# game/tutorial_atl.rpy:447
translate schinese tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "Ren'Py 中的大多数变换都使用 Animation and Transform Language（动画与变换语言，简称 ATL）构建。"

# game/tutorial_atl.rpy:449
translate schinese tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "目前，Ren'Py 中有三个地方可以使用 ATL。"

# game/tutorial_atl.rpy:454
translate schinese tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "第一个地方是 image 语句。图像不必定义为显示对象，也可以定义为一段 ATL 代码块。"

# game/tutorial_atl.rpy:456
translate schinese tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "采用这种方式时，必须确保 ATL 包含一个或多个实际要显示的显示对象。"

# game/tutorial_atl.rpy:461
translate schinese tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "第二种方式是使用 transform 语句。它把 ATL 代码块赋给一个 Python 变量，使其可以用于 at 子句和其他变换内部。"

# game/tutorial_atl.rpy:473
translate schinese tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "最后，ATL 代码块还可以作为 show 语句的一部分使用，代替 at 子句。"

# game/tutorial_atl.rpy:480
translate schinese tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though your click stopped the motion, the image remains in the same place."
    e "ATL 作为 show 语句的一部分使用时，即使变换发生改变，属性值也会保留。因此，即使点击停止了移动，图像仍会停在原来的位置。"

# game/tutorial_atl.rpy:488
translate schinese tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "ATL 的关键在于所谓的可组合性。ATL 由相对简单的命令组成，可以组合起来创建复杂的变换。"

# game/tutorial_atl.rpy:490
translate schinese tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "在解释 ATL 的工作方式之前，先说明动画和变换分别是什么。"

# game/tutorial_atl.rpy:495
translate schinese tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "动画是指正在显示的显示对象发生变化。例如，我现在正在改变表情。"

# game/tutorial_atl.rpy:522
translate schinese tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "变换包括移动或扭曲图像，例如在屏幕上定位、放大缩小、旋转，以及改变不透明度。"

# game/tutorial_atl.rpy:530
translate schinese tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "介绍 ATL 时，先看一个简单动画。这个动画由 image 语句中的五行 ATL 代码组成。"

# game/tutorial_atl.rpy:532
translate schinese tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "要更换显示对象，只需在 ATL 的一行中写出它。这里会在两张图像之间来回切换。"

# game/tutorial_atl.rpy:534
translate schinese tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "由于这里定义的是图像，ATL 的第一行必须提供一个显示对象，否则就没有内容可显示。"

# game/tutorial_atl.rpy:536
translate schinese tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "第二行和第四行是 pause 语句，会让 ATL 各等待半秒后继续。这就是图像之间延迟的来源。"

# game/tutorial_atl.rpy:538
translate schinese tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "最后一行是 repeat 语句，会重新开始执行当前 ATL 代码块。每个代码块只能有一个 repeat 语句。"

# game/tutorial_atl.rpy:543
translate schinese tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "如果改写为 repeat 2，动画就会循环两次后停止。"

# game/tutorial_atl.rpy:548
translate schinese tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "省略 repeat 语句后，动画会在执行到 ATL 代码块末尾时停止。"

# game/tutorial_atl.rpy:554
translate schinese tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "默认情况下，显示对象会立即替换。也可以使用 with 子句，在显示对象之间加入转场。"

# game/tutorial_atl.rpy:561
translate schinese tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "动画讲完了，接下来看看如何用 ATL 变换图像，先从在屏幕上定位图像开始。"

# game/tutorial_atl.rpy:570
translate schinese tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "最简单的做法是静态定位图像：先写出位置属性名称，再写出属性值。"

# game/tutorial_atl.rpy:575
translate schinese tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "再添加几条语句，就可以让物体在屏幕上移动。"

# game/tutorial_atl.rpy:577
translate schinese tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "这个例子先把图像放在屏幕右上方并等待一秒，然后移到左侧，再等待一秒并重复这一过程。"

# game/tutorial_atl.rpy:579
translate schinese tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "pause 和 repeat 语句就是动画示例中使用过的语句，它们在 ATL 代码的各处都能工作。"

# game/tutorial_atl.rpy:584
translate schinese tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "让图像在屏幕上跳来跳去并不太有用，因此 ATL 提供了 interpolation 语句。"

# game/tutorial_atl.rpy:586
translate schinese tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "interpolation 语句可以让变换属性的值从旧值平滑变化到新值。"

# game/tutorial_atl.rpy:588
translate schinese tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "这里，第二行 ATL 使用了 interpolation 语句。它先写时间函数名称，本例中是 linear。"

# game/tutorial_atl.rpy:590
translate schinese tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "后面是持续时间，本例中为三秒；最后是一组属性，每个属性后面跟着新值。"

# game/tutorial_atl.rpy:592
translate schinese tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "每个属性都会从语句开始时的值插值到语句结束时的值。这个过程每帧执行一次，因此动画很平滑。"

# game/tutorial_atl.rpy:603
translate schinese tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL 还支持 circle、spline motion 等更复杂的移动类型，不过这里不演示。"

# game/tutorial_atl.rpy:607
translate schinese tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "除了显示对象、pause、interpolation 和 repeat，还可以在 ATL 中使用其他一些语句。"

# game/tutorial_atl.rpy:619
translate schinese tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "使用该语句创建的 ATL 变换本身也会成为 ATL 语句。由于默认位置同样是变换，所以可以在 ATL 代码块中使用 left、right 和 center。"

# game/tutorial_atl.rpy:635
translate schinese tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "这里有两个新语句。block 语句可以包含一段 ATL 代码；由于 repeat 作用于代码块，因此可以只重复 ATL 变换的一部分。"

# game/tutorial_atl.rpy:637
translate schinese tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "还有 time 语句，它会在代码块开始经过指定秒数后执行。即使另一个语句仍在运行，time 也会执行并停止那个语句。"

# game/tutorial_atl.rpy:639
translate schinese tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "因此，这个例子会让图像来回弹跳 11.5 秒，然后移动到屏幕右侧。"

# game/tutorial_atl.rpy:653
translate schinese tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "parallel 语句可以同时运行两个 ATL 代码块。"

# game/tutorial_atl.rpy:655
translate schinese tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "这里，上方代码块沿水平方向移动图像，下方代码块沿垂直方向移动图像。由于速度不同，看起来就像图像在屏幕上弹跳。"

# game/tutorial_atl.rpy:669
translate schinese tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "最后，choice 语句会让 Ren'Py 随机选择一个 ATL 代码块，从而让 Ren'Py 显示的内容产生变化。"

# game/tutorial_atl.rpy:675
translate schinese tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "这个教程游戏只浅尝了 ATL 的能力。例如，我们甚至还没讲到 on 和 event 语句。更多信息请参阅{a=https://renpy.org/doc/html/atl.html}参考手册中的 ATL 章节{/a}。"

# game/tutorial_atl.rpy:684
translate schinese transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "Ren'Py 有不少变换属性，可以与 ATL、Transform 显示对象及 add 屏幕语言语句一起使用。"

# game/tutorial_atl.rpy:685
translate schinese transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "下面展示这些属性的实际效果，帮助你熟悉每个属性的作用。"

# game/tutorial_atl.rpy:701
translate schinese transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "首先，所有位置属性也都是变换属性，包括 pos、anchor、align、center 和 offset。"

# game/tutorial_atl.rpy:719
translate schinese transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "给 xpos 和 ypos 赋予负值，就可以在大于屏幕的显示对象上进行平移。"

# game/tutorial_atl.rpy:729
translate schinese transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "subpixel属性控制图像如何与界面对齐。如果为False，图像可以是像素完美的，但也可能存在像素跳跃。"

# game/tutorial_atl.rpy:736
translate schinese transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "当设置为True时，移动更平滑，但图像会模糊一点。"

# game/tutorial_atl.rpy:755
translate schinese transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "变换也支持极坐标。around 属性用像素坐标设置坐标系的中心。"

# game/tutorial_atl.rpy:763
translate schinese transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "angle 属性以度数指定角度。角度按顺时针计算，0 度位于屏幕顶部。"

# game/tutorial_atl.rpy:772
translate schinese transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "radius 属性指定显示对象锚点到坐标系中心的像素距离。"

# game/tutorial_atl.rpy:786
translate schinese transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "调整显示对象大小有几种方式。zoom 属性按倍数缩放显示对象，使其变大或变小。"

# game/tutorial_atl.rpy:799
translate schinese transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoom 和 yzoom 属性可以分别沿 X 轴和 Y 轴缩放显示对象。"

# game/tutorial_atl.rpy:809
translate schinese transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "将 xzoom 或 yzoom 设为负数，就可以水平或垂直翻转图像。"

# game/tutorial_atl.rpy:819
translate schinese transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "除了按倍数缩放，还可以使用 size 变换属性，把显示对象缩放到指定的像素尺寸。"

# game/tutorial_atl.rpy:834
translate schinese transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "alpha 属性用于改变显示对象的不透明度，可以让它出现或消失。"

# game/tutorial_atl.rpy:847
translate schinese transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "rotate 属性用于旋转显示对象。"

# game/tutorial_atl.rpy:858
translate schinese transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "默认情况下，旋转显示对象时，Ren'Py 会在四边保留额外空间，使其尺寸不会随旋转改变。这里可以看到左侧和顶部的额外空间，右侧和底部也一样。"

# game/tutorial_atl.rpy:870
translate schinese transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "将 rotate_pad 设为 False 可以去除这些空间，但代价是显示对象的尺寸会随旋转改变。"

# game/tutorial_atl.rpy:881
translate schinese transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "xtile 和 ytile 这两个 tile 变换属性会重复显示对象多次。"

# game/tutorial_atl.rpy:891
translate schinese transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "crop 属性会从显示对象中裁剪出一个矩形，只显示其中一部分。"

# game/tutorial_atl.rpy:905
translate schinese transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "结合使用 crop 和 size，就可以聚焦显示图像的特定部分。"

# game/tutorial_atl.rpy:917
translate schinese transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "xpan 和 ypan 属性可以按指定角度平移显示对象，角度以度数表示，0 表示中心。"

# game/tutorial_atl.rpy:924
translate schinese transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "这就是所有可用的变换属性。按正确顺序组合它们，就能创建复杂效果。"

translate schinese strings:

    # game/tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # game/tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # game/tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"
