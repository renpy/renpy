
# game/tutorial_screen_displayables.rpy:3
translate korean screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "꽤 많은 스크린 디스플레이어블이 있어. 여기서는, 가장 중요한 것들에 대해 이야기할 거야."

# game/tutorial_screen_displayables.rpy:9
translate korean screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "어떤 걸 알려줄까?" nointeract

# game/tutorial_screen_displayables.rpy:49
translate korean screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "모든 스크린 언어가 공유 할 수 있는 몇 가지 속성이 있어. 여길 잘 보도록 해."

# game/tutorial_screen_displayables.rpy:57
translate korean screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "우선, 모든 스크린 언어 디스플레이어블은 위치 속성을 지원해. 컨테이너가 디스플레이어블을 지원하면 align, anchor, pos 등의 속성을 사용할 수 있지."

# game/tutorial_screen_displayables.rpy:69
translate korean screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "at 속성은 show 문에서 at 절이 수행하는 것과 같은 방법으로 표시 가능한 객체에 변형을 적용해."

# game/tutorial_screen_displayables.rpy:106
translate korean screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "id 속성은 대개 대화를 표시하는 say 스크린과 함께 사용돼. say 스크린 밖에서는 별로 사용되지 않지."

# game/tutorial_screen_displayables.rpy:108
translate korean screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "그건 렌파이에게 어떤 디스플레이어블이 배경 창인지, '누가' 말하고, '무엇'을 말하는지 알려줘. 이 기능은 캐릭터별 스타일을 적용하고 자동진행(auto-forward) 모드를 지원하는 데 사용돼."

# game/tutorial_screen_displayables.rpy:123
translate korean screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "style 속성을 사용하면 단일 디스플레이어블의 스타일을 지정할 수 있는데,"

# game/tutorial_screen_displayables.rpy:144
translate korean screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "style_prefix 속성은 디스플레이어블과 그 자식에 사용되는 스타일 접두어를 설정해."

# game/tutorial_screen_displayables.rpy:146
translate korean screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "예를 들면, style_prefix 속성이 'green'일 때, vbox는 'green_vbox' 스타일을, 그 안의 글자들은 'green_text'를 취하지."

# game/tutorial_screen_displayables.rpy:150
translate korean screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "이것보다 몇 가지 속성이 더 있는데 나머지는 설명서에서 찾아보도록 해. 하지만 이것들은 게임의 기본 화면에서 볼 수 있는 것들이야."

# game/tutorial_screen_displayables.rpy:156
translate korean add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "때로는 이미지와 같이 화면에 추가할 수 있는 디스플레이어블을 가질 수 있어."

# game/tutorial_screen_displayables.rpy:165
translate korean add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "이것은 add 문을 사용하여 수행할 수 있어. add 문은 이미지나 다른 표시 가능한 객체를 화면에 추가하지."

# game/tutorial_screen_displayables.rpy:167
translate korean add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "이미지를 참조하는 데는 몇 가지 방법이 있어. images 디렉토리에 있거나 image 문으로 정의된 경우 따옴표로 묶은 문자열 안에 이름을 넣을 수 있고."

# game/tutorial_screen_displayables.rpy:176
translate korean add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "이미지는 게임 디렉토리를 기준으로 파일 이름을 참조할 수도 있어."

# game/tutorial_screen_displayables.rpy:185
translate korean add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "add 문을 사용하여 다른 디스플레이어블을 추가 할 수도 있어. 여기서는 단색(Solid) 디스플레이블을 추가하여 블록을 보여주고 있어."

# game/tutorial_screen_displayables.rpy:195
translate korean add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "디스플레이어블 외에도 add 문에 변형 속성을 지정할 수 있어. 이것들은 추가되는 디스플레이어블을 배치하거나 변환할 수 있지."

# game/tutorial_screen_displayables.rpy:207
translate korean add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "물론, add 문은 at 속성을 사용하여 보다 복잡한 변환을 제공할 수 있어."

# game/tutorial_screen_displayables.rpy:222
translate korean text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "스크린 언어 텍스트 명령문은 화면에 표시할 수 있는 글자를 추가해. 표시할 글자를 하나의 인수로 취하는 방식이야."

# game/tutorial_screen_displayables.rpy:224
translate korean text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "모든 디스플레이어블이 취하는 공통 속성 외에도 글자는 텍스트 스타일 속성을 사용해. 예를 들어 size는 텍스트의 크기를 설정하지."

# game/tutorial_screen_displayables.rpy:234
translate korean text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "텍스트 디스플레이어블은 대괄호로 묶인 값을 보간할 수도 있어."

# game/tutorial_screen_displayables.rpy:236
translate korean text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "스크린에 정의된 텍스트 문 변수를 사용하여 글자가 화면에 표시될 때는 정의된 변수보다 우선해."

# game/tutorial_screen_displayables.rpy:238
translate korean text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "이러한 변수는 화면에 지정된 매개 변수이거나 기본, 혹은 파이썬 문으로 정의되거나 SetScreenVariable을 사용하여 설정할 수 있어."

# game/tutorial_screen_displayables.rpy:247
translate korean text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "스크린 안에서 텍스트는 렌파이의 다른 모든 텍스트와 같은 방식으로 작동하기 때문에 여기에 관해서는 더 말할 것이 없어."

# game/tutorial_screen_displayables.rpy:255
translate korean layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "레이아웃(layout) 디스플레이어블은 다른 디스플레이어블을 가져와 화면에 배치해."

# game/tutorial_screen_displayables.rpy:269
translate korean layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "예를 들어, hbox 디스플레이어블은 자식을 가져와 수평으로 배치해."

# game/tutorial_screen_displayables.rpy:284
translate korean layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "vbox 디스플레이어블은 자식을 가져와 수직으로 배치한다는 점을 제외하면 hbox와 비슷해."

# game/tutorial_screen_displayables.rpy:286
translate korean layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "두 상자 모두 box 스타일 속성을 사용하는데, 가장 유용한 것은 자식들 사이에 남겨둘 간격(spacing)이야."

# game/tutorial_screen_displayables.rpy:301
translate korean layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "그리드(grid) 디스플레이어블은 자식을 동일한 크기의 셀 그리드에 표시해. 열의 수와 행의 수를 인수로 취하지."

# game/tutorial_screen_displayables.rpy:303
translate korean layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "그리드가 가득 채워지지 않으면 오류가 발생해. 이 예제에서 빈 셀은 null로 채워졌어."

# game/tutorial_screen_displayables.rpy:305
translate korean layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "박스처럼, 그리드는 간격 속성을 사용해 셀 사이의 간격을 지정할 수 있어."

# game/tutorial_screen_displayables.rpy:321
translate korean layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "그리드는 또한 왼쪽에서 오른쪽으로 채우기 전에 위에서 아래로 채울 수 있도록 이향(transpose) 속성을 사용해."

# game/tutorial_screen_displayables.rpy:338
translate korean layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "그리고 모든 셀이 똑같은 크기라는 것을 시연하기 위해, 하나의 자식이 다른 자식보다 크면 어떻게 되는지 보자."

# game/tutorial_screen_displayables.rpy:353
translate korean layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "고정(fixed) 디스플레이어블은 렌파이의 일반적인 배치 알고리즘을 사용하여 자식들을 표시해. 이를 통해 디스플레이어블을 화면의 어느 곳에나 배치할 수 있어."

# game/tutorial_screen_displayables.rpy:355
translate korean layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "기본적으로, 레이아웃은 사용 가능한 모든 공간을 채우도록 확장돼. 이걸 막으려면 xsize와 ysize 속성을 사용해서 크기를 미리 설정해야 해."

# game/tutorial_screen_displayables.rpy:369
translate korean layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "레이아웃이 아닌 디스플레이어블에 둘 이상의 자식이 주어지면 고정 디스플레이어블이 자동으로 추가되고 자식이 추가되기 때문에 따로 고정 디스플레이어블을 만들 필요가 없어."

# game/tutorial_screen_displayables.rpy:384
translate korean layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "마지막으로, 공간을 절약할 수 있는 한 가지 편한 방법이 있어. 많은 디스플레이어블이 중첩될 때 각각의 레이아웃을 추가하면 들여쓰기 수준이 높아질 수 있을 거야."

# game/tutorial_screen_displayables.rpy:386
translate korean layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "has 문은 레이아웃을 작성한 다음 상위의 모든 자식들을 해당 레이아웃에 추가해. 스크린을 더 읽기 쉽게 편의를 제공하지."

# game/tutorial_screen_displayables.rpy:395
translate korean window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "렌파이가 게임을 위해 생성하는 기본 GUI에서 대부분의 사용자 인터페이스 요소에는 일종의 배경이 예상될 거야."

# game/tutorial_screen_displayables.rpy:405
translate korean window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "배경이 없이는 글자를 읽기가 힘들어. 틀(frame)이 반드시 요구되는 것은 아니지만 많은 화면에는 하나 이상의 틀이 존재해."

# game/tutorial_screen_displayables.rpy:417
translate korean window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "하지만 배경을 추가하면 훨씬 쉬워. 그게 사용자 인터페이스 요소에 배경을 제공하기 위한 두 개의 디스플레이어블이 있는 이유야."

# game/tutorial_screen_displayables.rpy:419
translate korean window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "그 두 개의 디스플레이어블은 틀과 창이야. 틀은 위에서 사용된 거고, 사용자 인터페이스의 임의 부분에 대한 배경을 제공하도록 설계됐어."

# game/tutorial_screen_displayables.rpy:423
translate korean window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "반면에, 창 디스플레이어블은 매우 구체적이야. 그것은 지문 창(text window)을 제공하는 데 사용돼. 내가 말하는 것을 읽고 있다면 지문 창을 보고 있는 거야."

# game/tutorial_screen_displayables.rpy:425
translate korean window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "틀과 창은 모두 창 스타일 속성이 부여될 수 있어. 배경(background)과 창 주위의 여백(margin), 메움(padding)과 같은 항목을 변경할 수 있지."

# game/tutorial_screen_displayables.rpy:433
translate korean button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "가장 유연한 디스플레이어블 중 하나는 버튼(button) 디스플레이어블과 그것의 텍스트 버튼(textbutton), 이미지 버튼(imagebutton) 변체야."

# game/tutorial_screen_displayables.rpy:443
translate korean button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "버튼은 선택된 경우 작업을 실행하는 디스플레이어블이야. 버튼은 마우스, 터치 또는 키보드 및 컨트롤러로 선택할 수 있어."

# game/tutorial_screen_displayables.rpy:445
translate korean button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "동작(action)은 변수 설정, 화면 표시, 레이블로 점프 또는 값 반환과 같은 많은 작업을 수행 할 수 있어. {a=https://www.renpy.org/doc/html/screen_actions.html}렌파이 문서{/a}에는 많은 동작이 있고, 네가 원하는 동작을 만들 수도 있어."

# game/tutorial_screen_displayables.rpy:458
translate korean button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "게다가 버튼이 포커스를 잃었을 때 동작을 실행할 수도 있지."

# game/tutorial_screen_displayables.rpy:473
translate korean button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "버튼은 다른 디스플레이어블을 자식으로 사용해. 자식은 레이아웃이 될 수 있기 때문에 원하는 만큼의 자식을 취하게 할 수 있어."

# game/tutorial_screen_displayables.rpy:483
translate korean button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "많은 상황에서, 버튼에는 글자가 표시돼. 이걸 편하게 하기 위해서, 글자를 인자로 취하는 텍스트 버튼(textbutton) 디스플레이어블이 있어."

# game/tutorial_screen_displayables.rpy:485
translate korean button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "텍스트 버튼 디스플레이어블은 버튼 글자의 스타일을 관리하기 때문에 기본 GUI에서 가장 자주 사용되는 버튼 유형이야."

# game/tutorial_screen_displayables.rpy:498
translate korean button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "이미지 버튼(imagebutton) 역시 버튼을 표시할 수 있는 각 상태에 대해 하나씩 디스플레이어블 가져와 버튼으로 표시하지."

# game/tutorial_screen_displayables.rpy:500
translate korean button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "이미지 버튼을 사용하면 버튼의 모양을 가장 잘 제어할 수 있지만, 번역하기가 어려운 데다가 게임 창의 크기를 조정하면 모양이 좋아 보이지 않을 수 있어."

# game/tutorial_screen_displayables.rpy:522
translate korean button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "버튼은 배경(background), 여백(margin) 및 메움(padding)을 지정하는 데 사용되는 창 스타일 속성을 사용해. 또한 맴돔(hover)에서 재생할 사운드와 같은 버튼 관련 속성을 사용해."

# game/tutorial_screen_displayables.rpy:524
translate korean button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "버튼과 함께 사용하면 스타일 속성에 유휴(idle) 상태 및 맴돔(hover)과 같은 접두사를 지정하여 버튼 상태로 속성을 변경할 수 있어."

# game/tutorial_screen_displayables.rpy:526
translate korean button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "텍스트 버튼에는 글자 스타일 접두사가 붙어. 이것은 내부적으로 생성한 디스플레이어블에 적용돼."

# game/tutorial_screen_displayables.rpy:558
translate korean button_displayables_b89d12aa:

    # e "Of course, it's prety rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "물론, 그런 스크린에서 버튼을 사용자 정의하는 경우는 드물지. 대신에 사용자 정의 스타일을 만들어 렌파이에게 사용하도록 알려주는 거야."

# game/tutorial_screen_displayables.rpy:577
translate korean bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "bar와 vbar 디스플레이어블은 값을 나타내는 막대를 표시하는 유연한 디스플레이어블이야. 이 값은 정적, 애니메이션 또는 플레이어에 의해 조정될 수 있어."

# game/tutorial_screen_displayables.rpy:579
translate korean bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "값(value) 속성은 막대의 값과 범위를 결정하는 객체인 BarValue를 제공해. 여기에서 StaticValue는 범위를 100으로 설정하고 값은 66으로 설정하여 막대의 3 분의 2가 채워지지."

# game/tutorial_screen_displayables.rpy:581
translate korean bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "사용할 수 있는 모든 BarValues ​​목록은 {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}렌파이 설명서{/a}에 있어."

# game/tutorial_screen_displayables.rpy:583
translate korean bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "이 예제에서 우리는 프레임에 xsize 속성을 부여했어. 그러지 않았다면 막대가 사용 가능한 모든 수평 공간을 채웠을 거야."

# game/tutorial_screen_displayables.rpy:600
translate korean bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "기본 GUI에 정의된 몇 가지 다른 막대 스타일이 있어. 스타일은 style 속성과 값에 의해 선택된 기본으로 정해져."

# game/tutorial_screen_displayables.rpy:602
translate korean bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "상단 스타일은 '막대(bar)'스타일이야. 이 값은 플레이어가 조정할 수 없는 값(예: 수명 또는 진행률 막대)을 표시하는 데 사용돼."

# game/tutorial_screen_displayables.rpy:604
translate korean bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "중간 스타일은 '슬라이더(slider)' 값이야. 볼륨 설정과 같이 플레이어가 조정할 것으로 예상되는 값에 사용돼."

# game/tutorial_screen_displayables.rpy:606
translate korean bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "마지막으로, 하단은 수평 스크롤 막대에 사용되는 '스크롤바(scrollbar)' 스타일이야. 스크롤 막대로 사용하면 막대의 이동이 가능한 가운데는 뷰포트의 가시 영역을 반영하기 위해 크기가 변경돼."

# game/tutorial_screen_displayables.rpy:623
translate korean bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "vbar 디스플레이어블은 기본적으로 수직 스타일-'vbar', 'vslider', 'vscrollbar'-이라는 걸 제외하면 bar 디스플레이어블과 비슷해."

# game/tutorial_screen_displayables.rpy:626
translate korean bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "막대는 Bar 스타일 속성을 사용해서 모양과 느낌을 멋지게 사용자 정의할 수 있어. 막대, 슬라이더 및 스크롤 막대 스타일의 차이점을 살펴보도록 해."

# game/tutorial_screen_displayables.rpy:635
translate korean imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "이미지맵(imagemap)은 두 개 이상의 이미지를 사용하여 버튼과 막대를 표시해. 먼저 이미지맵을 사용하는 예를 보여줄게."

# game/tutorial_screen_displayables.rpy:657
translate korean swimming_405542a5:

    # e "You chose swimming."
    e "수영을 선택했어."

# game/tutorial_screen_displayables.rpy:659
translate korean swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "수영은 정말 재밌지만, 나는 오늘 수영복을 가져오지 않았어."

# game/tutorial_screen_displayables.rpy:665
translate korean science_83e5c0cc:

    # e "You chose science."
    e "과학을 선택했어."

# game/tutorial_screen_displayables.rpy:667
translate korean science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "몇몇 학교는 경쟁적인 과학 팀을 가지고 있다고 들었지만, 나에게 있어 연구는 서둘러서는 안 되는 거야."

# game/tutorial_screen_displayables.rpy:672
translate korean art_d2a94440:

    # e "You chose art."
    e "아트를 선택했어."

# game/tutorial_screen_displayables.rpy:674
translate korean art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "정말 좋은 배경 아트는 만들기 어려워. 그래서 많은 게임들이 필터링된 사진을 사용하지. 어쩌면 너는 그것을 바꿀 수 있을지도."

# game/tutorial_screen_displayables.rpy:680
translate korean home_373ea9a5:

    # e "You chose to go home."
    e "집으로 가는 것을 선택했어."

# game/tutorial_screen_displayables.rpy:686
translate korean imagemap_done_48eca0a4:

    # e "Anyway..."
    e "어쨌든..."

# game/tutorial_screen_displayables.rpy:691
translate korean imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "이미지맵을 결합하는 방법을 설명하기 위해 작은 이미지맵을 구성하는 다섯 개의 이미지를 보여줄게."

# game/tutorial_screen_displayables.rpy:697
translate korean imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "idle 이미지는 이미지 맵의 배경, 초점이 맞춰지지 않았거나 선택하지 않은 핫스팟 버튼 및 초점에서 벗어난 막대의 빈 부분에 사용돼."

# game/tutorial_screen_displayables.rpy:703
translate korean imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "hover 이미지는 초점은 맞춰졌지만 선택되지 않은 핫스팟과 초점이 맞춰진 막대의 빈 부분에 사용되고."

# game/tutorial_screen_displayables.rpy:705
translate korean imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "이 이미지에서 막대 및 버튼이 어떻게 강조 표시되는지 확인해봐. 스크린의 일부로 이들을 표시할 때 그 중 하나에 초점이 맞춰져."

# game/tutorial_screen_displayables.rpy:711
translate korean imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "이 selected_idle 이미지와 같은 선택된 이미지는 채워지는 막대의 부분, 현재 화면과 체크된 상자와 같은 선택된 버튼에 사용돼."

# game/tutorial_screen_displayables.rpy:717
translate korean imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "이건 selected_hover 이미지야. 여기에 있는 버튼은 선택된 것으로 표시되지 않기 때문에 절대 표시되지 않아."

# game/tutorial_screen_displayables.rpy:723
translate korean imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "마지막으로, 핫스팟과 상호작용할 수 없을 때 사용되는 insensitive 이미지가 주어질 수 있어."

# game/tutorial_screen_displayables.rpy:728
translate korean imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "이미지맵은 단지 이미지에만 국한되지 않아. 모든 디스플레이어블은 이미지가 예상되는 곳에 사용될 수 있어."

# game/tutorial_screen_displayables.rpy:743
translate korean imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "이건 5개의 이미지를 사용하여 생성 된 이미지맵이야. 원하는 경우 상호작용할 수 있어."

# game/tutorial_screen_displayables.rpy:755
translate korean imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "좀 더 간략하게하기 위해 '%%s'를 'idle', 'hover', 'selected_idle', 'selected_hover'또는 'insensitive'로 적절히 대체하는 자동(auto) 속성으로 5개의 이미지를 대체할 수 있어."

# game/tutorial_screen_displayables.rpy:757
translate korean imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "게임에서 반드시 필요하지 않은 경우에는 selected와 insensitive 이미지는 생략해도 돼. 렌파이는 idle이나 hover 이미지를 사용해 그것들을 대체할 거야."

# game/tutorial_screen_displayables.rpy:759
translate korean imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "hotspot과 hotbar 문은 버튼이나 바처럼 행동해야 하는 이미지 맵 영역을 나타내는데,"

# game/tutorial_screen_displayables.rpy:761
translate korean imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "이것들은 모두 영역의 좌표(x, y, width, height) 형식을 취해."

# game/tutorial_screen_displayables.rpy:763
translate korean imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "핫스팟은 핫스팟이 활성화될 때 실행되는 작업을 수행해. 버튼처럼 커서를 올리거나 내릴 때 실행되는 작업을 수행할 수도 있지."

# game/tutorial_screen_displayables.rpy:765
translate korean imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "hotbar는 막대가 얼마나 꽉 찼는지 설명하는 BarValue 객체와 막대, bar와 vbar 막대가 표시해야 하는 값의 범위를 사용해."

# game/tutorial_screen_displayables.rpy:772
translate korean imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "유용한 패턴은 레이블로 점프하는 핫스팟이 있는 이미지맵 스크린을 정의하고 call screen 명령문을 사용하여 호출하는 거야."

# game/tutorial_screen_displayables.rpy:774
translate korean imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "내가 전에 보여준 학교 예제가 바로 그 방식을 취하고 있었어. 여기에 있는 스크립트를 봐. 스크립트 자체는 길지만 이미지맵은 매우 간단해."

# game/tutorial_screen_displayables.rpy:778
translate korean imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "이미지맵은 장점과 단점이 있어. 디자이너가 쉽고 예쁘게 만들 수 있는 한 편 번역하기가 어려울 수 있고, 창 크기가 조정되면 이미지에 포함된 텍스트가 흐릿하게 보여질 수도 있어."

# game/tutorial_screen_displayables.rpy:780
translate korean imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "프로젝트에 이미지맵 사용여부를 결정하는 것은 너와 네 팀에게 달려 있어."

# game/tutorial_screen_displayables.rpy:787
translate korean viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "때로는 화면보다 더 큰 것을 보여주고 싶을 수 있어. 그럴 때 필요한 것이 뷰포트 디스플레이어블이야."

# game/tutorial_screen_displayables.rpy:803
translate korean viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "이건 화면보다 훨씬 큰 단일 이미지를 표시하는 데 사용되는 간단한 뷰포트의 예제야. 뷰포트는 스크린의 크기를 확장하기 때문에 xysize 속성을 사용해 뷰포트를 작게 만들었어."

# game/tutorial_screen_displayables.rpy:805
translate korean viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "기본적으로 뷰포트는 움직일 수 없지만, draggable, mousewheel, arrowkeys 속성을 사용해 여러 방법으로 이동하게 할 수 있어."

# game/tutorial_screen_displayables.rpy:820
translate korean viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "뷰포트에 edgescroll 속성을 지정하면 마우스가 가장자리 근처에 있을 때 뷰포트가 자동으로 스크롤돼. 두 숫자는 가장자리의 크기와 초당 픽셀 단위의 속도야."

# game/tutorial_screen_displayables.rpy:839
translate korean viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "뷰포트에 scrollbars 속성을 지정하면 스크롤바로 둘러싸게 돼. scrollbars 속성은 값으로 전체(both), 수평(horizontal), 그리고 수직(vertical)을 사용할 수 있고."

# game/tutorial_screen_displayables.rpy:841
translate korean viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "spacing 속성은 뷰포트와 스크롤 막대 사이의 간격을 픽셀 단위로 제어해."

# game/tutorial_screen_displayables.rpy:864
translate korean viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "xinitial과 yinitial 속성은 스크롤 가능한 양으로 스크롤의 초기 위치를 설정해."

# game/tutorial_screen_displayables.rpy:885
translate korean viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "마지막으로는 child_size 속성이 있어. 그것이 무엇을 하는지 설명하기 위해, 그 속성을 가지고 있지 않을 때 일어나는 일을 먼저 보여줄게."

# game/tutorial_screen_displayables.rpy:887
translate korean viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "보다시피 텍스트가 줄 바꿈돼. 렌파이가 제공하는 공간이 충분히 크지 않기 때문이야."

# game/tutorial_screen_displayables.rpy:909
translate korean viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "스크린에 child_size 속성을 사용하면, 자식들에게 더 많은 공간을 제공하여 스크롤을 허용하게 할 수 있어. 거기에는 수평(horizontal) 및 수직(vertical) 크기가 필요해. 만약 하나의 구성 요소가 None이면 뷰포트의 크기를 사용해."

# game/tutorial_screen_displayables.rpy:936
translate korean viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "마지막으로, vpgrid 디스플레이어블이 있어. 뷰포트와 그리드를 하나의 디스플레이어블에 하는 건데, 모든 자식을 그릴 필요가 없기 때문에 뷰포트와 그리드를 하나의 디스플레이 어블에 결합해."

# game/tutorial_screen_displayables.rpy:938
translate korean viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "vpgrid는 자식의 행(cols)과 열(rows)을 제공하는 속성을 사용해. 하나를 생략하면, 렌파이는 그것을 자식의 수와 다른 속성으로부터 계산해"

translate korean strings:

    # tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "모든 디스플레이어블이 공유하는 공통 속성."

    # tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "그림과 다른 디스플레이어블 추가."

    # tutorial_screen_displayables.rpy:9
    old "Text."
    new "글자."

    # tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "박스와 다른 레이아웃."

    # tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "틀과 창."

    # tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "버튼."

    # tutorial_screen_displayables.rpy:9
    old "Bars."
    new "막대."

    # tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "뷰포트."

    # tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "이미지맵."

    # tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "이전 단계로."

    # tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "이건 위치 속성을 사용해."

    # tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "그리고 세상이 거꾸로 됐어..."

    # tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "탱크의 비행 압력."

    # tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "내부 전원 켜기."

    # tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "실행됐어."

    # tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "이륙!"

    # tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "답은 [answer]이야."

    # tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "글자 태그는 스크린에서 {color=#c8ffc8}작동해{/color}."

    # tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "크게"

    # tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "이건 스크린이야."

    # tutorial_screen_displayables.rpy:402
    old "Okay"
    new "알았어"

    # tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "버튼을 클릭했어."

    # tutorial_screen_displayables.rpy:441
    old "Click me."
    new "나를 클릭해."

    # tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "버튼 위에 맴돌고 있어."

    # tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "버튼을 벗어났어."

    # tutorial_screen_displayables.rpy:470
    old "Heal"
    new "치유"

    # tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "이건 텍스트 버튼이야."

    # tutorial_screen_displayables.rpy:539
    old "Or me."
    new "또는 나."

    # tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "다른 버튼을 클릭했어."

    # tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "이 글자는 뷰포트의 넓이보다 넓게 작성돼 있어."

