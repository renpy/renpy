# File ini adalah dalam domain publik. Jangan ragu untuk memodifikasinya sebagai dasar
# Untuk layar Anda sendiri.

# Perhatikan bahwa banyak dari layar ini dapat diberikan argumen tambahan dalam masa depan.
# Penggunaan kwargs ** dalam daftar parameter memastikan kode Anda akan
# Pekerjaan di masa depan.

##############################################################################
# Say
#
# Layar yang digunakan untuk menampilkan dialog mode-adv.
# http://www.renpy.org/doc/html/screen_special.html#say
screen say(who, what, side_image=None, two_window=False):

    # Memutuskan apakah kita mau menggunakan varian satu jendela atau dua jendela.
    if not two_window:

        # Varian satu jendela.
        window:
            id "window"

            has vbox:
                style "say_vbox"

            if who:
                text who id "who"

            text what id "what"

    else:

        # Varian dua jendela.
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

    # Jika ada gambar samping, tampilkan di atas text.
    if side_image:
        add side_image
    else:
        add SideImage() xalign 0.0 yalign 1.0

    # Menggunakan menu cepat.
    use quick_menu


##############################################################################
# Pilihan
#
# Layar yang digunakan untuk menampilkan menu in-game
# http://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):

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
# Layar yang digunakan untuk menampilkan renpy.input()
# http://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):

    window style "input_window":
        has vbox

        text prompt style "input_prompt"
        input id "input" style "input_text"

    use quick_menu

##############################################################################
# Nvl
#
# Layar yang digunakan untuk menampilkan dialog mode-nvl dan menu
# http://www.renpy.org/doc/html/screen_special.html#nvl

screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            style "nvl_vbox"

        # Menampilkan dialog.
        for who, what, who_id, what_id, window_id in dialogue:
            window:
                id window_id

                has hbox:
                    spacing 10

                if who is not None:
                    text who id who_id

                text what id what_id

        # Menampilkan menu jika di di berikan.
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
# Menu Utama
#
# Layar yang digunakan untuk menampilkan menu utama saat pertamakali Ren'Py di jalankan
# http://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    # Ini memastikan layar menu yang lain di gantikan.
    tag menu

    # Background menu utama
    window:
        style "mm_root"

    # Tombol menu utama.
    frame:
        style_group "mm"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Mulai Game") action Start()
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Opsi") action ShowMenu("preferences")
        textbutton _("Bantuan") action Help()
        textbutton _("Keluar") action Quit(confirm=False)

init -2:

    # Make all the main menu buttons be the same size.
    style mm_button:
        size_group "mm"



##############################################################################
# Navigasi
#
# Layar yang termasuk dalam layar lainnya untuk menampilkan menu permainan
# Navigasi dan latar belakang.
# http://www.renpy.org/doc/html/screen_special.html#navigation
screen navigation():

    # Background menu permainan.
    window:
        style "gm_root"

    # The various buttons.
    frame:
        style_group "gm_nav"
        xalign .98
        yalign .98

        has vbox

        textbutton _("Kembali") action Return()
        textbutton _("Opsi") action ShowMenu("preferences")
        textbutton _("Simpan Game") action ShowMenu("save")
        textbutton _("Load Game") action ShowMenu("load")
        textbutton _("Menu Utama") action MainMenu()
        textbutton _("Bantuan") action Help()
        textbutton _("Keluar") action Quit()

init -2:

    # Membuat semua tombol navigasi dalam ukuran yang sama.
    style gm_nav_button:
        size_group "gm_nav"


##############################################################################
# Save, Load
#
# Layar yang memungkinkan pengguna untuk meload dan menyimpan permainan.
# http://www.renpy.org/doc/html/screen_special.html#save
# http://www.renpy.org/doc/html/screen_special.html#load

# Karena menyimpan dan meload sangat mirip, kami menggabungkan mereka ke dalam
# Satu layar, file_picker. Kami kemudian menggunakan layar file_picker
# untuk menciptakan load dan save yang simple.

screen file_picker():

    frame:
        style "file_picker_frame"

        has vbox

        # Tombol di atas yang memungkinkan pengguna memilih
        # halaman file.
        hbox:
            style_group "file_picker_nav"

            textbutton _("Sebelumnya"):
                action FilePagePrevious()

            textbutton _("Otomatis"):
                action FilePage("auto")

            textbutton _("Cepat"):
                action FilePage("quick")

            for i in range(1, 9):
                textbutton str(i):
                    action FilePage(i)

            textbutton _("Berikutnya"):
                action FilePageNext()

        $ columns = 2
        $ rows = 5

        # Menampilkan tabel slot file.
        grid columns rows:
            transpose True
            xfill True
            style_group "file_picker"

            # Menampilkan sepuluh slot file dari 1 - 10.
            for i in range(1, columns * rows + 1):

                # Setiap slot file adalah tombol.
                button:
                    action FileAction(i)
                    xfill True

                    has hbox

                    # Menambahkan screenshot.
                    add FileScreenshot(i)

                    $ file_name = FileSlotName(i, columns * rows)
                    $ file_time = FileTime(i, empty=_("Slot Kosong."))
                    $ save_name = FileSaveName(i)

                    text "[file_name]. [file_time!t]\n[save_name!t]"

                    key "save_delete" action FileDelete(i)


screen save():

    # Ini memastikan layar menu yang lain di gantikan.
    tag menu

    use navigation
    use file_picker

screen load():

    # Ini memastikan layar menu yang lain di gantikan.
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
# Preferensi
#
# Layar yang memungkinkan pengguna mengubah opsi/setting.
# http://www.renpy.org/doc/html/screen_special.html#prefereces

screen preferences():

    tag menu

    # Mengikutsertakan navigasi.
    use navigation

    # Menaruh kolom navigasi di tiga kolom lebar.
    grid 3 1:
        style_group "prefs"
        xfill True

        # Kolom kiri.
        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Display")
                textbutton _("Jendela") action Preference("display", "window")
                textbutton _("Layar Penuh") action Preference("display", "fullscreen")

            frame:
                style_group "pref"
                has vbox

                label _("Transisi")
                textbutton _("Semua") action Preference("transitions", "all")
                textbutton _("Mati") action Preference("transitions", "none")

            frame:
                style_group "pref"
                has vbox

                label _("Kecepatan Text")
                bar value Preference("text speed")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Joystick...") action Preference("joystick")


        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Loncati")
                textbutton _("Pesan Terlihat") action Preference("skip", "seen")
                textbutton _("Semua Pesan") action Preference("skip", "all")

            frame:
                style_group "pref"
                has vbox

                textbutton _("Mulai Loncati") action Skip()

            frame:
                style_group "pref"
                has vbox

                label _("Setelah Pilihan")
                textbutton _("Berhenti Loncati") action Preference("after choices", "stop")
                textbutton _("Tetap Loncati") action Preference("after choices", "skip")

            frame:
                style_group "pref"
                has vbox

                label _("Waktu Auto Forward")
                bar value Preference("auto-forward time")

                if config.has_voice:
                    textbutton _("Menunggu Untuk Suara") action Preference("wait for voice", "toggle")

        vbox:
            frame:
                style_group "pref"
                has vbox

                label _("Volume Musik")
                bar value Preference("music volume")

            frame:
                style_group "pref"
                has vbox

                label _("Volume Suara")
                bar value Preference("sound volume")

                if config.sample_sound:
                    textbutton _("Test"):
                        action Play("sound", config.sample_sound)
                        style "soundtest_button"

            if config.has_voice:
                frame:
                    style_group "pref"
                    has vbox

                    label _("Volume Percakapan")
                    bar value Preference("voice volume")

                    textbutton _("Pertahankan Percakapan") action Preference("voice sustain", "toggle")
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
# Layar yang menanyakan ya atau tidak kepada pengguna.
# http://www.renpy.org/doc/html/screen_special.html#yesno-prompt

screen yesno_prompt(message, yes_action, no_action):

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

            textbutton _("Ya") action yes_action
            textbutton _("Tidak") action no_action

    # Klik-kanan dan jawaban escape "Tidak/No"
    key "game_menu" action no_action

init -2:
    style yesno_button:
        size_group "yesno"

    style yesno_label_text:
        text_align 0.5
        layout "subtitle"


##############################################################################
# Menu Cepat
#
# Sebuah layar yang disertakan secara default layar say, dan menambahkan akses cepat ke
# Beberapa fungsi yang berguna.
screen quick_menu():

    # Menambahkan menucepat di dalam permainan.
    hbox:
        style_group "quick"

        xalign 1.0
        yalign 1.0

        textbutton _("Kembali") action Rollback()
        textbutton _("Simpan Game") action ShowMenu('save')
        textbutton _("Save.C") action QuickSave()
        textbutton _("Load.C") action QuickLoad()
        textbutton _("Lompati") action Skip()
        textbutton _("Lompati.C") action Skip(fast=True, confirm=True)
        textbutton _("Otomatis") action Preference("auto-forward", "toggle")
        textbutton _("Opsi") action ShowMenu('preferences')

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

