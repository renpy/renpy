## Questo file contiene alcune delle opzioni che possono essere modificate per
## personalizzare il tuo gioco Ren'Py. Contiene soltanto le opzioni più
## comuni - le possibilità qui non menzionate sono ben più vaste.
##
## Le linee che iniziano con due simboli '#' sono commenti: rimuovere i simboli
## significa "decommentare" il testo, e visto che i commenti non rappresentano
## codice eseguibile causerà un errore di esecuzione.
## Le linee che iniziano con un solo simbolo '#' invece sono sì commenti ma
## contengono codice eseguibile che è stato messo da parte e che può essere
## documentato quando necessario.

init -1 python hide:

    ## Permettiamo l'uso degli strumenti dello sviluppatore? Questa variabile
    ## dovrebbe essere impostata a False prima del rilascio del gioco, così da
    ## impedire all'utente di imbrogliare usando i suddetti.
    config.developer = True

    ## Queste variabili controllano, rispettivamente la larghezza ed altezza
    ## dello schermo di gioco (la risoluzione)
    config.screen_width = 800
    config.screen_height = 600

    ## Questa variabile controlla il titolo della finestra (qualora usata)
    config.window_title = u"PROJECT_NAME"

    # Queste variabili controllano il nome e la versione del gioco, segnalate
    # durante i traceback ed altri log di debug
    config.name = "PROJECT_NAME"
    config.version = "0.0"

    #########################################
    # Temi

    ## Proviamo quindi a chiamare una funzione relativa ai temi.
    ## theme.roundrect è un tema che permette di mostrare i rettangoli
    ## con gli angoli arrotondati.
    ##
    ## La funzione accetta un numero di parametri che permettono di
    ## personalizzare lo schema di colore.

    theme.roundrect(

        ## Per widget si intendono gli elementi visivi di un GUI

        ## Il colore di un widget non in uso
        widget = "#003c78",

        ## Il colore di un widget in uso
        widget_hover = "#0050a0",

        ## Il colore del testo in un widget
        widget_text = "#c8ffff",

        ## Il colore del testo in un widget selezionato
        widget_selected = "#ffffc8",

        ## Il colore di un widget disabilitato
        disabled = "#404040",

        ## Il colore del testo di un widget disabilitato
        disabled_text = "#c8c8c8",

        ## Il colore delle label (etichetta) di informazione
        label = "#ffffff",

        ## Il colore del frame (cornice) che contiene widgets
        frame = "#6496c8",

        ## Se questa variabile è impostata a True, la finestra di
        ## gioco è arrotondata; altrimenti, la finestra è rettangolare
        rounded_window = False,

        ## Lo sfondo del menù principale, che può essere sia un colore
        ## in formato RGB preceduto da '#' che il nome di un file
        ## immagine con dimensioni preferibilmente coincidenti con
        ## la risoluzione del gioco
        mm_root = "#dcebff",

        ## Lo sfondo del menù di gioco, che può essere sia un colore
        ## in formato RGB preceduto da '#' che il nome di un file
        ## immagine con dimensioni preferibilmente coincidenti con
        ## la risoluzione del gioco
        gm_root = "#dcebff",

        ## Abbiamo finito con il tema. Passiamo a modificare lo stile
        )


    #########################################
    ## Queste impostazioni ti permetteranno di personalizzare la
    ## finestra contenente il dialogo e la narrazione sostituendola
    ## con un immagine.

    ## Lo sfondo della finestra. In un Frame, i due numeri sono le
    ## dimensioni dei bordi sinistro/destro e alto/basso, rispettivamente
    # style.window.background = Frame("frame.png", 12, 12)

    ## Il margine è lo spazio che circonda la finestra e sul quale lo sfondo
    ## non viene disegnato
    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## L'imbottitura (padding) è lo spazio all'interno della finestra e sul
    ## quale lo sfondo viene disegnato
    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## Questa variabile rappresenta l'altezza minima della finestra, margine
    ## ed imbottitura compresi
    # style.window.yminimum = 250


    #########################################
    ## Questo ti permette di cambiare il posizionamento del menù principale.

    ## Un displayable é un oggetto visibile all'utente.

    ## Il posizionamento funziona così: troviamo un punto di ancora (anchor)
    ## nel displayable ed un punto di posizione (pos) sullo schermo e
    ## dopo di chè posizioniamo il displayable così da fare coincidere i due
    ## punti.

    ## I punti di anchor/pos possono essere forniti come numeri interi o a
    ## virgola mobile. Se intero, il numero viene interpretato come il numero
    ## di pixel di distanza dall'angolo in alto a sinistra. Se a virgola
    ## mobile, il numero viene interpretato come una frazione della grandezza
    ## del displayable o dello schermo.

    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## Queste variabili ti permettono di personalizzare il font predefinito
    ## usato per il testo in Ren'Py.

    ## Il file contenente il font predefinito
    # style.default.font = "DejaVuSans.ttf"

    ## La grandezza predefinita del testo
    # style.default.size = 22

    ## Nota che queste cambiano solo la grandezza di alcune porzioni di testo e
    ## che altri pulsanti hanno il loro stile indipendente.


    #########################################
    ## Queste impostazioni ti permettono di cambiare alcuni dei suoni usati da
    ## Ren'Py.

    ## Impostala a False se il gioco non ha alcun effetto audio
    config.has_sound = True

    ## Impostala a False se il gioco non ha alcuna musica
    config.has_music = True

    ## Impostala a False se il gioco ha doppiaggio
    config.has_voice = False

    ## Suoni usati quando i pulsanti e le imagemap sono clickati
    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Suoni usati all'entrata/uscita dal menù di gioco
    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## Suono di prova, usato per controllare il volume
    # config.sample_sound = "click.wav"

    ## Musica riprodotta in sottofondo al menù principale
    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Aiuto

    ## Questa variabile ti permette di configurare le opzioni di aiuto nei menu
    ## di Ren'Py.
    ## Può essere:
    ## - Una label nello script che viene chiamata per mostrare l'aiuto
    ## - Il nome di un file relativo alla cartella di base e che viene aperto
    ##   in un browser
    ## - None, per disabilitare l'aiuto
    config.help = "README.html"


    #########################################
    ## Transizioni.

    ## Usata quando si passa dal gioco al menù di gioco
    config.enter_transition = None

    ## Usata quando si passa dal menù di gioco al gioco
    config.exit_transition = None

    ## Usata quando si passa tra le schermate del menù di gioco
    config.intra_transition = None

    ## Usata quando si passa dal menù principale al menù di gioco
    config.main_game_transition = None

    ## Usata quando si passa dal gioco al menù principale
    config.game_main_transition = None

    ## Usata quando si passa dallo splash screen al menù principale
    config.end_splash_transition = None

    ## Usata quando si passa dalla fine del gioco al menù principale
    config.end_game_transition = None

    ## Usata quando il gioco viene caricato
    config.after_load_transition = None

    ## Usata quando la finestra viene mostrata
    config.window_show_transition = None

    ## Usata quando la finestra viene nascosta
    config.window_hide_transition = None

    ## Usata quando si mostra del testo in modalità NLV subito dopo del
    ## testo in modalità ADV
    config.adv_nvl_transition = dissolve

    ## Usata quando si mostra del testo in modalità ADV subito dopo del
    ## testo in modalità NVL
    config.nvl_adv_transition = dissolve

    ## Usata quando yesno viene mostrato
    config.enter_yesno_transition = None

    ## Usata quando yesno viene nascosto
    config.exit_yesno_transition = None

    ## Usato quando si inizia un replay
    config.enter_replay_transition = None

    ## Usato quando si finisce un replay
    config.exit_replay_transition = None

    ## Usato quando l'immagine viene cambiata da un comando "say" con attributi
    ## di immagine
    config.say_attribute_transition = None

    #########################################
    ## Questo è il nome della cartella dove i dati di gioco vengono salvati.
    ## È importante che venga impostato il più presto possibile così da
    ## permettere al codice di inizializzazione di trovare i dati persistenti.
python early:
    config.save_directory = "PROJECT_NAME-UNIQUE"

init -1 python hide:
    #########################################
    ## Valori predefiniti delle Preferenze.

    ## Nota: Queste opzioni vengono processate soltanto durante la prima
    ## esecuzione del gioco. Per ripetere l'esecuzione,
    ## cancella il gioco/i salvataggi/i dati persistenti.

    ## Modalità a schermo intero?
    config.default_fullscreen = False

    ## Velocità di scorrimento del testo predefinito. 0 rappresenta l'infinità
    config.default_text_cps = 0

    ## Tempo di auto-forward predefinito
    config.default_afm_time = 10

    #########################################
    ## Inserire altre personalizzazioni qui sotto.
