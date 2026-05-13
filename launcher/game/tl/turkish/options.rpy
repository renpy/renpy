
translate turkish strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## Bu dosya oyununuzu özelleştirmek için değiştirlebilecek ayarları içerir."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## İki '#' ile başlayan satırlar yorumdur, öyle kalmalıdırlar. Tek '#' ile başlayan satırlar etkin olmayan kodlardır, gerekli olduğunda '#' işareti silinerek etkinleştirilebilirler."

    # options.rpy:10
    old "## Basics"
    new "## Temeller"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## Oyunun insan tarafından okunabilir ismi. Varsayılan pencere başlığını ayarlamak için kullanılır, arayüzde ve hata raporlarında görünür."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## Stringi çevreleyen _(), stringin çeviriye uygun olduğu anlamına gelir."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 Varsayılan GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## Yukarıda yazılan başlığı ana menüde görünüp görünmeyeceğini belirler. Başlığı gizlemek için bunu etkinleştirmeyin."

    # options.rpy:26
    old "## The version of the game."
    new "## Oyunun versiyonu."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    new "## Oyunun 'hakkında' ekranına yerleştirilen metin. Metni üçlü-tırnak arasına yerleştirin, paragraflar arası boş bir satır bırakın."

    # options.rpy:38
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## Oyunun yayımlanacak derlemenin kısayollarında ve klasörlerinde kullanılacak kısa ismi. Bu sadece ASCII karakterleri içermeli; boşluk, iki nokta ya da noktalı virgül içermemeli."

    # options.rpy:45
    old "## Sounds and music"
    new "## Sesler ve müzik"

    # options.rpy:47
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## Bu üç değişken oynatıcıda varsayılan olarak gösterilecek mixer'ları kontrol eder. Bunların birini etkisizleştirmek, uygun mixer'ı saklar."

    # options.rpy:56
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## Kullanıcının ses kanalında bir örnek ses oynatabilmesine izin vermek istiyorsanız, aşağıdaki satırı etkinleştirin ve oynatılacak bir örnek ses seçin."

    # options.rpy:63
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Oyuncu ana menüdeyken oynatılacak bir ses dosyasını ayarlamak için aşağıdaki satırı etkinleştirin. Bu dosya oyun başladıktan sonra durdurulana ya da başka bir dosya oynatılana kadr çalmaya devam edecektir."

    # options.rpy:70
    old "## Transitions"
    new "## Geçişler"

    # options.rpy:72
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## Bu değişkenler belli olaylardan sonraki geçişleri ayarlamak için kullanılır. Her değişken bir geçişe ayarlanmalı, geçiş kullanılmak istenmiyorsa 'Hiçbiri' seçilmeli."

    # options.rpy:76
    old "## Entering or exiting the game menu."
    new "## Oyun menüsüne giriş ve menüden çıkış."

    # options.rpy:82
    old "## Between screens of the game menu."
    new "## Oyun menüleri ekranları arası."

    # options.rpy:87
    old "## A transition that is used after a game has been loaded."
    new "## Oyun yüklendikten sonra kullanılan bir geçiş."

    # options.rpy:92
    old "## Used when entering the main menu after the game has ended."
    new "## Oyun bittikten sonra ana menüye geçerken kullanılır."

    # options.rpy:97
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## Oyun başlangı sırasında kullanılan geçiş için bir değişken yok. Onun yerine, sahneyi gösterdikten sonra bir 'with' ifadesi kullanın."

    # options.rpy:102
    old "## Window management"
    new "## Pencere yönetimi"

    # options.rpy:104
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## Bu, diyalog ekranının ne zaman gösterildiğini kontrol eder. Eğer \"show\" seçili ise, her zaman gösterilir. Eğer \"hide\" ise, sadece diyalog olduğu zaman gösterilir. Eğer \"auto\" ise, sahne ifadelerinde pencere gizlenir ve diyalog sırasında yeniden gösterilir."

    # options.rpy:109
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## Bu, oyun başladıktan sonra \"window show\", \"window hide\", ve \"window auto\" ifadeleriyle değiştirilebilir."

    # options.rpy:115
    old "## Transitions used to show and hide the dialogue window"
    new "## Diyalog penceresini gösterip gizlerken kullanılan geçişler"

    # options.rpy:121
    old "## Preference defaults"
    new "## Tercih varsayılanları"

    # options.rpy:123
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Varsayılan metin hızını kontrol eder. Varsayılan olan 0 sayısı metni anında gösterir, eğer başka bir sayı girilirse bu sayı saniye başına yazılan karakter hızını belirler."

    # options.rpy:129
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## Varsayılan oto-ileri-sarma beklemesi. Uzun sayılar daha uzun beklemeye yol açar, 0 ve 30 arası uygundur."

    # options.rpy:135
    old "## Save directory"
    new "## Kayıt klasörü"

    # options.rpy:137
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Ren'Py'ın oyun kayıt dosyaları için kullanacağı, platforma özel olan yeri knotrol eder. Kayıt dosyaları şuraya yerleştirilecektir:"

    # options.rpy:140
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:142
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:144
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # options.rpy:146
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## Bu genelde değiştirilmemelidir, ancak değiştirilecekse mutlaka bir string olmalı, bir ifade değil."

    # options.rpy:152
    old "## Icon"
    new "## İkon"

    # options.rpy:154
    old "## The icon displayed on the taskbar or dock."
    new "## İşlem çubuğunda ya da kenetlenmiş durumda gösterilecek ikon."

    # options.rpy:159
    old "## Build configuration"
    new "## Derleme yapılandırması"

    # options.rpy:161
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## Bu bölüm Ren'Py'ın projenizi nasıl dağıtım dosyalarına dönüştüreceğini kontrol eder."

    # options.rpy:166
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## Bu fonksiyonlar dosya yolları gerektirir. Dosya yolları büyük-küçük harfe duyarsızdır ve başında ister / olsun ister olmasın ana klasöre göre eşleştirilirler. Eğer birden çok eşleşme olursa ilki kullanılır."

    # options.rpy:171
    old "## In a pattern:"
    new "## Bir yolda:"

    # options.rpy:173
    old "## / is the directory separator."
    new "## / karakteri klasör ayıracıdır."

    # options.rpy:175
    old "## * matches all characters, except the directory separator."
    new "## * klasör ayıracı dışında bütün karakterleri eşleştirir."

    # options.rpy:177
    old "## ** matches all characters, including the directory separator."
    new "## ** klasör ayıracı da dahil bütün karakterleri eşleştirir."

    # options.rpy:179
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## Örneğin, \"*.txt\" ana klasördeki bütün txt dosyalarını, \"game/**.ogg\" oyun klasöründeki ve alt klasörlerdeki bütün ogg'leri,  \"**.psd\" ise projenin herhangi bir yerindeki tüm psd dosyalarını eşleştirir."

    # options.rpy:183
    old "## Classify files as None to exclude them from the built distributions."
    new "## Dosyaları derlenmiş dağıtımlardan ayırmak için 'Hiçbiri (None)' olarak sınıflandırın."

    # options.rpy:191
    old "## To archive files, classify them as 'archive'."
    new "## Dosyaları arşivlemek için 'arşiv' olarak sınıflandırın."

    # options.rpy:196
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## Doküman yollarıyla eşleşen dosyalar mac uygulaması derlemesinde kopyalanır, böylece hem uygulamada hem de zip dosyasında görünürler."

    # options.rpy:202
    old "## Set this to a string containing your Apple Developer ID Application to enable codesigning on the Mac. Be sure to change it to your own Apple-issued ID."
    new "## Mac'te codesigning'i etkinleştirmek için bunu Apple Developer ID Application'ınızı içeren bir stringe ayarlayın. Bunun size Apple tarafından verilen ID olduğuna emin olun."

    # options.rpy:209
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## Uygulama içi satın alma ve genişletme paketleri indirmek için bir Google Play lisans anahtarı gerekir. Bu, Google Play geliştirici konsolunda \"Services & APIs\" sayfasında bulunabilir."

    # options.rpy:216
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## itch.io projesine bağlı, eğik çizgi ile ayrılmış kullanıcı adı ve proje adı."


translate turkish strings:

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    # Automatic translation.
    new "## Bu üç değişken, diğer şeylerin yanı sıra, hangi mikserlerin varsayılan olarak oynatıcıya gösterileceğini kontrol eder. Bunlardan birini False olarak ayarlamak ilgili mikseri gizleyecektir."

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    # Automatic translation.
    new "## Uygulama içi satın alımları gerçekleştirmek için bir Google Play lisans anahtarı gereklidir. Google Play geliştirici konsolunda, \"Para Kazan\" > \"Para Kazanma Kurulumu\" > \"Lisanslama\" altında bulunabilir."

