
translate finnish strings:

    # options.rpy:1
    old "## This file contains options that can be changed to customize your game."
    new "## Tämä tiedosto sisältää asetuksia, joita muokkaamalla voit mukauttaa peliäsi."

    # options.rpy:4
    old "## Lines beginning with two '#' marks are comments, and you shouldn't uncomment them. Lines beginning with a single '#' mark are commented-out code, and you may want to uncomment them when appropriate."
    new "## Rivit, jotka alkavat kahdells '#'-merkillä, ovat kommentteja eikä sinun tule muuttaa niitä ohjelmakoodiksi. Rivit, jotka alkavat yhdellä '#'-merkillä, ovat kommentoitua koodia, ja voit halutessasi palauttaa ne ohjelmakoodiksi."

    # options.rpy:10
    old "## Basics"
    new "## Perusteet"

    # options.rpy:12
    old "## A human-readable name of the game. This is used to set the default window title, and shows up in the interface and error reports."
    new "## Ihmisille luettava pelin nimi. Tätä käytetään peli-ikkunan nimen asetuksessa, ja se näkyy pelin ikkunassa sekä virheraporteissa."

    # options.rpy:15
    old "## The _() surrounding the string marks it as eligible for translation."
    new "## _() merkkijonon ympärillä merkitsee sen soveltuvaksi käännöksille."

    # options.rpy:17
    old "Ren'Py 7 Default GUI"
    new "Ren'Py 7 Oletusarvoinen GUI"

    # options.rpy:20
    old "## Determines if the title given above is shown on the main menu screen. Set this to False to hide the title."
    new "## Päättää, näytetäänkö ylläannettu nimi pelin päävalikossa. Aseta arvoksi False piilottaaksesi nimen."

    # options.rpy:26
    old "## The version of the game."
    new "## Pelin versio."

    # options.rpy:31
    old "## Text that is placed on the game's about screen. To insert a blank line between paragraphs, write \\n\\n."
    new "## Teksti, joka näkyy pelin tietoja-ikkunassa. Lisätäksesi tyhjän rivin lauseiden väliin, kirjoita \\n\\n."

    # options.rpy:37
    old "## A short name for the game used for executables and directories in the built distribution. This must be ASCII-only, and must not contain spaces, colons, or semicolons."
    new "## Lyhyt nimi pelille, jota käytetään kootuille ohjelmatiedostoille sekä kansioille. Nimen on oltava pelkkiä ASCII-merkkejä, eikä se saa sisältää välilyöntejä, pisteitä, eikä puolipisteitä."

    # options.rpy:44
    old "## Sounds and music"
    new "## Äänet ja musiikki"

    # options.rpy:46
    old "## These three variables control which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    new "## Nämä kolme muuttujaa ohjaavat, mitkä mikserit näytetään pelaajalle oletusarvoisesti. Asettamalla arvoksi False piilottaa kyseisen mikserin."

    # options.rpy:55
    old "## To allow the user to play a test sound on the sound or voice channel, uncomment a line below and use it to set a sample sound to play."
    new "## Mahdollistaaksesi käyttäjän soittaa testiääni äänitehoste- tai puhekanavilla, palauta seuraava kommentti takaisin ohjelmakoodiksi ja käytä sitä valitaksesi sopivan testiäänen."

    # options.rpy:62
    old "## Uncomment the following line to set an audio file that will be played while the player is at the main menu. This file will continue playing into the game, until it is stopped or another file is played."
    new "## Palauta seuraava rivi takaisin ohjelmakoodiksi valitaksesi äänitiedoston, jota soitetaan pelaajan ollessa päävalikossa. Tämän tiedoston toisto jatkuu pelin alkaessa, kunnes se pysäytetään tai toinen tiedosto alkaa soimaan."

    # options.rpy:69
    old "## Transitions"
    new "## Siirtymät"

    # options.rpy:71
    old "## These variables set transitions that are used when certain events occur. Each variable should be set to a transition, or None to indicate that no transition should be used."
    new "## Nämä muuttujat asettavat erilaisia siirtymiä eri tapahhtumien kohdalla. Jokainen muuttuja tulee asettaa johonkin siirtymään, tai None mikäli siirtymää ei haluta käyttää."

    # options.rpy:75
    old "## Entering or exiting the game menu."
    new "## Pelivalikon avaaminen ja sulkeminen."

    # options.rpy:81
    old "## A transition that is used after a game has been loaded."
    new "## Siirtymä, jota käytetään kun peli on ladattu."

    # options.rpy:86
    old "## Used when entering the main menu after the game has ended."
    new "## Käytetään siirryttäessä päävalikkoon pelin päätyttyä."

    # options.rpy:91
    old "## A variable to set the transition used when the game starts does not exist. Instead, use a with statement after showing the initial scene."
    new "## Muuttujaa siirtymän valitsemiseksi pelin alkaessa ei ole olemassa. Sen sijaan, käytä with-väitettä näytettyäsi ensimmäisen kohtauksen."

    # options.rpy:96
    old "## Window management"
    new "## Ikkunanhallinta"

    # options.rpy:98
    old "## This controls when the dialogue window is displayed. If \"show\", it is always displayed. If \"hide\", it is only displayed when dialogue is present. If \"auto\", the window is hidden before scene statements and shown again once dialogue is displayed."
    new "## Tämä muokkaa dialogi-ikkunan näkyvyyttä. Arvon ollessa \"show\", ikkuna on aina näkyvissä. Mikäli se on \"hide\", ikkuna näkyy vain kun on dialogia mitä näyttää. Ja jos se on \"auto\", ikkuna ei ole näkyvissä ennen scene-lauseita ja näytetään kun dialogia on näytettävänä."

    # options.rpy:103
    old "## After the game has started, this can be changed with the \"window show\", \"window hide\", and \"window auto\" statements."
    new "## Pelin alettua, tätä voidaan muuttaa \"window show\", \"window hide\", ja \"window auto\" -lauseilla."

    # options.rpy:109
    old "## Transitions used to show and hide the dialogue window"
    new "## Siirtymät, joita käytetään dialogi-ikkunan näytössä ja piilotuksessa"

    # options.rpy:115
    old "## Preference defaults"
    new "## Asetusten oletusarvot"

    # options.rpy:117
    old "## Controls the default text speed. The default, 0, is infinite, while any other number is the number of characters per second to type out."
    new "## Asettaa tekstin näytön oletusnopeuden. Oletusarvo, 0, on ääretön (teksti näkyy välittömästi), kaikki muut positiiviset luvut asettavat näytettyjen merkkien lukumäärän sekunnissa."

    # options.rpy:123
    old "## The default auto-forward delay. Larger numbers lead to longer waits, with 0 to 30 being the valid range."
    new "## Oletusarvoinen automaattisen jatkamisen viive. Suuremmat luvut johtavatt pidempiin viiveisiin, tuetut arvot ovat väliltä 0-30."

    # options.rpy:129
    old "## Save directory"
    new "## Tallennuskansio"

    # options.rpy:131
    old "## Controls the platform-specific place Ren'Py will place the save files for this game. The save files will be placed in:"
    new "## Asettaa alustariippuvaisen sijainnin, johon Ren'Py tallentaa pelitallennukset. Tallennustiedostot tallennetaan kansioon:"

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
    new "## Tätä ei yleensä kannata muuttaa, ja jos muutetaan, sen tulee aina olla merkkijonoliteraali eikä ekspressio."

    # options.rpy:146
    old "## Icon ########################################################################'"
    new "## Ikoni #######################################################################'"

    # options.rpy:148
    old "## The icon displayed on the taskbar or dock."
    new "## Tehtäväpalkissa tai työpöydällä näkyvä ikoni."

    # options.rpy:153
    old "## Build configuration"
    new "## Jakeluasetukset"

    # options.rpy:155
    old "## This section controls how Ren'Py turns your project into distribution files."
    new "## Tämä osio ohjaa Ren'Py:n käyttäytymistä pelin jakeluiden kokoamisvaiheessa."

    # options.rpy:160
    old "## The following functions take file patterns. File patterns are case- insensitive, and matched against the path relative to the base directory, with and without a leading /. If multiple patterns match, the first is used."
    new "## Seuraavat funktiot vaativat tiedostonimimallin. Mallit ovat kirjasinkokoriippumattomia, ja niitä verrataan projektikansiosta riippuvaisina, joko alkavan /-merkin kanssa tai ilman. Jos useampi malli täsmää, käytetään ensimmäistä sopivaa."

    # options.rpy:165
    old "## In a pattern:"
    new "## Mallin syntaksi:"

    # options.rpy:167
    old "## / is the directory separator."
    new "## / on kansioiden erotin."

    # options.rpy:169
    old "## * matches all characters, except the directory separator."
    new "## * täsmää kaikkiin merkkeihin, paitsi kansion erottimeen."

    # options.rpy:171
    old "## ** matches all characters, including the directory separator."
    new "## ** täsmää kaikkiin merkkeihin, mukaan lukien kansion erottimeen."

    # options.rpy:173
    old "## For example, \"*.txt\" matches txt files in the base directory, \"game/**.ogg\" matches ogg files in the game directory or any of its subdirectories, and \"**.psd\" matches psd files anywhere in the project."
    new "## Esimerkiksi, \"*.txt\" täsmää kaikkiin txt-tiedostoihin projektikansiossa, \"game/**.ogg\" täsmää kaikkiin ogg-tiedostoihin game-kansiossa tai sen alakansioissa, ja \"**.psd\" täsmää kaikkiin, missä tahansa projektissa sijaitseviin psd-tiedostoihin."

    # options.rpy:177
    old "## Classify files as None to exclude them from the built distributions."
    new "## Luokittele tiedostot arvolla None jättääksesi ne pois kootuista jakeluista."

    # options.rpy:185
    old "## To archive files, classify them as 'archive'."
    new "## Arkistoidaksesi tiedostoja, luokittele ne arvolla 'archive'."

    # options.rpy:190
    old "## Files matching documentation patterns are duplicated in a mac app build, so they appear in both the app and the zip file."
    new "## Dokumentaatiotiedostot kloonautuvat mac-sovelluksissa, joten ne sisältyvät sekä sovelluksessa että zip-tiedostossa."

    # options.rpy:196
    old "## A Google Play license key is required to download expansion files and perform in-app purchases. It can be found on the \"Services & APIs\" page of the Google Play developer console."
    new "## Google Play -lisenssiavain vaaditaan jotta lisäosatiedostoja ja sovelluksen sisäisiä ostoja voidaan tukea. Sen voi löytää \"Services & APIs\"-sivulta Google Play -kehittäjäkonsolista."

    # options.rpy:203
    old "## The username and project name associated with an itch.io project, separated by a slash."
    new "## Kauttaviivan erottama käyttäjänimi ja itch.io-projektinimi."


translate finnish strings:

    # gui/game/options.rpy:31
    old "## Text that is placed on the game's about screen. Place the text between the triple-quotes, and leave a blank line between paragraphs."
    # Automatic translation.
    new "## Teksti, joka sijoitetaan pelin about-näyttöön. Sijoita teksti kolmoislauseiden väliin ja jätä kappaleiden väliin tyhjä rivi."

    # gui/game/options.rpy:47
    old "## These three variables control, among other things, which mixers are shown to the player by default. Setting one of these to False will hide the appropriate mixer."
    # Automatic translation.
    new "## Nämä kolme muuttujaa säätelevät muun muassa sitä, mitkä mikserit näytetään pelaajalle oletusarvoisesti. Jonkin näistä muuttujista asettaminen Falseen piilottaa kyseisen mikserin."

    # gui/game/options.rpy:82
    old "## Between screens of the game menu."
    # Automatic translation.
    new "## Pelivalikon näyttöjen välillä."

    # gui/game/options.rpy:152
    old "## Icon"
    # Automatic translation.
    new "## Kuvake"

    # gui/game/options.rpy:203
    old "## A Google Play license key is required to perform in-app purchases. It can be found in the Google Play developer console, under \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."
    # Automatic translation.
    new "## Google Play -lisenssiavain tarvitaan sovelluksen sisäisten ostojen tekemiseen. Se löytyy Google Play -kehittäjäkonsolista kohdasta \"Monetize\" > \"Monetization Setup\" > \"Licensing\"."

