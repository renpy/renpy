
# game/indepth_displayables.rpy:15
translate schinese simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "Ren'Py有一个可视组件的概念，它类似于一个可以显示和隐藏的图像。"

# game/indepth_displayables.rpy:22
translate schinese simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "image语句用于为可视组件提供图像名。简单的方法是直接赋予图像文件名。"

# game/indepth_displayables.rpy:29
translate schinese simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "但这并不是一个图像唯一可以参考的东西。当字符串中没有“.”时，Ren'Py将其解释为对第二个图像的引用。"

# game/indepth_displayables.rpy:41
translate schinese simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "字符串还可以包含一个颜色代码，由十六进制数字组成，就像网页浏览器使用的颜色一样。"

# game/indepth_displayables.rpy:43
translate schinese simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "三位或六位数字的颜色是不透明的，包含红色、绿色和蓝色值。四位数和八位数的版本附加了alpha，允许半透明的颜色。"

# game/indepth_displayables.rpy:53
translate schinese simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "Transform可视组件使用一个可视组件并可以应用变换属性。"

# game/indepth_displayables.rpy:55
translate schinese simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "注意，因为它使用一个可视组件，可以是另一个图像。实际上，它可以接受这里定义的任何可视组件。"

# game/indepth_displayables.rpy:63
translate schinese simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "有一种更完整的Solid形式，可以使用样式属性。这允许我们更改Solid的大小，通常它会填充屏幕。"

# game/indepth_displayables.rpy:72
translate schinese simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "Text可视组件让Ren'Py把文本当作一个图像。"

# game/indepth_displayables.rpy:80
translate schinese simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "这意味着我们可以像对图像一样，将其他可视组件，如Transform，应用于文本。"

# game/indepth_displayables.rpy:91
translate schinese simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "Composite可视组件允许我们将多个可视组件组合成一个单一的可视组件，从底层到顶层。"

# game/indepth_displayables.rpy:101
translate schinese simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "一些可视组件经常被用来定制Ren'Py界面，其中一个就是Frame可视组件。Frame可视组件采用另一个可视组件，以及左、上、右、下边界的大小。"

# game/indepth_displayables.rpy:111
translate schinese simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "Frame可视组件将放大或缩小以适合其可用的区域。它通过在二维上缩放中心和在一维上缩放边来实现，同时保持角的大小不变。"

# game/indepth_displayables.rpy:118
translate schinese simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "Frame还可以平铺提供给它的可视组件，而不是缩放。"

# game/indepth_displayables.rpy:126
translate schinese simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "抽象的Frame可能看起来有点奇怪，但是当与纹理一起使用时，您可以看到我们如何创建可伸缩的界面组件。"

# game/indepth_displayables.rpy:132
translate schinese simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "这些只是最简单的可视组件，是您最常直接使用的内容。"

# game/indepth_displayables.rpy:134
translate schinese simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "如果你精通Python，你甚至可以为小游戏编写自定义的可视组件。但对于许多视觉小说，这些就是你所需要的全部了。"

translate schinese strings:

    # game/indepth_displayables.rpy:67
    old "This is a text displayable."
    new "这是一个文本可视组件。"
