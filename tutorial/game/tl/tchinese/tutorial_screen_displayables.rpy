
# game/tutorial_screen_displayables.rpy:3
translate tchinese screen_displayables_7c897a6d:

    # e "There are quite a few screen displayables. Here, I'll tell you about some of the most important ones."
    e "螢幕語言有相當多的顯示物件。這裡介紹其中一些最重要的。"

# game/tutorial_screen_displayables.rpy:9
translate tchinese screen_displayables_menu_fef7b441:

    # e "What would you like to know about?" nointeract
    e "你想了解什麼？" nointeract

# game/tutorial_screen_displayables.rpy:49
translate tchinese screen_displayable_properties_76c5639a:

    # e "There are a few properties that every screen language displayable shares. Here, I'll demonstrate them for you."
    e "有些屬性是每個螢幕語言顯示物件共用的，這裡示範給你看。"

# game/tutorial_screen_displayables.rpy:57
translate tchinese screen_displayable_properties_527d4b4e:

    # e "First off, every screen language displayable supports the position properties. When the container a displayable is in supports it, you can use properties like align, anchor, pos, and so so on."
    e "首先，每個螢幕語言顯示物件都支援位置屬性。容器支援時，可以使用 align、anchor、pos 等屬性。"

# game/tutorial_screen_displayables.rpy:69
translate tchinese screen_displayable_properties_8aff26dd:

    # e "The at property applies a transform to the displayable, the same way the at clause in the show statement does."
    e "at 屬性會對顯示物件套用變換，用法與 show 語句中的 at 子句相同。"

# game/tutorial_screen_displayables.rpy:106
translate tchinese screen_displayable_properties_2ed40a70:

    # e "The id property is mostly used with the say screen, which is used to show dialogue. Outside of the say screen, it isn't used much."
    e "id 屬性主要用於 say 螢幕，也就是顯示對話的螢幕。在 say 螢幕之外不常使用。"

# game/tutorial_screen_displayables.rpy:108
translate tchinese screen_displayable_properties_da5733d1:

    # e "It tells Ren'Py which displayables are the background window, 'who' is speaking, and 'what' is being said. This used to apply per-Character styles, and help with auto-forward mode."
    e "它告訴 Ren'Py 哪個顯示物件是背景視窗、誰（who）正在說話，以及說了什麼（what）。這會套用於每個 Character 樣式，並協助自動前進模式。"

# game/tutorial_screen_displayables.rpy:123
translate tchinese screen_displayable_properties_cc09fade:

    # e "The style property lets you specify the style of a single displayable."
    e "style 屬性讓你指定單一顯示物件的樣式。"

# game/tutorial_screen_displayables.rpy:144
translate tchinese screen_displayable_properties_a7f4e25c:

    # e "The style_prefix property sets the prefix of the style that's used for a displayable and its children."
    e "style_prefix 屬性會設定顯示物件及其子物件使用的樣式前綴。"

# game/tutorial_screen_displayables.rpy:146
translate tchinese screen_displayable_properties_6bdb0723:

    # e "For example, when the style_prefix property is 'green', the vbox has the 'green_vbox' style, and the text in it has the 'green_text' style."
    e "例如 style_prefix 設為 green 時，vbox 會使用 green_vbox 樣式，其中的文字會使用 green_text 樣式。"

# game/tutorial_screen_displayables.rpy:150
translate tchinese screen_displayable_properties_8a3a8635:

    # e "There are a few more properties than these, and you can find the rest in the documentation. But these are the ones you can expect to see in your game, in the default screens."
    e "還有其他屬性可以在文件中找到，但以上是你在預設螢幕中最常看到的屬性。"

# game/tutorial_screen_displayables.rpy:156
translate tchinese add_displayable_ec121c5c:

    # e "Sometimes you'll have a displayable, like an image, that you want to add to a screen."
    e "有時你會想把圖片等顯示物件加入螢幕。"

# game/tutorial_screen_displayables.rpy:165
translate tchinese add_displayable_7ec3e2b0:

    # e "This can be done using the add statement, which adds an image or other displayable to the screen."
    e "可以使用 add 語句，將圖片或其他顯示物件加入螢幕。"

# game/tutorial_screen_displayables.rpy:167
translate tchinese add_displayable_7112a377:

    # e "There are a few ways to refer to the image. If it's in the images directory or defined with the image statement, you can just put the name inside a quoted string."
    e "引用圖片有幾種方式。如果圖片位於 images 目錄，或以 image 語句定義，只要把名稱放入引號字串即可。"

# game/tutorial_screen_displayables.rpy:176
translate tchinese add_displayable_8ba81c26:

    # e "An image can also be referred to by it's filename, relative to the game directory."
    e "也可以使用相對於 game 目錄的檔名引用圖片。"

# game/tutorial_screen_displayables.rpy:185
translate tchinese add_displayable_1f5571e3:

    # e "Other displayables can also be added using the add statement. Here, we add the Solid displayable, showing a solid block of color."
    e "其他顯示物件也能用 add 語句加入。這裡加入 Solid 顯示物件，顯示一個實心色塊。"

# game/tutorial_screen_displayables.rpy:195
translate tchinese add_displayable_0213ffa2:

    # e "In addition to the displayable, the add statement can be given transform properties. These can place or otherwise transform the displayable being added."
    e "除了顯示物件，add 語句也能使用變換屬性，定位或變換加入的顯示物件。"

# game/tutorial_screen_displayables.rpy:207
translate tchinese add_displayable_3a56a464:

    # e "Of course, the add statement can also take the at property, letting you give it a more complex transform."
    e "當然，add 語句也可以使用 at 屬性進行更複雜的變換。"

# game/tutorial_screen_displayables.rpy:222
translate tchinese text_displayable_96f88225:

    # e "The screen language text statement adds a text displayable to the screen. It takes one argument, the text to be displayed."
    e "螢幕語言的 text 語句會將文字顯示物件加入螢幕，接收要顯示的文字作為參數。"

# game/tutorial_screen_displayables.rpy:224
translate tchinese text_displayable_1ed1a8c2:

    # e "In addition to the common properties that all displayables take, text takes the text style properties. For example, size sets the size of the text."
    e "除了所有顯示物件都有的一般屬性，文字還有文字樣式屬性。例如 size 會設定文字大小。"

# game/tutorial_screen_displayables.rpy:234
translate tchinese text_displayable_9351d9dd:

    # e "The text displayable can also interpolate values enclosed in square brackets."
    e "文字顯示物件也可以插入方括號中的值。"

# game/tutorial_screen_displayables.rpy:236
translate tchinese text_displayable_32d76ccb:

    # e "When text is displayed in a screen using the text statement variables defined in the screen take precedence over those defined outside it."
    e "使用 text 語句在螢幕中顯示文字時，螢幕內定義的變數會優先於外部變數。"

# game/tutorial_screen_displayables.rpy:238
translate tchinese text_displayable_7e84a5d1:

    # e "Those variables may be parameters given to the screen, defined with the default or python statements, or set using the SetScreenVariable action."
    e "這些變數可能是螢幕參數、由 default 或 python 語句定義，或由 SetScreenVariable 動作設定。"

# game/tutorial_screen_displayables.rpy:247
translate tchinese text_displayable_8bc866c4:

    # e "There's not much more to say about text in screens, as it works the same way as all other text in Ren'Py."
    e "關於螢幕中的文字沒有更多要說的；它和 Ren'Py 其他文字的運作方式相同。"

# game/tutorial_screen_displayables.rpy:255
translate tchinese layout_displayables_d75efbae:

    # e "The layout displayables take other displayables and lay them out on the screen."
    e "版面顯示物件接收其他顯示物件，並將它們排列在螢幕上。"

# game/tutorial_screen_displayables.rpy:269
translate tchinese layout_displayables_9a15144d:

    # e "For example, the hbox displayable takes its children and lays them out horizontally."
    e "例如，hbox 顯示物件會水平排列子物件。"

# game/tutorial_screen_displayables.rpy:284
translate tchinese layout_displayables_48eff197:

    # e "The vbox displayable is similar, except it takes its children and arranges them vertically."
    e "vbox 顯示物件類似，但會垂直排列子物件。"

# game/tutorial_screen_displayables.rpy:286
translate tchinese layout_displayables_74de8a66:

    # e "Both of the boxes take the box style properties, the most useful of which is spacing, the amount of space to leave between children."
    e "這兩種 box 都使用 box 樣式屬性，其中最有用的是 spacing，也就是子物件之間的空間。"

# game/tutorial_screen_displayables.rpy:301
translate tchinese layout_displayables_a156591f:

    # e "The grid displayable displays its children in a grid of equally-sized cells. It takes two arguments, the number of columns and the number of rows."
    e "grid 顯示物件會在大小相同的儲存格網格中顯示子物件，接收欄數和列數兩個參數。"

# game/tutorial_screen_displayables.rpy:303
translate tchinese layout_displayables_126f5816:

    # e "The grid has to be full, or Ren'Py will produce an error. Notice how in this example, the empty cell is filled with a null."
    e "grid 必須填滿，否則 Ren'Py 會產生錯誤。注意這個例子如何用 null 填入空白儲存格。"

# game/tutorial_screen_displayables.rpy:305
translate tchinese layout_displayables_bfaaaf9b:

    # e "Like the boxes, grid uses the spacing property to specify the space between cells."
    e "和 box 一樣，grid 使用 spacing 屬性指定儲存格之間的距離。"

# game/tutorial_screen_displayables.rpy:321
translate tchinese layout_displayables_3e931106:

    # e "Grid also takes the transpose property, to make it fill top-to-bottom before it fills left-to-right."
    e "grid 也接收 transpose 屬性，讓它先由上到下，再由左到右填入。"

# game/tutorial_screen_displayables.rpy:338
translate tchinese layout_displayables_afdc1b11:

    # e "And just to demonstrate that all cells are equally-sized, here's what happens when once child is bigger than the others."
    e "為了展示所有儲存格大小相同，這裡示範某個子物件比其他子物件更大時的情況。"

# game/tutorial_screen_displayables.rpy:353
translate tchinese layout_displayables_a23e2826:

    # e "The fixed displayable displays the children using Ren'Py's normal placement algorithm. This lets you place displayables anywhere in the screen."
    e "fixed 顯示物件使用 Ren'Py 一般的位置演算法顯示子物件，可以把顯示物件放在螢幕任意位置。"

# game/tutorial_screen_displayables.rpy:355
translate tchinese layout_displayables_fd3926ca:

    # e "By default, the layout expands to fill all the space available to it. To prevent that, we use the xsize and ysize properties to set its size in advance."
    e "預設情況下，版面會擴展填滿所有可用空間。為避免這種情況，我們用 xsize 和 ysize 屬性預先設定大小。"

# game/tutorial_screen_displayables.rpy:369
translate tchinese layout_displayables_eff42786:

    # e "When a non-layout displayable is given two or more children, it's not necessary to create a fixed. A fixed is automatically added, and the children are added to it."
    e "沒有版面的顯示物件包含兩個以上子物件時，不需要建立 fixed；fixed 會自動建立並把子物件加入其中。"

# game/tutorial_screen_displayables.rpy:384
translate tchinese layout_displayables_c32324a7:

    # e "Finally, there's one convenience to save space. When many displayables are nested, adding a layout to each could cause crazy indent levels."
    e "最後還有節省空間的便利功能。許多顯示物件巢狀時，為每一項加入版面可能造成令人抓狂的縮排層級。"

# game/tutorial_screen_displayables.rpy:386
translate tchinese layout_displayables_d7fa0f28:

    # e "The has statement creates a layout, and then adds all further children of its parent to that layout. It's just a convenience to make screens more readable."
    e "has 語句會建立版面，再把父物件的所有子物件加入其中，這只是為了讓螢幕更易讀。"

# game/tutorial_screen_displayables.rpy:395
translate tchinese window_displayables_14beb786:

    # e "In the default GUI that Ren'Py creates for a game, most user interface elements expect some sort of background."
    e "在 Ren'Py 為遊戲建立的預設 GUI 中，大多數使用者介面元素都需要某種背景。"

# game/tutorial_screen_displayables.rpy:405
translate tchinese window_displayables_495d332b:

    # e "Without the background, text can be hard to read. While a frame isn't strictly required, many screens have one or more of them."
    e "沒有背景時，文字可能很難閱讀。雖然 frame 並非絕對必要，但許多螢幕都會使用它。"

# game/tutorial_screen_displayables.rpy:417
translate tchinese window_displayables_2c0565ab:

    # e "But when I add a background, it's much easier. That's why there are two displayables that are intended to give backgrounds to user interface elements."
    e "加上背景後就容易閱讀多了。因此有兩種顯示物件專門為使用者介面元素提供背景。"

# game/tutorial_screen_displayables.rpy:419
translate tchinese window_displayables_c7d0968c:

    # e "The two displayables are frame and window. Frame is the one we use above, and it's designed to provide a background for arbitrary parts of the user interface."
    e "這兩種顯示物件是 frame 和 window。前面使用的 frame 可為使用者介面的任意部分提供背景。"

# game/tutorial_screen_displayables.rpy:423
translate tchinese window_displayables_7d843f62:

    # e "On the other hand, the window displayable is very specific. It's used to provide the text window. If you're reading what I'm saying, you're looking at the text window right now."
    e "另一方面，window 顯示物件用途很明確，用來提供文字視窗。你正在閱讀我說的話時，看到的就是文字視窗。"

# game/tutorial_screen_displayables.rpy:425
translate tchinese window_displayables_de5963e4:

    # e "Both frames and windows can be given window style properties, allowing you to change things like the background, margins, and padding around the window."
    e "frame 和 window 都能指定 window 樣式屬性，讓你變更背景（background）、視窗周圍的外距（margin）和內距（padding）。"

# game/tutorial_screen_displayables.rpy:433
translate tchinese button_displayables_ea626553:

    # e "One of the most flexible displayables is the button displayable, and its textbutton and imagebutton variants."
    e "最靈活的顯示物件之一是 button，以及 textbutton 和 imagebutton 變體。"

# game/tutorial_screen_displayables.rpy:443
translate tchinese button_displayables_372dcc0f:

    # e "A button is a displayable that when selected runs an action. Buttons can be selected by clicking with the mouse, by touch, or with the keyboard and controller."
    e "按鈕是被選取時會執行 action 的顯示物件。可以用滑鼠點擊、觸控、鍵盤或控制器選取按鈕。"

# game/tutorial_screen_displayables.rpy:445
translate tchinese button_displayables_a6b270ff:

    # e "Actions can do many things, like setting variables, showing screens, jumping to a label, or returning a value. There are many {a=https://www.renpy.org/doc/html/screen_actions.html}actions in the Ren'Py documentation{/a}, and you can also write your own."
    e "動作可以做很多事，例如設定變數、顯示螢幕、跳轉到標籤或傳回值。{a=https://www.renpy.org/doc/html/screen_actions.html}Ren'Py 文件中有許多動作{/a}，你也可以自行撰寫。"

# game/tutorial_screen_displayables.rpy:458
translate tchinese button_displayables_4c600d20:

    # e "It's also possible to run actions when a button gains and loses focus."
    e "按鈕取得或失去焦點時，也可以執行動作。"

# game/tutorial_screen_displayables.rpy:473
translate tchinese button_displayables_47af4bb9:

    # e "A button takes another displayable as children. Since that child can be a layout, it can takes as many children as you want."
    e "按鈕會把另一個顯示物件作為子物件。由於子物件可以是版面，按鈕能包含任意數量的子物件。"

# game/tutorial_screen_displayables.rpy:483
translate tchinese button_displayables_d01adde3:

    # e "In many cases, buttons will be given text. To make that easier, there's the textbutton displayable that takes the text as an argument."
    e "許多情況下，按鈕會包含文字。更簡單的做法是使用以文字作為參數的 textbutton 顯示物件。"

# game/tutorial_screen_displayables.rpy:485
translate tchinese button_displayables_01c551b3:

    # e "Since the textbutton displayable manages the style of the button text for you, it's the kind of button that's used most often in the default GUI."
    e "textbutton 顯示物件會替你管理按鈕文字的樣式，因此是預設 GUI 中最常用的按鈕類型。"

# game/tutorial_screen_displayables.rpy:498
translate tchinese button_displayables_6911fb9b:

    # e "There's also the imagebutton, which takes displayables, one for each state the button can be in, and displays them as the button."
    e "還有 imagebutton，它接收一組顯示物件，每個分別對應一種按鈕狀態，並作為按鈕顯示。"

# game/tutorial_screen_displayables.rpy:500
translate tchinese button_displayables_49720fa6:

    # e "An imagebutton gives you the most control over what a button looks like, but is harder to translate and won't look as good if the game window is resized."
    e "imagebutton 能讓你最大程度控制按鈕外觀，但很難翻譯，遊戲視窗大小改變時效果也可能不好。"

# game/tutorial_screen_displayables.rpy:522
translate tchinese button_displayables_e8d40fc8:

    # e "Buttons take Window style properties, that are used to specify the background, margins, and padding. They also take Button-specific properties, like a sound to play on hover."
    e "按鈕使用 window 樣式屬性指定背景、外距和內距，也使用按鈕專屬屬性，例如滑鼠移上時播放的音效。"

# game/tutorial_screen_displayables.rpy:524
translate tchinese button_displayables_1e40e311:

    # e "When used with a button, style properties can be given prefixes like idle and hover to make the property change with the button state."
    e "和按鈕一起使用時，樣式屬性可以加上 idle、hover 等前綴，讓屬性隨按鈕狀態改變。"

# game/tutorial_screen_displayables.rpy:526
translate tchinese button_displayables_220b020d:

    # e "A text button also takes Text style properties, prefixed with text. These are applied to the text displayable it creates internally."
    e "文字按鈕也使用文字樣式屬性，只要加上 text 前綴，就會套用於它內部建立的文字顯示物件。"

# game/tutorial_screen_displayables.rpy:558
translate tchinese button_displayables_b89d12aa:

    # e "Of course, it's pretty rare we'd ever customize a button in a screen like that. Instead, we'd create custom styles and tell Ren'Py to use them."
    e "當然，我們很少直接在螢幕中自訂按鈕，而是建立自訂樣式並讓 Ren'Py 使用。"

# game/tutorial_screen_displayables.rpy:577
translate tchinese bar_displayables_946746c2:

    # e "The bar and vbar displayables are flexible displayables that show bars representing a value. The value can be static, animated, or adjustable by the player."
    e "bar 和 vbar 顯示物件能靈活呈現代表數值的條。數值可以是靜態、動畫，或由玩家調整。"

# game/tutorial_screen_displayables.rpy:579
translate tchinese bar_displayables_af3a51b8:

    # e "The value property gives a BarValue, which is an object that determines the bar's value and range. Here, a StaticValue sets the range to 100 and the value to 66, making a bar that's two thirds full."
    e "value 屬性提供 BarValue，用來決定數值條的值和範圍。這裡 StaticValue 將範圍設為 100、值設為 66，讓數值條填滿三分之二。"

# game/tutorial_screen_displayables.rpy:581
translate tchinese bar_displayables_62f8b0ab:

    # e "A list of all the BarValues that can be used is found {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}in the Ren'Py documentation{/a}."
    e "所有可用 BarValue 的清單請參閱 {a=https://www.renpy.org/doc/html/screen_actions.html#bar-values}Ren'Py 文件{/a}。"

# game/tutorial_screen_displayables.rpy:583
translate tchinese bar_displayables_5212eb0a:

    # e "In this example, we give the frame the xsize property. If we didn't do that, the bar would expand to fill all available horizontal space."
    e "這個例子為 frame 設定 xsize 屬性。若不這麼做，數值條會擴展填滿所有可用的水平空間。"

# game/tutorial_screen_displayables.rpy:600
translate tchinese bar_displayables_67295018:

    # e "There are a few different bar styles that are defined in the default GUI. The styles are selected by the style property, with the default selected by the value."
    e "預設 GUI 定義了幾種不同的數值條樣式。樣式由 style 屬性選擇，預設會依數值選擇。"

# game/tutorial_screen_displayables.rpy:602
translate tchinese bar_displayables_1b037b21:

    # e "The top style is the 'bar' style. It's used to display values that the player can't adjust, like a life or progress bar."
    e "頂端樣式是 bar，用來顯示玩家無法調整的值，例如生命值或進度。"

# game/tutorial_screen_displayables.rpy:604
translate tchinese bar_displayables_c2aa4725:

    # e "The middle stye is the 'slider' value. It's used for values the player is expected to adjust, like a volume preference."
    e "中間樣式是 slider，用於玩家想調整的值，例如音量偏好設定。"

# game/tutorial_screen_displayables.rpy:606
translate tchinese bar_displayables_2fc44226:

    # e "Finally, the bottom style is the 'scrollbar' style, which is used for horizontal scrollbars. When used as a scrollbar, the thumb in the center changes size to reflect the visible area of a viewport."
    e "最後，底部樣式是 scrollbar，用於水平捲軸。作為捲軸時，中間的小方塊會改變大小來反映檢視區的可見範圍。"

# game/tutorial_screen_displayables.rpy:623
translate tchinese bar_displayables_26eb88bf:

    # e "The vbar displayable is similar to the bar displayable, except it uses vertical styles - 'vbar', 'vslider', and 'vscrollbar' - by default."
    e "vbar 顯示物件類似 bar，但預設使用 vbar、vslider 和 vscrollbar 等垂直樣式。"

# game/tutorial_screen_displayables.rpy:626
translate tchinese bar_displayables_11cf8af2:

    # e "Bars take the Bar style properties, which can customize the look and feel greatly. Just look at the difference between the bar, slider, and scrollbar styles."
    e "數值條使用 bar 樣式屬性，能大幅自訂外觀。看看 bar、slider 和 scrollbar 樣式的差異就知道了。"

# game/tutorial_screen_displayables.rpy:635
translate tchinese imagemap_displayables_d62fad02:

    # e "Imagemaps use two or more images to show buttons and bars. Let me start by showing you an example of an imagemap in action."
    e "imagemap 會使用兩張或更多圖片顯示按鈕和數值條。先看看 imagemap 的實際範例。"

# game/tutorial_screen_displayables.rpy:657
translate tchinese swimming_405542a5:

    # e "You chose swimming."
    e "你選了游泳。"

# game/tutorial_screen_displayables.rpy:659
translate tchinese swimming_264b5873:

    # e "Swimming seems like a lot of fun, but I didn't bring my bathing suit with me."
    e "游泳看起來很有趣，但我沒帶泳衣。"

# game/tutorial_screen_displayables.rpy:665
translate tchinese science_83e5c0cc:

    # e "You chose science."
    e "你選了科學。"

# game/tutorial_screen_displayables.rpy:667
translate tchinese science_319cdf4b:

    # e "I've heard that some schools have a competitive science team, but to me research is something that can't be rushed."
    e "我聽說有些學校有很有競爭力的科學團隊，但對我來說，研究是不能急於求成的事情。"

# game/tutorial_screen_displayables.rpy:672
translate tchinese art_d2a94440:

    # e "You chose art."
    e "你選了藝術。"

# game/tutorial_screen_displayables.rpy:674
translate tchinese art_e6af6f1d:

    # e "Really good background art is hard to make, which is why so many games use filtered photographs. Maybe you can change that."
    e "真正好的背景圖很難創作，所以很多遊戲會使用加上濾鏡的照片。也許你可以改變這點。"

# game/tutorial_screen_displayables.rpy:680
translate tchinese home_373ea9a5:

    # e "You chose to go home."
    e "你選擇回家。"

# game/tutorial_screen_displayables.rpy:686
translate tchinese imagemap_done_48eca0a4:

    # e "Anyway..."
    e "好吧……"

# game/tutorial_screen_displayables.rpy:691
translate tchinese imagemap_done_a60635a1:

    # e "To demonstrate how imagemaps are put together, I'll show you the five images that make up a smaller imagemap."
    e "為了示範 imagemap 如何組合，我來展示組成較小 imagemap 的五張圖片。"

# game/tutorial_screen_displayables.rpy:697
translate tchinese imagemap_done_ac9631ef:

    # e "The idle image is used for the background of the imagemap, for hotspot buttons that aren't focused or selected, and for the empty part of an unfocused bar."
    e "idle 圖片用於 imagemap 背景、未取得焦點或未選取的熱點按鈕，以及未取得焦點的數值條空白部分。"

# game/tutorial_screen_displayables.rpy:703
translate tchinese imagemap_done_123b5924:

    # e "The hover image is used for hotspots that are focused but not selected, and for the empty part of a focused bar."
    e "hover 圖片用於取得焦點但未選取的熱點，以及取得焦點的數值條空白部分。"

# game/tutorial_screen_displayables.rpy:705
translate tchinese imagemap_done_37f538dc:

    # e "Notice how both the bar and button are highlighted in this image. When we display them as part of a screen, only one of them will show up as focused."
    e "注意圖中數值條和按鈕如何高亮。把它們作為螢幕的一部分顯示時，只有其中一個會顯示為取得焦點。"

# game/tutorial_screen_displayables.rpy:711
translate tchinese imagemap_done_c76b072d:

    # e "Selected images like this selected_idle image are used for parts of the bar that are filled, and for selected buttons, like the current screen and a checked checkbox."
    e "selected 圖片（例如 selected_idle）用於數值條的填充部分，以及已選取的按鈕，例如目前的螢幕和勾選方塊。"

# game/tutorial_screen_displayables.rpy:717
translate tchinese imagemap_done_241a4112:

    # e "Here's the selected_hover image. The button here will never be shown, since it will never be marked as selected."
    e "這裡有 selected_hover 圖片。這個按鈕永遠不會顯示，因為它永遠不會被標記為已選取。"

# game/tutorial_screen_displayables.rpy:723
translate tchinese imagemap_done_3d8f454c:

    # e "Finally, an insensitive image can be given, which is used when a hotspot can't be interacted with."
    e "最後，可以提供 insensitive 圖片，在熱點無法互動時使用。"

# game/tutorial_screen_displayables.rpy:728
translate tchinese imagemap_done_ca286729:

    # e "Imagemaps aren't limited to just images. Any displayable can be used where an image is expected."
    e "imagemap 不限於圖片。任何顯示物件都能在需要圖片的地方使用。"

# game/tutorial_screen_displayables.rpy:743
translate tchinese imagemap_done_6060b17f:

    # e "Here's an imagemap built using those five images. Now that it's an imagemap, you can interact with it if you want to."
    e "這是用五張圖片建立的 imagemap。現在它已經是 imagemap，你可以和它互動。"

# game/tutorial_screen_displayables.rpy:755
translate tchinese imagemap_done_c817794d:

    # e "To make this a little more concise, we can replace the five images with the auto property, which replaces '%%s' with 'idle', 'hover', 'selected_idle', 'selected_hover', or 'insensitive' as appropriate."
    e "為了更簡潔，可以使用 auto 屬性取代五張圖片；它會依情況將「%%s」替換為 idle、hover、selected_idle、selected_hover 或 insensitive。"

# game/tutorial_screen_displayables.rpy:757
translate tchinese imagemap_done_c1ed91b8:

    # e "Feel free to omit the selected and insensitive images if your game doesn't need them. Ren'Py will use the idle or hover images to replace them."
    e "遊戲不需要時，可以省略 selected 和 insensitive 圖片。Ren'Py 會使用 idle 或 hover 圖片取代它們。"

# game/tutorial_screen_displayables.rpy:759
translate tchinese imagemap_done_166f75db:

    # e "The hotspot and hotbar statements describe areas of the imagemap that should act as buttons or bars, respectively."
    e "hotspot 和 hotbar 語句分別描述 imagemap 中應作為按鈕或數值條的區域。"

# game/tutorial_screen_displayables.rpy:761
translate tchinese imagemap_done_becb9688:

    # e "Both take the coordinates of the area, in (x, y, width, height) format."
    e "兩者都使用（水平座標、垂直座標、寬度、高度）格式的區域座標。"

# game/tutorial_screen_displayables.rpy:763
translate tchinese imagemap_done_fd56baa2:

    # e "A hotspot takes an action that is run when the hotspot is activated. It can also take actions that are run when it's hovered and unhovered, just like a button can."
    e "hotspot 需要提供熱點啟用時執行的動作，也能像按鈕一樣接收滑鼠移入和移開時執行的動作。"

# game/tutorial_screen_displayables.rpy:765
translate tchinese imagemap_done_5660a6a2:

    # e "A hotbar takes a BarValue object that describes how full the bar is, and the range of values the bar should display, just like a bar and vbar does."
    e "hotbar 接收 BarValue 物件，描述數值條的填充程度和要顯示的值範圍，就像 bar 和 vbar。"

# game/tutorial_screen_displayables.rpy:772
translate tchinese imagemap_done_10496a29:

    # e "A useful pattern is to define a screen with an imagemap that has hotspots that jump to labels, and call that using the call screen statement."
    e "一種實用模式是用 imagemap 定義包含跳轉到標籤之熱點的螢幕，再用 call screen 語句呼叫。"

# game/tutorial_screen_displayables.rpy:774
translate tchinese imagemap_done_dcb45224:

    # e "That's what we did in the school example I showed before. Here's the script for it. It's long, but the imagemap itself is fairly simple."
    e "先前展示的學校範例就是這樣做的。這是腳本，雖然很長，但 imagemap 本身相當簡單。"

# game/tutorial_screen_displayables.rpy:778
translate tchinese imagemap_done_5b5bc5e5:

    # e "Imagemaps have pluses and minuses. On one hand, they are easy for a designer to create, and can look very good. At the same time, they can be hard to translate, and text baked into images may be blurry when the window is scaled."
    e "imagemap 有優點也有缺點。一方面，設計師容易製作，外觀也很好；另一方面，它可能很難翻譯，圖片中的文字也可能因縮放而模糊。"

# game/tutorial_screen_displayables.rpy:780
translate tchinese imagemap_done_b6cebf2b:

    # e "It's up to you and your team to decide if imagemaps are right for your project."
    e "imagemap 是否適合你的專案，由你和團隊決定。"

# game/tutorial_screen_displayables.rpy:787
translate tchinese viewport_displayables_e509d50d:

    # e "Sometimes, you'll want to display something bigger than the screen. That's what the viewport displayable is for."
    e "有時你會想顯示比螢幕更大的內容，這就是 viewport 顯示物件的用途。"

# game/tutorial_screen_displayables.rpy:803
translate tchinese viewport_displayables_9853b0e3:

    # e "Here's an example of a simple viewport, used to display a single image that's far bigger than the screen. Since the viewport will expand to the size of the screen, we use the xysize property to make it smaller."
    e "以下是簡單 viewport 範例，用來顯示遠大於螢幕的單張圖片。由於 viewport 會擴展到螢幕大小，因此使用 xysize 屬性縮小它。"

# game/tutorial_screen_displayables.rpy:805
translate tchinese viewport_displayables_778668c8:

    # e "By default the viewport can't be moved, so we give the draggable, mousewheel, and arrowkeys properties to allow it to be moved in multiple ways."
    e "預設情況下 viewport 無法移動，因此提供 draggable、mousewheel 和 arrowkeys 屬性，允許用多種方式移動。"

# game/tutorial_screen_displayables.rpy:820
translate tchinese viewport_displayables_bbd63377:

    # e "When I give the viewport the edgescroll property, the viewport automatically scrolls when the mouse is near its edges. The two numbers are the size of the edges, and the speed in pixels per second."
    e "為 viewport 設定 edgescroll 屬性後，滑鼠靠近邊緣時 viewport 會自動捲動。這兩個數字是邊緣大小和捲動速度（像素／秒）。"

# game/tutorial_screen_displayables.rpy:839
translate tchinese viewport_displayables_7c4678ee:

    # e "Giving the viewport the scrollbars property surrounds it with scrollbars. The scrollbars property can take 'both', 'horizontal', and 'vertical' as values."
    e "為 viewport 設定 scrollbars 屬性後，viewport 會被捲軸包圍。scrollbars 可以使用 both、horizontal 和 vertical 作為值。"

# game/tutorial_screen_displayables.rpy:841
translate tchinese viewport_displayables_197953b5:

    # e "The spacing property controls the space between the viewport and its scrollbars, in pixels."
    e "spacing 屬性控制 viewport 與捲軸之間的距離（單位：像素）。"

# game/tutorial_screen_displayables.rpy:864
translate tchinese viewport_displayables_54dd6e7b:

    # e "The xinitial and yinitial properties set the initial amount of scrolling, as a fraction of the amount that can be scrolled."
    e "xinitial 和 yinitial 屬性設定初始捲動量，以可捲動量的一小部分表示。"

# game/tutorial_screen_displayables.rpy:885
translate tchinese viewport_displayables_c047efb5:

    # e "Finally, there's the child_size property. To explain what it does, I first have to show you what happens when we don't have it."
    e "最後還有 child_size 屬性。為了解釋它的作用，先看看沒有它時會發生什麼。"

# game/tutorial_screen_displayables.rpy:887
translate tchinese viewport_displayables_c563019f:

    # e "As you can see, the text wraps. That's because Ren'Py is offering it space that isn't big enough."
    e "如你所見，文字會換行，因為 Ren'Py 提供的空間不夠大。"

# game/tutorial_screen_displayables.rpy:909
translate tchinese viewport_displayables_4bcf0ad0:

    # e "When we give the screen a child_size, it offers more space to its children, allowing scrolling. It takes a horizontal and vertical size. If one component is None, it takes the size of the viewport."
    e "為螢幕提供 child_size 後，就能給子物件更多空間並允許捲動。它接收水平和垂直大小，其中一項為 None 時，會使用 viewport 的大小。"

# game/tutorial_screen_displayables.rpy:936
translate tchinese viewport_displayables_ae4ff821:

    # e "Finally, there's the vpgrid displayable. It combines a viewport and a grid into a single displayable, except it's more efficient than either, since it doesn't have to draw every child."
    e "最後是 vpgrid 顯示物件，會將 viewport 和 grid 組合成單一顯示物件；它比兩者更有效率，因為不必繪製每個子物件。"

# game/tutorial_screen_displayables.rpy:938
translate tchinese viewport_displayables_71fa0b8f:

    # e "It takes the cols and rows properties, which give the number of rows and columns of children. If one is omitted, Ren'Py figures it out from the other and the number of children."
    e "它接收 cols 和 rows 屬性，分別指定子物件的欄數和列數。省略其中一項時，Ren'Py 會依另一項和子物件數量計算。"

translate tchinese strings:

    # game/tutorial_screen_displayables.rpy:9
    old "Common properties all displayables share."
    new "所有顯示物件共用的一般屬性。"

    # game/tutorial_screen_displayables.rpy:9
    old "Adding images and other displayables."
    new "加入圖片和其他顯示物件。"

    # game/tutorial_screen_displayables.rpy:9
    old "Text."
    new "文字。"

    # game/tutorial_screen_displayables.rpy:9
    old "Boxes and other layouts."
    new "方盒和其他版面。"

    # game/tutorial_screen_displayables.rpy:9
    old "Windows and frames."
    new "視窗和框架。"

    # game/tutorial_screen_displayables.rpy:9
    old "Buttons."
    new "按鈕。"

    # game/tutorial_screen_displayables.rpy:9
    old "Bars."
    new "數值條。"

    # game/tutorial_screen_displayables.rpy:9
    old "Viewports."
    new "檢視區。"

    # game/tutorial_screen_displayables.rpy:9
    old "Imagemaps."
    new "圖片映射。"

    # game/tutorial_screen_displayables.rpy:9
    old "That's all for now."
    new "目前就這些。"

    # game/tutorial_screen_displayables.rpy:55
    old "This uses position properties."
    new "這使用位置屬性。"

    # game/tutorial_screen_displayables.rpy:63
    old "And the world turned upside down..."
    new "世界顛倒了……"

    # game/tutorial_screen_displayables.rpy:115
    old "Flight pressure in tanks."
    new "平衡飛行壓力。"

    # game/tutorial_screen_displayables.rpy:116
    old "On internal power."
    new "切換內部動力。"

    # game/tutorial_screen_displayables.rpy:117
    old "Launch enabled."
    new "發射準備完成。"

    # game/tutorial_screen_displayables.rpy:118
    old "Liftoff!"
    new "發射！"

    # game/tutorial_screen_displayables.rpy:232
    old "The answer is [answer]."
    new "答案是 [answer]。"

    # game/tutorial_screen_displayables.rpy:244
    old "Text tags {color=#c8ffc8}work{/color} in screens."
    new "文字標籤在螢幕中{color=#c8ffc8}同樣有效{/color}。"

    # game/tutorial_screen_displayables.rpy:336
    old "Bigger"
    new "更大"

    # game/tutorial_screen_displayables.rpy:401
    old "This is a screen."
    new "這是一個螢幕。"

    # game/tutorial_screen_displayables.rpy:402
    old "Okay"
    new "確定"

    # game/tutorial_screen_displayables.rpy:440
    old "You clicked the button."
    new "你點擊了按鈕。"

    # game/tutorial_screen_displayables.rpy:441
    old "Click me."
    new "點我。"

    # game/tutorial_screen_displayables.rpy:453
    old "You hovered the button."
    new "你的滑鼠停在按鈕上。"

    # game/tutorial_screen_displayables.rpy:454
    old "You unhovered the button."
    new "你的滑鼠離開了按鈕。"

    # game/tutorial_screen_displayables.rpy:470
    old "Heal"
    new "治療"

    # game/tutorial_screen_displayables.rpy:479
    old "This is a textbutton."
    new "這是一個文字按鈕。"

    # game/tutorial_screen_displayables.rpy:539
    old "Or me."
    new "或是我。"

    # game/tutorial_screen_displayables.rpy:541
    old "You clicked the other button."
    new "你點擊了另一個按鈕。"

    # game/tutorial_screen_displayables.rpy:880
    old "This text is wider than the viewport."
    new "這段文字比檢視區更寬。"
