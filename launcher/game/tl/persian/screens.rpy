
translate persian strings:

    # gui/game/screens.rpy:9
    old "## Styles"
    new "## استایل‌ها"

    # gui/game/screens.rpy:81
    old "## In-game screens"
    new "## صفحه‌های درون بازی"

    # gui/game/screens.rpy:85
    old "## Say screen"
    new "## صفحهٔ گفتار"

    # gui/game/screens.rpy:87
    old "## The say screen is used to display dialogue to the player. It takes two parameters, who and what, which are the name of the speaking character and the text to be displayed, respectively. (The who parameter can be None if no name is given.)"
    new "## صفحهٔ گفتار برای نمایش دیالوگ به بازیکن استفاد می‌شود. این صفحه دو پارامتر who و what را می‌گیرد، که به ترتیب نام شخصیت در حال صحبت و متنی که نمایش داده می‌شود هستند. (پارامتر who در صورت عدم ذکر نام می‌تواند None باشد.)"

    # gui/game/screens.rpy:92
    old "## This screen must create a text displayable with id \"what\", as Ren'Py uses this to manage text display. It can also create displayables with id \"who\" and id \"window\" to apply style properties."
    new "## این صفحه باید یک displayable متنی با شناسهٔ \"what\" بسازد، چراکه Ren'Py از این برای مدیریت نمایش متن استفاده می‌کند. این صفحه همچنین می‌تواند displayableهایی با شناسه‌های \"who\" و \"window\" برای اعمال ویژگی‌های استایل بسازد."

    # gui/game/screens.rpy:96
    old "## https://www.renpy.org/doc/html/screen_special.html#say"
    new "## https://www.renpy.org/doc/html/screen_special.html#say"

    # gui/game/screens.rpy:113
    old "## If there's a side image, display it above the text. Do not display on the phone variant - there's no room."
    new "## اگر تصویر کناری وجود داشته باشد، بالای متن نمایشه بده. در حالت گوشی نمایش نده، چون فضا کافی نیست."

    # gui/game/screens.rpy:119
    old "## Make the namebox available for styling through the Character object."
    new "## جعبهٔ نام را برای استایل کردن از طریق شیء Character موجود کن."

    # gui/game/screens.rpy:164
    old "## Input screen"
    new "## صفحهٔ ورودی"

    # gui/game/screens.rpy:166
    old "## This screen is used to display renpy.input. The prompt parameter is used to pass a text prompt in."
    new "## این صفحه برای نمایش renpy.input استفاده می‌شود. پارامتر پرامپت برای ارسال یک درخواست متن استفاده می‌شود."

    # gui/game/screens.rpy:169
    old "## This screen must create an input displayable with id \"input\" to accept the various input parameters."
    new "## این صفحه باید یک displayable ورودی با شناسهٔ \"input\" برای دریافت پارامترهایورودی مختلف بسازد."

    # gui/game/screens.rpy:172
    old "## https://www.renpy.org/doc/html/screen_special.html#input"
    new "## https://www.renpy.org/doc/html/screen_special.html#input"

    # gui/game/screens.rpy:199
    old "## Choice screen"
    new "## صفحهٔ انتخاب"

    # gui/game/screens.rpy:201
    old "## This screen is used to display the in-game choices presented by the menu statement. The one parameter, items, is a list of objects, each with caption and action fields."
    new "## این صفحه برای نمایش انتخاب‌های درون بازی ارائه شده توسط گزارهٔ منو استفاده می‌شود. تنها پارامتر آن، items، یک لیست از اشیاء است، که هر کدام دارای خانه‌های عنوان و عمل هستند."

    # gui/game/screens.rpy:205
    old "## https://www.renpy.org/doc/html/screen_special.html#choice"
    new "## https://www.renpy.org/doc/html/screen_special.html#choice"

    # gui/game/screens.rpy:233
    old "## Quick Menu screen"
    new "## صفحهٔ منوی سریع"

    # gui/game/screens.rpy:235
    old "## The quick menu is displayed in-game to provide easy access to the out-of-game menus."
    new "## منوی سریع داخل بازی برای فراهم کردن دسترسی سریع به منوهای بیرون بازی نمایش داده می‌شود."

    # gui/game/screens.rpy:240
    old "## Ensure this appears on top of other screens."
    new "## مطمئن ساختن از اینکه این بر روی صفحات دیگر ظاهر شود."

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
    new "ذخیرهٔ سریع"

    # gui/game/screens.rpy:257
    old "Q.Load"
    new "بارگذاری سریع"

    # gui/game/screens.rpy:258
    old "Prefs"
    new "ترجیحات"

    # gui/game/screens.rpy:261
    old "## This code ensures that the quick_menu screen is displayed in-game, whenever the player has not explicitly hidden the interface."
    new "## این کد از نمایش داده شدن صفحهٔ quick_menu داخل بازی هنگامی که بازیکن صریحاً رابط را پنهان نکرده است مطمئن می‌سازی."

    # gui/game/screens.rpy:279
    old "## Main and Game Menu Screens"
    new "## صفحه‌های منوی بازی و اصلی"

    # gui/game/screens.rpy:282
    old "## Navigation screen"
    new "## صفحهٔ پیمایش"

    # gui/game/screens.rpy:284
    old "## This screen is included in the main and game menus, and provides navigation to other menus, and to start the game."
    new "## این صفحه در منوهای بازی و اصلی وجود داشته، و پیمایش به منوهای دیگر، و شروع بازی را فراهم می‌کند."

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
    new "## کمک برای دستگاه‌های همراه الزامی و با به آن‌ها مرتبط نیست."

    # gui/game/screens.rpy:324
    old "Help"
    new "کمک"

    # gui/game/screens.rpy:328
    old "## The quit button is banned on iOS and unnecessary on Android and Web."
    new "## دکمهٔ خروج در iOS ممنوع شده و در اندروید و وب الزامی نیست."

    # gui/game/screens.rpy:329
    old "Quit"
    new "خروج"

    # gui/game/screens.rpy:343
    old "## Main Menu screen"
    new "## صفحهٔ منوی اصلی"

    # gui/game/screens.rpy:345
    old "## Used to display the main menu when Ren'Py starts."
    new "## برای نمایش منوی اصلی هنگام شروع Ren'Py استفاده می‌شود."

    # gui/game/screens.rpy:347
    old "## https://www.renpy.org/doc/html/screen_special.html#main-menu"
    new "## https://www.renpy.org/doc/html/screen_special.html#main-menu"

    # gui/game/screens.rpy:351
    old "## This ensures that any other menu screen is replaced."
    new "## این از جایگزینی هر منوی دیگر مطمئن می‌سازد."

    # gui/game/screens.rpy:356
    old "## This empty frame darkens the main menu."
    new "## این قاب خالی منوی اصلی را تیره‌تر می‌کند."

    # gui/game/screens.rpy:360
    old "## The use statement includes another screen inside this one. The actual contents of the main menu are in the navigation screen."
    new "## گزارهٔ use یک صفحهٔ دیگر را داخل این صفحه شامل می‌کند. خود محتویات منوی اصلی در صفحهٔ پیمایش قرار دارند."

    # gui/game/screens.rpy:405
    old "## Game Menu screen"
    new "## صفحهٔ منوی بازی"

    # gui/game/screens.rpy:407
    old "## This lays out the basic common structure of a game menu screen. It's called with the screen title, and displays the background, title, and navigation."
    new "## این ساختار بنیاد عمومی صفحهٔ منوی بازی را می‌چیند. این با تیتر صفحه فراخوانی می‌شود، و پس‌زمینه، تیتر، و پیمایش را نمایش می‌دهد."

    # gui/game/screens.rpy:410
    old "## The scroll parameter can be None, or one of \"viewport\" or \"vpgrid\". This screen is intended to be used with one or more children, which are transcluded (placed) inside it."
    new "## پارامتر scroll می‌تواند None، و یا یکی از \"viewport\" یا \"vpgrid\" باشد. این صفحه برای استفاده با یک یا چند فرزند، که در آن تراگنجانیده (قرار گرفته) شده در نظر گرفته شده است."

    # gui/game/screens.rpy:428
    old "## Reserve space for the navigation section."
    new "## فضای رزرو شده برای بخش هدایتی."

    # gui/game/screens.rpy:474
    old "Return"
    new "برگشت"

    # gui/game/screens.rpy:537
    old "## About screen"
    new "## صفجهٔ درباره"

    # gui/game/screens.rpy:539
    old "## This screen gives credit and copyright information about the game and Ren'Py."
    new "## این صفحه اطلاعات اعتبارها (کردیت) و حق تکثیر (کپی‌رایت) مربوط به بازی و Ren'Py را نمایش می‌دهد."

    # gui/game/screens.rpy:542
    old "## There's nothing special about this screen, and hence it also serves as an example of how to make a custom screen."
    new "## هیچ چیز خاصی دربارهٔ این صفحه وجود ندارد، و از این رو این صفحه یک مثال از چگونگی ساخت یک صفحهٔ شخصی‌سازی‌شده است."

    # gui/game/screens.rpy:549
    old "## This use statement includes the game_menu screen inside this one. The vbox child is then included inside the viewport inside the game_menu screen."
    new "## گزارهٔ use شامل صفحهٔ game_menu که داخل این است، می‌شود. فرزند vbox پس از این در viewport داخل صفحهٔ game_menu شامل می‌شود."

    # gui/game/screens.rpy:559
    old "Version [config.version!t]\n"
    new "نسخهٔ [config.version!t]\n"

    # gui/game/screens.rpy:561
    old "## gui.about is usually set in options.rpy."
    new "## gui.about معمولاً در options.rpy تنظیم می‌شود."

    # gui/game/screens.rpy:565
    old "Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"
    new "ساخته شده با {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]"

    # gui/game/screens.rpy:576
    old "## Load and Save screens"
    new "## صفحات بارگذاری و ذخیره"

    # gui/game/screens.rpy:578
    old "## These screens are responsible for letting the player save the game and load it again. Since they share nearly everything in common, both are implemented in terms of a third screen, file_slots."
    new "## این صفحات به بازیکن امکان ذخیره و بارگذاری مجدد بازی را می‌دهند. از آن‌جایی که تقریباً همه‌چیزشان مشترک است، هردو به صورت یک صفحهٔ سوم، file_slots، پیاده‌سازی می‌شوند."

    # gui/game/screens.rpy:582
    old "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"
    new "## https://www.renpy.org/doc/html/screen_special.html#save https://www.renpy.org/doc/html/screen_special.html#load"

    # gui/game/screens.rpy:601
    old "Page {}"
    new "صفحهٔ {}"

    # gui/game/screens.rpy:601
    old "Automatic saves"
    new "ذخیره‌های خودکار"

    # gui/game/screens.rpy:601
    old "Quick saves"
    new "ذخیره‌های سریع"

    # gui/game/screens.rpy:607
    old "## This ensures the input will get the enter event before any of the buttons do."
    new "## این از گرفتن رویداد ورود توسط ورودی قبل از هریک از دکمه‌ها مطمئن می‌سازد."

    # gui/game/screens.rpy:611
    old "## The page name, which can be edited by clicking on a button."
    new "## نام صفحه، که می‌تواند با کلیک کردن بر روی یک دکمه تغییر داده شود."

    # gui/game/screens.rpy:623
    old "## The grid of file slots."
    new "## شبکهٔ خانه‌های فایل‌ها."

    # gui/game/screens.rpy:643
    old "{#file_time}%A, %B %d %Y, %H:%M"
    new "{#file_time}%A, %d %B %Y, %H:%M"

    # gui/game/screens.rpy:643
    old "empty slot"
    new "خانهٔ خالی"

    # gui/game/screens.rpy:651
    old "## Buttons to access other pages."
    new "## دکمه‌هایی برای دسترسی به صفحات دیگر."

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
    new "## range(1, 10) اعداد 1 تا 9 را می‌دهد."

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
    new "## صفحهٔ ترجیحات"

    # gui/game/screens.rpy:724
    old "## The preferences screen allows the player to configure the game to better suit themselves."
    new "## صفحهٔ ترجیحات به بازیکن این امکان را می‌دهد که بازی را طوری تنظیم کند که برایش مناسب‌تر باشد."

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
    new "بعد از انتخاب‌ها"

    # gui/game/screens.rpy:753
    old "Transitions"
    new "گذارها"

    # gui/game/screens.rpy:755
    old "## Additional vboxes of type \"radio_pref\" or \"check_pref\" can be added here, to add additional creator-defined preferences."
    new "## vboxهای بیشتر از نوع \"radio_pref\" یا \"check_pref\" را می‌توان برای اضافه کردن ترجیحات تعریف شده توسط سازندهٔ بیشتر اینجا اضافه کردن."

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
    new "## صفحهٔ تاریخچه"

    # gui/game/screens.rpy:883
    old "## This is a screen that displays the dialogue history to the player. While there isn't anything special about this screen, it does have to access the dialogue history stored in _history_list."
    new "## این صفحه‌ای است که تاریخچهٔ دیالوگ را به بازیکن نمایش می‌دهد. اگرچه چیز خاصی در مورد این صفحه وجود ندارد، این صفحه باید به تاریخچهٔ دیالوگ ذخیره شده در _history_list دسترسی داشته باشد."

    # gui/game/screens.rpy:887
    old "## https://www.renpy.org/doc/html/history.html"
    new "## https://www.renpy.org/doc/html/history.html"

    # gui/game/screens.rpy:893
    old "## Avoid predicting this screen, as it can be very large."
    new "## جلوگیری از پیش‌بینی این صفحه، چراکه بسیار بزرگ می‌تواند باشد."

    # gui/game/screens.rpy:904
    old "## This lays things out properly if history_height is None."
    new "## این در صورتی که history_height مقدار None داشته باشد، به درستی همه‌چیز را می‌چیند."

    # gui/game/screens.rpy:914
    old "## Take the color of the who text from the Character, if set."
    new "## رنگ متن who را در صورتی که تنظیم شده باشد، از Character بگیر."

    # gui/game/screens.rpy:923
    old "The dialogue history is empty."
    new "تاریخچهٔ دیالوگ خالی است."

    # gui/game/screens.rpy:926
    old "## This determines what tags are allowed to be displayed on the history screen."
    new "## این تعیین می‌کند چه تگ‌هایی را می‌توان در صفحهٔ تاریخچه نمایش داد."

    # gui/game/screens.rpy:971
    old "## Help screen"
    new "## صفحهٔ کمک"

    # gui/game/screens.rpy:973
    old "## A screen that gives information about key and mouse bindings. It uses other screens (keyboard_help, mouse_help, and gamepad_help) to display the actual help."
    new "## صفحه‌ای که در مورد کلیدبندی و تنظیمات موشواره اطلاعات می‌دهد. این از صفحات دیگر (keyboard_help، mouse_help, و gamepad_help) برای نمایش خود کمک استفاده می‌کند."

    # gui/game/screens.rpy:992
    old "Keyboard"
    new "صفحه‌کلید"

    # gui/game/screens.rpy:993
    old "Mouse"
    new "موشواره"

    # gui/game/screens.rpy:996
    old "Gamepad"
    new "دستهٔ بازی"

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
    new "کلیدهای جهت"

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
    new "Right Trigger\nA/دکمهٔ پایین"

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
    new "\u200fStart، Guide، B/دکمهٔ راست"

    # gui/game/screens.rpy:1103
    old "Y/Top Button"
    new "\u200fY/دکمهٔ بالا"

    # gui/game/screens.rpy:1106
    old "Calibrate"
    new "واسنجی"

    # gui/game/screens.rpy:1134
    old "## Additional screens"
    new "## صفحات اضافی"

    # gui/game/screens.rpy:1138
    old "## Confirm screen"
    new "## صفحهٔ تأیید"

    # gui/game/screens.rpy:1140
    old "## The confirm screen is called when Ren'Py wants to ask the player a yes or no question."
    new "## صفحهٔ تأیید هنگامی فراخوانی می‌شود که Ren'Py بخواهد از بازیکن یک پرسش بله یا خیر بپرسد."

    # gui/game/screens.rpy:1143
    old "## https://www.renpy.org/doc/html/screen_special.html#confirm"
    new "## https://www.renpy.org/doc/html/screen_special.html#confirm"

    # gui/game/screens.rpy:1147
    old "## Ensure other screens do not get input while this screen is displayed."
    new "## از گرفتن ورودی توسط صفحات دیگر هنگام نمایش این صفحه خودداری می‌کند."

    # gui/game/screens.rpy:1171
    old "Yes"
    new "بله"

    # gui/game/screens.rpy:1172
    old "No"
    new "خیر"

    # gui/game/screens.rpy:1174
    old "## Right-click and escape answer \"no\"."
    new "## کلیک راست و escape «خیر» جواب می‌دهند."

    # gui/game/screens.rpy:1201
    old "## Skip indicator screen"
    new "## صفحهٔ نشانگر رد کردن"

    # gui/game/screens.rpy:1203
    old "## The skip_indicator screen is displayed to indicate that skipping is in progress."
    new "## صفحهٔ skip_indicator برای نشان دادن اینکه بازی در حال رد کردن متن است، نمایش داده می‌شود."

    # gui/game/screens.rpy:1206
    old "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"
    new "## https://www.renpy.org/doc/html/screen_special.html#skip-indicator"

    # gui/game/screens.rpy:1218
    old "Skipping"
    new "در حال رد کردن"

    # gui/game/screens.rpy:1225
    old "## This transform is used to blink the arrows one after another."
    new "## این تبدیل برای چشمک زدن پیکان‌ها یکی پس از دیگری استفاده می‌شود."

    # gui/game/screens.rpy:1252
    old "## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE glyph in it."
    new "## باید از یک فونت که دارای گلیف BLACK RIGHT-POINTING SMALL TRIANGLE می‌باشد استفاده کنیم."

    # gui/game/screens.rpy:1257
    old "## Notify screen"
    new "## Safhe-ye ettelā' resāni"

    # gui/game/screens.rpy:1259
    old "## The notify screen is used to show the player a message. (For example, when the game is quicksaved or a screenshot has been taken.)"
    new "## صفحهٔ اطلاع‌رسانی برای نمایش دادن یک پیام به بازیکن استفاده می‌شود. (به عنوان مثال، هنگامی که بازی ذخیرهٔ سریع شده یا یک اسکرین‌شات گرفته شده است.)"

    # gui/game/screens.rpy:1262
    old "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"
    new "## https://www.renpy.org/doc/html/screen_special.html#notify-screen"

    # gui/game/screens.rpy:1296
    old "## NVL screen"
    new "## صفحهٔ NVL"

    # gui/game/screens.rpy:1298
    old "## This screen is used for NVL-mode dialogue and menus."
    new "## این صفحه برای دیالوگ و منوهای NVL-mode استفاده می‌شود."

    # gui/game/screens.rpy:1300
    old "## https://www.renpy.org/doc/html/screen_special.html#nvl"
    new "## https://www.renpy.org/doc/html/screen_special.html#nvl"

    # gui/game/screens.rpy:1311
    old "## Displays dialogue in either a vpgrid or the vbox."
    new "## دیالوگ را به صورت یک vpgrid یا vbox نمایش می‌دهد."

    # gui/game/screens.rpy:1324
    old "## Displays the menu, if given. The menu may be displayed incorrectly if config.narrator_menu is set to True."
    new "## منو را در صورتی که داده شده باشد، نمایش می‌دهد. منو ممکن است به صورت نادرست نمایش داده شود اگر config.narrator_menu به True تنظیم شده باشد."

    # gui/game/screens.rpy:1354
    old "## This controls the maximum number of NVL-mode entries that can be displayed at once."
    new "## این حداکثر تعداد ورودی‌های NVL-mode که می‌توانند هم‌زمان نمایش داده شوند را کنترل می‌کند."

    # gui/game/screens.rpy:1414
    old "## Bubble screen"
    new "## صفحهٔ ابر"

    # gui/game/screens.rpy:1416
    old "## The bubble screen is used to display dialogue to the player when using speech bubbles. The bubble screen takes the same parameters as the say screen, must create a displayable with the id of \"what\", and can create displayables with the \"namebox\", \"who\", and \"window\" ids."
    new "## صفحهٔ ابر برای نمایش دیالوگ به بازیکن هنگام استفاده از ابرنویسه استفاده می‌شود. صفحهٔ ابر پارامترهای یکسانی با صفحهٔ گفتار می‌گیرد، باید یک displayable با شناسهٔ \"what\"بسازد، و می‌تواند displayableهایی با شناسه‌های \"namebox\"، \"who\"، و \"window\" بسازد."

    # gui/game/screens.rpy:1421
    old "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"
    new "## https://www.renpy.org/doc/html/bubble.html#bubble-screen"

    # gui/game/screens.rpy:1505
    old "## Mobile Variants"
    new "## حالت‌های همراه"

    # gui/game/screens.rpy:1512
    old "## Since a mouse may not be present, we replace the quick menu with a version that uses fewer and bigger buttons that are easier to touch."
    new "## از آن‌جایی که یک موشواره ممکن است موجود نباشد، ما منوی سریع را با یک نسخه که از دکمه‌های کمتر و بزرگ‌تر که برای لمس کردن راحت‌ترند استفاده می‌کنیم."

    # gui/game/screens.rpy:1530
    old "Menu"
    new "منو"
