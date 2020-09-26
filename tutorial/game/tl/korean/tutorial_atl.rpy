
# game/tutorial_atl.rpy:205
translate korean tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "이 길라잡이에서는 렌파이가 대상을 어떤 방식으로 화면에 배치하는지 알아볼 거야. 그러기 전에, 파이썬이 어떻게 숫자를 다루는지 알려줄게."

# game/tutorial_atl.rpy:207
translate korean tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "파이썬에는 숫자를 구성하는 '정수'와 '부동 소수점'의 두 가지 주요 종류가 있어. 정수는 모두 숫자로 구성되는 반면에 부동 소수점의 숫자에는 소수점이 있어."

# game/tutorial_atl.rpy:209
translate korean tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "예를 들어, 100은 '정수', 0.5는 부동 소수점 혹은 짧게 '실수'야. 이 시스템에는 정수 0과 실수 0.0인 두 개의 0이 있지."

# game/tutorial_atl.rpy:211
translate korean tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "렌파이는 절대 좌표를 나타내는데 정수를 사용하고 알려진 크기의 영역을 나타낼 때 실수를 사용해."

# game/tutorial_atl.rpy:213
translate korean tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "우리가 무언가의 위치를 잡을 때, 그 영역은 일반적으로 화면 전체일 거야."

# game/tutorial_atl.rpy:215
translate korean tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "이제 나를 화면 밖으로 내보내고, 위치들이 어디에 있는지 보여줄게."

# game/tutorial_atl.rpy:229
translate korean tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "원점은 화면의 왼쪽 위 모서리야. 거기는 x좌표(xpos)와 y좌표(ypos)가 모두 0인 곳이지."

# game/tutorial_atl.rpy:235
translate korean tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "xpos를 늘리면 오른쪽으로 이동해. 현재 여기의 xpos는 .5. 총 화면 너비의 절반이야."

# game/tutorial_atl.rpy:240
translate korean tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "xpos를 1.0으로 늘리면 화면의 오른쪽 모서리로 이동해."

# game/tutorial_atl.rpy:246
translate korean tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "우리는 정수로 절대 xpos를 사용할 수도 있어. 이 경우 xpos는 화면의 왼쪽에서부터 절대 픽셀 수로 지정돼. 예를 들어, 이 창은 가로가 1280 픽셀이니까 640의 xpos를 사용하면 대상이 가운데 상단으로 적용되지."

# game/tutorial_atl.rpy:248
translate korean tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "y좌표 혹은 ypos는 같은 방식으로 작동해. 지금 우리의 ypos 값은 0.0이야."

# game/tutorial_atl.rpy:254
translate korean tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "여기는 ypos 0.5."

# game/tutorial_atl.rpy:259
translate korean tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "1.0의 ypos 위치는 화면 하단이야. 잘 살펴보면 텍스트 창 아래에서 위치 표시기가 회전하는 것이 보일 거야."

# game/tutorial_atl.rpy:261
translate korean tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "xpos와 마찬가지로 ypos도 정수가 될 수 있어. 이 경우에, ypos는 화면 상단에서부터의 총 픽셀 수를 나타내."

# game/tutorial_atl.rpy:267
translate korean tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "이 위치가 어디인지 추측할 수 있겠어?" nointeract

# game/tutorial_atl.rpy:273
translate korean tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "미안, 그게 아니야. xpos는 .75, ypos는 .25야."

# game/tutorial_atl.rpy:275
translate korean tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "다른 말로는, 왼쪽으로부터 75%%를 온 거고 위쪽으로부터 25%%를 온 거야."

# game/tutorial_atl.rpy:279
translate korean tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "그래! 잘 맞췄어."

# game/tutorial_atl.rpy:283
translate korean tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "미안, 그게 아니야. xpos는 .75, ypos는 .25야."

# game/tutorial_atl.rpy:285
translate korean tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "다른 말로는, 왼쪽으로부터 75%%를 온 거고 위쪽으로부터 25%%를 온 거야."

# game/tutorial_atl.rpy:299
translate korean tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "두 번째 위치는 닻 혹은 앵커(anchor)야. anchor는 배치되는 대상의 지점이야."

# game/tutorial_atl.rpy:301
translate korean tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "예들 들면, 여기에 우리는 0.0의 xanchor와 0.0의 yanchor를 가지고 있어. 그건 로고 이미지의 왼쪽 상단에 있지."

# game/tutorial_atl.rpy:306
translate korean tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "우리가 xanchor를 1.0으로 늘리면, anchor는 이미지의 오른쪽으로 갈 거야."

# game/tutorial_atl.rpy:311
translate korean tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "비슷하게, xanchor와 yanchor 모두 1.0이면, anchor는 오른쪽 하단이 되지."

# game/tutorial_atl.rpy:318
translate korean tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "화면에 이미지를 배치하려면 위치와 앵커가 모두 필요해."

# game/tutorial_atl.rpy:326
translate korean tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "그런 다음 위치와 앵커가 모두 화면의 같은 지점에 오도록 앵커를 정렬해."

# game/tutorial_atl.rpy:336
translate korean tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "두 요소를 모두 왼쪽 상단 모서리에 놓으면 이미지가 화면의 왼쪽 상단 모서리로 이동하지."

# game/tutorial_atl.rpy:345
translate korean tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "위치와 앵커의 올바른 조합을 사용하면 이미지의 크기를 알지 못해도 화면의 모든 위치를 지정할 수 있어."

# game/tutorial_atl.rpy:357
translate korean tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "xpos와 xanchor를 종종 같은 값으로 설정하는 것이 유용해. 우리는 그걸 xalign이라 부르고, 화면에 분수 위치를 부여하는 거야."

# game/tutorial_atl.rpy:362
translate korean tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "예를 들어, xalign을 0.0으로 설정하면, 대상은 화면의 왼쪽으로 정렬되는 거야."

# game/tutorial_atl.rpy:367
translate korean tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "xalign을 1.0으로 설정하면, 화면의 오른쪽으로 정렬되는 거지."

# game/tutorial_atl.rpy:372
translate korean tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "xalign을 0.5로 설정하면 화면의 중앙으로 돌아가."

# game/tutorial_atl.rpy:374
translate korean tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "yalign을 설정하는 것은 좌표가 y값인 것을 제외하고는 비슷해."

# game/tutorial_atl.rpy:376
translate korean tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "xalign은 xpos와 xanchor를 같은 값으로 설정하고 yalign은 ypos와 yanchor를 같은 값으로 설정한다는 걸 기억해둬."

# game/tutorial_atl.rpy:381
translate korean tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "xcenter 및 ycenter 속성은 이미지의 가운데 위치야. 여기서, xcenter를 .75로 설정하면 이미지의 가운데는 화면의 오른쪽으로 4분의 3이야."

# game/tutorial_atl.rpy:386
translate korean tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "xalign과 xcenter의 차이점은 xcenter가 1.0이고 이미지의 절반이 화면의 오른쪽 밖으로 나갔을 때 명백히 드러나."

# game/tutorial_atl.rpy:394
translate korean tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "xoffset과 yoffset 속성은 다른 속성들 다음에 적용되고, 오른쪽 또는 아래쪽에 있는 것들을 각각 상쇄해."

# game/tutorial_atl.rpy:399
translate korean tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "물론, 너는 offset에 음수를 사용해서 대상을 왼쪽과 상단으로 놓을 수 있어."

# game/tutorial_atl.rpy:404
translate korean tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "마지막으로, align, pos, anchor 및 center 같은 속성들은 결합되어 있다는 걸 명심해. 정렬(align)은 한 쌍의 숫자를 취해 xalign을 첫 번째로, yalign을 두 번째로 설정해야 해. 나머지는 비슷해."

# game/tutorial_atl.rpy:411
translate korean tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "위치를 이해하면 변형(transform)을 사용해서 대상을 움직일 수 있어."

# game/tutorial_atl.rpy:418
translate korean tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "렌파이는 변형(transform)을 사용하여 이미지의 애니메이션, 조작 및 배치를 수행해. 우리는 방금 사용할 수 있는 변형 중 가장 간단한 것을 봤어."

# game/tutorial_atl.rpy:425
translate korean tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "변형은 오른쪽 변형(at right)과 같이 화면의 어딘가에 이미지를 배치하는 정말 간단한 작업이 될 수 있어."

# game/tutorial_atl.rpy:429
translate korean tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "하지만 변형은 애니메이션이나 효과가 혼합된 훨씬 복잡한 작업을 할 수도 있어. 시범으로, 완전무상 록 콘서트에 가자!"

# game/tutorial_atl.rpy:437
translate korean tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "그럼..., 완전무상 록 콘서트를 즐겨!"

# game/tutorial_atl.rpy:445
translate korean tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "그것은 많은 작업이었지만 작은 부품들로 만들어졌어."

# game/tutorial_atl.rpy:447
translate korean tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "렌파이에서 대부분의 변형은 애니메이션과 변형 언어(ATL, Animation and Transform Language)를 사용해 만들어졌어."

# game/tutorial_atl.rpy:449
translate korean tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "렌파이에는 현재 ATL이 사용될 수 있는 세 장소가 있어."

# game/tutorial_atl.rpy:454
translate korean tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "첫 번째는 이미지(image) 명령문의 부품으로 사용되는 거야. 디스플레이어블 대신에, 이미지는 ATL 코드의 블록으로 정의될 수 있지."

# game/tutorial_atl.rpy:456
translate korean tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "이 방법을 사용했을 때, 우리는 ATL이 실제로 보여줄 디스플레이어블을 포함하고 있는지 확인해야 해."

# game/tutorial_atl.rpy:461
translate korean tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "두 번째 방법은 변형(transform) 명령문을 통해 사용하는 거야. 이렇게하면 ATL 블록을 파이썬 변수에 할당해서 at 절이나 다른 변형에서 사용할 수 있어."

# game/tutorial_atl.rpy:473
translate korean tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "마지막으로, ATL 블록은 at 절을 대신해 show 명령문의 부품으로 사용될 수 있어."

# game/tutorial_atl.rpy:480
translate korean tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though a click your click stopped the motion, the image remains in the same place."
    e "ATL이 show 명령문의 부품으로 사용될 때, 변형이 변경되더라도 특성의 값은 존재해. 따라서 클릭으로 동작이 중단되더라도 이미지는 같은 위치에 유지되지."

# game/tutorial_atl.rpy:488
translate korean tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "우리는 ATL의 핵심을 '결합성'이라 불러. ATL은 상대적으로 간단한 명령으로 구성되어 있는데, 복잡한 명령을 함께 사용하여 복잡한 변형을 만들 수 있어."

# game/tutorial_atl.rpy:490
translate korean tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "ATL이 어떻게 작동하는지 알려주기 전에, 애니메이션과 변형이 무엇인지부터 설명할게."

# game/tutorial_atl.rpy:495
translate korean tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "애니메이션은 표시되는 디스플레이어블이 변경되는 거야. 예를 들어, 지금 나는 내 표정을 바꾸고 있어."

# game/tutorial_atl.rpy:522
translate korean tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "변형은 이미지를 움직이거나 왜곡시키는 거야. 여기에는 화면에 배치, 확대 및 축소, 회전 및 불투명도 변경이 포함돼."

# game/tutorial_atl.rpy:530
translate korean tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "ATL의 소개를 위해, 간단한 애니메이션을 보면서 시작할게. 다음은 이미지 명령문에 포함된 다섯 줄로 구성된 ATL 코드야."

# game/tutorial_atl.rpy:532
translate korean tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "디스플레이어블의 변경을 위해, ATL의 한 줄 씩 간단히 설명할게. 여기에서, 우리는 두 이미지 사이를 왔다갔다 해."

# game/tutorial_atl.rpy:534
translate korean tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "우리가 이미지를 정의하고 있기 때문에, ATL의 첫 번째 줄은 디스플레이어블을 제공해야 해. 그렇지 않으면 보여줄 것이 없으니까."

# game/tutorial_atl.rpy:536
translate korean tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "두 번째 및 네 번째 줄은 일시 중지(pause) 명령문으로, ATL이 이어지기 전에 각각 0.5초 동안 대기 시간을 주고 있어. 어떻게 이미지들 사이에 지연이 발생하는지 알려주는 거야."

# game/tutorial_atl.rpy:538
translate korean tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "마지막 줄은 반복(repeat) 명령문이야. 이건 현재의 ATL 블록을 재실행하는 거야. 반복 명령문은 블록별로 한 번만 쓸 수 있어."

# game/tutorial_atl.rpy:543
translate korean tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "우리가 repeat 2를 쓴다면, 애니메이션은 두 번 반복한 후에 멈추게 돼있어."

# game/tutorial_atl.rpy:548
translate korean tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "반복 명령문을 생략하면 ATL 코드 블록의 끝에 도달했을 때 애니메이션이 중지돼."

# game/tutorial_atl.rpy:554
translate korean tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "기본적으로, 디스플레이어블은 즉시 변경돼. with 절의 사용으로 디스플레이어블 사이를 전환할 수 있기도 해."

# game/tutorial_atl.rpy:561
translate korean tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "애니메이션이 끝났으니 ATL을 사용하여 이미지를 화면에 배치하는 방법부터 시작해서 이미지를 변형하는 방법을 알아보자."

# game/tutorial_atl.rpy:570
translate korean tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "우리가 할 수 있는 가장 간단한 일은 이미지를 정적으로 배치하는 거야. 위치 속성의 이름 뒤에 속성 값을 지정하면 되는 일이지."

# game/tutorial_atl.rpy:575
translate korean tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "몇 가지 더 많은 명령문을 통해 화면에서 대상을 움직이게 할 수 있어."

# game/tutorial_atl.rpy:577
translate korean tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "이 예제는 화면의 오른쪽 상단에서 이미지를 시작하고 잠시 기다려. 그런 다음 왼쪽으로 이동하고 잠시 기다린 다음 반복해."

# game/tutorial_atl.rpy:579
translate korean tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "일시 중지 및 반복 명령문은 우리가 애니메이션에서 사용한 것과 같아. 그것들은 ATL 코드를 통해 작동해."

# game/tutorial_atl.rpy:584
translate korean tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "화면에서 이미지가 순간이동하는 것은 그다지 유용하지 않아. 그게 ATL이 보간 명령문을 갖는 이유야."

# game/tutorial_atl.rpy:586
translate korean tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "보간문을 사용하면 변형 속성 값을 이전 값에서 새 값으로 부드럽게 변경할 수 있어."

# game/tutorial_atl.rpy:588
translate korean tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "여기, 우리는 두 번째 ATL 행에 보간 명령문이 있는 것을 확인할 수 있어. 그건 시간 함수로 시작하고, 이 경우는 선형(linear)이야."

# game/tutorial_atl.rpy:590
translate korean tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "이 코드에서 그것(linear)은 3초의 시간을 따르고 있어. 시간이 진행되면서 뒤에 오는 새로운 속성(xalign) 값을 따르게 되지."

# game/tutorial_atl.rpy:592
translate korean tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "각 속성의 값은 명령문 끝에서 명령문이 값을 시작할 때 그 값으로부터 보간돼. 이것은 프레임별로 한 번 수행하여 원활한 애니메이션을 가능하게 해."

# game/tutorial_atl.rpy:603
translate korean tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL은 원 및 스플라인 모션과 같은 복잡한 이동 유형도 지원해. 하지만 여기서 그것들을 모두 보여주진 않을 거야."

# game/tutorial_atl.rpy:607
translate korean tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "디스플레이어블, 일시 중지, 보간 및 반복을 제외하고도 ATL의 일부로 사용할 수 있는 몇 가지 다른 명령문이 있어."

# game/tutorial_atl.rpy:619
translate korean tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "명령문을 사용해 만들어진 ATL 변형은 ATL 명령문 자체가 돼. 기본 위치 또한 변형으로, ATL 블록 안에서 왼쪽, 오른쪽 및 가운데를 사용할 수 있다는 뜻이야."

# game/tutorial_atl.rpy:635
translate korean tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "여기에는 두 개의 새로운 명령문이 있어. 블록 명령문을 사용하면 ATL 코드의 블록을 포함할 수 있어. 반복(repeat) 명령문은 블록에 적용되는 것으로 ATL 변형의 일부만 반복하게 할 수 있어."

# game/tutorial_atl.rpy:637
translate korean tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "또한 블록의 시작부터 주어진 시간이 경과한 후에 실행되는 시간 명령문이 존재해. 그건 다른 명령문이 실행 중일 때도 실행되며 다른 명령문은 중지시켜."

# game/tutorial_atl.rpy:639
translate korean tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "따라서 이 예제에서는 이미지를 11.5초 동안 좌우로 왔다갔다 하고 나서 화면의 오른쪽으로 이동해."

# game/tutorial_atl.rpy:653
translate korean tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "평행(parallel) 문을 사용하여 동시에 두 블록의 ATL 코드를 실행해보자."

# game/tutorial_atl.rpy:655
translate korean tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "이 코드에서 상단 블록은 이미지를 수평 방향으로, 하단 블록은 수직 방향으로 이동시켜. 서로 다른 속도로 움직이기 때문에 이미지가 화면에서 튀는 것처럼 보이지."

# game/tutorial_atl.rpy:669
translate korean tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "마지막으로, 선택(choice) 명령문을 사용해서 렌파이가 임의로 ATL 코드 블록을 선택하게 해보자. 이건 렌파이가 보여주는 것과 같은 변형을 추가 할 수 있어."

# game/tutorial_atl.rpy:675
translate korean tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "이 길라잡이는 ATL로 수행 할 수 있는 작업의 일부만을 보여주는 거야. 예를 들어, 우린 on 및 event 문도 다루지 않았어. ATL의 보다 자세한 내용은 참조 설명서의 {a=https://renpy.org/doc/html/atl.html}ATL{/a}을 참고하길 바라."

# game/tutorial_atl.rpy:684
translate korean transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "렌파이는 ATL, 변형 디스플레이어블 및 add 스크린 언어 명령문에서 사용할 수 있는 꽤 많은 변형 속성을 가지고 있어."

# game/tutorial_atl.rpy:685
translate korean transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "여기서, 우리는 각각의 속성들이 하는 것을 보고 배우게 될 거야."

# game/tutorial_atl.rpy:701
translate korean transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "우선, 모든 위치 속성은 변형 속성이라는 걸 알아둬. 이러한 것들은 pos, anchor, align, center, 그리고 offset 속성을 포함해."

# game/tutorial_atl.rpy:719
translate korean transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "위치 속성은 xpos와 ypos에 음수로 값을 부여하여 스크린보다 더 큰 디스플레이어블을 밖으로 넘길 때도 사용할 수 있어."

# game/tutorial_atl.rpy:729
translate korean transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "서브 픽셀(subpixel) 속성은 대상이 화면에 어떻게 정렬되어 있는지를 제어해. 거짓(False)일 때, 이미지는 픽셀 단위로 완벽할 수 있지만 픽셀 점프가 있을 수 있어."

# game/tutorial_atl.rpy:736
translate korean transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "값을 참(True)으로 설정하면 이미지가 약간 희미해지는 대신에 부드럽게 움직이게 돼."

# game/tutorial_atl.rpy:755
translate korean transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "변형은 또한 극좌표를 지원해. 주변(around) 속성은 좌표계의 중심을 픽셀로 주어진 좌표로 설정하지."

# game/tutorial_atl.rpy:763
translate korean transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "각도(angle) 속성은 각도를 도(º)로 제공해. 각도는 시계 방향으로 돌고, 화면 상단의 각도는 0이야."

# game/tutorial_atl.rpy:772
translate korean transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "반경(radius) 속성은 디스플레이어블의 앵커에서 좌표계의 중심까지 거리를 픽셀 단위로 나타내."

# game/tutorial_atl.rpy:786
translate korean transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "디스플레이어블의 크기를 조정하는 방법에는 여러 가지가 있어. 줌(zoom) 속성을 사용하면 디스플레이어블을 배율로 해 그 배율을 조정하여 더 크게 또는 더 작게 만들 수 있지."

# game/tutorial_atl.rpy:799
translate korean transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoom과 yzoom 속성을 사용하면 디스플레이어블을 X 및 Y 방향으로 개별 조정할 수 있어."

# game/tutorial_atl.rpy:809
translate korean transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "xzoom이나 yzoom을 음수로 설정하면, 이미지를 수직 또는 수평으로 뒤집을 수 있고."

# game/tutorial_atl.rpy:819
translate korean transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "크기(size) 변형 속성은 디스플레이어블의 크기를 픽셀 단위로 조정하는데 사용될 수 있어."

# game/tutorial_atl.rpy:834
translate korean transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "알파(alpha) 속성은 디스플레이어블의 불투명도를 변경할 때 사용해. 이 속성은 대상을 보이거나 보이지 않게 만들 수 있지."

# game/tutorial_atl.rpy:847
translate korean transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "회전(rotate) 속성은 디스플레이어블을 회전시켜."

# game/tutorial_atl.rpy:858
translate korean transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "기본적으로, 렌파이는 네면에 여분의 공간을 포함하기 때문에 디스플레이어블이 회전됐을 때 크기가 변하지 않아. 여기서, 우리는 왼쪽과 위쪽에 여분의 공간을 볼 수 있고 오른쪽과 아래쪽도 마찬가지야."

# game/tutorial_atl.rpy:870
translate korean transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "rotate_pad를 거짓(False)으로 설정하면 회전할 때 디스플레이어블 크기가 변경되는 대신에 공간을 제거할 수 있어."

# game/tutorial_atl.rpy:881
translate korean transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "타일(tile) 변형 속성인 xtile과 ytile은 디스플레이어블을 여러 번 반복해."

# game/tutorial_atl.rpy:891
translate korean transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "자르기(crop) 속성은 디스플레이어블에서 사각형의 영역을 잘라내."

# game/tutorial_atl.rpy:905
translate korean transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "자르기(crop)와 크기(size)를 함께 사용하면 이미지의 특정 부분에 집중할 수 있어."

# game/tutorial_atl.rpy:917
translate korean transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "xpan과 ypan 속성은 0을 중심으로 디스플레이어블의 각도(0도 단위)를 표시하는 데 사용할 수 있어."

# game/tutorial_atl.rpy:924
translate korean transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "지금까지 본 것들은 모두 우리가 작업해야 하는 변형 속성이야. 올바른 순서로 함께 배치하면 복잡한 것을 만들 수도 있어."

translate korean strings:

    # tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"

