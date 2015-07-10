

# game/tutorial_atl.rpy:187
translate korean tutorial_positions_a09a3fd1:


    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "이 튜토리얼에서는, 렌'파이가 어떻게 컨트롤들을 배치하는지 알려드릴거예요. 하지만 그 전에, 파이썬이 숫자를 어떻게 처리하는지 조금 알아보도록 할까요?"


# game/tutorial_atl.rpy:189
translate korean tutorial_positions_ba39aabc:


    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "파이썬에는 크게 두가지 종류의 숫자가 있습니다. 정수와 부동 소수점 실수인데요."


# game/tutorial_atl.rpy:191
translate korean tutorial_positions_a60b775d:


    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "예를 들어, 100은 정수이고, 1.5는 부동 소수점 실수입니다. 이 시스템에서는 두가지 종류의 0이 있는데요, 정수 0과 부동 소숫점 실수 0.0입니다."


# game/tutorial_atl.rpy:193
translate korean tutorial_positions_7f1a560c:


    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "렌'파이는 절대 좌표를 표현할 때 정수를 사용하고, 주어진 공간의 비율을 얘기할 때 부동 소수점 실수를 사용합니다."


# game/tutorial_atl.rpy:195
translate korean tutorial_positions_8e7d3e52:


    # e "When we're positioning something, the area is usually the entire screen."
    e "렌'파이가 무언가를 배치할 때, 대개 주어진 공간은 스크린 전체입니다."


# game/tutorial_atl.rpy:197
translate korean tutorial_positions_fdcf9d8b:


    # e "Let me get out of the way, and I'll show you where some positions are."
    e "그러면 몇가지 위치의 예제를 보여드리도록 할게요."


# game/tutorial_atl.rpy:211
translate korean tutorial_positions_76d7a5bf:


    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "원점은 스크린의 왼쪽 위 모서리입니다. 즉, x위치(xpos)와 y위치(ypos)가 모두 0인 곳이죠."


# game/tutorial_atl.rpy:217
translate korean tutorial_positions_be14c7c3:


    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "xpos가 증가하면 증가할수록 점은 오른쪽으로 이동합니다. 그래서 이 점은 xpos가 0.5, 즉 스크린의 절반 부분에 위치해 있습니다."


# game/tutorial_atl.rpy:222
translate korean tutorial_positions_9b91be6c:


    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "xpos를 1.0으로 늘리면 점은 오른쪽 가장자리로 이동하지요."


# game/tutorial_atl.rpy:228
translate korean tutorial_positions_80be064f:


    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 800 pixels across, using an xpos of 400 will return the target to the center of the top row."
    e "물론 절대 xpos도 이용할 수 있습니다. xpos에 스크린의 왼쪽 가장자리로부터의 픽셀 수를 입력하면 됩니다. 예를 들어, 이 윈도우의 너비가 800픽셀이기 때문에 xpos를 400픽셀으로 설정하면 점이 화면의 중간에 위치하게 됩니다."


# game/tutorial_atl.rpy:230
translate korean tutorial_positions_c4d18c0a:


    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "y축 위치, 또는 ypos도 비슷하게 동작합니다. 지금 이 점의 위치의 ypos 값은 0.0 이에요."


# game/tutorial_atl.rpy:236
translate korean tutorial_positions_16933a61:


    # e "Here's a ypos of 0.5."
    e "ypos가 0.5일 때이구요."


# game/tutorial_atl.rpy:241
translate korean tutorial_positions_6eb36777:


    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "ypos 1.0은 화면의 밑바닥을 뜻합니다. 잘 보시면 이 텍스트 스크린 밑에 위치 표시 점이  있는 걸 보실 수 있어요."


# game/tutorial_atl.rpy:243
translate korean tutorial_positions_a423050f:


    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "xpos와 마찬가지로 ypos도 정수가 될 수 있습니다. 이 경우, 화면의 최상단으로부터의 픽셀 수가 되겠지요."


# game/tutorial_atl.rpy:249
translate korean tutorial_positions_bc7a809a:


    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "이 점의 위치를 한번 맞혀 보실래요? 상대 좌표로 말이죠." nointeract


# game/tutorial_atl.rpy:255
translate korean tutorial_positions_6f926e18:


    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "앗, 틀렸어요! xpos는 0.75고 ypos는 0.25인 포인트였습니다!"


# game/tutorial_atl.rpy:257
translate korean tutorial_positions_5d5feb98:


    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "바꿔 말하면, 화면의 왼쪽에서 75%% 위치, 그리고 화면의 상단에서 25%% 위치에 있는 점이라는 소리입니다."


# game/tutorial_atl.rpy:261
translate korean tutorial_positions_77b45218:


    # e "Good job! You got that position right."
    e "정답입니다!"


# game/tutorial_atl.rpy:265
translate korean tutorial_positions_6f926e18_1:


    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "앗, 틀렸어요! xpos는 0.75고 ypos는 0.25인 포인트였습니다!"


# game/tutorial_atl.rpy:267
translate korean tutorial_positions_5d5feb98_1:


    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "바꿔 말하면, 화면의 왼쪽에서 75%% 위치, 그리고 화면의 상단에서 25%% 위치에 있는 점이라는 소리입니다."


# game/tutorial_atl.rpy:281
translate korean tutorial_positions_e4380a83:


    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "다음으로 설명드릴 위치는 앵커입니다. 앵커는 렌'파이에 의해 위치되는 컨트롤 위의 점이에요."


# game/tutorial_atl.rpy:283
translate korean tutorial_positions_d1db1246:


    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "예를 들어, 이 로고 이미지는 xanchor 0.0, yanchor 0.0을 가지고 있습니다. 이는 이미지의 왼쪽 위 모서리를 뜻하죠."


# game/tutorial_atl.rpy:288
translate korean tutorial_positions_6056873f:


    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "이번에는 xanchor를 1.0으로 해 보았습니다. 표시점이 오른쪽 위 모서리로 움직였네요."


# game/tutorial_atl.rpy:293
translate korean tutorial_positions_7cdb8dcc:


    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "비슷하게, xanchor와 yanchor가 모두 1.0이면, 앵커는 디스플레이어블의 오른쪽 아래 모서리에 위치하게 됩니다."


# game/tutorial_atl.rpy:301
translate korean tutorial_positions_03a07da8:


    # e "To place an image on the screen, we need both the position and the anchor."
    e "이미지를 스크린에 배치하기 위해서는 위치와 앵커, 둘 다 필요합니다."


# game/tutorial_atl.rpy:309
translate korean tutorial_positions_8945054f:


    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "위치와 앵커가 결정되면, 렌'파이는 줄을 맞춰서 앵커와 위치가 같은 점에 위치하게 이미지를 옮깁니다."


# game/tutorial_atl.rpy:319
translate korean tutorial_positions_2b184a93:


    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "제가 위치와 앵커를 모두 왼쪽 위로 설정하면, 이미지는 화면의 왼쪽 위 모서리로 이동합니다."


# game/tutorial_atl.rpy:328
translate korean tutorial_positions_5aac4f3f:


    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "위치와 앵커의 조합을 잘 이용하면 스크린의 어느 위치던 표현이 가능합니다. 이미지의 크기를 몰라도 말이죠!"


# game/tutorial_atl.rpy:340
translate korean tutorial_positions_3b59b797:


    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "xpos와 xanchor를 같은 값으로 설정하는건 자주 유용하게 사용됩니다. 이것은 xalign이라고 불리는데요, 스크린 위의 위치를 소수로 나타냅니다."


# game/tutorial_atl.rpy:345
translate korean tutorial_positions_b8ebf9fe:


    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "예를 들어, xalign을 0.0으로 설정하면, 이미지는 화면의 왼쪽 가장자리에 위치하게 됩니다."


# game/tutorial_atl.rpy:350
translate korean tutorial_positions_8ce35d52:


    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "1.0이 된다면, 오른쪽 가장자리에 위치하게 되구요."


# game/tutorial_atl.rpy:355
translate korean tutorial_positions_6745825f:


    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "마지막으로 0.5로 설정하게 되면 다시 이미지가 화면 중앙으로 돌아옵니다."


# game/tutorial_atl.rpy:357
translate korean tutorial_positions_64428a07:


    # e "Setting yalign is similar, except along the y-axis."
    e "yalign도 비슷하게 동작합니다. y축을 따라 움직인다는 점만 빼구요."


# game/tutorial_atl.rpy:359
translate korean tutorial_positions_cfb77d42:


    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "xalign은 xpos와 xanchor를 같은 값으로 설정하고, yalign은 ypos와 yanchor를 같은 값으로 설정할 뿐이라는 점을 기억해 주세요."


# game/tutorial_atl.rpy:366
translate korean tutorial_positions_0f4ca2b6:


    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "위치에 대해 이해하셨다면, 이제 트랜스폼을 이용해서 스크린 위에 있는 디스플레이어블을 움직일 수 있습니다!"


# game/tutorial_atl.rpy:373
translate korean tutorial_atl_a1cc1bff:


    # e "While showing static images is often enough for most games, occasionally we'll want to change images, or move them around the screen."
    e "게임이 움직이지 않는 이미지만으로도 충분한 경우가 자주 있기는 합니다만, 이미지를 바꾸고 이리저리 움직이고도 싶은게 제작자의 마음이죠."


# game/tutorial_atl.rpy:375
translate korean tutorial_atl_81dbb8f2:


    # e "We call this a Transform, and it's what ATL, Ren'Py's Animation and Transformation Language, is for."
    e "이미지를 바꾸고 이리저리 움직이는 것을 트랜스폼이라고 합니다. 그리고 이 트랜스폼이, ATL, 즉 렌'파이의 Animation and Transformation Language의 존재 이유이기도 하지요."


# game/tutorial_atl.rpy:383
translate korean tutorial_atl_65badef3:


    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "그 전에… 공짜 락 콘서트를 즐겨 보자구요!"


# game/tutorial_atl.rpy:391
translate korean tutorial_atl_3ccfe2ac:


    # e "That was a lot of work, and before you can do that, we'll need to start with the basics of using ATL."
    e "방금 건 만드는데 좀 힘들었어요… 그러니까 이런 효과를 만들기 전에, ATL의 기본부터 배워볼까요?"


# game/tutorial_atl.rpy:393
translate korean tutorial_atl_1f22f875:


    # e "There are currently three places where ATL can be used in Ren'Py."
    e "현재 렌'파이에서는 세가지 부분에서 ATL을 사용할 수 있습니다."


# game/tutorial_atl.rpy:397
translate korean tutorial_atl_fd036bdf:


    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "ATL이 사용될 수 있는 부분 중 하나는 image 문입니다. 디스플레이어블 대신 이미지는 ATL 코드 블록으로 정의될 수 있습니다."


# game/tutorial_atl.rpy:399
translate korean tutorial_atl_7cad2ab9:


    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "이런 식으로 ATL이 사용될 때에는, 이 ATL이 실제로 표시할 디스플레이어블을 하나 이상 포함하고 있어야 합니다."


# game/tutorial_atl.rpy:403
translate korean tutorial_atl_c78b2a1e:


    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "두번쨰 방법은 transform 문을 사용하는 것입니다. 이 문은 ATL 블록을 파이썬 변수에 할당하는데요, 이 변수가 여러분이 만든 트랜스폼을 다른 트랜스폼이나 at 절에서 사용할 수 있게 해 줍니다."


# game/tutorial_atl.rpy:407
translate korean tutorial_atl_da7a7759:


    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "마지막으로, ATL 블록이 at 절 대신 show 문의 일부분으로서 사용될 수 있습니다."


# game/tutorial_atl.rpy:411
translate korean tutorial_atl_c21bc1d1:


    # e "The key to ATL is what we call composeability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "ATL의 핵심은 조합성입니다. ATL은 상대적으로 간단한 명령들을 조합해서 더욱 복잡한 트랜스폼을 만드는데 사용될 수 있거든요."


# game/tutorial_atl.rpy:413
translate korean tutorial_atl_ed82983f:


    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "제가 ATL이 실제로 어떻게 동작하는지 설명드리기 전에, 애니메이션과 트랜스폼이 무엇인지부터 살펴볼까요?"


# game/tutorial_atl.rpy:418
translate korean tutorial_atl_2807adff:


    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "애니메이션은 현재 보여지고 있는 디스플레이어블이 바뀌는 것을 말합니다."


# game/tutorial_atl.rpy:445
translate korean tutorial_atl_3eec202b:


    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "트랜스폼은 이미지의 이동, 왜곡 등을 말하죠. 이는 스크린 위에 위치시키는것, 확대와 축소, 회전, 투명도 조절 등을 모두 포함하는 거예요."


# game/tutorial_atl.rpy:453
translate korean tutorial_atl_fbc9bf83:


    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "ATL을 소개하기 위해서, 먼저 간단한 애니메이션을 체험해 보는 것부터 시작해 볼까요? 이 애니메이션은 image 문에 작성되어 있는 5줄로 이루어진 ATL 코드입니다."


# game/tutorial_atl.rpy:455
translate korean tutorial_atl_12c839ee:


    # e "In ATL, to change a displayable, simply mention it on a line of ATL code. Here, we're switching back and forth between two images."
    e "ATL에서 디스플레이어블을 바꾸기 위해선, 그냥 간단하게 ATL 코드 한 줄 안에 써 넣으면 됩니다. 이 경우에는, 이미지 2개를 번갈아서 보여주고 있네요."


# game/tutorial_atl.rpy:457
translate korean tutorial_atl_c671ed7d:


    # e "Since we're defining an image, the first line of ATL has to name a displayable. Otherwise, there would be nothing to show."
    e "지금 제가 이미지를 정의하고 있는 중이기 때문에, ATL 코드의 첫 줄은 디스플레이어블을 꼭 명시해줘야 해요. 안 그러면 아무것도 보이지 않게 되겠죠."


# game/tutorial_atl.rpy:459
translate korean tutorial_atl_99386181:


    # e "The second and fourth lines are pause statements, which cause ATL to wait half of a second each before continuing. That's how we give the delay between images."
    e "두 번째와 네 번째 줄은 pause 문입니다. 이 경우에는 다음 이미지로 변경하기 전에 0.5초를 기다리게(pause) 됩니다. 이런 방식으로 이미지 사이에 지연 시간을 넣을 수 있어요."


# game/tutorial_atl.rpy:461
translate korean tutorial_atl_60f2a5e8:


    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "맨 마지막 줄은 repeat 문입니다. 이 문은 repeat 문이 위치해 있는 블록의 처음으로 돌아가 다시 시작합니다. 하나의 블록은 단 하나의 repeat 문 만을 가질 수 있어요."


# game/tutorial_atl.rpy:466
translate korean tutorial_atl_146cf4c4:


    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "만약 repeat 단독으로 쓰는 것이 아닌, repeat 2를 사용하면 애니메이션은 두번 반복하고 멈추게 됩니다. "


# game/tutorial_atl.rpy:471
translate korean tutorial_atl_d90b1838:


    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "repeat 문은 생략하는 것은 ATL 블록의 끝에 도달하면 애니메이션을 멈춘다는 것을 의미합니다. "


# game/tutorial_atl.rpy:476
translate korean tutorial_atl_e5872360:


    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "기본값으로, 디스플레이어블들은 순간적으로 교체됩니다. with 절을 이용하면 디스플레이어블 사이에 트랜지션을 넣을 수 있어요."


# game/tutorial_atl.rpy:483
translate korean tutorial_atl_a7f8ed01:


    # e "Now, let's move on to see how we can use ATL to transform an image. We'll start off by seeing what we can do to position images on the screen."
    e "이제, ATL을 사용해서 어떻게 이미지를 \"트랜스폼\" 시킬 수 있는지 알아보아요. "


# game/tutorial_atl.rpy:492
translate korean tutorial_atl_24501213:


    # e "Perhaps the simplest thing we can do is to position the images on the screen. This can be done by simply giving the names of the transform properties, each followed by the value."
    e "제 생각에 지금 당장 보여드릴 수 있는 가장 간단한 것은 이미지를 스크린 위에 배치시키는 것인 것 같아요. 이는 간단하게 트랜스폼 속성들과 그 값들을 제공하는 것으로도 이뤄질 수 있어요."


# game/tutorial_atl.rpy:497
translate korean tutorial_atl_43516492:


    # e "With a few more statements, we can move things around on the screen."
    e "몇 개의 문을 더 추가하면 이런 것들을 스크린 상에서 옮길 수 있습니다."


# game/tutorial_atl.rpy:499
translate korean tutorial_atl_8b053b5a:


    # e "This code starts the image off at the top-right of the screen, and waits a second."
    e "이 코드는 이미지를 화면 우측 상단에 배치하고 1초를 기다립니다."


# game/tutorial_atl.rpy:501
translate korean tutorial_atl_d7fc5372:


    # e "It then moves it to the left side, waits another second, and repeats."
    e "그 다음 이미지를 화면 좌측 상단에 옮기고 다시 1초를 기다립니다. 그 다음 이를 반복하죠."


# game/tutorial_atl.rpy:503
translate korean tutorial_atl_7650ec09:


    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "pause 문과 repeat 문은 제가 애니메이션 부분에서 사용했던 그것과 동일한 거예요. 이 문들은 ATL 전반에 걸쳐서 사용될 수 있죠."


# game/tutorial_atl.rpy:508
translate korean tutorial_atl_d3416d4f:


    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "그렇지만 이미지가 아무런 준비 동작도 없이 이곳 저곳으로 움직이는 건 보기 좋지 않죠. 그래서 렌'파이의 ATL은 보간문을 지원합니다."


# game/tutorial_atl.rpy:510
translate korean tutorial_atl_4e7512ec:


    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "보간문은 트랜스폼 속성의 값이 새로운 값으로 부드럽게 바뀔 수 있도록 해 줍니다."


# game/tutorial_atl.rpy:512
translate korean tutorial_atl_685eeeaa:


    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "위 예제의 두번째 ATL 줄을 보면 보간문이 하나가 있습니다. 보간문은 워퍼(시간 함수)의 이름으로 시작을 합니다. 이 경우에는, linear(선형 보간)이 되죠."


# game/tutorial_atl.rpy:514
translate korean tutorial_atl_c5cb49de:


    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "워퍼 다음에는 시간 값이 초 단위로 붙습니다. 이 경우, 3초지요. 그 다음 바뀔 속성들과 새 속성값이 따라오게 됩니다."


# game/tutorial_atl.rpy:516
translate korean tutorial_atl_72d47fb6:


    # e "The old value is the value of the transform property at the start of the statement. By interpolating the property over time, we can change things on the screen."
    e "트랜스폼 속성의 old 값은 문의 시작 부분에서의 속성값입니다. 여러 시간에 걸쳐서 이 속성을 보간함으로서 스크린 상의 디스플레이어블을 움직일 수 있죠."


# game/tutorial_atl.rpy:526
translate korean tutorial_atl_2958f397:


    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL은 원 모양 모션이나 스플라인 모션같은 더욱 복잡한 종류의 모션을 지원합니다만, 여기서 바로 보여드리진 않을게요."


# game/tutorial_atl.rpy:528
translate korean tutorial_atl_4a02c8d8:


    # e "Next, let's take a look at some of the transform properties that we can change using ATL."
    e "다음으로, ATL을 사용해서 변경할 수 있는 트랜스폼 속성들을 몇 가지 살펴보도록 하겠습니다."


# game/tutorial_atl.rpy:543
translate korean tutorial_atl_821fcb91:


    # e "We've already seen the position properties. Along with xalign and yalign, we support the xpos, ypos, xanchor, and yanchor properties."
    e "이전에 제가 여러분께 위치 속성을 보여드렸는데요, xalign, yalign과 함께, 렌'파이는 xpos, ypos, xanchor, 그리고 yanchor 속성의 변경을 지원합니다."


# game/tutorial_atl.rpy:558
translate korean tutorial_atl_cca5082b:


    # e "We can perform a pan by using xpos and ypos to position images off of the screen."
    e "xpos와 ypos를 스크린에서 멀어지게 함으로써 팬 움직임을 구현할 수도 있어요."


# game/tutorial_atl.rpy:560
translate korean tutorial_atl_0394dd50:


    # e "This usually means giving them negative positions."
    e "이는 대개 위치 값을 음수로 주는 것을 말합니다."


# game/tutorial_atl.rpy:577
translate korean tutorial_atl_2624662e:


    # e "The zoom property lets us scale the displayable by a factor, making it bigger and smaller. For best results, zoom should always be greater than 0.5."
    e "zoom 속성은 디스플레이어블을 인수로 받은 값으로 확대하거나 축소시킵니다. 가장 좋은 결과를 위해서는 zoom 속성을 0.5보다 크게 설정하는 것이 좋아요."


# game/tutorial_atl.rpy:591
translate korean tutorial_atl_b6527546:


    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoom과 yzoom 속성들은 디스플레이어블을 x축과 y축 방향으로 따로따로 확대할 수 있게 해 줍니다."


# game/tutorial_atl.rpy:602
translate korean tutorial_atl_9fe238de:


    # e "The size property can be used to set a size, in pixels, that the displayable is scaled to."
    e "size 속성은 디스플레이어블이 보여질 크기를 픽셀 단위로 설정할 수 있어요."


# game/tutorial_atl.rpy:617
translate korean tutorial_atl_6b982a23:


    # e "The alpha property allows us to vary the opacity of a displayable. This can make it appear and disappear."
    e "alpha 속성은 디스플레이어블의 투명도를 조절하는 역할을 합니다. 말 그대로 사라지게, 다시 나타나게 할 수 있죠."


# game/tutorial_atl.rpy:631
translate korean tutorial_atl_60d6d9f3:


    # e "The rotate property lets us rotate a displayable."
    e "rotate 속성은 디스플레이어블을 회전시킬 수 있어요."


# game/tutorial_atl.rpy:633
translate korean tutorial_atl_898a138a:


    # e "Since rotation can change the size, usually you'll want to set xanchor and yanchor to 0.5 when positioning a rotated displayable."
    e "이미지 회전이 크기를 변화시킬 수 있기 때문에, 디스플레이어블을 회전시킬 때에는 xanchor와 yanchor를 모두 0.5로 설정하는 것이 좋아요."


# game/tutorial_atl.rpy:644
translate korean tutorial_atl_207b7fc8:


    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "crop 속성은 디스플레이어블을 직사각형 모양으로 잘라서 그 일부만 보여줍니다."


# game/tutorial_atl.rpy:658
translate korean tutorial_atl_ebb84988:


    # e "When used together, they can be used to focus in on specific parts of an image."
    e "이런 것들을 함께 사용하면 이미지의 어떤 부분에만 집중할 수 있도록 할 수 있어요."


# game/tutorial_atl.rpy:664
translate korean tutorial_atl_d08fe8d9:


    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "디스플레이어블, pause, 보간문과 repeat 말고도 ATL의 한 부분으로 쓸 수 있는 문이 몇 가지 더 있어요."


# game/tutorial_atl.rpy:678
translate korean tutorial_atl_db6302bd:


    # e "When we create an ATL transform using the transform statement, we can use that transform as an ATL statement."
    e "transform 문을 사용해서 ATL 트랜스폼을 만들면 그 트랜스폼을 ATL 내부에서 하나의 문처럼 쓸 수 있어요."


# game/tutorial_atl.rpy:680
translate korean tutorial_atl_785911cf:


    # e "Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "미리 정의된 위치도 마찬가지로 트랜스폼의 일종이기 때문에 left, right, center와 같은 위치를 ATL 블록 내에서 사용할 수 있다는 거죠."


# game/tutorial_atl.rpy:698
translate korean tutorial_atl_331126c1:


    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "위에 두가지 새로운 문이 있습니다. block 문은 여러분이 ATL 코드 안에 블록을 삽입할 수 있도록 하지요. repeat 문은 하나의 블록에서만 작용하기 때문에 이 문은 ATL 코드 중 어떤 한 부분만 반복하고 싶을 때 유용합니다."


# game/tutorial_atl.rpy:700
translate korean tutorial_atl_24f67b67:


    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "또 하나, time 문이 보이네요. time 문은 자신이 들어있는 블록이 시작된 이후로부터 주어진 시간만큼 지나면 실행됩니다. 다른 문이 실행되고 있어도 시간이 되면 실행되던 코드를 정지하고 자신을 실행합니다."


# game/tutorial_atl.rpy:702
translate korean tutorial_atl_30dc0008:


    # e "So this code will bounce the image back and forth for eleven and a half seconds, and then move back to the right side of the screen."
    e "그래서 위 코드를 실행하면 로고 이미지가 11초 하고 반 동안 양 옆으로 움직이다가 화면의 오른쪽 부분으로 이동하게 되죠."


# game/tutorial_atl.rpy:718
translate korean tutorial_atl_f903bc3b:


    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "parrallel 문은 두개의 ATL 코드 블록을 동시에 실행합니다."


# game/tutorial_atl.rpy:720
translate korean tutorial_atl_5d0f8f9d:


    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "위 코드에서, 위에 있는 블록은 이미지를 가로 방향으로 움직이고, 아래에 있는 블록은 이미지를 세로 방향으로 움직입니다. 이 둘이 움직이는 속도가 다르기 때문에, 이미지가 스크린 안에서 튀어 다니는 것처럼 보이게 되죠."


# game/tutorial_atl.rpy:737
translate korean tutorial_atl_28a7d27e:


    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "마지막으로, choice 문은 렌'파이가 ATL 코드 블록을 무작위로 선택하도록 합니다. 렌'파이가 보여줄 방식에 변화를 줄 수 있죠. "


# game/tutorial_atl.rpy:743
translate korean tutorial_atl_5fc8c0df:


    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out the ATL chapter in the reference manual."
    e "이 길라잡이 게임에서는 ATL을 수박 겉핥기 정도로 맛보기 해 보았습니다. 예를 들어, event 문에 관해서는 언급도 안 했어요. 더 많은 정보를 원하신다면, 렌'파이 레퍼런스 메뉴얼의 ATL 단원을 읽어 보세요."


# game/tutorial_atl.rpy:747
translate korean tutorial_atl_1358c6b4:


    # e "But for now, just remember that when it comes to animating and transforming, ATL is the hot new thing."
    e "그래도 지금은, ATL은 애니메이션과 트랜스폼을 위한 혁신적인 방법이라는 것, 기억해 두세요!"


translate korean strings:


    # game/tutorial_atl.rpy:249
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"


    # game/tutorial_atl.rpy:249
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"


    # game/tutorial_atl.rpy:249
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"
