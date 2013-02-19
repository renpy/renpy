# Translation updated at 2013-02-18 11:40

# game/demo_imageops.rpy:69
translate japanese demo_imageops_0e0e59e0:

    # e "Image operations allow us to manipulate images as they are loaded in."
    e "画像操作の関数を用いると、読み込まれた画像を操作できます。"

# game/demo_imageops.rpy:71
translate japanese demo_imageops_2dfc0c2e:

    # e "They're efficient, as they are only evaluated when an image is first loaded."
    e "これらは画像が1回目にロードされたときに評価するため、効率的です。"

# game/demo_imageops.rpy:73
translate japanese demo_imageops_9ee5a075:

    # e "This way, there's no extra work that needs to be done when each frame is drawn to the screen."
    e "この方法では、それぞれのフレームが画面に描画されるときに、処理した画像を得るための余計な操作が要りません。"

# game/demo_imageops.rpy:80
translate japanese demo_imageops_3f73f4c2:

    # e "Let me show you a test image, the Ren'Py logo."
    e "テスト画像であるRen'Pyのロゴを見せます。"

# game/demo_imageops.rpy:82
translate japanese demo_imageops_e3887927:

    # e "We'll be applying some image operations to it, to see how they can be used."
    e "これにいくつかの画像処理を行い、どのように使えるか見ます。"

# game/demo_imageops.rpy:87
translate japanese demo_imageops_d05ba9d9:

    # e "The im.Crop operation can take the image, and chop it up into a smaller image."
    e "im.Crop 関数を使うと、画像を取得して小さい画像に切り抜けます。"

# game/demo_imageops.rpy:92
translate japanese demo_imageops_f57f6496:

    # e "The im.Composite operation lets us take multiple images, and draw them into a single image."
    e "im.Composite 関数を使うと、複数の画像を取得して1つの画像に描画できます。"

# game/demo_imageops.rpy:94
translate japanese demo_imageops_634bc9da:

    # e "While you can do this by showing multiple images, this is often more efficient."
    e "複数の画像を表示するときにこの方法を使えれば、より効率的になり得ます。"

# game/demo_imageops.rpy:99
translate japanese demo_imageops_3a9392e4:

    # e "There's also LiveComposite, which is less efficent, but allows for animation."
    e "LiveComposite 関数は、効率はあまり良くないですがアニメーション表示できます。"

# game/demo_imageops.rpy:101
translate japanese demo_imageops_aab0c08f:

    # e "It isn't really an image operation, but we don't know where else to put it."
    e "これは本当は画像操作の関数ではありませんが、他に紹介できる場所が分かりませんでした。"

# game/demo_imageops.rpy:106
translate japanese demo_imageops_23cd24da:

    # e "The im.Scale operation lets us scale an image to a particular size."
    e "im.Scale 関数を使うと、画像を別の大きさに拡大・縮小できます。"

# game/demo_imageops.rpy:111
translate japanese demo_imageops_dcaf5d6b:

    # e "im.FactorScale lets us do the same thing, except to a factor of the original size."
    e "im.FactorScale も同様の操作ができますが、これは倍率によって指定します。"

# game/demo_imageops.rpy:116
translate japanese demo_imageops_eeaec24a:

    # e "The im.Map operation lets us mess with the red, green, blue, and alpha channels of an image."
    e "im.Map 関数を使うと、画像の赤、緑、青、アルファチャンネルに干渉できます。"

# game/demo_imageops.rpy:118
translate japanese demo_imageops_a2ed064d:

    # e "In this case, we removed all the red from the image, leaving only the blue and green channels."
    e "この場合は、画像からすべての赤を削除し、青と緑のチャンネルだけを残しました。"

# game/demo_imageops.rpy:125
translate japanese demo_imageops_77b0a263:

    # e "The im.Recolor operation can do the same thing, but is more efficient when we're linearly mapping colors."
    e "im.Recolor 関数は同じ事ができますが、色を直線的にマッピングする場合は、より効率的です。"

# game/demo_imageops.rpy:130
translate japanese demo_imageops_360723bc:

    # e "The im.Twocolor operation lets you take a black and white image, like this one..."
    e "im.Twocolor 関数を使うと、このようにモノクロの画像を取得できます。"

# game/demo_imageops.rpy:135
translate japanese demo_imageops_0948998c:

    # e "... and assign colors to replace black and white."
    e "... そして黒と白に別の色を割り当てます。"

# game/demo_imageops.rpy:140
translate japanese demo_imageops_75522403:

    # e "The im.MatrixColor operation lets you use a matrix to alter the colors. With the right matrix, you can desaturate colors..."
    e "im.MatrixColor 関数を使うと、色を変えるための行列を使えます。正しい行列を使えば、彩度を変えられます..."

# game/demo_imageops.rpy:145
translate japanese demo_imageops_6fe260b9:

    # e "... tint the image blue..."
    e "... 青っぽい色合いにしたり..."

# game/demo_imageops.rpy:150
translate japanese demo_imageops_85c10beb:

    # e "... rotate the hue... "
    e "... 色相を回転させたり... "

# game/demo_imageops.rpy:155
translate japanese demo_imageops_09d2d97f:

    # e "... or invert the colors, for a kinda scary look."
    e "... 色を反転させて不気味な感じにしたりできます。"

# game/demo_imageops.rpy:160
translate japanese demo_imageops_6dd8f586:

    # e "It can even adjust brightness and contrast."
    e "輝度やコントラストも調節できます。"

# game/demo_imageops.rpy:162
translate japanese demo_imageops_ba8ddf3e:

    # e "We've made some of the most common matrices into image operators."
    e "画像処理関数の中に、最も一般的な行列をいくつか入れてあります。"

# game/demo_imageops.rpy:167
translate japanese demo_imageops_4c62de6f:

    # e "im.Grayscale can make an image grayscale..."
    e "im.Grayscale は、画像をグレースケールにできます..."

# game/demo_imageops.rpy:172
translate japanese demo_imageops_7d471e4b:

    # e "... while im.Sepia can sepia-tone an image."
    e "... 一方、im.Sepia は画像をセピア調にできます。"

# game/demo_imageops.rpy:179
translate japanese demo_imageops_59ca3a66:

    # e "The im.Alpha operation can adjust the alpha channel on an image, making things partially transparent."
    e "im.Alpha 関数は画像のアルファチャンネルを調節し、部分的に透明にできます。"

# game/demo_imageops.rpy:184
translate japanese demo_imageops_514a55db:

    # e "It's useful if a character just happens to be ghost."
    e "キャラクターが幽霊になってしまった場合に便利です。"

# game/demo_imageops.rpy:190
translate japanese demo_imageops_05fc1200:

    # e "But that isn't the case with me."
    e "私のことを言っているのではありません。"

# game/demo_imageops.rpy:197
translate japanese demo_imageops_cf7fbb57:

    # e "Finally, there's im.Flip, which can flip an image horizontally or vertically."
    e "最後に、im.Flip があります。これは画像の上下、もしくは左右を入れ替えられます。"

# game/demo_imageops.rpy:199
translate japanese demo_imageops_49161c26:

    # e "I think the less I say about this, the better."
    e "このことについてはあまり言わないほうが良いでしょう。"

