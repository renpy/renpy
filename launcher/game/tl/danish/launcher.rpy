translate danish strings:

    # game/about.rpy:39
    old "[version!q]"
    new "[version!q]"

    # game/about.rpy:43
    old "View license"
    new "Vis licens"

    # game/add_file.rpy:28
    old "FILENAME"
    new "FILNAVN"

    # game/add_file.rpy:28
    old "Enter the name of the script file to create."
    new "Indtast navnet på den manuskriptfil, der oprettes."

    # game/add_file.rpy:37
    old "The file name may not be empty."
    new "Filnavnet må ikke være tomt."

    # game/add_file.rpy:41
    old "The filename must have the .rpy extension."
    new "Filnavnet skal have .rpy-filendelsen."

    # game/add_file.rpy:50
    old "The file already exists."
    new "Filen eksisterer allerede."

    # game/add_file.rpy:61
    old "# Ren'Py automatically loads all script files ending with .rpy. To use this\n# file, define a label and jump to it from another file.\n"
    new "# Ren'Py indlæser automatisk alle manuskriptfiler, der ender på .rpy. For at\n# bruge denne fil, så definer et mærkat og spring til det fra en anden fil.\n"

    # game/android.rpy:36
    old "To build Android packages, please download RAPT, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Hent venligst RAPT, udpak det og placer det i Ren'Py-mappen for at bygge Android-pakker. Genstart derefter Ren'Py-launcheren."

    # game/android.rpy:37
    old "A 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit is required to build Android packages on Windows. The JDK is different from the JRE, so it's possible you have Java without having the JDK.\n\nPlease {a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}download and install the JDK{/a}, then restart the Ren'Py launcher."
    new "En 64-bit/x64 Java [JDK_REQUIREMENT] Development Kit er nødvendigt for at bygge Android-pakker på Windows. JDK'et er forskelligt fra JRE'en, så det er muligt, at du har Java uden at have JDK'et.\n\n{a=https://www.renpy.org/jdk/[JDK_REQUIREMENT]}Hent og installér{/a} venligst JDK'et og genstart derefter Ren'Py-launcheren."

    # game/android.rpy:38
    old "RAPT has been installed, but you'll need to install the Android SDK before you can build Android packages. Choose Install SDK to do this."
    new "RAPT er blevet installeret, men du skal installere Android-SDK'et, før du kan fremstille Android-pakker. Vælg Installér SDK for at gøre dette."

    # game/android.rpy:39
    old "RAPT has been installed, but a key hasn't been configured. Please generate new keys, or copy android.keystore and bundle.keystore to the base directory."
    new "RAPT er blevet installeret, men en nøgle er ikke blevet konfigureret. Generér venæigt nye nøgler eller kopiér android.keystore og bundle.keystore til grundmappen."

    # game/android.rpy:40
    old "The current project has not been configured. Use \"Configure\" to configure it before building."
    new "Det nuværende projekt er ikke blevet konfigureret. Brug \"Konfigurer\" til at konfigurere det før fremstilling."

    # game/android.rpy:41
    old "Please select if you want a Play Bundle (for Google Play), or a Universal APK (for sideloading and other app stores)."
    new "Vælg venligst, om du vil have et Play-bundle (til Google Play) eller en universel APK (til sideindlæsning og andre appbutikker)."

    # game/android.rpy:42
    old "Choose \"Build\" to build the current project, or attach an Android device and choose \"Build & Install\" to build and install it on the device."
    new "Vælg \"Fremstil\" for at fremstille det nuværende projekt eller kobl en Android-enhed til og vælg \"Fremstil & installér\" for at fremstille og installere det på enheden."

    # game/android.rpy:44
    old "Attempts to emulate an Android phone.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Forsøger at emulere en Android-mobil.\n\nTouch-input emuleres gennem musen, men kun når knappen holdes nede. Escape er kortlagt til menuknappen og PageUp er kortlagt til tilbage-knappen."

    # game/android.rpy:45
    old "Attempts to emulate an Android tablet.\n\nTouch input is emulated through the mouse, but only when the button is held down. Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Forsøger at emulere en Android-tablet.\n\nTouch-input emuleres gennem musen, men kun når knappen holdes nede. Escape er kortlagt til menuknappen og PageUp er kortlagt til tilbage-knappen."

    # game/android.rpy:46
    old "Attempts to emulate a televison-based Android console.\n\nController input is mapped to the arrow keys, Enter is mapped to the select button, Escape is mapped to the menu button, and PageUp is mapped to the back button."
    new "Forsøger at emulere en tv-baseret Android-konsol.\n\nControllerinput er kortlagt til piltasterne, Retur er kortlagt til vælg-knappen, Escape er kortlagt til menuknappen og PageUp er kortlagt til tilbage-knappen."

    # game/android.rpy:48
    old "Downloads and installs the Android SDK and supporting packages."
    new "Henter og installerer Android-SDK'et og understøttende pakker."

    # game/android.rpy:49
    old "Generates the keys required to sign the package."
    new "Genererer nøglerne, der er påkrævet til signering af pakken."

    # game/android.rpy:50
    old "Configures the package name, version, and other information about this project."
    new "Konfigurerer pakkenavnet, -versionen og anden information om dette projekt."

    # game/android.rpy:51
    old "Builds the Android package."
    new "Fremstiller Android-pakken."

    # game/android.rpy:52
    old "Builds the Android package, and installs it on an Android device connected to your computer."
    new "Fremstiller Android-pakken og installerer den på en Android-enhed forbundet til din computer."

    # game/android.rpy:53
    old "Builds the Android package, installs it on an Android device connected to your computer, then launches the app on your device."
    new "Fremstiller Android-pakken, installerer den på en Android-enhed forbundet til din computer og opstarter derefter appen på din enhed."

    # game/android.rpy:55
    old "Retrieves the log from the Android device and writes it to a file."
    new "Indhenter loggen fra Android-enheden og skriver den til en fil."

    # game/android.rpy:56
    old "Lists the connected devices."
    new "Oplister de tilsluttede enheder."

    # game/android.rpy:57
    old "Pairs with a device over Wi-Fi, on Android 11+."
    new "Parrer med en enhed over wi-fi på Android 11+."

    # game/android.rpy:58
    old "Connects to a device over Wi-Fi, on Android 11+."
    new "Forbinder til en enhed over wi-fi på Android 11+."

    # game/android.rpy:59
    old "Disconnects a device connected over Wi-Fi."
    new "Frakobler en enhed forbundet over wi-fi."

    # game/android.rpy:61
    old "Removes Android temporary files."
    new "Fjerner midlertidige Android-filer."

    # game/android.rpy:63
    old "Builds an Android App Bundle (ABB), intended to be uploaded to Google Play. This can include up to 2GB of data."
    new "Fremstiller et Android-appbundle (ABB) tilsigtet at blive lagt op på Google Play. Dette kan indeholde op til 2GB data."

    # game/android.rpy:64
    old "Builds a Universal APK package, intended for sideloading and stores other than Google Play. This can include up to 2GB of data."
    new "Fremstiller en universel APK-pakke tilsigtet til sideindlæsning og butikker udover Google Play. Denne kan indeholde op til 2GB data."

    # game/android.rpy:258
    old "Copying Android files to distributions directory."
    new "Kopierer Android-filer til distributionsmappe."

    # game/android.rpy:327
    old "Android: [project.current.display_name!q]"
    new "Android: [project.current.display_name!q]"

    # game/android.rpy:347
    old "Emulation:"
    new "Emulering:"

    # game/android.rpy:356
    old "Phone"
    new "Mobil"

    # game/android.rpy:360
    old "Tablet"
    new "Tablet"

    # game/android.rpy:364
    old "Television"
    new "Tv"

    # game/android.rpy:376
    old "Build:"
    new "Fremstil:"

    # game/android.rpy:383
    old "Install SDK"
    new "Installér SDK"

    # game/android.rpy:387
    old "Generate Keys"
    new "Generér nøgler"

    # game/android.rpy:391
    old "Configure"
    new "Konfigurer"

    # game/android.rpy:397
    old "Play Bundle"
    new "Play Bundle"

    # game/android.rpy:402
    old "Universal APK"
    new "Universel APK"

    # game/android.rpy:409
    old "Build Package"
    new "Fremstil pakke"

    # game/android.rpy:413
    old "Build & Install"
    new "Fremstil & installér"

    # game/android.rpy:417
    old "Build, Install & Launch"
    new "Fremstil, installér & start op"

    # game/android.rpy:423
    old "Force Recompile"
    new "Gennemtving genkompilering"

    # game/android.rpy:440
    old "Other:"
    new "Andet:"

    # game/android.rpy:448
    old "Logcat"
    new "Logcat"

    # game/android.rpy:452
    old "List Devices"
    new "Oplist enheder"

    # game/android.rpy:456
    old "Wi-Fi Debugging Pair"
    new "Problemløsning af wi-fi-parring"

    # game/android.rpy:460
    old "Wi-Fi Debugging Connect"
    new "Problemløsning af wi-fi-forbindelse"

    # game/android.rpy:464
    old "Wi-Fi Debugging Disconnect"
    new "Problemløsning af wi-fi-frakobling"

    # game/android.rpy:468
    old "Clean"
    new "Opryd"

    # game/android.rpy:493
    old "Before packaging Android apps, you'll need to download RAPT, the Ren'Py Android Packaging Tool. Would you like to download RAPT now?"
    new "Før pakning af Android-apps skal du hente RAPT, Ren'Pys Android-pakningsværktøjet. Vil du gerne hente RAPT nu?"

    # game/android.rpy:554
    old "Retrieving logcat information from device."
    new "Indhenter logcar-information fra enheden."

    # game/android.rpy:573
    old "Wi-Fi Pairing Code"
    new "Wi-fi-parringskode"

    # game/android.rpy:573
    old "If supported, this can be found in 'Developer options', 'Wireless debugging', 'Pair device with pairing code'."
    new "Hvis understøttet kan dette findes i 'Udviklerindstillinger', 'Trådløs problemløsning', 'Par enhed med parringskode'."

    # game/android.rpy:580
    old "Pairing Host & Port"
    new "Parrer vært & port"

    # game/android.rpy:596
    old "IP Address & Port"
    new "IP-adresse & -port"

    # game/android.rpy:596
    old "If supported, this can be found in 'Developer options', 'Wireless debugging'."
    new "Hvis understøttet kan dette findes i 'Udviklerindstillinger', 'Trådløs problemløsning'."

    # game/android.rpy:612
    old "This can be found in 'List Devices'."
    new "Dette kan findes i 'Oplist enheder'."

    # game/android.rpy:632
    old "Cleaning up Android project."
    new "Rypper op i Android-projekt."

    # game/androidstrings.rpy:7
    old "{} is not a directory."
    new "{} er ikke en mappe."

    # game/androidstrings.rpy:8
    old "{} does not contain a Ren'Py game."
    new "{} indeholder ikke et Ren'Py-spil."

    # game/androidstrings.rpy:10
    old "Run configure before attempting to build the app."
    new "Kør konfiguation før forsøg på at fremstille appen."

    # game/androidstrings.rpy:11
    old "Updating project."
    new "Opdaterer projekt."

    # game/androidstrings.rpy:12
    old "Creating assets directory."
    new "Opretter mappe med aktiver."

    # game/androidstrings.rpy:13
    old "Packaging internal data."
    new "Pakker intern data."

    # game/androidstrings.rpy:14
    old "I'm using Gradle to build the package."
    new "Jeg bruger Gradle til at fremstille pakken."

    # game/androidstrings.rpy:15
    old "The build seems to have failed."
    new "Fremstillingen ser ud til at have mislykkedes."

    # game/androidstrings.rpy:16
    old "I'm installing the bundle."
    new "Jeg installerer bundlet."

    # game/androidstrings.rpy:17
    old "Installing the bundle appears to have failed."
    new "Installation af bundlet ser ud til at have mislykkedes."

    # game/androidstrings.rpy:18
    old "Launching app."
    new "Opstarter app."

    # game/androidstrings.rpy:19
    old "Launching the app appears to have failed."
    new "Opstart af app synes at være mislykkedes."

    # game/androidstrings.rpy:20
    old "The build seems to have succeeded."
    new "Fremstillingen ser ud til at have lykkedes."

    # game/androidstrings.rpy:21
    old "What is the full name of your application? This name will appear in the list of installed applications."
    new "Hvad er din applikations fulde navn? Dette navn vil forekomme i listen over installerede applikationer."

    # game/androidstrings.rpy:22
    old "What is the short name of your application? This name will be used in the launcher, and for application shortcuts."
    new "Hvad er din applikations korte navn? Dette navn bruges i launcheren og til applikationsgenveje."

    # game/androidstrings.rpy:23
    old "What is the name of the package?\n\nThis is usually of the form com.domain.program or com.domain.email.program. It may only contain ASCII letters and dots. It must contain at least one dot."
    new "Hvad er navnet på pakken?\n\nDette er sædvanligvis i formen com.domæne.program eller com.domæne.email.program. Det må kun indeholde ASCII-tegn og bogstaver. Det skal indeholde mindst ét punktum."

    # game/androidstrings.rpy:24
    old "The package name may not be empty."
    new "Pakkenavnet må ikke være tomt."

    # game/androidstrings.rpy:25
    old "The package name may not contain spaces."
    new "Pakkenavnet må ikke indeholde mellemrum."

    # game/androidstrings.rpy:26
    old "The package name must contain at least one dot."
    new "Pakkenavnet skal indeholde mindst et punktum."

    # game/androidstrings.rpy:27
    old "The package name may not contain two dots in a row, or begin or end with a dot."
    new "Pakkenavnet må ikke indeholde to punktummer i træk eller begynde eller slutte med et punktum."

    # game/androidstrings.rpy:28
    old "Each part of the package name must start with a letter, and contain only letters, numbers, and underscores."
    new "Hver del af pakkenavnet skal begynde med et bogstav og må kun indeholde bogstaver, tal og bundstreger."

    # game/androidstrings.rpy:29
    old "{} is a Java keyword, and can't be used as part of a package name."
    new "{} er et Java-nøgleord og kan ikke bruges som del af pakkenavnet."

    # game/androidstrings.rpy:30
    old "What is the application's version?\n\nThis should be the human-readable version that you would present to a person. It must contain only numbers and dots."
    new "Hvad er applikationens versionsnummer?\n\nDette bør være det menneskelæsbare nummer, som præsenteres for en person. Det må kun indeholde tal og punktummer."

    # game/androidstrings.rpy:31
    old "The version number must contain only numbers and dots."
    new "Versionsnummeret må kun indeholde tal og punktummer."

    # game/androidstrings.rpy:32
    old "How much RAM (in GB) do you want to allocate to Gradle?\nThis must be a positive integer number."
    new "Hvor meget RAM (i GB) vil du allokere til Gradle?\nDette skal være et positivt heltal."

    # game/androidstrings.rpy:33
    old "The RAM size must contain only numbers and be positive."
    new "RAM-størrelsen må kun indeholde tal og skal være positivt."

    # game/androidstrings.rpy:34
    old "How would you like your application to be displayed?"
    new "Hvordan ønsker du, at din applikation vises?"

    # game/androidstrings.rpy:35
    old "In landscape orientation."
    new "I landskabsorientering."

    # game/androidstrings.rpy:36
    old "In portrait orientation."
    new "I portrætorientering."

    # game/androidstrings.rpy:37
    old "In the user's preferred orientation."
    new "I brugerens foretrukne orientering."

    # game/androidstrings.rpy:38
    old "Which app store would you like to support in-app purchasing through?"
    new "Hvilken appbutik vil du understøtte in-app-betalinger gennem?"

    # game/androidstrings.rpy:39
    old "Google Play."
    new "Google Play."

    # game/androidstrings.rpy:40
    old "Amazon App Store."
    new "Amazon App Store."

    # game/androidstrings.rpy:41
    old "Both, in one app."
    new "Begge i én app."

    # game/androidstrings.rpy:42
    old "Neither."
    new "Ingen af dem."

    # game/androidstrings.rpy:43
    old "Do you want to automatically update the Java source code?"
    new "Vil du automatisk opdatere Java-kildekoden?"

    # game/androidstrings.rpy:44
    old "Yes. This is the best choice for most projects."
    new "Ja. Detter er det bedste valg for de fleste projekter."

    # game/androidstrings.rpy:45
    old "No. This may require manual updates when Ren'Py or the project configuration changes."
    new "Nej. Dette kræver muligvis manuelle opdateringer, når Ren'Py eller projektkonfiguationen ædnres."

    # game/androidstrings.rpy:46
    old "Unknown configuration variable: {}"
    new "Ukendt konfigurationsvariabel: {}"

    # game/androidstrings.rpy:47
    old "I'm compiling a short test program, to see if you have a working JDK on your system."
    new "Jeg kompilerer et kort testprogram for at se, om du har et fungerende JDK på dit system."

    # game/androidstrings.rpy:48
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please make sure you installed the 'JavaSoft (Oracle) registry keys'.\n\nWithout a working JDK, I can't continue."
    new "Jeg kunne ikke bruge javac til at kompilere en testfil. Hvis du ikke har installeret Java Development Kit endnu, så hent det venligst fra:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nJDK'et er forskelligt fra JRE'et, så det er muligt, at du har Java uden at have JDK'et. Sørg for, at du har installeret 'JavaSoft (Oracle)'-registernøglerne.\n\nUden et fungerende JDK kan jeg ikke fortsætte."

    # game/androidstrings.rpy:49
    old "The version of Java on your computer does not appear to be JDK 8, which is the only version supported by the Android SDK. If you need to install JDK 8, you can download it from:\n\n{a=https://adoptium.net/?variant=openjdk8}https://adoptium.net/?variant=openjdk8{/a}\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "Versionen af Java på din computer synes ikke at være JDK 8, hvilket er den eneste version understøttet af Android SDK'et. "

    # game/androidstrings.rpy:50
    old "The JDK is present and working. Good!"
    new "JDK'et findes og virker. Godt!"

    # game/androidstrings.rpy:51
    old "The Android SDK has already been unpacked."
    new "Android-SDK'et er allerede blevet udpakket."

    # game/androidstrings.rpy:52
    old "Do you accept the Android SDK Terms and Conditions?"
    new "Accepterer du Android-SDK'ets vilkår og betingelser?"

    # game/androidstrings.rpy:53
    old "I'm downloading the Android SDK. This might take a while."
    new "Jeg henter Android SDK'et. Dette tager muligvis et stykke tid."

    # game/androidstrings.rpy:54
    old "I'm extracting the Android SDK."
    new "Jeg udtrækker Android-SDK'et."

    # game/androidstrings.rpy:55
    old "I've finished unpacking the Android SDK."
    new "Jeg er færdig med at udpakke Android-SDK'et."

    # game/androidstrings.rpy:56
    old "I'm about to download and install the required Android packages. This might take a while."
    new "Jeg skal til at hente og installere de påkrævede Android-pakker. Dette tager muligvis et stykke tid."

    # game/androidstrings.rpy:57
    old "I was unable to accept the Android licenses."
    new "Jeg var ikke i stand til at acceptere Android-licenserne."

    # game/androidstrings.rpy:59
    old "I was unable to install the required Android packages."
    new "Jeg var ikke i stand til at installere de påkrævede Android-pakker."

    # game/androidstrings.rpy:60
    old "I've finished installing the required Android packages."
    new "Jeg er færdig med at installere de påkrævede Android-pakker."

    # game/androidstrings.rpy:61
    old "It looks like you're ready to start packaging games."
    new "Det ser ud til, at du er klar til at gå i gang med at pakke spil."

    # game/androidstrings.rpy:62
    old "Please enter your name or the name of your organization."
    new "Indtast venligst dit navn eller navnet på din organisation."

    # game/androidstrings.rpy:63
    old "I found an android.keystore file in the rapt directory. Do you want to use this file?"
    new "Jeg fandt en android.keystore-fil i rapt-mappen. Vil du bruge denne fil?"

    # game/androidstrings.rpy:64
    old "I can create an application signing key for you. This key is required to create Universal APK for sideloading and stores other than Google Play.\n\nDo you want to create a key?"
    new "Jeg kan oprette en applikationsigneringsnøgle for dig. Denne nøgle er nødvendig for at oprette en universel APK til sideindlæsning og butikker udover Google Play.\n\nVil du gerne oprette en nøgle?"

    # game/androidstrings.rpy:65
    old "I will create the key in the android.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of android.keystore, and keep it in a safe place?"
    new "Jeg opretter nøglen i filen android.keystore.\n\nDu skal sikkerhedskopiere denne fil. Hvis du mister den, vil du ikke være i stand til at opgradere din applikation.\n\nDu skal også opbevare nøglen sikker. Hvis onde personer får fat i denne fil, kan de lave falske udgaver af din applikation og potentielt stjæle dine brugeres data.\n\nLaver du en sikkerhedskopi af android.keystore og opbevarer den på et sikkert sted?"

    # game/androidstrings.rpy:66
    old "\n\nSaying 'No' will prevent key creation."
    new "\n\nHvis du siger 'Nej', forhindres nøgleoprettelse."

    # game/androidstrings.rpy:67
    old "Could not create android.keystore. Is keytool in your path?"
    new "Kunne ikke oprette android.keystore. Er keytool i din filsti?"

    # game/androidstrings.rpy:68
    old "I've finished creating android.keystore. Please back it up, and keep it in a safe place."
    new "Jeg er færdig med at oprette android.keystore. Sikkerhedskopiér den venligst og opbevar den på et sikkert sted."

    # game/androidstrings.rpy:69
    old "I found a bundle.keystore file in the rapt directory. Do you want to use this file?"
    new "Jeg fandt en bundle.keystore-fil i rapt-mappen. Vil du gerne bruge denne fil?"

    # game/androidstrings.rpy:70
    old "I can create a bundle signing key for you. This key is required to build an Android App Bundle (AAB) for upload to Google Play.\n\nDo you want to create a key?"
    new "Jeg kan oprette en bundle-signeringsnøgle til dig. Denne nøgle er nødvendig for at fremstille et Android-appbundle (AAB) til oplægning på Google Play.\n\nVil du gerne oprette en nøgle?"

    # game/androidstrings.rpy:71
    old "I will create the key in the bundle.keystore file.\n\nYou need to back this file up. If you lose it, you will not be able to upgrade your application.\n\nYou also need to keep the key safe. If evil people get this file, they could make fake versions of your application, and potentially steal your users' data.\n\nWill you make a backup of bundle.keystore, and keep it in a safe place?"
    new "Jeg opretter nøglen i filen bundle.keystore.\n\nDu skal sikkerhedskopiere denne fil. Hvis du mister den, vil du ikke være i stand til at opgradere din applikation.\n\nDu skal også opbevare nøglen sikker. Hvis onde personer får fat i denne fil, kan de lave falske udgaver af din applikation og potentielt stjæle dine brugeres data.\n\nLaver du en sikkerhedskopi af bundle.keystore og opbevarer den på et sikkert sted?"

    # game/androidstrings.rpy:73
    old "Could not create bundle.keystore. Is keytool in your path?"
    new "Kunne ikke oprette bundle.keystore. Er keytool i din filsti?"

    # game/androidstrings.rpy:74
    old "I've opened the directory containing android.keystore and bundle.keystore. Please back them up, and keep them in a safe place."
    new "Jeg har åbnet mappen, der indeholder android.keystore og bundle.keystore. Sikkerhedskopiér dem venligst og opbevar dem på et sikkert sted."

    # game/choose_directory.rpy:58
    old "Select Projects Directory"
    new "Vælg placering af projektmappe"

    # game/choose_directory.rpy:72
    old "No directory was selected, but one is required."
    new "Ingen placering blev valgt, men en påkræves."

    # game/choose_directory.rpy:80
    old "The selected directory does not exist."
    new "Den valgte placering findes ikke."

    # game/choose_directory.rpy:82
    old "The selected directory is not writable."
    new "Den valgte placering er kan ikke skrives til."

    # game/choose_theme.rpy:304
    old "Could not change the theme. Perhaps options.rpy was changed too much."
    new "Kunne ikke ændre temaet. Måske er options.rpy blevet ændret for meget."

    # game/choose_theme.rpy:371
    old "Planetarium"
    new "Planetarium"

    # game/choose_theme.rpy:426
    old "Choose Theme"
    new "Vælg designtema"

    # game/choose_theme.rpy:439
    old "Theme"
    new "Designtema"

    # game/choose_theme.rpy:464
    old "Color Scheme"
    new "Farveskema"

    # game/choose_theme.rpy:508
    old "changing the theme"
    new "ændrer temaet"

    # game/consolecommand.rpy:91
    old "INFORMATION"
    new "INFORMATION"

    # game/consolecommand.rpy:91
    old "The command is being run in a new operating system console window."
    new "Kommandoen køres i et nyt styresystemskonsolvindue."

    # game/distribute.rpy:528
    old "Scanning project files..."
    new "Skanner projektfiler..."

    # game/distribute.rpy:554
    old "Building distributions failed:\n\nThe build.directory_name variable may not include the space, colon, or semicolon characters."
    new "Fremstilning af distributioner mislykkedes:\n\nVariablen build.directory_name må ikke indeholde tegnene mellemrum, kolon eller semikolon."

    # game/distribute.rpy:554
    old "This may be derived from build.name and config.version or build.version."
    new "Denne kan afledes af build.name og config.version eller build.version."

    # game/distribute.rpy:603
    old "No packages are selected, so there's nothing to do."
    new "Ingen pakker er valgte, så der er intet at lave."

    # game/distribute.rpy:615
    old "Scanning Ren'Py files..."
    new "Skanner Ren'Py-filer..."

    # game/distribute.rpy:697
    old "All packages have been built.\n\nDue to the presence of permission information, unpacking and repacking the Linux and Macintosh distributions on Windows is not supported."
    new "Alle pakker er blevet fremstilt.\n\nPå grund af tilstedeværelsen af tilladelsesinformation understøttes udpakningen og genpakningen af Linux- og Macintosh-distributioner på Windows ikke."

    # game/distribute.rpy:908
    old "Archiving files..."
    new "Arkiverer filer..."

    # game/distribute.rpy:1279
    old "Unpacking the Macintosh application for signing..."
    new "Udpakker Macintosh-applikationen til signering..."

    # game/distribute.rpy:1289
    old "Signing the Macintosh application...\n(This may take a long time.)"
    new "Signerer Macintosh-applikationen...\n(Dette tager muligvis lang tid.)"

    # game/distribute.rpy:1312
    old "Creating the Macintosh DMG..."
    new "Opretter Macintosh-DMG'en..."

    # game/distribute.rpy:1323
    old "Signing the Macintosh DMG..."
    new "Signerer Macintosh-DMG'en..."

    # game/distribute.rpy:1551
    old "Writing the [variant] [format] package."
    new "Skriver pakken [variant] [format]."

    # game/distribute.rpy:1567
    old "Making the [variant] update zsync file."
    new "Laver zsync-filen til [variant]-opdatering."

    # game/distribute.rpy:1680
    old "Processed {b}[complete]{/b} of {b}[total]{/b} files."
    new "{b}[complete]{/b} ud af {b}[total]{/b} filer behandlet."

    # game/distribute.rpy:1741
    old "Recompiling all rpy files into rpyc files..."
    new "Genkompilerer alle rpy-filer til rpyc-filer..."

    # game/distribute.rpy:1756
    old "Copying files..."
    new "Kopierer filer..."

    # game/distribute_gui.rpy:157
    old "Build Distributions: [project.current.display_name!q]"
    new "Fremstil distributioner: [project.current.display_name!q]"

    # game/distribute_gui.rpy:171
    old "Directory Name:"
    new "Navn på mappe:"

    # game/distribute_gui.rpy:175
    old "Executable Name:"
    new "Navn på eksekverbar fil:"

    # game/distribute_gui.rpy:185
    old "Actions:"
    new "Handlinger:"

    # game/distribute_gui.rpy:193
    old "Edit options.rpy"
    new "Rediger options.rpy"

    # game/distribute_gui.rpy:194
    old "Add from clauses to calls, once"
    new "Tilføj from-sætninger til kald én gang"

    # game/distribute_gui.rpy:195
    old "Update old-game"
    new "Opdater old-game"

    # game/distribute_gui.rpy:196
    old "Refresh"
    new "Genopfrisk"

    # game/distribute_gui.rpy:200
    old "Upload to itch.io"
    new "Læg op på itch.io"

    # game/distribute_gui.rpy:216
    old "Build Packages:"
    new "Fremstil pakker:"

    # game/distribute_gui.rpy:231
    old "(DLC)"
    new "(DLC)"

    # game/distribute_gui.rpy:241
    old "Options:"
    new "Indstillinger:"

    # game/distribute_gui.rpy:246
    old "Build Updates"
    new "Fremstil opdateringer"

    # game/distribute_gui.rpy:248
    old "Add from clauses to calls"
    new "Tilføj from-sætninger til kald"

    # game/distribute_gui.rpy:253
    old "Build"
    new "Fremstil"

    # game/distribute_gui.rpy:257
    old "Adding from clauses to call statements that do not have them."
    new "Tilføjer from-sætninger til kaldeordrer, der ikke har dem."

    # game/distribute_gui.rpy:281
    old "Errors were detected when running the project. Please ensure the project runs without errors before building distributions."
    new "Fejl blev fundet under kørsel af projektet. Sørg venligst for, at projektet kører uden fejl, før du fremstiller distributioner."

    # game/distribute_gui.rpy:300
    old "Your project does not contain build information. Would you like to add build information to the end of options.rpy?"
    new "Dit projekt indeholder ikke fremstillingsinformation. Vil du gerne tilføje fremstillingsinformation til slutningen af options.rpy?"

    # game/dmgcheck.rpy:50
    old "Ren'Py is running from a read only folder. Some functionality will not work."
    new "Ren'Py kører fra en skrivebeskyttet mappe. Nogle funktioner kommer ikke til at fungere."

    # game/dmgcheck.rpy:50
    old "This is probably because Ren'Py is running directly from a Macintosh drive image. To fix this, quit this launcher, copy the entire %s folder somewhere else on your computer, and run Ren'Py again."
    new "Dette sker sandsynligvis, fordi Ren'Py kører direkte fra et Macintosh-drevaftryk. For at fikse dette skal du afslutte denne launcher, kopiere hele mappen %s et andet sted hen på din computer og køre Ren'Py igen."

    # game/editor.rpy:152
    old "A modern editor with many extensions including advanced Ren'Py integration."
    new "En moderne tekstbehandler med mange udvidelser, herunder avanceret Ren'Py-integration."

    # game/editor.rpy:153
    old "A modern editor with many extensions including advanced Ren'Py integration.\n{a=jump:reinstall_vscode}Upgrade Visual Studio Code to the latest version.{/a}"
    new "En moderne tekstbehandler med mange udvidelser, herunder avanceret Ren'Py-integration.\n{a=jump:reinstall_vscode}Opgrader Visual Studio Code til seneste version.{/a}"

    # game/editor.rpy:169
    old "Visual Studio Code"
    new "Visual Studio Code"

    # game/editor.rpy:169
    old "Up to 110 MB download required."
    new "Hentning af op til 110 MB påkrævet."

    # game/editor.rpy:182
    old "A modern and approachable text editor."
    new "En moderne og lettilgængelig tekstbehandler."

    # game/editor.rpy:196
    old "Atom"
    new "Atom"

    # game/editor.rpy:196
    old "Up to 150 MB download required."
    new "Hentning af op til 150 MB påkrævet."

    # game/editor.rpy:211
    old "jEdit"
    new "jEdit"

    # game/editor.rpy:211
    old "A mature editor that requires Java."
    new "En moden tekstbehandler, der kræver Java."

    # game/editor.rpy:211
    old "1.8 MB download required."
    new "Hentning af 1.8 MB påkrævet."

    # game/editor.rpy:211
    old "This may have occured because Java is not installed on this system."
    new "Dette er muligvis opstået, fordi Java ikke er installeret på dette system."

    # game/editor.rpy:220
    old "Visual Studio Code (System)"
    new "Visual Studio Code (System)"

    # game/editor.rpy:220
    old "Uses a copy of Visual Studio Code that you have installed outside of Ren'Py. It's recommended you install the language-renpy extension to add support for Ren'Py files."
    new "Bruger en kopi af Visual Studio Code, som du har installeret uden for Ren'Py. Det anbefales, at du installerer udvidelsen language-renpy for at tilføje understøttelse af Ren'Py-filer."

    # game/editor.rpy:226
    old "System Editor"
    new "Systemtekstbehandler"

    # game/editor.rpy:226
    old "Invokes the editor your operating system has associated with .rpy files."
    new "Starter tekstbehandleren, som dit styresystem har associeret .rpy-filer med."

    # game/editor.rpy:245
    old "None"
    new "Ingen"

    # game/editor.rpy:245
    old "Prevents Ren'Py from opening a text editor."
    new "Forhindrer Ren'Py i at åbne en tekstbehandler."

    # game/editor.rpy:352
    old "Edit [text]."
    new "Rediger [text]."

    # game/editor.rpy:401
    old "An exception occured while launching the text editor:\n[exception!q]"
    new "En undtagelse opstod under opstart af tekstbehandleren:\n[exception!q]"

    # game/editor.rpy:533
    old "Select Editor"
    new "Vælg tekstbehandler"

    # game/editor.rpy:548
    old "A text editor is the program you'll use to edit Ren'Py script files. Here, you can select the editor Ren'Py will use. If not already present, the editor will be automatically downloaded and installed."
    new "En tekstbehandler er det program, som du bruger til at redigere Ren'Py-manuskriptfiler. Her kan du vælge den tekstbehandler, som Ren'Py skal bruge. Hvis den ikke allerede findes, vil den blive hentet og installeret automatisk."

    # game/front_page.rpy:58
    old "PROJECTS:"
    new "PROJEKTER:"

    # game/front_page.rpy:60
    old "refresh"
    new "genopfrisk"

    # game/front_page.rpy:87
    old "+ Create New Project"
    new "+ Opret nyt projekt"

    # game/front_page.rpy:97
    old "Launch Project"
    new "Opstart projekt"

    # game/front_page.rpy:114
    old "[p.name!q] (template)"
    new "[p.name!q] (skabelon)"

    # game/front_page.rpy:116
    old "Select project [text]."
    new "Vælg projekt [text]."

    # game/front_page.rpy:132
    old "Tutorial"
    new "Tutorial"

    # game/front_page.rpy:133
    old "The Question"
    new "Spørgsmålet"

    # game/front_page.rpy:149
    old "Active Project"
    new "Aktivt projekt"

    # game/front_page.rpy:157
    old "Open Directory"
    new "Åbn projektmappe"

    # game/front_page.rpy:171
    old "Edit File"
    new "Rediger fil"

    # game/front_page.rpy:182
    old "Open project"
    new "Åbn projekt"

    # game/front_page.rpy:184
    old "All script files"
    new "Alle manuskriptfiler"

    # game/front_page.rpy:188
    old "Actions"
    new "Handlinger"

    # game/front_page.rpy:197
    old "Navigate Script"
    new "Naviger i manuskript"

    # game/front_page.rpy:198
    old "Check Script (Lint)"
    new "Tjek manuskript (Lint)"

    # game/front_page.rpy:201
    old "Change/Update GUI"
    new "Ændr/opdater GUI"

    # game/front_page.rpy:203
    old "Change Theme"
    new "Ændr tema"

    # game/front_page.rpy:206
    old "Delete Persistent"
    new "Slet vedvarende data"

    # game/front_page.rpy:215
    old "Build Distributions"
    new "Fremstil distributioner"

    # game/front_page.rpy:217
    old "Android"
    new "Android"

    # game/front_page.rpy:218
    old "iOS"
    new "iOS"

    # game/front_page.rpy:219
    old "Web"
    new "Web"

    # game/front_page.rpy:219
    old "(Beta)"
    new "(Beta)"

    # game/front_page.rpy:220
    old "Generate Translations"
    new "Generér oversættelser"

    # game/front_page.rpy:221
    old "Extract Dialogue"
    new "Udtræk dialog"

    # game/front_page.rpy:259
    old "Checking script for potential problems..."
    new "Tjekker manuskript for potentielle problemer..."

    # game/front_page.rpy:274
    old "Deleting persistent data..."
    new "Sletter vedvarende data..."

    # game/gui7.rpy:243
    old "Select Accent and Background Colors"
    new "Vælg accent- og baggrundsfarver"

    # game/gui7.rpy:257
    old "Please click on the color scheme you wish to use, then click Continue. These colors can be changed and customized later."
    new "Klik venlig på det farveskema, du gerne vil bruge, og klik derefter på Fortsæt. Disse farver kan ændres og tilpasses senere."

    # game/gui7.rpy:302
    old "{b}Warning{/b}\nContinuing will overwrite customized bar, button, save slot, scrollbar, and slider images.\n\nWhat would you like to do?"
    new "{b}Advarsel!{/b}\nHvis du fortsætter, vil tilpassede bjælke-, knap-, gemmeplads-, rullebjælke- og skyder-billeder blive overskrevet.\n\nHvad vil du gerne gøre?"

    # game/gui7.rpy:302
    old "{size=-4}\n\nThis will not overwrite gui/main_menu.png, gui/game_menu.png, and gui/window_icon.png, but will create files that do not exist.{/size}"
    new "{size=-4}\n\nDette overskriver ikke gui/main_menu.png, gui/game_menu.png og gui/window_icon.png, men vil komme til at oprette filer, der ikke eksisterer.{/size}"

    # game/gui7.rpy:302
    old "Choose new colors, then regenerate image files."
    new "Vælg nye farver og regenerer billedfiler."

    # game/gui7.rpy:302
    old "Regenerate the image files using the colors in gui.rpy."
    new "Regenerer billedfilerne med brug af farverne i gui.rpy."

    # game/gui7.rpy:333
    old "What resolution should the project use? Although Ren'Py can scale the window up and down, this is the initial size of the window, the size at which assets should be drawn, and the size at which the assets will be at their sharpest.\n\nThe default of [default_size[0]]x[default_size[1]] is a reasonable compromise."
    new "Hvilken opløsning skal projektet bruge? Selvom Ren'Py kan op- og nedskalere vinduet, så er dette den initiale størrelse på vinduet, den størrelse, hvorpå aktiver bør tegnes, og størrelsen, hvorpå aktiverne står skarpest. Standardstørrelsen på [default_size[0]]x[default_size[1]] er et fornuftigt kompromis."

    # game/gui7.rpy:333
    old "Custom. The GUI is optimized for a 16:9 aspect ratio."
    new "Brugertilpasset. GUI'en er optimeret til et 16:9-billedformat."

    # game/gui7.rpy:350
    old "WIDTH"
    new "BREDDE"

    # game/gui7.rpy:350
    old "Please enter the width of your game, in pixels."
    new "Indtast venligst bredden på dit spil i pixels."

    # game/gui7.rpy:360
    old "The width must be a number."
    new "Bredden skal være et tal."

    # game/gui7.rpy:366
    old "HEIGHT"
    new "HØJDE"

    # game/gui7.rpy:366
    old "Please enter the height of your game, in pixels."
    new "Indtast venligst højden på dit spil i pixels."

    # game/gui7.rpy:376
    old "The height must be a number."
    new "Højden skal være et tal."

    # game/gui7.rpy:420
    old "Creating the new project..."
    new "Opretter nyt projekt..."

    # game/gui7.rpy:422
    old "Updating the project..."
    new "Opdaterer projekt..."

    # game/gui7.rpy:424
    old "creating a new project"
    new "opretter nyt projekt"

    # game/gui7.rpy:428
    old "activating the new project"
    new "aktiverer nyt projekt"

    # game/install.rpy:33
    old "Could not install [name!t], as a file matching [zipglob] was not found in the Ren'Py SDK directory."
    new "Kunne ikke installere [name!t], da en fil [zipglob] ikke blev fundet i Ren'Pys SDK-mappe."

    # game/install.rpy:79
    old "Successfully installed [name!t]."
    new "Installation af [name!t] lykkedes."

    # game/install.rpy:115
    old "This screen allows you to install libraries that can't be distributed with Ren'Py. Some of these libraries may require you to agree to a third-party license before being used or distributed."
    new "Denne skærm gør det muligt for dig at installere biblioteker, der ikke kan distribueres med Ren'Py. Nogle af disse biblioteker kræver måske, at du accepterer tredjepartslicenser før brug eller distribution."

    # game/install.rpy:121
    old "Install Steam Support"
    new "Installér Steam-understøttelse"

    # game/install.rpy:130
    old "Before installing Steam support, please make sure you are a {a=https://partner.steamgames.com/}Steam partner{/a}."
    new "Sørg for, at du er en {a=https://partner.steamgames.com/}Steam-partner{/a} før installation af Steam-understøttelse."

    # game/install.rpy:142
    old "Steam support has already been installed."
    new "Steam-understøttelse er allerede installeret."

    # game/install.rpy:146
    old "Install Live2D Cubism SDK for Native"
    new "Installér Live2D Cubism SDK til Native"

    # game/install.rpy:160
    old "Install Libraries"
    new "Installér biblioteker"

    # game/install.rpy:186
    old "The {a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism SDK for Native{/a} adds support for displaying Live2D models. Place CubismSdkForNative-4-{i}version{/i}.zip in the Ren'Py SDK directory, and then click Install. Distributing a game with Live2D requires you to accept a license from Live2D, Inc."
    new "{a=https://www.live2d.com/en/download/cubism-sdk/download-native/}Cubism-SDK'en til Native{/a} tilføjer understøttelse til visning af Live2D-modeller. Placer CubismSdkForNative-4-{i}version{/i}.zip i Ren'Pys SDK-mappe og klik derefter på Installér. Distribuation af et spil med Live2D kræver, at du accepterer en licens fra Live2D, Inc."

    # game/install.rpy:190
    old "Live2D in Ren'Py doesn't support the Web, Android x86_64 (including emulators and Chrome OS), and must be added to iOS projects manually. Live2D must be reinstalled after upgrading Ren'Py or installing Android support."
    new "Live2D i Ren'Py understøtter ikke webbet eller Android x86_64 (inklusiv emulatorer og Chrome OS), og skal tilføjes til iOS-projekter manuelt. Live2D skal geninstalleres efter opgradering af Ren'Py eller installation af Android-understøttelse."

    # game/install.rpy:195
    old "Open Ren'Py SDK Directory"
    new "Åbn Ren'Pys SDK-mappe"

    # game/installer.rpy:10
    old "Downloading [extension.download_file]."
    new "Henter [extension.download_file]."

    # game/installer.rpy:11
    old "Could not download [extension.download_file] from [extension.download_url]:\n{b}[extension.download_error]"
    new "Kunne ikke hente [extension.download_file] fra [extension.download_url]:\n{b}[extension.download_error]"

    # game/installer.rpy:12
    old "The downloaded file [extension.download_file] from [extension.download_url] is not correct."
    new "Den hentede fil [extension.download_file] fra [extension.download_url] er ikke korrekt."

    # game/interface.rpy:122
    old "Documentation"
    new "Dokumentation"

    # game/interface.rpy:123
    old "Ren'Py Website"
    new "Ren'Pys hjemmeside"

    # game/interface.rpy:124
    old "[interface.version]"
    new "[interface.version]"

    # game/interface.rpy:131
    old "update"
    new "opdater"

    # game/interface.rpy:136
    old "preferences"
    new "præferencer"

    # game/interface.rpy:137
    old "quit"
    new "afslut"

    # game/interface.rpy:141
    old "Ren'Py Sponsor Information"
    new "Ren'Py-sponsorinformation"

    # game/interface.rpy:277
    old "Due to package format limitations, non-ASCII file and directory names are not allowed."
    new "På grund af pakkeformatsbegrænsninger er fil- og mappenavne med ikke-ASCII-tegn ikke tilladt."

    # game/interface.rpy:373
    old "ERROR"
    new "FEJL"

    # game/interface.rpy:385
    old "opening the log file"
    new "åbner logfilen"

    # game/interface.rpy:407
    old "While [what!qt], an error occured:"
    new "En fejl opstod under [what!qt]:"

    # game/interface.rpy:407
    old "[exception!q]"
    new "[exception!q]"

    # game/interface.rpy:440
    old "Text input may not contain the {{ or [[ characters."
    new "Tekstinput må ikke indeholde tegnene {{ eller [[."

    # game/interface.rpy:445
    old "File and directory names may not contain / or \\."
    new "Fil- og mappenavne må ikke indeholde / eller \\."

    # game/interface.rpy:451
    old "File and directory names must consist of ASCII characters."
    new "Fil- og mappenavne skal bestå af ASCII-tegn."

    # game/interface.rpy:519
    old "PROCESSING"
    new "BEHANDLER"

    # game/interface.rpy:536
    old "QUESTION"
    new "SPØRGSMÅL"

    # game/interface.rpy:549
    old "CHOICE"
    new "VALG"

    # game/ios.rpy:28
    old "To build iOS packages, please download renios, unzip it, and place it into the Ren'Py directory. Then restart the Ren'Py launcher."
    new "Hent venligst renios, udpak det og placer det i Ren'Py-mappen for at bygge iOS-pakker. Genstart derefter Ren'Py-launcheren."

    # game/ios.rpy:29
    old "The directory in where Xcode projects will be placed has not been selected. Choose 'Select Directory' to select it."
    new "Mappen, hvori Xcode-projekter placeres, er ikke blevet valgt. Tryk på 'Vælg mappe' for at vælge den."

    # game/ios.rpy:30
    old "There is no Xcode project corresponding to the current Ren'Py project. Choose 'Create Xcode Project' to create one."
    new "Der er intet Xcode-projekt tilsvarende til det nuværende Ren'Py-projekt. Tryk på 'Opret Xcode-projekt' for at oprette et."

    # game/ios.rpy:31
    old "An Xcode project exists. Choose 'Update Xcode Project' to update it with the latest game files, or use Xcode to build and install it."
    new "Et Xcode-projekt findes. Tryk på 'Opdater Xcode-projekt' for at opdatere det med de seneste spilfiler, eller brug Xcode til at bygge og installere det."

    # game/ios.rpy:33
    old "Attempts to emulate an iPhone.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Forsøger at emulere en iPhone.\n\nTouch-input emuleres gennem musen, men kun når knappen holdes nede."

    # game/ios.rpy:34
    old "Attempts to emulate an iPad.\n\nTouch input is emulated through the mouse, but only when the button is held down."
    new "Forsøger at emulere en iPad.\n\nTouch-input emuleres gennem musen, men kun når knappen holdes nede."

    # game/ios.rpy:36
    old "Selects the directory where Xcode projects will be placed."
    new "Vælger mappen, hvori Xcode-projekter placeres."

    # game/ios.rpy:37
    old "Creates an Xcode project corresponding to the current Ren'Py project."
    new "Opretter et Xcode-projekt tilsvarende til det nuværende Ren'Py-projekt."

    # game/ios.rpy:38
    old "Updates the Xcode project with the latest game files. This must be done each time the Ren'Py project changes."
    new "Opdaterer Xcode-projektet med de seneste spilfiler. Dette skal gøres, hver gang Ren'Py-projektet ændrer sig."

    # game/ios.rpy:39
    old "Opens the Xcode project in Xcode."
    new "Åbner Xcode-projektet i Xcode."

    # game/ios.rpy:41
    old "Opens the directory containing Xcode projects."
    new "Åbner mappen, der indeholder Xcode-projekter."

    # game/ios.rpy:139
    old "The Xcode project already exists. Would you like to rename the old project, and replace it with a new one?"
    new "Xcode-projektet findes allerede. Vil du gerne omdøbe det gamle projekt og erstatte det med et nyt et?"

    # game/ios.rpy:269
    old "iOS: [project.current.display_name!q]"
    new "iOS: [project.current.display_name!q]"

    # game/ios.rpy:298
    old "iPhone"
    new "iPhone"

    # game/ios.rpy:302
    old "iPad"
    new "iPad"

    # game/ios.rpy:322
    old "Select Xcode Projects Directory"
    new "Vælg Xcode-projektmappeplacering"

    # game/ios.rpy:326
    old "Create Xcode Project"
    new "Opret Xcode-projekt"

    # game/ios.rpy:330
    old "Update Xcode Project"
    new "Opdater Xcode-projekt"

    # game/ios.rpy:335
    old "Launch Xcode"
    new "Kør Xcode"

    # game/ios.rpy:358
    old "Open Xcode Projects Directory"
    new "Åbn Xcode-projektmappeplacering"

    # game/ios.rpy:379
    old "There are known issues with the iOS simulator on Apple Silicon. Please test on x86_64 or iOS devices."
    new "Der kendes til problemer med iOS-simulatoren på Apple Silicon. Test venligst på x86_64- eller iOS-enheder."

    # game/ios.rpy:395
    old "Before packaging iOS apps, you'll need to download renios, Ren'Py's iOS support. Would you like to download renios now?"
    new "Før pakning af iOS-apps skal du hente renios, Ren'Pys iOS-understøttelse. Vil du gerne hente renios nu?"

    # game/ios.rpy:404
    old "XCODE PROJECTS DIRECTORY"
    new "XCODE-PROJEKTMAPPEPLACERING"

    # game/ios.rpy:404
    old "Please choose the Xcode Projects Directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Vælg venligst Xcodes projektmappeplacering gennem stifinderen.\n{b}Stifinderen er måske åbnet bag dette vindue.{/b}"

    # game/ios.rpy:409
    old "Ren'Py has set the Xcode Projects Directory to:"
    new "Ren'Py har indstillet Xcodes projektmappeplacering til:"

    # game/itch.rpy:45
    old "Downloading the itch.io butler."
    new "Henter itch.io-butleren."

    # game/itch.rpy:91
    old "The built distributions could not be found. Please choose 'Build' and try again."
    new "De fremstillede distributioner kunne ikke findes. Vælg venligst 'Fremstil' og prøv igen."

    # game/itch.rpy:111
    old "No uploadable files were found. Please choose 'Build' and try again."
    new "Ingen sendbare filer blev funder. Vælg venligst 'Fremstil' og prøv igen."

    # game/itch.rpy:117
    old "The butler program was not found."
    new "Butler-programmet blev ikke fundet."

    # game/itch.rpy:117
    old "Please install the itch.io app, which includes butler, and try again."
    new "Installér venligt itch.op-appen, som inkluderer butler, og prøv igen."

    # game/itch.rpy:126
    old "The name of the itch project has not been set."
    new "Navnet på itch-projektet er ikke blevet indstillet."

    # game/itch.rpy:126
    old "Please {a=https://itch.io/game/new}create your project{/a}, then add a line like \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} to options.rpy."
    new "{a=https://itch.io/game/new}Opret{/a} venligst dit projekt og tilføj derefter en linje såsom \n{vspace=5}define build.itch_project = \"user-name/game-name\"\n{vspace=5} til options.rpy."

    # game/mobilebuild.rpy:114
    old "{a=%s}%s{/a}"
    new "{a=%s}%s{/a}"

    # game/navigation.rpy:168
    old "Navigate: [project.current.display_name!q]"
    new "Naviger: [project.current.display_name!q]"

    # game/navigation.rpy:178
    old "Order: "
    new "Rækkefølge: "

    # game/navigation.rpy:179
    old "alphabetical"
    new "alfabetisk"

    # game/navigation.rpy:181
    old "by-file"
    new "pr. fil"

    # game/navigation.rpy:183
    old "natural"
    new "naturlig"

    # game/navigation.rpy:195
    old "Category:"
    new "Kategori:"

    # game/navigation.rpy:198
    old "files"
    new "filer"

    # game/navigation.rpy:199
    old "labels"
    new "mærkater"

    # game/navigation.rpy:200
    old "defines"
    new "definitioner"

    # game/navigation.rpy:201
    old "transforms"
    new "transformationer"

    # game/navigation.rpy:202
    old "screens"
    new "skærme"

    # game/navigation.rpy:203
    old "callables"
    new "kaldbare funktioner"

    # game/navigation.rpy:204
    old "TODOs"
    new "TODO'er"

    # game/navigation.rpy:243
    old "+ Add script file"
    new "+ Tilføj manuskriptfil"

    # game/navigation.rpy:251
    old "No TODO comments found.\n\nTo create one, include \"# TODO\" in your script."
    new "Ingen TODO-kommentarer fundet.\n\nInkluder \"# TODO\" i dit manuskript for at oprette en."

    # game/navigation.rpy:258
    old "The list of names is empty."
    new "Listen over navne er tom."

    # game/new_project.rpy:38
    old "New GUI Interface"
    new "Ny GUI-grænseflade"

    # game/new_project.rpy:48
    old "Both interfaces have been translated to your language."
    new "Begge grænseflader er blevet oversat til dit sprog."

    # game/new_project.rpy:50
    old "Only the new GUI has been translated to your language."
    new "Kun den nye GUI er blevet oversat til dit sprog."

    # game/new_project.rpy:52
    old "Only the legacy theme interface has been translated to your language."
    new "Kun grænsefladen med forældet designtema er blevet oversat til dit sprog."

    # game/new_project.rpy:54
    old "Neither interface has been translated to your language."
    new "Ingen af grænsefladerne er blevet oversat til dit sprog."

    # game/new_project.rpy:63
    old "The projects directory could not be set. Giving up."
    new "Projektmappen kunne ikke opsættes. Giver op."

    # game/new_project.rpy:70
    old "Which interface would you like to use? The new GUI has a modern look, supports wide screens and mobile devices, and is easier to customize. Legacy themes might be necessary to work with older example code.\n\n[language_support!t]\n\nIf in doubt, choose the new GUI, then click Continue on the bottom-right."
    new "Hvilke grænseflader vil du gerne bruge? Den nye GUI har et moderne udseende, støtter bredformat og mobilenheder og er lettere at tilpasse. Forældede designtemaer er måske nødvendige for at arbejde med ældre eksempelkode.\n\n[language_support!t]\n\nVælg den nye GUI, hvis du er i tvivl, og klik derefter på Fortsæt nederst til højre."

    # game/new_project.rpy:70
    old "Legacy Theme Interface"
    new "Grænseflade med forældet designtema"

    # game/new_project.rpy:77
    old "{#language name and font}"
    new "Dansk"

    # game/new_project.rpy:81
    old "You will be creating an [new_project_language]{#this substitution may be localized} language project. Change the launcher language in preferences to create a project in another language."
    new "Du er ved at oprette et dansksproget projekt. Ændr launcher-sproget i præferencer for at oprette et projekt på et andet sprog."

    # game/new_project.rpy:86
    old "PROJECT NAME"
    new "PROJEKTNAVN"

    # game/new_project.rpy:86
    old "Please enter the name of your project:"
    new "Indtast venligst navnet på dit projekt:"

    # game/new_project.rpy:96
    old "The project name may not be empty."
    new "Projektnavnet må ikke være tomt."

    # game/new_project.rpy:102
    old "[project_name!q] already exists. Please choose a different project name."
    new "[project_name!q] findes allerede. Vælg venligst et andet projektnavn."

    # game/new_project.rpy:106
    old "[project_dir!q] already exists. Please choose a different project name."
    new "[project_dir!q] findes allerede. Vælg venligst et andet projektnavn."

    # game/new_project.rpy:124
    old "Choose Project Template"
    new "Vælg projektskabelon"

    # game/new_project.rpy:142
    old "Please select a template to use for your new project. The template sets the default font and the user interface language. If your language is not supported, choose 'english'."
    new "Vælg venligst en skabelon at bruge til dit nye projekt. Skabelonen indstiller standardskrifttypen og brugerfladesproget. Hvis dit sprog ikke understøttes, vælg da 'english'."

    # game/preferences.rpy:88
    old "Launcher Preferences"
    new "Launcher-præferencer"

    # game/preferences.rpy:106
    old "General"
    new "Generelt"

    # game/preferences.rpy:107
    old "Options"
    new "Indstillinger"

    # game/preferences.rpy:131
    old "Projects Directory:"
    new "Projektmappeplacering:"

    # game/preferences.rpy:138
    old "[persistent.projects_directory!q]"
    new "[persistent.projects_directory!q]"

    # game/preferences.rpy:140
    old "Projects directory: [text]"
    new "Projektmappeplacering: [text]"

    # game/preferences.rpy:142
    old "Not Set"
    new "Ikke indstillet"

    # game/preferences.rpy:155
    old "Text Editor:"
    new "Tekstbehandler:"

    # game/preferences.rpy:161
    old "Text editor: [text]"
    new "Tekstbehandler: [text]"

    # game/preferences.rpy:173
    old "Language:"
    new "Sprog:"

    # game/preferences.rpy:200
    old "Navigation Options:"
    new "Navigationsindstillinger:"

    # game/preferences.rpy:204
    old "Include private names"
    new "Inkluder private navne"

    # game/preferences.rpy:205
    old "Include library names"
    new "Inkluder biblioteksnavne"

    # game/preferences.rpy:214
    old "Launcher Options:"
    new "Launcher-indstillinger:"

    # game/preferences.rpy:218
    old "Show edit file section"
    new "Vis filredigeringssektion"

    # game/preferences.rpy:219
    old "Large fonts"
    new "Store skrifttyper"

    # game/preferences.rpy:222
    old "Console output"
    new "Konsoloutput"

    # game/preferences.rpy:224
    old "Sponsor message"
    new "Sponsorbesked"

    # game/preferences.rpy:227
    old "Daily check for update"
    new "Dagligt tjek efter opdatering"

    # game/preferences.rpy:246
    old "Launcher Theme:"
    new "Launcher-designtema:"

    # game/preferences.rpy:250
    old "Default theme"
    new "Standardtema"

    # game/preferences.rpy:251
    old "Dark theme"
    new "Mørkt tema"

    # game/preferences.rpy:252
    old "Custom theme"
    new "Brugertilpasset tema"

    # game/preferences.rpy:256
    old "Information about creating a custom theme can be found {a=https://www.renpy.org/doc/html/skins.html}in the Ren'Py Documentation{/a}."
    new "Information omkring oprettelse af et brugertilpasset tema kan findes {a=https://www.renpy.org/doc/html/skins.html}i Ren'Py-dokumentationen{/a}."

    # game/preferences.rpy:273
    old "Install Libraries:"
    new "Installér biblioteker:"

    # game/preferences.rpy:299
    old "Open launcher project"
    new "Åbn launcher-projekt"

    # game/preferences.rpy:300
    old "Reset window size"
    new "Nulstil vinduesstørrelse"

    # game/preferences.rpy:301
    old "Clean temporary files"
    new "Opryd midlertidige filer"

    # game/preferences.rpy:308
    old "Cleaning temporary files..."
    new "Oprydder midlertidige filer..."

    # game/preferences.rpy:338
    old "{#in language font}Welcome! Please choose a language"
    new "{#in language font}Velkommen! Vælg venligst et sprog"

    # game/preferences.rpy:373
    old "{#in language font}Start using Ren'Py in [lang_name]"
    new "{#in language font}Begynd at bruge Ren'Py på [lang_name]"

    # game/project.rpy:46
    old "After making changes to the script, press shift+R to reload your game."
    new "Tryk på shift+R for at genindlæse dit spil efter at have lavet ændringer i manuskriptet"

    # game/project.rpy:46
    old "Press shift+O (the letter) to access the console."
    new "Tryk på shift+O (bogstavet) for at tilgå konsollen."

    # game/project.rpy:46
    old "Press shift+D to access the developer menu."
    new "Tryk på shift+D for at til gå udviklermenuen."

    # game/project.rpy:46
    old "Have you backed up your projects recently?"
    new "Har du sikkerhedskopieret dine projekter for nyligt?"

    # game/project.rpy:46
    old "Lint checks your game for potential mistakes, and gives you statistics."
    new "Lint tjekker dit spil for potentielle fejl og giver dig statistik."

    # game/project.rpy:287
    old "Launching the project failed."
    new "Opstart af projektet mislykkedes."

    # game/project.rpy:287
    old "This may be because the project is not writeable."
    new "Dette skyldes måske, at projektet ikke er skrivbart."

    # game/project.rpy:289
    old "Please ensure that your project launches normally before running this command."
    new "Sørg venligst for, at dit projekt starter normalt op, før du kører denne kommando."

    # game/project.rpy:305
    old "Ren'Py is scanning the project..."
    new "Ren'Py skanner projektet..."

    # game/project.rpy:768
    old "Launching"
    new "Starter op"

    # game/project.rpy:810
    old "PROJECTS DIRECTORY"
    new "PROJEKTMAPPEPLACERING"

    # game/project.rpy:810
    old "Please choose the projects directory using the directory chooser.\n{b}The directory chooser may have opened behind this window.{/b}"
    new "Vælg venligst projektmappeplaceringen gennem stifinderen.\n{b}Stifinderen er måske åbnet bag dette vindue.{/b}"

    # game/project.rpy:810
    old "This launcher will scan for projects in this directory, will create new projects in this directory, and will place built projects into this directory."
    new "Denne launcher kigger efter projekter i denne mappe, opretter nye projekter i denne mappe og placerer fremstillede projekter i denne mappe."

    # game/project.rpy:815
    old "Ren'Py has set the projects directory to:"
    new "Ren'Py har indstillet projektmappeplaceringen til:"

    # game/translations.rpy:91
    old "Translations: [project.current.display_name!q]"
    new "Oversættelser: [project.current.display_name!q]"

    # game/translations.rpy:132
    old "The language to work with. This should only contain lower-case ASCII characters and underscores."
    new "Arbejdssproget. Dette bør kun indeholde små ASCII-bogstaver og bundstreger."

    # game/translations.rpy:158
    old "Generate empty strings for translations"
    new "Genererer tomme strenge til oversættelse"

    # game/translations.rpy:176
    old "Generates or updates translation files. The files will be placed in game/tl/[persistent.translate_language!q]."
    new "Genererer eller opdaterer oversættelsesfiler. Filerne placeres i game/tl/[persistent.translate_language!q]."

    # game/translations.rpy:196
    old "Extract String Translations"
    new "Udtræk strengoversættelser"

    # game/translations.rpy:198
    old "Merge String Translations"
    new "Flet strengoversættelser"

    # game/translations.rpy:203
    old "Replace existing translations"
    new "Erstat eksisterende oversættelser"

    # game/translations.rpy:204
    old "Reverse languages"
    new "Vend sprog om"

    # game/translations.rpy:208
    old "Update Default Interface Translations"
    new "Opdater standardoversættelser af grænsefladen"

    # game/translations.rpy:228
    old "The extract command allows you to extract string translations from an existing project into a temporary file.\n\nThe merge command merges extracted translations into another project."
    new "Udtræk-kommandoen gør det muligt for dig at udtrække strengoversættelser fra et eksisterende projekt ind i en midlertidig fil.\n\nFlet-kommandoen fletter udtrukne oversættelser sammen ind i et andet projekt."

    # game/translations.rpy:252
    old "Ren'Py is generating translations...."
    new "Ren'Py genererer oversættelser..."

    # game/translations.rpy:263
    old "Ren'Py has finished generating [language] translations."
    new "Ren'Py har færdiggenereret [language]-oversættelser."

    # game/translations.rpy:276
    old "Ren'Py is extracting string translations..."
    new "Ren'Py udtrækker strengoversættelser..."

    # game/translations.rpy:279
    old "Ren'Py has finished extracting [language] string translations."
    new "Ren'Py er færdig med udtrækning af [language]-strengoversættelser."

    # game/translations.rpy:299
    old "Ren'Py is merging string translations..."
    new "Ren'Py fletter strengoversættelser..."

    # game/translations.rpy:302
    old "Ren'Py has finished merging [language] string translations."
    new "Ren'Py er færdig med fletning af [language]-strengoversættelser."

    # game/translations.rpy:313
    old "Updating default interface translations..."
    new "Opdaterer standardskærmfladeoversættelser..."

    # game/translations.rpy:342
    old "Extract Dialogue: [project.current.display_name!q]"
    new "Udtræk dialog: [project.current.display_name!q]"

    # game/translations.rpy:358
    old "Format:"
    new "Format:"

    # game/translations.rpy:366
    old "Tab-delimited Spreadsheet (dialogue.tab)"
    new "Tabulatoradskilt regneark (dialogue.tab)"

    # game/translations.rpy:367
    old "Dialogue Text Only (dialogue.txt)"
    new "Kun dialogtekst (dialogue.txt)"

    # game/translations.rpy:380
    old "Strip text tags from the dialogue."
    new "Fjern tekstmærker fra dialogen."

    # game/translations.rpy:381
    old "Escape quotes and other special characters."
    new "Lav citationstegn og andre specielle tegn til undvigesekvenser."

    # game/translations.rpy:382
    old "Extract all translatable strings, not just dialogue."
    new "Udtræk alle oversættelige strenge, ikke kun dialog."

    # game/translations.rpy:391
    old "Language (or None for the default language):"
    new "Sprog (eller None for standardsproget):"

    # game/translations.rpy:428
    old "Ren'Py is extracting dialogue...."
    new "Ren'Py udtrækker dialog..."

    # game/translations.rpy:432
    old "Ren'Py has finished extracting dialogue. The extracted dialogue can be found in dialogue.[persistent.dialogue_format] in the base directory."
    new "Ren'Py har færdiggjort udtrækning af dialog. Den udtrukne dialog kan findes i dialogue.[persistent.dialogue_format] i grundmappen."

    # game/updater.rpy:63
    old "Release"
    new "Heludgave"

    # game/updater.rpy:64
    old "Release (Ren'Py 8, Python 3)"
    new "Heludgave (Ren'Py 8, Python 3)"

    # game/updater.rpy:65
    old "Release (Ren'Py 7, Python 2)"
    new "Heludgave (Ren'Py 7, Python 2)"

    # game/updater.rpy:66
    old "{b}Recommended.{/b} The version of Ren'Py that should be used in all newly-released games."
    new "{b}Anbefalet.{/b} Den version af Ren'Py, der bør bruges i alle nyudgivne spil."

    # game/updater.rpy:68
    old "Prerelease"
    new "Forhåndsudgave"

    # game/updater.rpy:69
    old "Prerelease (Ren'Py 8, Python 3)"
    new "Forhåndsudgave (Ren'Py 8, Python 3)"

    # game/updater.rpy:70
    old "Prerelease (Ren'Py 7, Python 2)"
    new "Forhåndsudgave (Ren'Py 7, Python 2)"

    # game/updater.rpy:71
    old "A preview of the next version of Ren'Py that can be used for testing and taking advantage of new features, but not for final releases of games."
    new "En forhåndsvisning af næste version af Ren'Py, som kan bruges til testning og udnyttelse af nye funktioner, men ikke til endelige udgivelser af spil."

    # game/updater.rpy:73
    old "Experimental"
    new "Eksperimentiel"

    # game/updater.rpy:74
    old "Experimental versions of Ren'Py. You shouldn't select this channel unless asked by a Ren'Py developer."
    new "Eksperimentielle versioner af Ren'Py. Du bør ikke vælge denne kanal, medmindre du er blevet bedt om det af en Ren'Py-udvikler."

    # game/updater.rpy:76
    old "Nightly Fix"
    new "Natlig fiksning"

    # game/updater.rpy:77
    old "Nightly Fix (Ren'Py 8, Python 3)"
    new "Natlig fiksning (Ren'Py 8, Python 3)"

    # game/updater.rpy:78
    old "Nightly Fix (Ren'Py 7, Python 2)"
    new "Natlig fiksning (Ren'Py 7, Python 2)"

    # game/updater.rpy:79
    old "A nightly build of fixes to the release version of Ren'Py."
    new "En natlig opdatering med fejlrettelser til den udgivne version af Ren'Py."

    # game/updater.rpy:81
    old "Nightly"
    new "Natlig"

    # game/updater.rpy:82
    old "Nightly (Ren'Py 8, Python 3)"
    new "Natlig (Ren'Py 8, Python 3)"

    # game/updater.rpy:83
    old "Nightly (Ren'Py 7, Python 2)"
    new "Natlig (Ren'Py 7, Python 2)"

    # game/updater.rpy:84
    old "The bleeding edge of Ren'Py development. This may have the latest features, or might not run at all."
    new "De allernyeste udviklinger i Ren'Py. Måske har udgaven de seneste funktioner, eller måske kører den slet ikke."

    # game/updater.rpy:102
    old "Select Update Channel"
    new "Vælg opdateringskanal"

    # game/updater.rpy:113
    old "The update channel controls the version of Ren'Py the updater will download."
    new "Opdateringskanalen styrer hvilken version af Ren'Py opdateringsprogrammet henter."

    # game/updater.rpy:121
    old "• {a=https://www.renpy.org/doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/doc/html/changelog.html}Se ændringslog{/a}"

    # game/updater.rpy:123
    old "• {a=https://www.renpy.org/dev-doc/html/changelog.html}View change log{/a}"
    new "• {a=https://www.renpy.org/dev-doc/html/changelog.html}Se ændringslog{/a}"

    # game/updater.rpy:129
    old "• This version is installed and up-to-date."
    new "• Denne version er installeret og ajour."

    # game/updater.rpy:141
    old "%B %d, %Y"
    new "%d. %B, %Y"

    # game/updater.rpy:163
    old "An error has occured:"
    new "En fejl er opstået:"

    # game/updater.rpy:165
    old "Checking for updates."
    new "Kigger efter opdateringer."

    # game/updater.rpy:167
    old "Ren'Py is up to date."
    new "Ren'Py er ajour."

    # game/updater.rpy:169
    old "[u.version] is now available. Do you want to install it?"
    new "[u.version] er nu tilgængelig. Vil du gerne installere denne?"

    # game/updater.rpy:171
    old "Preparing to download the update."
    new "Forbereder hentning af opdateringen."

    # game/updater.rpy:173
    old "Downloading the update."
    new "Henter opdateringen."

    # game/updater.rpy:175
    old "Unpacking the update."
    new "Udpakker opdateringen."

    # game/updater.rpy:177
    old "Finishing up."
    new "Færdiggør."

    # game/updater.rpy:179
    old "The update has been installed. Ren'Py will restart."
    new "Opdateringen er blevet installeret. Ren'Py genstarter."

    # game/updater.rpy:181
    old "The update has been installed."
    new "Opdatering er blevet installeret."

    # game/updater.rpy:183
    old "The update was cancelled."
    new "Opdateringen blev annulleret."

    # game/updater.rpy:200
    old "Ren'Py Update"
    new "Ren'Py-opdatering"

    # game/updater.rpy:206
    old "Proceed"
    new "Fortsæt"

    # game/updater.rpy:220
    old "Fetching the list of update channels"
    new "Henter listen over opdateringskanaler"

    # game/updater.rpy:225
    old "downloading the list of update channels"
    new "henter listen over opdateringskanaler"

    # game/web.rpy:428
    old "Preparing progressive download"
    new "Forbereder progressiv nedhentning"

    # game/web.rpy:485
    old "Creating package..."
    new "Opretter pakke..."

    # game/web.rpy:505
    old "Web: [project.current.display_name!q]"
    new "Web: [project.current.display_name!q]"

    # game/web.rpy:535
    old "Build Web Application"
    new "Fremstil webapplikation"

    # game/web.rpy:536
    old "Build and Open in Browser"
    new "Fremstil og åbn i browser"

    # game/web.rpy:537
    old "Open in Browser"
    new "Åbn i browser"

    # game/web.rpy:538
    old "Open build directory"
    new "Åbn fremstilningsmappe"

    # game/web.rpy:560
    old "Images and music can be downloaded while playing. A 'progressive_download.txt' file will be created so you can configure this behavior."
    new "Billeder og musik kan hentes under afspilning. En 'progressive_download.txt'-fil bliver oprettet, så du kan konfigurere denne opførsel."

    # game/web.rpy:568
    old "Before packaging web apps, you'll need to download RenPyWeb, Ren'Py's web support. Would you like to download RenPyWeb now?"
    new "Før du pakker webapps, skal du have hentet Ren'Pys websunderstøttelse, RenPyWeb. Vil du gerne hente RenPyWeb nu?"

    # game/androidstrings.rpy:46
    old "I was unable to use javac to compile a test file. If you haven't installed the Java Development Kit yet, please download it from:\n\n{a=https://adoptium.net}https://adoptium.net/{/a}\n\nThe JDK is different from the JRE, so it's possible you have Java without having the JDK. Please install JDK [JDK_REQUIREMENT], and add it to your PATH.\n\nWithout a working JDK, I can't continue."
    new "Jeg kunne ikke bruge javac til at kompilere en testfil. Hvis du ikke allerede har installere Java Development Kit, så hent det venligst fra \n\n{a=https://adoptium.net}https://adoptium.net/{/a}\n\nJDK'et er forskelligt fra JRE'et, så det er muligt, at du har Java uden at have JDK'et. Installér venligst JDK [JDK_REQUIREMENT] og tilføj det til din PATH.\n\nUden et fungerende JDK kan jeg ikke fortsætte."

    # game/androidstrings.rpy:47
    old "The version of Java on your computer does not appear to be JDK [JDK_REQUIREMENT], which is required to build Android apps. If you need to install a newer JDK, you can download it from:\n\n{a=https://adoptium.net/}https://adoptium.net/{/a}, and add it to your PATH.\n\nYou can also set the JAVA_HOME environment variable to use a different version of Java."
    new "Versionen af Java på din computer synes ikke at være JDK [JDK_REQUIREMENT], hvilket er påkrævet for at bygge Android-apps. Hvis du har brug for at installere et nyere JDK, kan du hente det fra:\n\n{a=https://adoptium.net/}https://adoptium.net/{/a} og tilføje det til din PATH.\n\nDu kan også indstille JAVA_HOME-miljøvariablen til at bruge en anden version af Java."

    # game/distribute.rpy:535
    old "Building distributions failed:\n\nThe project is the Ren'Py Tutorial, which can't be distributed outside of Ren'Py. Consider using The Question as a test project."
    new "Fremstilling af distributioner mislykkedes:\n\nProjektet er Ren'Py-tutorialen, som ikke kan distribueres uden for Ren'Py. Overvej at bruge Spørgsmålet som et testprojekt."

    # game/distribute.rpy:1620
    old "Finishing the [variant] [format] package."
    new "Færdiggør [variant] [format]-pakken."

    # game/editor.rpy:185
    old "Atom is deprecated and its bugs are known for corrupting games, using another editor is recommended."
    new "Atom er udfaset, og dens bugs vides at korrumpere spil, så det anbefales at bruge en anden tekstbehandler."

    # game/editor.rpy:214
    old "JEdit is deprecated, using another editor is recommended."
    new "JEdit er udfaset, så det anbefales at bruge en anden tekstbehandler."

    # game/editor.rpy:607
    old "The Atom text editor is no longer supported by its developers. We suggest switching to Visual Studio Code or another editor."
    new "Atom-tekstbehandleren understøttes ikke længere af dens udviklere. Vi anbefaler at skifte til Visual Studio Code eller en anden tekstbehandler."

    # game/editor.rpy:607
    old "Select editor now."
    new "Vælg tekstbehandler nu."

    # game/editor.rpy:607
    old "Ignore until next launch."
    new "Ignorer intil næste opstart."

    # game/editor.rpy:607
    old "Do not ask again."
    new "Spørg ikke igen."

    # game/new_project.rpy:38
    old "Warning : you are using Ren'Py 7. It is recommended to start new projects using Ren'Py 8 instead."
    new "Advarsel: Du bruger Ren'Py 7. Det anbefales at starte nye projekter med Ren'Py 8 i stedet."

    # game/new_project.rpy:49
    old "Please select a template project to use."
    new "Vælg venligst et skabelonprojekt at bruge."

    # game/new_project.rpy:49
    old "Do not use a template project."
    new "Brug ikke et skabelonprojekt."

    # game/preferences.rpy:94
    old "Lint"
    new "Lint"

    # game/preferences.rpy:233
    old "Game Options:"
    new "Spilindstillinger:"

    # game/preferences.rpy:240
    old "Skip splashscreen"
    new "Spring over opstartsskærm"

    # game/preferences.rpy:258
    old "Restore window position"
    new "Gendan vinduesplacering"

    # game/preferences.rpy:262
    old "Prefer RPU updates"
    new "Foretræk RPU-opdateringer"

    # game/preferences.rpy:332
    old "Open projects.txt"
    new "Åbn projects.txt"

    # game/preferences.rpy:356
    old "Lint toggles:"
    new "Lint-indstillinger:"

    # game/preferences.rpy:360
    old "Check for orphan/obsolete translations"
    new "Kontrollér for forældreløse/forældede oversættelser"

    # game/preferences.rpy:363
    old "Check parameters shadowing reserved names"
    new "Tjek parametre, der skygger reserverede navne"

    # game/preferences.rpy:366
    old "Print block, word, and character counts by speaking character."
    new "Udskriv blok-, ord- og figurantal efter talende figur."

    # game/preferences.rpy:369
    old "Unclosed text tags"
    new "Ulukkede tekstmærker"

    # game/preferences.rpy:372
    old "Show all unreachable blocks and orphaned translations."
    new "Vi alle utilgængelige blokke og forældreløse oversættelser."

    # game/project.rpy:776
    old "Splashscreen skipped in launcher preferences."
    new "Opstartsskærm sprunget over i launcher-præferencer."

