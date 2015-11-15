## Diese Datei enthält einige Optionen, die verändert werden können,
## um Ihr Ren'Py Spiel anzupassen. Sie enthält nur die häufigsten Optionen.
## Es gibt ziemlich viel, was angepasst werden kann.
##
## Zeilen, die mit zwei '#'-Zeichen beginnen, sind Kommentare und sollten
## nicht entfernt werden. Zeilen, die mit einem '#'-Zeichen beginnen,
## sind deaktivierte Codezeilen und können aktiviert werden, indem das
## Zeichen entfernt wird.

init -1 python hide:

    ## Sollen wir die Entwicklertools aktivieren? Das sollte auf
    ## "False" gesetzt werden, bevor das Spiel veröffentlicht wird,
    ## damit der Spieler mithilfe der Entwicklertools nicht schummeln kann.

    config.developer = True

    ## Hiermit wird die Breite und Höhe des Bildschirms festgelegt.

    config.screen_width = 800
    config.screen_height = 600

    ## Hiermit wird der Titel des Fensters festgelegt, wenn Ren'Py im
    ## Fenstermodus läuft.

    config.window_title = u"Ein Ren'Py Spiel"

    # Hiermit wird der Name und die Version des Spiels festgelegt,
    # die in Tracebacks und anderen Protokollen festgehalten werden.
    config.name = "Ein Ren'Py Spiel"
    config.version = "0.0"

    #########################################
    # Themes

    ## Hiermit lässt sich die Theme-Funktion anpassen. "themes.roundrect" ist
    ## ein Theme, das abgerundete Rechtecken verwendet. Es ist das einzige
    ## Theme, das derzeit unterstützt wird.
    ##
    ## Die Theme-Funktion läuft mit verschiedenen Parametern, die
    ## das Farbschema anpassen können.

    theme.roundrect(

        ## Die Farbe von einer Widget-Oberfläche.
        widget = "#003c78",

        ## Die Farbe von einer ausgewählter Widget-Oberfläche.
        widget_hover = "#0050a0",

        ## Die Farbe vom Text in einem Widget.
        widget_text = "#c8ffff",

        ## Die Farbe vom Text in einem ausgewählten Widget. (Zum
        ## Beispiel der derzeitige Wert einer Einstellung.)
        widget_selected = "#ffffc8",

        ## Die Farbe von einer deaktivierten Widget-Oberfläche.
        disabled = "#404040",

        ## Die Farbe eines deaktivierten Widget-Texts.
        disabled_text = "#c8c8c8",

        ## Die Farbe von Informations-Labels.
        label = "#ffffff",

        ## Die Farbe von einer Schaltfläche, die Widgets enthält.
        frame = "#6496c8",

        ## Wenn dies auf "True" steht, ist das Fenster im Spiel abgerundet.
        ## Wenn es auf "False" steht, ist das Fenster im Spiel rechteckig.
        rounded_window = False,

        ## Der Hintergrund des Hauptmenüs. Das kann eine Farbe sein,
        ## die mit '#' beginnt oder ein Dateiname. Letzteres sollte
        ## sich auf die vollständige Höhe und Breite des Bildschirms erstrecken.
        mm_root = "#dcebff",

        ## Der Hintergrund des Spielmenüs. Das kann eine Farbe sein,
        ## die mit '#' beginnt oder ein Dateiname. Letzteres sollte
        ## sich auf die vollständige Höhe und Breite des Bildschirms erstrecken.
        gm_root = "#dcebff",

        ## Und das war alles zum Theme. Das Theme kann durch verschiedene
        ## Stile weiter angepasst werden. Wenn wir dies ändern möchten,
        ## können wir das weiter unten tun.
        )


    #########################################
    ## Diese Einstellungen lassen Sie das Fenster anpassen, welches Dialoge
    ## und Erzählungen enthält. Sie können es mit einer Grafik ersetzen.

    ## Der Hintergrund des Fensters. Im "Frame" sind die zwei Nummern
    ## jeweils die Größe des linken/rechten und des oberen/unteren
    ## Abstands.

    # style.window.background = Frame("frame.png", 12, 12)

    ## Der Rand ist der Freiraum, der das Fenster umgibt und wo der Hintergrund
    ## nicht zu sehen ist.

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## "Padding" ist der Raum innerhalb des Fenster, wo der
    ## Hintergrund zu sehen ist.

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## Dies ist die Mindesthöhe des Fensters, inklusive des Randes
    ## und "Padding".

    # style.window.yminimum = 250


    #########################################
    ## Hiermit lässt sich die Platzierung des Hauptmenüs ändern.

    ## Um die Platzierung vorzunehmen, suchen wir uns einen
    ## Ankerpunkt auf einer anzeigbaren Position auf dem
    ## Bildschirm. Dann platzieren wir diesen so, damit
    ## beide Punkte an derselben Stelle sind.

    ## Ein Ankerpunkt kann als "integer" oder ein "floating point"
    ## Nummer angeben werden. Als "integer" wird die Nummer als eine
    ## Pixelanzahl von der oberen linken Ecke aus interpretiert. Als "floating point",
    ## wird die Nummer als ein Bruchteil der Grö0e der anzeigbaren
    ## Position oder des Bildschirms interpretiert.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## Hiermit können Sie die Standard-Schriftart einstellen, die Ren'Py für den Text verwendet.

    ## Die Datei, die die Standard-Schriftart enthält.

    # style.default.font = "DejaVuSans.ttf"

    ## Die Standardgröße des Texts.

    # style.default.size = 22

    ## Bedenken Sie, dass dies nur die Größe von einigen Texten anpassen kann.
    ## Andere Schaltflächen haben ihren eigenen Stile.


    #########################################
    ## Mit diesen Einstellungen können Sie die Soundeffekte anpassen, die
    ## Ren'Py verwendet.

    ## Stellen Sie dies auf "False", wenn das Spiel keine Soundeffekte bietet.

    config.has_sound = True

    ## Stellen Sie dies auf "False", wenn das Spiel keine Musik bietet.

    config.has_music = True

    ## Stellen Sie dies auf "True", wenn das Spiel Sprachausgabe bietet.

    config.has_voice = False

    ## Soundeffekte, die verwendet werden, wenn auf Schaltflächen oder "Imagemaps" geklickt wird.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Soundeffekte, die verwendet werden, wenn Sie das Spielmenü aufrufen oder verlassen.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## Ein Beispiel-Soundeffekt, der abgespielt werden kann, um die Lautstärke zu testen.

    # config.sample_sound = "click.wav"

    ## Musik, die abgespielt wird, während sich der Benutzer im Hauptmenü befindet.

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Hilfe.

    ## Hiermit lässt sich die Einstellung der Hilfeoption in den Ren'Py Menüs einstellen.
    ## Das könnte sein:
    ## - Ein Label im Skript, wobei zum Label gesprungen wird,
    ##   um dem Benutzer die Hilfe anzuzeigen.
    ## - Eine Datei, die sich im Hauptverzeichnis befinden und die dann
    ##   in einem Browser geöffnet wird.
    ## - None, um die Hilfe zu deaktivieren.
    config.help = "README.html"


    #########################################
    ## Übergänge.

    ## Beim Aufrufen des Spielmenüs aus dem Spiel heraus.
    config.enter_transition = None

    ## Beim Verlassen des Spielmenüs zurück ins Spiel.
    config.exit_transition = None

    ## Beim Wechsel zwischen Menüs im Spielmenü.
    config.intra_transition = None

    ## Beim Aufrufen des Spielmenüs aus dem Hauptmenü heraus.
    config.main_game_transition = None

    ## Beim Zurückkehren zum Hauptmenü aus dem Spiel heraus.
    config.game_main_transition = None

    ## Beim Aufrufen des Hauptmenüs vom "Splashscreen".
    config.end_splash_transition = None

    ## Beim Aufrufen des Hauptmenüs, nachdem das Spiel beendet wurde.
    config.end_game_transition = None

    ## Beim Laden eines Spiels.
    config.after_load_transition = None

    ## Beim Aufrufen des Fensters.
    config.window_show_transition = None

    ## Beim Verbergen des Fensters.
    config.window_hide_transition = None

    ## Beim Anzeigen des NVL-Modus direkt nach dem ADV-Modus.
    config.adv_nvl_transition = dissolve

    ## Beim Anzeigen des ADV-Modus direkt nach dem NVL-Modus.
    config.nvl_adv_transition = dissolve

    ## Beim Aufrufen der Ja/Nein Abfrage.
    config.enter_yesno_transition = None

    ## Beim Verlassen der Ja/Nein Abfrage.
    config.exit_yesno_transition = None

    ## Beim Aufrufen einer Wiederholung.
    config.enter_replay_transition = None

    ## Beim Verlassen einer Wiederholung.
    config.exit_replay_transition = None

    ## Beim Wechsel einer Grafik mit einem "say statement" und "image attributes".
    config.say_attribute_transition = None

    #########################################
    ## Dies ist der Name des Verzeichnisses, wo die Spieldaten gelagert
    ## werden. (Dies muss früh festgelegt werden, bevor ein anderer "init code"
    ## aufgerufen wird, damit die persistenten Informationen im "init code" gefunden werden können.)
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## Standardwerte für Einstellungen.

    ## Anmerkung: Diese Optionen werden nur beim ersten Start
    ## übernommen. Damit sie ein zweites Mal übernommen werden,
    ## löschen Sie game/saves/persistent.

    ## Soll das Spiel im Vollbildmodus starten?

    config.default_fullscreen = False

    ## Die Standardzeit für die Textgeschwindigkeit in Buchstaben pro Sekunde. 0 bedeutet ohne Zeitverzögerung.

    config.default_text_cps = 0

    ## Die Standardzeit für den automatischen Vorlauf.

    config.default_afm_time = 10

    #########################################
    ## Weitere Anpassungen können hier eingefügt werden.
