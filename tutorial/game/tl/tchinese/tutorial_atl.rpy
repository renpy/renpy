
# game/tutorial_atl.rpy:205
translate tchinese tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "在這份教學中，我會教你 Ren'Py 如何在畫面上定位物件。不過先來了解 Python 如何處理數字。"

# game/tutorial_atl.rpy:207
translate tchinese tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Python 主要有兩種數字：整數和浮點數。整數完全由數字組成，浮點數則包含小數點。"

# game/tutorial_atl.rpy:209
translate tchinese tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "例如，100 是整數，0.5 是浮點數。在這個系統中，零也有兩種：0 是整數，0.0 是浮點數。"

# game/tutorial_atl.rpy:211
translate tchinese tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Py 使用整數表示絕對座標，使用浮點數表示已知大小區域的比例。"

# game/tutorial_atl.rpy:213
translate tchinese tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "定位物件時，這個區域通常就是整個畫面。"

# game/tutorial_atl.rpy:215
translate tchinese tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "我先站到旁邊，讓你看看幾個位置。"

# game/tutorial_atl.rpy:229
translate tchinese tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "原點是畫面的左上角，那裡的 x 座標（xpos）和 y 座標（ypos）都是 0。"

# game/tutorial_atl.rpy:235
translate tchinese tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "增加 xpos 就會向右移動。xpos 為 .5 代表畫面寬度的一半。"

# game/tutorial_atl.rpy:240
translate tchinese tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "將 xpos 增加到 1.0，就會移到畫面的右邊界。"

# game/tutorial_atl.rpy:246
translate tchinese tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "也可以使用絕對 xpos，以距畫面左側的像素數表示。例如這個視窗寬 1280 像素，使用 xpos 640 就會讓目標位於頂列中央。"

# game/tutorial_atl.rpy:248
translate tchinese tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "y 軸位置 ypos 的運作方式相同。現在 ypos 是 0.0。"

# game/tutorial_atl.rpy:254
translate tchinese tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "這裡的 ypos 是 0.5。"

# game/tutorial_atl.rpy:259
translate tchinese tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "ypos 為 1.0 時，位置會在畫面底部。仔細看，位置指示器正在文字視窗下方旋轉。"

# game/tutorial_atl.rpy:261
translate tchinese tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "和 xpos 一樣，ypos 也可以是整數；這時代表距離畫面頂端的像素總數。"

# game/tutorial_atl.rpy:267
translate tchinese tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "你能猜出這個位置相對於畫面的位置嗎？" nointeract

# game/tutorial_atl.rpy:273
translate tchinese tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "抱歉，答案不對。xpos 是 .75，ypos 是 .25。"

# game/tutorial_atl.rpy:275
translate tchinese tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "換句話說，它距離左側 75%%，距離頂端 25%%。"

# game/tutorial_atl.rpy:279
translate tchinese tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "做得好！你猜對位置了。"

# game/tutorial_atl.rpy:283
translate tchinese tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "抱歉，答案不對。xpos 是 .75，ypos 是 .25。"

# game/tutorial_atl.rpy:285
translate tchinese tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "換句話說，它距離左側 75%%，距離頂端 25%%。"

# game/tutorial_atl.rpy:299
translate tchinese tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "我們關心的第二個位置是錨點（anchor），也就是被定位物件上的一個點。"

# game/tutorial_atl.rpy:301
translate tchinese tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "例如這裡的 xanchor 和 yanchor 都是 0.0，位於 logo 圖片的左上角。"

# game/tutorial_atl.rpy:306
translate tchinese tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "xanchor 增加到 1.0 時，錨點會移到圖片的右上角。"

# game/tutorial_atl.rpy:311
translate tchinese tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "同樣地，xanchor 和 yanchor 都是 1.0 時，錨點位於右下角。"

# game/tutorial_atl.rpy:318
translate tchinese tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "要在畫面上放置圖片，需要同時指定位置和錨點。"

# game/tutorial_atl.rpy:326
translate tchinese tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "將兩者對齊，就能讓位置和錨點位於畫面上的同一點。"

# game/tutorial_atl.rpy:336
translate tchinese tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "把兩者都放在左上角時，圖片就會移到畫面的左上角。"

# game/tutorial_atl.rpy:345
translate tchinese tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "只要正確組合位置和錨點，就能指定畫面上的任意位置，甚至不必知道圖片大小。"

# game/tutorial_atl.rpy:357
translate tchinese tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "通常將 xpos 和 xanchor 設為相同值很有用。我們稱之為 xalign，可用來指定畫面上的相對位置。"

# game/tutorial_atl.rpy:362
translate tchinese tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "例如，將 xalign 設為 0.0 時，物件會對齊畫面左側。"

# game/tutorial_atl.rpy:367
translate tchinese tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "設為 1.0 時，物件會對齊畫面右側。"

# game/tutorial_atl.rpy:372
translate tchinese tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "設為 0.5 時，物件會回到畫面中央。"

# game/tutorial_atl.rpy:374
translate tchinese tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "設定 yalign 的方式類似，只是作用在 y 軸。"

# game/tutorial_atl.rpy:376
translate tchinese tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "記住，xalign 只是把 xpos 和 xanchor 設為相同值，yalign 則是把 ypos 和 yanchor 設為相同值。"

# game/tutorial_atl.rpy:381
translate tchinese tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "xcenter 和 ycenter 屬性會定位圖片中心。這裡將 xcenter 設為 .75，圖片中心位於距離畫面右側四分之三的位置。"

# game/tutorial_atl.rpy:386
translate tchinese tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "xcenter 為 1.0 時，xalign 和 xcenter 的差異更明顯，圖片會有一半超出右邊界。"

# game/tutorial_atl.rpy:394
translate tchinese tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "xoffset 和 yoffset 屬性會在其他屬性套用後，分別讓物件向右或向下偏移。"

# game/tutorial_atl.rpy:399
translate tchinese tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "當然，也可以使用負數讓物件向左或向上偏移。"

# game/tutorial_atl.rpy:404
translate tchinese tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "最後介紹幾個組合屬性，例如 align、pos、anchor 和 center。align 接收一對數字，將 xalign 設為第一個、yalign 設為第二個；其他屬性也類似。"

# game/tutorial_atl.rpy:411
translate tchinese tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "理解位置後，就能使用變換在 Ren'Py 畫面上移動物件。"

# game/tutorial_atl.rpy:418
translate tchinese tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "Ren'Py 使用變換製作動畫、操作和放置圖片。我們已經看過最簡單的變換："

# game/tutorial_atl.rpy:425
translate tchinese tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "變換可以很簡單，只是把圖片放在畫面某處，例如 right 變換。"

# game/tutorial_atl.rpy:429
translate tchinese tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "但變換也能複雜得多，加入動畫和特效。為了示範，來場免費的搖滾演唱會吧！"

# game/tutorial_atl.rpy:437
translate tchinese tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "不過首先，來場……免費的搖滾演唱會！"

# game/tutorial_atl.rpy:445
translate tchinese tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "這工程規模不小，但其實是由許多小部分組成的。"

# game/tutorial_atl.rpy:447
translate tchinese tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "Ren'Py 中大多數變換都使用動畫與變換語言（Animation and Transform Language，簡稱 ATL）建立。"

# game/tutorial_atl.rpy:449
translate tchinese tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "目前在 Ren'Py 中有三個地方可以使用 ATL。"

# game/tutorial_atl.rpy:454
translate tchinese tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "ATL 的第一種用法是作為 image 語句的一部分。圖片可以定義為 ATL 程式碼區塊，而不是顯示物件。"

# game/tutorial_atl.rpy:456
translate tchinese tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "以這種方式使用時，必須確保 ATL 包含一個或多個實際要顯示的顯示物件。"

# game/tutorial_atl.rpy:461
translate tchinese tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "第二種方式是使用 transform 語句。將 ATL 區塊指定給 Python 變數，就能在 at 子句和其他變換中使用。"

# game/tutorial_atl.rpy:473
translate tchinese tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "最後，ATL 區塊也能作為 show 語句的一部分，而不是 at 子句。"

# game/tutorial_atl.rpy:480
translate tchinese tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though your click stopped the motion, the image remains in the same place."
    e "ATL 作為 show 語句的一部分時，即使變換已改變，屬性值仍會保留。因此即使點擊停止圖片移動，它仍會留在原本的位置。"

# game/tutorial_atl.rpy:488
translate tchinese tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "ATL 的關鍵在於可組合性。ATL 由相對簡單的指令組成，可以組合起來建立複雜變換。"

# game/tutorial_atl.rpy:490
translate tchinese tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "在說明 ATL 的運作方式前，先來解釋什麼是動畫和變換。"

# game/tutorial_atl.rpy:495
translate tchinese tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "動畫是顯示物件正在變化的狀態。例如，我現在正在改變表情。"

# game/tutorial_atl.rpy:522
translate tchinese tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "變換包括移動或扭曲圖片，例如定位、縮放、旋轉和變更不透明度。"

# game/tutorial_atl.rpy:530
translate tchinese tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "為了介紹 ATL，先看看簡單動畫。這段 image 語句中包含五行 ATL 程式碼。"

# game/tutorial_atl.rpy:532
translate tchinese tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "要變更顯示物件，只要在 ATL 的一行中提到它即可。這裡會在兩張圖片之間來回切換。"

# game/tutorial_atl.rpy:534
translate tchinese tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "由於要定義圖片，ATL 第一行必須提供顯示物件，否則就沒有內容可顯示。"

# game/tutorial_atl.rpy:536
translate tchinese tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "第二行和第四行是 pause 語句，會讓 ATL 各等待半秒再繼續。這就是在圖片之間設定延遲的方法。"

# game/tutorial_atl.rpy:538
translate tchinese tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "最後一行是 repeat 語句，會重新啟動目前的 ATL 區塊。每個區塊只能有一個 repeat 語句。"

# game/tutorial_atl.rpy:543
translate tchinese tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "如果改成 repeat 2，動畫會循環兩次後停止。"

# game/tutorial_atl.rpy:548
translate tchinese tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "省略 repeat 語句表示 ATL 程式碼執行到區塊末尾時，動畫就會停止。"

# game/tutorial_atl.rpy:554
translate tchinese tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "顯示物件預設會立即替換，也可以使用 with 子句在顯示物件之間加入轉場。"

# game/tutorial_atl.rpy:561
translate tchinese tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "動畫完成後，來了解如何使用 ATL 變換圖片，先從在畫面上定位圖片開始。"

# game/tutorial_atl.rpy:570
translate tchinese tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "最簡單的做法是靜態定位圖片：先寫位置屬性名稱，再寫屬性值。"

# game/tutorial_atl.rpy:575
translate tchinese tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "再加入幾個語句，就能在畫面上移動物件。"

# game/tutorial_atl.rpy:577
translate tchinese tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "這個例子中的圖片一開始位於畫面右上角，等待一秒後移到左側，再等一秒並重複。"

# game/tutorial_atl.rpy:579
translate tchinese tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "pause 和 repeat 語句與動畫範例中的相同，會貫穿 ATL 程式碼執行。"

# game/tutorial_atl.rpy:584
translate tchinese tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "讓圖片在畫面上跳來跳去不太實用，這就是 ATL 提供插值（interpolation）語句的原因。"

# game/tutorial_atl.rpy:586
translate tchinese tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "插值語句能讓屬性值從舊值平順地變成新值。"

# game/tutorial_atl.rpy:588
translate tchinese tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "這裡第二行 ATL 是插值語句，以時間函式名稱開頭，本例是 linear。"

# game/tutorial_atl.rpy:590
translate tchinese tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "接著是持續時間，本例為三秒；最後是屬性串列，每個屬性後面都是新值。"

# game/tutorial_atl.rpy:592
translate tchinese tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "每個屬性的插值會從語句開始時的值變到結束時的值，每幀執行一次以產生平滑動畫。"

# game/tutorial_atl.rpy:603
translate tchinese tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATL 也支援更複雜的移動類型，例如圓周和螺旋運動，但這裡不示範。"

# game/tutorial_atl.rpy:607
translate tchinese tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "除了顯示物件、pause、插值和 repeat，還有其他語句可以作為 ATL 的一部分。"

# game/tutorial_atl.rpy:619
translate tchinese tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "使用該語句建立的 ATL 變換本身也會成為 ATL 語句。由於預設位置也是變換，因此能在 ATL 區塊內使用 left、right 和 center。"

# game/tutorial_atl.rpy:635
translate tchinese tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "這裡有兩個新語句。block 語句能包含 ATL 程式碼區塊；由於 repeat 語句套用於區塊，因此可以只重複部分 ATL 變換。"

# game/tutorial_atl.rpy:637
translate tchinese tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "還有 time 語句，會在指定秒數後開始執行區塊，即使另一個語句仍在執行，也會讓它停止。"

# game/tutorial_atl.rpy:639
translate tchinese tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "這個例子會在 11.5 秒內讓圖片來回反彈，然後把它移到畫面右側。"

# game/tutorial_atl.rpy:653
translate tchinese tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "parallel 語句能讓我們同時執行兩個 ATL 程式碼區塊。"

# game/tutorial_atl.rpy:655
translate tchinese tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "這裡上方的區塊水平移動圖片，下方的區塊垂直移動圖片。由於速度不同，看起來就像在畫面上反彈。"

# game/tutorial_atl.rpy:669
translate tchinese tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "最後，choice 語句會讓 Ren'Py 隨機選擇一個 ATL 程式碼區塊，為顯示內容增加變化。"

# game/tutorial_atl.rpy:675
translate tchinese tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "這份教學只觸及 ATL 能做什麼的表面，例如甚至沒有討論 on 和 event 語句。詳細資訊請參閱{a=https://renpy.org/doc/html/atl.html}參考手冊中的 ATL 章節{/a}。"

# game/tutorial_atl.rpy:684
translate tchinese transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "Ren'Py 有許多可與 ATL、Transform 顯示物件和 add 螢幕語言語句搭配使用的變換屬性。"

# game/tutorial_atl.rpy:685
translate tchinese transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "這裡會展示這些屬性，讓你看到實際效果並熟悉各自的用途。"

# game/tutorial_atl.rpy:701
translate tchinese transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "首先，所有位置屬性也是變換屬性，包括 pos、anchor、align、center 和 offset。"

# game/tutorial_atl.rpy:719
translate tchinese transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "position 屬性也能透過給 xpos 和 ypos 負值，在比畫面更大的顯示物件上平移。"

# game/tutorial_atl.rpy:729
translate tchinese transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "subpixel 屬性控制物件如何與畫面對齊。設為 False 時，圖片可以達到像素級精準，但移動時可能出現像素跳動。"

# game/tutorial_atl.rpy:736
translate tchinese transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "設為 True 時，移動會更平滑，但圖片也會稍微變模糊。"

# game/tutorial_atl.rpy:755
translate tchinese transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "變換也支援極座標。around 屬性會將座標系中心設為以像素表示的座標。"

# game/tutorial_atl.rpy:763
translate tchinese transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "angle 屬性以度數表示角度，按順時針計算，零度位於畫面頂端。"

# game/tutorial_atl.rpy:772
translate tchinese transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "radius 屬性給出顯示物件錨點到座標系中心的像素距離。"

# game/tutorial_atl.rpy:786
translate tchinese transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "有幾種方式可以調整顯示物件大小。zoom 屬性能以倍數縮放顯示物件。"

# game/tutorial_atl.rpy:799
translate tchinese transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoom 和 yzoom 屬性能讓顯示物件分別在 X、Y 方向縮放。"

# game/tutorial_atl.rpy:809
translate tchinese transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "將 xzoom 或 yzoom 設為負數，就能水平或垂直翻轉圖片。"

# game/tutorial_atl.rpy:819
translate tchinese transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "不同於按倍數縮放，size 變換屬性可以將顯示物件縮放到指定像素大小。"

# game/tutorial_atl.rpy:834
translate tchinese transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "alpha 屬性用來變更顯示物件的不透明度，能讓圖片淡入或淡出。"

# game/tutorial_atl.rpy:847
translate tchinese transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "rotate 屬性會旋轉顯示物件。"

# game/tutorial_atl.rpy:858
translate tchinese transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "預設旋轉顯示物件時，Ren'Py 會在四邊保留額外空間，因此旋轉時大小不會改變。這裡可以看到左上及右下的額外空間。"

# game/tutorial_atl.rpy:870
translate tchinese transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "將 rotate_pad 設為 False 就能移除空間，但代價是顯示物件大小會隨旋轉改變。"

# game/tutorial_atl.rpy:881
translate tchinese transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "tile 變換屬性 xtile 和 ytile 會重複顯示物件多次。"

# game/tutorial_atl.rpy:891
translate tchinese transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "crop 屬性會從顯示物件裁切矩形，只顯示其中一部分。"

# game/tutorial_atl.rpy:905
translate tchinese transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "crop 和 size 一起使用時，可以聚焦圖片的特定部分。"

# game/tutorial_atl.rpy:917
translate tchinese transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "xpan 和 ypan 屬性能讓顯示物件以指定角度（單位為度）平移，0 代表中心。"

# game/tutorial_atl.rpy:924
translate tchinese transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "以上就是必須知道的變換屬性。以正確順序組合它們，就能創造複雜的效果。"

translate tchinese strings:

    # game/tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # game/tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # game/tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"
