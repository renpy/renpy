translate schinese strings:

    # gui/game/screens.rpy:9
    old "## Styles"
    new "## 样式"

    # gui/game/screens.rpy:81
    old "## In-game screens"
    new "## 游戏内屏幕"

    # gui/game/screens.rpy:85
    old "## Say screen"
    new "## 对话屏幕"

    # gui/game/screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## 对话屏幕用于向用户显示对话。它需要两个参数，who 和 what，分别是叙述角色的名字和所叙述的文本。（如果没有名字，参数 who 可以是 None。）"

    # gui/game/screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## 此屏幕必须创建一个 id 为 what 的文本可视控件，因为 Ren'Py 使用它来管理文本显示。它还可以创建 id 为 who 和 id 为 window 的可视控件来应用样式属性。"

    # gui/game/screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.cn/doc/screen_special.html#say"

    # gui/game/screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## 如果有对话框头像，会将其显示在文本之上。请不要在手机界面下显示这个，因为没有空间。"

    # gui/game/screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## 通过 Character 对象使名称框可用于样式化。"

    # gui/game/screens.rpy:165
    old "## Input screen"
    new "## 输入屏幕"

    # gui/game/screens.rpy:167
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## 此屏幕用于显示 renpy.input。prompt 参数用于传递文本提示。"

    # gui/game/screens.rpy:170
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## 此屏幕必须创建一个 id 为 input 的输入可视控件来接受各种输入参数。"

    # gui/game/screens.rpy:173
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.cn/doc/screen_special.html#input"

    # gui/game/screens.rpy:200
    old "## Choice screen"
    new "## 选择屏幕"

    # gui/game/screens.rpy:202
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## 此屏幕用于显示由 menu 语句生成的游戏内选项。参数 items 是一个对象列表，每个对象都有字幕和动作字段。"

    # gui/game/screens.rpy:206
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.cn/doc/screen_special.html#choice"

    # gui/game/screens.rpy:234
    old "## Quick Menu screen"
    new "## 快捷菜单屏幕"

    # gui/game/screens.rpy:236
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## 快捷菜单显示于游戏内，以便于访问游戏外的菜单。"

    # gui/game/screens.rpy:241
    old "## Ensure this appears on top of other screens."
    new "## 确保该菜单出现在其他屏幕之上，"

    # gui/game/screens.rpy:252
    old "Back"
    new "回退"

    # gui/game/screens.rpy:253
    old "History"
    new "历史"

    # gui/game/screens.rpy:254
    old "Skip"
    new "快进"

    # gui/game/screens.rpy:255
    old "Auto"
    new "自动"

    # gui/game/screens.rpy:256
    old "Save"
    new "保存"

    # gui/game/screens.rpy:257
    old "Q.Save"
    new "快存"

    # gui/game/screens.rpy:258
    old "Q.Load"
    new "快读"

    # gui/game/screens.rpy:259
    old "Prefs"
    new "设置"

    # gui/game/screens.rpy:262
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## 此代码确保只要用户没有主动隐藏界面，就会在游戏中显示 quick_menu 屏幕。"

    # gui/game/screens.rpy:280
    old "## Main and Game Menu Screens"
    new "## 标题和游戏菜单屏幕"

    # gui/game/screens.rpy:283
    old "## Navigation screen"
    new "## 导航屏幕"

    # gui/game/screens.rpy:285
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## 该屏幕包含在标题菜单和游戏菜单中，并提供导航到其他菜单，以及启动游戏。"

    # gui/game/screens.rpy:300
    old "Start"
    new "开始游戏"

    # gui/game/screens.rpy:308
    old "Load"
    new "读取游戏"

    # gui/game/screens.rpy:310
    old "Preferences"
    new "设置"

    # gui/game/screens.rpy:314
    old "End Replay"
    new "结束回放"

    # gui/game/screens.rpy:318
    old "Main Menu"
    new "标题菜单"

    # gui/game/screens.rpy:320
    old "About"
    new "关于"

    # gui/game/screens.rpy:324
    old "## Help isn't necessary or relevant to mobile devices."
    new "## “帮助”对移动设备来说并非必需或相关。"

    # gui/game/screens.rpy:325
    old "Help"
    new "帮助"

    # gui/game/screens.rpy:329
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## 退出按钮在 iOS 上是被禁止使用的，在安卓和网页上也不是必要的。"

    # gui/game/screens.rpy:330
    old "Quit"
    new "退出"

    # gui/game/screens.rpy:344
    old "## Main Menu screen"
    new "## 标题菜单屏幕"

    # gui/game/screens.rpy:346
    old "## Used to display the main menu when Ren'Py starts."
    new "## 用于在 Ren'Py 启动时显示标题菜单。"

    # gui/game/screens.rpy:348
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.cn/doc/screen_special.html#main-menu"

    # gui/game/screens.rpy:352
    old "## This ensures that any other menu screen is replaced."
    new "## 此语句可确保替换掉任何其他菜单屏幕。"

    # gui/game/screens.rpy:357
    old "## This empty frame darkens the main menu."
    new "## 此空框可使标题菜单变暗。"

    # gui/game/screens.rpy:361
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## use 语句将其他的屏幕包含进此屏幕。标题屏幕的实际内容在导航屏幕中。"

    # gui/game/screens.rpy:406
    old "## Game Menu screen"
    new "## 游戏菜单屏幕"

    # gui/game/screens.rpy:408
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## 此屏幕列出了游戏菜单的基本共同结构。可使用屏幕标题调用，并显示背景、标题和导航菜单。"

    # gui/game/screens.rpy:411
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## scroll 参数可以是 None，也可以是 viewport 或 vpgrid。此屏幕旨在与一个或多个子屏幕同时使用，这些子屏幕将被嵌入（放置）在其中。"

    # gui/game/screens.rpy:429
    old "## Reserve space for the navigation section."
    new "## 导航部分的预留空间。"

    # gui/game/screens.rpy:471
    old "Return"
    new "返回"

    # gui/game/screens.rpy:534
    old "## About screen"
    new "## 关于屏幕"

    # gui/game/screens.rpy:536
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## 此屏幕提供有关游戏和 Ren'Py 的制作人员和版权信息。"

    # gui/game/screens.rpy:539
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## 此屏幕没有什么特别之处，因此它也可以作为一个例子来说明如何制作一个自定义屏幕。"

    # gui/game/screens.rpy:546
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## 此 use 语句将 game_menu 屏幕包含到了这个屏幕内。子级 vbox 将包含在 game_menu 屏幕的 viewport 内。"

    # gui/game/screens.rpy:556
    old "Version [config.version!t]\n"
    new "版本 [config.version!t]\n"

    # gui/game/screens.rpy:558
    old "## gui.about is usually set in options.rpy."
    new "## gui.about 通常在 options.rpy 中设置。"

    # gui/game/screens.rpy:562
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "引擎：{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only]\n\n[renpy.license!t]"

    # gui/game/screens.rpy:573
    old "## Load and Save screens"
    new "## 读取和保存屏幕"

    # gui/game/screens.rpy:575
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## 这些屏幕负责让用户保存游戏并能够再次读取。由于它们几乎完全一样，因此这两个屏幕都是以第三个屏幕 file_slots 来实现的。"

    # gui/game/screens.rpy:579
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.cn/doc/screen_special.html#save https://www.renpy.cn/doc/screen_special.html#load"

    # gui/game/screens.rpy:598
    old "Page {}"
    new "第 {} 页"

    # gui/game/screens.rpy:598
    old "Automatic saves"
    new "自动存档"

    # gui/game/screens.rpy:598
    old "Quick saves"
    new "快速存档"

    # gui/game/screens.rpy:604
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## 此代码确保输入控件在任意按钮执行前可以获取 enter 事件。"

    # gui/game/screens.rpy:608
    old "## The page name, which can be edited by clicking on a button."
    new "## 页面名称，可以通过单击按钮进行编辑。"

    # gui/game/screens.rpy:620
    old "## The grid of file slots."
    new "## 存档位网格。"

    # gui/game/screens.rpy:640
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%Y-%m-%d %H:%M"

    # gui/game/screens.rpy:640
    old "empty slot"
    new "空存档位"

    # gui/game/screens.rpy:648
    old "## Buttons to access other pages."
    new "## 用于访问其他页面的按钮。"

    # gui/game/screens.rpy:657
    old "<"
    new "<"

    # gui/game/screens.rpy:660
    old "{#auto_page}A"
    new "{#auto_page}A"

    # gui/game/screens.rpy:663
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # gui/game/screens.rpy:665
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) 给出 1 到 9 之间的数字。"

    # gui/game/screens.rpy:669
    old ">"
    new ">"

    # gui/game/screens.rpy:704
    old "## Preferences screen"
    new "## 设置屏幕"

    # gui/game/screens.rpy:706
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## 设置屏幕允许用户配置游戏，使其更适合自己。"

    # gui/game/screens.rpy:709
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.cn/doc/screen_special.html#preferences"

    # gui/game/screens.rpy:726
    old "Display"
    new "显示"

    # gui/game/screens.rpy:727
    old "Window"
    new "窗口"

    # gui/game/screens.rpy:728
    old "Fullscreen"
    # Automatic translation.
    new "全屏"

    # gui/game/screens.rpy:733
    old "Unseen Text"
    new "未读文本"

    # gui/game/screens.rpy:734
    old "After Choices"
    new "选项后继续"

    # gui/game/screens.rpy:735
    old "Transitions"
    new "忽略转场"

    # gui/game/screens.rpy:737
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## 可在此处添加 radio_pref 或 check_pref 类型的额外 vbox，以添加额外的创建者定义的偏好设置。"

    # gui/game/screens.rpy:748
    old "Text Speed"
    new "文字速度"

    # gui/game/screens.rpy:752
    old "Auto-Forward Time"
    new "自动前进时间"

    # gui/game/screens.rpy:759
    old "Music Volume"
    new "音乐音量"

    # gui/game/screens.rpy:766
    old "Sound Volume"
    new "音效音量"

    # gui/game/screens.rpy:772
    old "Test"
    new "测试"

    # gui/game/screens.rpy:776
    old "Voice Volume"
    new "语音音量"

    # gui/game/screens.rpy:787
    old "Mute All"
    new "全部静音"

    # gui/game/screens.rpy:863
    old "## History screen"
    new "## 历史屏幕"

    # gui/game/screens.rpy:865
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## 这是一个向用户显示对话历史的屏幕。虽然此屏幕没有什么特别之处，但它必须访问储存在 _history_list 中的对话历史记录。"

    # gui/game/screens.rpy:869
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.cn/doc/history.html"

    # gui/game/screens.rpy:875
    old "## Avoid predicting this screen, as it can be very large."
    new "## 避免预缓存此屏幕，因为它可能非常大。"

    # gui/game/screens.rpy:886
    old "## This lays things out properly if history_height is None."
    new "## 此代码可确保如果 history_height 为 None 时仍可正常显示条目。"

    # gui/game/screens.rpy:896
    old "## Take the color of the who text from the Character, if set."
    new "## 从 Character 对象中获取叙述角色的文字颜色，如果设置了的话。"

    # gui/game/screens.rpy:905
    old "The dialogue history is empty."
    new "尚无对话历史记录。"

    # gui/game/screens.rpy:908
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## 此代码决定了允许在历史记录屏幕上显示哪些标签。"

    # gui/game/screens.rpy:953
    old "## Help screen"
    new "## 帮助屏幕"

    # gui/game/screens.rpy:955
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## 提供有关键盘和鼠标映射信息的屏幕。它使用其它屏幕（keyboard_help、mouse_help 和 gamepad_help）来显示实际的帮助内容。"

    # gui/game/screens.rpy:974
    old "Keyboard"
    new "键盘"

    # gui/game/screens.rpy:975
    old "Mouse"
    new "鼠标"

    # gui/game/screens.rpy:978
    old "Gamepad"
    new "手柄"

    # gui/game/screens.rpy:991
    old "Enter"
    new "回车"

    # gui/game/screens.rpy:992
    old "Advances dialogue and activates the interface."
    new "推进对话并激活界面。"

    # gui/game/screens.rpy:995
    old "Space"
    new "空格"

    # gui/game/screens.rpy:996
    old "Advances dialogue without selecting choices."
    new "在没有选择的情况下推进对话。"

    # gui/game/screens.rpy:999
    old "Arrow Keys"
    new "方向键"

    # gui/game/screens.rpy:1000
    old "Navigate the interface."
    new "导航界面。"

    # gui/game/screens.rpy:1003
    old "Escape"
    new "Esc"

    # gui/game/screens.rpy:1004
    old "Accesses the game menu."
    new "访问游戏菜单。"

    # gui/game/screens.rpy:1007
    old "Ctrl"
    # Automatic translation.
    new "键盘"

    # gui/game/screens.rpy:1008
    old "Skips dialogue while held down."
    new "按住时快进对话。"

    # gui/game/screens.rpy:1011
    old "Tab"
    new "Tab"

    # gui/game/screens.rpy:1012
    old "Toggles dialogue skipping."
    new "切换对话快进。"

    # gui/game/screens.rpy:1015
    old "Page Up"
    # Automatic translation.
    new "上一页"

    # gui/game/screens.rpy:1016
    old "Rolls back to earlier dialogue."
    new "回退至先前的对话。"

    # gui/game/screens.rpy:1019
    old "Page Down"
    # Automatic translation.
    new "下一页"

    # gui/game/screens.rpy:1020
    old "Rolls forward to later dialogue."
    new "向前至后来的对话。"

    # gui/game/screens.rpy:1024
    old "Hides the user interface."
    new "隐藏用户界面。"

    # gui/game/screens.rpy:1028
    old "Takes a screenshot."
    new "截图。"

    # gui/game/screens.rpy:1032
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "切换辅助{a=https://www.renpy.cn/doc/self_voicing.html}机器朗读{/a}。"

    # gui/game/screens.rpy:1036
    old "Opens the accessibility menu."
    new "打开无障碍菜单。"

    # gui/game/screens.rpy:1042
    old "Left Click"
    new "左键点击"

    # gui/game/screens.rpy:1046
    old "Middle Click"
    new "中键点击"

    # gui/game/screens.rpy:1050
    old "Right Click"
    new "右键点击"

    # gui/game/screens.rpy:1054
    old "Mouse Wheel Up\nClick Rollback Side"
    new "鼠标滚轮上\n点击回退操作区"

    # gui/game/screens.rpy:1058
    old "Mouse Wheel Down"
    new "鼠标滚轮下"

    # gui/game/screens.rpy:1065
    old "Right Trigger\nA/Bottom Button"
    new "右扳机键\nA/底键"

    # gui/game/screens.rpy:1069
    old "Left Trigger\nLeft Shoulder"
    new "左扳机键\n左肩键"

    # gui/game/screens.rpy:1073
    old "Right Shoulder"
    new "右肩键"

    # gui/game/screens.rpy:1078
    old "D-Pad, Sticks"
    new "十字键，摇杆"

    # gui/game/screens.rpy:1082
    old "Start, Guide"
    new "开始，向导"

    # gui/game/screens.rpy:1086
    old "Y/Top Button"
    new "Y/顶键"

    # gui/game/screens.rpy:1089
    old "Calibrate"
    new "校准"

    # gui/game/screens.rpy:1117
    old "## Additional screens"
    new "## 其他屏幕"

    # gui/game/screens.rpy:1121
    old "## Confirm screen"
    new "## 确认屏幕"

    # gui/game/screens.rpy:1123
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## 当 Ren'Py 需要询问用户有关确定或取消的问题时，会调用确认屏幕。"

    # gui/game/screens.rpy:1126
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.cn/doc/screen_special.html#confirm"

    # gui/game/screens.rpy:1130
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## 显示此屏幕时，确保其他屏幕无法输入。"

    # gui/game/screens.rpy:1154
    old "Yes"
    new "确定"

    # gui/game/screens.rpy:1155
    old "No"
    new "取消"

    # gui/game/screens.rpy:1157
    old "## Right-click and escape answer \"no\"."
    new "## 右键点击退出并答复 no（取消）。"

    # gui/game/screens.rpy:1184
    old "## Skip indicator screen"
    new "## 快进指示屏幕"

    # gui/game/screens.rpy:1186
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## skip_indicator 屏幕用于指示快进正在进行中。"

    # gui/game/screens.rpy:1189
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.cn/doc/screen_special.html#skip-indicator"

    # gui/game/screens.rpy:1201
    old "Skipping"
    new "正在快进"

    # gui/game/screens.rpy:1208
    old "## This transform is used to blink the arrows one after another."
    new "## 此变换用于一个接一个地闪烁箭头。"

    # gui/game/screens.rpy:1235
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## 我们必须使用包含“▸”（黑色右旋小三角）字形的字体。"

    # gui/game/screens.rpy:1240
    old "## Notify screen"
    new "## 通知屏幕"

    # gui/game/screens.rpy:1242
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## 通知屏幕用于向用户显示消息。（例如，当游戏快速保存或进行截屏时。）"

    # gui/game/screens.rpy:1245
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.cn/doc/screen_special.html#notify-screen"

    # gui/game/screens.rpy:1279
    old "## NVL screen"
    new "## NVL 模式屏幕"

    # gui/game/screens.rpy:1281
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## 此屏幕用于 NVL 模式的对话和菜单。"

    # gui/game/screens.rpy:1283
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.cn/doc/screen_special.html#nvl"

    # gui/game/screens.rpy:1294
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## 在 vpgrid 或 vbox 中显示对话框。"

    # gui/game/screens.rpy:1307
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## 显示菜单，如果给定的话。如果 config.narrator_menu 设置为 True，则菜单可能显示不正确。"

    # gui/game/screens.rpy:1337
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## 此语句控制一次可以显示的 NVL 模式条目的最大数量。"

    # gui/game/screens.rpy:1399
    old "## Mobile Variants"
    new "## 移动设备界面"

    # gui/game/screens.rpy:1406
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## 由于可能没有鼠标，我们将快捷菜单替换为一个使用更少、更大按钮的版本，这样更容易触摸。"

    # gui/game/screens.rpy:1424
    old "Menu"
    new "菜单"

    # gui/game/screens.rpy:676
    old "Upload Sync"
    new "上传同步"

    # gui/game/screens.rpy:680
    old "Download Sync"
    new "下载同步"

    # gui/game/screens.rpy:1410
    old "## Bubble screen"
    new "## 对话气泡屏幕"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## 对话气泡屏幕用于以对话气泡的形式向玩家显示对话。对话气泡屏幕的参数与 say 屏幕相同，必须创建一个 id 为 what 的可视控件，并且可以创建 id 为 namebox、who 和 window 的可视控件。"

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    
