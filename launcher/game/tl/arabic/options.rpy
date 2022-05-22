
translate arabic strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## هذا الملف يحتوي على الخيارات التي تستطيع تعديلها لتغيير محتويات لعبتك."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## الأسطر التي تبدأ بهذا الشعار مرتين'#' هي أسطر مقتبسه و لا يفترض عليك تغييرها. الأسطر التي تحتوي على '#' واحده هي أسطر برمجة يمكنك الغاء الاقتباس عندها لتفعيلها."

    # options.rpy:10
    old "## Basics"
    new "## الأساسيات"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## الإسم الرسمي للعبه. يتم استعمال هذا السطر كإسم النافذة و يظهرفي واجهة النظام التشغيلية و ملفات حصر الأخطاء."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## رمز _() حول النصوص يجعلها قابلة للترجمة."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "الواجهة التشغيلية القياسية لـ رينباي7"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## يحدد إذا ما تم إظهار العنوان في القائمة الرئيسية. لإخفاء العنوان اجعله False."

    # options.rpy:26
    old "## The version of the game."
    new "## نسخه اللعبة."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. To insert a blank line between paragraphs, write \\n\\n."
    new "## النص الظاهر على شاشة اللعبه. لإظهار سطر فارغ بين اجزاء النص اكتب \\n\\n."

    # options.rpy:37
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## اسم مختصر للعبه يتم استعماله في ملفات التشغيل و نسخ النشر. يجب ان يحتوي على احرف انجليزية فقط, دون فراغات ولا فواصل ولا فواصل منقوطة."

    # options.rpy:44
    old "## Sounds and music"
    new "## الصوت و الموسيقى"

    # options.rpy:46
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## هذه المتغيرات الثلاثة تحدد معالجات الأصوات الظاهره بشكل قياسي للاعب. إلغاء أحدها يجعله يختفي من الواجهة عن طريق اختيار False."

    # options.rpy:55
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## يسمح للاعب ان يسمع صوتا لاختبار ارتفاع الصوت او النطق, إمسح الاقتباس عن السطر التالي ليتم تفعيل زر العينة الصوتية."

    # options.rpy:62
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."

    # options.rpy:69
    old "## Transitions"
    new "## الإنتقال"

    # options.rpy:71
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."

    # options.rpy:75
    old "## Entering or exiting the game menu."
    new "## الدخول او الخروج من قائمة اللعبة."

    # options.rpy:81
    old "## A transition that is used after a game has been loaded."
    new "## الإنتقال الذي يحصل بعد ان تنتهي اللعبة من الإقلاع."

    # options.rpy:86
    old "## Used when entering the main menu after the game has ended."
    new "## يظهر عند الدخول إلى القائمة الرئيسية بعد انتهاء اللعبة."

    # options.rpy:91
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."

    # options.rpy:96
    old "## Window management"
    new "## خيارات النافذة"

    # options.rpy:98
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."

    # options.rpy:103
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."

    # options.rpy:109
    old "## Transitions used to show and hide the dialogue window"
    new "## الإنتقالات البصرية المستخدمه عند إظهار و إخفاء مربع الحوار"

    # options.rpy:115
    old "## Preference defaults"
    new "## الخيارات القياسية"

    # options.rpy:117
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."

    # options.rpy:123
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."

    # options.rpy:129
    old "## Save directory"
    new "## مجلد الحفظ"

    # options.rpy:131
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"

    # options.rpy:134
    old "## Windows: %APPDATA\\RenPy\\<config.save_directory>"
    new "## Windows: %APPDATA\\RenPy\\<config.save_directory>"

    # options.rpy:136
    old "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"
    new "## Macintosh: $HOME/Library/RenPy/<config.save_directory>"

    # options.rpy:138
    old "## Linux: $HOME/.renpy/<config.save_directory>"
    new "## Linux: $HOME/.renpy/<config.save_directory>"

    # options.rpy:140
    old "## This generally should not be changed, and if it is, should always be a literal string, not an expression."
    new "## This generally should not be changed, and if it is, should always be a literal string, not an expression."

    # options.rpy:146
    old "## Icon ########################################################################'"
    new "## أيقونة ########################################################################'"

    # options.rpy:148
    old "## The icon displayed on the taskbar or dock."
    new "## الأيقونة الظاهرة في شريط البرامج."

    # options.rpy:153
    old "## Build configuration"
    new "## معلومات ملف النشر"

    # options.rpy:155
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## هذا الجزء يتحكم بالمعلومات التي يستعملها رينباي لتحويل مشروعك إلى ملفات يمكن نشرها."

    # options.rpy:160
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."

    # options.rpy:165
    old "## In a pattern:"
    new "## In a pattern:"

    # options.rpy:167
    old "## / is the directory separator."
    new "## / is the directory separator."

    # options.rpy:169
    old "## * matches all characters, except the directory separator."
    new "## * matches all characters, except the directory separator."

    # options.rpy:171
    old "## ** matches all characters, including the directory separator."
    new "## ** matches all characters, including the directory separator."

    # options.rpy:173
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."

    # options.rpy:177
    old "## Classify files as None to exclude them from the built distributions."
    new "## Classify files as None to exclude them from the built distributions."

    # options.rpy:185
    old "## To archive files, classify them as 'archive'."
    new "## To archive files, classify them as 'archive'."

    # options.rpy:190
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."

    # options.rpy:196
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."

    # options.rpy:203
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## The username and project name associated with an itch.io project, separated by a slash."

