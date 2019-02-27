
translate simplified_chinese strings:

    # screens.rpy:9
    old "## Styles"
    new "## 样式"

    # screens.rpy:81
    old "## In-game screens"
    new "## 游戏内屏幕"

    # screens.rpy:85
    old "## Say screen"
    new "## Say 屏幕"

    # screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Say 屏幕用于向玩家显示对话。它需要两个参数，“who”和“what”，分别是叙述人的名称和所叙述的内容。（如果没有名称，参数“who”可以是“None”。）"

    # screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## 此屏幕必须创建一个 id 为“what”的文本可视控件，因为 Ren'Py 使用它来管理文本显示。它还可以创建 id 为“who”和 id 为“window”的可视控件来应用样式属性。"

    # screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## 如果有侧边图像，会将其显示在文本之上。请不要在手机界面下显示这个，因为没有空间。"

    # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## 通过 Character 对象使名称框可用于样式化。"

    # screens.rpy:164
    old "## Input screen"
    new "## 输入屏幕"

    # screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## 此屏幕用于显示 renpy.input。“prompt”参数用于传递文本提示。"

    # screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## 此屏幕必须创建一个 id 为“input”的输入可视控件来接受各种输入参数。"

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:199
    old "## Choice screen"
    new "## 选择屏幕"

    # screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## 此屏幕用于显示由“menu”语句生成的游戏内选项。参数“items”是一个对象列表，每个对象都有标题和操作字段。"

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## 若为True，菜单内的叙述会使用旁白 (narrator) 角色。否则，叙述会显示为菜单内的文字说明。"

    # screens.rpy:238
    old "## Quick Menu screen"
    new "## 快捷菜单屏幕"

    # screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## 快捷菜单显示于游戏内，以便于访问游戏外的菜单。"

    # screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new "## 确保该菜单出现在其他屏幕之上，"

    # screens.rpy:256
    old "Back"
    new "回退"

    # screens.rpy:257
    old "History"
    new "历史"

    # screens.rpy:258
    old "Skip"
    new "快进"

    # screens.rpy:259
    old "Auto"
    new "自动"

    # screens.rpy:260
    old "Save"
    new "保存"

    # screens.rpy:261
    old "Q.Save"
    new "快存"

    # screens.rpy:262
    old "Q.Load"
    new "快读"

    # screens.rpy:263
    old "Prefs"
    new "设置"

    # screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 此代码确保只要玩家没有明确隐藏界面，就会在游戏中显示“quick_menu”屏幕。"

    # screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## 标题和游戏菜单屏幕"

    # screens.rpy:287
    old "## Navigation screen"
    new "## 导航屏幕"

    # screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## 该屏幕包含在标题菜单和游戏菜单中，并提供导航到其他菜单，以及启动游戏。"

    # screens.rpy:304
    old "Start"
    new "开始游戏"

    # screens.rpy:312
    old "Load"
    new "读取游戏"

    # screens.rpy:314
    old "Preferences"
    new "设置"

    # screens.rpy:318
    old "End Replay"
    new "结束回放"

    # screens.rpy:322
    old "Main Menu"
    new "标题界面"

    # screens.rpy:324
    old "About"
    new "关于"

    # screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new "## “帮助”对移动设备来说并非必须或相关。"

    # screens.rpy:329
    old "Help"
    new "帮助"

    # screens.rpy:331
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## “退出”按钮在 iOS 上被禁止使用，在安卓上也不是必需的。"

    # screens.rpy:332
    old "Quit"
    new "退出"

    # screens.rpy:346
    old "## Main Menu screen"
    new "## 标题菜单屏幕"

    # screens.rpy:348
    old "## Used to display the main menu when Ren'Py starts."
    new "## 用于在 Ren'Py 启动时显示标题菜单。"

    # screens.rpy:350
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:354
    old "## This ensures that any other menu screen is replaced."
    new "## 此代码可确保替换掉任何其他菜单屏幕。"

    # screens.rpy:361
    old "## This empty frame darkens the main menu."
    new "## 此空框可使标题菜单变暗。"

    # screens.rpy:365
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## “use”语句将其他的屏幕包含进此屏幕。标题屏幕的实际内容在导航屏幕中。"

    # screens.rpy:408
    old "## Game Menu screen"
    new "## 游戏菜单屏幕"

    # screens.rpy:410
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## 此屏幕列出了游戏菜单的基本共同结构。此屏幕需使用屏幕标题（title）调用，并显示背景、标题和导航菜单。"

    # screens.rpy:413
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". When this screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## “scroll”参数可以是“None”，也可以是“viewport”或“vpgrid”。当此屏幕与一个或多个子菜单同时使用时，这些子菜单将被转移（放置）在其中。"

    # screens.rpy:431
    old "## Reserve space for the navigation section."
    new "## 导航部分的预留空间。"

    # screens.rpy:473
    old "Return"
    new "返回"

    # screens.rpy:536
    old "## About screen"
    new "## 关于屏幕"

    # screens.rpy:538
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## 此屏幕提供有关游戏和 Ren'Py 的制作人员和版权信息。"

    # screens.rpy:541
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## 这个屏幕没有什么特别之处，因此它也是如何制作自定义屏幕的一个例子。"

    # screens.rpy:548
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 此“use”语句将包含“game_menu”屏幕到此处。子级“vbox”将包含在“game_menu”屏幕的“viewport”内。"

    # screens.rpy:558
    old "Version [config.version!t]\n"
    new "版本 [config.version!t]\n"

    # screens.rpy:560
    old "## gui.about is usually set in options.rpy."
    new "## “gui.about”通常在 options.rpy 中设置。"

    # screens.rpy:564
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "基于 {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # screens.rpy:567
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## 此变量在 options.rpy 中重新定义，来添加文本到关于屏幕。"

    # screens.rpy:579
    old "## Load and Save screens"
    new "## 读取和保存屏幕"

    # screens.rpy:581
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 这些屏幕负责允许玩家保存游戏并将其重新读取。由于它们几乎完全一样，因此它们都是以第三方屏幕“file_slots”来实现的。"

    # screens.rpy:585
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:604
    old "Page {}"
    new "第 {} 页"

    # screens.rpy:604
    old "Automatic saves"
    new "自动存档"

    # screens.rpy:604
    old "Quick saves"
    new "快速存档"

    # screens.rpy:610
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## 此代码确保输入控件在任意按钮执行前可以获取“enter”事件。"

    # screens.rpy:614
    old "## The page name, which can be edited by clicking on a button."
    new "## 页面名称，可以通过单击按钮进行编辑。"

    # screens.rpy:626
    old "## The grid of file slots."
    new "## 存档位网格。"

    # screens.rpy:646
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%Y-%m-%d %H:%M"

    # screens.rpy:646
    old "empty slot"
    new "空存档位"

    # screens.rpy:654
    old "## Buttons to access other pages."
    new "## 用于访问其他页面的按钮。"

    # screens.rpy:663
    old "<"
    new "<"

    # screens.rpy:666
    old "{#auto_page}A"
    new "{#auto_page}A"

    # screens.rpy:669
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # screens.rpy:671
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## “range(1, 10)”给出1到9之间的数字。"

    # screens.rpy:675
    old ">"
    new ">"

    # screens.rpy:710
    old "## Preferences screen"
    new "## 设置屏幕"

    # screens.rpy:712
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## 设置屏幕允许玩家配置游戏以更好地适应自己。"

    # screens.rpy:715
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:732
    old "Display"
    new "显示"

    # screens.rpy:733
    old "Window"
    new "窗口"

    # screens.rpy:734
    old "Fullscreen"
    new "全屏"

    # screens.rpy:738
    old "Rollback Side"
    new "回退控制区"

    # screens.rpy:739
    old "Disable"
    new "禁用"

    # screens.rpy:740
    old "Left"
    new "左侧"

    # screens.rpy:741
    old "Right"
    new "右侧"

    # screens.rpy:746
    old "Unseen Text"
    new "未读文本"

    # screens.rpy:747
    old "After Choices"
    new "选项后继续"

    # screens.rpy:748
    old "Transitions"
    new "忽略转场"

    # screens.rpy:750
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## 可以在此处添加类型为“radio_pref”或“check_pref”的其他“vbox”，以添加其他创建者定义的首选项设置。"

    # screens.rpy:761
    old "Text Speed"
    new "文字速度"

    # screens.rpy:765
    old "Auto-Forward Time"
    new "自动前进时间"

    # screens.rpy:772
    old "Music Volume"
    new "音乐音量"

    # screens.rpy:779
    old "Sound Volume"
    new "音效音量"

    # screens.rpy:785
    old "Test"
    new "测试"

    # screens.rpy:789
    old "Voice Volume"
    new "语音音量"

    # screens.rpy:800
    old "Mute All"
    new "全部静音"

    # screens.rpy:876
    old "## History screen"
    new "## 历史屏幕"

    # screens.rpy:878
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## 这是一个向玩家显示对话历史的屏幕。虽然此屏幕没有任何特殊之处，但它必须访问储存在“_history_list”中的对话历史记录。"

    # screens.rpy:882
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:888
    old "## Avoid predicting this screen, as it can be very large."
    new "## 避免预缓存此屏幕，因为它可能非常大。"

    # screens.rpy:899
    old "## This lays things out properly if history_height is None."
    new "## 此代码可确保如果“history_height”为“None”的话仍可正常显示条目。"

    # screens.rpy:909
    old "## Take the color of the who text from the Character, if set."
    new "## 若角色颜色已设置，则从“Character”对象中读取颜色到叙述人文本中。"

    # screens.rpy:918
    old "The dialogue history is empty."
    new "对话历史记录为空。"

    # screens.rpy:921
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## 此代码决定了允许在历史记录屏幕上显示哪些标签。"

    # screens.rpy:968
    old "## Help screen"
    new "## 帮助屏幕"

    # screens.rpy:970
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## 提供有关键盘和鼠标映射信息的屏幕。它使用其它屏幕（“keyboard_help”，“mouse_help“和”gamepad_help“）来显示实际的帮助内容。"

    # screens.rpy:989
    old "Keyboard"
    new "键盘"

    # screens.rpy:990
    old "Mouse"
    new "鼠标"

    # screens.rpy:993
    old "Gamepad"
    new "手柄"

    # screens.rpy:1006
    old "Enter"
    new "回车"

    # screens.rpy:1007
    old "Advances dialogue and activates the interface."
    new "推进对话并激活界面。"

    # screens.rpy:1010
    old "Space"
    new "空格"

    # screens.rpy:1011
    old "Advances dialogue without selecting choices."
    new "推进对话但不选择选项。"

    # screens.rpy:1014
    old "Arrow Keys"
    new "方向键"

    # screens.rpy:1015
    old "Navigate the interface."
    new "导航界面。"

    # screens.rpy:1018
    old "Escape"
    new "Esc"

    # screens.rpy:1019
    old "Accesses the game menu."
    new "访问游戏菜单。"

    # screens.rpy:1022
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1023
    old "Skips dialogue while held down."
    new "按住时快进对话。"

    # screens.rpy:1026
    old "Tab"
    new "Tab"

    # screens.rpy:1027
    old "Toggles dialogue skipping."
    new "切换对话快进。"

    # screens.rpy:1030
    old "Page Up"
    new "Page Up"

    # screens.rpy:1031
    old "Rolls back to earlier dialogue."
    new "回退至先前的对话。"

    # screens.rpy:1034
    old "Page Down"
    new "Page Down"

    # screens.rpy:1035
    old "Rolls forward to later dialogue."
    new "向前至之后的对话。"

    # screens.rpy:1039
    old "Hides the user interface."
    new "隐藏用户界面。"

    # screens.rpy:1043
    old "Takes a screenshot."
    new "截图。"

    # screens.rpy:1047
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "切换辅助{a=https://www.renpy.org/l/voicing}自动朗读{/a}。"

    # screens.rpy:1053
    old "Left Click"
    new "左键点击"

    # screens.rpy:1057
    old "Middle Click"
    new "中键点击"

    # screens.rpy:1061
    old "Right Click"
    new "右键点击"

    # screens.rpy:1065
    old "Mouse Wheel Up\nClick Rollback Side"
    new "鼠标滚轮上\n点击回退控制区"

    # screens.rpy:1069
    old "Mouse Wheel Down"
    new "鼠标滚轮下"

    # screens.rpy:1076
    old "Right Trigger\nA/Bottom Button"
    new "右扳机键\nA/底键"

    # screens.rpy:1080
    old "Left Trigger\nLeft Shoulder"
    new "左扳机键\n左肩键"

    # screens.rpy:1084
    old "Right Shoulder"
    new "右肩键"

    # screens.rpy:1089
    old "D-Pad, Sticks"
    new "十字键，摇杆"

    # screens.rpy:1093
    old "Start, Guide"
    new "开始，向导"

    # screens.rpy:1097
    old "Y/Top Button"
    new "Y/顶键"

    # screens.rpy:1100
    old "Calibrate"
    new "校准"

    # screens.rpy:1128
    old "## Additional screens"
    new "## 其他屏幕"

    # screens.rpy:1132
    old "## Confirm screen"
    new "## 确认屏幕"

    # screens.rpy:1134
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## 当 Ren'Py 需要询问玩家是非问题时，会调用确认屏幕。"

    # screens.rpy:1137
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1141
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 显示此屏幕时，确保其他屏幕无法输入。"

    # screens.rpy:1165
    old "Yes"
    new "确定"

    # screens.rpy:1166
    old "No"
    new "取消"

    # screens.rpy:1168
    old "## Right-click and escape answer \"no\"."
    new "## 右键点击退出并答复“no”（取消）。"

    # screens.rpy:1195
    old "## Skip indicator screen"
    new "## 快进指示屏幕"

    # screens.rpy:1197
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## “skip_indicator”屏幕用于指示快进正在进行中。"

    # screens.rpy:1200
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1212
    old "Skipping"
    new "正在快进"

    # screens.rpy:1219
    old "## This transform is used to blink the arrows one after another."
    new "## 此变换用于一个接一个地闪烁箭头。"

    # screens.rpy:1246
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## 我们必须使用包含“BLACK RIGHT-POINTING SMALL TRIANGLE”字形的字体。"

    # screens.rpy:1251
    old "## Notify screen"
    new "## 通知屏幕"

    # screens.rpy:1253
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## 通知屏幕用于向玩家显示消息。（例如，当游戏快速保存或已截屏时。）"

    # screens.rpy:1256
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1290
    old "## NVL screen"
    new "## NVL 模式屏幕"

    # screens.rpy:1292
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## 此屏幕用于 NVL 模式的对话和菜单。"

    # screens.rpy:1294
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1305
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## 在“vpgrid”或“vbox”中显示对话框。"

    # screens.rpy:1318
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## 如果给定，则显示“menu”。 如果“config.narrator_menu”设置为“True”，则“menu”可能显示不正确，如前述。"

    # screens.rpy:1348
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 此代码控制一次可以显示的最大 NVL 模式条目数。"

    # screens.rpy:1410
    old "## Mobile Variants"
    new "## 移动设备界面"

    # screens.rpy:1417
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## 由于鼠标可能不存在，我们将快捷菜单替换为更容易触摸且按钮更少更大的版本。"

    # screens.rpy:1433
    old "Menu"
    new "菜单"
