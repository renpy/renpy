# Questo file è nel pubblico dominio - modificalo liberamente per le tue scene.

##############################################################################
# Say
#
# Schermo usato per mostrare il dialogo in modalità ADV
# http://www.renpy.org/doc/html/screen_special.html#say
screen say:

    # Valori predefiniti per side_image e two_window
    default side_image = None
    default two_window = False

    # Decidi se usare la variante ad una o due finestre
    if not two_window:

        # Ad una finestra
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # A due finestre
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

    # Se presente un'immagine laterale, mostrala sopra il testo
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Usa il menù rapido
    use quick_menu


##############################################################################
# Choice
#
# Schermo usato per mostrare i menù all'interno del gioco.
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

init -2:
    $ config.narrator_menu = True

    style menu_window is default

    style menu_choice is button_text:
        clear

    style menu_choice_button is button:
        xminimum int(config.screen_width * 0.75)
        xmaximum int(config.screen_width * 0.75)


##############################################################################
# Input
#
# Schermo usato per mostrare renpy.input().
# http://www.renpy.org/doc/html/screen_special.html#input

screen input:

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

###############################################################################
# Nvl
#
# Schermo usato per dialoghi in modalità NVL e menù.
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl:

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Mostra dialogo
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Mostra menù, se fornito
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
# Main Menu
#
# Schermo usato per mostrare il menù principale all'avvio di Ren'Py
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu:

    # Sostituisce altri eventuali menù
    tag menu

    # Sfondo del menù
    window:
        style "mm_root"

    # Pulsanti del menù
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Inizia Partita") action Start()
        textbutton _("Carica Partita") action ShowMenu("load")
        textbutton _("Preferenze") action ShowMenu("preferences")
        textbutton _("Aiuto") action Help()
        textbutton _("Esci") action Quit(confirm=False)

init -2:

    # Fai avere a tutti i pulsanti del menù principale la stessa dimensione
    style mm_button:
        size_group "mm"



##############################################################################
# Navigation
#
# Schermo incluso da altri schermi per mostrare la navigazione e lo sfondo
# del menù di gioco
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation:

    # Lo sfondo del menù di gioco
    window:
        style "gm_root"

    # I vari pulsanti
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Ritorna") action Return()
        textbutton _("Preferenze") action ShowMenu("preferences")
        textbutton _("Salva Partita") action ShowMenu("save")
        textbutton _("Carica Partita") action ShowMenu("load")
        textbutton _("Menù Principale") action MainMenu()
        textbutton _("Aiuto") action Help()
        textbutton _("Esci") action Quit()

init -2:

    # Fai avere a tutti i pulsanti del menù di gioco la stessa dimensione
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# Schermi che permettono all'utente di salvare e caricare la partita.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Visto che salvare e caricare sono simili, li combiniamo in un singolo schermo
# chiamato file_picker.

screen file_picker:

    frame:
        style "file_picker_frame"

        has vbox

        # I pulsanti in alto permettono all'utente di scegliere una pagina di
        # file
        hbox:
            style_group "file_picker_nav"

            textbutton _("Precedente"):
                action FilePagePrevious()

            textbutton _("Auto"):
                action FilePage("auto")

            textbutton _("Veloce"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _("Successivo"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # Mostra una griglia di slot per file
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Mostra dieci slot per file, numerati da 1 a 10
            for i in range(1, columns * rows + 1):

                # Ogni slot per file è un pulsante
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Aggiungi lo screenshot
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Slot Vuoto."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save:

    # Sostituisce altri eventuali menù
    tag menu

    use navigation
    use file_picker

screen load:

    # Sostituisce altri eventuali menù
    tag menu

    use navigation
    use file_picker

init -2:
    style file_picker_frame is menu_frame
    style file_picker_nav_button is small_button
    style file_picker_nav_button_text is small_button_text
    style file_picker_button is large_button
    style file_picker_text is large_button_text


##############################################################################
# Preferences
#
# Schermo che permette all'utente di cambiare le preferenze
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences:

    tag menu

    # Includi navigazione
    use navigation

    # Disponi le colonne di navigazione in una griglia di larghezza tre
    grid 3 1:
        style_group "prefs"
        xfill True

        # La colonna sinistra
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Schermo")
                textbutton _("Finestra") action Preference("display", "window")
                textbutton _("Schermo Intero") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transizioni")
                textbutton _("Tutte") action Preference("transitions", "all")
                textbutton _("Nessuna") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Velocità Testo")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Salta")
                textbutton _("Messagi Letti") action Preference("skip", "seen")
                textbutton _("Tutti i Messaggi") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Inizia a Saltare") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("Dopo le Scelte")
                textbutton _("Smetti di Saltare") action Preference("after choices", "stop")
                textbutton _("Continua a Saltare") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Auto-Forward Tempo")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Aspetta Voce") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Volume Musica")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Volume Suono")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Volume Voce")
                    bar value Preference("voice volume")

                    textbutton _("Sustain Voce") action Preference("voice sustain", "toggle")
                    if config.sample_voice:
                        textbutton _("Test"):
                            action Play("voice", config.sample_voice)
                            style "soundtest_button"

init -2:
    style pref_frame:
        xfill True
        xmargin 5
        top_margin 5

    style pref_vbox:
        xfill True

    style pref_button:
        size_group "pref"
        xalign 1.0

    style pref_slider:
        xmaximum 192
        xalign 1.0

    style soundtest_button:
        xalign 1.0


##############################################################################
# Yes/No Prompt
#
# Schermo che chiede all'utente una domanda "si o no"
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

            textbutton _("Si") action yes_action
            textbutton _("No") action no_action

    # Click destro ed ESC rispondono "no"
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# Quick Menu
#
# Uno schermo incluso dallo schermo "say" di default e che permette accesso
# rapido a diverse funzioni.
screen quick_menu:

    # Aggiungi un menù veloce accessibile durante il gioco
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Indietro") action Rollback()
        textbutton _("Salva") action ShowMenu('save')
        textbutton _("Salva Veloce") action QuickSave()
        textbutton _("Carica Veloce") action QuickLoad()
        textbutton _("Salta") action Skip()
        textbutton _("Salta Veloce") action Skip(fast=True, confirm=True)
        textbutton _("Auto") action Preference("auto-forward", "toggle")
        textbutton _("Preferenze") action ShowMenu('preferences')

init -2:
    style quick_button:
        is default
        background None
        xpadding 5

    style quick_button_text:
        is default
        size 12
        idle_color "#8888"
        hover_color "#ccc"
        selected_idle_color "#cc08"
        selected_hover_color "#cc0"
        insensitive_color "#4448"
