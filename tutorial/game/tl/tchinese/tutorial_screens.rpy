
# game/tutorial_screens.rpy:165
translate tchinese tutorial_screens_2faa22e5:

    # e "Screens are the most powerful part of Ren'Py. Screens let you customize the out-of-game interface, and create new in-game interface components."
    e "螢幕是 Ren'Py 最強大的部分。螢幕讓你自訂遊戲外介面，並建立新的遊戲內介面元件。"

# game/tutorial_screens.rpy:171
translate tchinese screens_menu_7f31d730:

    # e "What would you like to know about screens?" nointeract
    e "你想了解螢幕的哪一方面？" nointeract

# game/tutorial_screens.rpy:201
translate tchinese screens_demo_115a4b8f:

    # e "Screens are how we create the user interface in Ren'Py. With the exception of images and transitions, everything you see comes from a screen."
    e "螢幕是我們在 Ren'Py 中建立使用者介面的方式。除了圖片和轉場，你看到的一切都來自螢幕。"

# game/tutorial_screens.rpy:203
translate tchinese screens_demo_ce100e07:

    # e "When I'm speaking to you, I'm using the 'say' screen. It's responsible for taking dialogue and presenting it to the player."
    e "我和你說話時，使用的是「say」螢幕。它負責接收對話並呈現給玩家。"

# game/tutorial_screens.rpy:205
translate tchinese screens_demo_1bdfb4bd:

    # e "And when the menu statement displays an in-game choice, the 'choice' screen is used. Got it?" nointeract
    e "menu 語句顯示遊戲內選項時，會使用「choice」螢幕。明白嗎？" nointeract

# game/tutorial_screens.rpy:215
translate tchinese screens_demo_31a20e24:

    # e "Text input uses the 'input' screen, NVL mode uses the 'nvl' screen, and so on."
    e "文字輸入使用「input」螢幕，NVL 模式使用「nvl」螢幕，以此類推。"

# game/tutorial_screens.rpy:217
translate tchinese screens_demo_5a5aa2d5:

    # e "More than one screen can be displayed at once. For example, the buttons at the bottom - Back, History, Skip, and so on - are all displayed by a quick_menu screen that's shown all of the time."
    e "一次可以顯示多個螢幕。例如底部的「返回」、「歷史」、「跳過」等按鈕，都是由一直顯示的 quick_menu 螢幕呈現。"

# game/tutorial_screens.rpy:219
translate tchinese screens_demo_58d48fde:

    # e "There are a lot of special screens, like 'main_menu', 'load', 'save', and 'preferences'. Rather than list them all here, I'll {a=https://www.renpy.org/doc/html/screen_special.html}send you to the documentation{/a}."
    e "還有許多特殊螢幕，例如「main_menu」、「load」、「save」和「preferences」。與其在這裡全部列出，我推薦你參閱{a=https://www.renpy.org/doc/html/screen_special.html}文件{/a}。"

# game/tutorial_screens.rpy:221
translate tchinese screens_demo_27476d11:

    # e "In a newly created project, all these screens live in screens.rpy. You can edit that file in order to change them."
    e "新建立的專案會將這些螢幕全部放在 screens.rpy 中。你可以編輯該檔案來修改它們。"

# game/tutorial_screens.rpy:223
translate tchinese screens_demo_a699b1cb:

    # e "You aren't limited to these screens either. In Ren'Py, you can make your own screens, and use them for your game's interface."
    e "你也不受這些螢幕限制。在 Ren'Py 中，你可以製作自己的螢幕，作為遊戲介面使用。"

# game/tutorial_screens.rpy:230
translate tchinese screens_demo_a136e191:

    # e "For example, in an RPG like visual novel, a screen can display the player's statistics."
    e "例如在 RPG 類型的視覺小說中，螢幕可以顯示玩家的統計資料。"

# game/tutorial_screens.rpy:234
translate tchinese screens_demo_1f50f3d3:

    # e "Which reminds me, I should probably heal you."
    e "這提醒了我，應該幫你治療。"

# game/tutorial_screens.rpy:241
translate tchinese screens_demo_8a54de7a:

    # e "Complex screens can be the basis of whole game mechanics. A stats screen like this can be the basis of dating and life-sims."
    e "複雜的螢幕可以成為整套遊戲機制的基礎。像這樣的統計螢幕，就能作為戀愛或生活模擬遊戲的基礎。"

# game/tutorial_screens.rpy:246
translate tchinese screens_demo_62c184f8:

    # e "While screens might be complex, they're really just the result of a lot of simple parts working together to make something larger than all of them."
    e "螢幕雖然可能很複雜，但其實只是許多簡單部分協同運作，組合成比各部分更大的整體。"

# game/tutorial_screens.rpy:265
translate tchinese screens_showing_1b51e9a4:

    # e "Here's an example of a very simple screen. The screen statement is used to tell Ren'Py this is a screen, and it's name is simple_screen."
    e "以下是一個非常簡單的螢幕範例。screen 語句告訴 Ren'Py 這是一個螢幕，名稱是 simple_screen。"

# game/tutorial_screens.rpy:267
translate tchinese screens_showing_5a6bbad0:

    # e "Inside the screen statement, lines introduces displayables such as frame, vbox, text, and textbutton; or properties like action, xalign, and ypos."
    e "在 screen 語句中，各行會引入 frame、vbox、text、textbutton 等顯示物件，或 action、xalign、ypos 等屬性。"

# game/tutorial_screens.rpy:272
translate tchinese screens_showing_ae40755c:

    # e "I'll work from the inside out to describe the statements. But first, I'll show the screen so you can see it in action."
    e "我會由內到外介紹這些語句，但先顯示螢幕，讓你看看實際效果。"

# game/tutorial_screens.rpy:274
translate tchinese screens_showing_bc320819:

    # e "The text statement is used to display the text provided."
    e "text 語句用來顯示提供的文字。"

# game/tutorial_screens.rpy:276
translate tchinese screens_showing_64f23380:

    # e "The textbutton statement introduces a button that can be clicked. When the button is clicked, the provided action is run."
    e "textbutton 語句會建立可點擊的按鈕。點擊按鈕時，就會執行指定的動作。"

# game/tutorial_screens.rpy:278
translate tchinese screens_showing_e8f68c08:

    # e "Both are inside a vbox, which means vertical box, statement - that places the text on top of the button."
    e "兩者都放在 vbox（垂直方盒）語句中，因此文字會位於按鈕上方。"

# game/tutorial_screens.rpy:280
translate tchinese screens_showing_7e48fc22:

    # e "And that is inside a frame that provides the background and borders. The frame has an at property that takes a transform giving its position."
    e "以上內容都在提供背景和邊框的 frame 中。frame 有一個 at 屬性，接收用來指定位置的變換。"

# game/tutorial_screens.rpy:286
translate tchinese screens_showing_80425bf3:

    # e "There are a trio of statements that are used to display screens."
    e "有三種語句可以用來顯示螢幕。"

# game/tutorial_screens.rpy:291
translate tchinese screens_showing_7d2deb37:

    # e "The first is the show screen statement, which displays a screen and lets Ren'Py keep going."
    e "第一種是 show screen 語句，它會顯示螢幕並讓 Ren'Py 繼續執行。"

# game/tutorial_screens.rpy:293
translate tchinese screens_showing_7626dc8b:

    # e "The screen will stay shown until it is hidden."
    e "螢幕會持續顯示，直到被隱藏為止。"

# game/tutorial_screens.rpy:297
translate tchinese screens_showing_c79038a4:

    # e "Hiding a screen is done with the hide screen statement."
    e "隱藏螢幕要使用 hide screen 語句。"

# game/tutorial_screens.rpy:301
translate tchinese screens_showing_8f78a97d:

    # e "The call screen statement stops Ren'Py from executing script until the screen either returns a value, or jumps the script somewhere else."
    e "call screen 語句會讓 Ren'Py 暫停執行腳本，直到螢幕傳回值或將腳本跳轉到其他位置。"

# game/tutorial_screens.rpy:303
translate tchinese screens_showing_b52e420c:

    # e "Since we can't display dialogue at the same time, you'll have to click 'Okay' to continue."
    e "由於無法同時顯示對話，你必須點擊「確定」才能繼續。"

# game/tutorial_screens.rpy:310
translate tchinese screens_showing_c5ca730f:

    # e "When a call screen statement ends, the screen is automatically hidden."
    e "call screen 語句結束時，螢幕會自動隱藏。"

# game/tutorial_screens.rpy:312
translate tchinese screens_showing_a38d1702:

    # e "Generally, you use show screen to show overlays that are up all the time, and call screen to show screens the player interacts with for a little while."
    e "通常會使用 show screen 顯示一直開啟的覆蓋層，使用 call screen 顯示與玩家短暫互動的螢幕。"

# game/tutorial_screens.rpy:335
translate tchinese screens_parameters_0666043d:

    # e "Here's an example of a screen that takes three parameters. The message parameter is a message to show, while the okay and cancel actions are run when the appropriate button is chosen."
    e "以下是一個接收三個參數的螢幕範例。message 參數是要顯示的訊息，okay 和 cancel 動作會在點擊對應按鈕時執行。"

# game/tutorial_screens.rpy:337
translate tchinese screens_parameters_cf95b914:

    # e "While the message parameter always has to be supplied, the okay and cancel parameters have default values that are used if no argument is given."
    e "雖然一定要提供 message 參數，okay 和 cancel 參數都有預設值，未提供引數時就會使用預設值。"

# game/tutorial_screens.rpy:339
translate tchinese screens_parameters_4ce03111:

    # e "Each parameter is a variable that is defined inside the screen. Inside the screen, these variables take priority over those used in the rest of Ren'Py."
    e "每個參數都是在螢幕內定義的變數。在螢幕中，這些變數的優先權高於 Ren'Py 其他部分使用的變數。"

# game/tutorial_screens.rpy:343
translate tchinese screens_parameters_106c2a04:

    # e "When a screen is shown, arguments can be supplied for each of the parameters. Arguments can be given by position or by name."
    e "顯示螢幕時，可以為每個參數提供引數；引數可以依位置或名稱提供。"

# game/tutorial_screens.rpy:350
translate tchinese screens_parameters_12ac92d4:

    # e "Parameters let us change what a screen displays, simply by re-showing it with different arguments."
    e "參數讓我們只要改變引數並重新顯示，就能變更螢幕呈現的內容。"

# game/tutorial_screens.rpy:357
translate tchinese screens_parameters_d143a994:

    # e "The call screen statement can also take arguments, much like show screen does."
    e "call screen 語句也能接收參數，就像 show screen 一樣。"

# game/tutorial_screens.rpy:369
translate tchinese screens_properties_423246a2:

    # e "There are a few properties that can be applied to a screen itself."
    e "有幾個屬性可以套用於螢幕本身。"

# game/tutorial_screens.rpy:380
translate tchinese screens_properties_4fde164e:

    # e "When the modal property is true, you can't interact with things beneath the screen. You'll have to click 'Close This Screen' before you can continue."
    e "modal 屬性為 true 時，無法與螢幕下方的內容互動。你必須點擊「關閉此螢幕」才能繼續。"

# game/tutorial_screens.rpy:398
translate tchinese screens_properties_550c0bea:

    # e "When a screen has the tag property, it's treated like the tag part of an image name. Here, I'm showing a_tag_screen."
    e "螢幕有 tag 屬性時，會像圖片名稱的標籤部分一樣處理。這裡顯示的是 a_tag_screen 螢幕。"

# game/tutorial_screens.rpy:402
translate tchinese screens_properties_4fcf8af8:

    # e "When I show b_tag_screen, it replaces a_tag_screen."
    e "顯示 b_tag_screen 時，它會取代 a_tag_screen。"

# game/tutorial_screens.rpy:404
translate tchinese screens_properties_7ed5a791:

    # e "This is useful in the game and main menus, where you want the load screen to replace the preferences screen. By default, all those screens have tag menu."
    e "這在遊戲和主選單中很有用，例如用讀取螢幕取代偏好設定螢幕。預設情況下，這些螢幕都使用 menu 標籤。"

# game/tutorial_screens.rpy:408
translate tchinese screens_properties_5d51bd1e:

    # e "For some reason, tag takes a name, and not an expression. It's too late to change it."
    e "由於某些原因，tag 使用名稱而不是運算式；現在已經來不及改了。"

# game/tutorial_screens.rpy:432
translate tchinese screens_properties_6706e266:

    # e "The zorder property controls the order in which screens overlap each other. The larger the zorder number, the closer the screen is to the player."
    e "zorder 屬性控制螢幕彼此重疊的順序。zorder 數字越大，螢幕就越靠近玩家。"

# game/tutorial_screens.rpy:434
translate tchinese screens_properties_f7a2c73d:

    # e "By default, a screen has a zorder of 0. When two screens have the same zorder number, the screen that is shown second is closer to the player."
    e "螢幕的 zorder 預設為 0。兩個螢幕的 zorder 相同時，後顯示的螢幕會更靠近玩家。"

# game/tutorial_screens.rpy:454
translate tchinese screens_properties_78433eb8:

    # e "The variant property selects a screen based on the properties of the device it's running on."
    e "variant 屬性會根據執行裝置的特性選擇螢幕。"

# game/tutorial_screens.rpy:456
translate tchinese screens_properties_e6db6d02:

    # e "In this example, the first screen will be used for small devices like telephones, and the other screen will be used for tablets and computers."
    e "在這個例子中，第一個螢幕會用於手機等小型裝置，另一個則用於平板電腦和電腦。"

# game/tutorial_screens.rpy:475
translate tchinese screens_properties_d21b5500:

    # e "Finally, the style_prefix property specifies a prefix that's applied to the styles in the screen."
    e "最後，style_prefix 屬性指定套用於螢幕樣式的前綴。"

# game/tutorial_screens.rpy:477
translate tchinese screens_properties_560ca08a:

    # e "When the 'red' prefix is given, the frame gets the 'red_frame' style, and the text gets the 'red_text' style."
    e "指定「red」前綴時，frame 會使用「red_frame」樣式，文字則使用「red_text」樣式。"

# game/tutorial_screens.rpy:479
translate tchinese screens_properties_c7ad3a8e:

    # e "This can save a lot of typing when styling screens with many displayables in them."
    e "為包含許多顯示物件的螢幕設定樣式時，這能節省大量輸入。"

# game/tutorial_screens.rpy:491
translate tchinese screens_control_4a1d8d7c:

    # e "The screen language has a few statements that do things other than show displayables. If you haven't seen the section on {a=jump:warp_screen_displayables}Screen Displayables{/a} yet, you might want to check it out, then come back here."
    e "螢幕語言有些語句能做的不只是顯示顯示物件。如果你還沒看過{a=jump:warp_screen_displayables}螢幕顯示物件{/a}章節，可以先去看看再回來。"

# game/tutorial_screens.rpy:503
translate tchinese screens_control_0e939050:

    # e "The python statement works just about the same way it does in the script. A single line of Python is introduced with a dollar sign. This line is run each time the screen updates."
    e "python 語句的運作方式與腳本中大致相同。單行 Python 以美元符號開頭，每次螢幕更新時都會執行。"

# game/tutorial_screens.rpy:518
translate tchinese screens_control_6334650a:

    # e "Similarly, the python statement introduces an indented block of python statements. But there is one big difference in Python in screens and Python in scripts."
    e "同樣地，python 語句會引入縮排的多行 Python 區塊。但螢幕中的 Python 和腳本中的 Python 有一項重大差異。"

# game/tutorial_screens.rpy:520
translate tchinese screens_control_ba8f5f13:

    # e "The Python you use in screens isn't allowed to have side effects. That means that it can't do things like change the value of a variable."
    e "螢幕中使用的 Python 不允許有副作用，也就是不能變更變數的值。"

# game/tutorial_screens.rpy:522
translate tchinese screens_control_f75fa254:

    # e "The reason for this is that Ren'Py will run a screen, and the Python in it, during screen prediction."
    e "這是因為 Ren'Py 在螢幕預測期間會執行螢幕及其中的 Python。"

# game/tutorial_screens.rpy:536
translate tchinese screens_control_40c12afa:

    # e "The default statement lets you set the value of a screen variable the first time the screen runs. This value can be changed with the SetScreenVariable and ToggleScreenVariable actions."
    e "default 語句能在螢幕第一次執行時設定螢幕變數的值。可以使用 SetScreenVariable 和 ToggleScreenVariable 動作變更此值。"

# game/tutorial_screens.rpy:538
translate tchinese screens_control_39e0f7e6:

    # e "The default statement differs from the Python statement in that it is only run once. Python runs each time the screen updates, and hence the variable would never change value."
    e "default 語句只會執行一次，這點與 Python 語句不同。Python 每次螢幕更新都會執行，因此變數不會一直被重新設定。"

# game/tutorial_screens.rpy:557
translate tchinese screens_control_87a75fe7:

    # e "The if statement works like it does in script, running one block if the condition is true and another if the condition is false."
    e "if 語句的運作方式和腳本中類似：條件為 true 時執行一個區塊，條件為 false 時執行另一個。"

# game/tutorial_screens.rpy:572
translate tchinese screens_control_6a8c07f6:

    # e "The for statement takes a list of values, and iterates through them, running the block inside the for loop with the variable bound to each list item."
    e "for 語句接收值的串列並逐一走訪，在迴圈中執行區塊，讓變數依序綁定每個項目。"

# game/tutorial_screens.rpy:588
translate tchinese screens_control_f7b755fa:

    # e "The on and key statements probably only make sense at the top level of the screen."
    e "on 和 key 語句可能只有在螢幕頂層才有意義。"

# game/tutorial_screens.rpy:590
translate tchinese screens_control_328b0676:

    # e "The on statement makes the screen run an action when an event occurs. The 'show' event happens when the screen is first shown, and the 'hide' event happens when it is hidden."
    e "on 語句讓螢幕在事件發生時執行動作。「show」事件在螢幕首次顯示時發生，「hide」事件則在隱藏時發生。"

# game/tutorial_screens.rpy:592
translate tchinese screens_control_6768768b:

    # e "The key event runs an event when a key is pressed."
    e "key 事件會在按下按鍵時執行事件。"

# game/tutorial_screens.rpy:600
translate tchinese screen_use_c6a20a16:

    # e "The screen language use statement lets you include a screen inside another. This can be useful to prevent duplication inside screens."
    e "螢幕語言的 use 語句能在一個螢幕中包含另一個螢幕，有助於避免重複。"

# game/tutorial_screens.rpy:616
translate tchinese screen_use_95a34d3a:

    # e "Take for example this screen, which shows two stat entries. There's already a lot of duplication there, and if we had more stats, there would be more."
    e "以這個螢幕為例，它顯示兩個 stat 項目。這已經有不少重複，如果狀態更多，重複也會增加。"

# game/tutorial_screens.rpy:633
translate tchinese screen_use_e2c673d9:

    # e "Here, we moved the statements that show the text and bar into a second screen, and the use statement includes that screen in the first one."
    e "這裡把顯示文字和數值條的語句移到第二個螢幕，再用 use 語句將該螢幕加入第一個。"

# game/tutorial_screens.rpy:635
translate tchinese screen_use_2efdd2ff:

    # e "The name and amount of the stat are passed in as arguments to the screen, just as is done in the call screen statement."
    e "狀態的名稱和值會作為參數傳給螢幕，就像 call screen 語句一樣。"

# game/tutorial_screens.rpy:637
translate tchinese screen_use_f8d1bf9d:

    # e "By doing it this way, we control the amount of duplication, and can change the stat in one place."
    e "這樣就能控制重複數量，並在單一位置變更狀態。"

# game/tutorial_screens.rpy:653
translate tchinese screen_use_4e22c25e:

    # e "The transclude statement goes one step further, by letting the use statement take a block of screen language statements."
    e "transclude 語句更進一步，讓 use 語句取得螢幕語言的語句區塊。"

# game/tutorial_screens.rpy:655
translate tchinese screen_use_c83b97e3:

    # e "When the included screen reaches the transclude statement it is replaced with the block from the use statement."
    e "包含的螢幕執行到 transclude 語句時，會由 use 語句提供的區塊取代。"

# game/tutorial_screens.rpy:657
translate tchinese screen_use_1ad1f358:

    # e "The boilerplate screen is included in the first one, and the text from the first screen is transcluded into the boilerplate screen."
    e "boilerplate 螢幕會包含在第一個螢幕中，而第一個螢幕的文字會嵌入 boilerplate 螢幕。"

# game/tutorial_screens.rpy:659
translate tchinese screen_use_f74fab6e:

    # e "Use and transclude are complex, but very powerful. If you think about it, 'use boilerplate' is only one step removed from writing your own Screen Language statement."
    e "use 和 transclude 雖然複雜，卻非常強大。仔細想想，「使用樣板」只是省去撰寫自己螢幕語言語句的一步。"

translate tchinese strings:

    # game/tutorial_screens.rpy:26
    old " Lv. [lv]"
    new " Lv. [lv]"

    # game/tutorial_screens.rpy:29
    old "HP"
    new "HP"

    # game/tutorial_screens.rpy:58
    old "Morning"
    new "早上"

    # game/tutorial_screens.rpy:58
    old "Afternoon"
    new "下午"

    # game/tutorial_screens.rpy:58
    old "Evening"
    new "傍晚"

    # game/tutorial_screens.rpy:61
    old "Study"
    new "學習"

    # game/tutorial_screens.rpy:61
    old "Exercise"
    new "鍛鍊"

    # game/tutorial_screens.rpy:61
    old "Eat"
    new "吃"

    # game/tutorial_screens.rpy:61
    old "Drink"
    new "喝"

    # game/tutorial_screens.rpy:61
    old "Be Merry"
    new "開心"

    # game/tutorial_screens.rpy:107
    old "Strength"
    new "力量"

    # game/tutorial_screens.rpy:111
    old "Intelligence"
    new "智力"

    # game/tutorial_screens.rpy:115
    old "Moxie"
    new "勇氣"

    # game/tutorial_screens.rpy:119
    old "Chutzpah"
    new "狂妄"

    # game/tutorial_screens.rpy:171
    old "What screens can do."
    new "螢幕能做什麼。"

    # game/tutorial_screens.rpy:171
    old "How to show screens."
    new "如何顯示螢幕。"

    # game/tutorial_screens.rpy:171
    old "Passing parameters to screens."
    new "將參數傳給螢幕。"

    # game/tutorial_screens.rpy:171
    old "Screen properties."
    new "螢幕屬性。"

    # game/tutorial_screens.rpy:171
    old "Special screen statements."
    new "特殊螢幕語句。"

    # game/tutorial_screens.rpy:171
    old "Using other screens."
    new "使用其他螢幕。"

    # game/tutorial_screens.rpy:171
    old "That's it."
    new "就這些。"

    # game/tutorial_screens.rpy:205
    old "I do."
    new "我懂了。"

    # game/tutorial_screens.rpy:331
    old "Hello, world."
    new "Hello, world."

    # game/tutorial_screens.rpy:331
    old "You can't cancel this."
    new "你不能取消這個。"

    # game/tutorial_screens.rpy:346
    old "Shiro was here."
    new "西羅剛才在這裡。"

    # game/tutorial_screens.rpy:362
    old "Click either button to continue."
    new "點擊任一按鈕繼續。"

    # game/tutorial_screens.rpy:377
    old "Close This Screen"
    new "關閉此螢幕"

    # game/tutorial_screens.rpy:388
    old "A Tag Screen"
    new "A 標籤螢幕"

    # game/tutorial_screens.rpy:395
    old "B Tag Screen"
    new "B 標籤螢幕"

    # game/tutorial_screens.rpy:447
    old "You're on a small device."
    new "你正在使用小型裝置。"

    # game/tutorial_screens.rpy:452
    old "You're not on a small device."
    new "你沒有使用小型裝置。"

    # game/tutorial_screens.rpy:466
    old "This text is red."
    new "這段文字是紅色的。"

    # game/tutorial_screens.rpy:496
    old "Hello, World."
    new "Hello, World."

    # game/tutorial_screens.rpy:510
    old "It's good to meet you."
    new "很高興認識你。"

    # game/tutorial_screens.rpy:534
    old "Increase"
    new "增加"

    # game/tutorial_screens.rpy:563
    old "Earth"
    new "地球"

    # game/tutorial_screens.rpy:563
    old "Moon"
    new "月球"

    # game/tutorial_screens.rpy:563
    old "Mars"
    new "火星"

    # game/tutorial_screens.rpy:581
    old "Now press 'a'."
    new "現在按下「A」。"

    # game/tutorial_screens.rpy:583
    old "The screen was just shown."
    new "螢幕剛才顯示了。"

    # game/tutorial_screens.rpy:585
    old "You pressed the 'a' key."
    new "你按了「A」鍵。"

    # game/tutorial_screens.rpy:608
    old "Health"
    new "體力"

    # game/tutorial_screens.rpy:613
    old "Magic"
    new "魔力"

    # game/tutorial_screens.rpy:644
    old "There's not much left to see."
    new "沒什麼好看的了。"
