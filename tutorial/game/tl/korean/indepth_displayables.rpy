
# game/indepth_displayables.rpy:15
translate korean simple_displayables_db46fd25:

    # e "Ren'Py has the concept of a displayable, which is something like an image that can be shown and hidden."
    e "렌파이는 보여지거나 숨길 수 있는 이미지와 같은 디스플레이어블이라는 개념을 가지고 있어."

# game/indepth_displayables.rpy:22
translate korean simple_displayables_bfe78cb7:

    # e "The image statement is used to give an image name to a displayable. The easy way is to simply give an image filename."
    e "이미지(image) 구문은 디스플레이어블에 이미지 이름을 부여하는 데 사용돼. 간단하게는 이미지 파일을 지정하는 쉬운 방법이 있어."

# game/indepth_displayables.rpy:29
translate korean simple_displayables_cef4598b:

    # e "But that's not the only thing that an image can refer to. When the string doesn't have a dot in it, Ren'Py interprets that as a reference to a second image."
    e "그렇지만 그게 이미지가 참조할 수 있는 유일한 것은 아냐. 문자열에 점이 없으면 렌파이는 이를 두 번째 이미지에 대한 참조로 해석해."

# game/indepth_displayables.rpy:41
translate korean simple_displayables_a661fb63:

    # e "The string can also contain a color code, consisting of hexadecimal digits, just like the colors used by web browsers."
    e "문자열에는 웹 브라우저에서 사용되는 색상과 마찬가지로 16진수 숫자로 구성된 색상 코드가 포함될 수도 있어."

# game/indepth_displayables.rpy:43
translate korean simple_displayables_7f2efb23:

    # e "Three or six digit colors are opaque, containing red, green, and blue values. The four and eight digit versions append alpha, allowing translucent colors."
    e "3자리 또는 6자리 색상은 불투명하고, 빨강, 초록, 파랑 값을 포함해. 4자리 또는 8자리 색상은 알파 값을 포함해 반투명 색상을 허용하지."

# game/indepth_displayables.rpy:53
translate korean simple_displayables_9cd108c6:

    # e "The Transform displayable takes a displayable and can apply transform properties to it."
    e "변환(Transform) 디스플레이어블은 디스플레이어블에 변환 속성을 적용할 수 있어."

# game/indepth_displayables.rpy:55
translate korean simple_displayables_f8e1ba3f:

    # e "Notice how, since it takes a displayable, it can take another image. In fact, it can take any displayable defined here."
    e "예를 들어 디스플레이어블을 사용하기 때문에 다른 이미지를 사용할 수 있어. 사실은, 정의된 어떤 디스플레이어블이든 사용할 수 있지."

# game/indepth_displayables.rpy:63
translate korean simple_displayables_c6e39078:

    # e "There's a more complete form of Solid, that can take style properties. This lets us change the size of the Solid, where normally it fills the screen."
    e "스타일 속성을 취할 수 있는 보다 완벽한 솔리드(Solid) 형식이 있는데, 이렇게 하면 화면을 채우는 솔리드의 크기를 변경할 수 있어."

# game/indepth_displayables.rpy:72
translate korean simple_displayables_b102a029:

    # e "The Text displayable lets Ren'Py treat text as if it was an image."
    e "텍스트(Text) 디스플레이어블은 렌파이가 텍스트를 이미지처럼 취급하도록 하지."

# game/indepth_displayables.rpy:80
translate korean simple_displayables_0befbee0:

    # e "This means that we can apply other displayables, like Transform, to Text in the same way we do to images."
    e "이건 이미지와 같은 방식으로 변환(Transform)과 같은 다른 디스플레이어블을 텍스트에 적용할 수 있다는 걸 의미해."

# game/indepth_displayables.rpy:91
translate korean simple_displayables_fcf2325f:

    # e "The Composite displayable lets us group multiple displayables together into a single one, from bottom to top."
    e "복합(Composite) 디스플레이어블은 여러 디스플레이어블을 하나의 그룹으로 취하는 거야."

# game/indepth_displayables.rpy:101
translate korean simple_displayables_3dc0050e:

    # e "Some displayables are often used to customize the Ren'Py interface, with the Frame displayable being one of them. The frame displayable takes another displayable, and the size of the left, top, right, and bottom borders."
    e "일부 디스플레이어블은 렌파이의 인터페이스를 사용자 정의하는 데 종종 사용되고, 틀(Frame) 디스플레이어블은 그중 하나야. 틀 디스플레이어블은 왼쪽과 위쪽, 오른쪽 및 아래쪽 테두리의 크기를 취하는 또 다른 디스플레이어블이야."

# game/indepth_displayables.rpy:111
translate korean simple_displayables_801b7910:

    # e "The Frame displayable expands or shrinks to fit the area available to it. It does this by scaling the center in two dimensions and the sides in one, while keeping the corners the same size."
    e "틀 디스플레이어블은 사용 가능한 영역에 맞게 확장되거나 축소돼. 모서리를 같은 크기로 유지하면서 중심을 2차원으로, 측면을 1로 크기 조정하여 이 작업을 수행하지."

# game/indepth_displayables.rpy:118
translate korean simple_displayables_00603985:

    # e "A Frame can also tile sections of the displayable supplied to it, rather than scaling."
    e "틀은 제공된 디스플레이어블의 구역을 타일링-스케일링보다 나은- 할 수도 있어."

# game/indepth_displayables.rpy:126
translate korean simple_displayables_d8b23480:

    # e "Frames might look a little weird in the abstract, but when used with a texture, you can see how we create scalable interface components."
    e "틀은 추상적으로 약간 이상하게 보일 수 있지만 텍스처와 함께 사용하면 확장 가능한 인터페이스 구성 요소를 어떻게 만드는지 알 수 있어."

# game/indepth_displayables.rpy:132
translate korean simple_displayables_ae3f35f5:

    # e "These are just the simplest displayables, the ones you'll use directly the most often."
    e "이러한 것들은 가장 단순하고 자주 사용되는 디스플레이어블이야."

# game/indepth_displayables.rpy:134
translate korean simple_displayables_de555a92:

    # e "You can even write custom displayables for minigames, if you're proficient at Python. But for many visual novels, these will be all you'll need."
    e "파이썬을 능숙하게 사용한다면, 미니 게임용 커스텀 디스플레이어블을 작성할 수도 있어. 하지만 대부분의 비주얼 노벨에선, 여기까지가 너에게 필요한 내용 전부야."

translate korean strings:

    # indepth_displayables.rpy:67
    old "This is a text displayable."
    new "이건 텍스트 디스플레이어블이야."

