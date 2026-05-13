
# game/tutorial_atl.rpy:205
translate japanese tutorial_positions_a09a3fd1:

    # e "In this tutorial, I'll teach you how Ren'Py positions things on the screen. But before that, let's learn a little bit about how Python handles numbers."
    e "このチュートリアルでは、Ren'Pyの画面上の位置のことについて教えます。しかしその前に、Pythonが数字をどのように扱っているか少し学びましょう。"

# game/tutorial_atl.rpy:207
translate japanese tutorial_positions_ba39aabc:

    # e "There are two main kinds of numbers in Python: integers and floating point numbers. An integer consists entirely of digits, while a floating point number has a decimal point."
    e "Pythonでは数字は主に2種類あります。整数と浮動小数点数です。整数は数字のみで構成されており、浮動小数点数には小数点があります。"

# game/tutorial_atl.rpy:209
translate japanese tutorial_positions_a60b775d:

    # e "For example, 100 is an integer, while 0.5 is a floating point number, or float for short. In this system, there are two zeros: 0 is an integer, and 0.0 is a float."
    e "例えば、100は整数で、0.5は浮動小数点数またはfloatやshortといいます。このシステムでは0は2種類あります。0は整数、0.0は小数です。"

# game/tutorial_atl.rpy:211
translate japanese tutorial_positions_7f1a560c:

    # e "Ren'Py uses integers to represent absolute coordinates, and floats to represent fractions of an area with known size."
    e "Ren'Pyは絶対座標の表現に整数を、サイズが分っている領域の割合の表現に小数を用います。"
# game/tutorial_atl.rpy:213
translate japanese tutorial_positions_8e7d3e52:

    # e "When we're positioning something, the area is usually the entire screen."
    e "何かの位置を決定するとき、領域は通常スクリーン全体です。"

# game/tutorial_atl.rpy:215
translate japanese tutorial_positions_fdcf9d8b:

    # e "Let me get out of the way, and I'll show you where some positions are."
    e "私はここから離れ、どこを位置するのか見せます。"

# game/tutorial_atl.rpy:229
translate japanese tutorial_positions_76d7a5bf:

    # e "The origin is the upper-left corner of the screen. That's where the x position (xpos) and the y position (ypos) are both zero."
    e "原点は画面左上の角です。ここはX座標(xpos)、Y座標(ypos)ともに0となります。"

# game/tutorial_atl.rpy:235
translate japanese tutorial_positions_be14c7c3:

    # e "When we increase xpos, we move to the right. So here's an xpos of .5, meaning half the width across the screen."
    e "xpos を増やすと右に移動します。ここの xpos は .5 で、画面の幅の半分を意味します。"

# game/tutorial_atl.rpy:240
translate japanese tutorial_positions_9b91be6c:

    # e "Increasing xpos to 1.0 moves us to the right-hand border of the screen."
    e "xpos を 1.0 に増やすと、画面右手の縁に移動します。"

# game/tutorial_atl.rpy:246
translate japanese tutorial_positions_2b293304:

    # e "We can also use an absolute xpos, which is given in an absolute number of pixels from the left side of the screen. For example, since this window is 1280 pixels across, using an xpos of 640 will return the target to the center of the top row."
    e "xpos に絶対座標も使用できます。画面左端からのピクセル数の絶対値で指定します。例えば、このウィンドウの横幅は1280ピクセルなので、xpos を 640 にすると、対象は上部中央となります。"

# game/tutorial_atl.rpy:248
translate japanese tutorial_positions_c4d18c0a:

    # e "The y-axis position, or ypos works the same way. Right now, we have a ypos of 0.0."
    e "Y軸の位置、または ypos についても同じことです。今、ypos を 0.0 にしています。"

# game/tutorial_atl.rpy:254
translate japanese tutorial_positions_16933a61:

    # e "Here's a ypos of 0.5."
    e "ypos を 0.5 にしました。"

# game/tutorial_atl.rpy:259
translate japanese tutorial_positions_6eb36777:

    # e "A ypos of 1.0 specifies a position at the bottom of the screen. If you look carefully, you can see the position indicator spinning below the text window."
    e "ypos を 1.0 にすると、画面下部の位置を指定したことになります。よく見ると、ポジションインジケーターがテキストウィンドウの裏にあることが分かります。"

# game/tutorial_atl.rpy:261
translate japanese tutorial_positions_a423050f:

    # e "Like xpos, ypos can also be an integer. In this case, ypos would give the total number of pixels from the top of the screen."
    e "xpos と同様に ypos も整数にすることができます。この場合は、ypos には画面上部からの全ピクセル数を指定します。"

# game/tutorial_atl.rpy:267
translate japanese tutorial_positions_bc7a809a:

    # e "Can you guess where this position is, relative to the screen?" nointeract
    e "この位置は画面に対する相対位置でいくらだと思いますか？" nointeract

# game/tutorial_atl.rpy:273
translate japanese tutorial_positions_6f926e18:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "残念でした。間違いです。xpos は .75、ypos は .25 です。"

# game/tutorial_atl.rpy:275
translate japanese tutorial_positions_5d5feb98:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "別の言い方をすれば、左側から 75%% の位置で、上側から 25%% の位置です。"

# game/tutorial_atl.rpy:279
translate japanese tutorial_positions_77b45218:

    # e "Good job! You got that position right."
    e "いいですね。正しい位置を言い当てました。"

# game/tutorial_atl.rpy:283
translate japanese tutorial_positions_6f926e18_1:

    # e "Sorry, that's wrong. The xpos is .75, and the ypos is .25."
    e "残念でした。間違いです。xpos は .75、ypos は .25 です。"

# game/tutorial_atl.rpy:285
translate japanese tutorial_positions_5d5feb98_1:

    # e "In other words, it's 75%% of the way from the left side, and 25%% of the way from the top."
    e "別の言い方をすれば、左側から 75%% の位置で、上側から 25%% の位置です。"

# game/tutorial_atl.rpy:299
translate japanese tutorial_positions_e4380a83:

    # e "The second position we care about is the anchor. The anchor is a spot on the thing being positioned."
    e "2つ目に気をつける位置はアンカーです。アンカーは、物の位置決めをするための点です。"

# game/tutorial_atl.rpy:301
translate japanese tutorial_positions_d1db1246:

    # e "For example, here we have an xanchor of 0.0 and a yanchor of 0.0. It's in the upper-left corner of the logo image."
    e "例えば、今は xanchor が 0.0、yanchor が 0.0 です。この位置はロゴ画像の左上角に当たります。"

# game/tutorial_atl.rpy:306
translate japanese tutorial_positions_6056873f:

    # e "When we increase the xanchor to 1.0, the anchor moves to the right corner of the image."
    e "xanchor を 1.0 に増やすと、アンカーは画像の右上角に移動します。"

# game/tutorial_atl.rpy:311
translate japanese tutorial_positions_7cdb8dcc:

    # e "Similarly, when both xanchor and yanchor are 1.0, the anchor is the bottom-right corner."
    e "同様に、xanchor と yanchor とも 1.0 にすると、アンカーは右下角になります。"

# game/tutorial_atl.rpy:318
translate japanese tutorial_positions_03a07da8:

    # e "To place an image on the screen, we need both the position and the anchor."
    e "画面上に画像を位置づけするには、位置とアンカーが必要になります。"

# game/tutorial_atl.rpy:326
translate japanese tutorial_positions_8945054f:

    # e "We then line them up, so that both the position and anchor are at the same point on the screen."
    e "その2つを並べ、位置とアンカーは画面上の同一の点となります。"

# game/tutorial_atl.rpy:336
translate japanese tutorial_positions_2b184a93:

    # e "When we place both in the upper-left corner, the image moves to the upper-left corner of the screen."
    e "両方の場所を左上角にとると、画像は画面上の左上角に移動します。"

# game/tutorial_atl.rpy:345
translate japanese tutorial_positions_5aac4f3f:

    # e "With the right combination of position and anchor, any place on the screen can be specified, without even knowing the size of the image."
    e "位置とアンカーを適切に組み合わせるて、画像の大きさを知らなくても画面上のあらゆる場所を指定できます。"

# game/tutorial_atl.rpy:357
translate japanese tutorial_positions_3b59b797:

    # e "It's often useful to set xpos and xanchor to the same value. We call that xalign, and it gives a fractional position on the screen."
    e "xpos と xanchor を同じ値にすると扱いやすいことがあります。これを xalign といい、画面上の位置を小数で指定します。"

# game/tutorial_atl.rpy:362
translate japanese tutorial_positions_b8ebf9fe:

    # e "For example, when we set xalign to 0.0, things are aligned to the left side of the screen."
    e "例えば、xalign を 0.0 にすると、画像は画面左側に整列します。"

# game/tutorial_atl.rpy:367
translate japanese tutorial_positions_8ce35d52:

    # e "When we set it to 1.0, then we're aligned to the right side of the screen."
    e "1.0 にすると、画面右側に整列します。"

# game/tutorial_atl.rpy:372
translate japanese tutorial_positions_6745825f:

    # e "And when we set it to 0.5, we're back to the center of the screen."
    e "そして 0.5 にすると、画面中央に戻ります。"

# game/tutorial_atl.rpy:374
translate japanese tutorial_positions_64428a07:

    # e "Setting yalign is similar, except along the y-axis."
    e "yalign の設定も同様ですが、Y軸に沿います。"

# game/tutorial_atl.rpy:376
translate japanese tutorial_positions_cfb77d42:

    # e "Remember that xalign is just setting xpos and xanchor to the same value, and yalign is just setting ypos and yanchor to the same value."
    e "xalign は xpos と xanchor を同じ値にするだけ、yalign は ypos と yanchor 同じ値にするだけであることを覚えて下さい。"

# game/tutorial_atl.rpy:381
translate japanese tutorial_positions_cfc1723e:

    # e "The xcenter and ycenter properties position the center of the image. Here, with xcenter set to .75, the center of the image is three-quarters of the way to the right side of the screen."
    e "xcenter と ycenter プロパティーは画像の中心を指定します。ここでは xcenter .75 に設定され、画像の中心は画面右側3/4の位置にあります。"

# game/tutorial_atl.rpy:386
translate japanese tutorial_positions_7728dbf9:

    # e "The difference between xalign and xcenter is more obvious when xcenter is 1.0, and the image is halfway off the right side of the screen."
    e "xalign や yalign との違いは xcenter が 1.0 のときに分かりやすく、画像が画面右端で半分になります。"

# game/tutorial_atl.rpy:394
translate japanese tutorial_positions_1b1cedc6:

    # e "There are the xoffset and yoffset properties, which are applied after everything else, and offset things to the right or bottom, respectively."
    e "xoffset や yoffset プロパティーは他すべての後に適用され、それぞれ右または下側へオフセットします。"

# game/tutorial_atl.rpy:399
translate japanese tutorial_positions_e6da2798:

    # e "Of course, you can use negative numbers to offset things to the left and top."
    e "もちろん左と上への負のオフセット値も指定できます。"

# game/tutorial_atl.rpy:404
translate japanese tutorial_positions_e0fe2d81:

    # e "Lastly, I'll mention that there are combined properties like align, pos, anchor, and center. Align takes a pair of numbers, and sets xalign to the first and yalign to the second. The others are similar."
    e "最後に、align, pos, anchor, centerのような組合せ合わせられのプロパティーに言及しましょう。alignは数値のペアをとってxalignを一つ目に、yalignを二つ目に設定します。他も同様です。"

# game/tutorial_atl.rpy:411
translate japanese tutorial_positions_0f4ca2b6:

    # e "Once you understand positions, you can use transformations to move things around the Ren'Py screen."
    e "位置について理解できたら、Transformを使ってRen'Pyの画面上でものを移動できるようになります。"

# game/tutorial_atl.rpy:418
translate japanese tutorial_atl_d5d6b62a:

    # e "Ren'Py uses transforms to animate, manipulate, and place images. We've already seen the very simplest of transforms in use:"
    e "Ren'PyはTransformを使って画像のアニメーションや操作、配置をします。もっとも簡単なTransformがこちらです。:"

# game/tutorial_atl.rpy:425
translate japanese tutorial_atl_7e853c9d:

    # e "Transforms can be very simple affairs that place the image somewhere on the screen, like the right transform."
    e "Transformはright Transformのように画像を画面のどこかに配置するとても簡単なものもあります。"

# game/tutorial_atl.rpy:429
translate japanese tutorial_atl_87a6ecbd:

    # e "But transforms can also be far more complicated affairs, that introduce animation and effects into the mix. To demonstrate, let's have a Gratuitous Rock Concert!"
    e "しかしTransformはアニメーションやエフェクトのようなよりずっと複雑なこともできます。デモンストレーションとして無償のロックコンサートを初めましょう。"

# game/tutorial_atl.rpy:437
translate japanese tutorial_atl_65badef3:

    # e "But first, let's have... a Gratuitous Rock Concert!"
    e "でも、まずはやりましょう... 無償のロックコンサート！"

# game/tutorial_atl.rpy:445
translate japanese tutorial_atl_e0d3c5ec:

    # e "That was a lot of work, but it was built out of small parts."
    e "これが出来るようにするのは大変な作業ですが、いくかの小さな部分で成り立っています。"

# game/tutorial_atl.rpy:447
translate japanese tutorial_atl_f2407514:

    # e "Most transforms in Ren'Py are built using the Animation and Transform Language, or ATL for short."
    e "Ren'PyのほとんどのTransformはAnimation and Transform LanguageつまりATLを使用して作成されています。"

# game/tutorial_atl.rpy:449
translate japanese tutorial_atl_1f22f875:

    # e "There are currently three places where ATL can be used in Ren'Py."
    e "Ren'Pyには現在、ATLを使用できる場所が3箇所あります。"

# game/tutorial_atl.rpy:454
translate japanese tutorial_atl_fd036bdf:

    # e "The first place ATL can be used is as part of an image statement. Instead of a displayable, an image may be defined as a block of ATL code."
    e "まず1つ目はimageステートメントの一部としてです。imageステートメントは画像の代わりにATLコードのブロックとして定義できます。"

# game/tutorial_atl.rpy:456
translate japanese tutorial_atl_7cad2ab9:

    # e "When used in this way, we have to be sure that ATL includes one or more displayables to actually show."
    e "この方法を使うとき、ATLは実際に表示される画像を1つ、または複数含んでいることを確認して下さい。"

# game/tutorial_atl.rpy:461
translate japanese tutorial_atl_c78b2a1e:

    # e "The second way is through the use of the transform statement. This assigns the ATL block to a python variable, allowing it to be used in at clauses and inside other transforms."
    e "2つ目の方法は、transformステートメントによる方法です。この方法はATLブロックをPythonの変数に割り当てるので、節や他のtransformの内側に使えるようになります。"

# game/tutorial_atl.rpy:473
translate japanese tutorial_atl_da7a7759:

    # e "Finally, an ATL block can be used as part of a show statement, instead of the at clause."
    e "最後の方法は、ATLブロックをshowステートメントの一部として節の代わりに使う方法です。"

# game/tutorial_atl.rpy:480
translate japanese tutorial_atl_1dd345c6:

    # e "When ATL is used as part of a show statement, values of properties exist even when the transform is changed. So even though your click stopped the motion, the image remains in the same place."
    e "ATLがshowステートメントの一部に使用されると、プロパティーの値はTransformが変更された時も残ります。このためクリックで移動を止めても画像は同じ場所に残ります。"

# game/tutorial_atl.rpy:488
translate japanese tutorial_atl_98047789:

    # e "The key to ATL is what we call composability. ATL is made up of relatively simple commands, which can be combined together to create complicated transforms."
    e "ATLの鍵となるのはコンポーザーというものです。ATLは比較的単純なコマンドからなり、それらを組み合わせて複雑なTransformを作成できます。"

# game/tutorial_atl.rpy:490
translate japanese tutorial_atl_ed82983f:

    # e "Before I explain how ATL works, let me explain what animation and transformation are."
    e "ATLでどのようなことが出来るかの前に、アニメーションとTransformとは何かを説明します。"

# game/tutorial_atl.rpy:495
translate japanese tutorial_atl_2807adff:

    # e "Animation is when the displayable being shown changes. For example, right now I am changing my expression."
    e "アニメーションは画像の表示が変わるときを言います。例えば、このように私の表情が変化しているようにです。"

# game/tutorial_atl.rpy:522
translate japanese tutorial_atl_3eec202b:

    # e "Transformation involves moving or distorting an image. This includes placing it on the screen, zooming it in and out, rotating it, and changing its opacity."
    e "Transformは、画像の移動や変形を意味します。画面への表示、拡大・縮小、回転、透明度の変更といったものが含まれます。"

# game/tutorial_atl.rpy:530
translate japanese tutorial_atl_fbc9bf83:

    # e "To introduce ATL, let's start by looking at at a simple animation. Here's one that consists of five lines of ATL code, contained within an image statement."
    e "ATLを取り入れるために、簡単なアニメーションを見ることから始めましょう。imageステートメントに含まれた5行からなるATLコードがあります。"

# game/tutorial_atl.rpy:532
translate japanese tutorial_atl_bf92d973:

    # e "To change a displayable, simply mention it on a line of ATL. Here, we're switching back and forth between two images."
    e "画像を変更するために簡単なコードが記述されています。ここでは2つの画像を交互に切り替えています。"

# game/tutorial_atl.rpy:534
translate japanese tutorial_atl_51a41db4:

    # e "Since we're defining an image, the first line of ATL must give a displayable. Otherwise, there would be nothing to show."
    e "画像を定義するため、ATLの1行目には画像があります。これがない場合、画像は何も表示されません。"

# game/tutorial_atl.rpy:536
translate japanese tutorial_atl_3d065074:

    # e "The second and fourth lines are pause statements, which cause ATL to wait half a second each before continuing. That's how we give the delay between images."
    e "2行目と4行目にはpauseステートメントがあり、ATLは続行する前に0.5秒間停止します。これで画像と画像の間に時間差を付けることができます。"

# game/tutorial_atl.rpy:538
translate japanese tutorial_atl_60f2a5e8:

    # e "The final line is a repeat statement. This causes the current block of ATL to be restarted. You can only have one repeat statement per block."
    e "最後の行はrepeatステートメントです。これによって現在のブロックが再スタートします。repeatステートメントは1つのブロックにつき1つまで使えます。"

# game/tutorial_atl.rpy:543
translate japanese tutorial_atl_146cf4c4:

    # e "If we were to write repeat 2 instead, the animation would loop twice, then stop."
    e "代わりに repeat 2 と書いた場合は、アニメーションは2回繰り返して停止します。"

# game/tutorial_atl.rpy:548
translate japanese tutorial_atl_d90b1838:

    # e "Omitting the repeat statement means that the animation stops once we reach the end of the block of ATL code."
    e "repeatステートメントを省略した場合は、一度ATLコードの終端に達するとアニメーションは停止します。"

# game/tutorial_atl.rpy:554
translate japanese tutorial_atl_e5872360:

    # e "By default, displayables are replaced instantaneously. We can also use a with clause to give a transition between displayables."
    e "デフォルトでは画像は瞬時に置き換えられます。設定すれば、画像と画像の間にトランジションをつけることもできます。"

# game/tutorial_atl.rpy:561
translate japanese tutorial_atl_2e9d63ea:

    # e "With animation done, we'll see how we can use ATL to transform images, starting with positioning an image on the screen."
    e "アニメーションを実行してATLによってどのように画像をTransformするかを見ましょう。まずは画面に画像を配置します。"

# game/tutorial_atl.rpy:570
translate japanese tutorial_atl_ddc55039:

    # e "The simplest thing we can to is to statically position an image. This is done by giving the names of the position properties, followed by the property values."
    e "最も簡単に出来ることは静的に画像の配置を変えることです。これは位置プロパティー名に続いてプロパティーの値を設定してできます。"

# game/tutorial_atl.rpy:575
translate japanese tutorial_atl_43516492:

    # e "With a few more statements, we can move things around on the screen."
    e "さらにいくつかのステートメントを加えると、画面上を移動させることができます。"

# game/tutorial_atl.rpy:577
translate japanese tutorial_atl_fb979287:

    # e "This example starts the image off at the top-right of the screen, and waits a second. It then moves it to the left side, waits another second, and repeats."
    e "この例はまず画像を画面右上に設置して、1秒間待機します。次に画像を左側に設置してもう1秒間待ち、それを繰り返します。"

# game/tutorial_atl.rpy:579
translate japanese tutorial_atl_7650ec09:

    # e "The pause and repeat statements are the same statements we used in our animations. They work throughout ATL code."
    e "pauseとrepeatステートメントは、アニメーションの時に使ったステートメントと同じです。これらはATLコード全体で動作します。"

# game/tutorial_atl.rpy:584
translate japanese tutorial_atl_d3416d4f:

    # e "Having the image jump around on the screen isn't all that useful. That's why ATL has the interpolation statement."
    e "画像が画面を跳び回るのは、使いやすいとは限りません。そこで、ATLには補間ステートメントがあります。"

# game/tutorial_atl.rpy:586
translate japanese tutorial_atl_4e7512ec:

    # e "The interpolation statement allows you to smoothly vary the value of a transform property, from an old to a new value."
    e "補間ステートメントを使うと、Transformプロパティーの値を古い値から新しい値に少しずつ変化させることができます。"

# game/tutorial_atl.rpy:588
translate japanese tutorial_atl_685eeeaa:

    # e "Here, we have an interpolation statement on the second ATL line. It starts off with the name of a time function, in this case linear."
    e "ATLの2行目に補間ステートメントを入れたものです。これは時間関数の名前から始まっています。この場合は linear です。"

# game/tutorial_atl.rpy:590
translate japanese tutorial_atl_c5cb49de:

    # e "That's followed by an amount of time, in this case three seconds. It ends with a list of properties, each followed by its new value."
    e "次に継続時間が来ます。この場合は3秒です。そしてプロパティーのリストで終わります。各プロパティーにはそれぞれの新しい値が続きます。"

# game/tutorial_atl.rpy:592
translate japanese tutorial_atl_04b8bc1d:

    # e "The value of each property is interpolated from its value when the statement starts to the value at the end of the statement. This is done once per frame, allowing smooth animation."
    e "各プロパティーの値はステートメント開始時の値から終了時の値まで補間されます。これをフレーム毎に実行して滑らかなアニメーションを実現します。"

# game/tutorial_atl.rpy:603
translate japanese tutorial_atl_2958f397:

    # e "ATL supports more complicated move types, like circle and spline motion. But I won't be showing those here."
    e "ATLは、円や曲線的な動きのような、もっと複雑な動きにも対応しています。しかし、ここでは示しません。"

# game/tutorial_atl.rpy:607
translate japanese tutorial_atl_d08fe8d9:

    # e "Apart from displayables, pause, interpolation, and repeat, there are a few other statements we can use as part of ATL."
    e "画像、一時停止、補間、繰り返しの他に、ATLの一部に使えるステートメントはもう少しあります。"

# game/tutorial_atl.rpy:619
translate japanese tutorial_atl_84b22ac0:

    # e "ATL transforms created using the statement become ATL statements themselves. Since the default positions are also transforms, this means that we can use left, right, and center inside of an ATL block."
    e "ステートメントで作成されたATL Transformは自身もATLステートメントとなります。デフォルトの位置もTransformの一つなので、left、right、centerをATLブロックの中に使えます。"

# game/tutorial_atl.rpy:635
translate japanese tutorial_atl_331126c1:

    # e "Here, we have two new statements. The block statement allows you to include a block of ATL code. Since the repeat statement applies to blocks, this lets you repeat only part of an ATL transform."
    e "ここで、新しいステートメントが2つ出てきました。blockステートメントを使うと、ATLコードにブロックを含められるようになります。ブロックの中でrepeatステートメントが使われると、ATL Transformの一部だけが繰り返されます。"

# game/tutorial_atl.rpy:637
translate japanese tutorial_atl_24f67b67:

    # e "We also have the time statement, which runs after the given number of seconds have elapsed from the start of the block. It will run even if another statement is running, stopping the other statement."
    e "timeステートメントもあります。これは、ブロックが開始してから指定した時間が経過すると、次に進みます。これは、たとえ他のステートメントが実行中であっても、それを止めて実行します。"

# game/tutorial_atl.rpy:639
translate japanese tutorial_atl_b7709507:

    # e "So this example bounces the image back and forth for eleven and a half seconds, and then moves it to the right side of the screen."
    e "なので、この例はまず画像を左右に弾ませることを11.5秒間行い、その後、画像を画面右側に戻します。"

# game/tutorial_atl.rpy:653
translate japanese tutorial_atl_f903bc3b:

    # e "The parallel statement lets us run two blocks of ATL code at the same time."
    e "parallelステートメントを使うと、2つのATLコードのブロックを同時に実行できます。"

# game/tutorial_atl.rpy:655
translate japanese tutorial_atl_5d0f8f9d:

    # e "Here, the top block move the image in the horizontal direction, and the bottom block moves it in the vertical direction. Since they're moving at different speeds, it looks like the image is bouncing on the screen."
    e "ここでは、前のブロックでは画像を水平方向に移動し、後ろのブロックでは垂直方向に移動します。これらは異なる速度で動いているので、画像が画面上を跳ねているように見えます。"

# game/tutorial_atl.rpy:669
translate japanese tutorial_atl_28a7d27e:

    # e "Finally, the choice statement makes Ren'Py randomly pick a block of ATL code. This allows you to add some variation as to what Ren'Py shows."
    e "最後に、choiceステートメントはRen'PyにATLコードのブロックをランダムに選択させます。これにより、Ren'Pyの表示を多様なバリエーションにできます。"

# game/tutorial_atl.rpy:675
translate japanese tutorial_atl_2265254b:

    # e "This tutorial game has only scratched the surface of what you can do with ATL. For example, we haven't even covered the on and event statements. For more information, you might want to check out {a=https://renpy.org/doc/html/atl.html}the ATL chapter in the reference manual{/a}."
    e "このチュートリアルゲームはATLでできることのほんの一部で、onやeventステートメントもカバーしていません。詳しくは{a=https://ja.renpy.org/doc/html/atl.html}マニュアルのATLの項{/a}を参照してください。"

# game/tutorial_atl.rpy:684
translate japanese transform_properties_391169cf:

    # e "Ren'Py has quite a few transform properties that can be used with ATL, the Transform displayable, and the add Screen Language statement."
    e "Ren'PyにATLやTransform displayable、スクリーン言語ステートメントで使えるはかなりの数のTransformプロパティーがあります。"

# game/tutorial_atl.rpy:685
translate japanese transform_properties_fc895a1f:

    # e "Here, we'll show them off so you can see them in action and get used to what each does."
    e "ここでそれらを紹介して、それらが何をするかに慣れましょう。"

# game/tutorial_atl.rpy:701
translate japanese transform_properties_88daf990:

    # e "First off, all of the position properties are also transform properties. These include the pos, anchor, align, center, and offset properties."
    e "最初に、すべての位置プロパティーはTransformプロパティーでもあります。これらにはpos,  anchor,  center,  offsetプロパティーを含みます。"

# game/tutorial_atl.rpy:719
translate japanese transform_properties_d7a487f1:

    # e "The position properties can also be used to pan over a displayable larger than the screen, by giving xpos and ypos negative values."
    e "位置プロパティーはxposとyposに負の値を設定して画面より大きい画像のパンを振るのにも使えます。"

# game/tutorial_atl.rpy:729
translate japanese transform_properties_89e0d7c2:

    # "The subpixel property controls how things are lined up with the screen. When False, images can be pixel-perfect, but there can be pixel jumping."
    "subpixelプロパティーは画面上でどのように描画されるかを制御します。Falseなら、画像はピクセルパーフェクトですが、ピクセルジャンプもありえます。"

# game/tutorial_atl.rpy:736
translate japanese transform_properties_4194527e:

    # "When it's set to True, movement is smoother at the cost of blurring images a little."
    "Trueなら、移動はよりスムーズですが、画像にすこしブラーがかかります。"

# game/tutorial_atl.rpy:755
translate japanese transform_properties_35934e77:

    # e "Transforms also support polar coordinates. The around property sets the center of the coordinate system to coordinates given in pixels."
    e "Transformは極座標もサポートしています。aroundプロパティーは座標系の中心をピクセル単位で特定の座標に設定します。"

# game/tutorial_atl.rpy:763
translate japanese transform_properties_605ebd0c:

    # e "The angle property gives the angle in degrees. Angles run clockwise, with the zero angle at the top of the screen."
    e "angleプロパティーは度単位で角度を指定します。角度は時計回りで、0度が画面の一番上になります。"

# game/tutorial_atl.rpy:772
translate japanese transform_properties_6d4555ed:

    # e "The radius property gives the distance in pixels from the anchor of the displayable to the center of the coordinate system."
    e "radiusプロパティーは画像のアンカーから座標系の中心までのピクセルでの距離を指定します。"

# game/tutorial_atl.rpy:786
translate japanese transform_properties_7af037a5:

    # e "There are several ways to resize a displayable. The zoom property lets us scale a displayable by a factor, making it bigger and smaller."
    e "画像のサイズを変更するにはいくつか方法があります。zoomプロパティーは画像を倍数指定でスケールして拡大縮小します。"

# game/tutorial_atl.rpy:799
translate japanese transform_properties_b6527546:

    # e "The xzoom and yzoom properties allow the displayable to be scaled in the X and Y directions independently."
    e "xzoomとyzoomプロパティーを使うと、画像をX方向とY方向、それぞれにスケールできます。"

# game/tutorial_atl.rpy:809
translate japanese transform_properties_b98b780b:

    # e "By making xzoom or yzoom a negative number, we can flip the image horizontally or vertically."
    e "xzoomやyzoomを負の数にすると画像を水平または垂直方向に反転できます。"

# game/tutorial_atl.rpy:819
translate japanese transform_properties_74d542ff:

    # e "Instead of zooming by a scale factor, the size transform property can be used to scale a displayable to a size in pixels."
    e "倍数指定のzoomの代りに、size transformプロパティーを使用して画像をあるピクセルサイズまでスケールできます。"

# game/tutorial_atl.rpy:834
translate japanese transform_properties_438ed776:

    # e "The alpha property is used to change the opacity of a displayable. This can make it appear and disappear."
    e "alphaプロパティーを使うと画像の透明度を変更できます。これで画像の表示、非表示ができます。"

# game/tutorial_atl.rpy:847
translate japanese transform_properties_aee19f86:

    # e "The rotate property rotates a displayable."
    e "rotateプロパティーは画像を回転します。"

# game/tutorial_atl.rpy:858
translate japanese transform_properties_57b3235a:

    # e "By default, when a displayable is rotated, Ren'Py will include extra space on all four sides, so the size doesn't change as it rotates. Here, you can see the extra space on the left and top, and it's also there on the right and bottom."
    e "デフォルトでは、画像が回転されるとき、Ren'pyはすべての4辺の空白を含めるため、サイズは回転で変化しません。ここで左と上、右と下の空白の存在がみてとれます。"

# game/tutorial_atl.rpy:870
translate japanese transform_properties_66d29ee8:

    # e "By setting rotate_pad to False, we can get rid of the space, at the cost of the size of the displayable changing as it rotates."
    e "rotate_padをFalseに設定すると、画像のサイズは回転で変化しますが空間を除去できます。"

# game/tutorial_atl.rpy:881
translate japanese transform_properties_7f32e8ad:

    # e "The tile transform properties, xtile and ytile, repeat the displayable multiple times."
    e "tile transformプロパティーxtileとytileは画像を何回も繰替えします。"

# game/tutorial_atl.rpy:891
translate japanese transform_properties_207b7fc8:

    # e "The crop property crops a rectangle out of a displayable, showing only part of it."
    e "cropプロパティーは画像を長方形に切り抜いて、一部のみ表示します。"

# game/tutorial_atl.rpy:905
translate japanese transform_properties_e7e22d28:

    # e "When used together, crop and size can be used to focus in on specific parts of an image."
    e "同時に使用するとcropとsizeは画像の特定の部分にフォーカスをあてられます。"

# game/tutorial_atl.rpy:917
translate japanese transform_properties_f34abd82:

    # e "The xpan and ypan properties can be used to pan over a displayable, given an angle in degrees, with 0 being the center."
    e "xpanとypanプロパティーを使用すると画像をパンオーバーでき、度単位で角度を指定し、0度は中心です。"

# game/tutorial_atl.rpy:924
translate japanese transform_properties_bfa3b139:

    # e "Those are all the transform properties we have to work with. By putting them together in the right order, you can create complex things."
    e "これらはすべて使用する必要があるTransformプロパティーです。順番通りに配置して、複雑なものも作成できます。"

translate japanese strings:

    # game/tutorial_atl.rpy:267
    old "xpos 1.0 ypos .5"
    new "xpos 1.0 ypos .5"

    # game/tutorial_atl.rpy:267
    old "xpos .75 ypos .25"
    new "xpos .75 ypos .25"

    # game/tutorial_atl.rpy:267
    old "xpos .25 ypos .33"
    new "xpos .25 ypos .33"

