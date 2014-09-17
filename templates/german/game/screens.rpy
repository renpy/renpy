# Diese Datei ist frei zugänglich. Sie können sie gern modifizieren, um
# eine Basis für ihre eigenen Bildschirme zu schaffen.

##############################################################################
# ADV-Modus
#
# Der Bildschirm, der verwendet wird, um Dialog im ADV-Modus anzuzeigen.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # Standard für side_image und two_window
    default side_image = None
    default two_window = False

    # Entscheidung, ob wir die Variante für ein Fenster oder für zwei Fenster verwenden möchten.
    if not two_window:

        # Die Variante für ein Fenster.
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # Die Variante für zwei Fenster.
        vbox:
            style "say_two_window_vbox"

            if who:
                window:
                    style "say_who_window"

                    text who:
                        id "who"

            window:
                id "window"

                has vbox:
                    style "say_vbox"

                text what id "what"

    # Wenn ein "side image" vorhanden ist, wird es über dem Text angezeigt.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Verwendet das Schnellmenü.
    use quick_menu


##############################################################################
# Auswahl
#
# Der Bildschirm, der verwendet wird, um Auswahlmöglichkeiten im Spiel anzuzeigen.
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice:

    window:
        style "menu_window"
        xalign 0.5
        yalign 0.5

        vbox:
            style "menu"
            spacing 2

            for caption, action, chosen in items:

                if action:

                    button:
                        action action
                        style "menu_choice_button"

                        text caption style "menu_choice"

                else:
                    text caption style "menu_caption"

init -2 python:
    config.narrator_menu = True

    style.menu_window.set_parent(style.default)
    style.menu_choice.set_parent(style.button_text)
    style.menu_choice.clear()
    style.menu_choice_button.set_parent(style.button)
    style.menu_choice_button.xminimum = int(config.screen_width * 0.75)
    style.menu_choice_button.xmaximum = int(config.screen_width * 0.75)


##############################################################################
# Eingabe
#
# Der Bildschirm, der dafür genutzt wird, renpy.input() anzuzeigen.
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# NVL
#
# Der Bildschirm, der für den NVL-Modus verwendet wird.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Dialoganzeige.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Zeigt gegebenenfalls ein Menü an.
        if items:

            vbox:
                id "menu"

                for caption, action, chosen in items:

                    if action:

                        button:
                            style "nvl_menu_choice_button"
                            action action

                            text caption style "nvl_menu_choice"

                    else:

                        text caption style "nvl_dialogue"

    add SideImage() xalign 0.0 yalign 1.0

    use quick_menu

##############################################################################
# Hauptmenü
#
# Der Bildschirm, der verwendet wird, um das Hauptmenü anzuzeigen, wenn Ren'Py zum ersten Mal gestartet wird.
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # Dies stellt sicher, dass alle anderen Menübildschirme ersetzt werden.
    tag menu

    # Der Hintergrund des Hauptmenüs.
    window:
        style "mm_root"

    # Die Hauptmenü Schaltflächen.
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Start Game") action Start()
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit(confirm=False)

init -2 python:

    # Macht alle Hauptmenü Schaltflächen gleich groß.
    style.mm_button.size_group = "mm"


##############################################################################
# Navigation
#
# Der Bildschirm, der in anderen Menüs angezeigt wird, um die Navigation
# des Spielmenüs und den Hintergrund anzuzeigen.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # Der Hintergrund des Spielmenüs.
    window:
        style "gm_root"

    # Die verschiedenen Schaltflächen.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Return") action Return()
        textbutton _("Preferences") action ShowMenu("preferences")
        textbutton _("Save Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Main Menu") action MainMenu()
        textbutton _("Help") action Help()
        textbutton _("Quit") action Quit()

init -2 python:
    style.gm_nav_button.size_group = "gm_nav"


##############################################################################
# Save, Load
#
# Der Bildschirm, der es dem Benutzer ermöglicht, das Spiel zu speichern und zu laden.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Da das Speichern und Laden so ähnlich ist, kombinieren wir beides
# in einem einzigen Bildschirm: file_picker. Dann verwenden wir den "file_picker"
# Bildschirm für einfache Lade- und Speicherbildschirme.

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # Die oberen Schaltflächen ermöglichen es dem Benutzer,
        # eine Seite auszuwählen.
        hbox:
            style_group "file_picker_nav"

            textbutton _("Previous"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            textbutton _("Quick"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _("Next"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # Zeigt ein Raster von Speicherplätzen an.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Zeigt zehn Speicherplätze an, nummeriert von 1 - 10.
            for i in range(1, columns * rows + 1):

                # Jeder Speicherplatz ist eine Schaltfläche.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Fügt den Screenshot hinzu.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Empty Slot."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # Dies stellt sicher, dass alle anderen Menübildschirme ersetzt werden.
    tag menu

    use navigation
    use file_picker

screen load:

    # Dies stellt sicher, dass alle anderen Menübildschirme ersetzt werden.
    tag menu

    use navigation
    use file_picker

init -2 python:
    style.file_picker_frame = Style(style.menu_frame)

    style.file_picker_nav_button = Style(style.small_button)
    style.file_picker_nav_button_text = Style(style.small_button_text)

    style.file_picker_button = Style(style.large_button)
    style.file_picker_text = Style(style.large_button_text)



##############################################################################
# Einstellungen
#
# Der Bildschirm, der es dem Benutzer ermöglicht, die Einstellungen zu ändern.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # Fügt die Navigation hinzu.
    use navigation

    # Fügt die Navigationsspalten in einem dreiteiligen Raster hinzu.
    grid 3 1:
        style_group "prefs"
        xfill True

        # Die linke Spalte.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Window") action Preference("display", "window")
                textbutton _("Fullscreen") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transitions")
                textbutton _("All") action Preference("transitions", "all")
                textbutton _("None") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Text Speed")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Skip")
                textbutton _("Seen Messages") action Preference("skip", "seen")
                textbutton _("All Messages") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Begin Skipping") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("After Choices")
                textbutton _("Stop Skipping") action Preference("after choices", "stop")
                textbutton _("Keep Skipping") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Time")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Wait for Voice") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Music Volume")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Sound Volume")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Voice Volume")
                    bar value Preference("voice volume")

                    textbutton _("Voice Sustain") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Test"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2 python:
    style.pref_frame.xfill = True
    style.pref_frame.xmargin = 5
    style.pref_frame.top_margin = 5

    style.pref_vbox.xfill = True

    style.pref_button.size_group = "pref"
    style.pref_button.xalign = 1.0

    style.pref_slider.xmaximum = 192
    style.pref_slider.xalign = 1.0

    style.soundtest_button.xalign = 1.0


##############################################################################
# Ja/Nein Abfrage
#
# Der Bildschirm, der dem Benutzer eine Ja-oder-Nein-Frage stellt.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt:

    modal True

    window:
        style "gm_root"

    frame:
        style_group "yesno"

        xfill True
        xmargin .05
        ypos .1
        yanchor 0
        ypadding .05

        has vbox:
            xalign .5
            yalign .5
            spacing 30

        label _(message):
            xalign 0.5

        hbox:
            xalign 0.5
            spacing 100

            textbutton _("Yes") action yes_action
            textbutton _("No") action no_action

    # Rechtsklick und Escape antworten "Nein".
    key "game_menu" action no_action

init -2 python:
    style.yesno_button.size_group = "yesno"
    style.yesno_label_text.text_align = 0.5
    style.yesno_label_text.layout = "subtitle"


##############################################################################
# Schnellmenü
#
# Ein Menü, das im Standard "say screen" angezeigt wird und schnellen Zugriff
# auf verschiedene, nützliche Funktionen hinzufügt.
screen quick_menu:

    # Fügt ein Schnellmenü im Spiel hinzu.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Back") action Rollback()
        textbutton _("Save") action ShowMenu('save')
        textbutton _("Q.Save") action QuickSave()
        textbutton _("Q.Load") action QuickLoad()
        textbutton _("Skip") action Skip()
        textbutton _("F.Skip") action Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Prefs") action ShowMenu('preferences')

init -2 python:
    style.quick_button.set_parent('default')
    style.quick_button.background = None
    style.quick_button.xpadding = 5

    style.quick_button_text.set_parent('default')
    style.quick_button_text.size = 12
    style.quick_button_text.idle_color = "#8888"
    style.quick_button_text.hover_color = "#ccc"
    style.quick_button_text.selected_idle_color = "#cc08"
    style.quick_button_text.selected_hover_color = "#cc0"
    style.quick_button_text.insensitive_color = "#4448"
