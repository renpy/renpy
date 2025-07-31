# TODO: Translation updated at 2025-07-03 12:39

translate persian strings:

    # gui/game/screens.rpy:9
    old "## Styles"
    new "## Style hā"

    # gui/game/screens.rpy:81
    old "## In-game screens"
    new "## Menu hā-ye darun-e bāzi"

    # gui/game/screens.rpy:85
    old "## Say screen"
    new "## Safhe-ye goftār"

    # gui/game/screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Safhe-ye goftār barā-ye namāyeš-e diālog be bāzigar estefāde mišavad. In safhe do pārāmetr-e who va what rā migirad, ke be tartib nām-e šaxsiyat-e dar hāl-e sohbat va matn-e namāyeš dāde mišavad hastand. (pārāmetr-e who dar surat-e adam-e zekr-e nām mitavānad None bāšad.)"

    # gui/game/screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## In safhe bāyad yek displayable-e matni bā šenāse-ye \"what\" besāzad, čerā ke Ren'Py az in barā-ye modiriyat-e namāyeš-e matn estefāde mikonad. In safhe hamčenin mitavānad displayable hāyi bā šenāse hā-ye \"who\" va \"window\" barā-ye e'māl-e vižegi hā-ye style besāzad."

    # gui/game/screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # gui/game/screens.rpy:113
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Agar tasvir-e kenāri vojud dāšte bāšad, bālā-ye matn namāyeš bede. Dar hālat-e guši namāyeš nade, zirā fazā-ye kāfi nist."

    # gui/game/screens.rpy:119
    old "## Make the namebox available for styling through the Character object."
    new "## Ja'be-ye nām rā barā-ye style kardan az tariq-e šey'e Character mojud bekon."

    # gui/game/screens.rpy:164
    old "## Input screen"
    new "## Safhe-ye vorudi"

    # gui/game/screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## In safhe barā-ye namāyeš-e renpy.input estefāde mišavad. Pārāmetr-e prompt barā-ye ersāl-e yek darxāst-e matn estefāde mišavad."

    # gui/game/screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## In safhe bāyad yek displayable-e vorudi bā šenāse-ye \"input\" barā-ye daryāft-e pārāmetr hā-ye vorudi-ye moxtalef besāzad."

    # gui/game/screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:199
    old "## Choice screen"
    new "## Safhe-ye entexāb"

    # gui/game/screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## In safhe barā-ye namāyeš-e entexāb hā-ye darun-e bāzi-ye erā'e šode tavassot-e gozāre-ye menu estefāde mišavad. Tanhā pārāmetr-e ān, items, yek list az ašiyā' ast, ke har kodām dārā-ye xāne hā-ye onvān va amal hastand."

    # gui/game/screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:233
    old "## Quick Menu screen"
    new "## Safhe-ye menu-ye sari'"

    # gui/game/screens.rpy:235
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Menu-ye sari' dāxel-e bāzi barā-ye farāham kardan-e dastresi-ye sari' be menu hā-ye birun-e bāzi namāyeš dāde mišavad."

    # gui/game/screens.rpy:240
    old "## Ensure this appears on top of other screens."
    new "## Motma'en sāxtan az inke in bar ru-ye safahāt-e digar zāher bešavad."

    # gui/game/screens.rpy:251
    old "Back"
    new "عقب"

    # gui/game/screens.rpy:252
    old "History"
    new "تاریخچه"

    # gui/game/screens.rpy:253
    old "Skip"
    new "رد کردن"

    # gui/game/screens.rpy:254
    old "Auto"
    new "اتوماتیک"

    # gui/game/screens.rpy:255
    old "Save"
    new "ذخیره"

    # gui/game/screens.rpy:256
    old "Q.Save"
    new "ذخیرۀ سریع"

    # gui/game/screens.rpy:257
    old "Q.Load"
    new "بارگذاری سریع"

    # gui/game/screens.rpy:258
    old "Prefs"
    new "ترجیحات"

    # gui/game/screens.rpy:261
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## In code az namāyeš dāde šodan-e safhe-ye quick_menu dāxel-e bāzi hengāmi ke bāzigar sarihan rābet rā penhān nakarde ast motma'en misāzad."

    # gui/game/screens.rpy:279
    old "## Main and Game Menu Screens"
    new "## Safhe hā-ye menu-ye asli va bāzi"

    # gui/game/screens.rpy:282
    old "## Navigation screen"
    new "## Safhe-ye peymāyeš"

    # gui/game/screens.rpy:284
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## In safhe dar menu hā-ye asli va bāzi vojud dāšte, va peymāyeš be menu hā-ye digar, va šoru'-e bāzi rā farāham mikonad."

    # gui/game/screens.rpy:299
    old "Start"
    new "شروع"

    # gui/game/screens.rpy:307
    old "Load"
    new "بارگذاری"

    # gui/game/screens.rpy:309
    old "Preferences"
    new "ترجیحات"

    # gui/game/screens.rpy:313
    old "End Replay"
    new "پایان بازپخش"

    # gui/game/screens.rpy:317
    old "Main Menu"
    new "منوی اصلی"

    # gui/game/screens.rpy:319
    old "About"
    new "درباره"

    # gui/game/screens.rpy:323
    old "## Help isn't necessary or relevant to mobile devices."
    new "## Komak barā-ye dastgāh hā-ye hamrāh elzāmi va yā be ān hā mortabet nist."

    # gui/game/screens.rpy:324
    old "Help"
    new "کمک"

    # gui/game/screens.rpy:328
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## Dokme-ye xoruj dar iOS mamnu' šode va dar Android va Web elzāmi nist."

    # gui/game/screens.rpy:329
    old "Quit"
    new "خروج"

    # gui/game/screens.rpy:343
    old "## Main Menu screen"
    new "## Safhe-ye menu-ye asli"

    # gui/game/screens.rpy:345
    old "## Used to display the main menu when Ren'Py starts."
    new "## Barā-ye namāyeš-e menu-ye asli hengām-e šoru'-e Ren'Py estefāde mišavad."

    # gui/game/screens.rpy:347
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:351
    old "## This ensures that any other menu screen is replaced."
    new "## In az jāygozini-ye har menu-ye digar motma'en misāzad."

    # gui/game/screens.rpy:356
    old "## This empty frame darkens the main menu."
    new "## In qāb-e xāli menu-ye asli rā tiretar mikonad."

    # gui/game/screens.rpy:360
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## Gozāre-ye use yek safhe-ye digar rā dāxel-e in safhe šāmel mikonad. Xod-e mohtaviyāt-e menu-ye asli dar safhe-ye peymāyeš qarār dārand."

    # gui/game/screens.rpy:405
    old "## Game Menu screen"
    new "## Safhe-ye menu-ye bāzi"

    # gui/game/screens.rpy:407
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## In sāxtār-e bonyādi-ye omumi-ye safhe-ye menu-ye bāzi rā mičinad. In bā titr-e safhe farāxāni mišavad, va paszamine, titr, va peymāyeš rā namāyeš midahad."

    # gui/game/screens.rpy:410
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Pārāmetr-e scroll mitavānad None, va yā yeki az \"viewport\" yā \"vpgrid\" bāšad. In safhe barā-ye estefāde bā yek yā čand farzand, ke dar ān tarāgonjānide (qarār gerefte) šode ast dar nazar gerefte šode ast."

    # gui/game/screens.rpy:428
    old "## Reserve space for the navigation section."
    new "## Fazā-ye reserve šode barā-ye baxš-e hedāyati."

    # gui/game/screens.rpy:474
    old "Return"
    new "برگشت"

    # gui/game/screens.rpy:537
    old "## About screen"
    new "## Safhe-ye darbāre"

    # gui/game/screens.rpy:539
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## In safhe ettelā'āt-e e'tebār hā (credit) va haqq-e taksir-e (copyright) marbut be bāzi va Ren'Py rā namāyeš midahad."

    # gui/game/screens.rpy:542
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## Hič čiz-e xāssi darbāre-ye in safhe vojud nadārad, va az in ru in safhe yek mesāl az čegunegi-ye sāxt-e yek safhe-ye šaxtisāzi šode ast."

    # gui/game/screens.rpy:549
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Gozāre-ye use šāmel-e safhe-ye game_menu-ye dāxel-e in mišavad. Farzand-e vbox pas az in dar viewport-e dāxel-e safhe-ye game_menu šāmel mišavad."

    # gui/game/screens.rpy:559
    old "Version [config.version!t]\n"
    new "نسخۀ [config.version!t]\n"

    # gui/game/screens.rpy:561
    old "## gui.about is usually set in options.rpy."
    new "## gui.about ma'mulan dar options.rpy tanzim mišavad."

    # gui/game/screens.rpy:565
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "ساخته شده با {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # gui/game/screens.rpy:576
    old "## Load and Save screens"
    new "## Safahāt-e bārgozāri vā zaxire"

    # gui/game/screens.rpy:578
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## In safahāt be bāzigar emkān-e zaxire va bārgozāri-ye mojaddad-e bāzi rā midahand. Az ānjāyi ke taqriban hame čizešan moštarak ast, har do be surat-e yek safhe-ye sevvom, file_slots, piyādesāzi mišavand."

    # gui/game/screens.rpy:582
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # gui/game/screens.rpy:601
    old "Page {}"
    new "صفحۀ {}"

    # gui/game/screens.rpy:601
    old "Automatic saves"
    new "ذخیره‌های خودکار"

    # gui/game/screens.rpy:601
    old "Quick saves"
    new "ذخیره‌های سریع"

    # gui/game/screens.rpy:607
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## In az gereftan-e ruydād-e vorud tavassot-e vorudi qabl az har yek az dokme hā motma'en misāzad."

    # gui/game/screens.rpy:611
    old "## The page name, which can be edited by clicking on a button."
    new "## Nām-e safhe, ke mitavānad bā click kardan bar ru-ye yek dokme taqir dāde šavad."

    # gui/game/screens.rpy:623
    old "## The grid of file slots."
    new "## Šabake-ye xāne hā-ye file hā."

    # gui/game/screens.rpy:643
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %d %B %Y, %H:%M"

    # gui/game/screens.rpy:643
    old "empty slot"
    new "خانۀ خالی"

    # gui/game/screens.rpy:651
    old "## Buttons to access other pages."
    new "## Dokme hāyi barā-ye dastresi be safahāt-e digar."

    # gui/game/screens.rpy:663
    old "<"
    new "<"

    # gui/game/screens.rpy:667
    old "{#auto_page}A"
    new "{#auto_page}A"

    # gui/game/screens.rpy:670
    old "{#quick_page}Q"
    new "{#quick_page}Q"

    # gui/game/screens.rpy:672
    old "## range(1, 10) gives the numbers from 1 to 9."
    new "## range(1, 10) a'dād-e 1 tā 9 rā midahad."

    # gui/game/screens.rpy:676
    old ">"
    new ">"

    # gui/game/screens.rpy:681
    old "Upload Sync"
    new "آپلود همگام‌سازی"

    # gui/game/screens.rpy:685
    old "Download Sync"
    new "دانلود همگام‌سازی"

    # gui/game/screens.rpy:722
    old "## Preferences screen"
    new "## Safhe-ye tarjihāt"

    # gui/game/screens.rpy:724
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Safhe-ye tarjihāt be bāzigar in emkan rā midahad ke bāzi rā towri tanzim konad barāyaš monāsebtar bāšad."

    # gui/game/screens.rpy:727
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # gui/game/screens.rpy:744
    old "Display"
    new "نمایش"

    # gui/game/screens.rpy:745
    old "Window"
    new "پنجره"

    # gui/game/screens.rpy:746
    old "Fullscreen"
    new "تمام‌صفحه"

    # gui/game/screens.rpy:751
    old "Unseen Text"
    new "متن نادیده"

    # gui/game/screens.rpy:752
    old "After Choices"
    new "پس‌انتخاب‌ها"

    # gui/game/screens.rpy:753
    old "Transitions"
    new "گذارها"

    # gui/game/screens.rpy:755
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## vbox hā-ye bištar az no'-e \"radio_pref\" yā \"check_pref\" rā mitavān barā-ye ezāfe kardan-e tarjihāt-e ta'rif šode tavassot-e sāzande-ye bištar injā ezāfe kard."

    # gui/game/screens.rpy:766
    old "Text Speed"
    new "سرعت متن"

    # gui/game/screens.rpy:770
    old "Auto-Forward Time"
    new "زمان عبور خودکار"

    # gui/game/screens.rpy:777
    old "Music Volume"
    new "بلندی موسیقی"

    # gui/game/screens.rpy:784
    old "Sound Volume"
    new "بلندی صوت"

    # gui/game/screens.rpy:790
    old "Test"
    new "تست"

    # gui/game/screens.rpy:794
    old "Voice Volume"
    new "بلندی گفتار"

    # gui/game/screens.rpy:805
    old "Mute All"
    new "بی‌صدا کردن همه"

    # gui/game/screens.rpy:881
    old "## History screen"
    new "## Safhe-ye tārixče"

    # gui/game/screens.rpy:883
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## In safheyi ast ke tārixče-ye diālog rā be bāzigar namāyeš midahad. Agar če hič čiz-e xāssi darbāre-ye in safhe vojud nadārad, in safhe bāyad be tārixče-ye diālog-e zaxire šode dar _history_list dastresi dāšte bāšad."

    # gui/game/screens.rpy:887
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # gui/game/screens.rpy:893
    old "## Avoid predicting this screen, as it can be very large."
    new "## Jelowgiri az pišbini-ye in safhe, čerā ke besiyār bozorg mitavānad bāšad."

    # gui/game/screens.rpy:904
    old "## This lays things out properly if history_height is None."
    new "## In dar surati ke history_height None bāšad, be dorosti hame čiz rā mičinad."

    # gui/game/screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## Rang-e matn-e who rā, dar surāti ke tanzim šode bāšad, az Character begir."

    # gui/game/screens.rpy:923
    old "The dialogue history is empty."
    new "تاریخچۀ دیالوگ خالی است."

    # gui/game/screens.rpy:926
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## In ta'in mikonad če tag hāyi rā mitavān dar safhe-ye tārixče namāyeš dād."

    # gui/game/screens.rpy:971
    old "## Help screen"
    new "## Safhe-ye komak"

    # gui/game/screens.rpy:973
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## Safheyi ke dar mowred-e kelidbandi vā tanzimāt-e mušvāre ettelā'āt midahad. In az safahāt-e digar (keyboard_help, mouse_help, and gamepad_help) barā-ye namāyeš-e xod-e komak estefāde mikonad."

    # gui/game/screens.rpy:992
    old "Keyboard"
    new "صفحه‌کلید"

    # gui/game/screens.rpy:993
    old "Mouse"
    new "موشواره"

    # gui/game/screens.rpy:996
    old "Gamepad"
    new "دستۀ بازی"

    # gui/game/screens.rpy:1009
    old "Enter"
    new "Enter"

    # gui/game/screens.rpy:1010
    old "Advances dialogue and activates the interface."
    new "دیالوگ را پیش می‌برد و رابط را فعال می‌کند."

    # gui/game/screens.rpy:1013
    old "Space"
    new "Space"

    # gui/game/screens.rpy:1014
    old "Advances dialogue without selecting choices."
    new "دیالوگ را بدون انتخاب گزینه‌ها پیش می‌برد."

    # gui/game/screens.rpy:1017
    old "Arrow Keys"
    new "کلیدهای فلش‌ها"

    # gui/game/screens.rpy:1018
    old "Navigate the interface."
    new "پیمایش رابط"

    # gui/game/screens.rpy:1021
    old "Escape"
    new "Escape"

    # gui/game/screens.rpy:1022
    old "Accesses the game menu."
    new "دسترسی به منوی بازی"

    # gui/game/screens.rpy:1025
    old "Ctrl"
    new "Ctrl"

    # gui/game/screens.rpy:1026
    old "Skips dialogue while held down."
    new "هنگام فشرده نگه داشته شدن، دیالوگ را رد می‌کند."

    # gui/game/screens.rpy:1029
    old "Tab"
    new "Tab"

    # gui/game/screens.rpy:1030
    old "Toggles dialogue skipping."
    new "روشن یا خاموش کردن رد کردن دیالوگ"

    # gui/game/screens.rpy:1033
    old "Page Up"
    new "Page Up"

    # gui/game/screens.rpy:1034
    old "Rolls back to earlier dialogue."
    new "به دیالوگ قبلی عقب‌گرد می‌کند."

    # gui/game/screens.rpy:1037
    old "Page Down"
    new "Page Down"

    # gui/game/screens.rpy:1038
    old "Rolls forward to later dialogue."
    new "به دیالوگ بعدی جلورفت می‌کند."

    # gui/game/screens.rpy:1042
    old "Hides the user interface."
    new "رابط کاربری را پنهان می‌کند."

    # gui/game/screens.rpy:1046
    old "Takes a screenshot."
    new "یک اسکرین‌شات می‌گیرد."

    # gui/game/screens.rpy:1050
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "{a=https://www.renpy.org/l/voicing}گفتار خودکار{/a} کمکی را روشن یا خاموش می‌کند."

    # gui/game/screens.rpy:1054
    old "Opens the accessibility menu."
    new "منوی دسترس‌پذیری را باز می‌کند."

    # gui/game/screens.rpy:1060
    old "Left Click"
    new "کلیک چپ"

    # gui/game/screens.rpy:1064
    old "Middle Click"
    new "کلیک وسط"

    # gui/game/screens.rpy:1068
    old "Right Click"
    new "کلیک راست"

    # gui/game/screens.rpy:1072
    old "Mouse Wheel Up"
    new "اسکرول به بالا"

    # gui/game/screens.rpy:1076
    old "Mouse Wheel Down"
    new "اسکرول به پایین"

    # gui/game/screens.rpy:1083
    old "Right Trigger\nA/Bottom Button"
    new "Right Trigger\nA/دکمۀ پایین"

    # gui/game/screens.rpy:1087
    old "Left Trigger\nLeft Shoulder"
    new "Left Trigger\nLeft Shoulder"

    # gui/game/screens.rpy:1091
    old "Right Shoulder"
    new "Right Shoulder"

    # gui/game/screens.rpy:1095
    old "D-Pad, Sticks"
    new "\u200fD-Pad، آنالوگ‌ها"

    # gui/game/screens.rpy:1099
    old "Start, Guide, B/Right Button"
    new "\u200fStart، Guide، B/دکمۀ راست"

    # gui/game/screens.rpy:1103
    old "Y/Top Button"
    new "\u200fY/دکمۀ بالا"

    # gui/game/screens.rpy:1106
    old "Calibrate"
    new "واسنجی"

    # gui/game/screens.rpy:1134
    old "## Additional screens"
    new "## Safahāt-e ezāfi"

    # gui/game/screens.rpy:1138
    old "## Confirm screen"
    new "## Safhe-ye ta'id"

    # gui/game/screens.rpy:1140
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Safhe-ye ta'id hengāmi farāxāni mišavad ke Ren'Py bexāhad az bāzigar yek porseš-e bale yā xeyr beporsad."

    # gui/game/screens.rpy:1143
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1147
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Az gereftan-e vorudi tavassot-e safahāt-e digar hengām-e namāyeš-e in safhe xoddāri mikonad."

    # gui/game/screens.rpy:1171
    old "Yes"
    new "بله"

    # gui/game/screens.rpy:1172
    old "No"
    new "خیر"

    # gui/game/screens.rpy:1174
    old "## Right-click and escape answer \"no\"."
    new "## Click rāst va escape \"xeyr\" javāb midahand."

    # gui/game/screens.rpy:1201
    old "## Skip indicator screen"
    new "## Safhe-ye nešāngar-e rad kardan"

    # gui/game/screens.rpy:1203
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Safhe-ye skip_indicator barā-ye nešān dādan-e dar hāl-e rad kardan budan namāyeš dāde mišavad."

    # gui/game/screens.rpy:1206
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # gui/game/screens.rpy:1218
    old "Skipping"
    new "در حال رد کردن"

    # gui/game/screens.rpy:1225
    old "## This transform is used to blink the arrows one after another."
    new "## In tabdil barā-ye češmak zadan-e feleš hā yeki pas az digari estefāde mišavad."

    # gui/game/screens.rpy:1252
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## Bāyad az yek font ke dārā-ye glyph-e BLACK RIGHT-POINTING SMALL TRIANGLE bāšad estefāde konim."

    # gui/game/screens.rpy:1257
    old "## Notify screen"
    new "## Safhe-ye ettelā' resāni"

    # gui/game/screens.rpy:1259
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Safhe-ye ettelā' resāni barā-ye namāyeš dādan-e yek payām be bāzigar estefāde mišavad. (Be onvān-e mesāl, hengāmi ke bāzi zaxire-ye sari' šode va yā yek screenshot gerefte šode ast.)"

    # gui/game/screens.rpy:1262
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # gui/game/screens.rpy:1296
    old "## NVL screen"
    new "## Safhe-ye NVL"

    # gui/game/screens.rpy:1298
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## In safhe barā-ye diālog va menu hā-ye NVL-mode estefāde mišavad."

    # gui/game/screens.rpy:1300
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1311
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Diālog rā be surat-e yek vpgrid yā vbox namāyeš midahad."

    # gui/game/screens.rpy:1324
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## Menu rā, dar surati ke dāde šode bāšad, namāyeš midahad. Menu momken ast be surat-e nādorost namāyeš dāde šavad agar config.narrator_menu be True tanzim šode bāšad."

    # gui/game/screens.rpy:1354
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## In hadd-e aksar te'dād-e vorudi hā-ye NVL-mode ke mitavānand ham zamān namāyeš dāde šavand rā control mikonad."

    # gui/game/screens.rpy:1414
    old "## Bubble screen"
    new "## Safhe-ye abr"

    # gui/game/screens.rpy:1416
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## Safhe-ye abr barā-ye namāyeš-e diālog be bāzigar hengām-e estefāde az abrnevise estefāde mišavad. Safhe-ye abr parametr hā-ye yeksāni ba safhe-ye goftār migirad, bāyad yek displayable bā šenāse-ye \"what\" besāzad, va mitavānad displayable hāyi bā šenāse hā-ye \"namebox\", \"who\", va \"window\" besāzad."

    # gui/game/screens.rpy:1421
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"

    # gui/game/screens.rpy:1505
    old "## Mobile Variants"
    new "## Hālat hā-ye hamrāh"

    # gui/game/screens.rpy:1512
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Az ānjāyi ke yek mušvāre momken ast mowjud nabāšad, mā menu-ye sari' rā bā yek nosxe ke az dokme hā-ye kamtar va bozorgtar ke barā-ye lams kardan rāhat tarand estefāde mikonim."

    # gui/game/screens.rpy:1530
    old "Menu"
    new "منو"
