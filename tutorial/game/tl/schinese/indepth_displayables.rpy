
# game/indepth_displayables.rpy:15
translate schinese simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "Ren'Py 有“显示对象”的概念。显示对象类似图像，可以显示或隐藏。"

# game/indepth_displayables.rpy:22
translate schinese simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "image 语句用于为显示对象定义图像名称。最简单的方式是直接提供图像文件名。"

# game/indepth_displayables.rpy:29
translate schinese simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "不过，image 不只能引用文件。当字符串中没有句点时，Ren'Py 会将其解释为对另一个图像定义的引用。"

# game/indepth_displayables.rpy:41
translate schinese simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "字符串还可以包含颜色代码，由十六进制数字组成，就像网页浏览器使用的颜色代码一样。"

# game/indepth_displayables.rpy:43
translate schinese simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "三位或六位颜色代码是不透明的，包含红、绿、蓝值；四位或八位版本还会附加 alpha 值，从而支持半透明颜色。"

# game/indepth_displayables.rpy:53
translate schinese simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "Transform 显示对象接收另一个显示对象，并可以对它应用变换属性。"

# game/indepth_displayables.rpy:55
translate schinese simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "注意，由于它接收显示对象，所以也可以接收另一个图像。实际上，这里定义的任何显示对象都可以传给它。"

# game/indepth_displayables.rpy:63
translate schinese simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "Solid 还有一种更完整的写法，可以接受样式属性。这样就能改变 Solid 的大小；通常情况下，Solid 会填满屏幕。"

# game/indepth_displayables.rpy:72
translate schinese simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "Text 显示对象让 Ren'Py 可以像处理图像一样处理文本。"

# game/indepth_displayables.rpy:80
translate schinese simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "这意味着我们可以像对图像一样，把 Transform 等其他显示对象应用到 Text 上。"

# game/indepth_displayables.rpy:91
translate schinese simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "Composite 显示对象可以把多个显示对象按从下到上的顺序组合成一个显示对象。"

# game/indepth_displayables.rpy:101
translate schinese simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "有些显示对象经常用于定制 Ren'Py 界面，Frame 就是其中之一。Frame 接收另一个显示对象，以及左、上、右、下边框的宽度。"

# game/indepth_displayables.rpy:111
translate schinese simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "Frame 显示对象会放大或缩小，以适应可用区域。它会在两个方向缩放中心、在一个方向缩放边缘，同时保持角落大小不变。"

# game/indepth_displayables.rpy:118
translate schinese simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "Frame 还可以平铺传入显示对象的各个部分，而不是进行缩放。"

# game/indepth_displayables.rpy:126
translate schinese simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "单独看 Frame 可能有点奇怪，但配合纹理使用时，就能看到如何创建可缩放的界面组件。"

# game/indepth_displayables.rpy:132
translate schinese simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "这些只是最简单的显示对象，也是你最常直接使用的几种。"

# game/indepth_displayables.rpy:134
translate schinese simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "如果熟悉 Python，甚至可以为小游戏编写自定义显示对象。不过对许多视觉小说来说，这些显示对象已经够用了。"

translate schinese strings:

    # game/indepth_displayables.rpy:67
    old "This is a text displayable."
    new "这是一个文本可视组件。"
