

# game/demo_imageops.rpy:69
translate korean demo_imageops_0e0e59e0:


    # e "Image operations allow us to manipulate images as they are loaded in."
    e "이미지 조작는 이미 로드된 이미지를 변경할 수 있게 해줍니다."


# game/demo_imageops.rpy:71
translate korean demo_imageops_2dfc0c2e:


    # e "They're efficient, as they are only evaluated when an image is first loaded."
    e "이러한 기능들은 굉장히 효과적인데요, 이미지들이 로드될 때 단 한번만 계산되기 때문입니다."


# game/demo_imageops.rpy:73
translate korean demo_imageops_9ee5a075:


    # e "This way, there's no extra work that needs to be done when each frame is drawn to the screen."
    e "이 방법을 사용하면 이미 그려져 있는 프레임을 변경하는데 별로 힘들이지 않고 할 수 있습니다."


# game/demo_imageops.rpy:80
translate korean demo_imageops_3f73f4c2:


    # e "Let me show you a test image, the Ren'Py logo."
    e "그럼 테스트 이미지로 렌'파이 로고를 볼까요?"


# game/demo_imageops.rpy:82
translate korean demo_imageops_e3887927:


    # e "We'll be applying some image operations to it, to see how they can be used."
    e "제가 이 이미지에 어떤 조작을 할 건데요, 어떻게 사용될 수 있는지 보자구요."


# game/demo_imageops.rpy:87
translate korean demo_imageops_d05ba9d9:


    # e "The im.Crop operation can take the image, and chop it up into a smaller image."
    e "im.Crop 조작은 이미지를 받아서 작은 이미지로 잘라냅니다."


# game/demo_imageops.rpy:92
translate korean demo_imageops_f57f6496:


    # e "The im.Composite operation lets us take multiple images, and draw them into a single image."
    e "im.Composite 조작은 여러 장의 이미지를 받은 후, 이 둘을 하나의 이미지로서 화면에 그립니다."


# game/demo_imageops.rpy:94
translate korean demo_imageops_634bc9da:


    # e "While you can do this by showing multiple images, this is often more efficient."
    e "물론 여러 이미지를 보이는 방법으로도 할 수 있습니다만, 이미지 조작을 사용하는 편이 훨씬 경제적이에요."


# game/demo_imageops.rpy:99
translate korean demo_imageops_3a9392e4:


    # e "There's also LiveComposite, which is less efficent, but allows for animation."
    e "LiveComposite이라는 녀석도 있는데요, 이 아이는 Composite보다는 덜 경제적이지만 애니메이션을 추가할 수 있답니다."


# game/demo_imageops.rpy:101
translate korean demo_imageops_aab0c08f:


    # e "It isn't really an image operation, but we don't know where else to put it."
    e "이건 엄밀히 말하면 이미지 조작이 아니기는 합니다만, 어디에 넣어야 할지 모르겠어서 이미지 조작에서 설명드립니다."


# game/demo_imageops.rpy:106
translate korean demo_imageops_23cd24da:


    # e "The im.Scale operation lets us scale an image to a particular size."
    e "im.Scale은 이미지를 주어진 크기로 키우거나 줄입니다."


# game/demo_imageops.rpy:111
translate korean demo_imageops_dcaf5d6b:


    # e "im.FactorScale lets us do the same thing, except to a factor of the original size."
    e "im.FactorScale도 같은 역할을 하지만, 이 조작은 원본 크기의 비율을 받습니다."


# game/demo_imageops.rpy:116
translate korean demo_imageops_eeaec24a:


    # e "The im.Map operation lets us mess with the red, green, blue, and alpha channels of an image."
    e "im.Map 조작은 이미지의 빨강, 초록, 파랑, 알파 채널의 값을 바꿀 수 있게 해 줍니다."


# game/demo_imageops.rpy:118
translate korean demo_imageops_a2ed064d:


    # e "In this case, we removed all the red from the image, leaving only the blue and green channels."
    e "이 경우, 제가 옆 이미지에서 빨간색을 전부 없애고 초록색 채널과 파란색 채널만 남겨뒀어요."


# game/demo_imageops.rpy:125
translate korean demo_imageops_77b0a263:


    # e "The im.Recolor operation can do the same thing, but is more efficient when we're linearly mapping colors."
    e "im.Recolor도 같은 역할을 합니다만, 색상을 선형으로 매핑할 때는 이쪽이 더 효율적입니다."


# game/demo_imageops.rpy:130
translate korean demo_imageops_360723bc:


    # e "The im.Twocolor operation lets you take a black and white image, like this one..."
    e "im.Twocolor 조작은 옆 이미지와 같이 흑백 이미지를 받아서..."


# game/demo_imageops.rpy:135
translate korean demo_imageops_0948998c:


    # e "... and assign colors to replace black and white."
    e "...검정과 하양을 대체할 색상을 설정할 수 있습니다."


# game/demo_imageops.rpy:140
translate korean demo_imageops_75522403:


    # e "The im.MatrixColor operation lets you use a matrix to alter the colors. With the right matrix, you can desaturate colors..."
    e "im.MatrixColor 조작은 여러분이 행렬을 사용해서 색상을 조정할 수 있도록 해 줍니다. 적당한 행렬을 사용하면 채도를 떨어뜨리거나..."


# game/demo_imageops.rpy:145
translate korean demo_imageops_6fe260b9:


    # e "... tint the image blue..."
    e "...색조를 파란색으로 하거나..."


# game/demo_imageops.rpy:150
translate korean demo_imageops_85c10beb:


    # e "... rotate the hue... "
    e "...색상을 회전시키던가..."


# game/demo_imageops.rpy:155
translate korean demo_imageops_09d2d97f:


    # e "... or invert the colors, for a kinda scary look."
    e "...반전시킬 수도 있어요. 조금 무섭네요."


# game/demo_imageops.rpy:160
translate korean demo_imageops_6dd8f586:


    # e "It can even adjust brightness and contrast."
    e "밝기와 대비도 조정할 수 있구요."


# game/demo_imageops.rpy:162
translate korean demo_imageops_ba8ddf3e:


    # e "We've made some of the most common matrices into image operators."
    e "여기서 제가 가장 널리 쓰이는 행렬들을 이미지 조작기로 만들어 보았습니다."


# game/demo_imageops.rpy:167
translate korean demo_imageops_4c62de6f:


    # e "im.Grayscale can make an image grayscale..."
    e "im.Grayscale은 이미지를 회색조로 변환하고..."


# game/demo_imageops.rpy:172
translate korean demo_imageops_7d471e4b:


    # e "... while im.Sepia can sepia-tone an image."
    e "...im.Sepia는 이미지를 세피아 톤으로 합니다."


# game/demo_imageops.rpy:179
translate korean demo_imageops_59ca3a66:


    # e "The im.Alpha operation can adjust the alpha channel on an image, making things partially transparent."
    e "im.Alpha 조작은 이미지의 알파 채널을 조작할 수 있는데요, 이미지를 반투명하게 할 수 있습니다."


# game/demo_imageops.rpy:184
translate korean demo_imageops_514a55db:


    # e "It's useful if a character just happens to be ghost."
    e "캐릭터가 유령이거나 할 때 유용하게 사용되죠."


# game/demo_imageops.rpy:190
translate korean demo_imageops_05fc1200:


    # e "But that isn't the case with me."
    e "전 유령이 아니니 해당사항 없네요."


# game/demo_imageops.rpy:197
translate korean demo_imageops_cf7fbb57:


    # e "Finally, there's im.Flip, which can flip an image horizontally or vertically."
    e "마지막으로, im.Flip이 남았네요. 이는 이미지를 가로로, 또는 세로로 뒤집습니다."


# game/demo_imageops.rpy:199
translate korean demo_imageops_49161c26:


    # e "I think the less I say about this, the better."
    e "백문 불여일견, 어떻게 동작하는지 보는게 빠를 것 같네요."