
# game/tutorial_screens.rpy:165
translate japanese tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e "スクリーンはRen'Pyで最も強力な部分です。スクリーンでは(訳注メインメニューやゲームメニューのような)ゲーム外のインターフェースをカスタマイズしたり、ゲーム内の新しいインターフェース構成を作成できます。"

# game/tutorial_screens.rpy:171
translate japanese screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "スクリーンについて何が知りたいですか？" nointeract

# game/tutorial_screens.rpy:201
translate japanese screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e "スクリーンはRen'Pyでユーザーインターフェースを作成する手段です。画像やトランジションを除き、見えるものは全てスクリーンで出来ています。"

# game/tutorial_screens.rpy:203
translate japanese screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e "私があなたと話しているとき、私は'say'スクリーンを使用しています。これは台詞をプレイヤーに表示する役割を担います。"

# game/tutorial_screens.rpy:205
translate japanese screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "また、menuステートメントがゲーム内の選択肢を表示しているときは'choice'スクリーンが使用されています。わかりましたか？" nointeract

# game/tutorial_screens.rpy:215
translate japanese screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e "他にも、テキストの入力には'input'スクリーンを使用し、NVLモードには'nvl'スクリーンを使用する、などがあります。"

# game/tutorial_screens.rpy:217
translate japanese screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e "１つ以上のスクリーンを一度に表示できます。例えば、下部にあるロールバック、ヒストリー、スキップなどのボタンはquick_menuスクリーンにより描画され、常に表示されています。"

# game/tutorial_screens.rpy:219
translate japanese screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e "'main_menu'や'load'、'save'、'preferences'のような特殊なスクリーンも数多くあります。ここで全て取り上げることはせず、{a=https://ja.renpy.org/doc/html/screen_special.html}ドキュメント{/a}を紹介いたします。"

# game/tutorial_screens.rpy:221
translate japanese screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e "新しく作成されたプロジェクトでは、これらのスクリーンは全てscreens.rpyに含まれています。あなたはこれらを変更するためにファイルを編集できます。"

# game/tutorial_screens.rpy:223
translate japanese screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e "これらのスクリーンに限らず、Ren'Pyではあなた自身のスクリーンを作成し、ゲームのインターフェースに使用できます。"

# game/tutorial_screens.rpy:230
translate japanese screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e "例えば、RPGのようなビジュアルノベルの中で、スクリーンはプレイヤーのステータスを表示できます。"

# game/tutorial_screens.rpy:234
translate japanese screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e "あら、あなたを回復しないといけませんね。"

# game/tutorial_screens.rpy:241
translate japanese screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e "複雑なスクリーンはゲーム全体のメカニクスの基礎となります。こちらのようなステータススクリーンは日付や体力シミュレーションの基本であります。"

# game/tutorial_screens.rpy:246
translate japanese screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e "スクリーンが複雑そうに見えたとしても、それはたくさんのシンプルなパーツが組み合わさった結果に大きくなったに過ぎません。"

# game/tutorial_screens.rpy:265
translate japanese screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."
    e "こちらは非常にシンプルなスクリーンの一例です。screenステートメントは、これがスクリーンであることとsimple_screenという名前であることをRen'Pyに示すために用いられます。"

# game/tutorial_screens.rpy:267
translate japanese screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e "screenステートメント内にはframe、vbox、text、textbuttonといったdisplayablesやaction、xalign、yposのようなプロパティを導入する行があります。"

# game/tutorial_screens.rpy:272
translate japanese screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e "これからこのステートメントを徹底的に説明していきます。ですがまず、実際にご覧いただけるようにスクリーンをお見せします"

# game/tutorial_screens.rpy:274
translate japanese screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e "textステートメントは与えられたテキストを表示するために用いられます。"

# game/tutorial_screens.rpy:276
translate japanese screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e "textbuttonステートメントはクリック可能なボタンを表示します。ボタンがクリックされると与えられたアクションが起こります。"

# game/tutorial_screens.rpy:278
translate japanese screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e "いずれもvbox、即ちテキストを上から下に並べる垂直なボックスに含まれています。"

# game/tutorial_screens.rpy:280
translate japanese screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e "また、これは背景や境界線を指定されたフレームの中にあります。このフレームは位置を与えるTransformを行うatプロパティを持ちます。"

# game/tutorial_screens.rpy:286
translate japanese screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e "スクリーンを表示するには３種類のステートメントを使用します。"

# game/tutorial_screens.rpy:291
translate japanese screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e "１つ目はshow screenステートメントで、これはスクリーンを表示したままRen'Pyを継続させます。"

# game/tutorial_screens.rpy:293
translate japanese screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e "このスクリーンは非表示にするまで表示され続けます。"

# game/tutorial_screens.rpy:297
translate japanese screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e "hide screenステートメントを使用するとスクリーンを非表示にできます。"

# game/tutorial_screens.rpy:301
translate japanese screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e "call screenステートメントは、スクリーンがいずれかの値を返すか、どこかへジャンプするまでRen'Pyスクリプトの実行を停止します。"

# game/tutorial_screens.rpy:303
translate japanese screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e "ダイアログを同時に表示することができないので、続けるには「了解」を押してください。"

# game/tutorial_screens.rpy:310
translate japanese screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e "call screenステートメントが終了すると、そのスクリーンは自動的に非表示になります。"

# game/tutorial_screens.rpy:312
translate japanese screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e "一般に、常に見せたいものを表示する際にはshow screenを使用し、プレイヤーにちょっとした操作を求める際にはcall screenを使用します。"

# game/tutorial_screens.rpy:335
translate japanese screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e "こちらは３つのパラメータを取るスクリーンの例です。messageパラメータは表示するメッセージで、okayとcancelのアクションはそれぞれのボタンが選択されたときに発生します。"

# game/tutorial_screens.rpy:337
translate japanese screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e "messageパラメータは常に与えられなければいけませんが、okayやcancelのパラメータはデフォルト値を持っているので引数が与えられなければそれらを用います。"

# game/tutorial_screens.rpy:339
translate japanese screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e "それぞれのパラメータはスクリーン内で定義される変数です。スクリーン内ではこれらの変数はRen'Pyの他の場所で用いられる変数より優先されます。"

# game/tutorial_screens.rpy:343
translate japanese screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e "スクリーンが表示されているとき、各パラメータに対し引数を与えることができます。引数は順番または名前によって与えられます。"

# game/tutorial_screens.rpy:350
translate japanese screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e "パラメータによってスクリーンの表示を変更できます。異なる引数を与えて再度表示するだけです。"

# game/tutorial_screens.rpy:357
translate japanese screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e "call screenステートメントも、show screenと同様に引数を取ります。"

# game/tutorial_screens.rpy:369
translate japanese screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e "スクリーン自身にもいくつか適用されるプロパティがあります。"

# game/tutorial_screens.rpy:380
translate japanese screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e "modalプロパティがtrueのとき、このスクリーンの下にあるものには触れることができません。続けるには「このスクリーンを閉じる」をクリックしてください。"

# game/tutorial_screens.rpy:398
translate japanese screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e "スクリーンがtagプロパティを持っていると、画像名のタグの部分のように扱われます。今、私はa_tag_screenを表示しています。"

# game/tutorial_screens.rpy:402
translate japanese screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e "私がb_tag_screenを表示すると、a_tag_screenと置き換わります。"

# game/tutorial_screens.rpy:404
translate japanese screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e "これはゲームメニューやメインメニューで、ロード画面を環境設定画面に置き換えたい場面などに便利です。デフォルトでは、これらのようなスクリーンはmenuタグを持っています。"

# game/tutorial_screens.rpy:408
translate japanese screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e "いくつかの理由で、tagは名前を取りますが式は取りません。この仕様を変更するには既に手遅れでして。"

# game/tutorial_screens.rpy:432
translate japanese screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e "zorderプロパティは互いに重なるスクリーンの順序を制御します。zorderの数字が大きいほどプレイヤーに近いスクリーンとなります。"

# game/tutorial_screens.rpy:434
translate japanese screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e "デフォルトでは、各スクリーンのzorderは0となっています。２つのスクリーンが同じzorderの数字を持つ場合、２つ目に表示されるスクリーンがプレイヤー側に表示されます。"

# game/tutorial_screens.rpy:454
translate japanese screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e "variantプロパティは起動しているデバイスに基づいて選択されます。"

# game/tutorial_screens.rpy:456
translate japanese screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e "この例では、１つ目のスクリーンは携帯電話のような小さいデバイス用、他のスクリーンはタブレットやパソコン用です。"

# game/tutorial_screens.rpy:475
translate japanese screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e "最後に、style_prefixプロパティはスクリーン内で適用するスタイルの接頭辞を指定します。"

# game/tutorial_screens.rpy:477
translate japanese screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e "'red'という接頭辞が与えられると、フレームは'red_frame'スタイルを取り、テキストは'red_text'スタイルを取ります。"

# game/tutorial_screens.rpy:479
translate japanese screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e "これで、多くのdisplayableを含むスクリーンのスタイルを指定するときも、入力の手間を省けます。"

# game/tutorial_screens.rpy:491
translate japanese screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e "スクリーン言語はdisplayableを表示する以外に２、３のステートメントを持ちます。もし{a=jump:warp_screen_displayables}スクリーンDisplayables{/a}のセクションを見ていないのでしたら、ご覧になってから戻ってきてください。"

# game/tutorial_screens.rpy:503
translate japanese screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e "pythonステートメントはスクリプト内と同様の働きをします。一行Pythonはドル印によって記述されます。この行はスクリーンが更新されるたびに実行されます。"

# game/tutorial_screens.rpy:518
translate japanese screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e "同様に、pythonステートメントはインデントされたpythonステートメントのブロックによって記述されます。ですが、スクリーン内のPythonとスクリプト内のPythonには１つ大きな違いがあります。"

# game/tutorial_screens.rpy:520
translate japanese screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e "スクリーン内で用いられるPythonは副作用を持ってはいけません。つまり、変数の値を変更するようなことはできません。"

# game/tutorial_screens.rpy:522
translate japanese screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e "これは、Ren'Pyがスクリーンを予測している間にスクリーンとその中のPythonを実行してしまうためです。"

# game/tutorial_screens.rpy:536
translate japanese screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e "defaultステートメントは、スクリーンが初めて実行されたときにスクリーンの変数に値を与えます。この値はSetScreenVariableやToggleScreenVariableといったアクションで変更できます。"

# game/tutorial_screens.rpy:538
translate japanese screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e "defaultステートメントはPythonステートメントと違って１度だけ実行されます。Pythonだとスクリーンが更新されるたびに実行されてしまうので、変数の値を変更することができません。"

# game/tutorial_screens.rpy:557
translate japanese screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e "ifステートメントはスクリプトと同様に働き、１つのブロックは状態がtrueのときに、もう１つのブロックは状態がfalseのときに実行されます。"

# game/tutorial_screens.rpy:572
translate japanese screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e "forステートメントは値のリストを取得し、リストの各要素からの変数でforループ内のブロックを実行してそれらを繰り返し処理します。"

# game/tutorial_screens.rpy:588
translate japanese screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e "onやkeyステートメントは恐らくスクリーンの最上位でのみ意味を成します。"

# game/tutorial_screens.rpy:590
translate japanese screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e "onステートメントは、いずれかのイベントが発生したときにスクリーンにアクションを起こします。'show'イベントはスクリーンが最初に表示されたときに発生し、'hide'イベントはスクリーンが非表示にされるときに発生します。"

# game/tutorial_screens.rpy:592
translate japanese screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e "keyイベントはキーが押されたときに実行されます。"

# game/tutorial_screens.rpy:600
translate japanese screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e "スクリーン言語のuseステートメントを使用すると、スクリーンを別のスクリーンに含めることができます。 これは、スクリーン内でのダブりを避けるのに役立ちます。"

# game/tutorial_screens.rpy:616
translate japanese screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e "例えば、このスクリーンは２つのステータスを表示しています。すでに多くのダブりが含まれていて、更にステータスが増えるとダブりも更に増えてしまいます。"

# game/tutorial_screens.rpy:633
translate japanese screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e "今、ステートメントを変更しました。２つ目のスクリーンでテキストとバーを表示し、このステートメントを含むuseステートメントを最初のスクリーンに入れました。"

# game/tutorial_screens.rpy:635
translate japanese screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e "ステータスの名前と値は、call screenステートメントが実行されるのと同じように、引数として渡されます。"

# game/tutorial_screens.rpy:637
translate japanese screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e "この方法を行うことで、いくつもの複製を制御しつつ、一か所でステータスを変更できます。"

# game/tutorial_screens.rpy:653
translate japanese screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e "transcludeステートメントは、スクリーン言語ステートメントのブロックをuseステートメントに取得させることにより、さらに一歩先を行きます。"

# game/tutorial_screens.rpy:655
translate japanese screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e "組み込まれたスクリーンのtranscludeステートメントはそのuseステートメントに与えられたブロックで置き換えられます。"

# game/tutorial_screens.rpy:657
translate japanese screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e "boilerplateスクリーンは１つ目のスクリーンに含まれていて、1つ目のスクリーンにあるテキストはboilerplateスクリーンに挿入されます。"

# game/tutorial_screens.rpy:659
translate japanese screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e "useやtranscludeは複雑ですが、非常に強力です。'use boilerplate'は単にスクリーン言語ステートメントを記述する際に、１つだけですが手順を減らすことができると考えるとよいです。"

translate japanese strings:

    # game/tutorial_screens.rpy:26
    old " Lv. [lv]"
    new " Lv. [lv]"

    # game/tutorial_screens.rpy:29
    old "HP"
    new "HP"

    # game/tutorial_screens.rpy:58
    old "Morning"
    new "朝"

    # game/tutorial_screens.rpy:58
    old "Afternoon"
    new "昼下がり"

    # game/tutorial_screens.rpy:58
    old "Evening"
    new "夕暮れ"

    # game/tutorial_screens.rpy:61
    old "Study"
    new "勉強"

    # game/tutorial_screens.rpy:61
    old "Exercise"
    new "運動"

    # game/tutorial_screens.rpy:61
    old "Eat"
    new "食事"

    # game/tutorial_screens.rpy:61
    old "Drink"
    new "飲料"

    # game/tutorial_screens.rpy:61
    old "Be Merry"
    new ""

    # game/tutorial_screens.rpy:107
    old "Strength"
    new "強さ"

    # game/tutorial_screens.rpy:111
    old "Intelligence"
    new "賢さ"

    # game/tutorial_screens.rpy:115
    old "Moxie"
    new "根性"

    # game/tutorial_screens.rpy:119
    old "Chutzpah"
    new "大胆さ"

    # game/tutorial_screens.rpy:171
    old "What screens can do."
    new "スクリーンにできること"

    # game/tutorial_screens.rpy:171
    old "How to show screens."
    new "スクリーンを表示する方法"

    # game/tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new "スクリーンにパラメータを渡す"

    # game/tutorial_screens.rpy:171
    old "Screen properties."
    new "スクリーンプロパティ"

    # game/tutorial_screens.rpy:171
    old "Special screen statements."
    new "特別なscreenステートメント"

    # game/tutorial_screens.rpy:171
    old "Using other screens."
    new "他のスクリーンを使用する"

    # game/tutorial_screens.rpy:171
    old "That's it."
    new "もう結構です"

    # game/tutorial_screens.rpy:205
    old "I do."
    new "やります" #TODO

    # game/tutorial_screens.rpy:331
    old "Hello, world."
    new "Hello, world."

    # game/tutorial_screens.rpy:331
    old "You can't cancel this."
    new "これはキャンセルできません。"

    # game/tutorial_screens.rpy:346
    old "Shiro was here."
    new "シロはここです。"

    # game/tutorial_screens.rpy:362
    old "Click either button to continue."
    new "続けるにはいずれかのボタンを押してください。"

    # game/tutorial_screens.rpy:377
    old "Close This Screen"
    new "このスクリーンを閉じる"

    # game/tutorial_screens.rpy:388
    old "A Tag Screen"
    new "Aタグスクリーン"

    # game/tutorial_screens.rpy:395
    old "B Tag Screen"
    new "Bタグスクリーン"

    # game/tutorial_screens.rpy:447
    old "You're on a small device."
    new "あなたは小さなデバイスです。"

    # game/tutorial_screens.rpy:452
    old "You're not on a small device."
    new "あなたは小さなデバイスではありません。"

    # game/tutorial_screens.rpy:466
    old "This text is red."
    new "このテキストは赤色です。"

    # game/tutorial_screens.rpy:496
    old "Hello, World."
    new "Hello, World"

    # game/tutorial_screens.rpy:510
    old "It's good to meet you."
    new "お会いできて嬉しいです。"

    # game/tutorial_screens.rpy:534
    old "Increase"
    new "増加"

    # game/tutorial_screens.rpy:563
    old "Earth"
    new "地球"

    # game/tutorial_screens.rpy:563
    old "Moon"
    new "月"

    # game/tutorial_screens.rpy:563
    old "Mars"
    new "火星"

    # game/tutorial_screens.rpy:581
    old "Now press 'a'."
    new "今「a」キーを押してください。"

    # game/tutorial_screens.rpy:583
    old "The screen was just shown."
    new "スクリーンが表示されているだけです。"

    # game/tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new "あなたは「a」キーを押しました。"

    # game/tutorial_screens.rpy:608
    old "Health"
    new "健康"

    # game/tutorial_screens.rpy:613
    old "Magic"
    new "魔法"

    # game/tutorial_screens.rpy:644
    old "There's not much left to see."
    new "あと少しです。"

