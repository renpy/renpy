## File ini mengandung beberapa opsi yang dapat mengubah dan mengkustomisasi
## permainan Ren'Py mu. Ini hanya berisi opsi yang paling sering di gunakan...
## Masih ada banyak lagi yang dapat kamu lakukan.
##
## Line yang di awali dengan dua tanda '#' Contoh : '##'
## Adalah komentar dan kamu tidak seharus nya menghilangkan nya.
## Line dengan satu tanda '#' adalah kode yang di komentari / di matikan, dan kamu dapat menyalakan nya kembali
## Dengan menghapus tanda '#' jika di perlukan.

init -1 python hide:

    ## Ini mengendalikan panjang dan lebar dari layar.

    config.screen_width = 800
    config.screen_height = 600

    ## Ini mengatur nama jendela saat Ren'Py
    ## Menjalankan program nya.

    config.window_title = u"NAMA_PROYEK"

    # Ini mengendalikan nama dan versi game, yang di laporkan di
    # Traceback dan log debug lainnya
    config.name = "NAMA_PROYEK"
    config.version = "0.0"

    #########################################
    # Tema

    ## Kita ingin memanggil fungsi tema. theme.roundrect adalah
    ## tema yang memiliki fitur penggunaan persegi panjang bulat.
    ##
    ## Fungsi tema mengambil sejumlah parameter
    ## yang dapat menyesuaikan skema warna.

    theme.roundrect(

        ## Warna dari widget yang idle.
        widget = "#003c78",

        ## Warna dari widget yang di fokus.
        widget_hover = "#0050a0",

        ## Warna text di widget.
        widget_text = "#c8ffff",

        ## Warna dari text di widget yang di pilih. (Sbg
        ## contoh, nilai sekarang dari preferensi.)
        widget_selected = "#ffffc8",

        ##Warna dari widget yang dimatikan
        disabled = "#404040",

        ##Warna dari text widget yang dimatikan
        disabled_text = "#c8c8c8",

        ##Warna label informasi
        label = "#ffffff",

        ## The color of a frame containing widgets. Warna frame yang berisi widget
        frame = "#6496c8",

        ## Jika ini 'True' jendela in-game akan bulat,
        ## Jika 'False' Jendela in-game akan kotak.
        rounded_window = False,

        ## Latar belakang menu utama. Ini bisa menjadi warna yang diawali dengan '#',
        ## atau nama file gambar.
        ## Yang terakhir ini harus mengambil tinggi penuh dan lebar layar.
        mm_root = "#dcebff",

        ##Latar belakang menu game. Ini bisa menjadi warna
        ##dimulai dengan '#', atau nama file gambar.
        ##Yang terakhir ini harus mengambil tinggi penuh dan lebar layar.
        gm_root = "#dcebff",

        ## Dan kita sudah selesai dengan tema. tema akan menyesuaikan dengan
        ## berbagai gaya, jadi, jika kita ingin mengubahnya, kita harus
        ## melakukannya di bawah ini.
        )


    #####################################################################
    ##Pengaturan ini memungkinkan Anda menyesuaikan jendela yang berisi
    ##dialog dan narasi, dengan menggantinya dengan gambar.

    ##Latar belakang jendela. Dalam Frame, dua angka
    ##adalah ukuran kiri / kanan dan atas / bawah perbatasan,
    ##masing-masing.

    # style.window.background = Frame("frame.png", 12, 12)

    ## 'Margin' Adalah jarak yang mengelilingi jendela, yang dimana
    ## latar belakang tidak di gambar

    # style.window.left_margin = 6
    # style.window.right_margin = 6
    # style.window.top_margin = 6
    # style.window.bottom_margin = 6

    ## 'Padding' Adalah jarak di dalam jendela, yang dimana
    ## latar belakang tidak di gambar

    # style.window.left_padding = 6
    # style.window.right_padding = 6
    # style.window.top_padding = 6
    # style.window.bottom_padding = 6

    ## ## Ini adalah tinggi mimimal jendela, termasuk 'Margins' dan
    ## 'Padding'.

    # style.window.yminimum = 250


    ###################################################################
    ##Hal ini memungkinkan Anda mengubah penempatan menu utama.

    ##Cara penempatan bekerja adalah bahwa kita menemukan titik anchor
    ##di dalam dapat ditampilkan, dan titik posisi (pos) pada
    ##layar. Kami kemudian tempatkan dapat ditampilkan sehingga dua poin
    ##di tempat yang sama.

    ##Jangkar / pos dapat diberikan sebagai integer atau floating point
    ##jumlah. Jika integer, jumlah ini ditafsirkan sebagai angka
    ##pixel dari pojok kiri atas. Jika floating point,
    ##jumlah ini ditafsirkan sebagai sebagian kecil dari ukuran
    ##dapat ditampilkan atau layar.


    # style.mm_menu_frame.xpos = 0.5
    # style.mm_menu_frame.xanchor = 0.5
    # style.mm_menu_frame.ypos = 0.75
    # style.mm_menu_frame.yanchor = 0.5


    #########################################
    ## Memungkinkan kamu mengganti font bawaan yang di gunakan Ren'Py.

    ## File yang berisi font bawaan.

    # style.default.font = "DejaVuSans.ttf"

    ## Ukuran Text.

    # style.default.size = 22

    ## Catatan ini hanya mengubah ukuran beberapa text
    ## Tombol lain mempunyai gaya tersendiri.


    #########################################
    ## Pengaturan ini memungkinkan kamu untuk mengubah
    ## beberapa suara yang di gunakan oleh Ren'Py.

    ## Set ke 'False' jika game tidak memiliki efek suara sama sekali.

    config.has_sound = True

    ## Set ke 'False' jika game tidak memiliki efek musik sama sekali.

    config.has_music = True

    ## Set ke 'True' jika game memiliki pengisi suara / aktor.

    config.has_voice = False

    ## Suara yang digunakan ketika tombol dan imagemap di klik.

    # style.button.activate_sound = "click.wav"
    # style.imagemap.activate_sound = "click.wav"

    ## Suara yang digunakan ketika memasuki/keluar dari menu permainan.

    # config.enter_sound = "click.wav"
    # config.exit_sound = "click.wav"

    ## Suara sample yang dapat di putar ketika mengetes volume efek.

    # config.sample_sound = "click.wav"

    ## Musik yang di mainkan pada saat pemain berada di main menu.

    # config.main_menu_music = "main_menu_theme.ogg"


    #########################################
    ## Bantuan.

    ## Ini memungkinkan kamu untuk mengganti opsi bantuan di menu Ren'Py.
    ## Dapat berisi:
    ## - Label di script, yang dimana label tersebut di panggil
    ##   untuk menunjukkan bantuan ke pengguna.
    ## - Namafile yang relatif di direktori dasar , yang dimana terbuka di
    ##   peramban web.
    ## - None, Untuk mematikan bantuan.
    config.help = "README.html"


    #########################################
    ## Transisi

    ## Digunakan ketika memasuki menu permainan dari game.
    config.enter_transition = None

    ## Digunakan ketika keluar dari menu permainan ke game.
    config.exit_transition = None

    ## Digunakan antara layar dan menu permainan.
    config.intra_transition = None

    ## Digunakan ketika masuk ke menu permainan dari menu utama.
    config.main_game_transition = None

    ## Digunakan ketika kembali ke menu utama dari permainan.
    config.game_main_transition = None

    ## Digunakan ketika memasuki menu utama dari layar splash.
    config.end_splash_transition = None

    ## Digunakan ketika memasuki menu utama ketika permainan telah usai.
    config.end_game_transition = None

    ## Digunakan setelah game di load.
    config.after_load_transition = None

    ## Digunakan ketika jendela di perlihatkan.
    config.window_show_transition = None

    ## Digunakan ketika jendela di sembunyikan.
    config.window_hide_transition = None

    ## Digunakan ketika menampilkan text mode-NVL secara langsung setelah text mode-ADV.
    config.adv_nvl_transition = dissolve

    ## Digunakan ketika menampilkan text mode-ADV secara langsung setelah text mode-NVL.
    config.nvl_adv_transition = dissolve

    ## Digunakan ketika yatidak di tampilkan.
    config.enter_yesno_transition = None

    ## Digunakan ketika yatidak di sembunyikan.
    config.exit_yesno_transition = None

    ## Digunakan ketika memasuki replay.
    config.enter_replay_transition = None

    ## Digunakan ketika keluar replay.
    config.exit_replay_transition = None

    ## Digunakan ketika gambar di ganti oleh pernyataan dengan atribut gambar.
    config.say_attribute_transition = None

    #########################################
    ## Ini nama dari direktori dimana data permainan di simpan
    ## (Ini perlu diatur lebih awal, sebelum kode init lainnya
    ## dijalankan, sehingga informasi yang terus-menerus dapat ditemukan dengan kode init.)
python early:
    config.save_directory = "NAMA_PROYEK_UNIK"

init -1 python hide:
    #########################################
    ## Nilai default dari Preferences.

    ## Catatan : Ini hanya dijalankan pada saat pertama game di jalankan
    ## Untuk membuat nya jalan untuk ke duakali, hapus
    ## game/saves/persistent

    ## Apa kita harus berjalan di mode layar penuh?

    config.default_fullscreen = False

    ## Kecepatan bawaan text di karakter per detik, 0 adalah infiniti

    config.default_text_cps = 0

    ## Pengaturan bawaan waktu auto-forward.

    config.default_afm_time = 10

    #########################################
    ## Kustomisasi yang lain dapat di mulai di sini.
