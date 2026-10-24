
# game/indepth_displayables.rpy:15
translate tchinese simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "Ren'Py 有顯示物件的概念，它類似於可以顯示和隱藏的圖片。"

# game/indepth_displayables.rpy:22
translate tchinese simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "image 語句用來為顯示物件指定圖片名稱。最簡單的方式是直接提供圖片檔名。"

# game/indepth_displayables.rpy:29
translate tchinese simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "不過，圖片名稱並不只能指向檔案。字串中沒有句點時，Ren'Py 會將它解讀為對另一張圖片的引用。"

# game/indepth_displayables.rpy:41
translate tchinese simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "字串也可以包含由十六進位數字組成的色碼，就像網頁瀏覽器使用的顏色。"

# game/indepth_displayables.rpy:43
translate tchinese simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "三位或六位數的色碼是不透明的，包含紅、綠、藍三個值。四位和八位版本會附加 alpha 值，允許半透明顏色。"

# game/indepth_displayables.rpy:53
translate tchinese simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "Transform 顯示物件接收另一個顯示物件，並可套用變換屬性。"

# game/indepth_displayables.rpy:55
translate tchinese simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "注意，由於它接收顯示物件，因此也能接收另一張圖片。事實上，這裡定義的任何顯示物件都可以使用。"

# game/indepth_displayables.rpy:63
translate tchinese simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "Solid 還有一種更完整的形式，可以接收樣式屬性。這讓我們能變更 Solid 的大小；通常它會填滿畫面。"

# game/indepth_displayables.rpy:72
translate tchinese simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "Text 顯示物件讓 Ren'Py 將文字視為圖片。"

# game/indepth_displayables.rpy:80
translate tchinese simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "因此，我們可以像處理圖片一樣，將 Transform 等其他顯示物件套用到文字上。"

# game/indepth_displayables.rpy:91
translate tchinese simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "Composite 顯示物件能將多個顯示物件由下到上組合成單一顯示物件。"

# game/indepth_displayables.rpy:101
translate tchinese simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "有些顯示物件常用來自訂 Ren'Py 介面，Frame 就是其中之一。Frame 顯示物件接收另一個顯示物件，以及左、上、右、下邊界的大小。"

# game/indepth_displayables.rpy:111
translate tchinese simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "Frame 顯示物件會放大或縮小以符合可用區域；它會在二維方向縮放中心、在一維方向縮放邊緣，同時保持角落大小不變。"

# game/indepth_displayables.rpy:118
translate tchinese simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "Frame 也可以平鋪提供給它的顯示物件，而不是縮放。"

# game/indepth_displayables.rpy:126
translate tchinese simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "單看抽象的 Frame 可能有點奇怪，但搭配材質使用時，就能看出如何建立可縮放的介面元件。"

# game/indepth_displayables.rpy:132
translate tchinese simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "這些只是最簡單的顯示物件，也是你最常直接使用的物件。"

# game/indepth_displayables.rpy:134
translate tchinese simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "如果你精通 Python，甚至可以為小遊戲撰寫自訂顯示物件。不過對許多視覺小說來說，這些就已經足夠。"

translate tchinese strings:

    # game/indepth_displayables.rpy:67
    old "This is a text displayable."
    new "這是一個文字顯示物件。"
