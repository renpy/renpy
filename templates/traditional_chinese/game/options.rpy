## 本檔包含部分可用於修改與定制的選項代碼，
## 它將會起作用於您的遊戲之中。 但這只是很多選項中的一部分，
## 您還可以對它進行很多自由的添加與修改。
##
## 以兩個「#」號開頭的行是注釋行，您不應該清除這些注釋。
## 而以單個「#」號開頭的行是反注釋或備用參數，您可以在有必要的時候
## 選擇清除掉這些行
##
## 注釋：Ren'py引擎對空格等符號有著嚴格的要求，並且不能識別Tab定位字元，
## 無論是在此輸入參數，還是今後編輯遊戲腳本時，請務必小心空格的數量，
## 同時不能存在Tab定位字元，否則將會導致整個專案無法啟動！

init -1 python hide:

    ## 此選項可供調整開發者工具的開關，
    ## 在遊戲正式發佈之前，應設定為False，
    ## 以避免使用者使用開發者工具進行遊戲作弊。

    config.developer = True

    ## 此選項控制遊戲視窗的解析度。

    config.screen_width = 800
    config.screen_height = 600

    ## 當Ren'py專案以視窗化運行時，
    ## 此選項控制視窗的標題名稱。
    ## 注釋：需要命名為非英文字元時，需要在雙引號前加「u」以表示Unicode字元，
    ## 但即使命名為英文名稱也不一定需要將「u」去掉。

    config.window_title = u"PROJECT_NAME"

    # 此選項控制遊戲的名稱與版本號，
    # 並將它們回饋至debug工具與日誌中。
    #
    # 注釋：此選項通常針對開發者，SDK主介面的專案名稱、開發過程中的traceback.txt、
    # 編譯時的可執行程式名稱、以及壓縮檔名稱中會有所體現，但與上述視窗標題無關。
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    # 主題

    ## 接著，我們就希望使用到主題功能。 theme.roundrect
    ## 代表著使用圓角矩形特性的主題。
    ##
    ## 主題功能擁有幾個參數
    ## 可使您對主題進行一定的自訂。

    theme.roundrect(

        ## 空閒控制項的顏色。
        ## 注釋：控制項通常體現在按鈕上，此處為滑鼠指標未指向時的顏色。
        widget = "#003c78",

        ## 被指向控制項的顏色。
        widget_hover = "#0050a0",

        ## 控制項內文本顏色。
        widget_text = "#c8ffff",

        ## 被選中控制項內的文本顏色。
        ## 例：當前使用的參數。
        widget_selected = "#ffffc8",

        ## 被遮罩控制項的顏色。
        disabled = "#404040",

        ## 被遮罩控制項內文本的顏色。
        disabled_text = "#c8c8c8",

        ## 資訊框內的文本顏色。
        label = "#ffffff",

        ## 含框架的控制項顏色。
        frame = "#6496c8",

        ## 若設定為True，則遊戲內視窗顯示為圓角。
        ## 若為False，則遊戲內視窗顯示為矩形。
        rounded_window = False,

        ## 主選單的背景。
        ## 此處可以以「#」開頭代表一個顏色，或引用一個檔。
        ## 謹記，圖片檔的解析度要與實際視窗的解析度相同。
        mm_root = "#dcebff",

        ## 遊戲內選單的背景。
        ## 使用方法與注意事項同上。
        gm_root = "#dcebff",

        ## 主題的設定到此結束。
        ## 主題控制著多個可視性效果，若需要修改，
        ## 請參見下方參數。
        )


    #########################################
    ## 此處的設定可允許您修改含有對話或旁白的文字方塊背景。
    ## 通過引用一個檔來修改它。

    ## 文字方塊的背景。 在Frame後的括弧中，兩個數字分別代表
    ## 左右邊距和上下邊距。

    # style.window.background = Frame("frame.png", 12, 12)

    ## 留邊參數用於設定文字方塊視窗周圍的空白部分。
    ## 這些部分將不會覆蓋背景圖。
    ## 注釋：如數值越大，則文字方塊周圍的空白越多，文字方塊本身越小，
    ## 但這僅限於文字方塊圖形本身，文字不受此參數影響。

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## 填充參數是文字方塊視窗內的空白部分。
    ## 注釋：與上一個參數作用正好相反，
    ## 它會影響文字方塊內文字的顯示範圍。

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## 此參數控制視窗最低高度，並包含留邊與填充參數。

    # style.window.yminimum = 250


    #########################################
    ## 此處參數可使您修改主選單放置的位置。

    ## 此參數的原理是在視覺化元素內尋找一個定位點(anchor)，
    ## 以及在遊戲螢幕上尋找一個位置點(pos)。
    ## 接著我們會將兩個點進行重合。
    ##
    ## 注釋：視覺化元素內的定位點可假想為一個圖片中指定的點，
    ## 當pos參數指定一個遊戲視窗內的位置（點）後，
    ## 引擎便會將圖片中指定的點與視窗中指定好的點進行重合放置。
    ## 預設情況下，兩軸的anchor都為0.5時，定位點位於視覺化元素中心。

    ## 定位點與位置點均可使用整數或小數表達。
    ## 如果設定為整數，則會被理解為距離左上角的圖元數量。
    ## 如果設定為小數，則會被理解為遊戲視窗分數化的位置。
    ##
    ## 注釋：分數化位置不難理解，如0.5，則代表遊戲視窗的二分之一處，
    ## 此時xy兩軸依舊有效。

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## 此處可修改Ren'py遊戲內的預設字型。

    ## 引用一個字體檔。

    style.default.font = "tl/None/DroidSansFallback.ttf"
    style._default.font = "tl/None/DroidSansFallback.ttf"

    ## 修改字體大小。

    # style.default.size = 22

    ## 注意此參數僅能修改部分字體的大小，
    ## 一些按鈕擁有它們自己的風格參數。


    #########################################
    ## 此參數可使您修改Ren'py遊戲內使用的一些聲音。

    ## 若為False，您的遊戲內將不會包含任何聲音效果。

    config.has_sound = True

    ## 若您的遊戲內不包含任何音樂，請設定為False。

    config.has_music = True

    ## 若您的遊戲含有人物語音，請設定為True。

    config.has_voice = False

    ## 設定在您點擊按鈕和圖片映射時的效果音。

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## 設定在您進入和退出遊戲內選單時的聲音效果。

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## 設定一個聲音用於測試音量大小。

    # config.sample_sound = "click.wav"

    ## 設定使用者位於主選單時的音樂。

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## 説明

    ## 此參數可讓您控制Ren'py遊戲內的「説明」選項。
    ## 它可以是：
    ## - 腳本中的一個label，用於在點擊後向使用者顯示一段説明。
    ## - 遊戲根目錄下的一個檔，點擊後將會打開網頁瀏覽器。
    ## - 若為None，則關閉此功能。
    ##
    ## 注釋：label通常用於遊戲劇情腳本，如script.rpy中，label start:
    ## 指的就是點擊開始遊戲時指向的label。 label中可包含對話、旁白、
    ## 選項、背景、聲音等參數。
    config.help = "README.html"


    #########################################
    ## 過渡特效

    ## 從遊戲中進入遊戲內選單時的過渡特效。
    config.enter_transition = None

    ## 退出選單回到遊戲時的過渡特效。
    config.exit_transition = None

    ## 在遊戲選單內進行切換時的過渡特效。
    config.intra_transition = None

    ## 從主選單進入遊戲內選單時的過渡特效。
    config.main_game_transition = None

    ## 退出選單回到主選單時的過渡特效。
    config.game_main_transition = None

    ## 從封面進入主選單時的過渡特效。
    ## 注釋：封面(splashscreen)指的是打開遊戲時
    ## 先看到的一些發行商圖片或遊戲宣傳視頻等。
    ## 封面需要另外添加代碼實現，請參見官方文檔。
    config.end_splash_transition = None

    ## 當遊戲結束時返回主選單的過渡特效。
    config.end_game_transition = None

    ## 當一個進度被載入時的過渡特效。
    config.after_load_transition = None

    ## 當一個遊戲內視窗顯示時的過渡特效。
    ## 注釋：遊戲內視窗多指文字方塊。
    config.window_show_transition = None

    ## 當一個遊戲內視窗被隱藏時的過渡特效。
    config.window_hide_transition = None

    ## 當顯示完ADV-mode下的文本後直接轉為NVL-mode文本時的過渡特效。
    ## 注釋：ADV-mode是指文本位於螢幕底部文字方塊中的遊戲模式，
    ## NVL-mode是指文本全屏顯示的遊戲模式。
    config.adv_nvl_transition = dissolve

    ## 當顯示完NVL-mode的文本後直接轉為ADV-mode文本時的過渡特效。
    config.nvl_adv_transition = dissolve

    ## 當確認取消按鈕出現時的過渡特效。
    config.enter_yesno_transition = None

    ## 當確認取消按鈕隱藏時的過渡特效
    config.exit_yesno_transition = None

    ## 當進入重播時的過渡特效。
    config.enter_replay_transition = None

    ## 當退出重播時的過渡特效。
    config.exit_replay_transition = None

    ## 當圖像被say參數附帶屬性進行修改時的過渡特效。
    config.say_attribute_transition = None

    #########################################
    ## 此處可使您修改遊戲存檔資料存放的目錄。
    ## 這需要在遊戲開發之初，在任何init代碼都未被運行之前就進行設定，
    ## 以便在init中找到正確的持久性資料資訊。
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## 設定中的預設選項。

    ## 注意：這些選項僅會在第一次運行遊戲時生效。
    ## 若需要再生效一次，請刪除：
    ## game/saves/persistent

    ## 是否開啟全螢幕模式？

    config.default_fullscreen = False

    ## 預設的每秒顯示文字數量，0為無限。

    config.default_text_cps = 0

    ## 預設的自動閱讀模式等待時間。

    config.default_afm_time = 10

    ## 預設開啟換行後保持語音播放功能。

    config.default_voice_sustain = True

    #########################################
    ## 您可以從此處開始進行更多的自訂設定。
    ## 注釋：以下為範本原文的追加代碼。

    ## 此選項可讓您使用滑鼠滾輪閱讀劇情。
    # config.keymap['dismiss'].append('mousedown_5')

    ## Windows 用標題列圖示設定。
    ## 圖像尺寸必須為 32x32 。
    # config.windows_icon = "image/head.png"

    ## 圖像快取最高值設定。
    ## 數量過高有可能導致遊戲崩潰。
    # config.image_cache_size = 8

    ## 設定跳過文字功能。
    ## 無法停止暫時性跳過時，請設定為None。
    # config.allow_skipping = True

    ## 設定跳過文字的延遲時間。
    # config.skip_delay = 25

    ## 是否允許非開發者通過>鍵使用快速略過模式。
    ## 注釋：快速略過模式非常快，所有未讀文字也將被略過。
    # config.fast_skipping = False

    ## 設定文字回滾功能。
    ## 若需要持續回滾劇情，請使用renpy.block_rollback()。
    ## hard_rollback_limit 參數記錄回滾的行數。
    # config.rollback_enabled = True
    # config.hard_rollback_limit = 500

    ## 修改存檔位的縮略圖解析度。
    # config.thumbnail_height = 75
    # config.thumbnail_width = 100

    ## 若角色圖片檔使用image命令顯示時，
    ## 若此參數設定為True，則角色圖像僅以側邊圖(side image)
    ## 形式呈現。
    # config.side_image_only_not_showing = False

    ## 預設圖層。
    # config.layers = [ 'master', 'transient', 'screens', 'overlay' ]

    ## 添加最上方圖層。
    ## 此圖層不受過渡特效影響。
    # config.top_layers = [ ]

    ## 回滾劇情時使用NVL-mode。
    # config.nvl_paged_rollback = True

    ## 選項出現時使用NVL-mode。
    # menu = nvl_menu

    ## 設定是否允許通過滑鼠拖拽改變視窗大小。
    # config.gl_resize = False

    ## 遊戲啟動時視窗居中。
    # import os
    # os.environ['SDL_VIDEO_CENTERED'] = '1'

    ## 設定音樂預設的淡化(fade)時間。
    # config.fade_music = 0.0

    ## 定義一個角色語音存放的資料夾，在腳本中可以直接進行調用。
    ## 定義以後，您只需輸入音訊的檔案名即可播放音訊。
    # config.auto_voice = "voice/{filename}.ogg"
    # config.voice_filename_format = "{filename}.ogg"

    ## 預設聲音通道。
    ## file_prefix中填入路徑，file_suffix中填入尾碼名，
    ## 即可實現僅需輸入檔案名就能重播聲音。
    # renpy.music.register_channel("music", mixer="music" loop = True, file_prefix="", file_suffix="")
    # renpy.music.register_channel("sound", mixer="sfx", loop = False, file_prefix="", file_suffix="")
    # renpy.music.register_channel("voice", mixer="voice", loop = False, file_prefix="", file_suffix="")

    ## 按鍵連按參數。
    ## (.3,.03)的情況下，按住按鍵.3秒後，將會以.03秒為間隔自動連按。
    # config.key_repeat = (.3, .03)


## 此區域控制您將如何產生一個釋出版本程式。

init python:

    ## 此參數用於修改發行版本壓縮檔與資料夾的名稱。
    ## 假如設定為「mygame-1.0」，則將會在產生Windows釋出版本時自動將遊戲放置在
    ## 「mygame-1.0-win」資料夾下，並產生mygame-1.0-win.zip的壓縮檔。
    ## 產生其他平臺的釋出版本時除「win」字元以外其他依舊沿用此處設定。
    build.directory_name = "HANA-Build-1.0"

    ## 遊戲可執行程式的檔案名。
    ## 例如設定為「mygame」時，則產生發行版本後，
    ## 其遊戲目錄下可執行檔的檔案名將會為「mygame.exe」，
    build.executable_name = "SHIRAYUKI"

    ## 如果設定為True，則此Ren'py遊戲將包含升級資訊，
    ## 使其允許升級程式運行。
    build.include_update = False

    ## 檔案模式：

    ## 以下功能稱作檔案模式，檔案模式對大小寫並不敏感，
    ## 並且將「/」用於表示目錄的分層。
    ## 若存在多個檔案模式，則優先使用第一個。

    ## 在檔案模式中：

    ## /
    ## 這是一個目錄的分隔符號。

    ## *
    ## 代表所有字元，除目錄分隔符號以外。

    ## **
    ## 代表所有字元，包括目錄分隔符號。

    ## 例如：

    ## *.txt
    ## 代表遊戲根目錄下的所有txt檔。

    ## game/**.ogg
    ## 代表game資料夾下及其所有子資料夾中的ogg檔。

    ## **.psd
    ## 代表專案中所有地方的psd檔。

    ## 定義為None的檔將不會被包含在分佈版中。

    build.classify('**~', None)
    # build.classify('**.bak', None)
    # build.classify('**/.**', None)
    build.classify('**/#**', None)
    build.classify('**/thumbs.db', None)

    ## 此處用於定義遊戲資源封裝的名稱。
    ## 注釋：您需要預先在此處預先定義封裝的名稱後，
    ## 才能在下一個參數中設定使用對應名稱的封裝。
    # build.archive('script', 'all')
    # build.archive('image', 'all')
    # build.archive('bg', 'all')
    # build.archive('voice', 'all')
    # build.archive('char', 'all')
    # build.archive('sound', 'all')
    # build.archive('data', 'all')

    ## 若要將遊戲資源檔封裝，
    ## 請將它們定義為「archive」。
    ## 注釋：此處用於定義需要放進封裝的遊戲資源檔案清單，需要事先定義。
    ## 同時，在上方定義好archive的名稱後，可以在下方直接使用自訂名稱。
    # build.classify('game/*.rpy', 'script')
    # build.classify('game/*.rpyc', 'script')
    # build.classify('game/*.rpyb', 'script')
    # build.classify('game/bg/*.png', 'image')
    # build.classify('game/char/*.png', 'image')
    # build.classify('game/image/*.png', 'image')
    # build.classify('game/voice/*.ogg', 'voice')
    # build.classify('game/sound/*.ogg', 'sound')
    # build.classify('game/data/**.*', 'data')
    # build.classify('game/data/mask/**.*', 'data')

    ## 符合documentation樣式的檔，
    ## 在mac用分發版中同時包含在app與zip中。

    build.documentation('*.html')
    build.documentation('*.txt')

    ## 定義一整個資料夾的圖像，在腳本中可直接使用檔案名進行調用，
    ## 避免單個檔定義的繁瑣步驟。
    ## 注釋：詳細使用方法請參閱官方文檔。
    # config.automatic_images = [ '/' ]
    # config.automatic_images_strip = [ '/' ]

    ## 打開行動平臺上的視頻硬體加速，提升視頻播放效能。
    ## 理論上絕大多數平臺支援硬體加速功能。
    # config.hw_video = True

    ## 打開選擇肢自動封存功能，存檔將會放到Q.Save位置。
    # config.autosave_on_choice = True
