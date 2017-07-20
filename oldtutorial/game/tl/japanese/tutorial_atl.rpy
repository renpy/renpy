# Translation updated at 2013-02-18 11:40

# game/tutorial_atl.rpy:187
translate japanese tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "このチュートリアルでは、Ren'Pyの画面上の位置のことについて教えます。しかしその前に、Pythonが数字をどのように扱っているか少し学びましょう。"

# game/tutorial_atl.rpy:189
translate japanese tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Pythonでは数字は主に2種類あります。整数と浮動小数点数です。整数は数字のみで構成されており、浮動小数点数には小数点があります。"

# game/tutorial_atl.rpy:191
translate japanese tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "例えば、100は整数で、0.5は浮動小数点数またはfloatやshortといいます。このシステムでは0は2種類あります。0は整数、0.0は小数です。"

# game/tutorial_atl.rpy:193
translate japanese tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Pyは絶対座標の表現に整数を用います。小数は決まった領域を分割した表現をするのに用います。"

# game/tutorial_atl.rpy:195
translate japanese tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "何かの位置を決定するとき、領域は通常スクリーン全体です。"

# game/tutorial_atl.rpy:197
translate japanese tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "私はここから離れ、どこを位置するのか見せます。"

# game/tutorial_atl.rpy:211
translate japanese tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "原点は画面左上の角です。ここはX座標(xpos)、Y座標(ypos)ともに0となります。"

# game/tutorial_atl.rpy:217
translate japanese tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "xpos を増やすと右に移動します。ここの xpos は .5 で、画面の幅の半分を意味します。"

# game/tutorial_atl.rpy:222
translate japanese tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "xpos を 1.0 に増やすと、画面右手の縁に移動します。"

# game/tutorial_atl.rpy:228
translate japanese tutorial_positions_80be064f:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 800 pixels across, using an xpos of 400 will return the target to the center of the top row."
    e "xpos に絶対座標も使用できます。画面左端からのピクセル数の絶対値で指定します。例えば、このウィンドウの横幅は800ピクセルなので、xpos を 400 にすると、対象は上部中央となります。"

# game/tutorial_atl.rpy:230
translate japanese tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "Y軸の位置、または ypos についても同じことです。今、ypos を 0.0 にしています。"

# game/tutorial_atl.rpy:236
translate japanese tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "ypos を 0.5 にしました。"

# game/tutorial_atl.rpy:241
translate japanese tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "ypos を 1.0 にすると、画面下部の位置を指定したことになります。よく見ると、ポジションインジケーターがテキストウィンドウの裏にあることが分かります。"

# game/tutorial_atl.rpy:243
translate japanese tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "xpos と同様に ypos も整数にすることができます。この場合は、ypos には画面上部からの全ピクセル数を指定します。"

# game/tutorial_atl.rpy:249
translate japanese tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "この位置は画面に対する相対位置でいくらだと思いますか？" nointeract

# game/tutorial_atl.rpy:255
translate japanese tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "残念でした。間違いです。xpos は .75、ypos は .25 です。"

# game/tutorial_atl.rpy:257
translate japanese tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "別の言い方をすれば、左側から 75%% の位置で、上側から 25%% の位置です。"

# game/tutorial_atl.rpy:261
translate japanese tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "いいですね。正しい位置を言い当てました。"

# game/tutorial_atl.rpy:265
translate japanese tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "残念でした。間違いです。xpos は .75、ypos は .25 です。"

# game/tutorial_atl.rpy:267
translate japanese tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "別の言い方をすれば、左側から 75%% の位置で、上側から 25%% の位置です。"

# game/tutorial_atl.rpy:281
translate japanese tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "2つ目に気をつける位置はアンカーです。アンカーは、物の位置決めをするための点です。"

# game/tutorial_atl.rpy:283
translate japanese tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "例えば、今は xanchor が 0.0、yanchor が 0.0 です。この位置はロゴ画像の左上角に当たります。"

# game/tutorial_atl.rpy:288
translate japanese tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "xanchor を 1.0 に増やすと、アンカーは画像の右上角に移動します。"

# game/tutorial_atl.rpy:293
translate japanese tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "同様に、xanchor と yanchor とも 1.0 にすると、アンカーは右下角になります。"

# game/tutorial_atl.rpy:301
translate japanese tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "画面上に画像を位置づけするには、位置とアンカーが必要になります。"

# game/tutorial_atl.rpy:309
translate japanese tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "その2つを並べ、位置とアンカーは画面上の同一の点となります。"

# game/tutorial_atl.rpy:319
translate japanese tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "両方の場所を左上角にとると、画像は画面上の左上角に移動します。"

# game/tutorial_atl.rpy:328
translate japanese tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "位置とアンカーを適切に組み合わせることで、画像の大きさを知らなくても画面上のあらゆる場所を指定できます。"

# game/tutorial_atl.rpy:340
translate japanese tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "xpos と xanchor を同じ値にすると扱いやすいことがあります。これを xalign といい、画面上の位置を小数で指定します。"

# game/tutorial_atl.rpy:345
translate japanese tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "例えば、xalign を 0.0 にすると、画像は画面左側に整列します。"

# game/tutorial_atl.rpy:350
translate japanese tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "1.0 にすると、画面右側に整列します。"

# game/tutorial_atl.rpy:355
translate japanese tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "そして 0.5 にすると、画面中央に戻ります。"

# game/tutorial_atl.rpy:357
translate japanese tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "yalign の設定も同様ですが、Y軸に沿います。"

# game/tutorial_atl.rpy:359
translate japanese tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "xalign は xpos と xanchor を同じ値にするだけ、yalign は ypos と yanchor 同じ値にするだけであることを覚えて下さい。"

# game/tutorial_atl.rpy:366
translate japanese tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "位置について理解できたら、変換を使ってRen'Pyの画面上でものを移動できるようになります。"

# game/tutorial_atl.rpy:373
translate japanese tutorial_atl_a1cc1bff:

    # e "While showing static images is often enough for most games, occasionally we'll want to change images, or move them around the screen."
    e "ゲームでは静止画を表示することが最も多いですが、時々画像を変えたかったり周囲に移動させたかったりします。"

# game/tutorial_atl.rpy:375
translate japanese tutorial_atl_81dbb8f2:

    # e "We call this a Transform, and it's what ATL, Ren'Py's Animation and Transformation Language, is for."
    e "私たちはこれを変換(Transform)と呼び、これを行うのがRen'Pyの ATL (Animation and Transformation Language) です。"

# game/tutorial_atl.rpy:383
translate japanese tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "でも、まずはやりましょう... 無償のロックコンサート！"

# game/tutorial_atl.rpy:391
translate japanese tutorial_atl_3ccfe2ac:

    # e "That was a lot of work, and before you can do that, we'll need to start with the basics of using ATL."
    e "これが出来るようにするのは大変な作業なので、まずはATLの基本的なところから始める必要があります。"

# game/tutorial_atl.rpy:393
translate japanese tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "Ren'Pyには現在、ATLを使用できる場所が3箇所あります。"

# game/tutorial_atl.rpy:397
translate japanese tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "まず1つ目はimageステートメントの一部としてです。imageステートメントは画像の代わりにATLコードのブロックとして定義できます。"

# game/tutorial_atl.rpy:399
translate japanese tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "この方法を使うとき、ATLは実際に表示される画像を1つ、または複数含んでいることを確認して下さい。"

# game/tutorial_atl.rpy:403
translate japanese tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "2つ目の方法は、transformステートメントによる方法です。この方法はATLブロックをPythonの変数に割り当てるので、項や他のtransformの内側に使えるようになります。"

# game/tutorial_atl.rpy:407
translate japanese tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "最後の方法は、ATLブロックをshowステートメントの一部として項の代わりに使う方法です。"

# game/tutorial_atl.rpy:411
translate japanese tutorial_atl_c21bc1d1:

    # e "The key to ATL is what we call composeability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "ATLの鍵となるのはコンポーザーというものです。ATLは比較的単純なコマンドからなり、それらを組み合わせることで複雑な変換を作成できます。"

# game/tutorial_atl.rpy:413
translate japanese tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "ATLでどのようなことが出来るかの前に、アニメーションと変換とは何かを説明します。"

# game/tutorial_atl.rpy:418
translate japanese tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "アニメーションは画像の表示が変わるときを言います。例えば、このように私の表情が変化しているようにです。"

# game/tutorial_atl.rpy:445
translate japanese tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "変換は、画像が移動や変形を伴うときを言います。画面への表示、拡大・縮小、回転、透明度の変更といったものが含まれます。"

# game/tutorial_atl.rpy:453
translate japanese tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "ATLを取り入れるために、簡単なアニメーションを見ることから始めましょう。imageステートメントに含まれた5行からなるATLコードがあります。"

# game/tutorial_atl.rpy:455
translate japanese tutorial_atl_12c839ee:

    # e "In ATL, to change a displayable, simply mention it on a line of ATL code. Here, we're switching back and forth between two images."
    e "ATLでは、画像を変更するために簡単なコードが記述されています。ここでは2つの画像を交互に切り替えています。"

# game/tutorial_atl.rpy:457
translate japanese tutorial_atl_c671ed7d:

    # e "Since we're defining an image, the first line of ATL has to name a displayable. Otherwise, there would be nothing to show."
    e "画像を定義するため、ATLの1行目には画像の名前があります。これがない場合、画像は何も表示されません。"

# game/tutorial_atl.rpy:459
translate japanese tutorial_atl_99386181:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half of a second each before continuing. That's how we give the delay between images."
    e "2行目と4行目にはpauseステートメントがあり、ATLは続行する前に0.5秒間停止します。これで画像と画像の間に時間差を付けることができます。"

# game/tutorial_atl.rpy:461
translate japanese tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "最後の行はrepeatステートメントです。これによって現在のブロックが再スタートします。repeatステートメントは1つのブロックにつき1つまで使えます。"

# game/tutorial_atl.rpy:466
translate japanese tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "代わりに repeat 2 と書いた場合は、アニメーションは2回繰り返して停止します。"

# game/tutorial_atl.rpy:471
translate japanese tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "repeatステートメントを省略した場合は、一度ATLコードの終端に達するとアニメーションは停止します。"

# game/tutorial_atl.rpy:476
translate japanese tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "デフォルトでは画像は瞬時に置き換えられます。設定すれば、画像と画像の間にトランジションをつけることもできます。"

# game/tutorial_atl.rpy:483
translate japanese tutorial_atl_a7f8ed01:

    # e "Now, let's move on to see how we can use ATL to transform an image. We'll start off by seeing what we can do to position images on the screen."
    e "では、次はATLをどのように使うことで画像を変換できるか見てみましょう。画像の配置を変えることから始めます。"

# game/tutorial_atl.rpy:492
translate japanese tutorial_atl_24501213:

    # e "Perhaps the simplest thing we can do is to position the images on the screen. This can be done by simply giving the names of the transform properties, each followed by the value."
    e "おそらく、最も簡単に出来ることは画像の配置を変えることです。これは単純に、決まった変換プロパティーに各々の値を設定するだけでできます。"

# game/tutorial_atl.rpy:497
translate japanese tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "さらにいくつかのステートメントを加えると、画面上を移動させることができます。"

# game/tutorial_atl.rpy:499
translate japanese tutorial_atl_8b053b5a:

    # e "This code starts the image off at the top-right of the screen, and waits a second."
    e "このコードは、まず画像を画面右上に設置して、1秒間待機します。"

# game/tutorial_atl.rpy:501
translate japanese tutorial_atl_d7fc5372:

    # e "It then moves it to the left side, waits another second, and repeats."
    e "次に画像を左側に設置してもう1秒間待ち、それを繰り返します。"

# game/tutorial_atl.rpy:503
translate japanese tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "pauseとrepeatステートメントは、アニメーションの時に使ったステートメントと同じです。これらはATLコード全体で動作します。"

# game/tutorial_atl.rpy:508
translate japanese tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "画像が画面を跳び回るのは、使いやすいとは限りません。そこで、ATLには補間ステートメントがあります。"

# game/tutorial_atl.rpy:510
translate japanese tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "補間ステートメントを使うと、変換プロパティーの値を古い値から新しい値に徐々に変化させることができます。"

# game/tutorial_atl.rpy:512
translate japanese tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "ATLの2行目に補間ステートメントを入れたものです。これは時間関数の名前から始まっています。この場合は linear です。"

# game/tutorial_atl.rpy:514
translate japanese tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "次に継続時間が来ます。この場合は3秒です。そしてプロパティーのリストで終わります。各プロパティーにはそれぞれの新しい値が続きます。"

# game/tutorial_atl.rpy:516
translate japanese tutorial_atl_72d47fb6:

    # e "The old value is the value of the transform property at the start of the statement. By interpolating the property over time, we can change things on the screen."
    e "古い値は、ステートメントの始めにある変換プロパティーの値です。一定期間プロパティーを補間することで、この値を変えられます。"

# game/tutorial_atl.rpy:526
translate japanese tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATLは、円や曲線的な動きのような、もっと複雑な動きにも対応しています。しかし、ここでは示しません。"

# game/tutorial_atl.rpy:528
translate japanese tutorial_atl_4a02c8d8:

    # e "Next, let's take a look at some of the transform properties that we can change using ATL."
    e "次に、ATLを使って変えられる変換プロパティーをいくつか見てみましょう。"

# game/tutorial_atl.rpy:543
translate japanese tutorial_atl_821fcb91:

    # e "We've already seen the position properties. Along with xalign and yalign, we support the xpos, ypos, xanchor, and yanchor properties."
    e "位置プロパティーは既に見ました。xalign、yalign、xpos、ypos、xanchor、yanchorプロパティーも同様に対応しています。"

# game/tutorial_atl.rpy:558
translate japanese tutorial_atl_cca5082b:

    # e "We can perform a pan by using xpos and ypos to position images off of the screen."
    e "xposとyposを使って画像の位置を変えることで、パンを演出できます。"

# game/tutorial_atl.rpy:560
translate japanese tutorial_atl_0394dd50:

    # e "This usually means giving them negative positions."
    e "パンでは通常、位置に負の値を設定します。"

# game/tutorial_atl.rpy:577
translate japanese tutorial_atl_2624662e:

    # e "The zoom property lets us scale the displayable by a factor, making it bigger and smaller. For best results, zoom should always be greater than 0.5."
    e "zoomプロパティーを使うと、倍率によって画像を拡大・縮小できます。いい結果を得るには、倍率は常に0.5以上にすべきです。"

# game/tutorial_atl.rpy:591
translate japanese tutorial_atl_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoomとyzoomプロパティーを使うと、画像をX方向とY方向、別々にスケールできます。"

# game/tutorial_atl.rpy:602
translate japanese tutorial_atl_9fe238de:

    # e "The size property can be used to set a size, in pixels, that the displayable is scaled to."
    e "sizeプロパティーは、大きさをピクセル単位で設定することで、画像をスケールできます。"

# game/tutorial_atl.rpy:617
translate japanese tutorial_atl_6b982a23:

    # e "The alpha property allows us to vary the opacity of a displayable. This can make it appear and disappear."
    e "alphaプロパティーを使うと、画像の透明度を変えられます。これによって、画像の表示・非表示を切り替えられます。"

# game/tutorial_atl.rpy:631
translate japanese tutorial_atl_60d6d9f3:

    # e "The rotate property lets us rotate a displayable."
    e "rotateプロパティーを使うと、画像を回転できます。"

# game/tutorial_atl.rpy:633
translate japanese tutorial_atl_898a138a:

    # e "Since rotation can change the size, usually you'll want to set xanchor and yanchor to 0.5 when positioning a rotated displayable."
    e "回転処理は画像の大きさが変わるので、画像を回転させる時は通常xanchorとyanchorを0.5に設定する必要があります。"

# game/tutorial_atl.rpy:644
translate japanese tutorial_atl_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "cropプロパティーは画像を長方形に切り抜いて、一部のみ表示します。"

# game/tutorial_atl.rpy:658
translate japanese tutorial_atl_ebb84988:

    # e "When used together, they can be used to focus in on specific parts of an image."
    e "これらを一緒に使うと、画像を指定した部分にフォーカスできます。"

# game/tutorial_atl.rpy:664
translate japanese tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "画像、一時停止、補間、繰り返しの他に、ATLの一部に使えるステートメントはもう少しあります。"

# game/tutorial_atl.rpy:678
translate japanese tutorial_atl_db6302bd:

    # e "When we create an ATL transform using the transform statement, we can use that transform as an ATL statement."
    e "transformステートメントを使ってATL変換を作ると、その変換をATLのステートメントに使うことができます。"

# game/tutorial_atl.rpy:680
translate japanese tutorial_atl_785911cf:

    # e "Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "デフォルトの位置も変換の一つなので、left、right、centerをATLブロックの中に使えます。"

# game/tutorial_atl.rpy:698
translate japanese tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "ここで、新しいステートメントが2つ出てきました。blockステートメントを使うと、ATLコードにブロックを含められるようになります。ブロックの中でrepeatステートメントが使われると、ATL変換の一部だけが繰り返されます。"

# game/tutorial_atl.rpy:700
translate japanese tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "timeステートメントもあります。これは、ブロックが開始してから指定した時間が経過すると、次に進みます。これは、たとえ他のステートメントが実行中であっても、それを止めて実行します。"

# game/tutorial_atl.rpy:702
translate japanese tutorial_atl_30dc0008:

    # e "So this code will bounce the image back and forth for eleven and a half seconds, and then move back to the right side of the screen."
    e "なので、このコードはまず画像を左右に弾ませることを11.5秒間行い、その後、画像を画面右側に戻します。"

# game/tutorial_atl.rpy:718
translate japanese tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "parallelステートメントを使うと、2つのATLコードのブロックを同時に実行できます。"

# game/tutorial_atl.rpy:720
translate japanese tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "ここでは、前のブロックでは画像を水平方向に移動し、後ろのブロックでは垂直方向に移動します。これらは異なる速度で動いているので、画像が画面上を跳ねているように見えます。"

# game/tutorial_atl.rpy:737
translate japanese tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "最後に、choiceステートメントはRen'PyにATLコードのブロックをランダムに選択させます。これにより、Ren'Pyの表示を様々なバリエーションにできます。"

# game/tutorial_atl.rpy:743
translate japanese tutorial_atl_5fc8c0df:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out the ATL chapter in the reference manual."
    e "このチュートリアルゲームでやったことは、ATLで出来ることのほんの一部に過ぎません。例えば、onとeventステートメントについては扱っていません。更なる情報はリファレンスマニュアルのATLの章を見るといいでしょう。"

# game/tutorial_atl.rpy:747
translate japanese tutorial_atl_1358c6b4:

    # e "But for now, just remember that when it comes to animating and transforming, ATL is the hot new thing."
    e "しかし今は、アニメーションと変換について、ATLは最新の方法だということを覚えておいて下さい。"

translate japanese strings:

    # game/tutorial_atl.rpy:249
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # game/tutorial_atl.rpy:249
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # game/tutorial_atl.rpy:249
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"

