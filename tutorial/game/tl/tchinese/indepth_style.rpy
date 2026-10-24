
# game/indepth_style.rpy:40
translate tchinese new_gui_17a0326e:

    # e "When you create a new project, Ren'Py will automatically create a GUI - a Graphical User Interface - for it."
    e "建立新專案時，Ren'Py 會自動為專案建立圖形使用者介面（GUI）。"

# game/indepth_style.rpy:42
translate tchinese new_gui_12c814ed:

    # e "It defines the look of both in-game interface, like this text box, and out-of-game interface like the main and game menus."
    e "它定義遊戲內介面（例如這個文字框）以及遊戲外介面（例如主選單和遊戲選單）的外觀。"

# game/indepth_style.rpy:44
translate tchinese new_gui_0a2a73bb:

    # e "The default GUI is meant to be nice enough for a simple project. With a few small changes, it's what you're seeing in this game."
    e "對簡單專案而言，預設 GUI 已經相當美觀。稍微修改後，就能呈現你在這個遊戲中看到的效果。"

# game/indepth_style.rpy:46
translate tchinese new_gui_22adf68e:

    # e "The GUI is also meant to be easy for an intermediate creator to customize. Customizing the GUI consists of changing the image files in the gui directory, and changing variables in gui.rpy."
    e "預設 GUI 也方便有一定經驗的創作者自訂。自訂 GUI 包括修改 gui 目錄中的圖片檔案，以及修改 gui.rpy 中的變數。"

# game/indepth_style.rpy:48
translate tchinese new_gui_da21de30:

    # e "At the same time, even when customized, the default GUI might be too recognizable for an extremely polished game. That's why we've made it easy to totally replace."
    e "不過，即使經過自訂，預設 GUI 對追求高度打磨的遊戲來說仍可能過於容易辨認。因此我們讓它可以被完全替換。"

# game/indepth_style.rpy:50
translate tchinese new_gui_45765574:

    # e "We've put an extensive guide to customizing the GUI on the Ren'Py website. So if you want to learn more, visit the {a=https://www.renpy.org/doc/html/gui.html}GUI customization guide{/a}."
    e "Ren'Py 網站提供詳盡的 GUI 自訂指南。想了解更多資訊，請參閱 {a=https://www.renpy.org/doc/html/gui.html}GUI 自訂指南{/a}。"

# game/indepth_style.rpy:58
translate tchinese styles_fa345a38:

    # e "Ren'Py has a powerful style system that controls what displayables look like."
    e "Ren'Py 擁有強大的樣式系統，可以控制顯示物件的外觀。"

# game/indepth_style.rpy:60
translate tchinese styles_6189ee12:

    # e "While the default GUI uses variables to provide styles with sensible defaults, if you're replacing the GUI or creating your own screens, you'll need to learn about styles yourself."
    e "預設 GUI 會使用變數為樣式提供合理的預設值；但若要替換 GUI 或建立自己的螢幕，就需要了解樣式。"

# game/indepth_style.rpy:66
translate tchinese styles_menu_a4a6913e:

    # e "What would you like to know about styles?" nointeract
    e "你想了解樣式的哪一方面？" nointeract

# game/indepth_style.rpy:98
translate tchinese style_basics_9a79ef89:

    # e "Styles let a displayable look different from game to game, or even inside the same game."
    e "樣式可以讓顯示物件在不同遊戲中，甚至同一個遊戲的不同位置呈現不同外觀。"

# game/indepth_style.rpy:103
translate tchinese style_basics_48777f2c:

    # e "Both of these buttons use the same displayables. But since different styles have been applied, the buttons look different from each other."
    e "這兩個按鈕使用相同的顯示物件，但套用不同樣式後，外觀各不相同。"

# game/indepth_style.rpy:108
translate tchinese style_basics_57704d8c:

    # e "Styles are a combination of information from four different places."
    e "樣式由來自四個不同地方的資訊組合而成。"

# game/indepth_style.rpy:121
translate tchinese style_basics_144731f6:

    # e "The first place Ren'Py can get style information from is part of a screen. Each displayable created by a screen can take a style name and style properties."
    e "Ren'Py 取得樣式資訊的第一個地方是螢幕的一部分。螢幕建立的每個顯示物件都可以指定樣式名稱和樣式屬性。"

# game/indepth_style.rpy:138
translate tchinese style_basics_67e48162:

    # e "When a screen displayable contains text, style properties prefixed with text_ apply to that text."
    e "螢幕顯示物件包含文字時，以 text_ 開頭的樣式屬性會套用於該文字。"

# game/indepth_style.rpy:151
translate tchinese style_basics_03516b4a:

    # e "The next is as part of a displayable created in an image statement. Style properties are just arguments to the displayable."
    e "第二個地方是 image 語句中建立的顯示物件。樣式屬性就是傳給顯示物件的參數。"

# game/indepth_style.rpy:160
translate tchinese style_basics_ccc0d1ca:

    # egreen "Style properties can also be given as arguments when defining a character."
    egreen "定義人物時，樣式屬性也可以作為參數。"

# game/indepth_style.rpy:162
translate tchinese style_basics_013ab314:

    # egreen "Arguments beginning with who_ are style properties applied to the character's name, while those beginning with what_ are applied to the character's dialogue."
    egreen "以 who_ 開頭的參數是套用於人物名稱的樣式屬性，而以 what_ 開頭的參數則套用於人物對話。"

# game/indepth_style.rpy:164
translate tchinese style_basics_dbe80939:

    # egreen "Style properties that don't have a prefix are also applied to the character's name."
    egreen "沒有前綴的樣式屬性也會套用於人物名稱。"

# game/indepth_style.rpy:174
translate tchinese style_basics_ac6a8414:

    # e "Finally, there is the style statement, which creates or changes a named style. By giving Text the style argument, we tell it to use the blue_text style."
    e "最後是 style 語句，它會建立或修改命名樣式。為 Text 指定 style 參數，就會讓它使用 blue_text 樣式。"

# game/indepth_style.rpy:180
translate tchinese style_basics_3d9bdff7:

    # e "A style property can inherit from a parent. If a style property is not given in a style, it comes from the parent of that style."
    e "樣式屬性可以繼承自父樣式。如果某個樣式沒有指定屬性，就會從父樣式繼承。"

# game/indepth_style.rpy:182
translate tchinese style_basics_49c5fbfe:

    # e "By default the parent of the style has the same name, with the prefix up to the first underscore removed. If the style does not have an underscore in its name, 'default' is used."
    e "預設情況下，父樣式名稱與目前樣式相同，但會移除第一個底線之前的前綴。樣式名稱沒有底線時，會使用 default。"

# game/indepth_style.rpy:184
translate tchinese style_basics_6ab170a3:

    # e "For example, blue_text inherits from text, which in turn inherits from default. The default style defines all properties, so it doesn't inherit from anything."
    e "例如，blue_text 繼承自 text，而 text 又繼承自 default。default 樣式定義所有屬性，因此不繼承任何樣式。"

# game/indepth_style.rpy:190
translate tchinese style_basics_f78117a7:

    # e "The parent can be explicitly changed by giving the style statement an 'is' clause. In this case, we're explictly setting the style to the parent of text."
    e "為 style 語句加入 is 子句，就能明確變更父樣式。這裡我們把樣式的父樣式明確設為 text 的父樣式。"

# game/indepth_style.rpy:194
translate tchinese style_basics_6007040b:

    # e "Each displayable has a default style name. By default, it's usually the lower-case displayable name, like 'text' for Text, or 'button' for buttons."
    e "每個顯示物件都有預設樣式名稱，通常是顯示物件名稱的小寫形式，例如 Text 使用 text，按鈕使用 button。"

# game/indepth_style.rpy:196
translate tchinese style_basics_35db9a05:

    # e "In a screen, a displayable can be given the style_prefix property to give a prefix for that displayable and it's children."
    e "在螢幕中，style_prefix 屬性會為顯示物件及其子物件提供樣式前綴。"

# game/indepth_style.rpy:198
translate tchinese style_basics_422a87f7:

    # e "For example, a text displayable with a style_prefix of 'help' will be given the style 'help_text'."
    e "例如，style_prefix 為 help 的文字顯示物件會使用 help_text 樣式。"

# game/indepth_style.rpy:200
translate tchinese style_basics_bad2e207:

    # e "Lastly, when a displayable is a button, or inside a button, it can take style prefixes."
    e "最後，如果顯示物件本身是按鈕或位於按鈕內部，也可以使用樣式前綴。"

# game/indepth_style.rpy:202
translate tchinese style_basics_22ed20a1:

    # e "The prefixes idle_, hover_, and insensitive_ are used when the button is unfocused, focused, and unfocusable."
    e "按鈕未取得焦點、取得焦點和不可用時，分別使用 idle_、hover_ 和 insensitive_ 前綴。"

# game/indepth_style.rpy:204
translate tchinese style_basics_7a58037e:

    # e "These can be preceded by selected_ to change how the button looks when it represents a selected value or screen."
    e "這些前綴前面還可以加上 selected_，在按鈕表示選取值或螢幕時改變外觀。"

# game/indepth_style.rpy:233
translate tchinese style_basics_0cdcb8c3:

    # e "This screen shows the style prefixes in action. You can click on a button to select it, or click outside to advance."
    e "這個螢幕展示樣式前綴的實際效果。點擊按鈕可以選取它，點擊外部則繼續。"

# game/indepth_style.rpy:240
translate tchinese style_basics_aed05094:

    # e "Those are the basics of styles. If GUI customization isn't enough for you, styles let you customize just about everything in Ren'Py."
    e "這就是樣式的基礎。如果 GUI 自訂仍然不夠，樣式幾乎可以自訂 Ren'Py 中的一切。"

# game/indepth_style.rpy:253
translate tchinese style_general_81f3c8ff:

    # e "The first group of style properties that we'll go over are the general style properties. These work with every displayable, or at least many different ones."
    e "接下來介紹第一組樣式屬性：一般樣式屬性。它們適用於每個顯示物件，至少適用於許多顯示物件。"

# game/indepth_style.rpy:264
translate tchinese style_general_a8d99699:

    # e "Every displayable takes the position properties, which control where it can be placed on screen. Since I've already mentioned them, I won't repeat them here."
    e "每個顯示物件都接受位置屬性，用來控制它在畫面上的位置。前面已經介紹過，這裡不再重複。"

# game/indepth_style.rpy:275
translate tchinese style_general_58d4a18f:

    # e "The xmaximum and ymaximum properties set the maximum width and height of the displayable, respectively. This will cause Ren'Py to shrink things, if possible."
    e "xmaximum 和 ymaximum 屬性分別設定顯示物件的最大寬度和高度；如果可能，Ren'Py 會依此縮小內容。"

# game/indepth_style.rpy:277
translate tchinese style_general_cae9a39f:

    # e "Sometimes, the shrunken size will be smaller than the size given by xmaximum and ymaximum."
    e "有時縮小後的尺寸會小於 xmaximum 和 ymaximum 指定的尺寸。"

# game/indepth_style.rpy:279
translate tchinese style_general_5928c24e:

    # e "Similarly, the xminimum and yminimum properties set the minimum width and height. If the displayable is smaller, Ren'Py will try to make it bigger."
    e "同樣地，xminimum 和 yminimum 屬性設定最小寬度和高度。如果顯示物件太小，Ren'Py 會嘗試放大。"

# game/indepth_style.rpy:289
translate tchinese style_general_35a8ee5e:

    # e "The xsize and ysize properties set the minimum and maximum size to the same value, fixing the size."
    e "xsize 和 ysize 屬性會把最小值和最大值設為相同值，從而固定尺寸。"

# game/indepth_style.rpy:291
translate tchinese style_general_fcfb0640:

    # e "These only works for displayables than can be resized. Some displayables, like images, can't be made bigger or smaller."
    e "這些屬性只適用於可調整大小的顯示物件。有些顯示物件（例如圖片）無法放大或縮小。"

# game/indepth_style.rpy:299
translate tchinese style_general_cd5cc97c:

    # e "The area property takes a tuple - a parenthesis bounded list of four items. The first two give the position, and the second two the size."
    e "area 屬性接收一個元組，也就是以圓括號括起的四項清單。前兩項表示位置，後兩項表示尺寸。"

# game/indepth_style.rpy:308
translate tchinese style_general_e5a58f0b:

    # e "Finally, the alt property changes the text used by self-voicing for the hearing impaired."
    e "最後，alt 屬性會改變自動朗讀提供給使用者的文字。"

# game/indepth_style.rpy:335
translate tchinese style_text_fe457b8f:

    # e "The text style properties apply to text and input displayables."
    e "文字樣式屬性適用於 text 和 input 顯示物件。"

# game/indepth_style.rpy:337
translate tchinese style_text_7ab53f03:

    # e "Text displayables can be created implicitly or explicitly. For example, a textbutton creates a text displayable with a style ending in button_text."
    e "文字顯示物件可以隱式或明確建立。例如，textbutton 會建立樣式名稱以 button_text 結尾的文字顯示物件。"

# game/indepth_style.rpy:339
translate tchinese style_text_6dd42a57:

    # e "These can also be set in gui.rpy by changing or defining variables with names like gui.button_text_size."
    e "也可以在 gui.rpy 中修改或定義名稱類似 gui.button_text_size 的變數來設定這些屬性。"

# game/indepth_style.rpy:347
translate tchinese style_text_c689130e:

    # e "The bold style property makes the text bold. This can be done using an algorithm, rather than a different version of the font."
    e "bold 樣式屬性會讓文字變粗。它可以透過演算法實現，不一定需要另一套字型。"

# game/indepth_style.rpy:355
translate tchinese style_text_3420bfe4:

    # e "The color property changes the color of the text. It takes hex color codes, just like everything else in Ren'Py."
    e "color 屬性會變更文字顏色，接收十六進位色碼，和 Ren'Py 其他部分相同。"

# game/indepth_style.rpy:363
translate tchinese style_text_14bd6327:

    # e "The first_indent style property determines how far the first line is indented."
    e "first_indent 樣式屬性決定第一行縮排的距離。"

# game/indepth_style.rpy:371
translate tchinese style_text_779ac517:

    # e "The font style property changes the font the text uses. Ren'Py takes TrueType and OpenType fonts, and you'll have to include the font file as part of your visual novel."
    e "font 樣式屬性會變更文字使用的字型。Ren'Py 支援 TrueType 和 OpenType 字型，你必須將字型檔案作為視覺小說的一部分提供。"

# game/indepth_style.rpy:379
translate tchinese style_text_917e2bca:

    # e "The size property changes the size of the text."
    e "size 屬性會變更文字大小。"

# game/indepth_style.rpy:388
translate tchinese style_text_1a46cd43:

    # e "The italic property makes the text italic. Again, this is better done with a font, but for short amounts of text Ren'Py can do it for you."
    e "italic 屬性會讓文字變成斜體。同樣地，使用字型通常效果更好，但短文字可以交給 Ren'Py 處理。"

# game/indepth_style.rpy:397
translate tchinese style_text_472f382d:

    # e "The justify property makes the text justified, lining all but the last line up on the left and the right side."
    e "justify 屬性會讓文字左右對齊，使除了最後一行以外的各行同時貼齊左右邊緣。"

# game/indepth_style.rpy:405
translate tchinese style_text_87b075f8:

    # e "The kerning property kerns the text. When it's negative, characters are closer together. When positive, characters are farther apart."
    e "kerning 屬性會調整字距。值為負時字元更靠近，值為正時字元間距更大。"

# game/indepth_style.rpy:415
translate tchinese style_text_fe7dec14:

    # e "The line_leading and line_spacing properties put spacing before each line, and between lines, respectively."
    e "line_leading 和 line_spacing 屬性分別設定每行之前以及各行之間的間距。"

# game/indepth_style.rpy:424
translate tchinese style_text_aee9277a:

    # e "The outlines property puts outlines around text. This takes a list of tuples, which is a bit complicated."
    e "outlines 屬性會在文字周圍繪製外框。它接收元組清單，寫法稍微複雜一些。"

# game/indepth_style.rpy:426
translate tchinese style_text_b4c5190f:

    # e "But if you ignore the brackets and parenthesis, you have the width of the outline, the color, and then horizontal and vertical offsets."
    e "忽略方括號和圓括號後，可以看到其中依序是外框寬度、顏色，以及水平和垂直偏移量。"

# game/indepth_style.rpy:434
translate tchinese style_text_5a0c2c02:

    # e "The rest_indent property controls the indentation of lines after the first one."
    e "rest_indent 屬性控制第一行之後各行的縮排。"

# game/indepth_style.rpy:443
translate tchinese style_text_430c1959:

    # e "The textalign property controls the positioning of multiple lines of text inside the text displayable. For example, 0.5 means centered."
    e "textalign 屬性控制文字顯示物件內多行文字的位置，例如 0.5 表示置中。"

# game/indepth_style.rpy:445
translate tchinese style_text_19aa0833:

    # e "It doesn't change the position of the text displayable itself. For that, you'll often want to set the textalign and xalign to the same value."
    e "它不會改變文字顯示物件本身的位置。要改變物件位置，通常需要把 textalign 和 xalign 設為相同值。"

# game/indepth_style.rpy:455
translate tchinese style_text_efc3c392:

    # e "When both textalign and xalign are set to 1.0, the text is properly right-justified."
    e "當 textalign 和 xalign 都設為 1.0 時，文字就會正確右對齊。"

# game/indepth_style.rpy:464
translate tchinese style_text_43be63b9:

    # e "The underline property underlines the text."
    e "underline 屬性會為文字加上底線。"

# game/indepth_style.rpy:471
translate tchinese style_text_343f6d34:

    # e "Those are the most common text style properties, but not the only ones. Here are a few more that you might need in special circumstances."
    e "這些是最常見的文字樣式屬性，但並不是全部。以下還有一些特殊情況可能會需要的屬性。"

# game/indepth_style.rpy:479
translate tchinese style_text_e7204a95:

    # e "By default, text in Ren'Py is antialiased, to smooth the edges. The antialias property can turn that off, and make the text a little more jagged."
    e "預設情況下，Ren'Py 中的文字會啟用反鋸齒，讓邊緣更平滑。antialias 屬性可以關閉反鋸齒，讓文字邊緣更生硬。"

# game/indepth_style.rpy:487
translate tchinese style_text_a5316e4c:

    # e "The adjust_spacing property is a very subtle one, that only matters when a player resizes the window. When True, characters will be shifted a bit so the Text has the same relative spacing."
    e "adjust_spacing 屬性很細微，只有玩家調整視窗大小時才會影響結果。設為 True 時，字元會略微移動，使 Text 維持相同的相對間距。"

# game/indepth_style.rpy:496
translate tchinese style_text_605d4e4a:

    # e "When False, the text won't jump around as much. But it can be a little wider or narrower based on screen size."
    e "設為 False 時，文字不會跳動得那麼明顯，但寬度可能會隨畫面尺寸略有變化。"

# game/indepth_style.rpy:505
translate tchinese style_text_acf8a0e1:

    # e "The layout property has a few special values that control where lines are broken. The 'nobreak' value disables line breaks entirely, making the text wider."
    e "layout 屬性有幾個特殊值，用來控制換行位置。nobreak 會完全停用換行，使文字變得更寬。"

# game/indepth_style.rpy:516
translate tchinese style_text_785729cf:

    # e "When the layout property is set to 'subtitle', the line breaking algorithm is changed to try to make all lines even in length, as subtitles usually are."
    e "layout 設為 subtitle 時，會改變換行演算法，盡量讓每行長度接近字幕通常的效果。"

# game/indepth_style.rpy:524
translate tchinese style_text_9c26f218:

    # e "The strikethrough property draws a line through the text. It seems pretty unlikely you'd want to use this one."
    e "strikethrough 屬性會在文字中間畫線，一般不太會需要使用它。"

# game/indepth_style.rpy:534
translate tchinese style_text_c7229243:

    # e "The vertical style property places text in a vertical layout. It's meant for Asian languages with special fonts."
    e "vertical 樣式屬性會以直排方式放置文字，主要用於使用特殊字型的亞洲語言。"

# game/indepth_style.rpy:540
translate tchinese style_text_724bd5e0:

    # e "And those are the text style properties. There might be a lot of them, but we want to give you a lot of control over how you present text to your players."
    e "這些就是文字樣式屬性。屬性可能很多，但我們希望讓你充分控制呈現給玩家的文字。"

# game/indepth_style.rpy:580
translate tchinese style_button_300b6af5:

    # e "Next up, we have the window and button style properties. These apply to windows like the text window at the bottom of this screen and frames like the ones we show examples in."
    e "接下來是 window 和 button 樣式屬性，適用於畫面底部的文字視窗，以及範例中的 frame 等視窗。"

# game/indepth_style.rpy:582
translate tchinese style_button_255a18e4:

    # e "These properties also apply to buttons, in-game and out-of-game. To Ren'Py, a button is a window you can click."
    e "這些屬性也適用於遊戲內外的按鈕。對 Ren'Py 來說，按鈕就是可點擊的視窗。"

# game/indepth_style.rpy:593
translate tchinese style_button_9b53ce93:

    # e "I'll start off with this style, which everything will inherit from. To make our lives easier, it inherits from the default style, rather than the customizes buttons in this game's GUI."
    e "先從這個樣式開始，其他內容都會繼承它。為了簡化設定，它繼承 default 樣式，而不是這個遊戲 GUI 中用來自訂按鈕的樣式。"

# game/indepth_style.rpy:595
translate tchinese style_button_aece4a8c:

    # e "The first style property is the background property. It adds a background to the a button or window. Since this is a button, idle and hover variants choose different backgrounds when focused."
    e "第一個樣式屬性是 background，會為按鈕或視窗加入背景。這裡是按鈕，因此 idle 和 hover 狀態會選擇不同背景。"

# game/indepth_style.rpy:597
translate tchinese style_button_b969f04a:

    # e "We also center the two buttons, using the xalign position property."
    e "我們也使用 xalign 位置屬性讓兩個按鈕置中。"

# game/indepth_style.rpy:601
translate tchinese style_button_269ae069:

    # e "We've also customized the style of the button's text, using this style. It centers the text and makes it change color when hovered."
    e "我們也用這個樣式自訂按鈕文字，讓文字置中，並在滑鼠移上去時改變顏色。"

# game/indepth_style.rpy:612
translate tchinese style_button_1009f3e1:

    # e "Without any padding around the text, the button looks odd. Ren'Py has padding properties that add space inside the button's background."
    e "文字周圍沒有內距時，按鈕看起來會很奇怪。Ren'Py 提供 padding 屬性，為按鈕背景內部增加空間。"

# game/indepth_style.rpy:621
translate tchinese style_button_5bdfa45a:

    # e "More commonly used are the xpadding and ypadding style properties, which add the same padding to the left and right, or the top and bottom, respectively."
    e "更常用的是 xpadding 和 ypadding 樣式屬性，分別在左右兩側或上下兩側加入相同的內距。"

# game/indepth_style.rpy:629
translate tchinese style_button_81283d42:

    # e "The margin style properties work the same way, except they add space outside the background. The full set exists: left_margin, right_margin, top_margin, bottom_margin, xmargin, and ymargin."
    e "margin 樣式屬性的運作方式類似，但會在背景外部加入空間。完整屬性包括 left_margin、right_margin、top_margin、bottom_margin、xmargin 和 ymargin。"

# game/indepth_style.rpy:638
translate tchinese style_button_0b7aca6b:

    # e "The size_group style property takes a string. Ren'Py will make sure that all the windows or buttons with the same size_group string are the same size."
    e "size_group 樣式屬性接收字串。Ren'Py 會讓所有使用相同 size_group 字串的視窗或按鈕保持相同大小。"

# game/indepth_style.rpy:647
translate tchinese style_button_4c6da7d9:

    # e "Alternatively, the xfill and yfill style properties make a button take up all available space in the horizontal or vertical directions."
    e "另一種方式是使用 xfill 和 yfill 樣式屬性，讓按鈕在水平方向或垂直方向填滿所有可用空間。"

# game/indepth_style.rpy:657
translate tchinese style_button_fd5338b2:

    # e "The foreground property gives a displayable that is placed on top of the contents and background of the window or button."
    e "foreground 屬性提供一個顯示物件，把它放在視窗或按鈕的內容和背景之上。"

# game/indepth_style.rpy:659
translate tchinese style_button_b8af697c:

    # e "One way to use it is to provide extra decorations to a button that's serving as a checkbox. Another would be to use it with a Frame to provide a glossy shine that overlays the button's contents."
    e "一種用法是給作為核取方塊的按鈕加入額外裝飾。另一種是搭配 Frame，覆蓋按鈕內容並提供光澤效果。"

# game/indepth_style.rpy:668
translate tchinese style_button_c0b1b62e:

    # e "There are also a few style properties that only apply to buttons. The hover_sound and activate_sound properties play sound files when a button is focused and activated, respectively."
    e "還有一些只適用於按鈕的樣式屬性。按鈕取得焦點和啟用時，hover_sound 和 activate_sound 屬性會分別播放音效檔案。"

# game/indepth_style.rpy:677
translate tchinese style_button_02fa647e:

    # e "Finally, the focus_mask property applies to partially transparent buttons. When it's set to True, only areas of the button that aren't transparent cause a button to focus."
    e "最後，focus_mask 屬性適用於部分透明的按鈕。設為 True 時，只有按鈕中不透明的區域會讓它取得焦點。"

# game/indepth_style.rpy:757
translate tchinese style_bar_414d454a:

    # e "To demonstrate styles, let me first show two of the images we'll be using. This is the image we're using for parts of the bar that are empty."
    e "為了示範樣式，先看看要使用的兩張圖片。這是數值條空白部分使用的圖片。"

# game/indepth_style.rpy:761
translate tchinese style_bar_9422b7b0:

    # e "And here's what we use for parts of the bar that are full."
    e "這是數值條填滿部分使用的圖片。"

# game/indepth_style.rpy:773
translate tchinese style_bar_8ae6a14b:

    # e "The left_bar and right_bar style properties, and their hover variants, give displayables for the left and right side of the bar. By default, the value is shown on the left."
    e "left_bar 和 right_bar 樣式屬性及其 hover 變體，分別提供數值條左側和右側的顯示物件。預設值顯示在左側。"

# game/indepth_style.rpy:775
translate tchinese style_bar_7f0f50e5:

    # e "Also by default, both the left and right displayables are rendered at the full width of the bar, and then cropped to the appropriate size."
    e "同樣預設情況下，左右顯示物件會以數值條完整寬度算繪，再裁切成合適尺寸。"

# game/indepth_style.rpy:777
translate tchinese style_bar_9ef4f62f:

    # e "We give the bar the ysize property to set how tall it is. We could also give it xsize to choose how wide, but here it's limited by the width of the frame it's in."
    e "我們為數值條設定 ysize 屬性指定高度，也可以設定 xsize 指定寬度，但這裡的寬度受所在 frame 限制。"

# game/indepth_style.rpy:790
translate tchinese style_bar_d4c29710:

    # e "When the bar_invert style property is True, the bar value is displayed on the right side of the bar. The left_bar and right_bar displayables might also need to be swapped."
    e "bar_invert 屬性為 True 時，數值會顯示在數值條右側，也可能需要交換 left_bar 和 right_bar 顯示物件。"

# game/indepth_style.rpy:804
translate tchinese style_bar_cca67222:

    # e "The bar_resizing style property causes the bar images to be resized to represent the value, rather than being rendered at full size and cropped."
    e "bar_resizing 樣式屬性會調整數值條圖片大小來表示數值，而不是以完整尺寸算繪後再裁切。"

# game/indepth_style.rpy:817
translate tchinese style_bar_7d361bac:

    # e "The thumb style property gives a thumb image, that's placed based on the bars value. In the case of a scrollbar, it's resized if possible."
    e "thumb 樣式屬性提供滑塊圖片，其位置由數值條的值決定。用於捲軸時，如果可能也會調整滑塊大小。"

# game/indepth_style.rpy:819
translate tchinese style_bar_b6dfb61b:

    # e "Here, we use it with the base_bar style property, which sets both bar images to the same displayable."
    e "這裡將它與 base_bar 樣式屬性一起使用，讓兩張數值條圖片使用同一個顯示物件。"

# game/indepth_style.rpy:834
translate tchinese style_bar_996466ad:

    # e "The left_gutter and right_gutter properties set a gutter on the left or right size of the bar. The gutter is space the bar can't be dragged into, that can be used for borders."
    e "left_gutter 和 right_gutter 屬性會在數值條左側或右側設定不可拖曳的邊距，可用來放置邊框。"

# game/indepth_style.rpy:849
translate tchinese style_bar_fa41a83c:

    # e "The bar_vertical style property displays a vertically oriented bar. All of the other properties change names - left_bar becomes top_bar, while right_bar becomes bottom_bar."
    e "bar_vertical 樣式屬性會顯示垂直數值條。其他屬性也會改名：left_bar 變成 top_bar，right_bar 變成 bottom_bar。"

# game/indepth_style.rpy:854
translate tchinese style_bar_5d33c5dc:

    # e "Finally, there's one style we can't show here, and it's unscrollable. It controls what happens when a scrollbar can't be moved at all."
    e "最後還有一個這裡無法示範的樣式：unscrollable。它控制數值條完全無法移動時的行為。"

# game/indepth_style.rpy:856
translate tchinese style_bar_e8e32280:

    # e "By default, it's shown. But if unscrollable is 'insensitive', the bar becomes insensitive. If it's 'hide', the bar is hidden, but still takes up space."
    e "預設會顯示數值條。但 unscrollable 設為 insensitive 時，數值條會變成不可用；設為 hide 時，數值條會隱藏但仍佔用空間。"

# game/indepth_style.rpy:860
translate tchinese style_bar_f1292000:

    # e "That's it for the bar properties. By using them, a creator can customize bars, scrollbars, and sliders."
    e "數值條屬性就介紹到這裡。利用這些屬性，創作者可以自訂數值條、捲軸和滑塊。"

# game/indepth_style.rpy:959
translate tchinese style_box_5fd535f4:

    # e "The hbox displayable is used to lay its children out horizontally. By default, there's no spacing between children, so they run together."
    e "hbox 顯示物件用來水平排列子物件。預設子物件之間沒有間距，因此會連在一起。"

# game/indepth_style.rpy:965
translate tchinese style_box_0111e5dc:

    # e "Similarly, the vbox displayable is used to lay its children out vertically. Both support style properties that control placement."
    e "同樣地，vbox 顯示物件用來垂直排列子物件。兩者都支援控制位置的樣式屬性。"

# game/indepth_style.rpy:970
translate tchinese style_box_5a44717b:

    # e "To make the size of the box displayable obvious, I'll add a highlight to the box itself, and not the frame containing it."
    e "為了清楚展示 box 顯示物件的大小，我會高亮 box 本身，而不是包含它的 frame。"

# game/indepth_style.rpy:978
translate tchinese style_box_239e7a8f:

    # e "Boxes support the xfill and yfill style properties. These properties make a box expand to fill the available space, rather than the space of the largest child."
    e "box 支援 xfill 和 yfill 樣式屬性，讓 box 擴展到填滿可用空間，而不是只佔用最大子物件的大小。"

# game/indepth_style.rpy:988
translate tchinese style_box_e513c946:

    # e "The spacing style property takes a value in pixels, and adds that much spacing between each child of the box."
    e "spacing 樣式屬性接收像素值，在 box 的每個子物件之間加入相應的間距。"

# game/indepth_style.rpy:998
translate tchinese style_box_6ae4f94d:

    # e "The first_spacing style property is similar, but it only adds space between the first and second children. This is useful when the first child is a title that needs different spacing."
    e "first_spacing 樣式屬性類似，但只在第一個和第二個子物件之間加入間距。第一個子物件是需要特殊間距的標題時，這很有用。"

# game/indepth_style.rpy:1008
translate tchinese style_box_0c518d9f:

    # e "The box_reverse style property reverses the order of entries in the box."
    e "box_reverse 樣式屬性會反轉 box 中項目的順序。"

# game/indepth_style.rpy:1021
translate tchinese style_box_f73c1422:

    # e "We'll switch back to a horizontal box for our next example."
    e "下一個例子會切換回水平 box。"

# game/indepth_style.rpy:1031
translate tchinese style_box_285592bb:

    # e "The box_wrap style property fills the box with children until it's full, then starts again on the next line."
    e "box_wrap 樣式屬性會持續向 box 填入子物件，填滿後就在下一行繼續。"

# game/indepth_style.rpy:1044
translate tchinese style_box_a7637552:

    # e "Grids bring with them two more style properties. The xspacing and yspacing properties control spacing in the horizontal and vertical directions, respectively."
    e "Grid 還有兩個樣式屬性。xspacing 和 yspacing 分別控制水平方向和垂直方向的間距。"

# game/indepth_style.rpy:1051
translate tchinese style_box_4006f74b:

    # e "Lastly, we have the fixed layout. The fixed layout usually expands to fill all space, and shows its children from back to front."
    e "最後是 fixed 版面。fixed 通常會擴展到填滿所有空間，並按從後到前的順序顯示子物件。"

# game/indepth_style.rpy:1053
translate tchinese style_box_4a2866f0:

    # e "But of course, we have some style properties that can change that."
    e "當然，也有一些樣式屬性可以改變這種行為。"

# game/indepth_style.rpy:1062
translate tchinese style_box_66e042c4:

    # e "When the xfit style property is True, the fixed lays out all its children as if it was full size, and then shrinks in width to fit them. The yfit style works the same way, but in height."
    e "xfit 樣式屬性為 True 時，fixed 會以完整尺寸排列所有子物件，再縮小寬度以容納它們。yfit 的運作方式相同，但作用於高度。"

# game/indepth_style.rpy:1070
translate tchinese style_box_6a593b10:

    # e "The order_reverse style property changes the order in which the children are shown. Instead of back-to-front, they're displayed front-to-back."
    e "order_reverse 樣式屬性會改變顯示子物件的順序，不再從後到前，而是從前到後。"

# game/indepth_style.rpy:1082
translate tchinese style_inspector_21bc0709:

    # e "Sometimes it's hard to figure out what style is being used for a particular displayable. The displayable inspector can help with that."
    e "有時很難判斷某個顯示物件使用了什麼樣式。顯示物件檢查器可以提供協助。"

# game/indepth_style.rpy:1084
translate tchinese style_inspector_243c50f0:

    # e "To use it, place the mouse over a portion of the Ren'Py user interface, and hit shift+I. That's I for inspector."
    e "要使用檢查器，將滑鼠移到 Ren'Py 使用者介面的一部分上，然後按 Shift+I。這裡的 I 指 inspector（檢查器）。"

# game/indepth_style.rpy:1086
translate tchinese style_inspector_bcbdc396:

    # e "Ren'Py will pop up a list of displayables the mouse is over. Next to each is the name of the style that displayable uses."
    e "Ren'Py 會彈出滑鼠所在位置的顯示物件清單，每個顯示物件旁都會顯示使用的樣式名稱。"

# game/indepth_style.rpy:1088
translate tchinese style_inspector_d981e5c8:

    # e "You can click on the name of the style to see where it gets its properties from."
    e "點擊樣式名稱即可查看它從哪裡繼承屬性。"

# game/indepth_style.rpy:1090
translate tchinese style_inspector_ef46b86d:

    # e "By default, the inspector only shows interface elements like screens, and not images. Type shift+alt+I if you'd like to see images as well."
    e "預設情況下，檢查器只顯示螢幕等介面元素，不顯示圖片。想同時查看圖片，請按 Shift+Alt+I。"

# game/indepth_style.rpy:1092
translate tchinese style_inspector_b59c6b69:

    # e "You can try the inspector right now, by hovering this text and hitting shift+I."
    e "現在可以把滑鼠移到這段文字上並按 Shift+I，試試檢查器。"

translate tchinese strings:

    # game/indepth_style.rpy:20
    old "Button 1"
    new "Button 1"

    # game/indepth_style.rpy:22
    old "Button 2"
    new "Button 2"

    # game/indepth_style.rpy:66
    old "Style basics."
    new "樣式基礎。"

    # game/indepth_style.rpy:66
    old "General style properties."
    new "一般樣式屬性。"

    # game/indepth_style.rpy:66
    old "Text style properties."
    new "Text 樣式屬性。"

    # game/indepth_style.rpy:66
    old "Window and Button style properties."
    new "window 和 button 樣式屬性。"

    # game/indepth_style.rpy:66
    old "Bar style properties."
    new "bar 樣式屬性。"

    # game/indepth_style.rpy:66
    old "Box, Grid, and Fixed style properties."
    new "box、grid 和 fixed 樣式屬性。"

    # game/indepth_style.rpy:66
    old "The Displayable Inspector."
    new "顯示物件檢查器。"

    # game/indepth_style.rpy:66
    old "That's all I want to know."
    new "我只想知道這些。"

    # game/indepth_style.rpy:112
    old "This text is colored green."
    new "這段文字是綠色的。"

    # game/indepth_style.rpy:126
    old "Danger"
    new "危險"

    # game/indepth_style.rpy:142
    old "This text is colored red."
    new "這段文字是紅色的。"

    # game/indepth_style.rpy:170
    old "This text is colored blue."
    new "這段文字是藍色的。"

    # game/indepth_style.rpy:248
    old "Orbiting Earth in the spaceship, I saw how beautiful our planet is.\n–Yuri Gagarin"
    new "當我乘坐太空船繞行地球時，看見我們星球的美麗。\n——尤里・加加林"

    # game/indepth_style.rpy:303
    old "\"Orbiting Earth in the spaceship, I saw how beautiful our planet is.\" Said by Yuri Gagarin."
    new "「當我乘坐太空船繞行地球時，看見我們星球的美麗。」尤里・加加林說。"

    # game/indepth_style.rpy:326
    old "Vertical"
    new "垂直"

    # game/indepth_style.rpy:329
    old "Far better it is to dare mighty things, to win glorious triumphs, even though checkered by failure, than to rank with those poor spirits who neither enjoy nor suffer much, because they live in the gray twilight that knows not victory nor defeat.\n\n–Theodore Roosevelt"
    new "敢於做偉大的事情、贏得光榮的勝利，即使一路伴隨失敗，也遠勝那些既不享受也不受苦、活在不知勝敗的灰色暮光中的怯懦靈魂。\n\n——西奧多・羅斯福"

    # game/indepth_style.rpy:561
    old "Top Choice"
    new "頂端選項"

    # game/indepth_style.rpy:566
    old "Bottom Choice"
    new "底端選項"

    # game/indepth_style.rpy:877
    old "First Child"
    new "第一個子物件"

    # game/indepth_style.rpy:878
    old "Second Child"
    new "第二個子物件"

    # game/indepth_style.rpy:879
    old "Third Child"
    new "第三個子物件"

    # game/indepth_style.rpy:882
    old "Fourth Child"
    new "第四個子物件"

    # game/indepth_style.rpy:883
    old "Fifth Child"
    new "第五個子物件"

    # game/indepth_style.rpy:884
    old "Sixth Child"
    new "第六個子物件"
