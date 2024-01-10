translate turkish strings:

    # screens.rpy:9
    old "## Styles"
    new "## Stiller"

    # screens.rpy:81
    old "## In-game screens"
    new "## Oyun içi ekranlar"

    # screens.rpy:85
    old "## Say screen"
    new "## Söyleme ekranı"

    # screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## Söyleme ekranı oyuncuya diyalogu göstermek için kullanılır. İki parametre alır; kim ve ne. Bunlar sırasıyla konuşan karaktere ve gösterliecek metne karşılık gelir. (Eğer isim verilmezse 'kim' parametresi Hiçbiri (None) olabilir.)"

    # screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## Ren'Py, bu ekranı gösterilen metni düzenlemek için kullandığından \"what\" id'si ile gösterilebilir bir metin yaratmalıdır. Aynı zamanda gösterilebilir yaratmak için \"who\" ve stil özelliklerini uygulamak için \"window\" id'lerini alabilir."

    # screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # screens.rpy:114
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## Bir yan resim varsa, metnin üzerinde göster. Telefon versiyonunda gösterme - yeterince yer yok."

    # screens.rpy:120
    old "## Make the namebox available for styling through the Character object."
    new "## Karakter nesnesi aracılığıyla isim kutusunun stillendirilmesine izin ver."

    # screens.rpy:164
    old "## Input screen"
    new "## Giriş ekranı"

    # screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## Bu ekran renpy.input'u göstermek için kullanılır. Komut istemi parametresi bir metin komutu aktarmak için kullanılır."

    # screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## Bu ekran çeşitli giriş parametrelerini kabul etmek için \"input\" id'si ile bir giriş göstermeli."

    # screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # screens.rpy:199
    old "## Choice screen"
    new "## Seçim ekranı"

    # screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## Bu ekran menü ifadesiyle sunulan oyun içi seçimleri göstermek için kullanılır. Tek parametre olan maddeler, nesne listeleridir; her birinin başlığı ve eylem alanı vardır."

    # screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # screens.rpy:215
    old "## When this is true, menu captions will be spoken by the narrator. When false, menu captions will be displayed as empty buttons."
    new "## Bu etkinken, menü başlıkları anlatıcı tarafından okunur. Etkin değilken, menü başlıkları boş düğmeler olarak gösterilir."

    # screens.rpy:238
    old "## Quick Menu screen"
    new "## Hızlı Menü ekranı"

    # screens.rpy:240
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## Hızlı menü, oyun-dışı menülere kolay erişim için oyunda gösterilir."

    # screens.rpy:245
    old "## Ensure this appears on top of other screens."
    new "## Bunun diğer ekranlar üzerinde göründüğünden emin olun."

    # screens.rpy:256
    old "Back"
    new "Geri"

    # screens.rpy:257
    old "History"
    new "Geçmiş"

    # screens.rpy:258
    old "Skip"
    new "Atla"

    # screens.rpy:259
    old "Auto"
    new "Oto"

    # screens.rpy:260
    old "Save"
    new "Kayıt"

    # screens.rpy:261
    old "Q.Save"
    new "H.Kayıt"

    # screens.rpy:262
    old "Q.Load"
    new "H.Yükle"

    # screens.rpy:263
    old "Prefs"
    new "Tercih"

    # screens.rpy:266
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## Bu kod, oyuncu kasten arayüzü gizlemediği sürece hızlı menünün oyunda gösterildiğinden emin olmak içindir."

    # screens.rpy:284
    old "## Main and Game Menu Screens"
    new "## Ana Menü ve Oyun Menüsü Ekranları"

    # screens.rpy:287
    old "## Navigation screen"
    new "## Gezinti ekranı"

    # screens.rpy:289
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## Bu ekran ana menü ve oyun menülerindedir, diğer menülere gezintiyi sağlar veya oyunu başlatabilir."

    # screens.rpy:304
    old "Start"
    new "Başla"

    # screens.rpy:312
    old "Load"
    new "Yükle"

    # screens.rpy:314
    old "Preferences"
    new "Tercihler"

    # screens.rpy:318
    old "End Replay"
    new "Yeniden Oynatmayı Durdur"

    # screens.rpy:322
    old "Main Menu"
    new "Ana Menü"

    # screens.rpy:324
    old "About"
    new "Hakkında"

    # screens.rpy:328
    old "## Help isn't necessary or relevant to mobile devices."
    new "## Yardım mobil cihazlarla alakalı ya da gerekli değildir."

    # screens.rpy:329
    old "Help"
    new "Yardım"

    # screens.rpy:331
    old "## The quit button is banned on iOS and unnecessary on Android."
    new "## Çıkış butonu iOS'ta yasak ve Android'de gereksizdir."

    # screens.rpy:332
    old "Quit"
    new "Çıkış"

    # screens.rpy:346
    old "## Main Menu screen"
    new "## Ana Menü ekranı"

    # screens.rpy:348
    old "## Used to display the main menu when Ren'Py starts."
    new "## Ren'Py başlatıldığında ana menüyü göstermek için kullanılır."

    # screens.rpy:350
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # screens.rpy:354
    old "## This ensures that any other menu screen is replaced."
    new "## Bu diğer herhangi bir menünün aktif olmadığından emin olur."

    # screens.rpy:361
    old "## This empty frame darkens the main menu."
    new "## Bu boş çerçeve ana menüyü karartır."

    # screens.rpy:365
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## Kullan ifadesi bunun içine başka bir ekranı dahil eder. Ana menünün asıl içeriği gezinti ekranındadır."

    # screens.rpy:408
    old "## Game Menu screen"
    new "## Oyun Menüsü ekranı"

    # screens.rpy:410
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## Bu, bir oyun menüsünün temel yapısını ortaya koyar. Ekran başlığı ile çağrılır; arka planı, başlığı ve gezinmeyi gösterir."

    # screens.rpy:413
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## Kaydırma parametresi Hiçbiri (None), \"viewport\" veya \"vpgrid\" olabilir. Bu ekran, içine yerleştirilen bir veya birden çok alt nesne (children) ile kullanılmak içindir."

    # screens.rpy:431
    old "## Reserve space for the navigation section."
    new "## Gezinti bölmesi için yer ayır."

    # screens.rpy:473
    old "Return"
    new "Dön"

    # screens.rpy:536
    old "## About screen"
    new "## Hakkında ekranı"

    # screens.rpy:538
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## Bu ekran oyun ve Ren'Py ile ilgili telif hakkı ve atıf bilgisi içerir."

    # screens.rpy:541
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## Bu ekranla ilgili özel bir şey yoktur. Özelleştirilmiş bir ekran yaratmak için örnek olarak kullanılabilir."

    # screens.rpy:548
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## Bu kullan ifadesi bu ekrana oyun menüsünü dahil eder. Vbox alt nesnesi (child) daha sonra oyun menüsü ekranındaki gözlemci (viewport) içine yerleştirilir."

    # screens.rpy:558
    old "Version [config.version!t]\n"
    new "Versiyon [config.version!t]\n"

    # screens.rpy:560
    old "## gui.about is usually set in options.rpy."
    new "## gui.about genelde options.rpy'de ayarlanır."

    # screens.rpy:564
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "{a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t] ile yapılmıştır."

    # screens.rpy:567
    old "## This is redefined in options.rpy to add text to the about screen."
    new "## Bu, hakkında ekranına metin eklemek için options.rpy'de yeniden tanımlanmıştır."

    # screens.rpy:579
    old "## Load and Save screens"
    new "## Yükleme ve Kayıt ekranları"

    # screens.rpy:581
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## Bu ekranlar oyuncunun oyunu kaydetmesi ve yeniden yüklemesi içindir. İkisi de neredeyse aynı olduğundan üçüncü bir ekran olan file_slots olarak eklenmiştir."

    # screens.rpy:585
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # screens.rpy:604
    old "Page {}"
    new "Sayfa {}"

    # screens.rpy:604
    old "Automatic saves"
    new "Otomatik kayıtlar"

    # screens.rpy:604
    old "Quick saves"
    new "Hızlı kayıtlar"

    # screens.rpy:610
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## Bu, girişin diğer bütün düğmelerden önce önce giriş olayını almasını sağlar."

    # screens.rpy:614
    old "## The page name, which can be edited by clicking on a button."
    new "## Bir düğmeye basılarak düzenlenebilen sayfa adı."

    # screens.rpy:626
    old "## The grid of file slots."
    new "## Dosya slotları ızgarası."

    # screens.rpy:646
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %B %d %Y, %H:%M"

    # screens.rpy:646
    old "empty slot"
    new "boş slot"

    # screens.rpy:654
    old "## Buttons to access other pages."
    new "## Diğer sayfalara ulaşmak için düğmeler."

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
    new "## range(1, 10) ifadesi 1'den 9'a kadar sayıları verir."

    # screens.rpy:675
    old ">"
    new ">"

    # screens.rpy:710
    old "## Preferences screen"
    new "## Tercihler ekranı"

    # screens.rpy:712
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## Tercihler ekranı oyuncunun oyunu kendisine uygun şekilde yapılandırmasını sağlar."

    # screens.rpy:715
    old "## https://www.renpy.org/doc/html/screen_special.html#preferences"
    new "## https://www.renpy.org/doc/html/screen_special.html#preferences"

    # screens.rpy:732
    old "Display"
    new "Görüntü"

    # screens.rpy:733
    old "Window"
    new "Pencere"

    # screens.rpy:734
    old "Fullscreen"
    new "Tam ekran"

    # screens.rpy:738
    old "Rollback Side"
    new "Geri-Sarma Yanı"

    # screens.rpy:739
    old "Disable"
    new "Devre Dışı Bırak"

    # screens.rpy:740
    old "Left"
    new "Sol"

    # screens.rpy:741
    old "Right"
    new "Sağ"

    # screens.rpy:746
    old "Unseen Text"
    new "Görülmemiş Metin"

    # screens.rpy:747
    old "After Choices"
    new "Seçim Sonrası"

    # screens.rpy:748
    old "Transitions"
    new "Geçişler"

    # screens.rpy:750
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## \"radio_pref\" veya \"check_pref\" türündeki ek vbox'lar, yaratıcı tarafından belirlenmiş tercihlere burada eklenebilir."

    # screens.rpy:761
    old "Text Speed"
    new "Metin Hızı"

    # screens.rpy:765
    old "Auto-Forward Time"
    new "Zamanı Oto İleri Sar"

    # screens.rpy:772
    old "Music Volume"
    new "Müzik Düzeyi"

    # screens.rpy:779
    old "Sound Volume"
    new "Ses Düzeyi"

    # screens.rpy:785
    old "Test"
    new "Test"

    # screens.rpy:789
    old "Voice Volume"
    new "Konuşma Düzeyi"

    # screens.rpy:800
    old "Mute All"
    new "Hepsini Sustur"

    # screens.rpy:876
    old "## History screen"
    new "## Geçmiş ekranı"

    # screens.rpy:878
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## Bu ekran oyuncuya diyalog geçmişini gösterir. Bu ekranla ilgili özel bir şey olmasa da _history_list'te depolanmış diyalog geçmişine erişmesi gerekmektedir."

    # screens.rpy:882
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # screens.rpy:888
    old "## Avoid predicting this screen, as it can be very large."
    new "## Bu ekranı öngörmekten uzak dur, çünkü çok büyük olabilir."

    # screens.rpy:899
    old "## This lays things out properly if history_height is None."
    new "## Geçmiş yüksekliği (history_height) yok ise her şeyi düzgünce yerleştirir."

    # screens.rpy:909
    old "## Take the color of the who text from the Character, if set."
    new "## Eğer seçili ise, Karakter'den metin rengini al."

    # screens.rpy:918
    old "The dialogue history is empty."
    new "Diyalog geçmişi boş."

    # screens.rpy:921
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## Geçmiş ekranında ne tür etiketlerin gösterilmesine izin verileceğini belirler."

    # screens.rpy:968
    old "## Help screen"
    new "## Yardım ekranı"

    # screens.rpy:970
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## Tuş ve fare girdileriyle ilgili bilgi veren bir ekran. Asıl yardımı görüntülemek için diğer ekranları kullanır. (keyboard_help, mouse_help, ve gamepad_help)"

    # screens.rpy:989
    old "Keyboard"
    new "Klavye"

    # screens.rpy:990
    old "Mouse"
    new "Fare"

    # screens.rpy:993
    old "Gamepad"
    # Automatic translation.
    new "Oyun Kumandası"

    # screens.rpy:1006
    old "Enter"
    # Automatic translation.
    new "Girin"

    # screens.rpy:1007
    old "Advances dialogue and activates the interface."
    new "Diyalogu ilerletir ve arayüzü aktifleştirir."

    # screens.rpy:1010
    old "Space"
    new "Boşluk"

    # screens.rpy:1011
    old "Advances dialogue without selecting choices."
    new "Seçim yapmadan diyalogu ilerletir."

    # screens.rpy:1014
    old "Arrow Keys"
    new "Ok Tuşları"

    # screens.rpy:1015
    old "Navigate the interface."
    new "Arayüzde gezinmeyi sağlar."

    # screens.rpy:1018
    old "Escape"
    # Automatic translation.
    new "Kaçış"

    # screens.rpy:1019
    old "Accesses the game menu."
    new "Oyun menüsüne erişir."

    # screens.rpy:1022
    old "Ctrl"
    new "Ctrl"

    # screens.rpy:1023
    old "Skips dialogue while held down."
    new "Basılı iken diyalogu atlar."

    # screens.rpy:1026
    old "Tab"
    new "Tab"

    # screens.rpy:1027
    old "Toggles dialogue skipping."
    new "Diyalog atlamayı etkinleştirir ya da devre dışı bırakır."

    # screens.rpy:1030
    old "Page Up"
    # Automatic translation.
    new "Sayfa Yukarı"

    # screens.rpy:1031
    old "Rolls back to earlier dialogue."
    new "Önceki diyaloga geri sarar."

    # screens.rpy:1034
    old "Page Down"
    # Automatic translation.
    new "Sayfa Aşağı"

    # screens.rpy:1035
    old "Rolls forward to later dialogue."
    new "Daha yeni diyaloga ileri sarar."

    # screens.rpy:1039
    old "Hides the user interface."
    new "Kullanıcı arayüzünü gizler."

    # screens.rpy:1043
    old "Takes a screenshot."
    new "Ekran görüntüsü kaydeder."

    # screens.rpy:1047
    old "Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}."
    new "Yardımcı {a=https://www.renpy.org/l/voicing}kendiliğniden-seslendirme{/a}yi açar veya kapatır."

    # screens.rpy:1053
    old "Left Click"
    new "Sol Tıklama"

    # screens.rpy:1057
    old "Middle Click"
    new "Orta Tıklama"

    # screens.rpy:1061
    old "Right Click"
    new "Sağ Tıklama"

    # screens.rpy:1065
    old "Mouse Wheel Up"
    new "Fare Tekerleği Yukarı"

    # screens.rpy:1069
    old "Mouse Wheel Down"
    new "Fare Tekerleği Aşağı"

    # screens.rpy:1076
    old "Right Trigger\nA/Bottom Button"
    new "Sağ Trigger\nA/Alt Tuş"

    # screens.rpy:1080
    old "Left Trigger\nLeft Shoulder"
    new "Sol Trigger\nSol Omuz"

    # screens.rpy:1084
    old "Right Shoulder"
    new "Sağ Omuz"

    # screens.rpy:1089
    old "D-Pad, Sticks"
    new "D-Pad, Çubuklar"

    # screens.rpy:1093
    old "Start, Guide"
    new "Başla, Rehber"

    # screens.rpy:1097
    old "Y/Top Button"
    new "Y/Üst Tuş"

    # screens.rpy:1100
    old "Calibrate"
    new "Kalibre Et"

    # screens.rpy:1128
    old "## Additional screens"
    new "## Ek ekranlar"

    # screens.rpy:1132
    old "## Confirm screen"
    new "## Doğrulama ekranı"

    # screens.rpy:1134
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## Doğrulama ekranı, Ren'Py oyuncuya bir evet-hayır sorusu sorduğunda kullanılır."

    # screens.rpy:1137
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # screens.rpy:1141
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## Bu ekran gösterilirken diğer ekranların girdi almamasını sağla."

    # screens.rpy:1165
    old "Yes"
    new "Evet"

    # screens.rpy:1166
    old "No"
    new "Hayır"

    # screens.rpy:1168
    old "## Right-click and escape answer \"no\"."
    new "## Sağ tık ve Escape \"no\" anlamına gelir."

    # screens.rpy:1195
    old "## Skip indicator screen"
    new "## Atlama gösterge ekranı"

    # screens.rpy:1197
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## Atlama gösterge ekranı, atlama işleminin devam ettiğini gösterir."

    # screens.rpy:1200
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # screens.rpy:1212
    old "Skipping"
    new "Atlama"

    # screens.rpy:1219
    old "## This transform is used to blink the arrows one after another."
    new "## Bu transform, okları arka arkaya yakıp söndürmek için kullanılır."

    # screens.rpy:1246
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## İçinde SİYAH, SAĞI GÖSTEREN KÜÇÜK ÜÇGEN olan bir font kullanmalıyız."

    # screens.rpy:1251
    old "## Notify screen"
    new "## Bildirim ekranı"

    # screens.rpy:1253
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## Bildirim ekranı oyuncuya bir mesaj göstermek için kullanılır. (Mesela hızlı kayıt yapıldığında veya ekran görüntüsü alındığında.)"

    # screens.rpy:1256
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # screens.rpy:1290
    old "## NVL screen"
    new "## NVL ekranı"

    # screens.rpy:1292
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## Bu ekran NVL-modu diyalogları ve menüleri için kullanılır."

    # screens.rpy:1294
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # screens.rpy:1305
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## Diyalogu vpgrid ya da vbox'ta gösterir."

    # screens.rpy:1318
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True, as it is above."
    new "## Eğer varsa menüyü gösterir. Eğer yukarıdaki gibi config.narrator_menu etkinse menü yanlış gösterilebilir."

    # screens.rpy:1348
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## Bu, bir seferde gösterilen NVL-modu girdilerinin maksimum sayısını kontrol eder."

    # screens.rpy:1410
    old "## Mobile Variants"
    new "## Mobil Varyasyonlar"

    # screens.rpy:1417
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## Fare olmayabileceği için, hızlı menüyü dokunması daha kolay olan daha büyük ve daha az düğmeli bir versiyonu ile değiştiririz."

    # screens.rpy:1435
    old "Menu"
    new "Menü"


translate turkish strings:

    # gui/game/screens.rpy:329
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    # Automatic translation.
    new "## Çıkış düğmesi iOS'ta yasaklanmıştır ve Android ve Web'de gereksizdir."

    # gui/game/screens.rpy:676
    old "Upload Sync"
    # Automatic translation.
    new "Yükleme Senkronizasyonu"

    # gui/game/screens.rpy:680
    old "Download Sync"
    # Automatic translation.
    new "Sync'i İndirin"

    # gui/game/screens.rpy:1049
    old "Opens the accessibility menu."
    # Automatic translation.
    new "Erişilebilirlik menüsünü açar."

    # gui/game/screens.rpy:1320
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    # Automatic translation.
    new "## Verilmişse menüyü görüntüler. config.narrator_menu True olarak ayarlanırsa menü yanlış görüntülenebilir."

    # gui/game/screens.rpy:1410
    old "## Bubble screen"
    # Automatic translation.
    new "## Kabarcık ekranı"

    # gui/game/screens.rpy:1412
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    # Automatic translation.
    new "## Baloncuk ekranı, konuşma balonları kullanıldığında oyuncuya diyalog görüntülemek için kullanılır. Kabarcık ekranı say ekranı ile aynı parametreleri alır, \"what\" id'si ile bir görüntülenebilir oluşturmalıdır ve \"namebox\", \"who\" ve \"window\" id'leri ile görüntülenebilir oluşturabilir."

    # gui/game/screens.rpy:1417
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
