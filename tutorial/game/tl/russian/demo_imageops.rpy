
# game/demo_imageops.rpy:69
translate russian demo_imageops_0e0e59e0:

    # e "Image operations allow us to manipulate images as they are loaded in."
    e "Операции над изображениями позволяют манипулировать изображениями при их загрузке."

# game/demo_imageops.rpy:71
translate russian demo_imageops_2dfc0c2e:

    # e "They're efficient, as they are only evaluated when an image is first loaded."
    e "Они эффективны, так как они выполняются лишь при первой загрузке изображения."

# game/demo_imageops.rpy:73
translate russian demo_imageops_9ee5a075:

    # e "This way, there's no extra work that needs to be done when each frame is drawn to the screen."
    e "Таким образом, не нужно выполнять дополнительной работы при отрисовке кадра на экране."

# game/demo_imageops.rpy:80
translate russian demo_imageops_3f73f4c2:

    # e "Let me show you a test image, the Ren'Py logo."
    e "Позвольте вам показать тестовое изображение, логотип Ren'Py."

# game/demo_imageops.rpy:82
translate russian demo_imageops_e3887927:

    # e "We'll be applying some image operations to it, to see how they can be used."
    e "Мы применим к нему несколько операций, чтобы увидеть, как они используются."

# game/demo_imageops.rpy:87
translate russian demo_imageops_d05ba9d9:

    # e "The im.Crop operation can take the image, and chop it up into a smaller image."
    e "Операция im.Crop берет изображение и режет его в более мелкое."

# game/demo_imageops.rpy:92
translate russian demo_imageops_f57f6496:

    # e "The im.Composite operation lets us take multiple images, and draw them into a single image."
    e "Операция im.Composite позволяет сочетать несколько изображений в одном."

# game/demo_imageops.rpy:94
translate russian demo_imageops_634bc9da:

    # e "While you can do this by showing multiple images, this is often more efficient."
    e "Хотя вы можете просто отобразить несколько изображений, это может оказаться более эффективным."

# game/demo_imageops.rpy:99
translate russian demo_imageops_3a9392e4:

    # e "There's also LiveComposite, which is less efficent, but allows for animation."
    e "Существует также LiveComposite. Он менее эффективен, но позволяет использовать анимации."

# game/demo_imageops.rpy:101
translate russian demo_imageops_aab0c08f:

    # e "It isn't really an image operation, but we don't know where else to put it."
    e "Это, вообщем-то, не операция над изображением, но мы не знаем, где еще о нем сказать."

# game/demo_imageops.rpy:106
translate russian demo_imageops_23cd24da:

    # e "The im.Scale operation lets us scale an image to a particular size."
    e "Операция im.Scale позволяет масштабировать изображение до заданного размера."

# game/demo_imageops.rpy:111
translate russian demo_imageops_dcaf5d6b:

    # e "im.FactorScale lets us do the same thing, except to a factor of the original size."
    e "Операция im.FactorScale делает то же самое, но увеличивает размер изображения в заданное количество раз."

# game/demo_imageops.rpy:116
translate russian demo_imageops_eeaec24a:

    # e "The im.Map operation lets us mess with the red, green, blue, and alpha channels of an image."
    e "Операция im.Map позволяет издеваться над количеством красного, зеленого, синего и прозрачностью в изображении."

# game/demo_imageops.rpy:118
translate russian demo_imageops_a2ed064d:

    # e "In this case, we removed all the red from the image, leaving only the blue and green channels."
    e "В этом случае, мы убрали все красное из изображения, оставив лишь синее и зеленое."

# game/demo_imageops.rpy:125
translate russian demo_imageops_77b0a263:

    # e "The im.Recolor operation can do the same thing, but is more efficient when we're linearly mapping colors."
    e "Операция im.Recolor делает то же самое, но она более эффективна при линейной обработке цветов."

# game/demo_imageops.rpy:130
translate russian demo_imageops_360723bc:

    # e "The im.Twocolor operation lets you take a black and white image, like this one..."
    e "Операция im.Twocolor позволит взять черно-белое изображение, вроде такого..."

# game/demo_imageops.rpy:135
translate russian demo_imageops_0948998c:

    # e "... and assign colors to replace black and white."
    e "... и заменить белый и черный на два других цвета."

# game/demo_imageops.rpy:140
translate russian demo_imageops_75522403:

    # e "The im.MatrixColor operation lets you use a matrix to alter the colors. With the right matrix, you can desaturate colors..."
    e "Операция im.MatrixColor позволяет использовать матрицу для изменения цветов. С правильной матрицей, вы можете снизить насыщенность..."

# game/demo_imageops.rpy:145
translate russian demo_imageops_6fe260b9:

    # e "... tint the image blue..."
    e "... покрасить изображение в синий..."

# game/demo_imageops.rpy:150
translate russian demo_imageops_85c10beb:

    # e "... rotate the hue... "
    e "... повернуть оттенки..."

# game/demo_imageops.rpy:155
translate russian demo_imageops_09d2d97f:

    # e "... or invert the colors, for a kinda scary look."
    e "... или инвертировать цвета, если вы хотите кого-то испугать."

# game/demo_imageops.rpy:160
translate russian demo_imageops_6dd8f586:

    # e "It can even adjust brightness and contrast."
    e "Это даже позволяет изменять яркость и контраст."

# game/demo_imageops.rpy:162
translate russian demo_imageops_ba8ddf3e:

    # e "We've made some of the most common matrices into image operators."
    e "Некоторые из часто используемых матриц были выведены в отдельные операции."

# game/demo_imageops.rpy:167
translate russian demo_imageops_4c62de6f:

    # e "im.Grayscale can make an image grayscale..."
    e "Операция im.Grayscale приводит изображение к оттенкам серого..."

# game/demo_imageops.rpy:172
translate russian demo_imageops_7d471e4b:

    # e "... while im.Sepia can sepia-tone an image."
    e "... а im.Sepia - к сепии."

# game/demo_imageops.rpy:179
translate russian demo_imageops_59ca3a66:

    # e "The im.Alpha operation can adjust the alpha channel on an image, making things partially transparent."
    e "Операция im.Alpha позволяет изменить альфа-канал изображения, делая его частично прозрачным."

# game/demo_imageops.rpy:184
translate russian demo_imageops_514a55db:

    # e "It's useful if a character just happens to be ghost."
    e "Это полезно, если ваш персонаж - призрак."

# game/demo_imageops.rpy:190
translate russian demo_imageops_05fc1200:

    # e "But that isn't the case with me."
    e "Но я - не такая."

# game/demo_imageops.rpy:197
translate russian demo_imageops_cf7fbb57:

    # e "Finally, there's im.Flip, which can flip an image horizontally or vertically."
    e "Наконец, есть im.Flip для переворота изображения по горизонтали или вертикали."

# game/demo_imageops.rpy:199
translate russian demo_imageops_49161c26:

    # e "I think the less I say about this, the better."
    e "Думаю, об этом больше говорить не стоит."

