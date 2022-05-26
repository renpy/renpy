translate arabic strings:
    # game/new_project.rpy:77
    old "{#language name and font}"
    new "{font=DejaVuSans.ttf}العربية{/font}"

    # about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # about.rpy:43
    old "View license"
    new "عرض الرخصة"

    # add_file.rpy:28
    old "FILENAME"
    new "اسم الملف"

    # add_file.rpy:28
    old "Enter the name of the script file to create."
    new "إختر اسم لملف الحوار الذي سيتم تكوينه"

    # add_file.rpy:31
    old "The filename must have the .rpy extension."
    new "يجب ان ينتهي اسم الملف بالصيغة .rpy"

    # add_file.rpy:39
    old "The file already exists."
    new "هذا الملف موجود مسبقاً"

    # add_file.rpy:42
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "رينباي يقوم بتشغيل الملفات المنتهية بـ .rpy تلقائياً. لكي تستعمل هذا الملف, اختر له تبويب وافتحه عبر ملف آخر."

    # android.rpy:30
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "لبناء ملفات الأندرويد, الرجاء تحميل RAPT, ثم فك الضغط عن الملف ووضعه في مجلد رينباي. قد تحتاج لإعادة تشغيل رينباي ليعمل بشكل صحيح."

    # android.rpy:31
    old "An x86 Java Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "تحتاج لنسخة برمجية من جافا تعتمد الـ 32-بت لتستطيع إنشاء ملفات الأندرويد على نظام الوندوز. حزمة JDK تختلف عن JRE, قد تكون الجافا لديك موجوده لكنها تفتقد الـ JDK. \n\n الرجاء {a=http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html}تحميل و تنصيب JDK{/a} ثم إعادة تشغيل رينباي"

    # android.rpy:32
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "حزمة الاندرويد RAPT موجوده, لكنك تحتاج لتنصيب Android SDK قبل ان تبدأ بتجهيز حزم للعمل على اندرويد. الرجاء اختيار تنصيب Android SDK لتستطيع ذلك."

    # android.rpy:33
    old "RAPT has been installed, but a key hasn't been configured. Please create a new key, or restore android.keystore."
    new "حزمة اندرويد RAPT موجوده, لكن المفتاح لم يتم تجهيزه. الرجاء تكوين مفتاح جديد او استرجاع android.keystore"

    # android.rpy:34
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "المشروع الحالي لم يتم تجهيز إعدادته. الرجاء اختيار \"Configure\" لتقوم بتجهيزها قبل بناء الحزمة."

    # android.rpy:35
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "قم باختيار زر \"Build\" لتقوم بتجهيز المشروع الحالي إلى حزمة قابلة للعمل على اندرويد. او قم بربط جهاز اندرويد و اختيار \"Build & Install\" ليتم تنصيبها مباشرة على الجهاز المطلوب."

    # android.rpy:37
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "يقوم بمحاكاة جهاز اندرويد هاتفي محمول. \n\n خاصية اللمس يتم محاكاتها عبر مؤشر الفأره, لكن فقط حين يكون زر الفأره مضغوطاً. زر الخروج يقوم باستدعاء نافذة القائمة الرئيسية, و PageUp هو زر العودة إلى الوراء."

    # android.rpy:38
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "يقوم بمحاكاة جهاز اندرويد تابلت. \n\n خاصية اللمس يتم محاكاتها عبر مؤشر الفأره, لكن فقط حين يكون زر الفأره مضغوطاً. زر الخروج يقوم باستدعاء نافذة القائمة الرئيسية, و PageUp هو زر العودة إلى الوراء"

    # android.rpy:39
    old "Attempts to emulate a televison-based Android console, like the OUYA or Fire TV.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "يحاول محاكاة نظام تلفزيوني للأندرويد مثل جهاز OUYA او Fire TV. \n\n يتم تخطيط الأزرار لعصا التحكم لتناسب ازرار جهاز التحكم عن بعد. Controller input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."

    # android.rpy:41
    old "Downloads and installs the Android SDK and supporting packages. Optionally, generates the keys required to sign the package."
    new "يقوم بتحميل و تنصيب Android SDK والحزم المساندة لها. يعطيك خيار تكوين المفاتيح المطلوبة لتتمكن من استعمال الحزمة."

    # android.rpy:42
    old "Configures the package name, version, and other information about this project."
    new "يقوم بتجهيز إعدادات الحزمة, رقم النسخة, و معلومات أخرى تتعلق بهذا المشروع."

    # android.rpy:43
    old "Opens the file containing the Google Play keys in the editor.\n\nThis is only needed if the application is using an expansion APK. Read the documentation for more details."
    new "يفتح الملف الخاص بمعلومات مفتاح Google Play في محرر النصوص. \n\n هذه الخطوة غير مطلوبة إلا لو كان البرنامج يحتاج إحدى الحوم المساندة expansion APK. الرجاء الإطلاع على ملفات المساعدة للحصول على المزيد من المعلومات."

    # android.rpy:44
    old "Builds the Android package."
    new "يقوم ببناء حزمة للأندرويد."

    # android.rpy:45
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "يقوم ببناء حزمة للأندرويد, ثم يقوم بتنصيبها على جهاز أندرويد المتصل بحاسوبك."

    # android.rpy:46
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "يبني الحزمة الخاصة بالأندرويد و يقوم بتنصيبها على جهاز أندرويد متصل بجهازك, ثم يقوم بإقلاع البرنامج على جهاز الأندرويد."

    # android.rpy:48
    old "Connects to an Android device running ADB in TCP/IP mode."
    new "يتصل بجهاز أندرويد يعمل على نظام ADB عن طريق TCP/IP mode"

    # android.rpy:49
    old "Disconnects from an Android device running ADB in TCP/IP mode."
    new "يفصل الاتصال عن جهاز أندرويد يعمل على نظام ADB عن طريق TCP/IP mode"

    # android.rpy:50
    old "Retrieves the log from the Android device and writes it to a file."
    new "يجلب قائمة المهام من جعاز الأندرويد و يكتبها في ملف."

    # android.rpy:240
    old "Copying Android files to distributions directory."
    new "يتم الآن نسخ ملفات الأندرويد إلى المجلد الخاص بالنشر"

    # android.rpy:304
    old "Android: [project.current.name!q]"
    new "أندرويد: [project.current.name!q]"

    # android.rpy:324
    old "Emulation:"
    new "محاكاة"

    # android.rpy:333
    old "Phone"
    new "هاتف"

    # android.rpy:337
    old "Tablet"
    new "تابلت/ لوحي"

    # android.rpy:341
    old "Television"
    new "تلفاز"

    # android.rpy:353
    old "Build:"
    new "بناء"

    # android.rpy:361
    old "Install SDK & Create Keys"
    new "تنصيب SDK و اختلاق مفاتيح"

    # android.rpy:365
    old "Configure"
    new "إعدادات"

    # android.rpy:369
    old "Build Package"
    new "بناء الحزمة"

    # android.rpy:373
    old "Build & Install"
    new "بناء و تنصيب"

    # android.rpy:377
    old "Build, Install & Launch"
    new "بناء,تنصيب و إقلاع."

    # android.rpy:388
    old "Other:"
    new "آخر:"

    # android.rpy:396
    old "Remote ADB Connect"
    new "الإتصال عن بعد عن طريق ADB"

    # android.rpy:400
    old "Remote ADB Disconnect"
    new "قطع إتصال ADB عن بعد"

    # android.rpy:404
    old "Logcat"
    new "Logcat"

    # android.rpy:437
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "قبل ان تصتطيع إنشاء ملفات للأندرويد, عليك ان تقوم بتحميل ملفات RAPT الخاصة بتحويل ملفات رينباي للأندرويد. هل تريد ان تقوم بتحميل الحزمة الآن؟"

    # android.rpy:496
    old "Remote ADB Address"
    new "عنوان ADB عن بعد"

    # android.rpy:496
    old "Please enter the IP address and port number to connect to, in the form \"192.168.1.143:5555\". Consult your device's documentation to determine if it supports remote ADB, and if so, the address and port to use."
    new "الرجاء إدخال عنوان الأي بي ورقم المنفذ المطلوب للإتصال, على شكل \"192.168.1.143:5555\". الرجاء العودة لدليل المستخدم الخاص بجهازك لتعرف إن كان يدعم الإتصال عن بعد للـ ADB و إن كان قادراً على ذلك, ستجد العنوان و المنفذ المطلوبان."

    # android.rpy:508
    old "Invalid remote ADB address"
    new "عنوان ِADB خاطيء"

    # android.rpy:508
    old "The address must contain one exactly one ':'."
    new "العنوان يجب ان يحتوي على علامة ':' واحده فقط لا غير"

    # android.rpy:512
    old "The host may not contain whitespace."
    new "الخادم يجب ان لا يحتوي على مساحات فارغة"

    # android.rpy:518
    old "The port must be a number."
    new "يجب ان يكون العنوان مكون من أرقام فقط"

    # android.rpy:544
    old "Retrieving logcat information from device."
    new "يتم النسخ من الجهاز لمعلومات Logcat"

    # choose_directory.rpy:73
    old "Ren'Py was unable to run python with tkinter to choose the directory. Please install the python-tk or tkinter package."
    new "لم يتمكن رينباي من تشغيل بايثون باستخدام tkinter لاختيار المجلد. الرجال تنصيب حزمة tkinter أو python-tk."

    # choose_theme.rpy:303
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "لم يتمكن رينباي من تغيير المظهر, ربما ملف options.rpy قد تغير بشكل كبير"

    # choose_theme.rpy:370
    old "Planetarium"
    new "Planetarium"

    # choose_theme.rpy:425
    old "Choose Theme"
    new "إختر المظهر"

    # choose_theme.rpy:438
    old "Theme"
    new "المظهر"

    # choose_theme.rpy:463
    old "Color Scheme"
    new "توليفة الألوان"

    # choose_theme.rpy:495
    old "Continue"
    new "استمرار"

    # consolecommand.rpy:84
    old "INFORMATION"
    new "معلومات"

    # consolecommand.rpy:84
    old "The command is being run in a new operating system console window."
    new "The command is being run in a new operating system console window."

    # distribute.rpy:443
    old "Scanning project files..."
    new "يتم فحص الملفات..."

    # distribute.rpy:459
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "فشل بناء ملفات النشر. build.directory_name يجب أن لا يحتوي على مساحات فارغة, فواصل, او فواصل منقوطة في إسم المجلد "

    # distribute.rpy:504
    old "No packages are selected, so there's nothing to do."
    new "لم يتم اختيار اي حزمة, لم يحصل اي شيء."

    # distribute.rpy:516
    old "Scanning Ren'Py files..."
    new "يتم فحص ملفات رينباي..."

    # distribute.rpy:569
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "تم الإنتهاء من تكوين رزمة البيانات لنشر اللعبة. بسبب اختلاف نظام الملفات في الأنظمة التشغيلية ماك و لينوكس, لا يمكن فك الضغط عن الرزمة الخاصة بتلك الأنظمة على نظام وندوز."

    # distribute.rpy:752
    old "Archiving files..."
    new "يتم أرشفة الملفات..."

    # distribute.rpy:1050
    old "Unpacking the Macintosh application for signing..."
    new "Unpacking the Macintosh application for signing..."

    # distribute.rpy:1060
    old "Signing the Macintosh application..."
    new "Signing the Macintosh application..."

    # distribute.rpy:1082
    old "Creating the Macintosh DMG..."
    new "Creating the Macintosh DMG..."

    # distribute.rpy:1091
    old "Signing the Macintosh DMG..."
    new "Signing the Macintosh DMG..."

    # distribute.rpy:1248
    old "Writing the [variant] [format] package."
    new "يتم كتابة ملفات [variant] [format]"

    # distribute.rpy:1261
    old "Making the [variant] update zsync file."
    new "Making the [variant] update zsync file."

    # distribute.rpy:1404
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "تم انهاء {b}[complete]{/b} من عدد {b}[total]{/b} من الملفات."

    # distribute_gui.rpy:157
    old "Build Distributions: [project.current.name!q]"
    new "تجميع الملفات تجهيزاً للنشر: [project.current.name!q]"

    # distribute_gui.rpy:171
    old "Directory Name:"
    new "اسم المجلد:"

    # distribute_gui.rpy:175
    old "Executable Name:"
    new "اسم الملف التشغيلي:"

    # distribute_gui.rpy:185
    old "Actions:"
    new "الأوامر:"

    # distribute_gui.rpy:193
    old "Edit options.rpy"
    new "تحرير options.rpy"

    # distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "إضافة بند 'مِن' إلى أمر الجلب, مرة واحدة"

    # distribute_gui.rpy:195
    old "Refresh"
    new "إعادة تحميل"

    # distribute_gui.rpy:199
    old "Upload to itch.io"
    new "تحميل المشروع إلى itch.io"

    # distribute_gui.rpy:215
    old "Build Packages:"
    new "بناء الحزمة البيانية:"

    # distribute_gui.rpy:234
    old "Options:"
    new "خيارات:"

    # distribute_gui.rpy:239
    old "Build Updates"
    new "بناء تحديثات:"

    # distribute_gui.rpy:241
    old "Add from clauses to calls"
    new "إضافة بنود 'مِن' إلى أمر الجلب"

    # distribute_gui.rpy:242
    old "Force Recompile"
    new "إعادة حزم الملفات"

    # distribute_gui.rpy:246
    old "Build"
    new "بناء"

    # distribute_gui.rpy:250
    old "Adding from clauses to call statements that do not have them."
    new "إضافة بنود 'مِن' إلى أوامر الجلب التي لا تحتوي عليها."

    # distribute_gui.rpy:271
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "تم ايجاد بعض الاخطاء في المشروع. الرجاء التأكد من خلو المشروع من الأخطاء قبل نشره بشكل نهائي."

    # distribute_gui.rpy:288
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "مشروعك يخلو من معلومات النشر, هل ترغب في إضافة هذه المعلومات في نهاية ملف options.rpy؟"

    # editor.rpy:150
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input."
    new "{b}نقترح.{/b} محرر نص له واجهة سهلة الاستعمال ويعين على كتابة النصوص البرمجية يفضل برنامج يحتوي على مدقق لغوي. Editraحالياً لا يدعم اللغات الأجنبية مثل اللغه الكورية و الصينية و اليابانية."

    # editor.rpy:151
    old "{b}Recommended.{/b} A beta editor with an easy to use interface and features that aid in development, such as spell-checking. Editra currently lacks the IME support required for Chinese, Japanese, and Korean text input. On Linux, Editra requires wxPython."
    new "{b}نقترح.{/b} محرر نص له واجهة سهلة الاستعمال ويعين على كتابة النصوص البرمجية يفضل برنامج يحتوي على مدقق لغوي. Editraحالياً لا يدعم اللغات الأجنبية مثل اللغه الكورية و الصينية و اليابانية. على نظام لينوكس, Editra يحتاج wxPython."

    # editor.rpy:167
    old "This may have occured because wxPython is not installed on this system."
    new "قد يكون سبب ذلك ان wxPython غير موجود في نظام التشغيل لديك"

    # editor.rpy:169
    old "Up to 22 MB download required."
    new "مطلوب تحميل ملف بحجم  22 ميغا بايت."

    # editor.rpy:182
    old "A mature editor that requires Java."
    new "محرر متخصص يستعمل لغة جافا"

    # editor.rpy:182
    old "1.8 MB download required."
    new "مطلوب تحميل ملف بحجم 1.8 ميغا بايت."

    # editor.rpy:182
    old "This may have occured because Java is not installed on this system."
    new "قد يكون السبب ان الجافا غير موجوده على هذا الجهاز."

    # editor.rpy:191
    old "Invokes the editor your operating system has associated with .rpy files."
    new "يقوم بفتح البرنامج المسؤول عن تحرير ملفات .rpy في نظامك التشغيلي"

    # editor.rpy:207
    old "Prevents Ren'Py from opening a text editor."
    new "يمنع رينباي من فتح اي محرر نصوص"

    # editor.rpy:359
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "حصل استثناء اثناء فتح المحرر: \n[exception!q]"

    # editor.rpy:457
    old "Select Editor"
    new "الرجاء اختيار المحرر"

    # editor.rpy:472
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "محرر النصوص هو برنامج يساعدك على تعديل ملفات رينباي البرمجية والحوار. هنا, يمكنك اختيار المحرر الذي سيستعلمه رينباي. إذا لم يكن لديك مسبقاً, سيتم تحميله و تنصيبه بشكل اوتوماتيكي."

    # editor.rpy:494
    old "Cancel"
    new "إلغاء الأمر"

    # front_page.rpy:35
    old "Open [text] directory."
    new "فتح المجلد [text]"

    # front_page.rpy:93
    old "refresh"
    new "إعادة تحميل"

    # front_page.rpy:120
    old "+ Create New Project"
    new "+ إبدأ مشروعاً جديداً"

    # front_page.rpy:130
    old "Launch Project"
    new "تشغيل المشروع"

    # front_page.rpy:147
    old "[p.name!q] (template)"
    new "[p.name!q] (template)"

    # front_page.rpy:149
    old "Select project [text]."
    new "اختر المشروع [text]"

    # front_page.rpy:165
    old "Tutorial"
    new "الدليل العملي"

    # front_page.rpy:166
    old "The Question"
    new "السؤال"

    # front_page.rpy:182
    old "Active Project"
    new "المشروع الحالي"

    # front_page.rpy:190
    old "Open Directory"
    new "فتح مجلد"

    # front_page.rpy:195
    old "game"
    new "اللعبة"

    # front_page.rpy:196
    old "base"
    new "المشروع كله"

    # front_page.rpy:197
    old "images"
    new "الصور"

    # front_page.rpy:198
    old "gui"
    new "الواجهة"

    # front_page.rpy:204
    old "Edit File"
    new "تحرير ملف"

    # front_page.rpy:214
    old "All script files"
    new "جميع الملفات النصية"

    # front_page.rpy:223
    old "Navigate Script"
    new "مهام إضافية"

    # front_page.rpy:234
    old "Check Script (Lint)"
    new "فحص الملف (لينت)"

    # front_page.rpy:237
    old "Change/Update GUI"
    new "نغيير او تحديث الواجهة"

    # front_page.rpy:239
    old "Change Theme"
    new "تغيير المظهر"

    # front_page.rpy:242
    old "Delete Persistent"
    new "حذف الملفات المؤقتة"

    # front_page.rpy:251
    old "Build Distributions"
    new "تجميع المشروع للنشر"

    # front_page.rpy:253
    old "Android"
    new "أندرويد"

    # front_page.rpy:254
    old "iOS"
    new "iOS نظام تشغيل"

    # front_page.rpy:255
    old "Generate Translations"
    new "تجهيز ملفات للترجمة"

    # front_page.rpy:256
    old "Extract Dialogue"
    new "استخراج النص"

    # front_page.rpy:272
    old "Checking script for potential problems..."
    new "يتم فحص الملفات لأي اخطاء محتملة..."

    # front_page.rpy:287
    old "Deleting persistent data..."
    new "يتم الآن حذف الملفات المؤقتة "

    # front_page.rpy:295
    old "Recompiling all rpy files into rpyc files..."
    new "يتم إعادة حزم الملفات من صيغة rpy إلى rpyc..."

    # gui7.rpy:236
    old "Select Accent and Background Colors"
    new "اختر لون الخلفية و المجموعة اللونية"

    # gui7.rpy:250
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "الرجاء اختيار الألوان التي ترغب بها ثم اضغط زر الاستمرار, ستتمكن من تغيير هذه الالوان لاحقا."

    # gui7.rpy:294
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"

    # gui7.rpy:294
    old "Choose new colors, then regenerate image files."
    new "اختر الوان جديدة ثم أعد تكوين ملفات الصور لتطابق اللون الذي اخترته."

    # gui7.rpy:294
    old "Regenerate the image files using the colors in gui.rpy."
    new "يقوم بإعادة تكوين الصور حسب الألوان التي تم وضعها في ملف gui.rpy."

    # gui7.rpy:314
    old "PROJECT NAME"
    new "اسم المشروع"

    # gui7.rpy:314
    old "Please enter the name of your project:"
    new "الرجاء اختيار اسم لمشروعك الجديد"

    # gui7.rpy:322
    old "The project name may not be empty."
    new "لا يمكن ان يكون اسم المشروع فارغاً"

    # gui7.rpy:327
    old "[project_name!q] already exists. Please choose a different project name."
    new "الاسم [project_name!q] يوجد مسبقاً, الرجاء اختيار اسم مختلف."

    # gui7.rpy:330
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] يوجد مسبقاً, الرجاء اختيار اسم مختلف."

    # gui7.rpy:341
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    new "ما هو الحجم المطلوب للمشروع؟ رينباي يستطيع تكبير و تصغير حجم النافذة لتناسب الشاشة, لكن الحجم الذي ستختاره هنا هو الحجم القياسي, و الذي ستظهر فيه الصور و الشخصيات في أوضح شكل لها. \n\n الحجم الذي يناسب اغلب الشاشات هو 1280×730 بكسل."

    # gui7.rpy:389
    old "Creating the new project..."
    new "يتم الآن تكوين المشروع الجديد..."

    # gui7.rpy:391
    old "Updating the project..."
    new "يتم الآن تحديث معلومات المشروع..."

    # interface.rpy:107
    old "Documentation"
    new "المستندات المرفقة"

    # interface.rpy:108
    old "Ren'Py Website"
    new "موقع رينباي"

    # interface.rpy:109
    old "Ren'Py Games List"
    new "قائمة ألعاب رينباي"

    # interface.rpy:117
    old "update"
    new "تحديث"

    # interface.rpy:119
    old "preferences"
    new "خيارات"

    # interface.rpy:120
    old "quit"
    new "خروج"

    # interface.rpy:232
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "بسبب محدودية التجميع, الاحرف الغير لاتينيه غير مسموح بها في اسم الملف او المجلدات"

    # interface.rpy:327
    old "ERROR"
    new "خطأ"

    # interface.rpy:356
    old "While [what!qt], an error occured:"
    new "حصل خطأ أثناء [what!qt]"

    # interface.rpy:356
    old "[exception!q]"
    new "[exception!q]"

    # interface.rpy:375
    old "Text input may not contain the {{ or [[ characters."
    new "لا يمكن استعمال الرمزان {{ و ]] هنا"

    # interface.rpy:380
    old "File and directory names may not contain / or \\."
    new "غير مسموح ان يحتوي اسم الملف او المجلد على الرمزان / أو \\"

    # interface.rpy:386
    old "File and directory names must consist of ASCII characters."
    new "اسم الملف و المجلدات التي تحتويه يجب ان تكون مكتوبة بأحرف ASCII "

    # interface.rpy:454
    old "PROCESSING"
    new "يتم إجراء العمليات"

    # interface.rpy:471
    old "QUESTION"
    new "سؤال"

    # interface.rpy:484
    old "CHOICE"
    new "إختيار"

    # ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "لبناء حزم الـ iOS, الرجاء تحميل البرنامج الخاص بذلك renios و فك الضغط عنه, ثم وضعه في مجلد رينباي الرئيسي. بعد ذلك قم بإعادة تشغيل رينباي."

    # ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "لم يتم اختيار المسار الذي سيتم وضع Xcode فيه. الرجاء ضغط زر اختيار المجلد لاختيار المكان الصحيح."

    # ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "لا يوجد مشروع Xcode متطابق مع مشروع رينباي الحالي. الرجاء اختيار زر 'صنع مشروع Xcode' لبدء واحد."

    # ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "يوجد مشروع Xcode. لتحديثه قم بضغط زر 'تحديث مشروع Xcode' ليصبح متطابقاً مع آخر التعديلات على اللعبة’ او قم باستعمال Xcode للبناء و التنصيب."

    # ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "يقوم بمحاكاة جهاز أيفون. اللمس يتم محاكاته عن طريق الضغط بالزر الأيسر للفأرة."

    # ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "يقوم بمحاكاة جهاز أيفون. اللمس يتم محاكاته عن طريق الضغط بالزر الأيسر للفأرة."

    # ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "إختر المجلد الذي سيكون فيه مشروع Xcode."

    # ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "يقوم بصنع مشروع Xcode متطابق مع مشروع رينباي الحالي."

    # ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "يقوم بتحديث مشروع Xcode ليصبح متطابقاً مع ملفات اللعبة. يجب أن يتم تكرار هذه العملية مع كل تغيير في اللعبة."

    # ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "يقوم بفتح مشروع Xcode في Xcode."

    # ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "يقوم بفتح المجلد الموجود فيه مشاريع Xcode."

    # ios.rpy:126
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "مشروع Xcode موجود مسبقاً. هل تريد تغيير إسم المشروع القديم, و استبداله بالجديد؟"

    # ios.rpy:211
    old "iOS: [project.current.name!q]"
    new "iOS: [project.current.name!q]"

    # ios.rpy:240
    old "iPhone"
    new "أيفون"

    # ios.rpy:244
    old "iPad"
    new "أيباد"

    # ios.rpy:264
    old "Select Xcode Projects Directory"
    new "إختر مسار مشاريع Xcode"

    # ios.rpy:268
    old "Create Xcode Project"
    new "صنع مشروع Xcode"

    # ios.rpy:272
    old "Update Xcode Project"
    new "تحديث مشروع Xcode"

    # ios.rpy:277
    old "Launch Xcode"
    new "إقلاع Xcode"

    # ios.rpy:312
    old "Open Xcode Projects Directory"
    new "فتح مجلد مشاريع Xcode"

    # ios.rpy:345
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "قبل صنع الحزم الخاصة ببرامج iOS يجب ان تقوم بتحميل برنامج renios المساند لرينباي على اجهزة أبل. هل تريد تحميل renios الآن؟"

    # ios.rpy:354
    old "XCODE PROJECTS DIRECTORY"
    new "مسار مشاريع Xcode"

    # ios.rpy:354
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "الرجاء إختيار المجلد الذي سيتم وضع مشاريع Xcode فيه باستخدام نافذة اختيار المجلد. قد تكون النافذة مفتوحة خلف هذه النافذة."

    # ios.rpy:359
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "رينباي قام بتحديد مجلد مشاريع Xcode إلى:"

    # itch.rpy:60
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "لم يتمكن رينباي من ايجاد حزمة المشروع الجاهزة للرفع, الرجاء ضغط زر البناء و المحاولة مجدداَ."

    # itch.rpy:91
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "لم يتمكن رينباي من ايجاد ملفات جاهزة للرفع. الرجاء ضغط زر البناء و المحاولة مجدداَ."

    # itch.rpy:99
    old "The butler program was not found."
    new "The butler program was not found."

    # itch.rpy:99
    old "Please install the itch.io app, which includes butler, and try again."
    new "Please install the itch.io app, which includes butler, and try again."

    # itch.rpy:108
    old "The name of the itch project has not been set."
    new "لم تقم باختيار اسم للمشروع للرفع على itch."

    # itch.rpy:108
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."

    # mobilebuild.rpy:109
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # navigation.rpy:168
    old "Navigate: [project.current.name]"
    new "الذهاب إلى: [project.current.name]"

    # navigation.rpy:177
    old "Order: "
    new "الترتيب:"

    # navigation.rpy:178
    old "alphabetical"
    new "أبجدي"

    # navigation.rpy:180
    old "by-file"
    new "ملف ملف"

    # navigation.rpy:182
    old "natural"
    new "طبيعي"

    # navigation.rpy:194
    old "Category:"
    new "فئة:"

    # navigation.rpy:196
    old "files"
    new "ملفات"

    # navigation.rpy:197
    old "labels"
    new "وسم"

    # navigation.rpy:198
    old "defines"
    new "تحديد"

    # navigation.rpy:199
    old "transforms"
    new "التحول"

    # navigation.rpy:200
    old "screens"
    new "النوافذ"

    # navigation.rpy:201
    old "callables"
    new "ما يمكن استجلابه"

    # navigation.rpy:202
    old "TODOs"
    new "TODOs"

    # navigation.rpy:241
    old "+ Add script file"
    new "+إضافة ملف نص"

    # navigation.rpy:249
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."

    # navigation.rpy:256
    old "The list of names is empty."
    new "قائمة الأسماء فارغة"

    # new_project.rpy:38
    old "New GUI Interface"
    new "واجهة المستخدم الجديدة"

    # new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "تمت ترجمة كلا الواجهتين إلى اللغة التي قمت باختيارها."

    # new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "تمت ترجمة الواجهة الجديدة فقط إلى اللغه التي قمت باختيارها."

    # new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "تمت ترجمة الواجهة القديمة فقط إلى اللغه التي قمت باختيارها."

    # new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "لم تتم ترجمة اي من الواجهتين إلى اللغه المطلوبة."

    # new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "لم يتم تحديد مجلد المشاريع, سيتم الإلغاء"

    # new_project.rpy:69
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "أي من الواجهتين ترغب في استخدامه؟ واجهة المستخدم الجديدة تناسب الاجهزة المحمولة وجميع احجام الشاشات, و أسهل في اضافة التفاصيل و التخصيص. الواجهة القديمة قد تكون مهمة للمشاريع التي تم انجازها سابقا.\n\n ان لم تكن متأكدا قم باختيار الواجهة الجديدة ثم اضغط استمرار في الجهة اليمنى السفلى."

    # new_project.rpy:69
    old "Legacy Theme Interface"
    new "واجهة المستخدم القديمة"

    # new_project.rpy:90
    old "Choose Project Template"
    new "الرجاء اختيار تصميم المظهر للمشروع"

    # new_project.rpy:108
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "الرجاء اختيار القالب المطلوب للمشروع الجديد. هذه القوالب تقوم بتجهيز اتجاه النص و اللغه المستخدمة في الواجهة لتسهل عملية البدء. إذا لم تكن لغتك مدعومة الرجاء اختيار اللغة الانجليزية."

    # preferences.rpy:64
    old "Launcher Preferences"
    new "خيارات برنامج التشغيل"

    # preferences.rpy:85
    old "Projects Directory:"
    new "دليل المشاريع:"

    # preferences.rpy:92
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # preferences.rpy:94
    old "Projects directory: [text]"
    new "مجلد المشاريع [text]"

    # preferences.rpy:96
    old "Not Set"
    new "غير محدد"

    # preferences.rpy:111
    old "Text Editor:"
    new "محرر الملفات النصية:"

    # preferences.rpy:117
    old "Text editor: [text]"
    new "محرر النصوص [text]"

    # preferences.rpy:133
    old "Update Channel:"
    new "مصدر التحديثات:"

    # preferences.rpy:153
    old "Navigation Options:"
    new "خيارات استعراض المجلدات"

    # preferences.rpy:157
    old "Include private names"
    new "تضمين الأسماء الخاصة"

    # preferences.rpy:158
    old "Include library names"
    new "تضمين اسماء المكتبات"

    # preferences.rpy:168
    old "Launcher Options:"
    new "خيارات برنامج التشغيل:"

    # preferences.rpy:172
    old "Hardware rendering"
    new "الإستعراض بواسطة قطع الجهاز الداخلية"

    # preferences.rpy:173
    old "Show templates"
    new "عرض القوالب"

    # preferences.rpy:174
    old "Show edit file section"
    new "عرض قسم تعديل الملف"

    # preferences.rpy:175
    old "Large fonts"
    new "خط كبير"

    # preferences.rpy:178
    old "Console output"
    new "الإستعراض بواسطة البرمجيات المتوفرة"

    # preferences.rpy:199
    old "Open launcher project"
    new "فتح الواجهة التشغيلية كمشروع"

    # preferences.rpy:213
    old "Language:"
    new "اللغة:"

    # project.rpy:47
    old "After making changes to the script, press shift+R to reload your game."
    new "عند إجراء أي تغييرات في ملف الحوار, يمكنك ضغط shift+R لترى التغييرات داخل اللعبة"

    # project.rpy:47
    old "Press shift+O (the letter) to access the console."
    new "إضغط shift+O للدخول على لوحة التحكم"

    # project.rpy:47
    old "Press shift+D to access the developer menu."
    new "إضغط shift+D للدخول على لوحة تحكم المبرمج"

    # project.rpy:47
    old "Have you backed up your projects recently?"
    new "هل قمت بعمل نسخة احتياطية من مشاريعك مؤخراً؟"

    # project.rpy:229
    old "Launching the project failed."
    new "لم تنجح محاولة إقلاع المشروع"

    # project.rpy:229
    old "Please ensure that your project launches normally before running this command."
    new "الرجاء التأكد من سلامة إقلاع المشروع قبل تشغيل هذا الأمر البرمجي"

    # project.rpy:242
    old "Ren'Py is scanning the project..."
    new "رينباي يقوم بفحص المشروع"

    # project.rpy:568
    old "Launching"
    new "جاري الإقلاع"

    # project.rpy:597
    old "PROJECTS DIRECTORY"
    new "سياق مجلدات المشاريع"

    # project.rpy:597
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "الرجاء اختيار نسق المشاريع من الصفحة الخاصة بذلك. \n{b}قد تكون النافذة ظهرت خلف هذه النافذة.{/b}"

    # project.rpy:597
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "سيقوم البرنامج بفحص المجلد هذا لإيجاد المشاريع السابقة, أو ليضع المشاريع الجديده فيه, و ايضاً لوضع المشاريع المنتهيه عند تجهيزها للنشر."

    # project.rpy:602
    old "Ren'Py has set the projects directory to:"
    new "رينباي قام بتحديد مجلد المشاريع إلى المكان التالي:"

    # translations.rpy:63
    old "Translations: [project.current.name!q]"
    new "Translations: [project.current.name!q]"

    # translations.rpy:104
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "اختر اللغه التي ستعمل بها. يجب ان يكون اسم اللغه مكتوبا باحرف انجليزية فقط: lower-case ASCII and underscores"

    # translations.rpy:130
    old "Generate empty strings for translations"
    new "صنع خانات فارغة للترجمات"

    # translations.rpy:148
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "يقوم بتكوين او تحديث ملفات الترجمة. سيتم وضع الملفات في game/tl/[persistent.translate_language!q]."

    # translations.rpy:168
    old "Extract String Translations"
    new "استخراج نصوص الترجمة"

    # translations.rpy:170
    old "Merge String Translations"
    new "دمج نصوص الترجمة"

    # translations.rpy:175
    old "Replace existing translations"
    new "استبدال نصوص الترجمة الحالية"

    # translations.rpy:176
    old "Reverse languages"
    new "استبدال لغه بالأخرى"

    # translations.rpy:180
    old "Update Default Interface Translations"
    new "تحديث لغة واجهة رينباي التشغيلية"

    # translations.rpy:200
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "أمر استخراج نصوص الترجمة يقوم بنسخ الأسطر إلى ملف مؤقت. \n\n أمر دمج نصوص الترجمة يقوم باستخراج النصوص إلى مشروع آخر."

    # translations.rpy:224
    old "Ren'Py is generating translations...."
    new "يقوم رينباي بتصنيع ملفات الترجمة..."

    # translations.rpy:235
    old "Ren'Py has finished generating [language] translations."
    new "انتهى رينباي من صناعة ملفات الترجمة إلى [language]"

    # translations.rpy:248
    old "Ren'Py is extracting string translations..."
    new "يقوم رينباي باستخراج ملفات الترجمة..."

    # translations.rpy:251
    old "Ren'Py has finished extracting [language] string translations."
    new "انتهى رينباي من استخراج أسطر الترجمة الخاصة باللغه [language]."

    # translations.rpy:271
    old "Ren'Py is merging string translations..."
    new "يقوم رينباي بدمج اسطر الترجمة..."

    # translations.rpy:274
    old "Ren'Py has finished merging [language] string translations."
    new "انتهى رينباي من دمج أسطر الترجمة الخاصة باللغه [language]."

    # translations.rpy:282
    old "Updating default interface translations..."
    new "يقوم رينباي بتحديث اسطر الترجمة الخاصة بالواجهة التشغيلية..."

    # translations.rpy:306
    old "Extract Dialogue: [project.current.name!q]"
    new "Extract Dialogue: [project.current.name!q]"

    # translations.rpy:322
    old "Format:"
    new "الصيغة:"

    # translations.rpy:330
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Tab-delimited Spreadsheet (dialogue.tab)"

    # translations.rpy:331
    old "Dialogue Text Only (dialogue.txt)"
    new "Dialogue Text Only (dialogue.txt)"

    # translations.rpy:344
    old "Strip text tags from the dialogue."
    new "Strip text tags from the dialogue."

    # translations.rpy:345
    old "Escape quotes and other special characters."
    new "Escape quotes and other special characters."

    # translations.rpy:346
    old "Extract all translatable strings, not just dialogue."
    new "Extract all translatable strings, not just dialogue."

    # translations.rpy:374
    old "Ren'Py is extracting dialogue...."
    new "رينباي يقوم باستخراج الحوار إلى ملف نص"

    # translations.rpy:378
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "انتهى رينباي من استخراج اسطر النص. الحوار الذي تم استخراجه موجود في المجلد الرئيسي للمشروع dialogue.[persistent.dialogue_format]."

    # updater.rpy:75
    old "Select Update Channel"
    new "الرجاء اختيار طريقة التحديث"

    # updater.rpy:86
    old "The update channel controls the version of Ren'Py the updater will download. Please select an update channel:"
    new "طريقة التحديث تحدد لبرنامج رينباي اي المواقع يستخدم لإيجاد النسخ الجديدة. الرجاء اختيار الطريقة التي تناسبك."

    # updater.rpy:91
    old "Release"
    new "نسخة مكتملة"

    # updater.rpy:97
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}موصى به.{/b} نسخة رينباي التي يفضل استعمالها مع كل الالعاب الجديدة."

    # updater.rpy:102
    old "Prerelease"
    new "نسخة مبدأية"

    # updater.rpy:108
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "عينة من نسخة رينباي القادمة تسمح لك بتجربة الإضافات الجديدة. لا ننصح باستعمالها لصناعة ألعاب معدة للنشر."

    # updater.rpy:114
    old "Experimental"
    new "نسخة تجريبية"

    # updater.rpy:120
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "النسخ التجريبية من رينباي. الأفضل ألا تستعمل هذه النسخ إلا لو طلب منك ذلك احد مبرمجي رينباي"

    # updater.rpy:126
    old "Nightly"
    new "مسائي"

    # updater.rpy:132
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "أحدث نسخة طازجة من رينباي التجريبي, قد يحتوي على آخر مستجدات رينباي و قد لا يعمل مطلقاً"

    # updater.rpy:152
    old "An error has occured:"
    new "حصل خطأ:"

    # updater.rpy:154
    old "Checking for updates."
    new "جاري البحث عن تحديثات"

    # updater.rpy:156
    old "Ren'Py is up to date."
    new "نسخة رينباي التي لديك هي الأحدث."

    # updater.rpy:158
    old "[u.version] is now available. Do you want to install it?"
    new "النسخة [u.version] متوفرة, هل ترغب في تنصيبها؟"

    # updater.rpy:160
    old "Preparing to download the update."
    new "يتم التجهيز لتنزيل التحديث."

    # updater.rpy:162
    old "Downloading the update."
    new "يتم تنزيل التحديث."

    # updater.rpy:164
    old "Unpacking the update."
    new "يتم فك الضغط عن التحديث."

    # updater.rpy:166
    old "Finishing up."
    new "يتم ختم العملية"

    # updater.rpy:168
    old "The update has been installed. Ren'Py will restart."
    new "تم تنصيب التحديثات بنجاح, سيتم إعادة تشغيل رينباي الآن."

    # updater.rpy:170
    old "The update has been installed."
    new "تم تنصيب التحديثات."

    # updater.rpy:172
    old "The update was cancelled."
    new "تم إلغاء التحديث."

    # updater.rpy:189
    old "Ren'Py Update"
    new "تحديثات رينباي."

    # updater.rpy:195
    old "Proceed"
    new "استمرار"
