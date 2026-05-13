translate schinese strings:

    # gui/game/gui.rpy:2
    old "## Initialization"
    new "## 初始化"

    # gui/game/gui.rpy:5
    old "## The init offset statement causes the initialization statements in this file to run before init statements in any other file."
    new "## “init offset”语句可使此文件中的初始化语句在任何其他文件中的“init”语句之前运行。"

    # gui/game/gui.rpy:9
    old "## Calling gui.init resets the styles to sensible default values, and sets the width and height of the game."
    new "## 调用 gui.init 会将样式重置为合理的默认值，并设置游戏的宽度和高度（基准分辨率）。"

    # gui/game/gui.rpy:17
    old "## GUI Configuration Variables"
    new "## GUI 配置变量"

    # gui/game/gui.rpy:21
    old "## Colors"
    new "## 颜色"

    # gui/game/gui.rpy:23
    old "## The colors of text in the interface."
    new "## 界面中文本的颜色。"

    # gui/game/gui.rpy:25
    old "## An accent color used throughout the interface to label and highlight text."
    new "## 整个界面中使用的强调色，用于标记和突出显示文本。"

    # gui/game/gui.rpy:29
    old "## The color used for a text button when it is neither selected nor hovered."
    new "## 当文本按钮既未被选中也未被悬停时使用的颜色。"

    # gui/game/gui.rpy:32
    old "## The small color is used for small text, which needs to be brighter/darker to achieve the same effect."
    new "## 小的颜色用于小的文本，需要更亮/更暗才能达到同样的效果。"

    # gui/game/gui.rpy:36
    old "## The color that is used for buttons and bars that are hovered."
    new "## 当按钮和滑条被悬停时使用的颜色。"

    # gui/game/gui.rpy:39
    old "## The color used for a text button when it is selected but not focused. A button is selected if it is the current screen or preference value."
    new "## 当文本按钮被选中但非焦点时使用的颜色。当一个按钮为当前屏幕或设置选项值时，会处于选中状态。"

    # gui/game/gui.rpy:43
    old "## The color used for a text button when it cannot be selected."
    new "## 当文本按钮无法被选择时使用的颜色。"

    # gui/game/gui.rpy:46
    old "## Colors used for the portions of bars that are not filled in. These are not used directly, but are used when re-generating bar image files."
    new "## 滑条未填充的部分使用的颜色。这些颜色不直接使用，但在重新生成条形图像文件时使用。"

    # gui/game/gui.rpy:51
    old "## The colors used for dialogue and menu choice text."
    new "## 对话和菜单选择文本使用的颜色。"

    # gui/game/gui.rpy:56
    old "## Fonts and Font Sizes"
    new "## 字体和字体大小"

    # gui/game/gui.rpy:58
    old "## The font used for in-game text."
    new "## 游戏内文本使用的字体。"

    # gui/game/gui.rpy:61
    old "## The font used for character names."
    new "## 角色名称使用的字体。"

    # gui/game/gui.rpy:64
    old "## The font used for out-of-game text."
    new "## 游戏外文本使用的字体。"

    # gui/game/gui.rpy:67
    old "## The size of normal dialogue text."
    new "## 普通对话文本的大小。"

    # gui/game/gui.rpy:70
    old "## The size of character names."
    new "## 角色名称的大小。"

    # gui/game/gui.rpy:73
    old "## The size of text in the game's user interface."
    new "## 游戏用户界面中文本的大小。"

    # gui/game/gui.rpy:76
    old "## The size of labels in the game's user interface."
    new "## 游戏用户界面中标签的大小。"

    # gui/game/gui.rpy:79
    old "## The size of text on the notify screen."
    new "## 通知屏幕上文本的大小。"

    # gui/game/gui.rpy:82
    old "## The size of the game's title."
    new "## 游戏标题的大小。"

    # gui/game/gui.rpy:86
    old "## Main and Game Menus"
    new "## 标题和游戏菜单"

    # gui/game/gui.rpy:88
    old "## The images used for the main and game menus."
    new "## 标题菜单和游戏菜单使用的图像。"

    # gui/game/gui.rpy:93
    old "## Dialogue"
    new "## 对话"

    # gui/game/gui.rpy:95
    old "## These variables control how dialogue is displayed on the screen one line at a time."
    new "## 这些变量控制对话如何在屏幕上逐行显示。"

    # gui/game/gui.rpy:98
    old "## The height of the textbox containing dialogue."
    new "## 包含对话的文本框的高度。"

    # gui/game/gui.rpy:101
    old "## The placement of the textbox vertically on the screen. 0.0 is the top, 0.5 is center, and 1.0 is the bottom."
    new "## 文本框在屏幕上的垂直位置。0.0 是顶部，0.5 是居中，1.0 是底部。"

    # gui/game/gui.rpy:106
    old "## The placement of the speaking character's name, relative to the textbox. These can be a whole number of pixels from the left or top, or 0.5 to center."
    new "## 叙述角色名字相对于文本框的位置。可以是从左侧或顶部起的整数像素，或设为 0.5 来居中。"

    # gui/game/gui.rpy:111
    old "## The horizontal alignment of the character's name. This can be 0.0 for left-aligned, 0.5 for centered, and 1.0 for right-aligned."
    new "## 角色名字的水平对齐方式。0.0 为左侧对齐，0.5 为居中显示，而 1.0 为右侧对齐。"

    # gui/game/gui.rpy:115
    old "## The width, height, and borders of the box containing the character's name, or None to automatically size it."
    new "## 包含角色名字的方框的宽度、高度和边框尺寸，或设为 None 来自动确定其大小。"

    # gui/game/gui.rpy:120
    old "## The borders of the box containing the character's name, in left, top, right, bottom order."
    new "## 包含角色名字的方框的边界尺寸，以左、上、右、下顺序排列。"

    # gui/game/gui.rpy:124
    old "## If True, the background of the namebox will be tiled, if False, the background of the namebox will be scaled."
    new "## 若为 True，则名字框的背景将平铺；若为 False，则名字框的背景将缩放。"

    # gui/game/gui.rpy:129
    old "## The placement of dialogue relative to the textbox. These can be a whole number of pixels relative to the left or top side of the textbox, or 0.5 to center."
    new "## 对话相对于文本框的位置。可以是相对于文本框从左侧或顶部起的整数像素，或设为 0.5 来居中。"

    # gui/game/gui.rpy:135
    old "## The maximum width of dialogue text, in pixels."
    new "## 对话文本的最大宽度，以像素为单位。"

    # gui/game/gui.rpy:138
    old "## The horizontal alignment of the dialogue text. This can be 0.0 for left-aligned, 0.5 for centered, and 1.0 for right-aligned."
    new "## 对话文本的水平对齐方式。0.0 为左侧对齐，0.5 为居中显示，而 1.0 为右侧对齐。"

    # gui/game/gui.rpy:143
    old "## Buttons"
    new "## 按钮"

    # gui/game/gui.rpy:145
    old "## These variables, along with the image files in gui/button, control aspects of how buttons are displayed."
    new "## 这些变量以及 gui/button 中的图像文件控制着按钮显示方式。"

    # gui/game/gui.rpy:148
    old "## The width and height of a button, in pixels. If None, Ren'Py computes a size."
    new "## 按钮的宽度和高度像素数。如果为 None，则 Ren'Py 将计算大小。"

    # gui/game/gui.rpy:152
    old "## The borders on each side of the button, in left, top, right, bottom order."
    new "## 按钮两侧的边框，按左、上、右、下的顺序排列。"

    # gui/game/gui.rpy:155
    old "## If True, the background image will be tiled. If False, the background image will be linearly scaled."
    new "## 若为 True，则背景图像将平铺。若为 False，则背景图像将线性缩放。"

    # gui/game/gui.rpy:159
    old "## The font used by the button."
    new "## 按钮使用的字体。"

    # gui/game/gui.rpy:162
    old "## The size of the text used by the button."
    new "## 按钮所使用的文本大小。"

    # gui/game/gui.rpy:165
    old "## The color of button text in various states."
    new "## 按钮文本在各种状态下的颜色。"

    # gui/game/gui.rpy:171
    old "## The horizontal alignment of the button text. (0.0 is left, 0.5 is center, 1.0 is right)."
    new "## 按钮文本的水平对齐方式。（0.0 为左侧对齐，0.5 为居中对齐，而 1.0 为右侧对齐）。"

    # gui/game/gui.rpy:176
    old "## These variables override settings for different kinds of buttons. Please see the gui documentation for the kinds of buttons available, and what each is used for."
    new "## 这些变量覆盖了不同类型按钮的设置。关于可用的按钮种类以及每种按钮的用途，请参阅 gui 文档。"

    # gui/game/gui.rpy:180
    old "## These customizations are used by the default interface:"
    new "## 这些定制由默认界面使用："

    # gui/game/gui.rpy:195
    old "## You can also add your own customizations, by adding properly-named variables. For example, you can uncomment the following line to set the width of a navigation button."
    new "## 您还可以通过添加正确命名的变量来添加自己的定制。例如，您可以将以下几行取消注释来设置导航按钮的宽度。"

    # gui/game/gui.rpy:202
    old "## Choice Buttons"
    new "## 选项按钮"

    # gui/game/gui.rpy:204
    old "## Choice buttons are used in the in-game menus."
    new "## 游戏内菜单使用的选项按钮。"

    # gui/game/gui.rpy:218
    old "## File Slot Buttons"
    new "## 存档按钮"

    # gui/game/gui.rpy:220
    old "## A file slot button is a special kind of button. It contains a thumbnail image, and text describing the contents of the save slot. A save slot uses image files in gui/button, like the other kinds of buttons."
    new "## 存档按钮是一种特殊的按钮。它包含一个缩略图和描述该存档内容的文本。存档使用 gui/button 中的图像文件，就像其他类型的按钮一样。"

    # gui/game/gui.rpy:224
    old "## The save slot button."
    new "## 存档位按钮。"

    # gui/game/gui.rpy:234
    old "## The width and height of thumbnails used by the save slots."
    new "## 存档所用缩略图的宽度和高度。"

    # gui/game/gui.rpy:238
    old "## The number of columns and rows in the grid of save slots."
    new "## 存档网格中的列数和行数。"

    # gui/game/gui.rpy:243
    old "## Positioning and Spacing"
    new "## 定位和间距"

    # gui/game/gui.rpy:245
    old "## These variables control the positioning and spacing of various user interface elements."
    new "## 这些变量控制各种用户界面元素的位置和间距。"

    # gui/game/gui.rpy:248
    old "## The position of the left side of the navigation buttons, relative to the left side of the screen."
    new "## 导航按钮左侧相对于屏幕左侧的位置。"

    # gui/game/gui.rpy:252
    old "## The vertical position of the skip indicator."
    new "## 快进指示器的垂直位置。"

    # gui/game/gui.rpy:255
    old "## The vertical position of the notify screen."
    new "## 通知界面的垂直位置。"

    # gui/game/gui.rpy:258
    old "## The spacing between menu choices."
    new "## 菜单选项之间的间距。"

    # gui/game/gui.rpy:261
    old "## Buttons in the navigation section of the main and game menus."
    new "## 标题菜单和游戏菜单的导航部分中的按钮。"

    # gui/game/gui.rpy:264
    old "## Controls the amount of spacing between preferences."
    new "## 控制设置项目之间的间隔量。"

    # gui/game/gui.rpy:267
    old "## Controls the amount of spacing between preference buttons."
    new "## 控制设置按钮之间的间距。"

    # gui/game/gui.rpy:270
    old "## The spacing between file page buttons."
    new "## 存档页面按钮之间的间距。"

    # gui/game/gui.rpy:273
    old "## The spacing between file slots."
    new "## 存档按钮之间的间距。"

    # gui/game/gui.rpy:276
    old "## The position of the main menu text."
    new "## 标题菜单文本的位置。"

    # gui/game/gui.rpy:280
    old "## Frames"
    new "## 框架"

    # gui/game/gui.rpy:282
    old "## These variables control the look of frames that can contain user interface components when an overlay or window is not present."
    new "## 这些变量控制在不存在覆盖层或窗口时可以包含用户界面组件的框架的外观。"

    # gui/game/gui.rpy:285
    old "## Generic frames."
    new "## 通用框架。"

    # gui/game/gui.rpy:288
    old "## The frame that is used as part of the confirm screen."
    new "## 用作确认界面部分的框架。"

    # gui/game/gui.rpy:291
    old "## The frame that is used as part of the skip screen."
    new "## 用作快进界面部分的框架。"

    # gui/game/gui.rpy:294
    old "## The frame that is used as part of the notify screen."
    new "## 用作通知界面部分的框架。"

    # gui/game/gui.rpy:297
    old "## Should frame backgrounds be tiled?"
    new "## 框架背景是否应平铺？"

    # gui/game/gui.rpy:301
    old "## Bars, Scrollbars, and Sliders"
    new "## 条，滚动条和滑块"

    # gui/game/gui.rpy:303
    old "## These control the look and size of bars, scrollbars, and sliders."
    new "## 这些语句控制条，滚动条和滑块的外观和大小。"

    # gui/game/gui.rpy:305
    old "## The default GUI only uses sliders and vertical scrollbars. All of the other bars are only used in creator-written screens."
    new "## 默认的 GUI 仅使用滑块和垂直滚动条。所有其他栏仅在创建者编写的屏幕中使用。"

    # gui/game/gui.rpy:308
    old "## The height of horizontal bars, scrollbars, and sliders. The width of vertical bars, scrollbars, and sliders."
    new "## 水平条，滚动条和滑块的高度。垂直条，滚动条和滑块的宽度。"

    # gui/game/gui.rpy:314
    old "## True if bar images should be tiled. False if they should be linearly scaled."
    new "## 若为 True，则条的底图平铺。若为 False，则条的底图线性缩放。"

    # gui/game/gui.rpy:319
    old "## Horizontal borders."
    new "## 水平边框。"

    # gui/game/gui.rpy:324
    old "## Vertical borders."
    new "## 垂直边框。"

    # gui/game/gui.rpy:329
    old "## What to do with unscrollable scrollbars in the gui. \"hide\" hides them, while None shows them."
    new "## 如何处理 GUI 中不可滚动的滚动条。 hide 为隐藏， None 为显示。"

    # gui/game/gui.rpy:334
    old "## History"
    new "## 历史"

    # gui/game/gui.rpy:336
    old "## The history screen displays dialogue that the player has already dismissed."
    new "## 历史记录屏幕显示玩家已经阅读过的对话。"

    # gui/game/gui.rpy:338
    old "## The number of blocks of dialogue history Ren'Py will keep."
    new "## Ren'Py 将保留的对话历史块数。"

    # gui/game/gui.rpy:341
    old "## The height of a history screen entry, or None to make the height variable at the cost of performance."
    new "## 历史屏幕条目的高度，或设置为 None 以使高度变量自适应。"

    # gui/game/gui.rpy:345
    old "## The position, width, and alignment of the label giving the name of the speaking character."
    new "## 所指定叙述角色的标签的坐标、宽度和对齐方式。"

    # gui/game/gui.rpy:352
    old "## The position, width, and alignment of the dialogue text."
    new "## 对话文本的坐标、宽度和对齐方式。"

    # gui/game/gui.rpy:359
    old "## NVL-Mode"
    new "## NVL 模式"

    # gui/game/gui.rpy:361
    old "## The NVL-mode screen displays the dialogue spoken by NVL-mode characters."
    new "## NVL 模式屏幕显示 NVL 模式的角色所产生的对话。"

    # gui/game/gui.rpy:363
    old "## The borders of the background of the NVL-mode background window."
    new "## NVL 模式背景窗口的背景边框。"

    # gui/game/gui.rpy:366
    old "## The maximum number of NVL-mode entries Ren'Py will display. When more entries than this are to be show, the oldest entry will be removed."
    new "## Ren'Py 所显示的 NVL 模式条目的最大数量。当要显示的条目多于此数量时，最旧的条目将被删除。"

    # gui/game/gui.rpy:370
    old "## The height of an NVL-mode entry. Set this to None to have the entries dynamically adjust height."
    new "## NVL 模式条目的高度。将此设置为 None 可使条目动态调整高度。"

    # gui/game/gui.rpy:374
    old "## The spacing between NVL-mode entries when gui.nvl_height is None, and between NVL-mode entries and an NVL-mode menu."
    new "## 当 gui.nvl_height 为 None 时，NVL 模式条目之间的间距，以及 NVL 模式条目和 NVL 模式菜单之间的间距。"

    # gui/game/gui.rpy:391
    old "## The position, width, and alignment of nvl_thought text (the text said by the nvl_narrator character.)"
    new "## nvl_thought 文本（由 nvl_narrator 字符表示的文本）的位置，宽度和对齐方式。"

    # gui/game/gui.rpy:398
    old "## The position of nvl menu_buttons."
    new "## NVL menu_buttons 的位置。"

    # gui/game/gui.rpy:402
    old "## Localization"
    new "## 本地化"

    # gui/game/gui.rpy:404
    old "## This controls where a line break is permitted. The default is suitable for most languages. A list of available values can be found at https://www.renpy.org/doc/html/style_properties.html#style-property-language"
    new "## 该变量控制允许在何时换行。默认值适用于大多数语言。可用的值请参见 https://www.renpy.org/doc/html/style_properties.html#style-property-language"

    # gui/game/gui.rpy:412
    old "## Mobile devices"
    new "## 移动设备"

    # gui/game/gui.rpy:417
    old "## This increases the size of the quick buttons to make them easier to touch on tablets and phones."
    new "## 该变量增加快捷菜单按钮的尺寸来使它们在平板和手机上更容易被按到。"

    # gui/game/gui.rpy:424
    old "## This changes the size and spacing of various GUI elements to ensure they are easily visible on phones."
    new "## 该变量更改各个 GUI 元素的尺寸和间距来确保它们在手机上更容易被辨识。"

    # gui/game/gui.rpy:429
    old "## Font sizes."
    new "## 字体大小。"

    # gui/game/gui.rpy:437
    old "## Adjust the location of the textbox."
    new "## 调整对话框的位置。"

    # gui/game/gui.rpy:443
    old "## Change the size and spacing of various things."
    new "## 更改各元素的尺寸和间距。"

    # gui/game/gui.rpy:457
    old "## File button layout."
    new "## 文件按钮布局。"

    # gui/game/gui.rpy:461
    old "## NVL-mode."
    new "## NVL 模式。"

    # gui/game/gui.rpy:14
    old "## Enable checks for invalid or unstable properties in screens or transforms"
    new "## 启用对屏幕或变换中无效或不稳定属性的检查"

    # gui/game/gui.rpy:347
    old "## Additional space to add between history screen entries."
    new "## 在历史记录屏幕条目之间添加额外的空间。"
